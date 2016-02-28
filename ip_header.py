from socket import*
import struct


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
