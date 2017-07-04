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


class TestTermination(unittest.TestCase):

    def test_unpack(self):

        data_hex = b'\x03\x00\x00\x00\x0c\x05\x00\x01\x00\x02\x00\x00'
        self.assertEqual(
            {
                'type': Message.TERMINATION,
                'msg': {'reason': Message.unpack(data_hex).reason_codict[0]}
            },
            Message.unpack(data_hex).dict())
