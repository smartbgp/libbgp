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

from .capability import Capability, CapabilityCode


class Capabilities(object):

    registered_capability = dict()

    def __init__(self, value, hex_value=None):
        self.value = value
        self.hex_value = hex_value

    @classmethod
    def register(cls, capa_code=None):
        def decorator(klass):
            capacode = klass.TYPE if capa_code is None else capa_code
            if capacode in cls.registered_capability:
                raise RuntimeError('duplicated capability type')
            cls.registered_capability[capacode] = klass
            return klass
        return decorator

    @staticmethod
    def pack_header(capability_type, capability_hex):
        """pack header for each capability as a Optional Parameter
        """
        capability = struct.pack('!BB', capability_type, len(capability_hex)) + capability_hex
        return struct.pack('!BB', 0x02, len(capability)) + capability

    @classmethod
    def unpack(cls, data):
        """unpack BGP Open optional parameters
        """
        capabilities = {}
        while data:
            para_type = ord(data[0:1])
            para_len = ord(data[1:2])
            if para_type != 2:
                data = data[2 + para_len:]
                continue
            # for type = 2, capability
            para_data = data[2: 2 + para_len]
            while para_data:
                capability_type = ord(para_data[0:1])
                capability_len = ord(para_data[1:2])
                capability_hex = para_data[2: 2 + capability_len]
                para_data = para_data[2 + capability_len:]
                if capability_type in cls.registered_capability:
                    capability = cls.registered_capability[capability_type].unpack(capability_hex)
                else:
                    # for unknown capability
                    capability = Capability.unpack(capability_hex)
                    capability.TYPE_STR += '(' + str(capability_type) + ')'
                if capability.TYPE_STR not in capabilities:
                    capabilities[capability.TYPE_STR] = capability.value
                else:
                    # if there already has a same
                    if not isinstance(capabilities[capability.TYPE_STR], list):
                        capabilities[capability.TYPE_STR] = [capabilities[capability.TYPE_STR]]
                    capabilities[capability.TYPE_STR].append(capability.value)

            data = data[2 + para_len:]

        return cls(value=capabilities)

    @classmethod
    def pack(cls, data):
        capabilities_hex = b''
        for capability in data:
            capability_type = CapabilityCode.hex_code.get(capability)
            if capability_type in cls.registered_capability:
                if isinstance(data[capability], list):
                    for sub_capability in data[capability]:
                        capability_hex = cls.registered_capability[capability_type].pack(sub_capability).hex_value
                        capabilities_hex += cls.pack_header(capability_type, capability_hex)
                else:
                    capability_hex = cls.registered_capability[capability_type].pack(data[capability]).hex_value
                    capabilities_hex += cls.pack_header(capability_type, capability_hex)
        return cls(value=data, hex_value=capabilities_hex)
