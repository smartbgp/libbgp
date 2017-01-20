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
class AtomicAggregate(Attribute):
    """
    ATOMIC_AGGREGATE is a well-known discretionary attribute of length 0.
    """

    TYPE = AttributeID.ATOMIC_AGGREGATE
    FLAG = AttributeFlag.TRANSITIVE

    @classmethod
    def unpack(cls, data, capability):

        """
        parse bgp ATOMIC_AGGREGATE attribute
        :param data:
        """
        if len(data) == 1:
            return cls(value=struct.unpack('!B', data)[0])
        else:
            raise BGPNotification(3, 5)

    @classmethod
    def pack(cls, data, capability):
        return cls(value=data, hex_value=struct.pack('!B', data))
