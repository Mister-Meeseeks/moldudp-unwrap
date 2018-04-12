#!/usr/bin/python

import sys
import multicast
import consume
import argparse

parser = argparse.ArgumentParser\
         (description="Unwrap MoldUDP Binary Packet Stream")
parser.add_argument('--beginSeq', default="", help="Only echo messages with " +
                    "seqNum >= to [arg]. Only works with normal mode")
parser.add_argument('--endSeq', default="", help="Only echo messages with " +
                    "seqNum <= than [arg]. Only works with normal mode")
parser.add_argument('--header', action="store_true",
                    help="Mode to parse packet header fields, instead of body")
parser.add_argument('--msgHeader', action="store_true",
                    help="Mode to print header metadata associated with " \
                    + "each message")
parser.add_argument('--gapSeq', action="store_true",
                    help="Print the header metadata of messages that"
                    + " bookend gaps in the sequence number.")
parser.add_argument('--multicast', action="append",
                    help="Multicast parsed packets. Format: [IPAddr]:[Port]")
parser.add_argument('--throttle', default="1",
                    help="Milliseconds between multicast transmits")
parser.add_argument('--echo', action="store_true",
                    help="Mode to parse and echo bytes back. Acts as "
                    + "'cat' unless parse broke. Used for testing")
args = parser.parse_args()

in_stream = sys.stdin
out_stream = sys.stdout

min_seq = int(args.beginSeq) if len(args.beginSeq) else None
max_seq = int(args.endSeq) if len(args.endSeq) else None

def read_and_print_headers (in_stream):
    for fmt_str in consume.format_packet_stream_headers(in_stream):
        print fmt_str

def read_and_print_gap_headers (in_stream):
    for fmt_str in consume.format_gap_bookend_headers\
        (in_stream, min_seq, max_seq):
        print fmt_str

def join_and_print_msg_headers (in_stream):
    for fmt_str in consume.format_header_msg_joins(in_stream, min_seq, max_seq):
        print fmt_str

def parse_multicast (dest_arg):
    (ipAddr, port) = dest_arg.split(":")
    return (ipAddr, int(port))
        
if (args.header):
    read_and_print_headers(in_stream)
elif (args.msgHeader):
    join_and_print_msg_headers(in_stream)
elif (args.gapSeq):
    read_and_print_gap_headers(in_stream)
elif (args.echo):
    consume.split_packets_from_stream(in_stream, out_stream)
elif (args.multicast is not None and len(args.multicast) > 0):
    mult_dests = map(parse_multicast, args.multicast)
    cast_socket = multicast.Multicaster(mult_dests, int(args.throttle))
    consume.split_packets_from_stream(in_stream, cast_socket)
else:
    consume.packet_stream_to_message_stream\
        (in_stream, out_stream, min_seq, max_seq)

