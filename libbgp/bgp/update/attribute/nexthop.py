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

from libbgp.exception import BGPNotification
from libbgp.net import IPAddress
from .attribute import Attribute, AttributeID, AttributeFlag
from .attributes import Attributes


@Attributes.register()
class NextHop(Attribute):
    """
        This is a well-known mandatory attribute that defines the
    (unicast) IP address of the router that SHOULD be used as
    the next hop to the destinations listed in the Network Layer
    Reachability Information field of the UPDATE message.
    """

    TYPE = AttributeID.NEXT_HOP
    FLAG = AttributeFlag.TRANSITIVE

    @classmethod
    def unpack(cls, data, capability):

        """
        Parse BGP nexthop.
        :param data: raw binary data
        """
        if len(data) % 4 == 0:
            next_hop = IPAddress.unpack(data)
            return cls(value=next_hop)
        else:
            raise BGPNotification(3, 5)

    @classmethod
    def pack(cls, data, capability):
        try:
            return cls(data, IPAddress.pack(data))
        except:
            raise BGPNotification(3, 5)
