
from socket import*
import struct
import sys
import time
import os


def calc_checksum(b_msg):
    s = 0
    # loop taking 2 characters at a time(sum of 16 bit words)
    for i in range(0, len(b_msg), 2):
        word = b_msg[i] + (b_msg[i+1] << 8)
        s += word

    s = (s >> 16) + (s & 0xffff)
    s = s + (s >> 16)
    # complement and mask to 4 byte short
    s = ~s & 0xffff
    return s


def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)


def calc_chcksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        word = msg[i] + (msg[i+1] << 8)
        s = carry_around_add(s, word)
    return ~s & 0xffff


class IP_Header:
    def __init__(self, pack_id, ttl, proto, src_addr, dst_addr):
        self.version = 4
        # size in octets?
        self.h_size = 5
        # type of service
        self.tos = 0
        # kernel will fill
        self.total_len = 0
        # id of the packet
        self.id = pack_id
        self.flag_offset = 0
        self.ttl = ttl
        self.proto = proto
        # kernel will fill correct checksum ?
        self.checksum = 0
        self.src_addr = inet_aton(src_addr)
        self.dst_addr = inet_aton(dst_addr)
        self.header = None

    def pack(self):
        # one octet
        ver_hsize = (self.version << 4) + self.h_size
        # the ! in the pack format string means network order
        self.header = struct.pack('!BBHHHBBH4s4s', ver_hsize, self.tos, self.total_len, self.id, self.flag_offset,
                                  self.ttl, self.proto, self.checksum, self.src_addr, self.dst_addr)
        return self.header


class ICMP_Packet:
    def __init__(self, icmp_type, code, icmp_id, sequence):
        self.type = icmp_type            # 8
        self.code = code                # 8
        self.checksum = 0               # 16
        self.id = icmp_id                # 16
        self.sequence = sequence        # 16
        self.data = None
        self.packet = None
        self.header = None

    def pack(self):
        # make a dummy header for calc checksum
        checksum = 0
        dummy_header = struct.pack('!BBHHH', self.type, self.code, checksum, self.id, self.sequence)
        # data = time of the packet creation
        self.data = struct.pack('d', time.time())
        # calc checksum on the data and the dummy header
        checksum = calc_checksum(dummy_header + self.data)
        # Now that we have the right checksum, we put that in. It's just easier
        # to make up a new header than to stuff it into the dummy.
        self.header = struct.pack('!BBHHH', self.type, self.code, htons(checksum), self.id, self.sequence)
        self.packet = self.header + self.data
        return self.packet


def send_ping(src_ip, dst_ip, process_id):
    send_sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW)
    catch_sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
    catch_sock.bind(('0.0.0.0', 0))
    ip_header = IP_Header(process_id, 1, IPPROTO_ICMP, src_ip, dst_ip)
    icmp_pack = ICMP_Packet(8, 0, process_id, 1)
    send_sock.sendto(ip_header.pack() + icmp_pack.pack(), (dst_ip, 34000))
    datagram, addr = catch_sock.recvfrom(1024)
    print(addr)


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
        self.recv_sock.bind(('0.0.0.0',0))

    def trace(self, max_hops):
        # for ttl in range(1,max_hops):
            ttl = 1
            self.send_sock.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('!B', ttl))
            self.send_sock.sendto(b'', (self.target_addr, self.port))
            msg, addr = self.recv_sock.recvfrom(1024)
            print(addr)

if __name__ == '__main__':
    # get id of the process
    proc_id = os.getpid() & 0xffff
    dst_ip = getaddrinfo(sys.argv[1], 'http', AF_INET)[0][4][0]
    send_ping('192.168.1.3', dst_ip, proc_id)
    # traceroute = UDP_Traceroute(sys.argv[1],30)
    # traceroute.trace(30)
    # tr = Traceroute(sys.argv[1], proc_id)
    # tr.send_ping(1)
    a = 5



