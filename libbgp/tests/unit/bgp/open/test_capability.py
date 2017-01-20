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

from libbgp.bgp.open.capability.capabilities import Capabilities
from libbgp.bgp.open.capability.capability import CapabilityCode


class TestCapabilities(unittest.TestCase):

    def test_unpack_asn4(self):
        data_hex = b'\x02\x06\x41\x04\x00\x00\x12\xe5'
        self.assertEqual(
            {str(CapabilityCode(CapabilityCode.FOUR_BYTES_ASN)): 4837},
            Capabilities.unpack(data_hex).value
        )

    def test_pack_asn4(self):
        data_hex = b'\x02\x06\x41\x04\x00\x00\x12\xe5'
        data_dict = {str(CapabilityCode(CapabilityCode.FOUR_BYTES_ASN)): 4837}
        self.assertEqual(
            data_hex,
            Capabilities.pack(data_dict).hex_value
        )

    def test_unpack_route_refresh(self):
        data_hex = b'\x02\x02\x02\x00\x02\x02\x80\x00'
        self.assertEqual(
            {
                str(CapabilityCode(CapabilityCode.ROUTE_REFRESH)): True,
                str(CapabilityCode(CapabilityCode.CISCO_ROUTE_REFRESH)): True
            },
            Capabilities.unpack(data_hex).value
        )

    def test_pack_route_refresh(self):
        data_dict = {
            str(CapabilityCode(CapabilityCode.ROUTE_REFRESH)): True,
            str(CapabilityCode(CapabilityCode.CISCO_ROUTE_REFRESH)): True
        }
        data_hex = Capabilities.pack(data_dict).hex_value
        self.assertEqual(data_dict, Capabilities.unpack(data_hex).value)

    def test_unpack_multi_protocol(self):
        data_hex = b'\x02\x06\x01\x04\x00\x02\x00\x80\x02\x06\x01\x04\x00\x02' \
                   b'\x00\x01\x02\x06\x01\x04\x00\x02\x00\x04'
        self.assertEqual(
            {'afi-safi': ['ipv6-mplsvpn', 'ipv6-unicast', 'ipv6-label_unicast']},
            Capabilities.unpack(data_hex).value
        )

    def test_pack_multi_protocol(self):
        data_hex = b'\x02\x06\x01\x04\x00\x02\x00\x80\x02\x06\x01\x04\x00\x02' \
                   b'\x00\x01\x02\x06\x01\x04\x00\x02\x00\x04'
        data_dict = {'afi-safi': ['ipv6-mplsvpn', 'ipv6-unicast', 'ipv6-label_unicast']}
        self.assertEqual(
            data_hex,
            Capabilities.pack(data_dict).hex_value
        )

    def test_unpack_unknow(self):
        data_hex = b'\x02\x02\x87\x00'
        self.assertEqual(
            {'UNKNOWN(135)': b''},
            Capabilities.unpack(data_hex).value
        )
