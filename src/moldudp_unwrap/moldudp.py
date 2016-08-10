#!/usr/bin/python

import sys
import consume
import argparse

parser = argparse.ArgumentParser\
         (description="Unwrap MoldUDP Binary Packet Stream")
parser.add_argument('--header', action="store_true",
                    help="Parse packet header fields, instead of body")
args = parser.parse_args()

in_stream = sys.stdin
out_stream = sys.stdout

def readAndPrintHeaders (in_stream):
    for fmt_str in consume.format_packet_stream_headers(in_stream):
        print fmt_str

if (args.header):
    readAndPrintHeaders(in_stream)
else:
    consume.packet_stream_to_message_stream(in_stream, out_stream)

