from socket import*
import struct
import sys
import time
import os
from ip_header import*
from icmp_packet import*


class Tracert:

    ICMP_ECHO_REQ_TYPE = 8
    ICMP_ECHO_REQ_CODE = 0

    def __init__(self, target):
        self.target_ip = getaddrinfo(target, 'http', AF_INET)[0][4][0]
        self.host_ip = '192.168.1.3'
        # id of the running process
        self.proc_id = os.getpid() & 0xffff
        self.ttl = 1
        self.timeout = 3
        self.max_hops = 30
        # ports to send the ICMP Request ( it would be nice if they are closed )
        self.unused_ports = [33460, 36230, 58203]
        # must be unique
        self.icmp_seq_num = 0
        self.send_sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW)
        self.catch_sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
        self.catch_sock.bind(('0.0.0.0', 0))
        self.catch_sock.settimeout(self.timeout)

    def ping(self, ttl):
        # send ICMP Echo-Request and catch ICMP Echo-Reply or ICMP Destination Unreachable
        ping_results = []
        ip_header = IP_Header(self.proc_id, ttl, IPPROTO_ICMP, self.host_ip, self.target_ip)
        for port in self.unused_ports:
            icmp_pack = ICMP_Packet(Tracert.ICMP_ECHO_REQ_TYPE, Tracert.ICMP_ECHO_REQ_CODE, self.proc_id, self.icmp_seq_num)
            self.send_sock.sendto(ip_header.pack() + icmp_pack.pack(), (self.target_ip, port))
            icmp_reply, host_addr = self.catch_sock.recvfrom(1024)
            ip_header_bytes = icmp_reply[0:20]
            repl_ip_header = IP_Header()
            repl_ip_header.unpack(icmp_reply)
            self.icmp_seq_num += 1

    @staticmethod
    def __parse_icmp_reply(self,icmp_reply):
        pass


def send_ping(src_ip, dst_ip, process_id):
    send_sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW)
    catch_sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
    catch_sock.bind(('0.0.0.0', 0))
    ip_header = IP_Header(process_id, 6, IPPROTO_ICMP, src_ip, dst_ip)
    icmp_pack = ICMP_Packet(8, 0, process_id, 1)
    send_sock.sendto(ip_header.pack() + icmp_pack.pack(), (dst_ip, 34000))
    datagram, addr = catch_sock.recvfrom(1024)
    print(addr)


if __name__ == '__main__':
    tracert = Tracert('www.google.com')
    tracert.ping(1)




