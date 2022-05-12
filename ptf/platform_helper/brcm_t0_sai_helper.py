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
LOCAL_IP_128V6_PREFIX = 'fe80::f68e:38ff:fe16:bc75/128'
LOCAL_IP_10V6_PREFIX = 'fe80::/10'
PORT_MTU=9122
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

        port_list = sai_thrift_object_list_t(count=100)
        p_list = sai_thrift_get_switch_attribute(
            self.client, port_list=port_list)
        self.port_list = p_list['port_list'].idlist
        

        print("Create loop back interface...")
        attr = sai_thrift_get_switch_attribute(self.client, default_virtual_router_id=True)
        self.default_vrf = attr['default_virtual_router_id']
        self.assertNotEqual(self.default_vrf, 0)
        self.lpbk_intf = sai_thrift_create_router_interface(
            self.client, type=SAI_ROUTER_INTERFACE_TYPE_LOOPBACK,
            virtual_router_id=self.default_vrf)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        print("Get default 1Q bridge...")
        def_attr = sai_thrift_get_switch_attribute(
            self.client, default_1q_bridge_id=True, default_vlan_id=True)
        self.default_1q_bridge_id = def_attr['default_1q_bridge_id']
        self.default_vlan_id = def_attr['default_vlan_id'] 


        print("Remove vlan and members...")
        vlan_member_list = sai_thrift_object_list_t(count=100)
        mbr_list = sai_thrift_get_vlan_attribute(
            self.client, self.default_vlan_id, member_list=vlan_member_list)
        vlan_members = mbr_list['SAI_VLAN_ATTR_MEMBER_LIST'].idlist
        count = mbr_list['SAI_VLAN_ATTR_MEMBER_LIST'].count

        for member in vlan_members:
            sai_thrift_remove_vlan_member(self.client, vlan_member_oid=member)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        print("Remove bridge ports...")
        bridge_port_list = sai_thrift_object_list_t(count=100)
        bp_list = sai_thrift_get_bridge_attribute(
            self.client, self.default_1q_bridge_id, port_list=bridge_port_list)
        bp_ports = bp_list['port_list'].idlist
        for port in bp_ports:
            sai_thrift_remove_bridge_port(self.client, port)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        print("Create default v4 & v6 route entry...")
        v6_default = sai_thrift_ip_prefix_t(
            addr_family=1, addr=sai_thrift_ip_addr_t(ip6='0000:0000:0000:0000:0000:0000:0000:0000'), 
            mask=sai_thrift_ip_addr_t(ip6='0000:0000:0000:0000:0000:0000:0000:0000'))
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

        print("Set port...")
        for i, port in enumerate(self.port_list):
            sai_thrift_set_port_attribute(
                self.client, port_oid=port, mtu=PORT_MTU, admin_state=True)
        
        print("Recreate Port serdes...")
        for i, port in enumerate(self.port_list):
            sai_thrift_set_port_attribute(
                self.client, port_oid=port, mtu=PORT_MTU, admin_state=True)


    def start_switch(self):
        """
        Start switch and wait seconds for a warm up.
        """
        switch_init_wait = 5

        self.switch_id = sai_thrift_create_switch(
            self.client, init_switch=True, src_mac_address=ROUTER_MAC)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        print("Waiting for switch to get ready, {} seconds ...".format(switch_init_wait))
        #time.sleep(switch_init_wait)
