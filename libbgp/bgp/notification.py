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

"""Notification Message Class
"""

import struct

from libbgp.bgp.message import Message


@Message.register
class Notification(Message):

    TYPE = Message.NOTIFICATION
    TYPE_STR = 'notification'

    error_code = {
        1: "Message header error",
        2: "OPEN message error",
        3: "UPDATE message error",
        4: "Hold timer expired",
        5: "State machine error",
        6: "Cease"
    }

    error_subcode = {
        (1, 0): "Unspecific",
        (1, 1): "Connection Not Synchronized",
        (1, 2): "Bad Message Length",
        (1, 3): "Bad Message Type",

        (2, 0): "Unspecific",
        (2, 1): "Unsupported Version Number",
        (2, 2): "Bad Peer AS",
        (2, 3): "Bad BGP Identifier",
        (2, 4): "Unsupported Optional Parameter",
        (2, 5): "Authentication Notification (Deprecated)",
        (2, 6): "Unacceptable Hold Time",
        # RFC 5492
        (2, 7): "Unsupported Capability",

        # draft-ietf-idr-bgp-multisession-06
        (2, 8): "Grouping Conflict",
        (2, 9): "Grouping Required",
        (2, 10): "Capability Value Mismatch",

        (3, 0): "Unspecific",
        (3, 1): "Malformed Attribute List",
        (3, 2): "Unrecognized Well-known Attribute",
        (3, 3): "Missing Well-known Attribute",
        (3, 4): "Attribute Flags Error",
        (3, 5): "Attribute Length Error",
        (3, 6): "Invalid ORIGIN Attribute",
        (3, 7): "AS Routing Loop",
        (3, 8): "Invalid NEXT_HOP Attribute",
        (3, 9): "Optional Attribute Error",
        (3, 10): "Invalid Network Field",
        (3, 11): "Malformed AS_PATH",

        (4, 0): "Unspecific",

        (5, 0): "Unspecific",
        # RFC 6608
        (5, 1): "Receive Unexpected Message in OpenSent State",
        (5, 2): "Receive Unexpected Message in OpenConfirm State",
        (5, 3): "Receive Unexpected Message in Established State",

        (6, 0): "Unspecific",
        # RFC 4486
        (6, 1): "Maximum Number of Prefixes Reached",
        (6, 2): "Administrative Shutdown",  # augmented with draft-ietf-idr-shutdown
        (6, 3): "Peer De-configured",
        (6, 4): "Administrative Reset",
        (6, 5): "Connection Rejected",
        (6, 6): "Other Configuration Change",
        (6, 7): "Connection Collision Resolution",
        (6, 8): "Out of Resources",

        # draft-keyur-bgp-enhanced-route-refresh-00
        (7, 1): "Invalid Message Length",
        (7, 2): "Malformed Message Subtype"
    }

    @classmethod
    def unpack(cls, data, length, capability):
        """unpack notification binary message
        """
        error, suberror = struct.unpack('!BB', data[:2])
        if (error, suberror) in cls.error_subcode:
            return cls(
                value={
                    'code': [error, suberror],
                    'msg': cls.error_subcode[(error, suberror)]
                },
                length=length
            )
        else:
            return cls(value='unknown error', length=length)

    @classmethod
    def pack(cls, data, capability):
        """pack message to binary
        """
        msg = struct.pack('!BB', data['code'][0], data['code'][1])
        return cls(value=data, hex_value=msg)
