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

from libbgp.net.family import Family, AFI, SAFI


class TestFamily(unittest.TestCase):

    def test_str(self):

        self.assertEqual('ipv4-unicast', str(Family(AFI.INET, SAFI.UNICAST)))
        self.assertEqual('ipv4-label_unicast', str(Family(AFI.INET, SAFI.MPLS_LABEL)))
        self.assertEqual('l2vpn-evpn', str(Family(AFI.L2VPN, SAFI.EVPN)))
        self.assertEqual('ipv4-flowspec', str(Family(AFI.INET, SAFI.FLOWSPEC)))
        self.assertEqual('ipv4-mplsvpn', str(Family(AFI.INET, SAFI.MPLS_VPN)))
        self.assertEqual('linkstate-linkstate', str(Family(AFI.BGPLS, SAFI.BGPLS)))
        self.assertEqual('ipv6-mplsvpn', str(Family(AFI.INET6, SAFI.MPLS_VPN)))
