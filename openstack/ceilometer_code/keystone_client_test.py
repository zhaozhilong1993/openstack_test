#!/usr/bin/env python

import novaclient
from novaclient import client as nova_client
from ceilometer import keystone_client
from keystoneauth1 import loading as ka_loading

logger = None

def get_session(requests_session=None):
    """Get a ceilometer service credentials auth session."""
    auth_plugin = ka_loading.load_auth_from_conf_options(cfg.CONF, CFG_GROUP)
    session = ka_loading.load_session_from_conf_options(
        cfg.CONF, CFG_GROUP, auth=auth_plugin, session=requests_session
    )
    return session



nova_client = nova_client.Client(
            version=2,
            session=keystone_client.get_session(),
            region_name=None,
            interface="public",
            service_type="compute",
            endpoint_override=None,
            auth=None,
            logger=logger)
