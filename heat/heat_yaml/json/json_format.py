#!/usr/bin/env python

fp = open('server.json', 'r')
tmp_str = fp.read()
fp.close()

import json
import six

a = json.loads(tmp_str)

for key, value in six.iteritems(a):
    print key, value