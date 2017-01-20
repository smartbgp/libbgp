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

from libbgp.bgp.update.attribute.med import MED
from libbgp.exception import BGPNotification


class TestMED(unittest.TestCase):

    def test_unpack(self):

        data_hex = b'\x00\x00\x00\xa0'
        self.assertEqual(160, MED.unpack(data=data_hex, capability={}).value)

    def test_bad_message_len(self):
        data_hex = b'\x00\x00\x00\x00\x64'
        self.assertRaises(BGPNotification, MED.unpack, data_hex, {})

    def test_pack(self):
        self.assertEqual(b'\x00\x00\x00\xa0', MED.pack(160, {}).hex_value)

    def test_pack_bad_value(self):
        self.assertRaises(BGPNotification, MED.pack, 65536, {})


if __name__ == '__main__':
    unittest.main()
