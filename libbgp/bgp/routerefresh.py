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

# Message Format: One <AFI, SAFI> encoded as
# 0       7       15      23     31
# +-------+-------+-------+-------+
# |      AFI      | Res.  | SAFI  |
# +-------+-------+-------+-------+

import struct

from .message import Message
from libbgp.net.family import Family


@Message.register
class RouteRefresh(Message):

    TYPE = Message.ROUTE_REFRESH
    TYPE_STR = 'route-refresh'

    @classmethod
    def unpack(cls, data, length, capability):

        afi, res, safi = struct.unpack("!HBB", data)
        return cls(value=str(Family(afi, safi)), length=length)

    @classmethod
    def pack(cls, data, capability):
        afi, safi = Family.str_2_int(data)
        if afi and safi:
            msg_body = struct.pack('!H', afi) + b'\x00' + struct.pack('!B', safi)
            return cls(value=data, hex_value=msg_body)
        else:
            raise RuntimeError('AFI/SAFI error')
