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

from libbgp.bgp.update.attribute.community.rfc1997.communities import Communities
from libbgp.exception import BGPNotification


class TestCommunity(unittest.TestCase):

    def test_unpack(self):

        data_hex = b'\x12\xe5&\xc9\xff\xff\x02\x9a'
        self.assertEqual(
            ['4837:9929', 'BLACKHOLE'],
            Communities.unpack(data=data_hex, capability={}).value
        )
        data_hex = b'\x14\xe5&\xc9\xff\xff\x02\x9a\x1a'
        self.assertRaises(BGPNotification, Communities.unpack, data_hex, {})

    def test_pack(self):

        community_list = ['NONO', '1234:5678']
        self.assertRaises(BGPNotification, Communities.pack, community_list, {})

        community_list = ['4837:9929', 'BLACKHOLE']
        self.assertEqual(
            b'\x12\xe5&\xc9\xff\xff\x02\x9a',
            Communities.pack(community_list, {}).hex_value
        )


if __name__ == '__main__':
    unittest.main()
