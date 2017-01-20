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
from libbgp.bgp.update.attribute.attribute import Attribute, AttributeID, AttributeFlag
from libbgp.bgp.update.attribute.attributes import Attributes


WELL_KNOW_COMMUNITY_INT_2_STR = {
    0xFFFF0000: 'PLANNED_SHUT',
    0xFFFF0001: 'ACCEPT_OWN',
    0xFFFF0002: 'ROUTE_FILTER_TRANSLATED_v4',
    0xFFFF0003: 'ROUTE_FILTER_v4',
    0xFFFF0004: 'ROUTE_FILTER_TRANSLATED_v6',
    0xFFFF0005: 'ROUTE_FILTER_v6',
    0xFFFF029A: 'BLACKHOLE',
    0xFFFFFF01: 'NO_EXPORT',
    0xFFFFFF02: 'NO_ADVERTISE',
    0xFFFFFF03: 'NO_EXPORT_SUBCONFED',
    0xFFFFFF04: 'NOPEER'
}

WELL_KNOW_COMMUNITY_STR_2_INT = dict(
    [(r, l) for (l, r) in WELL_KNOW_COMMUNITY_INT_2_STR.items()])


@Attributes.register()
class Communities(Attribute):
    """
        COMMUNITIES path attribute is an optional
    transitive attribute of variable length. The attribute consists of a
    set of four octet values, each of which specify a community. All
    routes with this attribute belong to the communities listed in the
    attribute.
        The COMMUNITIES attribute has Type Code 8.
        http://www.iana.org/assignments/bgp-well-known-communities/bgp-well-known-communities.xml
    """
    TYPE = AttributeID.COMMUNITY
    FLAG = AttributeFlag.OPTIONAL + AttributeFlag.TRANSITIVE

    @classmethod
    def unpack(cls, data, capability):
        community = []
        if data:
            try:
                length = len(data) / 2
                value_list = list(struct.unpack('!%dH' % length, data))
                while value_list:
                    value_type = value_list[0] * 16 * 16 * 16 * 16 + value_list[1]
                    if value_type in WELL_KNOW_COMMUNITY_INT_2_STR:
                        community.append(WELL_KNOW_COMMUNITY_INT_2_STR[value_type])
                    else:
                        community.append("%s:%s" % (value_list[0], value_list[1]))
                    value_list = value_list[2:]
            except Exception:
                raise BGPNotification(3, 5)
        return cls(value=community)

    @classmethod
    def pack(cls, data, capability):
        community_hex = b''
        for community in data:
            if community.upper() in WELL_KNOW_COMMUNITY_STR_2_INT:
                value = WELL_KNOW_COMMUNITY_STR_2_INT[community.upper()]
                community_hex += struct.pack('!I', value)
            else:
                try:
                    value = community.split(':')
                    value = int(value[0]) * 16 * 16 * 16 * 16 + int(value[1])
                    community_hex += struct.pack('!I', value)
                except Exception:
                    raise BGPNotification(3, 5)
        return cls(value=data, hex_value=community_hex)
