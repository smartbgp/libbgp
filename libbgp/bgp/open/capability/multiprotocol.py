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

import struct

from .capability import Capability
from .capability import CapabilityCode
from .capabilities import Capabilities
from libbgp.net.family import Family


@Capabilities.register()
class MultiProtocol(Capability):

    TYPE = CapabilityCode.MULTIPROTOCOL_EXTENSIONS
    TYPE_STR = str(CapabilityCode(TYPE))

    @classmethod
    def unpack(cls, data):
        afi, res, safi = struct.unpack('!HBB', data)
        return cls(value=str(Family(afi, safi)))

    @classmethod
    def pack(cls, data):
        afi, safi = Family.str_2_int(data)
        return cls(value=data, hex_value=struct.pack('!HBB', afi, 0, safi))
