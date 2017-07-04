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

from .message import Message

#  0                   1                   2                   3
#  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |          Information Type     |       Information Length      |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                 Information (variable)                        |
# ~                                                               ~
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


@Message.register
class Initiation(Message):

    TYPE = Message.INITIATION
    TYPE_STR = 'initiation'

    @classmethod
    def unpack(cls, data):

        # o  Type = 0: String
        # o  Type = 1: sysDescr
        # o  Type = 2: sysName
        infor_tlv = dict()
        while data:
            info_type, info_len = struct.unpack('!HH', data[0:4])
            info_value = data[4: 4 + info_len]
            if info_type == 0:
                infor_tlv['string'] = info_value.decode('ascii')
            elif info_type == 1:
                infor_tlv['sysDescr'] = info_value.decode('ascii')
            elif info_type == 2:
                infor_tlv['sysName'] = info_value.decode('ascii')
            data = data[4 + info_len:]
        return cls(value=infor_tlv)
