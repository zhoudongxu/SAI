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
from typing import Dict, List
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from data_module.vlan import Vlan
    from data_module.lag import Lag
    from data_module.nexthop import Nexthop
    from data_module.nexthop_group import NexthopGroup
    from data_module.port import Port


class Dut(object):
    """
    Dut config, represent the dut object in the test structure.
    Class attributes:
            default_vrf 
            default_ipv6_route_entry 
            default_ipv4_route_entry 
            loopback_intf 
            local_10v6_route_entry 
            local_128v6_route_entry
            routev4_list
            routev6_list 

            # vlan
            default_vlan_id 
            vlans

            # switch
            switch_id 

            # fdb
            default_vlan_fdb_list 
            vlan_10_fdb_list 
            vlan_20_fdb_list 

            # port
            default_1q_bridge_id 
            default_trap_group 
            host_intf_table_id 
            port_list
            hostif_list 
            rif_list       

            # lag
            lag1 
            lag2

            #L3
            nexthopv4_list: next hop id list
            nexthopv6_list: next hop id list
            neighborv4_list
            neighborv6_list

            # nexthop group
            nhp_grpv4_list: Nexthop group list, contains exthopv4 objects
            nhp_grpv6_list: Nexthop group list, contains exthopv6 objects
    """

    def __init__(self):
        """
        Init all of the class attributes
        """

        self.cpu_port = None

        # router
        self.default_vrf = None
        self.default_ipv6_route_entry = None
        self.default_ipv4_route_entry = None
        self.loopback_intf = None
        self.local_10v6_route_entry = None
        self.local_128v6_route_entry = None
        self.routev4_list: List = []
        self.routev6_list: List = []
        # nexthop
        self.nexthopv4_list: List[Nexthop] = []
        """
        nexthop list, contains nexthop objects
        """
        self.nexthopv6_list: List[Nexthop] = []
        """
        nexthop list, contains nexthop objects
        """
        self.neighborv4_list = []
        self.neighborv6_list = []

        # vlan
        self.default_vlan_id = None
        self.vlans: Dict[int, Vlan] = {}
        """
        Vlan object list, key: int, Value: Vlan object
        """

        # switch
        self.switch_id = None

        # fdb
        self.fdb_entry_list: List = []
        """
        FDB entry list
        """

        # port
        self.default_1q_bridge_id = None
        self.default_trap_group = None
        """
        Local device port index list, 0, 1, ...
        """
        self.host_intf_table_id = None
        self.port_obj_list: List['Port'] = []
        """
        Port object list
        """
        self.port_id_list = []
        """
        port id list, use to present all the port ids
        """
        self.hostif_list = None
        """
        Host interface list
        """
        self.default_bridge_port_list = []
        """
        Default bridge port list
        """
        self.host_if_port_idx_map = []
        """
        list in order of the host interface create sequence, and with the value for port index
        """
        self.host_if_name_list = []
        """
        List of the interface name
        """

        self.rif_list: List = []
        """
        Rif list. save the rif object id.
        """

        # lag
        self.lag_list: List[Lag] = []

        # nexthop group
        self.nhp_grpv4_list: List[NexthopGroup] = []
        """
        Nexthop group list, contains nexthop ipv4 objects
        """
        self.nhp_grpv6_list: List[NexthopGroup] = []
        """
        Nexthop group list, contains nexthop ipv6 objects
        """
