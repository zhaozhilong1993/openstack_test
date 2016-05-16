#!/usr/bin/env python

from collections import defaultdict
from hashlib import md5
import itertools
import operator
import threading
import uuid

from gnocchiclient import client
from gnocchiclient import exceptions as gnocchi_exc
from keystoneauth1 import session as ka_session
from oslo_config import cfg
from oslo_log import log
import requests
import retrying
import six
from stevedore import extension

from ceilometer import declarative
from ceilometer import dispatcher
from ceilometer.i18n import _, _LE, _LW
from ceilometer import keystone_client
from ceilometer import utils

_ks_client = keystone_client.get_client()
project = _ks_client.projects.find(name='gnocchi')