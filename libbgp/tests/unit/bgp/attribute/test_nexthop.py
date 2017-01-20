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

from libbgp.bgp.update.attribute.nexthop import NextHop
from libbgp.exception import BGPNotification


class TestNextHop(unittest.TestCase):

    def test_unpack(self):

        self.assertEqual(
            '10.10.10.1',
            NextHop.unpack(data=b'\x0a\x0a\x0a\x01', capability={}).value
        )
        self.assertEqual(
            '0.0.0.0',
            NextHop.unpack(data=b'\x00\x00\x00\x00', capability={}).value
        )
        self.assertEqual(
            '255.255.255.255',
            NextHop.unpack(data=b'\xff\xff\xff\xff', capability={}).value
        )

    def test_bad_message_len(self):
        data_hex = b'\x00\x00\x00\x00\x64'
        self.assertRaises(BGPNotification, NextHop.unpack, data_hex, {})

    def test_pack(self):
        data = b'\x0a\x0a\x0a\x01'
        self.assertEqual(data, NextHop.pack('10.10.10.1', {}).hex_value)

    def test_pack_bad_ip_address(self):
        self.assertRaises(BGPNotification, NextHop.pack, '300.0.0.1', {})


if __name__ == '__main__':
    unittest.main()
