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

from libbgp.bmp.message import Message


class TestCommon(unittest.TestCase):

    def test_wrong_version(self):

        data_hex = b'\x04\x00\x00\x00\x06\x04'
        self.assertRaises(RuntimeError, Message.unpack, data_hex)

    def test_unknow_msg_type(self):
        data_hex = b'\x03\x00\x00\x00\x06\x07'
        self.assertRaises(RuntimeError, Message.unpack, data_hex)

    def test_per_peer_header(self):
        data_hex = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                   b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0a\x4b\x2c\x0b' \
                   b'\x00\x00\xfd\xfe\x0a\x4b\x2c\x0b\x00\x00\x00\x00\x00' \
                   b'\x00\x00\x00'

        header = {
            'addr': '10.75.44.11',
            'asn': 65022,
            'bgp-id': '10.75.44.11',
            'distinguisher': 0,
            'flag': {'A': 0, 'L': 0, 'V': 0},
            'time': (0, 0),
            'type': 'Global Instance Peer'}
        self.assertEqual(header, Message.unpack_peer_header(data_hex))
