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
import struct

from libbgp.bgp.update.attribute.origin import Origin
from libbgp.exception import BGPNotification


class TestOrigin(unittest.TestCase):

    def test_unpack(self):

        for data in [b'\x00', b'\x01', b'\x02']:
            self.assertEqual(ord(data[0:1]), Origin.unpack(data=data, capability={}).value)

    def test_bad_origin_type(self):
        data_hex = b'\x05'
        self.assertRaises(BGPNotification, Origin.unpack, data_hex, {})

    def test_pack_bad_origin_type(self):
        data = 5
        self.assertRaises(BGPNotification, Origin.pack, data, {})

    def test_pack(self):
        for data in [0, 1, 2]:
            self.assertEqual(struct.pack('!B', data), Origin.pack(data, {}).hex_value)


if __name__ == '__main__':
    unittest.main()
