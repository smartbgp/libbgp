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
class ASPath(Attribute):
    """
        AS_PATH is a well-known mandatory attribute that is composed
    of a sequence of AS path segments. Each AS path segment is
    represented by a triple <path segment type, path segment
    length, path segment value>.
        The path segment type is a 1-octet length field with the
    following values defined:
    Value     Segment Type
        1       AS_SET: unordered set of ASes a route in the
                UPDATE message has traversed
        2       AS_SEQUENCE: ordered set of ASes a route in
                the UPDATE message has traversed
        3       AS_CONFED_SEQUENCE: ordered set of Member Autonomous
                Systems in the local confederation that the UPDATE message
                has traversed
        4       AS_CONFED_SET: unordered set of Member Autonomous Systems
                in the local confederation that the UPDATE message has
                traversed
        The path segment length is a 1-octet length field,
    containing the number of ASes (not the number of octets) in
    the path segment value field.
        The path segment value field contains one or more AS
    numbers, each encoded as a 2-octet length field.
    """
    AS_SET = 0x01
    AS_SEQUENCE = 0x02
    AS_CONFED_SEQUENCE = 0x03
    AS_CONFED_SET = 0x04

    TYPE = AttributeID.AS_PATH
    FLAG = AttributeFlag.TRANSITIVE

    @classmethod
    def unpack(cls, data, capability):

        """
        Parse AS PATH attributes.
        :param data: raw binary balue
        """
        # Loop over all path segments
        aspath = []
        while len(data) > 0:
            seg_type, length = struct.unpack('!BB', data[:2])
            if seg_type not in [cls.AS_SET, cls.AS_SEQUENCE, cls.AS_CONFED_SEQUENCE, cls.AS_CONFED_SET]:
                raise BGPNotification(3, 11)
            try:
                if capability.get('asn4'):
                    segment = list(struct.unpack('!%dI' % length, data[2:2 + length * 4]))
                    data = data[2 + length * 4:]

                else:
                    segment = list(struct.unpack('!%dH' % length, data[2:2 + length * 2]))
                    data = data[2 + length * 2:]
            except Exception:
                raise BGPNotification(3, 11)
            aspath.append((seg_type, segment))
        return cls(value=aspath)

    @classmethod
    def pack(cls, data, capability):
        as_path_raw = b''
        for segment in data:
            as_seg_raw = b''
            seg_type = segment[0]
            as_path_list = segment[1]
            if seg_type not in [cls.AS_SET, cls.AS_SEQUENCE, cls.AS_CONFED_SET, cls.AS_CONFED_SEQUENCE]:
                raise BGPNotification(3, 11)

            as_count = 0
            for asn in as_path_list:
                if capability.get('asn4'):
                    as_seg_raw += struct.pack('!I', asn)
                else:
                    as_seg_raw += struct.pack('!H', asn)
                as_count += 1
            as_path_raw += struct.pack('!B', seg_type) + struct.pack('!B', as_count) + as_seg_raw

        return cls(value=data, hex_value=as_path_raw)
