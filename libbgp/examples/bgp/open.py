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

# decode BGP Open Message

open_msg_binary = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff' \
                  b'\xff\xff\xff\x00\x35\x01\x04\xea\x60\x00\xb4\x48\xa3' \
                  b'\xe2\xbe\x18\x02\x06\x01\x04\x00\x01\x00\x01\x02\x02' \
                  b'\x80\x00\x02\x02\x02\x00\x02\x06\x41\x04\x00\x00\xea\x60'

open_msg = Message.unpack(open_msg_binary)
print(open_msg.dict())

# >>> from __future__ import print_function
# >>> from libbgp.bgp.message import Message
# >>> open_msg_binary = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff' \
# ...                   b'\xff\xff\xff\x00\x35\x01\x04\xea\x60\x00\xb4\x48\xa3' \
# ...                   b'\xe2\xbe\x18\x02\x06\x01\x04\x00\x01\x00\x01\x02\x02' \
# ...                   b'\x80\x00\x02\x02\x02\x00\x02\x06\x41\x04\x00\x00\xea\x60'
# >>>
# >>> open_msg = Message.unpack(open_msg_binary)
# >>> open_msg.value
# {'hold-time': 180, 'version': 4, 'asn': 60000, 'capabilities': {'cisco-route-refresh': True,
# 'route-refresh': True, 'asn4': 60000, 'afi-safi': 'ipv4-unicast'}, 'bgp-id': '72.163.226.190'}
# >>> open_msg.dict()
# {'msg': {'hold-time': 180, 'version': 4, 'asn': 60000, 'capabilities': {'cisco-route-refresh': True,
# 'route-refresh': True, 'asn4': 60000, 'afi-safi': 'ipv4-unicast'}, 'bgp-id': '72.163.226.190'}, 'type': 1}
# >>>

# pabgp
open_msg_dict = {
    'msg': {
        'hold-time': 180,
        'version': 4,
        'asn': 60000,
        'capabilities': {
            'cisco-route-refresh': True,
            'route-refresh': True,
            'asn4': 60000,
            'afi-safi': 'ipv4-unicast'
        },
        'bgp-id': '72.163.226.190'
    },
    'type': 1
}

open_msg = Message.pack(open_msg_dict)

# >>> from __future__ import print_function
# >>> from libbgp.bgp.message import Message
# >>> open_msg_dict = {
# ...     'msg': {
# ...         'hold-time': 180,
# ...         'version': 4,
# ...         'asn': 60000,
# ...         'capabilities': {
# ...             'cisco-route-refresh': True,
# ...             'route-refresh': True,
# ...             'asn4': 60000,
# ...             'afi-safi': 'ipv4-unicast'
# ...         },
# ...         'bgp-id': '72.163.226.190'
# ...     },
# ...     'type': 1
# ... }
# >>> open_msg = Message.pack(open_msg_dict)
# >>> open_msg.value
# {'hold-time': 180, 'version': 4, 'asn': 60000, 'capabilities': {'cisco-route-refresh': True,
# 'afi-safi': 'ipv4-unicast', 'asn4': 60000, 'route-refresh': True}, 'bgp-id': '72.163.226.190'}
# >>> open_msg.hex_value
# '\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x005\x01\x04\xea`\x00\xb4H
# \xa3\xe2\xbe\x18\x02\x02\x80\x00\x02\x06\x01\x04\x00\x01\x00\x01\x02\x06A\x04\x00\x00\xea`\x02\x02\x02\x00'
# >>> Message.unpack(open_msg.hex_value).value
# {'hold-time': 180, 'version': 4, 'asn': 60000, 'capabilities': {'cisco-route-refresh': True,
# 'route-refresh': True, 'asn4': 60000, 'afi-safi': 'ipv4-unicast'}, 'bgp-id': '72.163.226.190'}
# >>>
