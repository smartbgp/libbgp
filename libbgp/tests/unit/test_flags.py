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

from libbgp.flag import ByteFlag


class TestByteFlag(unittest.TestCase):

    def test_dict(self):

        ByteFlag.FLAGS = ['A', 'B', 'C', 'D']
        flags = ByteFlag(0b10100000)
        self.assertEqual({'B': 0, 'C': 1, 'A': 1, 'D': 0}, flags.dict())
