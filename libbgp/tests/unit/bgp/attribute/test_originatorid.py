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

from libbgp.bgp.update.attribute.originatorid import OriginatorID
from libbgp.exception import BGPNotification


class TestOriginatorID(unittest.TestCase):

    def test_unpack(self):

        data_hex = b'\xc0\xa8\x01\x01'
        self.assertEqual('192.168.1.1', OriginatorID.unpack(data=data_hex, capability={}).value)

    def test_bad_message_len(self):
        data_hex = b'\x00\x00\x00\x00\x64'
        self.assertRaises(BGPNotification, OriginatorID.unpack, data_hex, {})

    def test_pack(self):
        data_hex = b'\xc0\xa8\x01\x01'
        self.assertEqual(data_hex, OriginatorID.pack('192.168.1.1', {}).hex_value)
        self.assertRaises(BGPNotification, OriginatorID.pack, '1111.111.11.1', {})


if __name__ == '__main__':
    unittest.main()
