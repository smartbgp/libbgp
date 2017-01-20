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


class TestOpen(unittest.TestCase):

    def test_unpack(self):

        data_hex = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff' \
                   b'\xff\xff\xff\x00\x51\x01\x04\x12\xe5\x00\xb4\xc0\xa8' \
                   b'\x01\x07\x34\x02\x06\x01\x04\x00\x02\x00\x80\x02\x06' \
                   b'\x01\x04\x00\x02\x00\x01\x02\x06\x01\x04\x00\x02\x00' \
                   b'\x04\x02\x06\x01\x04\x00\x01\x00\x01\x02\x02\x80\x00' \
                   b'\x02\x02\x02\x00\x02\x02\x87\x00\x02\x06\x41\x04\x00' \
                   b'\x00\x12\xe5'
        msg_open = {
            'msg': {
                'asn': 4837,
                'bgp-id': '192.168.1.7',
                'capabilities': {
                    'UNKNOWN(135)': b'',
                    'afi-safi': [
                        'ipv6-mplsvpn',
                        'ipv6-unicast',
                        'ipv6-label_unicast',
                        'ipv4-unicast'],
                    'asn4': 4837,
                    'cisco-route-refresh': True,
                    'route-refresh': True},
                'hold-time': 180,
                'version': 4},
            'type': 1}
        self.assertEqual(
            msg_open,
            Message.unpack(data=data_hex).dict()
        )

    def test_pack(self):
        data_dict = {
            'type': 1,
            'msg': {
                'version': 4,
                'asn': 60000,
                'hold-time': 180,
                'bgp-id': '10.140.0.32',
                'capabilities': {
                    'afi-safi': ['ipv4-unicast', 'ipv4-mplsvpn'],
                    'cisco-route-refresh': True,
                    'route-refresh': True,
                    'asn4': 60000
                }
            }
        }
        data_hex = Message.pack(data_dict).hex_value
        self.assertEqual(data_dict, Message.unpack(data=data_hex).dict())


if __name__ == '__main__':
    unittest.main()
