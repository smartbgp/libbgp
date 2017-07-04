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

# https://tools.ietf.org/html/rfc4271#section-4.3
# +-----------------------------------------------------+
# |   Withdrawn Routes Length (2 octets)                |
# +-----------------------------------------------------+
# |   Withdrawn Routes (variable)                       |
# +-----------------------------------------------------+
# |   Total Path Attribute Length (2 octets)            |
# +-----------------------------------------------------+
# |   Path Attributes (variable)                        |
# +-----------------------------------------------------+
# |   Network Layer Reachability Information (variable) |
# +-----------------------------------------------------+

import struct

from libbgp.bgp.message import Message
from libbgp.net import IPAddress
from libbgp.bgp.update.attribute.attributes import Attributes
from libbgp.exception import BGPNotification


@Message.register
class Update(Message):

    TYPE = Message.UPDATE
    TYPE_STR = 'update'

    @classmethod
    def unpack(cls, data, length, capability):

        results_dict = dict()

        # get each part of the message
        withdraw_len = struct.unpack('!H', data[:2])[0]
        withdraw_data = data[2:withdraw_len + 2]
        results_dict['withdraw'] = cls.unpack_nlri(withdraw_data, capability.get('addpath'))

        attr_len = struct.unpack('!H', data[withdraw_len + 2:withdraw_len + 4])[0]
        attribute_data = data[withdraw_len + 4:withdraw_len + 4 + attr_len]

        nlri_data = data[withdraw_len + 4 + attr_len:]
        results_dict['nlri'] = cls.unpack_nlri(nlri_data, capability.get('addpath'))

        results_dict.update(Attributes.unpack(attribute_data, capability).dict())

        return cls(value=results_dict, length=length)

    @classmethod
    def pack(cls, data, capability):
        attributes_hex = Attributes.pack(data.get('attr') or {}, capability).hex_value
        nlri_hex = cls.pack_nlri(data.get('nlri') or [], capability.get('addpath'))
        withdraw_hex = cls.pack_nlri(data.get('withdraw') or [], capability.get('addpath'))
        if nlri_hex and attributes_hex:
            msg_body = struct.pack('!H', 0) + struct.pack('!H', len(attributes_hex)) + attributes_hex + nlri_hex
        elif not nlri_hex and attributes_hex:
            msg_body = struct.pack('!H', 0) + struct.pack('!H', len(attributes_hex)) + attributes_hex + nlri_hex
        elif withdraw_hex:
            msg_body = struct.pack('!H', len(withdraw_hex)) + withdraw_hex + struct.pack('!H', 0)
        return cls(value=data, hex_value=msg_body)

    @staticmethod
    def unpack_nlri(data, addpath=False):
        """
        Parses an RFC4271 encoded blob of BGP prefixes into a list

        :param data: hex data
        :param addpath: support addpath or not
        :return: prefix_list
        """
        prefixes = []
        postfix = data
        while len(postfix) > 0:
            # for python2 and python3
            if addpath:
                path_id = struct.unpack('!I', postfix[0:4])[0]
                postfix = postfix[4:]
            if isinstance(postfix[0], int):
                prefix_len = postfix[0]
            else:
                prefix_len = ord(postfix[0:1])
            if prefix_len > 32:
                raise BGPNotification(3, 10, 'Prefix Length larger than 32')
            octet_len, remainder = int(prefix_len / 8), prefix_len % 8
            if remainder > 0:
                # prefix length doesn't fall on octet boundary
                octet_len += 1
            tmp = postfix[1:octet_len + 1]
            # for python2 and python3
            if isinstance(postfix[0], int):
                prefix_data = [i for i in tmp]
            else:
                prefix_data = [ord(i[0:1]) for i in tmp]
            # Zero the remaining bits in the last octet if it didn't fall
            # on an octet boundary
            if remainder > 0:
                prefix_data[-1] &= 255 << (8 - remainder)
            prefix_data = prefix_data + list(str(0)) * 4
            prefix = "%s.%s.%s.%s" % (tuple(prefix_data[0:4])) + '/' + str(prefix_len)
            if not addpath:
                prefixes.append(prefix)
            else:
                prefixes.append({'prefix': prefix, 'path_id': path_id})
            # Next prefix
            postfix = postfix[octet_len + 1:]

        return prefixes

    @staticmethod
    def pack_nlri(nlri, add_path=False):
        """
        constructs NLRI prefix list
        :param nlri: prefix list
        :param add_path: support add path or not
        """
        nlri_raw_hex = b''
        for prefix in nlri:
            if add_path and isinstance(prefix, dict):
                path_id = prefix.get('path_id')
                prefix = prefix.get('prefix')
                nlri_raw_hex += struct.pack('!I', path_id)
            ip, masklen = prefix.split('/')
            ip_hex = IPAddress.pack(ip)
            masklen = int(masklen)
            if 16 < masklen <= 24:
                ip_hex = ip_hex[0:3]
            elif 8 < masklen <= 16:
                ip_hex = ip_hex[0:2]
            elif masklen <= 8:
                ip_hex = ip_hex[0:1]
            nlri_raw_hex += struct.pack('!B', masklen) + ip_hex
        return nlri_raw_hex
