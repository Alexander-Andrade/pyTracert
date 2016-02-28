from socket import*
import struct
from checksum import*


class Traceroute:

    def __init__(self, target, id_seed):
        self.dst_ip = getaddrinfo(target, 80, AF_INET)[0][4][0]
        self.send_sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
        self.catch_sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
        self.catch_sock.bind(('0.0.0.0', 0))
        self.id_seed = id_seed

    def send_ping(self, ttl):
        self.send_sock.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('!B', ttl))
        # ping
        icmp_type = 8
        icmp_code = 0
        icmp_checksum = 0
        icmp_id = self.id_seed
        # use ttl as sequence number as it is unique for every packet sent
        icmp_sequence = ttl
        icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_sequence)
        icmp_checksum = calc_checksum(icmp_header)
        icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_sequence)
        # send
        self.send_sock.sendto(icmp_header, (self.dst_ip, 0))
        # catch
        mes, addr = self.catch_sock.recvfrom(1024)
        print(addr)


class UDP_Traceroute:

    def __init__(self, target, time_out):
        self.target_addr = getaddrinfo(target, 'http', AF_INET, SOCK_DGRAM, IPPROTO_UDP)[0][4][0]
        self.timeout = time_out
        self.port = 33434
        self.recv_sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
        self.send_sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.recv_sock.bind(('0.0.0.0', 0))

    def trace(self, max_hops):
        # for ttl in range(1,max_hops):
            ttl = 1
            self.send_sock.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('!B', ttl))
            self.send_sock.sendto(b'', (self.target_addr, self.port))
            msg, addr = self.recv_sock.recvfrom(1024)
            print(addr)
