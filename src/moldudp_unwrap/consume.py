
"""
Library contains functions transforming MoldUDP packet streams various
parsed inputs.
"""


import struct
import extract as ex

def packet_stream_to_message_stream (packet_stream, message_stream,
                                     min_seq=None, max_seq=None):
    """ Reads from a package stream, then writes unpakced binary messages
    to an output stream
    Args: packet_stream - input stream or object supporting .read(int)
          message_stream - output stream or object supporting .write(string)
          min_seq - Minimum seq number to cutoff output at (use None to ignore)
          max_seq - Maximum seq number to cutoff output at (use None to ignore)
    """
    for msg in _iterate_messages_from_packets(packet_stream, min_seq, max_seq):
        _write_message_stream(msg, message_stream)

def _write_message_stream(msg_str, msg_stream):
    msg_size_bytes = struct.pack(">H", len(msg_str))
    msg_stream.write(msg_size_bytes)
    msg_stream.write(msg_str)

def split_packets_from_stream (packet_stream, out_stream, min_seq, max_seq):
    """ Reads from a package byte stream, then makes write() calls, where each 
    call represents the byte array corresponding to one single, complete packet.
    Args: packet_stream: input stream or object supporting .read(int)
          message_stream - output stream or object supporting .write(string)
          min_seq - Minimum seq number to cutoff output at (use None to ignore)
          max_seq - Maximum seq number to cutoff output at (use None to ignore)
    """
    while (True):
        packet_bytes = ex.read_next_packet_bytes(packet_stream)
        if (len(packet_bytes) == 0):
            break
        if (_is_packet_in_range(packet_bytes, min_seq, max_seq)):
            out_stream.write(packet_bytes)

def format_packet_stream_headers (packet_stream, min_seq=None, max_seq=None):
    """ Reads from a package stream, returns a generator of strings
    describing packet header content.
    Args: packet_stream - input stream or object supporting .read(int)
          min_seq - Minimum seq number to cutoff output at (use None to ignore)
          max_seq - Maximum seq number to cutoff output at (use None to ignore)
    Returns: generator of formatted strings based on packet header
    """
    for unpacked in _iterate_packet_stream(packet_stream):
        if (_is_header_in_range(unpacked, min_seq, max_seq)):
            yield _format_unpacked_headers(unpacked)

def format_header_msg_joins (packet_stream, min_seq=None, max_seq=None):
    """ Reads from a package stream, returns a generator of strings
    describing the header content for every message (i.e. some headers
    be duplicated). Useful to line up headers with individual msgs. 
    Args: packet_stream - input stream or object supporting .read(int)
          min_seq - Minimum seq number to cutoff output at (use None to ignore)
          max_seq - Maximum seq number to cutoff output at (use None to ignore)
    Returns: generator of formatted strings based on packet header
    """
    for unpacked in _iterate_messages_as_packets\
        (packet_stream, min_seq, max_seq):
        yield _format_unpacked_headers(unpacked)


def format_gap_bookend_headers (packet_stream, min_seq=None, max_seq=None):
    """ Reads from a package stream, returns a generator of strings
    for messages that bookend gaps in the sequence number.
    Args: packet_stream - input stream or object supporting .read(int)
          min_seq - Minimum seq number to cutoff output at (use None to ignore)
          max_seq - Maximum seq number to cutoff output at (use None to ignore)
    Returns: generator of formatted strings based on packet header
    """
    last_seq = 0
    last_fmt = None
    for (ses, seq, msgs) in _iterate_messages_as_packets\
        (packet_stream, min_seq, max_seq):
        fmt = _format_unpacked_headers((ses, seq, msgs))
        if (seq > last_seq + 1):
            yield _format_bookend(last_fmt, fmt)
        last_seq = seq
        last_fmt = fmt

def _format_unpacked_headers (docket):
    (sesNum, seqNum, msgs) = docket
    return "SessionNum=%d SeqNum=%d MsgCount=%d MsgSizes=%s" % \
        (sesNum, seqNum, len(msgs), list(map(len, msgs)))

def _format_bookend (open_fmt, close_fmt):
    prefix = "------------------------------------------------------------"
    open_paste = "< " if open_fmt is None else "< %s" % open_fmt
    close_paste = "> %s" % close_fmt
    return "\n".join([prefix, open_paste, close_paste, ""])

def _iterate_packet_stream (packet_stream):
    while ex.peek_ahead_packets_left(packet_stream):
        yield ex.extract_msgs_from_byte_source(packet_stream)

def _iterate_messages_from_packets (packets, min_seq, max_seq):
    for (_, _, [msg]) in _iterate_messages_as_packets\
        (packets, min_seq, max_seq):
        yield msg

def _iterate_messages_as_packets (packet_stream, min_seq, max_seq):
    for (sess, seq, msgs) in _iterate_packet_stream(packet_stream):
        for msg in msgs:
            if (_in_seq_range(seq, min_seq, max_seq)):
                yield (sess, seq, [msg])
            seq = seq + 1
            
def _in_seq_range (seq, min_seq, max_seq):
    above_min = seq >= min_seq if min_seq is not None else True
    below_max = seq <= max_seq if max_seq is not None else True
    return above_min and below_max

def _is_packet_in_range (packet_bytes, min_seq, max_seq):
    if (min_seq is None and max_seq is None):
        return True  # Trap out when range is unset to increase performance
    (lower, upper) = ex.parse_seq_range(packet_bytes)
    return _is_lower_upper_in_range(lower, upper, min_seq, max_seq)

def _is_lower_upper_in_range (lower, upper, min_seq, max_seq):
    return _in_seq_range(upper, min_seq, None) and \
        _in_seq_range(lower, None, max_seq)

def _is_header_in_range (docket, min_seq, max_seq):
    (_, seq_num, msgs) = docket
    end_seq = seq_num + len(msgs) - 1
    return _is_lower_upper_in_range(seq_num, end_seq, min_seq, max_seq)
