# -*- coding: utf-8 -*-


"""
This module duplicates part of koji,
to make kobo work on Python 3.
"""


import struct


def hex_string(s):
    """Converts a string to a string of hex digits"""
    return ''.join(['%02x' % ord(x) for x in s])


def __parse_packet_header(pgp_packet):
    """Parse pgp_packet header, return tag type and the rest of pgp_packet"""
    byte0 = ord(pgp_packet[0])
    if (byte0 & 0x80) == 0:
        raise ValueError('Not an OpenPGP packet')
    if (byte0 & 0x40) == 0:
        tag = (byte0 & 0x3C) >> 2
        len_type = byte0 & 0x03
        if len_type == 3:
            offset = 1
            length = len(pgp_packet) - offset
        else:
            (fmt, offset) = {0: ('>B', 2), 1: ('>H', 3), 2: ('>I', 5)}[len_type]
            length = struct.unpack(fmt, pgp_packet[1:offset])[0]
    else:
        tag = byte0 & 0x3F
        byte1 = ord(pgp_packet[1])
        if byte1 < 192:
            length = byte1
            offset = 2
        elif byte1 < 224:
            length = ((byte1 - 192) << 8) + ord(pgp_packet[2]) + 192
            offset = 3
        elif byte1 == 255:
            length = struct.unpack('>I', pgp_packet[2:6])[0]
            offset = 6
        else:
            # Who the ... would use partial body lengths in a signature packet?
            raise NotImplementedError('OpenPGP packet with partial body lengths')
    if len(pgp_packet) != offset + length:
        raise ValueError('Invalid OpenPGP packet length')
    return (tag, pgp_packet[offset:])


def __subpacket_key_ids(subs):
    """Parse v4 signature subpackets and return a list of issuer key IDs"""
    res = []
    while len(subs) > 0:
        byte0 = ord(subs[0])
        if byte0 < 192:
            length = byte0
            off = 1
        elif byte0 < 255:
            length = ((byte0 - 192) << 8) + ord(subs[1]) + 192
            off = 2
        else:
            length = struct.unpack('>I', subs[1:5])[0]
            off = 5
        if ord(subs[off]) == 16:
            res.append(subs[off+1: off+length])
        subs = subs[off+length:]
    return res


def get_sigpacket_key_id(sigpacket):
    """Return ID of the key used to create sigpacket as a hexadecimal string"""
    (tag, sigpacket) = __parse_packet_header(sigpacket)
    if tag != 2:
        raise ValueError('Not a signature packet')
    if ord(sigpacket[0]) == 0x03:
        key_id = sigpacket[11:15]
    elif ord(sigpacket[0]) == 0x04:
        sub_len = struct.unpack('>H', sigpacket[4:6])[0]
        off = 6 + sub_len
        key_ids = __subpacket_key_ids(sigpacket[6:off])
        sub_len = struct.unpack('>H', sigpacket[off:off+2])[0]
        off += 2
        key_ids += __subpacket_key_ids(sigpacket[off:off+sub_len])
        if len(key_ids) != 1:
            raise NotImplementedError('Unexpected number of key IDs: %s' % len(key_ids))
        key_id = key_ids[0][-4:]
    else:
        raise NotImplementedError('Unknown PGP signature packet version %s' % ord(sigpacket[0]))
    return hex_string(key_id)
