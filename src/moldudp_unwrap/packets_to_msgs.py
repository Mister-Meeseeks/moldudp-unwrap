#!/usr/bin/python

import sys
import consume

in_stream = sys.stdin

for fmt_str in consume.format_packet_stream_headers(in_stream):
    print fmt_str

