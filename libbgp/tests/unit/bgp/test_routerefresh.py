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
from libbgp.net.family import Family, AFI, SAFI


class TestRouteRefresh(unittest.TestCase):

    def test_unpack_cisco_route_refresh(self):

        data_hex = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff' \
                   b'\xff\xff\xff\x00\x17\x80\x00\x01\x00\x01'
        self.assertEqual(
            {
                'msg': str(Family(AFI.INET, SAFI.UNICAST)),
                'type': Message.CISCO_ROUTE_REFRESH},
            Message.unpack(data=data_hex).dict()
        )

    def test_pack_cisco_route_refresh(self):
        data_hex = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff' \
                   b'\xff\xff\xff\x00\x17\x80\x00\x01\x00\x01'
        json_msg = {
            'type': Message.CISCO_ROUTE_REFRESH,
            'msg': str(Family(AFI.INET, SAFI.UNICAST))
        }
        self.assertEqual(
            data_hex,
            Message.pack(data=json_msg).hex_value
        )

    def test_unpack_route_refresh(self):
        data_hex = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff' \
                   b'\xff\xff\xff\x00\x17\x05\x00\x02\x00\x80'
        self.assertEqual(
            {
                'msg': str(Family(AFI.INET6, SAFI.MPLS_VPN)),
                'type': Message.ROUTE_REFRESH},
            Message.unpack(data=data_hex).dict()
        )

    def test_pack_route_refresh(self):
        data_hex = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff' \
                   b'\xff\xff\xff\x00\x17\x05\x00\x02\x00\x80'
        json_msg = {
            'msg': str(Family(AFI.INET6, SAFI.MPLS_VPN)),
            'type': Message.ROUTE_REFRESH
        }
        self.assertEqual(
            data_hex,
            Message.pack(data=json_msg).hex_value
        )


if __name__ == '__main__':
    unittest.main()
