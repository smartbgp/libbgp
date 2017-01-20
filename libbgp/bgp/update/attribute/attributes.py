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

from .attribute import Attribute, AttributeFlag


class Attributes(object):

    registered_attrs = dict()

    def __init__(self, value, hex_value=None):
        self.value = value
        self.hex_value = hex_value

    @classmethod
    def register(cls, attr_id=None):
        def decorator(klass):
            aid = klass.TYPE if attr_id is None else attr_id
            if aid in cls.registered_attrs:
                raise RuntimeError('duplicated attribute type')
            cls.registered_attrs[aid] = klass
            return klass
        return decorator

    def dict(self):
        return {'attr': self.value}

    @classmethod
    def unpack(cls, data, capability):
        attributes = {}
        while data:
            flags, type_code = struct.unpack('!BB', data[:2])
            if flags & AttributeFlag.EXTENDED_LENGTH:
                    attr_len = struct.unpack('!H', data[2:4])[0]
                    attr_data = data[4: 4 + attr_len]
                    data = data[4 + attr_len:]
            else:
                if isinstance(data[2], int):
                    attr_len = data[2]
                else:
                    attr_len = ord(data[2:3])
                attr_data = data[3:3 + attr_len]
                data = data[3 + attr_len:]
            if type_code in cls.registered_attrs:
                attributes.update(cls.registered_attrs[type_code].unpack(attr_data, capability).dict())
            else:
                unknown_attr = Attribute.unpack(attr_data)
                unknown_attr.TYPE = type_code
                attributes.update(unknown_attr.dict())

        return cls(value=attributes)

    @staticmethod
    def pack_header(attribute):
        return struct.pack('!B', attribute.FLAG) + struct.pack('!B', attribute.TYPE) \
            + struct.pack('!B', len(attribute.hex_value)) + attribute.hex_value

    @classmethod
    def pack(cls, data, capability):

        attributes_hex = b''
        for type_code, value in data.items():
            if type_code not in cls.registered_attrs:
                raise RuntimeError("unsupported attribute type %s", type_code)
            attributes_hex += cls.pack_header(cls.registered_attrs[type_code].pack(value, capability))
        return cls(value=data, hex_value=attributes_hex)
