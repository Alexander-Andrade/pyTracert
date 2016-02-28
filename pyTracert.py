from socket import*
import struct
import sys
import time
import os
import math
from ip_header import*
from icmp_packet import*


class DestinationReached(Exception):
    pass


class Tracert:

    def __init__(self, target):
        self.target_ip = getaddrinfo(target, 'http', AF_INET)[0][4][0]
        self.host_ip = '192.168.1.3'
        # id of the running process
        self.proc_id = os.getpid() & 0xffff
        self.timeout = 1
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
        fl_dest_reached = False
        ip_header = IP_Header(self.proc_id, ttl, IPPROTO_ICMP, self.host_ip, self.target_ip)
        for port in self.unused_ports:
            icmp_pack = ICMP_Packet(ICMP_Packet.ECHO_REQ_TYPE, ICMP_Packet.ECHO_REQ_CODE, self.proc_id, self.icmp_seq_num)
            start_time = time.time()
            self.send_sock.sendto(ip_header.pack() + icmp_pack.pack(), (self.target_ip, port))
            try:
                icmp_reply, host_addr = self.catch_sock.recvfrom(1024)
                time_stamps.append(time.time() - start_time)
                repl_ip_header = IP_Header()
                repl_icmp_pack = ICMP_Packet()
                repl_ip_header.unpack(icmp_reply)
                repl_icmp_pack.unpack(icmp_reply)
                # test on ICMP Echo-Reply = destination reached
                if repl_icmp_pack.type == ICMP_Packet.ECHO_REPLY_TYPE and repl_icmp_pack.code == ICMP_Packet.ECHO_REPLY_CODE:
                    fl_dest_reached = True
                self.icmp_seq_num += 1
            except OSError as e:
                # infinite expectation
                return None
        # ttl, domain name, IPv4, [time1..time3]
        return ttl, getfqdn(repl_ip_header.src_addr), repl_ip_header.src_addr, time_stamps, fl_dest_reached

    def trace(self):
        trace_table = []
        for i in range(1, self.max_hops):
            ping_results = self.ping(i)
            if ping_results is not None:
                trace_table.append(ping_results[:4])
                if ping_results[4]:
                    break
        return trace_table







