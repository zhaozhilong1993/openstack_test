#!/usr/bin/env python
# encoding=utf-8

from heatclient import client as hclient
import get_auth

print 'is my token..'

hc2 = hclient.Client("1", endpoint='http://192.168.122.1:8004/v1/7b8caf30e9fa4d7aae369e95c8e32443', token=get_auth.auth_token)

stack_list = hc2.stacks.list()
for stack in stack_list:
    print stack
    print stack.description, type(stack.description)
# a = hc2.stacks.get('1f801f24-af07-4d48-ab0c-6d3253bc1dfa')
# print a

