
"""
Library contains functions transforming MoldUDP packet streams various
parsed inputs.
"""


import struct
import extract as ex

def packet_stream_to_message_stream (packet_stream, message_stream):
    """ Reads from a package stream, then writes unpakced binary messages
    to an output stream
    Args: packet_stream - input stream or object supporting .read(int)
          message_stream - output stream or object supporting .write(string)
    """
    for msg in _iterate_message_from_packets(packet_stream):
        _write_message_stream(msg, message_stream)

def _write_message_stream(msg_str, msg_stream):
    msg_size_bytes = struct.pack(">H", len(msg_str))
    msg_stream.write(msg_size_bytes)
    msg_stream.write(msg_str)

def split_packets_from_stream (packet_stream, out_stream):
    """ Reads from a package byte stream, then makes write() calls, where each 
    call represents the byte array corresponding to one single, complete packet.
    Args: packet_stream: input stream or object supporting .read(int)
          message_stream - output stream or object supporting .write(string)
    """
    while (True):
        packet_bytes = ex.read_next_packet_bytes(packet_stream)
        if (len(packet_bytes) == 0):
            break
        out_stream.write(packet_bytes)

def format_packet_stream_headers (packet_stream):
    """ Reads from a package stream, returns a generator of strings
    describing packet header content.
    Args: packet_stream - input stream or object supporting .read(int)
    Returns: generator of formatted strings based on packet header
    """
    for unpacked_packet in _iterate_packet_stream(packet_stream):
        yield _format_unpacked_headers(unpacked_packet)

def format_header_msg_joins (packet_stream):
    """ Reads from a package stream, returns a generator of strings
    describing the header content for every message (i.e. some headers
    be duplicated). Useful to line up headers with individual msgs. 
    Args: packet_stream - input stream or object supporting .read(int)
    Returns: generator of formatted strings based on packet header
    """
    for (sess, seq, msgs) in _iterate_packet_stream(packet_stream):
        for msg in msgs:
            yield _format_unpacked_headers((sess, seq, [msg]))

def _format_unpacked_headers ((sesNum, seqNum, msgs)):
    return "SessionNum=%d SeqNum=%d MsgCount=%d MsgSizes=%s" % \
        (sesNum, seqNum, len(msgs), map(len, msgs))

def _iterate_message_from_packets (packet_stream):
    for (_, _, msgs) in _iterate_packet_stream(packet_stream):
        for msg in msgs:
            yield msg    

def _iterate_packet_stream (packet_stream):
    while ex.peek_ahead_packets_left(packet_stream):
        yield ex.extract_msgs_from_byte_source(packet_stream)
        
