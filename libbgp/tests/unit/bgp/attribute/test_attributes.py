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

from libbgp.bgp.update.attribute.attributes import Attributes


class TestAttributes(unittest.TestCase):

    def test_pack_unpack(self):

        data_dict = {
            1: 0,
            2: [(2, [1, 2, 3])],
            3: '172.16.1.14',
            4: 0,
            5: 100,
            9: '172.16.1.14',
            10: ['2.2.2.2', '100.100.100.100']}
        data_hex = Attributes.pack(data_dict, {}).hex_value
        self.assertEqual(data_dict, Attributes.unpack(data_hex, {}).value)

    def test_pack_unknown_attr(self):
        data_dict = {
            1: 0,
            198: 0
        }
        self.assertRaises(RuntimeError, Attributes.pack, data_dict, {})

    def test_unpack_unknown_attr(self):
        data_hex = b'\x40\xff\x01\x00'
        self.assertEqual({255: b'00'}, Attributes.unpack(data_hex, {}).value)


if __name__ == '__main__':
    unittest.main()
