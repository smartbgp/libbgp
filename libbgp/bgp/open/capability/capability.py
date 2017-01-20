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

from libbgp.tlv import TLV


class Capability(TLV):

    def __init__(self, value, hex_value=None):
        self.value = value
        self.hex_value = hex_value


class CapabilityCode(int):

    """Capability Codes (IANA)
    http://www.iana.org/assignments/capability-codes/"""

    MULTIPROTOCOL_EXTENSIONS = 0x01  # [RFC2858]
    ROUTE_REFRESH = 0x02  # [RFC2918]

    FOUR_BYTES_ASN = 0x41  # [RFC4893]

    ENHANCED_ROUTE_REFRESH = 0x46

    CISCO_ROUTE_REFRESH = 0x80

    hex_code = {
        'afi-safi': MULTIPROTOCOL_EXTENSIONS,
        'route-refresh': ROUTE_REFRESH,
        'cisco-route-refresh': CISCO_ROUTE_REFRESH,
        'asn4': FOUR_BYTES_ASN,
        'enhanced-route-refresh': ENHANCED_ROUTE_REFRESH
    }

    def __str__(self):
        if self == self.MULTIPROTOCOL_EXTENSIONS:
            return 'afi-safi'
        elif self == self.ROUTE_REFRESH:
            return 'route-refresh'
        elif self == self.FOUR_BYTES_ASN:
            return 'asn4'
        elif self == self.ENHANCED_ROUTE_REFRESH:
            return 'enhanced-route-refresh'
        elif self == self.CISCO_ROUTE_REFRESH:
            return 'cisco-route-refresh'
