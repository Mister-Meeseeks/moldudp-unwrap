
import extract as ex

def packet_stream_to_message_stream (packet_stream, write_stream):
    for (_, _, msgs) in _iterate_packet_stream(packet_stream):
        for msg in msgs:
            write_stream.write(msg)

def format_packet_stream_headers (packet_stream):
    for unpacked_packet in _iterate_packet_stream(packet_stream):
        yield _format_unpacked_headers(unpacked_packet)

def _format_unpacked_headers ((sesNum, seqNum, msgs)):
    return "SessionNum=%d SeqNum=%d MsgCount=%d MsgSizes=%s" % \
        (sesNum, seqNum, len(msgs), map(len, msgs))

def _iterate_packet_stream (packet_stream):
    while ex.peek_ahead_packets_left(packet_stream):
        yield ex.extract_msgs_from_byte_source(packet_stream)
        
