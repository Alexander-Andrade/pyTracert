from socket import*
import struct
import sys
import time
import os
from ip_header import*
from icmp_packet import*


class Tracert:

    def __init__(self):
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
    # get id of the process
    proc_id = os.getpid() & 0xffff
    dst_ip = getaddrinfo(sys.argv[1], 'http', AF_INET)[0][4][0]
    send_ping('192.168.1.3', dst_ip, proc_id)
    # traceroute = UDP_Traceroute(sys.argv[1],30)
    # traceroute.trace(30)
    # tr = Traceroute(sys.argv[1], proc_id)
    # tr.send_ping(1)




