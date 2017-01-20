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

from libbgp.bgp.update.attribute.atomicaggregate import AtomicAggregate
from libbgp.exception import BGPNotification


class TestAtomicAggregate(unittest.TestCase):

    def test_unpack(self):

        self.assertEqual(0, AtomicAggregate.unpack(b'\x00', {}).value)
        self.assertRaises(BGPNotification, AtomicAggregate.unpack, b'\x00\x01', {})

    def test_pack(self):
        self.assertEqual(b'\x00', AtomicAggregate.pack(0, {}).hex_value)
