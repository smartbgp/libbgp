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

# https://tools.ietf.org/html/rfc4271#section-4.2
# In addition to the fixed-size BGP header, the OPEN message contains
# the following fields:
# 0                   1                   2                   3
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+
# |    Version    |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |     My Autonomous System      |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |           Hold Time           |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                         BGP Identifier                        |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# | Opt Parm Len  |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                                                               |
# |             Optional Parameters (variable)                    |
# |                                                               |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import struct

from libbgp.bgp.message import Message
from libbgp.exception import BGPNotification
from libbgp.net import IPAddress
from .capability.capabilities import Capabilities


@Message.register
class Open(Message):

    TYPE = Message.OPEN
    TYPE_STR = 'open'

    VERSION = 4

    @classmethod
    def unpack(cls, data, length, capability):
        open_msg = dict()
        try:
            open_msg['version'], open_msg['asn'], open_msg['hold-time'] = struct.unpack('!BHH', data[:5])
        except:
            raise BGPNotification(1, 2)
        if open_msg['version'] != cls.VERSION:
            # BGP-4
            raise BGPNotification(2, 1)

        if open_msg['asn'] == 0:
            raise BGPNotification(2, 2)

        if isinstance(open_msg['asn'], float):
            tmp = str(open_msg['asn']).split('.')
            open_msg['asn'] = 65536 * (int(tmp[0])) + int(tmp[1])

        try:
            open_msg['bgp-id'] = IPAddress.unpack(data[5:9])
        except:
            raise BGPNotification(2, 3)

        opt_para_len = struct.unpack('!B', data[9:10])
        if opt_para_len:
            open_msg['capabilities'] = Capabilities.unpack(data[10:]).value
        return cls(value=open_msg, length=length)

    @classmethod
    def pack(cls, data, capability):
        capabilities = Capabilities.pack(data.get('capabilities')).hex_value
        open_header = struct.pack(
            '!BHH',
            data.get('version') or cls.VERSION,
            data.get('asn'),
            data.get('hold-time')
        ) + IPAddress.pack(data.get('bgp-id')) + struct.pack('!B', len(capabilities))
        return cls(value=data, hex_value=open_header + capabilities)
