#!/usr/bin/env python

from gnocchiclient import client as gnocchi_clinet

def gnocchiclient(request, password=None):
    api_version = "1"
    insecure = None
    cacert = None
    endpoint = None
    kwargs = {
        'token': request.user.token.id,
        'insecure': insecure,
        'ca_file': cacert,
        'username': request.user.username,
        'password': password
        # 'timeout': args.timeout,
        # 'ca_file': args.ca_file,
        # 'cert_file': args.cert_file,
        # 'key_file': args.key_file,
    }
    client = gnocchi_clinet.Client(api_version, endpoint, **kwargs)
    return client