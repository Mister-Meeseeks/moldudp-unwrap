#!/usr/bin/python

import sys
import extract as ex

in_stream = sys.stdin

while True:
    print ex.extract_msgs_from_byte_source(in_stream)

