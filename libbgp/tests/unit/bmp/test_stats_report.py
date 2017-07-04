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


class TestInitiation(unittest.TestCase):

    def test_unpack(self):

        data_hex = b'\x03\x00\x00\x00\xe4\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                   b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0a\x4b\x2c\x0b' \
                   b'\x00\x00\xfd\xfe\x0a\x4b\x2c\x0b\x00\x00\x00\x00\x00\x00\x00\x00' \
                   b'\x00\x00\x00\x11\x00\x00\x00\x04\x00\x00\x00\x00\x00\x01\x00\x04' \
                   b'\x00\x00\x00\x00\x00\x02\x00\x04\x00\x00\x00\x00\x00\x03\x00\x04' \
                   b'\x00\x00\x00\x00\x00\x04\x00\x04\x00\x00\x00\x00\x00\x05\x00\x04' \
                   b'\x00\x00\x00\x00\x00\x06\x00\x04\x00\x00\x00\x00\x00\x07\x00\x08' \
                   b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x08\x00\x00\x00\x00' \
                   b'\x00\x00\x00\x00\x7f\xff\x00\x08\x00\x00\x00\x00\x00\x00\x03\xe8' \
                   b'\x80\x00\x00\x08\x00\x00\x00\x00\x00\x00\x03\xeb\x80\x01\x00\x08' \
                   b'\x00\x00\x00\x00\x00\x00\x00\x03\x80\x02\x00\x08\x00\x00\x00\x00' \
                   b'\x00\x00\x03\xeb\x80\x03\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00' \
                   b'\x80\x04\x00\x08\x00\x00\x00\x00\x00\x00\x03\xe8\x80\x05\x00\x08' \
                   b'\x00\x00\x00\x00\x00\x00\x00\xc8\x80\x06\x00\x08\x00\x00\x00\x00' \
                   b'\x00\x00\x05\xb4'
        msg_dict = {
            'msg': {
                0: 0,
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0,
                6: 0,
                7: 0,
                8: 0,
                32767: 1000,
                32768: 1003,
                32769: 3,
                32770: 1003,
                32771: 0,
                32772: 1000,
                32773: 200,
                32774: 1460},
            'type': 1
        }
        self.assertEqual(
            msg_dict,
            Message.unpack(data_hex).dict())
