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

import struct

from libbgp.exception import BGPNotification
from .attribute import Attribute, AttributeID, AttributeFlag
from .attributes import Attributes


@Attributes.register()
class Origin(Attribute):
    """
        ORIGIN is a well-known mandatory attribute that defines the
    origin of the path information. The data octet can assume
    the following values:
    Value       Meaning
        0        IGP  -  Network Layer Reachability Information
                  is interior to the originating AS
        1        EGP - Network Layer Reachability Information
                  learned via the EGP protocol [RFC904]
        2        INCOMPLETE - Network Layer Reachability
                 Information learned by some other means
    """
    TYPE = AttributeID.ORIGIN
    FLAG = AttributeFlag.TRANSITIVE

    IGP = 0x00
    EGP = 0x01
    INCOMPLETE = 0x02

    @classmethod
    def unpack(cls, data, capability):

        origin = struct.unpack('!B', data)[0]
        if origin not in [cls.IGP, cls.EGP, cls.INCOMPLETE]:
            raise BGPNotification(3, 6)
        return cls(value=origin)

    @classmethod
    def pack(cls, data, capability):
        if data not in [cls.IGP, cls.EGP, cls.INCOMPLETE]:
            raise BGPNotification(3, 6)
        return cls(data, struct.pack('!B', data))
