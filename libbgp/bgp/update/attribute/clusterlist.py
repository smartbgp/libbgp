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

from libbgp.exception import BGPNotification
from libbgp.net import IPAddress
from .attribute import Attribute, AttributeID, AttributeFlag
from .attributes import Attributes


@Attributes.register()
class ClusterList(Attribute):
    """
        CLUSTER_LIST is a new, optional, non-transitive BGP attribute of Type
    code 10. It is a sequence of CLUSTER_ID values representing the
    reflection path that the route has passed.
    When an RR reflects a route, it MUST prepend the local CLUSTER_ID to
    the CLUSTER_LIST. If the CLUSTER_LIST is empty, it MUST create a new
    one. Using this attribute an RR can identify if the routing
    information has looped back to the same cluster due to
    misconfiguration. If the local CLUSTER_ID is found in the
    CLUSTER_LIST, the advertisement received SHOULD be ignored.
    (RFC 4456 Page 7)
    """

    TYPE = AttributeID.CLUSTER_LIST
    FLAG = AttributeFlag.OPTIONAL

    @classmethod
    def unpack(cls, data, capability):

        """
        Parse culster list
        :param data
        """
        cluster_list = []
        if len(data) % 4 != 0:
            raise BGPNotification(3, 5)
        while data:
            cluster_list.append(IPAddress.unpack(data[0:4]))
            data = data[4:]
        return cls(value=cluster_list)

    @classmethod
    def pack(cls, data, capability):
        try:
            return cls(value=data, hex_value=b''.join([IPAddress.pack(cluster_id) for cluster_id in data]))
        except:
            raise BGPNotification(3, 5)
