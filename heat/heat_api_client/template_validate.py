#!/usr/bin/env python
# encoding=utf-8

from heatclient.common import template_format

tmpl = '''
    heat_template_version: 2013-05-23
    resources:
      server1:
        type: OS::Nova::Server
        properties:
            flavor: m1.medium
            image: cirros
            user_data_format: RAW
            user_data:
              get_file: http://test.example/example
    '''

template_format.parse(tmpl)