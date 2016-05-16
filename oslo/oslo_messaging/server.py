#!/usr/bin/env python

import oslo_messaging as messaging
from oslo_config import cfg


class NotificationEndpoint(object):
    def warn(self):
        pass


class ErrorEndpoint(object):
    def error(self):
        pass

transport = messaging.get_transport(cfg.CONF)
targets = [
    messaging.Target(topic='notification'),
    messaging.Target(topic='notification_bis')
]

endpoints = [
    NotificationEndpoint(),
    ErrorEndpoint(),
]

listener = messaging.get_notification_listener(transport,
                                               targets,
                                               endpoints)

listener.start()
listener.wait()