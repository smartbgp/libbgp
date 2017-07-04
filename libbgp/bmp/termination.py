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


@Message.register
class Termination(Message):

    TYPE = Message.TERMINATION
    TYPE_STR = 'termination'

    reason_codict = {
        0: "Session administratively closed.  The session might be re-initiated.",
        1: "Unspecified reason.",
        2: "Out of resources.  The router has exhausted resources available for the BMP session.",
        3: "Redundant connection.  The router has determined\
            that this connection is redundant with another one.",

        4: "Session permanently administratively closed,\
            will not be re-initiated.  Monitoring station should reduce\
            (potentially to 0) the rate at which it attempts\
            reconnection to the monitored router."
    }

    @classmethod
    def unpack(cls, data):

        infor_tlv = dict()
        while data:
            info_type, info_len = struct.unpack('!HH', data[0:4])
            info_value = data[4: 4 + info_len]
            if info_type == 0:
                infor_tlv['string'] = info_value.decode('ascii')
            elif info_type == 1:
                infor_tlv['reason'] = cls.reason_codict[struct.unpack('!H', info_value)[0]]
            data = data[4 + info_len:]
        return cls(value=infor_tlv)
