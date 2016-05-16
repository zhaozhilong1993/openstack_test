#!/usr/bin/env python
# encoding=utf-8

from heatclient import client as hclient
import get_auth

tenant_id = '35eda61677ff473aa77e82ee4185c797'
hc2 = hclient.Client("1", endpoint='http://192.168.122.1:8004/v1/%s' % tenant_id, token=get_auth.auth_token)

stack_id = 'ed4e79f1-5894-4713-8ebc-084caf2ec99a'
snapshot_id = '209b79e7-291a-4f8b-8b45-c85b97a94027'

resp = hc2.stacks.snapshot_delete(stack_id, snapshot_id)

print resp