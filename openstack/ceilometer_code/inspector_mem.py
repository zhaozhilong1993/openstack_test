#!/usr/bin/env python
# encoding=utf-8
'''
下面模拟了一个插件获取instance也就是虚拟主机的一个代码过程，由于ceilometer里面的
一些资源我们无法直接获取，只能模拟。
'''

from ceilometer.compute.pollsters import util
from ceilometer.compute.virt.libvirt import inspector as libvirt_inspector
from ceilometer import sample
from oslo_utils import timeutils
import collections

CPUStats = collections.namedtuple('CPUStats', ['number', 'time'])


class Server():
    def __init__(self, id=None, flavor=None, name=None,
                 user_id=None, tenant_id=None):
        self.id = id
        self.flavor = flavor
        self.name = name
        self.user_id = user_id
        self.tenant_id = tenant_id


# 模拟了一个虚拟主机类
instance = Server(id='d5e7e7fe-bd03-4845-aa0e-2c56f3a07173',
                  flavor='m1.tiny',
                  name='test1',
                  user_id='deb4be01e1f94c81bddd9c90852c8657',
                  tenant_id='35eda61677ff473aa77e82ee4185c797')

'''
def _get_connection():
    libvirt = __import__('libvirt')
    libvirt.openReadOnly(self.uri)
'''


def inspect_memory_usage(instance):
    # 调用了libvirt的虚拟化的API
    looking_instance = libvirt_inspector.LibvirtInspector()

    connection = looking_instance._get_connection()
    domain = connection.lookupByUUIDString(instance.id)
    return domain.memoryStats()

memery_info = inspect_memory_usage(instance)
print memery_info



