
import struct

def extract_msgs_from_byte_source (byte_source):
    session_num = _consume_session_num(byte_source)
    seq_num = _consume_seq_num(byte_source)
    msgs = _consume_packet_msgs(byte_source)
    return (session_num, seq_num, len(msgs))

def _consume_session_num (byte_source):
    n_session_bytes = 10
    session_bytes = byte_source.read(n_session_bytes)
    session_parsable_bytes = _truncate_session_bytes_to_intable(session_bytes)
    return struct.unpack(">Q", session_parsable_bytes)[0]

def _truncate_session_bytes_to_intable (session_num_bytes):
    return session_num_bytes[-8:]

def _consume_seq_num (byte_source):
    n_seq_num_bytes = 8
    session_bytes = byte_source.read(n_seq_num_bytes)
    return struct.unpack(">Q", session_bytes)[0]

def _consume_packet_msgs (byte_source):
    msg_count = _consume_message_count(byte_source)
    return map(lambda i: _consume_message(byte_source),
               range(msg_count))

def _consume_message (byte_source):
    msg_size = _consume_message_size(byte_source)
    return byte_source.read(msg_size)

def _consume_message_size (byte_source):
    return _consume_field_size(byte_source)

def _consume_message_count (byte_source):
    return _consume_field_size(byte_source)

def _consume_field_size (byte_source):
    n_size_bytes = 2
    size_bytes = byte_source.read(n_size_bytes)
    return struct.unpack(">H", size_bytes)[0]


        
