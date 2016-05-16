#!/usr/bin/env python
# encoding=utf-8

import argparse
import sys

args = sys.argv[1:]

parser = argparse.ArgumentParser()
parser.add_argument("--version",
                    default='1',
                    help='your version'
                    )

args_list = parser.parse_args(args)
print args_list
print args_list.version



