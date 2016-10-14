
import time
import socket

def _open_multicast_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    return sock

class Multicaster:
    def __init__ (self, ip_addr, port):
        self._sock = _open_multicast_socket()
        self._dest = (ip_addr, port)
        self._throttle_ms = 1

    def write (self, packet_bytes):
        self._sock.sendto(packet_bytes, self._dest)
        time.sleep(self._throttle_ms / 1000.0)
