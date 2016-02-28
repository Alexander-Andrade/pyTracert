from socket import*
import struct
import time
from checksum import*


class ICMP_Packet:

    ICMP_ECHO_REPLY_TYPE = 0
    ICMP_ECHO_REPLY_CODE = 0
    ICMP_TIME_EXCEEDED_TYPE = 11
    ICMP_TIME_EXCEEDED_CODE = 0


    def __init__(self, icmp_type=0, code=0, icmp_id=0, sequence=0):
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

    def unpack(self, packet):
        self.packet = packet[20:]
        # define data field config by the ICMP type and code
        self.type, self.code, self.checksum = struct.unpack('!BBH', self.packet[:4])
        # if ICMP Echo-Reply

        if self.type == ICMP_Packet.ICMP_TIME_EXCEEDED_TYPE and self.code == ICMP_Packet.ICMP_TIME_EXCEEDED_CODE:
            pass
