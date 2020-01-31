
import time
import socket

def _open_multicast_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    return sock

class Multicaster:
    def __init__ (self, dests, throttle_ms):
        self._casters = list(map(_MulticastChannel, dests))
        self._throttle_ms = throttle_ms
        
    def write (self, packet_bytes):
        for c in self._casters:
            c.write(packet_bytes)
        time.sleep(self._throttle_ms / 1000.0)

class _MulticastChannel:
    def __init__ (self, dest):
        (ip_addr, port) = dest
        self._sock = _open_multicast_socket()
        self._dest = (ip_addr, port)

    def write (self, packet_bytes):
        self._sock.sendto(packet_bytes, self._dest)
