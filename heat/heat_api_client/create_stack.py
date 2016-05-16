#!/usr/bin/env python
# encoding=utf-8

from heatclient import client as hclient
import get_auth

tenant_id = '35eda61677ff473aa77e82ee4185c797'
hc2 = hclient.Client("1", endpoint='http://192.168.122.1:8004/v1/%s' % tenant_id, token=get_auth.auth_token)

resp = hc2.stacks.create(

    files={},
    disable_rollback=True,
    parameters={},
    stack_name='zhao3',
    environment={'stack_owner': "admin"},
    template={
        'heat_template_version': '2013-05-23',
        'description': 'HOT template for two interconnected VMs with floating ips.',
        'resources': {
            'private_subnet': {
                'type': 'OS::Neutron::Subnet',
                'properties': {
                    'network_id':
                        {'get_resource': 'private_net'},
                    'cidr': '172.16.2.0/24',
                    'gateway_ip': '172.16.2.1'
                }
            },
            'private_net': {
                'type': 'OS::Neutron::Net',
                'properties': {
                    'name': 'private-net'
                }
            }
        },
        'outputs': {
            'subnet': {
                'description': "this is a Test description.",
                'value': {
                    'get_attr': ['private_subnet', 'show']
                }
            }
        }
    },
    tags="a, 123, b, 456"
)

print resp,type(resp)