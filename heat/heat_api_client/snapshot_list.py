#!/usr/bin/env python
# encoding=utf-8

from heatclient import client as hclient
import get_auth

hc2 = hclient.Client("1", endpoint='http://192.168.122.1:8004/v1/1acd0026829f4d28bb2eff912d7aad0d', token=get_auth.auth_token)

stack_id = '472cdce1-628b-4be7-a607-4aac711eb2e4'

resp = hc2.stacks.snapshot_list('zhao3')


print resp['snapshots'][0]
print resp['snapshots'][1]