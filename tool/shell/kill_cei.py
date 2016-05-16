#!/usr/bin/env python

import commands 


cmd=" ps ax | grep ceilometer | awk '{print $1}'"
cmd_rec=commands.getstatusoutput(cmd)[1]
all = cmd_rec.split('\n')
for i in all:
  cmd = "kill -5 %s" % i
  print commands.getstatusoutput(cmd)[1]
