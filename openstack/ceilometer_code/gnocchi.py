#!/usr/bin/env python

from ceilometer import keystone_client
from oslo_config import cfg

opts = [
    cfg.StrOpt('filter_project',
               default='gnocchi')
]

cfg.CONF.register_opts(opts, group="dispatcher_gnocchi")

ks_client = keystone_client.get_client()


# project = ks_client.projects.find("")
