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
import binascii

from .message import Message


"""These messages contain information that could be used by the
monitoring station to observe interesting events that occur on the
router.
"""
# 0 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                         Stats Count                           |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Each counter is encoded as follows,
# 0 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |           Stat Type           |            Stat Len           |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                           Stat Data                           |
# ~                                                               ~
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


@Message.register
class StatsReport(Message):

    TYPE = Message.STATISTICS_REPORT
    TYPE_STR = 'stats-report'

    state_type = {
        0: 'Number of prefixes rejected by inbound policy',
        1: 'Number of (known) duplicate prefix advertisements',
        2: 'Number of (known) duplicate withdraws',
        3: 'Number of updates invalidated due to CLUSTER_LIST loop',
        4: 'Number of updates invalidated due to AS_PATH loop',
        5: 'Number of updates invalidated due to ORIGINATOR_ID',
        6: 'Number of updates invalidated due to AS_CONFED loop',
        7: 'Number of routes in Adj-RIBs-In',
        8: 'Number of routes in Loc-RIB',
        9: 'Number of routes in per-AFI/SAFI Adj-RIB-In',
        10: 'Number of routes in per-AFI/SAFI Loc-RIB',
        11: 'Number of updates subjected to treat-as-withdraw',
        12: 'Number of prefixes subjected to treat-as-withdraw',
        13: 'Number of duplicate update messages received',
        32767: 'SRTT',
        32768: 'RTTO',
        32769: 'RTV',
        32770: 'KRTT',
        32771: 'minRTT',
        32772: 'maxRTT',
        32773: 'ACK hold',
        32774: 'Datagrams'
    }

    @classmethod
    def unpack(cls, data):
        count_num = struct.unpack('!I', data[0:4])[0]
        stats_dict = {}
        data = data[4:]
        while count_num:
            stat_type, stat_len = struct.unpack('!HH', data[0:4])
            stat_data = data[4:4 + stat_len]
            data = data[4 + stat_len:]
            stat_value = int(binascii.b2a_hex(stat_data), 16)
            stats_dict[stat_type] = stat_value
            count_num -= 1
        return cls(value=stats_dict)
