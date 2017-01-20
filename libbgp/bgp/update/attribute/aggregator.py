# Copyright 2015-2017 Cisco Systems, Inc.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import struct

from libbgp.exception import BGPNotification
from libbgp.net import IPAddress
from .attribute import Attribute, AttributeID, AttributeFlag
from .attributes import Attributes


@Attributes.register()
class Aggregator(Attribute):
    """
        AGGREGATOR is an optional transitive attribute of length 6.
    The attribute contains the last AS number that formed the
    aggregate route (encoded as 2 octets), followed by the IP
    address of the BGP speaker that formed the aggregate route
    (encoded as 4 octets). This SHOULD be the same address as
    the one used for the BGP Identifier of the speaker
    """

    TYPE = AttributeID.AGGREGATOR
    FLAG = AttributeFlag.OPTIONAL + AttributeFlag.TRANSITIVE

    @classmethod
    def unpack(cls, data, capability):

        """
        Parse Aggregator attributes.
        :param data: raw binary data
        """
        try:
            if not capability.get('asn4'):
                asn = struct.unpack('!H', data[:2])[0]
                aggregator = IPAddress.unpack(data[2:])
            else:
                asn = struct.unpack('!I', data[:4])[0]
                aggregator = IPAddress.unpack(data[4:])
        except Exception:
            raise BGPNotification(3, 5)

        return cls(value=[asn, aggregator])

    @classmethod
    def pack(cls, data, capability):
        try:
            if capability.get('asn4'):
                return cls(value=data, hex_value=struct.pack('!I', data[0]) + IPAddress.pack(data[1]))
            else:
                return cls(value=data, hex_value=struct.pack('!H', data[0]) + IPAddress.pack(data[1]))
        except:
            raise BGPNotification(3, 5)
