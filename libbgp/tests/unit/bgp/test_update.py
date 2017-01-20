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

from libbgp.bgp.update import Update
from libbgp.bgp.message import Message


class TestUpdate(unittest.TestCase):

    def test_pack_nlri(self):
        nlri = ['184.157.224.1/32', '32.65.243.12/30', '89.232.254.0/23', '69.179.221.0/24',
                '61.172.0.0/16', '202.223.128.0/17', '156.152.0.0/15', '15.0.0.0/8',
                '209.102.178.0/24', '66.112.100.0/22', '208.54.194.0/24']
        hex_nlri = b' \xb8\x9d\xe0\x01\x1e A\xf3\x0c\x17Y\xe8\xfe\x18E\xb3\xdd\x10='\
                   b'\xac\x11\xca\xdf\x80\x0f\x9c\x98\x08\x0f\x18\xd1f\xb2\x16Bpd\x18\xd06\xc2'
        self.assertEqual(hex_nlri, Update.pack_nlri(nlri))

    def test_unpack_nlri(self):
        nlri = ['184.157.224.1/32', '32.65.243.12/30', '89.232.254.0/23', '69.179.221.0/24',
                '61.172.0.0/16', '202.223.128.0/17', '156.152.0.0/15', '15.0.0.0/8',
                '209.102.178.0/24', '66.112.100.0/22', '208.54.194.0/24']
        hex_nlri = b' \xb8\x9d\xe0\x01\x1e A\xf3\x0c\x17Y\xe8\xfe\x18E\xb3\xdd\x10='\
                   b'\xac\x11\xca\xdf\x80\x0f\x9c\x98\x08\x0f\x18\xd1f\xb2\x16Bpd\x18\xd06\xc2'
        self.assertEqual(nlri, Update.unpack_nlri(hex_nlri))

    def test_unpack_nlri_with_addpath(self):
        hex_nlri = b'\x00\x00\x00\x01\x20\x05\x05\x05\x05\x00\x00\x00\x01\x20\xc0\xa8\x01\x05'
        nlri = [
            {'prefix': '5.5.5.5/32', 'path_id': 1},
            {'prefix': '192.168.1.5/32', 'path_id': 1}
        ]
        self.assertEqual(nlri, Update.unpack_nlri(hex_nlri, True))

    def test_pack_nlri_with_addpath(self):
        hex_nlri = b'\x00\x00\x00\x01\x20\x05\x05\x05\x05\x00\x00\x00\x01\x20\xc0\xa8\x01\x05'
        nlri = [
            {'prefix': '5.5.5.5/32', 'path_id': 1},
            {'prefix': '192.168.1.5/32', 'path_id': 1}
        ]
        self.assertEqual(hex_nlri, Update.pack_nlri(nlri, True))

    def test_ipv4_unicast_with_rr(self):
        # data_hex = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff' \
        #            b'\xff\xff\xff\x00\x4a\x02\x00\x00\x00\x2e\x40\x01\x01' \
        #            b'\x00\x40\x02\x00\x40\x03\x04\xac\x10\x01\x0e\x80\x04' \
        #            b'\x04\x00\x00\x00\x00\x40\x05\x04\x00\x00\x00\x64\x80' \
        #            b'\x0a\x08\x02\x02\x02\x02\x64\x64\x64\x64\x80\x09\x04' \
        #            b'\xac\x10\x01\x0e\x20\xac\x10\x01\x0e'
        data_dict = {
            'msg': {
                'attr': {
                    1: 0,
                    2: [],
                    3: '172.16.1.14',
                    4: 0,
                    5: 100,
                    8: ['1234:5678', '1122:3344', 'NO_EXPORT'],
                    9: '172.16.1.14',
                    10: ['2.2.2.2', '100.100.100.100']},
                'nlri': ['172.16.1.14/32'],
                'withdraw': []},
            'type': 2}
        data_hex = Message.pack(data_dict, {}).hex_value
        self.assertEqual(data_dict, Message.unpack(data_hex).dict())

    def test_ipv4_unicast_withdraw(self):
        data_dict = {
            'msg': {
                'withdraw': ['172.16.1.14/32', '192.168.1.1/32']
            },
            'type': 2
        }
        data_hex = Message.pack(data_dict, {}).hex_value
        data_dict_2 = Message.unpack(data_hex).dict()
        self.assertEqual(data_dict['type'], data_dict_2['type'])
        self.assertEqual(data_dict['msg']['withdraw'], data_dict_2['msg']['withdraw'])


if __name__ == '__main__':
    unittest.main()
