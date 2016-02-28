from socket import*
import struct


class IP_Header:
    def __init__(self, pack_id=0, ttl=0, proto=0, src_addr=None, dst_addr=None):
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
        self.src_addr = src_addr
        self.dst_addr = dst_addr
        self.header = None

    def pack(self):
        if self.header is None:
            # one octet
            ver_hsize = (self.version << 4) + self.h_size
            # the ! in the pack format string means network order
            self.header = struct.pack('!BBHHHBBH4s4s', ver_hsize, self.tos, self.total_len, self.id, self.flag_offset,
                                      self.ttl, self.proto, self.checksum, inet_aton(self.src_addr), inet_aton(self.dst_addr))
        return self.header

    def unpack(self, packet):
        b_header = packet[:20]
        ver_hsize, self.tos, self.total_len, self.id, self.flag_offset, self.ttl, self.proto, self.checksum, b_src_addr, b_dst_addr = struct.unpack('!BBHHHBBH4s4s', b_header)
        self.version = ver_hsize >> 4
        self.h_size = ver_hsize & 0xF
        self.src_addr = inet_ntoa(b_src_addr)
        self.dst_addr - inet_ntoa(b_dst_addr)