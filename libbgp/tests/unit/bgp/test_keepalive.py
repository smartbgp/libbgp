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

import unittest

from libbgp.bgp.message import Message
from libbgp.exception import BGPNotification


class TestKeepAlive(unittest.TestCase):

    def test_unpack(self):

        data_hex = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x13\x04'
        self.assertEqual({'msg': None, 'type': Message.KEEPALIVE}, Message.unpack(data=data_hex).dict())

        multi_message_data_hex = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff' \
                                 b'\xff\xff\xff\xff\xff\xff\xff\x00\x13\x04' \
                                 b'\xff\xff\xff\xff\xff\xff\xff\xff\xff' \
                                 b'\xff\xff\xff\xff\xff\xff\xff\x00\x13\x04'
        while multi_message_data_hex:
            msg = Message.unpack(data=multi_message_data_hex)
            multi_message_data_hex = multi_message_data_hex[msg.length:]
            self.assertEqual({'msg': None, 'type': Message.KEEPALIVE}, msg.dict())

    def test_pack(self):
        data_hex = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x13\x04'
        self.assertEqual(data_hex, Message.pack({'msg': None, 'type': Message.KEEPALIVE}).hex_value)

    def test_bad_message_len(self):
        try:
            data_hex = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x14\x04\x00'
            Message.unpack(data=data_hex).dict()
        except BGPNotification as e:
            self.assertEqual(e.error_code, 1)
            self.assertEqual(e.sub_error_code, 2)


if __name__ == '__main__':
    unittest.main()
