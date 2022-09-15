# Copyright (c) 2021 Microsoft Open Technologies, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#    THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR
#    CONDITIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT
#    LIMITATION ANY IMPLIED WARRANTIES OR CONDITIONS OF TITLE, FITNESS
#    FOR A PARTICULAR PURPOSE, MERCHANTABILITY OR NON-INFRINGEMENT.
#
#    See the Apache Version 2.0 License for specific language governing
#    permissions and limitations under the License.
#
#    Microsoft would like to thank the following companies for their review and
#    assistance with these files: Intel Corporation, Mellanox Technologies Ltd,
#    Dell Products, L.P., Facebook, Inc., Marvell International Ltd.
#
#

# IPv4
DEFAULT_IP_V4_PREFIX = '0.0.0.0/0'
DEFAULT_IP_V6_PREFIX = '0000:0000:0000:0000:0000:0000:0000:0000'
FDB_MAC_PREFIX = '00:01:01'

LOCAL_IP_128V6_PREFIX = 'fe80::f68e:38ff:fe16:bc75/128'
LOCAL_IP_10V6_PREFIX = 'fe80::/10'

# MAC
ROUTER_MAC = '00:77:66:55:44:00'
"""Route mac address"""
BROADCAST_MAC = "ff:ff:ff:ff:ff:ff"
"""broadcast mac address"""
MULTICAST_MAC = "01:00:5e:11:22:33"
"""multicast mac address"""

# Others
PORT_MTU = 9122
THRIFT_PORT = 9092

FDB_SERVER_NUM = '99'
"""Stand for the server in the fdb"""
FDB_T1_NUM = '01'
FDB_T0_NUM = '00'

SERVER_IPV4_PATTERN = '192.168.{}.{}'
T0_IPV4_PREFIX = '10.0.{}.{}'
T1_IPV4_PATTERN = '10.1.{}.{}'

SERVER_IPV6_PATTERN = 'fc02::{}:{}'
T0_IPV6_PREFIX = 'fc00:0::{}:{}'
T1_IPV6_PATTERN = 'fc00:1::{}:{}'
