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
from .message import Message


@Message.register
class KeepAlive(Message):

    TYPE = Message.KEEPALIVE
    TYPE_STR = 'keepalive'

    @classmethod
    def unpack(cls, data, length, capability):
        if len(data) != 0:
            raise BGPNotification(1, 2)
        return cls(value=None, length=length + cls.HDR_LEN)

    @classmethod
    def pack(cls, data, capability):
        return cls(value=data, hex_value=b'')
