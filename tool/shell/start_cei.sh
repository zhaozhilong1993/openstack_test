#!/bin/bash

nohup /usr/bin/python /usr/bin/ceilometer-polling --polling-namespaces central --config-file /etc/ceilometer/ceilometer.conf  &
nohup /usr/bin/python /usr/bin/ceilometer-agent-notification --config-file /etc/ceilometer/ceilometer.conf    &
nohup /usr/bin/python /usr/bin/ceilometer-polling --polling-namespaces ipmi --config-file /etc/ceilometer/ceilometer.conf  &
nohup /usr/bin/python /usr/bin/ceilometer-collector --config-file /etc/ceilometer/ceilometer.conf    &
nohup /usr/bin/python /usr/bin/ceilometer-polling --polling-namespaces compute --config-file /etc/ceilometer/ceilometer.conf  &
nohup /usr/bin/python /usr/bin/ceilometer-api --polling-namespaces compute --config-file /etc/ceilometer/ceilometer.conf  &

