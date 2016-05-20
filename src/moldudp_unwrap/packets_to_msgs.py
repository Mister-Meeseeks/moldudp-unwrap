#!/usr/bin/python

import sys
import consume

in_stream = sys.stdin
out_stream = sys.stdout

consume.packet_stream_to_message_stream(in_stream, out_stream)

