# Copyright 2015-2017 Cisco Systems, Inc.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# https://tools.ietf.org/html/rfc7854

import struct

from libbgp.flag import ByteFlag
from libbgp.net import IPAddress


class PeerType(int):

    key_value = {
        0: 'Global Instance Peer',
        1: 'RD Instance Peer',
        2: 'Local Instance Peer'
    }

    def __str__(self):
        return self.key_value.get(self, 'unknown')


class PeerFlag(ByteFlag):

    FLAGS = ['V', 'L', 'A']


class Message(object):

    VERSION = 3

    PER_PEER_HEADER_LEN = 42

    registered_message = dict()

    ROUTE_MONITORING = 0
    STATISTICS_REPORT = 1
    PEER_DOWN_NOTIFICATION = 2
    PEER_UP_NOTIFICATION = 3
    INITIATION = 4
    TERMINATION = 5
    ROUTE_MIRRORING = 6

    def __init__(self, value, hex_value=None):
        self.value = value
        self.hex_value = hex_value

    @classmethod
    def register(cls, klass):
        if klass.TYPE in cls.registered_message:
            raise RuntimeError('duplicated message type')
        cls.registered_message[klass.TYPE] = klass
        return klass

    def dict(self):
        return {'type': self.TYPE, 'msg': self.value}

    @staticmethod
    def pack_header(msg_type, msg_body):
        pass

    @staticmethod
    def unpack_peer_header(header_raw):
        header_dict = dict()
        header_dict['type'] = str(PeerType(ord(header_raw[0: 1])))
        header_dict['flag'] = PeerFlag(ord(header_raw[1: 2])).dict()
        header_dict['distinguisher'] = struct.unpack('!2I', header_raw[2: 10])[0]
        if header_dict['flag']['V']:
            header_dict['addr'] = IPAddress.unpack(header_raw[10: 26])
        else:
            header_dict['addr'] = IPAddress.unpack(header_raw[22: 26])
        header_dict['asn'] = struct.unpack('!I', header_raw[26: 30])[0]
        header_dict['bgp-id'] = IPAddress.unpack(header_raw[30: 34])
        header_dict['time'] = struct.unpack('!II', header_raw[34: 42])
        return header_dict

    @classmethod
    def unpack(cls, data):
        """unpack BMP message based on its type"""

        version, length, msg_type = struct.unpack('!BIB', data[:6])
        if version != cls.VERSION:
            raise RuntimeError('Version should be %s' % cls.VERSION)

        if msg_type not in cls.registered_message:
            raise RuntimeError('Unknown message type')

        if msg_type in [cls.INITIATION, cls.TERMINATION]:
            msg_body = data[6: length]
        else:
            msg_body = data[6 + cls.PER_PEER_HEADER_LEN: length]
        klass = cls.registered_message[msg_type].unpack(data=msg_body)
        return klass

    @classmethod
    def pack(cls, data):
        pass
