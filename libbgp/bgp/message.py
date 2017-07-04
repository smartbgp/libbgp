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

# https://tools.ietf.org/html/rfc4271#section-4.1
# BGP Message Header
# 0                   1                   2                   3
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                                                               |
# +                                                               +
# |                                                               |
# +                                                               +
# |                           Marker                              |
# +                                                               +
# |                                                               |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |          Length               |      Type     |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

"""Message base class
"""
import struct

from libbgp.exception import MessageUncompleted
from libbgp.exception import BGPNotification


class Message(object):

    """The basic class of BGP message, every kind of BGP message
    should inherit from this class and implement at least two methods:
    pack() and unpack()
    """
    MARKER = b'\xff' * 16
    HDR_LEN = 19
    MAX_LEN = 4096

    registered_message = dict()

    TYPE = None
    OPEN = 1
    UPDATE = 2
    NOTIFICATION = 3
    KEEPALIVE = 4
    ROUTE_REFRESH = 5
    CISCO_ROUTE_REFRESH = 128

    def __init__(self, value, length=None, hex_value=None):
        self.value = value
        self.length = length
        self.hex_value = hex_value

    @classmethod
    def register(cls, klass):
        """class decorator for automatically register
        new types of BGP messages class
        """
        if klass.TYPE in cls.registered_message:
            raise RuntimeError('duplicated message type')
        cls.registered_message[klass.TYPE] = klass
        return klass

    def dict(self):
        """return dictionary format
        """
        return {'type': self.TYPE, 'msg': self.value}

    @staticmethod
    def pack_header(msg_type, msg_body):
        """Prepends the mandatory header to a constructed BGP message
        """
        #    16-octet     2-octet  1-octet
        # ---------------+--------+---------+----------+
        #    Maker      | Length |  Type   |  msg_body |
        # ---------------+--------+---------+----------+
        return Message.MARKER + struct.pack('!H', Message.HDR_LEN + len(msg_body)) + \
            struct.pack('!B', msg_type) + msg_body

    @classmethod
    def unpack(cls, data, length=0, capability={}):
        """unpack bgp message based on its type
        """
        if len(data) < cls.HDR_LEN:
            # Every BGP message is at least 19 octets. The message is
            # uncompleted or the rest hasn't arrived yet.
            raise MessageUncompleted(
                message="The message is uncompleted or the rest hasn't arrived yet.")

        # unpack the message header
        # check whether the first 16 octets of the data consist of the
        # BGP marker (all bits one)
        marker, length, msg_type = struct.unpack('!16sHB', data[:cls.HDR_LEN])
        if marker != cls.MARKER:
            raise BGPNotification(1, 1)

        if length < cls.HDR_LEN or length > cls.MAX_LEN:
            raise BGPNotification(1, 2)  # Bad Message Length

        if len(data) < length:
            raise MessageUncompleted()

        if msg_type not in cls.registered_message:
            raise BGPNotification(1, 3)  # Bad Message type

        msg_body = data[cls.HDR_LEN: length]
        klass = cls.registered_message[msg_type].unpack(
            data=msg_body,
            length=length,
            capability=capability)
        return klass

    @classmethod
    def pack(cls, data, capability={}):
        """pack message data into binary data.
        """
        msg_type = data.get('type')
        if msg_type not in cls.registered_message:
            raise BGPNotification(1, 3)
        msg_body = cls.registered_message[msg_type].pack(data=data.get('msg'), capability=capability)
        return cls(
            value=data.get('msg'),
            hex_value=cls.pack_header(msg_type, msg_body.hex_value)
        )
