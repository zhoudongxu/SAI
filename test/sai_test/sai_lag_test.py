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

from sai_test_base import T0TestBase
from sai_utils import *


class LagConfigTest(T0TestBase):
    """
    Verify the load-balance of l3
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        T0TestBase.setUp(self)

    def load_balance_on_src_ip(self):
        self.recv_dev_port_idxs = self.get_dev_port_indexes(self.servers[11][1].l3_lag_obj.member_port_indexs)
        ip_dst = self.servers[11][1].ipv4
        pkt1 = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                 eth_src=self.servers[1][1].mac,
                                 ip_dst=ip_dst,
                                 ip_src=self.servers[1][1].ipv4,
                                 ip_id=105,
                                 ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                 eth_src=self.servers[2][1].mac,
                                 ip_dst=ip_dst,
                                 ip_src=self.servers[2][1].ipv4,
                                 ip_id=105,
                                 ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                     eth_src=ROUTER_MAC,
                                     ip_dst=ip_dst,
                                     ip_src=self.servers[1][1].ipv4,
                                     ip_id=105,
                                     ip_ttl=63)
        exp_pkt2 = simple_tcp_packet(eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                     eth_src=ROUTER_MAC,
                                     ip_dst=ip_dst,
                                     ip_src=self.servers[2][1].ipv4,
                                     ip_id=105,
                                     ip_ttl=63)
        import pdb    
        pdb.set_trace()                        
        send_packet(self, self.dut.port_obj_list[1].dev_port_index, pkt1)
        verify_packet_any_port(
            self, exp_pkt1, self.recv_dev_port_idxs)
        send_packet(self, self.dut.port_obj_list[1].dev_port_index, pkt2)
        verify_packet_any_port(
            self, exp_pkt2, self.recv_dev_port_idxs)

    def runTest(self):
        try:
            self.load_balance_on_src_ip()
        finally:
            pass

    def tearDown(self):
        super().tearDown()


class LoadbalanceOnSrcPortTest(T0TestBase):
    """
    Test load balance of l3 by source port.
    """

    def setUp(self):
        """
        Test the basic setup process
        """
        T0TestBase.setUp(self)

    def runTest(self):
        """
        1. Generate different packets by updating src port
        2. send these packets on port1
        3. Check if packets are received on ports of lag1 equally
        """
        try:
            print("Lag l3 load balancing test based on src port")
            
            self.recv_dev_port_idxs = self.get_dev_port_indexes(self.servers[11][1].l3_lag_obj.member_port_indexs)
            max_itrs = 99
            begin_port = 2000
            rcv_count = [0, 0]
            for i in range(0, max_itrs):
                src_port = begin_port + i
                pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                        eth_src=self.servers[1][1].mac,
                                        ip_dst=self.servers[11][1].ipv4,
                                        ip_src=self.servers[1][1].ipv4,
                                        tcp_sport=src_port,
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                            eth_src=ROUTER_MAC,
                                            ip_dst=self.servers[11][1].ipv4,
                                            ip_src=self.servers[1][1].ipv4,
                                            tcp_sport=src_port,
                                            ip_id=105,
                                            ip_ttl=63)
                send_packet(self, self.dut.port_obj_list[1].dev_port_index, pkt)
                rcv_idx, _ = verify_packet_any_port(
                    self, exp_pkt, self.recv_dev_port_idxs)
                print('src_port={}, rcv_port={}'.format(src_port, rcv_idx))
                rcv_count[rcv_idx] += 1
            print(rcv_count)
            for i in range(0, 2):
                self.assertTrue((rcv_count[i] >= ((max_itrs/2) * 0.8)),
                                "Not all paths are equally balanced")
        finally:
            pass

    def tearDown(self):
        super().tearDown()


class LoadbalanceOnDesPortTest(T0TestBase):
    """
    Test load balance of l3 by destinstion port.
    """

    def setUp(self):
        """
        Test the basic setup process
        """
        T0TestBase.setUp(self)

    def runTest(self):
        """
        1. Generate different packets by updating des port
        2. send these packets on port1
        3. Check if packets are received on ports of lag1 equally
        """
        try:
            print("Lag l3 load balancing test based on des port")
            
            self.recv_dev_port_idxs = self.get_dev_port_indexes(self.servers[11][1].l3_lag_obj.member_port_indexs)
            max_itrs = 99
            begin_port = 2000
            rcv_count = [0, 0]
            for i in range(0, max_itrs):
                des_port = begin_port + i
                pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                        eth_src=self.servers[1][1].mac,
                                        ip_dst=self.servers[11][1].ipv4,
                                        ip_src=self.servers[1][1].ipv4,
                                        tcp_dport=des_port,
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                            eth_src=ROUTER_MAC,
                                            ip_dst=self.servers[11][1].ipv4,
                                            ip_src=self.servers[1][1].ipv4,
                                            tcp_dport=des_port,
                                            ip_id=105,
                                            ip_ttl=63)
                send_packet(self, self.dut.port_obj_list[1].dev_port_index, pkt)
                rcv_idx, _ = verify_packet_any_port(
                    self, exp_pkt, self.recv_dev_port_idxs)
                print('des_port={}, rcv_port={}'.format(des_port, rcv_idx))
                rcv_count[rcv_idx] += 1

            print(rcv_count)
            for i in range(0, 2):
                self.assertTrue(
                    (rcv_count[i] >= ((max_itrs/2) * 0.8)), "Not all paths are equally balanced")
        finally:
            pass

    def tearDown(self):
        super().tearDown()


class LoadbalanceOnSrcIPTest(T0TestBase):
    """
    Test load balance of l3 by source IP.
    """

    def setUp(self):
        """
        Test the basic setup process
        """
        T0TestBase.setUp(self)

    def runTest(self):
        """
        1. Generate different packets by updating src ip
        2. send these packets on port1
        3. Check if packets are received on ports of lag1 equally
        """
        try:
            print("Lag l3 load balancing test based on src IP")
            
            self.recv_dev_port_idxs = self.get_dev_port_indexes(self.servers[11][1].l3_lag_obj.member_port_indexs)
            max_itrs = 99
            rcv_count = [0, 0]
            for i in range(1, max_itrs):
                pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                        eth_src=self.servers[1][i].mac,
                                        ip_dst=self.servers[11][1].ipv4,
                                        ip_src=self.servers[1][i].ipv4,
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                            eth_src=ROUTER_MAC,
                                            ip_dst=self.servers[11][1].ipv4,
                                            ip_src=self.servers[1][i].ipv4,
                                            ip_id=105,
                                            ip_ttl=63)
                send_packet(self, self.dut.port_obj_list[1].dev_port_index, pkt)
                rcv_idx, _ = verify_packet_any_port(
                    self, exp_pkt, self.recv_dev_port_idxs)
                print('ip_src={}, rcv_port={}'.format(
                    self.servers[1][i].ipv4, rcv_idx))
                rcv_count[rcv_idx] += 1

            print(rcv_count)
            for i in range(0, 2):
                self.assertTrue(
                    (rcv_count[i] >= ((max_itrs/2) * 0.8)), "Not all paths are equally balanced")
        finally:
            pass

    def tearDown(self):
        super().tearDown()


class LoadbalanceOnDesIPTest(T0TestBase):
    """
    Test load balance of l3 by destinstion IP.
    """

    def setUp(self):
        """
        Test the basic setup process
        """
        T0TestBase.setUp(self)

    def runTest(self):
        """
        1. Generate different packets by updating des ip
        2. send these packets on port1
        3. Check if packets are received on ports of lag1 equally
        """
        try:
            print("Lag l3 load balancing test based on des IP")
            
            self.recv_dev_port_idxs = self.get_dev_port_indexes(self.servers[11][1].l3_lag_obj.member_port_indexs)
            max_itrs = 99
            rcv_count = [0, 0]
            for i in range(1, max_itrs):
                pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                        eth_src=self.servers[1][1].mac,
                                        ip_dst=self.servers[11][i].ipv4,
                                        ip_src=self.servers[1][1].ipv4,
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                            eth_src=ROUTER_MAC,
                                            ip_dst=self.servers[11][i].ipv4,
                                            ip_src=self.servers[1][1].ipv4,
                                            ip_id=105,
                                            ip_ttl=63)
                send_packet(self, self.dut.port_obj_list[1].dev_port_index, pkt)
                rcv_idx, _ = verify_packet_any_port(
                    self, exp_pkt, self.recv_dev_port_idxs)
                print('des_src={}, rcv_port={}'.format(
                    self.servers[1][1].ipv4, rcv_idx))
                rcv_count[rcv_idx] += 1

            print(rcv_count)
            for i in range(0, 2):
                self.assertTrue(
                    (rcv_count[i] >= ((max_itrs/2) * 0.8)), "Not all paths are equally balanced")
        finally:
            pass

    def tearDown(self):
        super().tearDown()


"""
Skip test for broadcom, can't load balance on protocol such as tcp and udp.Item: 15023123
"""

class LoadbalanceOnProtocolTest(T0TestBase):
    """
    Test load balance of l3 by protocol.
    """
    def setUp(self):
        """
        Test the basic setup process
        """                  
        T0TestBase.setUp(
            self,
            skip_reason ="SKIP! Skip test for broadcom, can't load balance on protocol such as tcp and udp.Item: 15023123")

    def runTest(self):
        """
        1. Generate different packets with tcp and icmp
        2. send these packets on port1
        3. Check if packets are received on ports of lag1 equally
        """
        try:
            print("Lag l3 load balancing test based on protocol")
            
            self.recv_dev_port_idxs = self.get_dev_port_indexes(self.servers[11][1].l3_lag_obj.member_port_indexs)
            max_itrs = 99
            rcv_count = [0, 0]
            for i in range(0, max_itrs):
                if i % 2 == 0:
                    pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                            eth_src=self.servers[1][1].mac,
                                            ip_dst=self.servers[11][1].ipv4,
                                            ip_src=self.servers[1][1].ipv4,
                                            ip_id=105,
                                            ip_ttl=64)
                    exp_pkt = simple_tcp_packet(eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                                eth_src=ROUTER_MAC,
                                                ip_dst=self.servers[11][1].ipv4,
                                                ip_src=self.servers[1][1].ipv4,
                                                ip_id=105,
                                                ip_ttl=63)
                else:
                    print("icmp")
                    pkt = simple_icmp_packet(eth_dst=ROUTER_MAC,
                                             eth_src=self.servers[1][1].mac,
                                             ip_dst=self.servers[11][1].ipv4,
                                             ip_src=self.servers[1][1].ipv4,
                                             ip_id=105,
                                             ip_ttl=64)
                    exp_pkt = simple_icmp_packet(eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                                 eth_src=ROUTER_MAC,
                                                 ip_dst=self.servers[11][1].ipv4,
                                                 ip_src=self.servers[1][1].ipv4,
                                                 ip_id=105,
                                                 ip_ttl=63)
                send_packet(self, self.dut.port_obj_list[1].dev_port_index, pkt)
                rcv_idx, _ = verify_packet_any_port(
                    self, exp_pkt, self.recv_dev_port_idxs)
                print('des_src={}, rcv_port={}'.format(
                    self.servers[1][1].ipv4, rcv_idx))
                rcv_count[rcv_idx] += 1

            print(rcv_count)
            for i in range(0, 2):
                self.assertTrue(
                    (rcv_count[i] >= ((max_itrs/2) * 0.8)), "Not all paths are equally balanced")
        finally:
            pass

    def tearDown(self):
        super().tearDown()


class DisableEgressTest(T0TestBase):
    """
    When disable egress on a lag member, we expect traffic drop on the disabled lag member.
    """

    def setUp(self):
        """
        Test the basic setup process
        """
        T0TestBase.setUp(self)

    def runTest(self):
        """
        1. Generate different packets by updating src_port
        2. send these packets on port1
        3. Check if packets are received on ports of lag1 equally
        4. Disable port18 egress
        5. Generate different packets by updating src_port
        6. send these packets on port1
        7. Check if packets are received on port17
        """
        try:
            print("Lag disable egress lag member test")
            
            pkts_num = 10
            begin_port = 2000
            exp_drop = []
            self.recv_dev_port_idxs = self.get_dev_port_indexes(self.servers[11][1].l3_lag_obj.member_port_indexs)
            for i in range(0, pkts_num):
                src_port = begin_port + i
                pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                        eth_src=self.servers[1][1].mac,
                                        ip_dst=self.servers[11][1].ipv4,
                                        ip_src=self.servers[1][1].ipv4,
                                        tcp_sport=src_port,
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                            eth_src=ROUTER_MAC,
                                            ip_dst=self.servers[11][1].ipv4,
                                            ip_src=self.servers[1][1].ipv4,
                                            tcp_sport=src_port,
                                            ip_id=105,
                                            ip_ttl=63)
                send_packet(self, self.dut.port_obj_list[1].dev_port_index, pkt)
                rcv_idx, _ = verify_packet_any_port(
                    self, exp_pkt, self.recv_dev_port_idxs)
                if rcv_idx == 18:
                    exp_drop.append(src_port)

            # disable egress of lag member: port18
            print("disable port18 egress")
            status = sai_thrift_set_lag_member_attribute(self.client,
                                                         self.servers[11][1].l3_lag_obj.lag_members[1],
                                                         egress_disable=True)
            self.assertEqual(status, SAI_STATUS_SUCCESS)

            for i in range(0, pkts_num):
                src_port = begin_port + i
                pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                        eth_src=self.servers[1][1].mac,
                                        ip_dst=self.servers[11][1].ipv4,
                                        ip_src=self.servers[1][1].ipv4,
                                        tcp_sport=src_port,
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                            eth_src=ROUTER_MAC,
                                            ip_dst=self.servers[11][1].ipv4,
                                            ip_src=self.servers[1][1].ipv4,
                                            tcp_sport=src_port,
                                            ip_id=105,
                                            ip_ttl=63)
                send_packet(self, self.dut.port_obj_list[1].dev_port_index, pkt)
                if src_port in exp_drop:
                    verify_no_packet(self, exp_pkt, self.get_dev_port_index(18))
                verify_packet(self, exp_pkt, self.get_dev_port_index(17))
        finally:
            pass

    def tearDown(self):
        status = sai_thrift_set_lag_member_attribute(self.client,
                                                     self.servers[11][1].l3_lag_obj.lag_members[1],
                                                     egress_disable=False)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        super().tearDown()


"""
Skip test for broadcom, can't disable ingress of lag member
Item: 14988584
"""
class DisableIngressTest(T0TestBase):
    """
    When disable ingress on a lag member, we expect traffic drop on the disabled lag member.
    """

    def setUp(self):
        """
        Test the basic setup process
        """                        
        T0TestBase.setUp(
            self,
            skip_reason = "SKIP! Skip test for broadcom, can't disable ingress of lag member. Item: 14988584")

    def runTest(self):
        """
        1. Generate different packets by updating src_port
        2. send these packets on port 18
        3. Check if packets are received on port1
        4. Disable port18 ingress
        5. Generate same different packets in step 1 by updating src_port
        6. send these packets on port 18
        7. Check if packets are received on port1
        """
        try:
            print("Lag disable ingress lag member test")
            
            pkts_num = 10
            begin_port = 2000
            for i in range(0, pkts_num):
                src_port = begin_port + i
                pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                        eth_src=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                        ip_dst=self.servers[1][1].ipv4,
                                        ip_src=self.servers[11][1].ipv4,
                                        tcp_sport=src_port,
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_dst=self.servers[1][1].mac,
                                            eth_src=ROUTER_MAC,
                                            ip_dst=self.servers[1][1].ipv4,
                                            ip_src=self.servers[11][1].ipv4,
                                            tcp_sport=src_port,
                                            ip_id=105,
                                            ip_ttl=63)
                send_packet(self, self.dut.port_obj_list[18].dev_port_index, pkt)
                verify_packet(self, exp_pkt, self.dut.port_obj_list[1].dev_port_index)
            # git disable ingress of lag member: port18
            print("disable port18 ingress")
            status = sai_thrift_set_lag_member_attribute(
                self.client, self.lag_list[0].lag_members[1], ingress_disable=True)
            self.assertEqual(status, SAI_STATUS_SUCCESS)

            for i in range(0, pkts_num):
                src_port = begin_port + i
                pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                        eth_src=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                        ip_dst=self.servers[1][1].ipv4,
                                        ip_src=self.servers[11][1].ipv4,
                                        tcp_sport=src_port,
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_dst=self.servers[1][1].mac,
                                            eth_src=ROUTER_MAC,
                                            ip_dst=self.servers[1][1].ipv4,
                                            ip_src=self.servers[11][1].ipv4,
                                            tcp_sport=src_port,
                                            ip_id=105,
                                            ip_ttl=63)
                send_packet(self, self.dut.port_obj_list[18].dev_port_index, pkt)
                verify_no_packet(self, exp_pkt, self.dut.port_obj_list[1].dev_port_index)
        finally:
            pass

    def tearDown(self):
        super().tearDown()


class RemoveLagMemberTest(T0TestBase):
    """
    When remove lag member, we expect traffic drop on the removed lag member.
    """

    def setUp(self):
        """
        Test the basic setup process
        """
        T0TestBase.setUp(self)

    def runTest(self):
        """
        1. Generate different packets by updating src_port
        2. Send these packets on port1
        3. Check if packets are received on ports of lag1 equally
        4. Remove port18 in lag1 
        5. Generate same different packets in step 1 by updating src_port
        6. Send these packets on port1
        7. Check if packets aren't received on port18
        """
        try:
            print("Lag remove lag member test")
            
            self.recv_dev_port_idxs = self.get_dev_port_indexes(self.servers[11][1].l3_lag_obj.member_port_indexs)
            pkts_num = 10
            begin_port = 2000
            for i in range(0, pkts_num):
                src_port = begin_port + i
                pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                        eth_src=self.servers[1][1].mac,
                                        ip_dst=self.servers[11][1].ipv4,
                                        ip_src=self.servers[1][1].ipv4,
                                        tcp_sport=src_port,
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                            eth_src=ROUTER_MAC,
                                            ip_dst=self.servers[11][1].ipv4,
                                            ip_src=self.servers[1][1].ipv4,
                                            tcp_sport=src_port,
                                            ip_id=105,
                                            ip_ttl=63)
                send_packet(self, self.dut.port_obj_list[1].dev_port_index, pkt)
                verify_packet_any_port(
                    self, exp_pkt, self.recv_dev_port_idxs)

            self.lag_configer.remove_lag_member_by_port_idx(
                lag_obj=self.servers[11][1].l3_lag_obj, port_idx=18)

            for i in range(0, pkts_num):
                src_port = begin_port + i
                pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                        eth_src=self.servers[1][1].mac,
                                        ip_dst=self.servers[11][1].ipv4,
                                        ip_src=self.servers[1][1].ipv4,
                                        tcp_sport=src_port,
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                            eth_src=ROUTER_MAC,
                                            ip_dst=self.servers[11][1].ipv4,
                                            ip_src=self.servers[1][1].ipv4,
                                            tcp_sport=src_port,
                                            ip_id=105,
                                            ip_ttl=63)
                send_packet(self, self.dut.port_obj_list[1].dev_port_index, pkt)
                verify_no_packet(self, exp_pkt, self.get_dev_port_index(18))
            self.lag_configer.create_lag_member(lag_obj=self.servers[11][1].l3_lag_obj,
                                                lag_port_idxs=range(18, 19))
        finally:
            pass

    def tearDown(self):
        super().tearDown()


class AddLagMemberTest(T0TestBase):
    """
    When  add lag member, we expect traffic appear on the added lag member.
    """

    def setUp(self):
        """
        set up configurations
        """
        T0TestBase.setUp(self)

    def runTest(self):
        """
        1. Generate different packets by updating tcp_sport
        2. Send these packets on port1
        3. Check if packets are received on ports of lag1 equally
        4. Add port21 as lag1 member
        5. Generate same different packets in step 1 by updating tcp_sport
        6. Send these packets on port1
        7. Check if packets are received on lag1(port 17,18,21)
        """
        try:
            print("Lag add lag member test")
            
            self.recv_dev_port_idxs = self.get_dev_port_indexes(self.servers[11][1].l3_lag_obj.member_port_indexs)
            pkts_num = 10
            begin_port = 2000
            rcv_count = [0, 0, 0]
            for i in range(0, pkts_num):
                src_port = begin_port + i
                pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                        eth_src=self.servers[1][1].mac,
                                        ip_dst=self.servers[11][1].ipv4,
                                        ip_src=self.servers[1][1].ipv4,
                                        tcp_sport=src_port,
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                            eth_src=ROUTER_MAC,
                                            ip_dst=self.servers[11][1].ipv4,
                                            ip_src=self.servers[1][1].ipv4,
                                            tcp_sport=src_port,
                                            ip_id=105,
                                            ip_ttl=63)
                send_packet(self, self.dut.port_obj_list[1].dev_port_index, pkt)
                verify_packet_any_port(
                    self, exp_pkt, self.recv_dev_port_idxs)
            print("add port21 into lag1")
            self.lag_configer.create_lag_member(lag_obj=self.servers[11][1].l3_lag_obj,
                                                lag_port_idxs=range(21, 22))
            self.recv_dev_port_idxs = self.get_dev_port_indexes(self.servers[11][1].l3_lag_obj.member_port_indexs)
            for i in range(0, pkts_num):
                src_port = begin_port + i
                pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                        eth_src=self.servers[1][1].mac,
                                        ip_dst=self.servers[11][1].ipv4,
                                        ip_src=self.servers[1][1].ipv4,
                                        tcp_sport=src_port,
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                            eth_src=ROUTER_MAC,
                                            ip_dst=self.servers[11][1].ipv4,
                                            ip_src=self.servers[1][1].ipv4,
                                            tcp_sport=src_port,
                                            ip_id=105,
                                            ip_ttl=63)
                send_packet(self, self.dut.port_obj_list[1].dev_port_index, pkt)
                rcv_idx, _ = verify_packet_any_port(
                    self, exp_pkt, self.recv_dev_port_idxs)
                rcv_count[rcv_idx] += 1
            for cnt in rcv_count:
                self.assertGreater(
                    cnt, 0, "each member in lag1 should receive pkt")
            self.lag_configer.remove_lag_member_by_port_idx(
                lag_obj=self.servers[11][1].l3_lag_obj, port_idx=21)
        finally:
            pass

    def tearDown(self):
        super().tearDown()


class IndifferenceIngressPortTest(T0TestBase):
    """
    Verify the ingress ports should not be as a hash factor in lag load balance.
    Forwarding the same packet from different ingress ports, if only the ingress
    port changed, the load balance should not happen among lag members.
    """

    def setUp(self):
        T0TestBase.setUp(self)

    def runTest(self):
        try:
            pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                    eth_src=self.servers[1][1].mac,
                                    ip_dst=self.servers[11][1].ipv4,
                                    ip_src=self.servers[1][1].ipv4,
                                    ip_id=105,
                                    ip_ttl=64)
            exp_pkt = simple_tcp_packet(eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                        eth_src=ROUTER_MAC,
                                        ip_dst=self.servers[11][1].ipv4,
                                        ip_src=self.servers[1][1].ipv4,
                                        ip_id=105,
                                        ip_ttl=63)

            exp_port_idx = -1
            exp_port_list = self.get_dev_port_indexes(self.servers[11][1].l3_lag_obj.member_port_indexs)
            for i in range(1, 9):
                send_packet(self, self.dut.port_obj_list[i].dev_port_index, pkt)
                if exp_port_idx == -1:
                    exp_port_idx, _ = verify_packet_any_port(
                        self, exp_pkt, exp_port_list)
                else:
                    verify_packet(self, exp_pkt, exp_port_list[exp_port_idx])
        finally:
            pass

    def tearDown(self):
        super().tearDown()
