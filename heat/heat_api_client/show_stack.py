#!/usr/bin/env python
# encoding=utf-8

from heatclient import client as hclient
import get_auth

print 'is my token..'

hc2 = hclient.Client("1", endpoint='http://192.168.122.1:8004/v1/091af6ceedc840f2872d3b71fb181937', token=get_auth.auth_token)

stack_info = hc2.stacks.get('bug1')
print stack_info
