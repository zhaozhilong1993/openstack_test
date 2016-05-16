#!/usr/bin/env python

from senlinclient import client
import get_auth

senclient = client.Client('1',
              auth_url='http://127.0.0.1:5000/v2.0',
              project_id='1acd0026829f4d28bb2eff912d7aad0d',
              token=get_auth.auth_token,
              user_id='0818abde5a934a0ba7cfda39798cf7c5',
              auth_plugin='token'
              )

params = {
        'name': 'demo',
        'profile_id': 'c5603c40',
        'desired_capacity': 2,
        'min_size': 1,
        'max_size': 3,
        'metadata': None,
        'timeout': 60
}

# senclient.delete_cluster('demo')
cluster = senclient.create_cluster(**params)
print cluster