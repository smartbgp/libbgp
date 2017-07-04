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
from libbgp.bgp.notification import Notification


class TestNotification(unittest.TestCase):

    def test_unpack(self):

        data_hex = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff' \
                   b'\xff\xff\xff\xff\x00\x17\x03\x01\x02\x10\x06'
        msg = {
            'type': Message.NOTIFICATION,
            'msg': {'code': [1, 2], 'msg': Notification.error_subcode[(1, 2)]}}
        self.assertEqual(
            msg, Message.unpack(data=data_hex).dict())

    def test_pack(self):

        msg = {
            'type': Message.NOTIFICATION,
            'msg': {
                'code': [1, 2],
                'msg': []
            }
        }
        data_hex = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff' \
                   b'\xff\xff\xff\xff\x00\x15\x03\x01\x02'
        self.assertEqual(data_hex, Message.pack(data=msg).hex_value)


if __name__ == '__main__':
    unittest.main()
