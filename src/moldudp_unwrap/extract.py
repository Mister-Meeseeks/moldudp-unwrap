
import struct

def peek_ahead_packets_left (byte_source):
    n_peek_bytes = 2
    read_attempt = byte_source.read(n_peek_bytes)
    return len(read_attempt) == n_peek_bytes

def extract_msgs_from_byte_source (byte_source):
    session_num = _consume_session_num_post_peek(byte_source)
    seq_num = _consume_seq_num(byte_source)
    msgs = _consume_packet_msgs(byte_source)
    return (session_num, seq_num, len(msgs))

def _consume_session_num_post_peek (byte_source):
    session_bytes = byte_source.read(_get_session_read_bytes())
    session_parsable_bytes = _truncate_session_bytes_to_intable(session_bytes)
    return struct.unpack(">Q", session_parsable_bytes)[0]

# We can only use up to 8 bytes for sesssion num, so it's alright to discard
# 2 to peek-ahead at any packets left.
def _get_session_read_bytes():
    n_session_bytes = 10
    return n_session_bytes - _get_packet_peek_bytes()

def _get_packet_peek_bytes():
    return 2    

def _truncate_session_bytes_to_intable (session_num_bytes):
    return session_num_bytes[-8:]

def _consume_seq_num (byte_source):
    n_seq_num_bytes = 8
    session_bytes = byte_source.read(n_seq_num_bytes)
    return struct.unpack(">Q", session_bytes)[0]

def _consume_packet_msgs (byte_source):
    msg_count = _pop_message_count(byte_source)
    return map(lambda i: _scan_message(byte_source),
               range(msg_count))

def _scan_message (byte_source):
    msg_size = _pop_message_size(byte_source)
    return byte_source.read(msg_size)

def _pop_message_size (byte_source):
    return _read_field_size(byte_source)

def _determine_message_count (byte_source):
    count_field_val = _pop_message_count(byte_source)
    end_of_stream_count = 65535
    return count_field_val if \
        count_field_val != end_of_stream_count else 0

def _pop_message_count (byte_source):
    return _read_field_size(byte_source)

def _read_field_size (byte_source):
    n_size_bytes = 2
    size_bytes = byte_source.read(n_size_bytes)
    return struct.unpack(">H", size_bytes)[0]


        
