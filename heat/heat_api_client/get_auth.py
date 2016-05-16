#!/usr/bin/env python

import logging

import requests

try:
    import json
except ImportError:
    import simplejson as json

from six.moves.urllib import parse

from novaclient import api_versions
from novaclient import exceptions
from novaclient import utils

class HTTPClient(object):
    USER_AGENT = 'python-novaclient'

    def __init__(self, user, password, projectid=None, auth_url=None,
                 insecure=False, timeout=None, proxy_tenant_id=None,
                 proxy_token=None, region_name=None,
                 endpoint_type='publicURL', service_type=None,
                 service_name=None, volume_service_name=None,
                 timings=False, bypass_url=None,
                 os_cache=False, no_cache=True,
                 http_log_debug=False, auth_system='keystone',
                 auth_plugin=None, auth_token=None,
                 cacert=None, tenant_id=None, user_id=None,
                 connection_pool=False, api_version=None, version=None):
        self.user = user
        self.user_id = user_id
        self.password = password
        self.projectid = projectid
        self.tenant_id = tenant_id
        self.api_version = api_version or api_versions.APIVersion()


        # This will be called by #_get_password if self.password is None.
        # EG if a password can only be obtained by prompting the user, but a
        # token is available, you don't want to prompt until the token has
        # been proven invalid
        self.password_func = None

        if auth_system and auth_system != 'keystone' and not auth_plugin:
            raise exceptions.AuthSystemNotFound(auth_system)

        if not auth_url and auth_system and auth_system != 'keystone':
            auth_url = auth_plugin.get_auth_url()
            if not auth_url:
                raise exceptions.EndpointNotFound()
        self.auth_url = auth_url.rstrip('/') if auth_url else auth_url
        self.version = version
        self.region_name = region_name
        self.endpoint_type = endpoint_type
        self.service_type = service_type
        self.service_name = service_name
        self.volume_service_name = volume_service_name
        self.timings = timings
        self.bypass_url = bypass_url.rstrip('/') if bypass_url else bypass_url
        self.os_cache = os_cache or not no_cache
        self.http_log_debug = http_log_debug
        if timeout is not None:
            self.timeout = float(timeout)
        else:
            self.timeout = None

        self.times = []  # [("item", starttime, endtime), ...]

        self.management_url = self.bypass_url or None
        self.auth_token = auth_token
        self.proxy_token = proxy_token
        self.proxy_tenant_id = proxy_tenant_id
        self.keyring_saver = None
        self.keyring_saved = False

        if insecure:
            self.verify_cert = False
        else:
            if cacert:
                self.verify_cert = cacert
            else:
                self.verify_cert = True

        self.auth_system = auth_system
        self.auth_plugin = auth_plugin
        self._session = None
        self._current_url = None
        self._logger = logging.getLogger(__name__)

        if self.http_log_debug and not self._logger.handlers:
            # Logging level is already set on the root logger
            ch = logging.StreamHandler()
            self._logger.addHandler(ch)
            self._logger.propagate = False
            if hasattr(requests, 'logging'):
                rql = requests.logging.getLogger(requests.__name__)
                rql.addHandler(ch)
                # Since we have already setup the root logger on debug, we
                # have to set it up here on WARNING (its original level)
                # otherwise we will get all the requests logging messages
                rql.setLevel(logging.WARNING)

        self.service_catalog = None
        self.services_url = {}
        self.last_request_id = None

    def http_log_req(self, method, url, kwargs):
        if not self.http_log_debug:
            return

    def _get_session(self, url):
        if self._connection_pool:
            magic_tuple = parse.urlsplit(url)
            scheme, netloc, path, query, frag = magic_tuple
            service_url = '%s://%s' % (scheme, netloc)
            if self._current_url != service_url:
                # Invalidate Session object in case the url is somehow changed
                if self._session:
                    self._session.close()
                self._current_url = service_url
                self._logger.debug(
                    "New session created for: (%s)" % service_url)
                self._session = requests.Session()
                self._session.mount(service_url,
                                    self._connection_pool.get(service_url))
            return self._session
        elif self._session:
            return self._session

    def request(self, url, method, **kwargs):

        kwargs.setdefault('headers', kwargs.get('headers', {}))
        kwargs['headers']['User-Agent'] = self.USER_AGENT
        kwargs['headers']['Accept'] = 'application/json'
        if 'body' in kwargs:
            kwargs['headers']['Content-Type'] = 'application/json'
            kwargs['data'] = json.dumps(kwargs['body'])
            del kwargs['body']
        api_versions.update_headers(kwargs["headers"], self.api_version)
        if self.timeout is not None:
            kwargs.setdefault('timeout', self.timeout)
        kwargs['verify'] = self.verify_cert

        self.http_log_req(method, url, kwargs)

        request_func = requests.request
        #session = self._get_session(url)
        session = None
        if session:
            request_func = session.request

        resp = request_func(
            method,
            url,
            **kwargs)

        api_versions.check_headers(resp, self.api_version)

        #self.http_log_resp(resp) #write to log

        if resp.text:
            # TODO(dtroyer): verify the note below in a requests context
            # NOTE(alaski): Because force_exceptions_to_status_code=True
            # httplib2 returns a connection refused event as a 400 response.
            # To determine if it is a bad request or refused connection we need
            # to check the body.  httplib2 tests check for 'Connection refused'
            # or 'actively refused' in the body, so that's what we'll do.
            if resp.status_code == 400:
                if ('Connection refused' in resp.text or
                        'actively refused' in resp.text):
                    raise exceptions.ConnectionRefused(resp.text)
            try:
                body = json.loads(resp.text)
            except ValueError:
                body = None
        else:
            body = None

        self.last_request_id = (resp.headers.get('x-openstack-request-id')
                                if resp.headers else None)
        if resp.status_code >= 400:
            raise exceptions.from_response(resp, body, url, method)

        return resp, body

    def _v2_auth(self, url):
        """Authenticate against a v2.0 auth service."""
        if self.auth_token:
            body = {"auth": {
                    "token": {"id": self.auth_token}}}
        elif self.user_id:
            body = {"auth": {
                    "passwordCredentials": {"userId": self.user_id,
                                            "password": self.password}}}
        else:
            body = {"auth": {
                    "passwordCredentials": {"username": self.user,
                                            "password": self.password}}}

        if self.tenant_id:
            body['auth']['tenantId'] = self.tenant_id
        elif self.projectid:
            body['auth']['tenantName'] = self.projectid

        return self._authenticate(url, body)


    def _time_request(self, url, method, **kwargs): ## write limited time in header
        with utils.record_time(self.times, self.timings, method, url):
            resp, body = self.request(url, method, **kwargs)
        return resp, body


    def _authenticate(self, url, body, **kwargs):
        """Authenticate and extract the service catalog."""
        method = "POST"
        token_url = url + "/tokens"

        # Make sure we follow redirects when trying to reach Keystone
        resp, respbody = self._time_request(
            token_url,
            method,
            body=body,
            allow_redirects=True,
            **kwargs)

        return url, resp, respbody


    def authenticate(self):
        if self.version == "v2.0":  # FIXME(chris): This should be better.
           if not self.auth_system or self.auth_system == 'keystone':
              self.auth_url , resp, respbody = self._v2_auth(self.auth_url) ## at this get the token
              return respbody['access']['token']['id']




client = HTTPClient(
    version='v2.0',
    auth_url='http://127.0.0.1:5000/v2.0',
    user='admin',
    password='stack',
    projectid='admin',
)

auth_token = client.authenticate()
print auth_token



