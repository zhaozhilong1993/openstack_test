#!/usr/bin/env python

from oslo_config import cfg
import oslo_messaging as messaging

transport = messaging.get_transport(cfg.CONF)
notifier = messaging.Notifier(transport,
                              driver='messaging',
                              topic='notification')

notifier2 = notifier.prepare(publisher_id='compute')
notifier2.error(ctxt={},
                event_type='my_type',
                payload={'content': 'error'})