from socket import*
import struct
import sys
import time
import os
from ip_header import*
from icmp_packet import*


class Tracert:

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
        time_stamps = []
        ip_header = IP_Header(self.proc_id, ttl, IPPROTO_ICMP, self.host_ip, self.target_ip)
        for port in self.unused_ports:
            icmp_pack = ICMP_Packet(ICMP_Packet.ECHO_REQ_TYPE, ICMP_Packet.ECHO_REQ_CODE, self.proc_id, self.icmp_seq_num)
            start_time = time.time()
            self.send_sock.sendto(ip_header.pack() + icmp_pack.pack(), (self.target_ip, port))
            icmp_reply, host_addr = self.catch_sock.recvfrom(1024)
            time_stamps.append(time.time() - start_time)
            repl_ip_header = IP_Header()
            repl_icmp_pack = ICMP_Packet()
            repl_ip_header.unpack(icmp_reply)
            repl_icmp_pack.unpack(icmp_reply)
            self.icmp_seq_num += 1
        # ttl, domain name, IPv4, [time1..time3]
        return ttl, getfqdn(repl_ip_header.src_addr), repl_ip_header.src_addr, time_stamps


if __name__ == '__main__':
    #tracert = Tracert('www.google.com')
    #tracert.ping(1)
    print(gethostbyname('www.google.com'))
    print(gethostbyaddr(gethostbyname('www.google.com')))
    print(getfqdn('www.google.com'))




