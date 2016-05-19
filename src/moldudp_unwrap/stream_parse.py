#!/usr/bin/python

import sys
import extract as ex

in_stream = sys.stdin

while ex.peek_ahead_packets_left(in_stream):
    print ex.extract_msgs_from_byte_source(in_stream)

