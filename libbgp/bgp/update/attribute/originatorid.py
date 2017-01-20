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
class OriginatorID(Attribute):
    """
        ORIGINATOR_ID is a new optional, non-transitive BGP attribute of Type
    code 9. This attribute is 4 bytes long and it will be created by an
    RR in reflecting a route. This attribute will carry the BGP
    Identifier of the originator of the route in the local AS. A BGP
    speaker SHOULD NOT create an ORIGINATOR_ID attribute if one already
    exists. A router that recognizes the ORIGINATOR_ID attribute SHOULD
    ignore a route received with its BGP Identifier as the ORIGINATOR_ID.
    (RFC 4456 Page 6)
    """

    TYPE = AttributeID.ORIGINATOR_ID
    FLAG = AttributeFlag.OPTIONAL

    @classmethod
    def unpack(cls, data, capability):
        """
        Parse originator id
        :param data:
        """
        if len(data) != 4:
            raise BGPNotification(3, 5)
        return cls(value=IPAddress.unpack(data))

    @classmethod
    def pack(cls, data, capability):
        try:
            return cls(data, IPAddress.pack(data))
        except:
            raise BGPNotification(3, 5)
