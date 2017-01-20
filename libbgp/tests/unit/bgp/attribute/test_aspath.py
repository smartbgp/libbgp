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

from libbgp.bgp.update.attribute.aspath import ASPath
from libbgp.exception import BGPNotification


class TestASPath(unittest.TestCase):

    def test_unpack(self):

        # as set
        data_hex = b'\x01\x02\x00d\x00\xc8'
        data = [(1, [100, 200])]
        self.assertEqual(data, ASPath.unpack(data_hex, {}).value)

        # 2bytes AS
        data_hex = b'\x02\x04\x0c\xb9y3\x88 S\xd9'
        self.assertEqual(
            [(2, [3257, 31027, 34848, 21465])],
            ASPath.unpack(data=data_hex, capability={}).value
        )

        # 4bytes AS
        data_hex = b'\x02\x04\x00\x00\x0c\xb9\x00\x00y3\x00\x00\x88 \x00\x00S\xd9'
        self.assertEqual(
            [(2, [3257, 31027, 34848, 21465])],
            ASPath.unpack(data=data_hex, capability={'asn4': True}).value
        )

        # as confederations
        data_hex = b'\x04\x02\x03\xe9\x03\xea\x03\x02\x03\xeb\x03\xec'
        self.assertEqual(
            [(4, [1001, 1002]), (3, [1003, 1004])],
            ASPath.unpack(data=data_hex, capability={}).value
        )

    def test_bad_as_path_type(self):
        data_hex = b'\x00\x00\x00\x00\x64'
        self.assertRaises(BGPNotification, ASPath.unpack, data_hex, {})

    def test_bad_message_len(self):

        data_hex = b'\x02\x04\x0c\xb9y3\x88 S'
        self.assertRaises(BGPNotification, ASPath.unpack, data_hex, {})

    def test_pack(self):

        # as set
        data_hex = b'\x01\x02\x00d\x00\xc8'
        data = [(1, [100, 200])]
        self.assertEqual(data_hex, ASPath.pack(data, {}).hex_value)

        # 2bytes as
        data_hex = b'\x02\x04\x0c\xb9y3\x88 S\xd9'
        data = [(2, [3257, 31027, 34848, 21465])]
        self.assertEqual(data_hex, ASPath.pack(data, {}).hex_value)

        # 4bytes as
        data_hex = b'\x02\x04\x00\x00\x0c\xb9\x00\x00y3\x00\x00\x88 \x00\x00S\xd9'
        data = [(2, [3257, 31027, 34848, 21465])]
        self.assertEqual(data_hex, ASPath.pack(data, {'asn4': True}).hex_value)

        # as confederations
        data_hex = b'\x04\x02\x03\xe9\x03\xea\x03\x02\x03\xeb\x03\xec'
        data = [(4, [1001, 1002]), (3, [1003, 1004])]
        self.assertEqual(data_hex, ASPath.pack(data, {}).hex_value)

    def test_pack_bad_as_path_type(self):
        self.assertRaises(BGPNotification, ASPath.pack, [(5, [1, 2])], {})

if __name__ == '__main__':
    unittest.main()
