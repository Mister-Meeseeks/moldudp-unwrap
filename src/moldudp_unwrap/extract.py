
import sys
import struct

def parse_seq_range (packet_bytes):
    seq_bytes = packet_bytes[10:18]
    cnt_bytes = packet_bytes[18:20]
    seq_num = struct.unpack(">Q", seq_bytes)[0]
    cnt_num = struct.unpack(">H", cnt_bytes)[0]
    return (seq_num, seq_num + cnt_num)

def peek_ahead_packets_left (byte_source):
    expected_bytes = _get_packet_peek_bytes()
    read_attempt = _discard_session_ignored(byte_source)
    return len(read_attempt) == expected_bytes

def extract_msgs_from_byte_source (byte_source):
    (session_num, _) = _consume_session_num_post_peek(byte_source)
    (seq_num, _) = _consume_seq_num(byte_source)
    (msgs, _) = _consume_packet_msgs(byte_source)
    return (session_num, seq_num, msgs)

def read_next_packet_bytes (byte_source):
    discard_bytes = _discard_session_ignored(byte_source)
    return discard_bytes + _read_packet_post_discard(byte_source) \
        if len(discard_bytes) else []

def _read_packet_post_discard(byte_source):
    (_, session_bytes) = _consume_session_num_post_peek(byte_source)
    (_, seq_num_bytes) = _consume_seq_num(byte_source)
    (_, msg_bytes) = _consume_packet_msgs(byte_source)
    return session_bytes + seq_num_bytes + msg_bytes

def _discard_session_ignored (byte_source):
    return byte_source.read(_get_packet_peek_bytes());

def _consume_session_num_post_peek (byte_source):
    session_bytes = byte_source.read(_get_session_read_bytes())
    session_parsable_bytes = _truncate_session_bytes_to_intable(session_bytes)
    return (struct.unpack(">Q", session_parsable_bytes)[0], session_bytes)

# We can only use up to 8 bytes for sesssion num, so it's alright to discard
# 2 to peek-ahead at any packets left.
def _get_session_bytes():
    return 10

def _get_session_read_bytes():
    return _get_session_bytes() - _get_packet_peek_bytes()

def _get_packet_peek_bytes():
    return 2    

def _truncate_session_bytes_to_intable (session_num_bytes):
    return session_num_bytes[-8:]

def _consume_seq_num (byte_source):
    n_seq_num_bytes = 8
    seq_bytes = byte_source.read(n_seq_num_bytes)
    return (struct.unpack(">Q", seq_bytes)[0], seq_bytes)

def _consume_packet_msgs (byte_source):
    (msg_count, count_bytes) = _determine_message_count(byte_source)
    scan_rets = map(lambda i: _scan_message(byte_source), range(msg_count))
    return (_unpack_msgs_from_scans(scan_rets),
            count_bytes + _join_bytes_from_scans (scan_rets))

def _unpack_msgs_from_scans (scan_rets):
    return map(lambda i: i[0], scan_rets)

def _join_bytes_from_scans (scan_rets):
    unpacked_bytes = map(lambda i: i[1], scan_rets)
    return reduce(lambda x,y: x+y, unpacked_bytes, "")

def _scan_message (byte_source):
    (msg_size, size_bytes) = _pop_message_size(byte_source)
    msg_bytes = byte_source.read(msg_size)
    return (msg_bytes, size_bytes + msg_bytes)

def _pop_message_size (byte_source):
    return _read_field_size(byte_source)

def _determine_message_count (byte_source):
    (count_field_val, count_bytes) = _pop_message_count(byte_source)
    msg_count = _pivot_for_end_stream_count(count_field_val)
    return (msg_count, count_bytes)

def _pivot_for_end_stream_count (count_val):
    end_of_stream_count = 65535
    return count_val if \
        count_val != end_of_stream_count else 0    

def _pop_message_count (byte_source):
    return _read_field_size(byte_source)

def _read_field_size (byte_source):
    n_size_bytes = 2
    size_bytes = byte_source.read(n_size_bytes)
    return (struct.unpack(">H", size_bytes)[0], size_bytes)
