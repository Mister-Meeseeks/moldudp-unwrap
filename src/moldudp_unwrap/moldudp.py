#!/usr/bin/python

import sys
import multicast
import consume
import argparse

parser = argparse.ArgumentParser\
         (description="Unwrap MoldUDP Binary Packet Stream")
parser.add_argument('--header', action="store_true",
                    help="Parse packet header fields, instead of body")
parser.add_argument('--multicast', action="append",
                    help="Multicast parsed packets. Format: [IPAddr]:[Port]")
parser.add_argument('--throttle', default="1",
                    help="Milliseconds between multicast transmits")
parser.add_argument('--echo', action="store_true",
                    help="Parse each echo then write bytes, acts as "
                    + "'cat' unless parse broke. Used for testing")
args = parser.parse_args()

in_stream = sys.stdin
out_stream = sys.stdout

def read_and_print_headers (in_stream):
    for fmt_str in consume.format_packet_stream_headers(in_stream):
        print fmt_str

def parse_multicast (dest_arg):
    (ipAddr, port) = dest_arg.split(":")
    return (ipAddr, int(port))
        
if (args.header):
    read_and_print_headers(in_stream)
elif (args.echo):
    # Option effectively acts as cat, unless parsing's broke. Used for debugging
    consume.split_packets_from_stream(in_stream, out_stream)
elif (len(args.multicast) > 0):
    mult_dests = map(parse_multicast, args.multicast)
    cast_socket = multicast.Multicaster(mult_dests, int(args.throttle))
    consume.split_packets_from_stream(in_stream, cast_socket)
else:
    consume.packet_stream_to_message_stream(in_stream, out_stream)

