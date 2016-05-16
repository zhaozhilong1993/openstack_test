#!/usr/bin/env python

import requests

header = {
    'X-Auth-Token' : '8c6cf78925f041b999c6b8be2cdfb99a'
}

body = {
    "back_window": 0,
    "definition": [{
        "granularity": "1s",
        "timespan": "1 hour"
                   },{
        "points": 48,
        "timespan": "1 day"
    }],
    "name": "low2"
}

url = 'http://127.0.0.1:8041'
part_path = '/v1/archive_policy'
path = url + part_path
res = requests.post(path, data=body, headers=header)

print res
