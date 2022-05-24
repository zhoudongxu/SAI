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

"""
This file contains class for brcm specified functions.
"""
import pdb
from socket import AddressFamily
from platform_helper.common_sai_helper import * # pylint: disable=wildcard-import; lgtm[py/polluting-import]

DEFAULT_IP_V4_PREFIX = '0.0.0.0/0'
DEFAULT_IP_V6_PREFIX = '0000:0000:0000:0000:0000:0000:0000:0000'
#Todo make those two parameters from input
LOCAL_IP_128V6_PREFIX = 'fe80::f68e:38ff:fe16:bc75/128'
LOCAL_IP_10V6_PREFIX = 'fe80::/10'

IPV4_USED_BY_TUNNEL = '10.1.0.32/32'
IPV6_USED_BY_TUNNEL = 'fc00:1::32/128'

PORT_MTU=9122
ROUTER_INTERFACE_MTU=9100

class BrcmT0SaiHelper(CommonSaiHelper):
    """
    This class contains broadcom(brcm) specified functions for the platform setup and test context configuration.
    """

    platform = 'brcm'
    role_config = 't0'

    def normal_setup(self):
        """
        Normal setup
        """
        print("BrcmT0SaiHelper::normal_setup")
        self.start_switch()
        self.config_meta_port()


    def config_meta_port(self):
        """
        Default configuation, with metadata and ports configurations.
        """
        self.get_port_list()
        self.create_default_route_intf()
        self.get_default_1q_bridge()
        self.get_default_vlan()
        self.remove_vlan_member()
        self.remove_bridge_port()
        self.create_default_v4_v6_route_entry()
        self.create_local_v6_route()
        self.create_host_intf()
        self.turn_on_port_admin_state()
        self.create_tunnel()
        #self.set_port_serdes()


    def start_switch(self):
        """
        Start switch and wait seconds for a warm up.
        """
        switch_init_wait = 1

        self.switch_id = sai_thrift_create_switch(
            self.client, init_switch=True, src_mac_address=ROUTER_MAC)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        print("Waiting for switch to get ready, {} seconds ...".format(switch_init_wait))
        time.sleep(switch_init_wait)


    def get_port_list(self):
        """
        Set the class variable port_list.
        
        Output variable:
            self.port_list
        """
        port_list = sai_thrift_object_list_t(count=100)
        p_list = sai_thrift_get_switch_attribute(
            self.client, port_list=port_list)
        self.port_list = p_list['port_list'].idlist


    def create_default_route_intf(self):
        """
        Create default route interface on loop back interface.

        Output variables:
            self.default_vrf
            self.lpbk_intf
        """
        print("Create loop back interface...")
        attr = sai_thrift_get_switch_attribute(self.client, default_virtual_router_id=True)
        self.default_vrf = attr['default_virtual_router_id']
        self.assertNotEqual(self.default_vrf, 0)
        self.lpbk_intf = sai_thrift_create_router_interface(
            self.client, type=SAI_ROUTER_INTERFACE_TYPE_LOOPBACK,
            virtual_router_id=self.default_vrf, mtu=ROUTER_INTERFACE_MTU)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        self.overlay_loop_itf1 = sai_thrift_create_router_interface(
            self.client, type=SAI_ROUTER_INTERFACE_TYPE_LOOPBACK,
            virtual_router_id=self.default_vrf, mtu=ROUTER_INTERFACE_MTU)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        self.overlay_loop_itf2 = sai_thrift_create_router_interface(
            self.client, type=SAI_ROUTER_INTERFACE_TYPE_LOOPBACK,
            virtual_router_id=self.default_vrf, mtu= ROUTER_INTERFACE_MTU)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)


    def get_default_1q_bridge(self):
        """
        Get defaule 1Q bridge.

        Output variables:
            self.default_1q_bridge_id
        """
        print("Get default 1Q bridge...")
        def_attr = sai_thrift_get_switch_attribute(
            self.client, default_1q_bridge_id=True)
        self.default_1q_bridge_id = def_attr['default_1q_bridge_id']


    def get_default_vlan(self):
        """
        Get defaule vlan.

        Output variables:
            self.default_vlan_id
        """
        print("Get default vlan...")
        def_attr = sai_thrift_get_switch_attribute(
            self.client, default_vlan_id=True)
        self.default_vlan_id = def_attr['default_vlan_id']

    
    def remove_vlan_member(self):
        """
        Remove vlan member when init the environment.
        """
        print("Remove vlan and members...")
        vlan_member_list = sai_thrift_object_list_t(count=100)
        mbr_list = sai_thrift_get_vlan_attribute(
            self.client, self.default_vlan_id, member_list=vlan_member_list)
        vlan_members = mbr_list['SAI_VLAN_ATTR_MEMBER_LIST'].idlist

        for member in vlan_members:
            sai_thrift_remove_vlan_member(self.client, vlan_member_oid=member)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)


    def remove_bridge_port(self):
        """
        Remove bridge ports.
        """
        print("Remove bridge ports...")
        bridge_port_list = sai_thrift_object_list_t(count=100)
        bp_list = sai_thrift_get_bridge_attribute(
            self.client, self.default_1q_bridge_id, port_list=bridge_port_list)
        bp_ports = bp_list['port_list'].idlist
        for port in bp_ports:
            sai_thrift_remove_bridge_port(self.client, port)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)


    def create_default_v4_v6_route_entry(self):
        """
        Create default v4 and v6 route entry.

        Output variable:
            self.default_ipv6_route_entry
            self.default_ipv4_route_entry
        """
        print("Create default v4 & v6 route entry...")
        v6_default = sai_thrift_ip_prefix_t(
            addr_family=1, addr=sai_thrift_ip_addr_t(ip6=DEFAULT_IP_V6_PREFIX),
            mask=sai_thrift_ip_addr_t(ip6=DEFAULT_IP_V6_PREFIX))
        entry = sai_thrift_route_entry_t(
            vr_id=self.default_vrf,
            destination=v6_default,
            switch_id=self.switch_id)
        self.default_ipv6_route_entry = sai_thrift_create_route_entry(
            self.client, route_entry=entry, packet_action=SAI_PACKET_ACTION_DROP)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        entry = sai_thrift_route_entry_t(
            vr_id=self.default_vrf,
            destination=sai_ipprefix(DEFAULT_IP_V4_PREFIX),
            switch_id=self.switch_id)
        self.default_ipv4_route_entry = sai_thrift_create_route_entry(
            self.client, route_entry=entry, packet_action=SAI_PACKET_ACTION_DROP)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)


    def create_local_v6_route(self):
        """
        Create local v6 route base on the configuration of the actual switch.

        Output variable:
            self.local_10v6_route_entry
            self.local_128v6_route_entry
        """
        #Todo make the v6 prefix from actual device config.

        print("Create Local V6 route...")
        entry = sai_thrift_route_entry_t(
            vr_id=self.default_vrf,
            destination=sai_ipprefix(LOCAL_IP_10V6_PREFIX),
            switch_id=self.switch_id)
        self.local_10v6_route_entry = sai_thrift_create_route_entry(
            self.client, route_entry=entry, packet_action=SAI_PACKET_ACTION_FORWARD)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        entry = sai_thrift_route_entry_t(
            vr_id=self.default_vrf,
            destination=sai_ipprefix(LOCAL_IP_128V6_PREFIX),
            switch_id=self.switch_id)
        self.local_128v6_route_entry = sai_thrift_create_route_entry(
            self.client, route_entry=entry, packet_action=SAI_PACKET_ACTION_FORWARD)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)


    def create_host_intf(self):
        """
        Craete host interface.
        Steps:
         1. create host table entry
         2. create host interface trap
         3. set host interface base on the port_config.int (this file contains the lanes, name and index information.)

        Output variables:
            self.host_intf_table_id
            self.ports_config
            self.port_to_hostif_map
            self.hostifs
        """
        print("Create Host intfs...")
        self.host_intf_table_id = sai_thrift_create_hostif_table_entry(
            self.client, type=SAI_HOSTIF_TABLE_ENTRY_TYPE_WILDCARD,
            channel_type=SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_NETDEV_PHYSICAL_PORT)
        attr = sai_thrift_get_switch_attribute(self.client, default_trap_group=True)
        self.default_trap_group = attr['default_trap_group']
        sai_thrift_create_hostif_trap(
            self.client, trap_type=SAI_HOSTIF_TRAP_TYPE_TTL_ERROR, packet_action=SAI_PACKET_ACTION_TRAP,
            trap_group=self.default_trap_group, trap_priority=0)

        self.ports_config = self.parsePortConfig(
            self.test_params['port_config_ini'])
        self.port_to_hostif_map = {}
        self.hostifs = []
        for i, _ in enumerate(self.port_list):
            try:
                setattr(self, 'port%s' % i, self.port_list[i])
                hostif = sai_thrift_create_hostif(
                    self.client, 
                    type=SAI_HOSTIF_TYPE_NETDEV,
                    obj_id=self.port_list[i],
                    name=self.ports_config[i]['name'])
                setattr(self, 'host_if%s' % i, hostif)
                self.port_to_hostif_map[i]=hostif
                sai_thrift_set_hostif_attribute(self.client, hostif_oid=hostif, oper_status=False)
                self.hostifs.append(hostif)
            except BaseException as e:
                print("Cannot create hostif, error : {}".format(e))


    def turn_on_port_admin_state(self):
        """
        Turn on port admin state
        """
        print("Set port...")
        for i, port in enumerate(self.port_list):
            sai_thrift_set_port_attribute(
                self.client, port_oid=port, mtu=PORT_MTU, admin_state=True)


    def set_port_serdes(self):
        """
        Set prot Serdes.
        """
        print("Recreate Port serdes...")
        for i, port in enumerate(self.port_list):
            sai_thrift_set_port_attribute(
                self.client, port_oid=port, mtu=PORT_MTU, admin_state=True)

    def create_policier_trap_group(self):
        """
        Create hostif trap group and policifer
        """
        policer_id = sai_thrift_create_policer(self.client, meter_type=SAI_METER_TYPE_PACKETS, mode=SAI_POLICER_MODE_SR_TCM, cbs=6000, cir=6000, red_packet_action=SAI_PACKET_ACTION_DROP)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        trap_group_id = sai_thrift_create_hostif_trap_group(self.client, queue=1, policer=policer_id)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_create_hostif_trap(self.client, trap_type=SAI_HOSTIF_TRAP_TYPE_IP2ME, trap_group= trap_group_id, packet_action= SAI_PACKET_ACTION_TRAP, trap_priority=1)
        
        #priority=4 groups:
        packet_action_list = [SAI_PACKET_ACTION_TRAP, SAI_PACKET_ACTION_COPY, SAI_PACKET_ACTION_TRAP]
        trap_type_set = [[SAI_HOSTIF_TRAP_TYPE_BGP, SAI_HOSTIF_TRAP_TYPE_BGPV6, SAI_HOSTIF_TRAP_TYPE_LACP], [SAI_HOSTIF_TRAP_TYPE_ARP_REQUEST, SAI_HOSTIF_TRAP_TYPE_ARP_RESPONSE, SAI_HOSTIF_TRAP_TYPE_IPV6_NEIGHBOR_DISCOVERY], [SAI_HOSTIF_TRAP_TYPE_DHCP, SAI_HOSTIF_TRAP_TYPE_DHCPV6, SAI_HOSTIF_TRAP_TYPE_LLDP, SAI_HOSTIF_TRAP_TYPE_UDLD]]
        for i in range(3):
            if i==1:
               policer_id = sai_thrift_create_policer(self.client, meter_type=SAI_METER_TYPE_PACKETS, mode=SAI_POLICER_MODE_SR_TCM, cbs=600, cir=600, red_packet_action=SAI_PACKET_ACTION_DROP)
               self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
            else:
               policer_id = None

            trap_group_id = sai_thrift_create_hostif_trap_group(self.client, queue=4, policer=policer_id)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
            trap_type_group= trap_type_set[i]
            packet_action_internal = packet_action_list[i]
            for trap in trap_type_group:
                sai_thrift_create_hostif_trap(self.client, trap_type=trap, trap_group= trap_group_id, packet_action= packet_action_internal, trap_priority=4)
                self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
    
    def set_hostif_oper_status(self):
        """
        Set hostif oper stauts sd true
        """
        for hostif in  self.hostifs:
            sai_thrift_set_hostif_attribute(self.client, hostif_oid=hostif, oper_status=True)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

    def create_tunnel(self):
        """
        Create  tunnle interface  
        """
        #self.create_route_entry_by_ip(IPV4_USED_BY_TUNNEL, IPV6_USED_BY_TUNNEL)
        #The router entries are used by creating tunnel table term, but these teerms are unnecessary now.
        self.tunnel_itf_v4 = sai_thrift_create_tunnel(self.client, type = SAI_TUNNEL_TYPE_IPINIP, underlay_interface= self.lpbk_intf, overlay_interface= self.overlay_loop_itf1, decap_ecn_mode=SAI_TUNNEL_DECAP_ECN_MODE_COPY_FROM_OUTER, decap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, decap_dscp_mode=SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        self.tunnel_itf_v6 = sai_thrift_create_tunnel(self.client, type = SAI_TUNNEL_TYPE_IPINIP, underlay_interface= self.lpbk_intf, overlay_interface= self.overlay_loop_itf2, decap_ecn_mode=SAI_TUNNEL_DECAP_ECN_MODE_COPY_FROM_OUTER, decap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, decap_dscp_mode=SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)


    def create_route_entry_by_ip(self, ipv4, ipv6):
        """
        Create local v6 route base on the configuration of the actual switch.

        Output variable:
            self.local_10v6_route_entry
            self.local_128v6_route_entry
        """
       
        print("Create  route entry ...")
        entry_v4 = sai_thrift_route_entry_t(
            vr_id=self.default_vrf,
            destination=sai_ipprefix(ipv4),
            switch_id=self.switch_id)
        sai_thrift_create_route_entry(
            self.client, route_entry=entry_v4, packet_action=SAI_PACKET_ACTION_FORWARD)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        entry_v6 = sai_thrift_route_entry_t(
            vr_id=self.default_vrf,
            destination=sai_ipprefix(ipv6),
            switch_id=self.switch_id)
        sai_thrift_create_route_entry(
            self.client, route_entry=entry_v6, packet_action=SAI_PACKET_ACTION_FORWARD)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        
