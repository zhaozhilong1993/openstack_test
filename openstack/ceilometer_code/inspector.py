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
instance = Server(id='51de64df-7108-4fbe-94c0-aef8d1fcdc01',
                  flavor='m1.tiny',
                  name='test1',
                  user_id='aff6c943c15843b593e98a41fde972f7',
                  tenant_id='a087b275f6da40a0a06be67ee74089e3')

'''
def _get_connection():
    libvirt = __import__('libvirt')
    libvirt.openReadOnly(self.uri)
'''

def inspect_cpu(instance):
    # 调用了libvirt的虚拟化的API
    looking_instance = libvirt_inspector.LibvirtInspector()

    # 查找虚拟主机，然后与虚拟主机取得连接接着获取虚拟主机的信息
    # _get_connnection 里面调用了libvirt这个虚拟化管理库用的是python的__import__
    connection = looking_instance._get_connection()
    domain = connection.lookupByUUIDString(instance.id)
    domain_info = domain.info()
    print domain_info
    print 'inspector data:', domain_info[3], domain_info[4]
    return CPUStats(number=domain_info[3], time=domain_info[4])


def inspect_memory_usage(instance):
    # 调用了libvirt的虚拟化的API
    looking_instance = libvirt_inspector.LibvirtInspector()

    connection = looking_instance._get_connection()
    domain = connection.lookupByUUIDString(instance.id)
    return domain.memoryStats()


class CPUPollster(object):

    def get_samples(self):

        cpu_info = inspect_cpu(instance)

        # next tranlate the meta data
        name = instance.name
        unit = 'ns'
        volume = cpu_info.time

        # create the sample data
        yield sample.Sample(
            name=name,
            type=type,
            unit=unit,
            volume=volume,
            user_id=instance.user_id,
            project_id=instance.tenant_id,
            resource_id=instance.id,
            timestamp=timeutils.utcnow().isoformat(),
            resource_metadata='',
        )


class MemoryUsagePollster():

    def get_samples(self):
        memory_info = inspect_cpu()


# cuppoll is a generator
cuppoll = CPUPollster().get_samples()
for i in cuppoll:
    print 'cpu:', i


