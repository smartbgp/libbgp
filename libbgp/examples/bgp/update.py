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

from __future__ import print_function

from libbgp.bgp.message import Message


update_msg_dict = {
    'type': 2,
    'msg': {
        'attr': {
            1: 2,
            2: [(2, [701, 71])],
            3: '219.158.1.204',
            5: 100,
            6: 0,
            7: [71, '16.96.243.103'],
            9: '219.158.1.204',
            10: ['219.158.1.209', '0.0.0.30']
        },
        'nlri': ['192.168.1.1/32', '172.16.1.1/32'],
        'withdraw': []
    }
}

update_msg = Message.pack(update_msg_dict)
print(update_msg.hex_value)

# >>> from __future__ import print_function
# >>>
# >>> from libbgp.bgp.message import Message
# >>>
# >>>
# >>> update_msg_dict = {
# ...     'type': 2,
# ...     'msg': {
# ...         'attr': {
# ...             1: 2,
# ...             2: [(2, [701, 71])],
# ...             3: '219.158.1.204',
# ...             5: 100,
# ...             6: 0,
# ...             7: [71, '16.96.243.103'],
# ...             9: '219.158.1.204',
# ...             10: ['219.158.1.209', '0.0.0.30']
# ...         },
# ...         'nlri': ['192.168.1.1/32', '172.16.1.1/32'],
# ...         'withdraw': []
# ...     }
# ... }
# >>>
# >>> update_msg = Message.pack(update_msg_dict)
# >>> update_msg.value
# {'attr': {1: 2, 2: [(2, [701, 71])], 3: '219.158.1.204', 5: 100, 6: 0, 7: [71, '16.96.243.103'],
# 9: '219.158.1.204', 10: ['219.158.1.209', '0.0.0.30']}, 'withdraw': [], 'nlri': ['192.168.1.1/32', '172.16.1.1/32']}
# >>> update_msg.hex_value
# '\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00[\x02\x00\x00
# \x00:@\x01\x01\x02@\x02\x06\x02\x02\x02\xbd\x00G@\x03\x04\xdb\x9e\x01\xcc@\x05\x04
# \x00\x00\x00d@\x06\x01\x00\xc0\x07\x06\x00G\x10`\xf3g\x80\t\x04\xdb\x9e\x01\xcc\x80
# \n\x08\xdb\x9e\x01\xd1\x00\x00\x00\x1e \xc0\xa8\x01\x01 \xac\x10\x01\x01'
# >>> Message.unpack(update_msg.hex_value).value
# {'nlri': ['192.168.1.1/32', '172.16.1.1/32'], 'withdraw': [], 'attr': {1: 2, 2: [(2, [701, 71])],
# 3: '219.158.1.204', 5: 100, 6: 0, 7: [71, '16.96.243.103'], 9: '219.158.1.204', 10: ['219.158.1.209', '0.0.0.30']}}
# >>> Message.unpack(update_msg.hex_value).value == update_msg.value
# True
# >>>
