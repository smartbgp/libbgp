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

from libbgp.tlv import TLV


class Attribute(TLV):

    def __init__(self, value, hex_value=None):
        self.value = value
        self.hex_value = hex_value


class AttributeFlag(int):
    """
    +-------------------------------------------+
    | bit 0 | bit 1 | bit 2 | bit 3 | bit 4 - 7 |
    +-------------------------------------------+
    bit 0:
        It defines whether the attribute is optional (if set to 1)
    or well-known (if set to 0).
    bit 1:
        It defines whether an optional attribute is transitive
    (if set to 1) or non-transitive (if set to 0).
        For well-known attributes, the Transitive bit MUST be set to 1.
    bit 2:
        It defines whether the information contained in the optional
    transitive attribute is partial (if set to 1) or complete (if set to 0).
    For well-known attributes and for optional non-transitive attributes,
    the Partial bit MUST be set to 0.
    bit 3:
        It defines whether the Attribute Length is one octet
    (if set to 0) or two octets (if set to 1).
    bit 4 - 7
        The lower-order four bits of the Attribute Flags octet are
    unused. They MUST be zero when sent and MUST be ignored when
    received.
    """

    EXTENDED_LENGTH = 0x10  # 16  RFC 4271
    PARTIAL = 0x20  # 32  RFC 4271
    TRANSITIVE = 0x40  # 64  RFC 4271
    OPTIONAL = 0x80  # 128 RFC 4271


class AttributeID(int):
    """
    Attribute Type Code
    """

    ORIGIN = 0x01  # 1   [RFC4271]
    AS_PATH = 0x02  # 2   [RFC4271]
    NEXT_HOP = 0x03  # 3   [RFC4271]
    MULTI_EXIT_DISC = 0x04  # 4   [RFC4271]
    LOCAL_PREF = 0x05  # 5   [RFC4271]
    ATOMIC_AGGREGATE = 0x06  # 6   [RFC4271]
    AGGREGATOR = 0x07  # 7   [RFC4271]
    COMMUNITY = 0x08  # 8   [RFC1997]
    ORIGINATOR_ID = 0x09  # 9   [RFC4456]
    CLUSTER_LIST = 0x0a  # 10  [RFC4456]

    MP_REACH_NLRI = 0x0e  # 14  [RFC4760]
    MP_UNREACH_NLRI = 0x0f  # 15  [RFC4760]
    EXTENDED_COMMUNITY = 0x10  # 16  [Eric_Rosen][draft-ramachandra-bgp-ext-communities-00][RFC4360]
    AS4_PATH = 0x11  # 17  [RFC4893]
    AS4_AGGREGATOR = 0x12  # 18  [RFC4893]

    PMSI_TUNNEL = 0x16  # 22  [RFC-ietf-l3vpn-2547bis-mcast-bgp-08]
    Tunnel_Encapsulation_Attribute = 0x17  # 23  [RFC5512]
    Traffic_Engineering = 0x18  # 24  [RFC5543]
    IPv6_Address_Specific_Extended_Community = 0x19  # 25  [RFC5701]

    LINK_STATE = 0x1d
    ATTR_SET = 0x80  # 128 [RFC6368]

    Unassigned = list(range(27, 127)) + list(range(129, 254))
    Reserved_For_Development = 255
