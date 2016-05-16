#!/usr/bin/env python

from ceilometer.api.controllers.v2.samples import SamplesController

a = SamplesController()
a.get_all()