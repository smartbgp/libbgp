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

from libbgp.bgp.update.attribute.aggregator import Aggregator
from libbgp.exception import BGPNotification


class TestAggregator(unittest.TestCase):

    def test_unpack(self):

        # 2 bytes as
        data_hex = b'\x70\xd5\x3e\xe7\xff\x79'
        self.assertEqual(
            [28885, '62.231.255.121'],
            Aggregator.unpack(data=data_hex, capability={}).value
        )

        # 4bytes as
        data_hex = b'\x00\x00\x70\xd5\x3e\xe7\xff\x79'
        self.assertEqual(
            [28885, '62.231.255.121'],
            Aggregator.unpack(data=data_hex, capability={'asn4': True}).value
        )

    def test_bad_message_len(self):
        data_hex = b'\x00\x00\x00\x00\x64'
        self.assertRaises(BGPNotification, Aggregator.unpack, data_hex, {})

    def test_pack(self):

        # 2 bytes as
        data_hex = b'\x70\xd5\x3e\xe7\xff\x79'
        data = [28885, '62.231.255.121']
        self.assertEqual(
            data_hex,
            Aggregator.pack(data=data, capability={}).hex_value
        )

        self.assertRaises(BGPNotification, Aggregator.pack, [65537, '1.1.1.1'], {})

        # 4bytes as
        data_hex = b'\x00\x00\x70\xd5\x3e\xe7\xff\x79'
        data = [28885, '62.231.255.121']
        self.assertEqual(
            data_hex,
            Aggregator.pack(data=data, capability={'asn4': True}).hex_value
        )


if __name__ == '__main__':
    unittest.main()
