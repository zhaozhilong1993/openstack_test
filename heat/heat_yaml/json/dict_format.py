#!/usr/bin/env python

import json


fp = open('server.json','r')
tmp_str = fp.read()
fp.close()

a = json.loads(tmp_str)

def print_dict(d):
 new = {}
 for k, v in d.iteritems():
     if isinstance(v, dict):
         v = print_dict(v)

     new_k = str(k).strip()
     new_v = str(v).strip()

     new[new_k] = new_v
 return new

new_a = print_dict(a)

print new_a