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
