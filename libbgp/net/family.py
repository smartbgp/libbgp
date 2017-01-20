# Copyright 2015-2017 Cisco Systems, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
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

"""
Address family numbers, from
http://www.iana.org/assignments/address-family-numbers
"""


class AFI(int):

    INET = 0x01
    INET6 = 0x02
    L2VPN = 0x19
    BGPLS = 0x4004

    hex_code = {
        'ipv4': INET,
        'ipv6': INET6,
        'l2vpn': L2VPN,
        'linkstate': BGPLS
    }

    def __str__(self):

        if self == self.INET:
            return 'ipv4'
        elif self == self.INET6:
            return 'ipv6'
        elif self == self.L2VPN:
            return 'l2vpn'
        elif self == self.BGPLS:
            return 'linkstate'


class SAFI(int):

    UNICAST = 0x01
    MPLS_LABEL = 0x04
    EVPN = 70
    BGPLS = 71
    MPLS_VPN = 128
    FLOWSPEC = 133

    hex_code = {
        'unicast': UNICAST,
        'label_unicast': MPLS_LABEL,
        'evpn': EVPN,
        'linkstate': BGPLS,
        'mplsvpn': MPLS_VPN,
        'flowspec': FLOWSPEC
    }

    def __str__(self):
        if self == self.UNICAST:
            return 'unicast'
        elif self == self.MPLS_LABEL:
            return 'label_unicast'
        elif self == self.EVPN:
            return 'evpn'
        elif self == self.BGPLS:
            return 'linkstate'
        elif self == self.FLOWSPEC:
            return 'flowspec'
        elif self == self.MPLS_VPN:
            return 'mplsvpn'


class Family (object):

    __slots__ = ['afi', 'safi']

    def __init__(self, afi, safi):
        self.afi = AFI(afi)
        self.safi = SAFI(safi)

    def __str__(self):
        return '%s-%s' % (str(self.afi), str(self.safi))

    @staticmethod
    def str_2_int(afi_safi):
        afi, safi = afi_safi.split('-')
        return AFI.hex_code.get(afi), SAFI.hex_code.get(safi)
