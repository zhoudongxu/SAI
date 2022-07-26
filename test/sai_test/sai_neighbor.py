from sai_test_base import T0TestBase
from sai_utils import *

class NoHostRouteTest(T0TestBase):
    """
    Verifies if IPv4 host route is not created according to
    SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE attribute value
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        T0TestBase.setUp(self)
          
        self.dev_port1 = self.dev_port_list[1]
        self.ipv4_addr = "01.1.1.10"
        self.mac_addr  = "00:10:10:10:10:10"
        self.nbr_entry_v4 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipaddress(self.ipv4_addr))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_v4,
                dst_mac_address=self.mac_addr,
                no_host_route=True)
        self.assertEqual(status, SAI_STATUS_SUCCESS)

    
    def noHostRouteNeighborTest(self):
        '''
        Verifies if IPv4 host route is not created according to
        SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE attribute value
        '''
        print("\nnoHostRouteNeighborTest()")

        print("Sending IPv4 packet when host route not exists")
            
        pkt = simple_udp_packet(eth_dst=ROUTER_MAC,
                                        ip_dst=self.ipv4_addr,
                                        ip_ttl=64)

        send_packet(self, self.dev_port1, pkt)
        verify_no_other_packets(self)
        print("Packet dropped")
        
    def runTest(self):
        try:
            self.noHostRouteNeighborTest()
        finally:
            pass
    
    def tearDown(self):
        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_v4)
        super().tearDown()

class NoHostRouteTestV6(T0TestBase):
    """
    Verifies if IPv4 host route is not created according to
    SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE attribute value
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        T0TestBase.setUp(self)
          
        self.dev_port1 = self.dev_port_list[1]
        self.ipv6_addr = "2001:0db8::1:10"
        self.mac_addr  = "00:10:10:10:10:10"
        self.nbr_entry_v6 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipaddress(self.ipv6_addr))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_v6,
                dst_mac_address=self.mac_addr,
                no_host_route=True)
        self.assertEqual(status, SAI_STATUS_SUCCESS)

    
    def noHostRouteNeighborTestV6(self):
        '''
        Verifies if IPv4 host route is not created according to
        SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE attribute value
        '''
        print("\nnoHostRouteNeighborTestv6()")

        print("Sending IPv4 packet when host route not exists")
            
        pkt = simple_udpv6_packet(eth_dst=ROUTER_MAC,
                                  ipv6_dst=self.ipv6_addr,
                                  ipv6_hlim=64)
                                             
        send_packet(self, self.dev_port1, pkt)
        verify_no_other_packets(self)
        print("Packet dropped")
        
    def runTest(self):
        try:
            self.noHostRouteNeighborTestV6()
        finally:
            pass
    
    def tearDown(self):
        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_v6)
        super().tearDown()

class AddHostRouteTest(T0TestBase):
    """
    Verifies if IPv4 host route is created according to
    SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE attribute value
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        T0TestBase.setUp(self)
          
        self.dev_port1 = self.dev_port_list[1]
        self.ipv4_addr = "10.1.1.10"
        self.mac_addr  = "00:10:10:10:10:10"
        self.nbr_entry_v4 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipaddress(self.ipv4_addr))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_v4,
                dst_mac_address=self.mac_addr,
                no_host_route=False)
        self.assertEqual(status, SAI_STATUS_SUCCESS)

    def addHostRouteNeighborTest(self):
        '''
        Verifies if IPv4 host route is created according to
        SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE attribute value
        '''
        print("\naddHostRouteIpv4NeighborTest()")

        pkt = simple_udp_packet(eth_dst=ROUTER_MAC,
                                ip_dst=self.ipv4_addr,
                                ip_ttl=64)

        exp_pkt = simple_udp_packet(eth_dst=self.mac_addr,
                                    eth_src=ROUTER_MAC,
                                    ip_dst=self.ipv4_addr,
                                    ip_ttl=63)

        print("Sending IPv4 packet when host route exists")
        send_packet(self, self.dev_port1, pkt)
        verify_packet_any_port(self, exp_pkt, [17, 18])
        print("Packet forwarded")

    def runTest(self):
        try:
            self.addHostRouteNeighborTest()
        finally:
            pass

    def tearDown(self):
        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_v4)
        super().tearDown()

class AddHostRouteTestV6(T0TestBase):
    """
    Verifies if IPv4 host route is created according to
    SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE attribute value
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        T0TestBase.setUp(self)
          
        self.dev_port1 = self.dev_port_list[1]
        self.ipv6_addr = "2001:0db8::1:10"
        self.mac_addr  = "00:10:10:10:10:10"
        self.nbr_entry_v6 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipaddress(self.ipv6_addr))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_v6,
                dst_mac_address=self.mac_addr,
                no_host_route=False)
        self.assertEqual(status, SAI_STATUS_SUCCESS)

    def addHostRouteNeighborTestV6(self):
        '''
        Verifies if IPv4 host route is created according to
        SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE attribute value
        '''
        print("\naddHostRouteNeighborTestV6()")

        exp_pkt_v6 = simple_udpv6_packet(eth_dst=self.mac_addr,
                                              eth_src=ROUTER_MAC,
                                              ipv6_dst=self.ipv6_addr,
                                              ipv6_hlim=63)

        pkt_v6 = simple_udpv6_packet(eth_dst=ROUTER_MAC,
                                             ipv6_dst=self.ipv6_addr,
                                             ipv6_hlim=64)

        print("Sending IPv4 packet when host route exists")
        send_packet(self, self.dev_port1, pkt_v6)
        verify_packet_any_port(self, exp_pkt_v6, [17, 18])
        print("Packet forwarded")
       
    def runTest(self):
        try:
            self.addHostRouteNeighborTestV6()
        finally:
            pass

    def tearDown(self):
        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_v6)
        super().tearDown()

class RemoveAddNeighborTestIPV4(T0TestBase):
    """
    Verifies if IPv4 host route is not created according to
    SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE attribute value
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        T0TestBase.setUp(self)
          
        self.dev_port1 = self.dev_port_list[1]
        self.ipv4_addr = "10.1.1.10"
        self.mac_addr  = "00:10:10:10:10:10"

        self.nbr_entry_v4 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipaddress(self.ipv4_addr))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_v4,
                dst_mac_address=self.mac_addr)              
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        net_route = sai_thrift_route_entry_t(vr_id=self.default_vrf, destination=sai_ipprefix(self.ipv4_addr+'/32'))
        sai_thrift_create_route_entry(self.client, net_route, next_hop_id=self.lag1_rif)       
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

    
    def RemoveAddNeighborTestV4(self):
        '''
        Verifies 
        '''
        print("\nRemoveAddNeighborTest()")

        print("Sending IPv4 packet when host route not exists")
            
        pkt = simple_udp_packet(eth_dst=ROUTER_MAC,
                                        ip_dst=self.ipv4_addr,
                                        ip_ttl=64)

        exp_pkt = simple_udp_packet(eth_dst=self.mac_addr,
                                    eth_src=ROUTER_MAC,
                                    ip_dst=self.ipv4_addr,
                                    ip_ttl=63)

        send_packet(self, self.dev_port1, pkt)
        verify_packet_any_port(self, exp_pkt, [17, 18])

        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_v4)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        pre_cpu_queue_state = sai_thrift_get_queue_stats(self.client, self.cpu_queue0)["SAI_QUEUE_STAT_PACKETS"]
        send_packet(self, self.dev_port1, pkt)
        verify_no_other_packets(self)
        print("Packet dropped")
        post_cpu_queue_state = sai_thrift_get_queue_stats(self.client, self.cpu_queue0)["SAI_QUEUE_STAT_PACKETS"]
        self.assertEqual(post_cpu_queue_state - pre_cpu_queue_state, 1)
        print(str(post_cpu_queue_state - pre_cpu_queue_state))
        sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_v4,
                dst_mac_address=self.mac_addr)              
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        send_packet(self, self.dev_port1, pkt)
        verify_packet_any_port(self, exp_pkt, [17, 18])

 
    def runTest(self):
        try:
            self.RemoveAddNeighborTestV4()
        finally:
            pass
    
    def tearDown(self):
        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_v4)
        super().tearDown()

class RemoveAddNeighborTestIPV6(T0TestBase):
    """
    Verifies if IPv6 host route is not created according to
    SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE attribute value
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        T0TestBase.setUp(self)
          
        self.dev_port1 = self.dev_port_list[1]
        self.ipv6_addr = "2001:0db8::1:10"
        self.mac_addr  = "00:10:10:10:10:10"

        self.nbr_entry_v6 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipaddress(self.ipv6_addr))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_v6,
                dst_mac_address=self.mac_addr)              
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        net_route = sai_thrift_route_entry_t(vr_id=self.default_vrf, destination=sai_ipprefix(self.ipv6_addr+'/128'))
        sai_thrift_create_route_entry(self.client, net_route, next_hop_id=self.lag1_rif)       
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

    
    def RemoveAddNeighborTestV6(self):
        '''
        Verifies 
        '''
        print("\nRemoveAddNeighborTest()")

        print("Sending IPv6 packet when host route not exists")
            
        exp_pkt_v6 = simple_udpv6_packet(eth_dst=self.mac_addr,
                                              eth_src=ROUTER_MAC,
                                              ipv6_dst=self.ipv6_addr,
                                              ipv6_hlim=63)

        pkt_v6 = simple_udpv6_packet(eth_dst=ROUTER_MAC,
                                             ipv6_dst=self.ipv6_addr,
                                             ipv6_hlim=64)
        send_packet(self, self.dev_port1, pkt_v6)
        verify_packet_any_port(self, exp_pkt_v6, [17, 18])

        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_v6)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        pre_cpu_queue_state = sai_thrift_get_queue_stats(self.client, self.cpu_queue0)["SAI_QUEUE_STAT_PACKETS"]
        send_packet(self, self.dev_port1, pkt_v6)
        verify_no_other_packets(self)
        print("Packet dropped")
        post_cpu_queue_state = sai_thrift_get_queue_stats(self.client, self.cpu_queue0)["SAI_QUEUE_STAT_PACKETS"]
        self.assertEqual(post_cpu_queue_state - pre_cpu_queue_state, 1)
        print(str(post_cpu_queue_state - pre_cpu_queue_state))
        sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_v6,
                dst_mac_address=self.mac_addr)              
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        send_packet(self, self.dev_port1, pkt_v6)
        verify_packet_any_port(self, exp_pkt_v6, [17, 18])

 
    def runTest(self):
        try:
            self.RemoveAddNeighborTestV6()
        finally:
            pass
    
    def tearDown(self):
        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_v6)
        super().tearDown()

class NeighborDiffPrefixRemoveLonger(T0TestBase):
    """
    Verifies 
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        T0TestBase.setUp(self)
          
        self.dev_port1 = self.dev_port_list[1]
        self.ipv4_addr = "10.1.1.10"
        self.mac_addr1  = "00:10:10:10:10:10"
        self.mac_addr2  = "00:20:20:20:20:20"
    
    def test_neighbor_diff_prefix_add_remove_longer(self):
        '''
        Verifies
        '''
       
        self.nbr_entry_12 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipprefix(self.ipv4_addr + '/12'))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_12,
                dst_mac_address=self.mac_addr1)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        
        self.nbr_entry_24 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipprefix(self.ipv4_addr + '/24'))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_24,
                dst_mac_address=self.mac_addr2)
        self.assertEqual(status, SAI_STATUS_SUCCESS)


        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_24)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        
        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_12)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

    def runTest(self):
        try:
            self.test_neighbor_diff_prefix_add_remove_longer()
        finally:
            pass
    
    def tearDown(self):
        super().tearDown()

class NeighborDiffPrefixRemoveLongerV6(T0TestBase):
    """
    Verifies 
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        T0TestBase.setUp(self)
          
        self.dev_port1 = self.dev_port_list[1]
        self.ipv6_addr = "2001:0db8::1:10"
        self.mac_addr1  = "00:10:10:10:10:10"
        self.mac_addr2  = "00:20:20:20:20:20"

    def test_neighbor_diff_prefix_add_remove_longer_v6(self):
        '''
        Verifies
        '''
        self.nbr_entry_64 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipprefix(self.ipv6_addr + '/64'))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_64,
                dst_mac_address=self.mac_addr1)
        self.assertEqual(status, SAI_STATUS_SUCCESS)

        self.nbr_entry_128 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipprefix(self.ipv6_addr + '/128'))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_128,
                dst_mac_address=self.mac_addr2)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        
        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_128)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        
        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_64)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

    def runTest(self):
        try:
            self.test_neighbor_diff_prefix_add_remove_longer_v6()
        finally:
            pass
    
    def tearDown(self):
        super().tearDown()

class NeighborDiffPrefixRemoveShorter(T0TestBase):
    """
    Verifies 
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        T0TestBase.setUp(self)
          
        self.dev_port1 = self.dev_port_list[1]
        self.ipv4_addr = "10.1.1.10"
        self.mac_addr1  = "00:10:10:10:10:10"
        self.mac_addr2  = "00:20:20:20:20:20"
  
    def test_neighbor_diff_prefix_add_remove_shorter(self):
        '''
        Verifies
        '''

        self.nbr_entry_24 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipprefix(self.ipv4_addr + '/24'))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_24,
                dst_mac_address=self.mac_addr1)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        
        self.nbr_entry_12 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipprefix(self.ipv4_addr + '/12'))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_12,
                dst_mac_address=self.mac_addr2)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
     
        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_12)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_24)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

    def runTest(self):
        try:
            self.test_neighbor_diff_prefix_add_remove_shorter()
        finally:
            pass
    
    def tearDown(self):
        super().tearDown()

class NhopDiffPrefixRemoveLonger(T0TestBase):
    """
    Verifies 
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        T0TestBase.setUp(self)
          
        self.dev_port1 = self.dev_port_list[1]
        self.ipv4_addr = "10.1.1.10"
        self.mac_addr1  = "00:10:10:10:10:10"
        self.mac_addr2  = "00:20:20:20:20:20"
    
    def test_neighbor_diff_prefix_add_remove_longer(self):
        '''
        Verifies
        '''
        self.nbr_entry_16 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipprefix(self.ipv4_addr + '/16'))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_16,
                dst_mac_address=self.mac_addr1)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        self.subnet_nhop_16 = sai_thrift_create_next_hop(self.client, ip=sai_ipprefix(self.ipv4_addr +'/16'), router_interface_id=self.lag1_rif, type=SAI_NEXT_HOP_TYPE_IP)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        
        self.nbr_entry_24 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipprefix(self.ipv4_addr + '/24'))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_24,
                dst_mac_address=self.mac_addr2)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        self.subnet_nhop_24 = sai_thrift_create_next_hop(self.client, ip=sai_ipprefix(self.ipv4_addr +'/24'), router_interface_id=self.lag1_rif, type=SAI_NEXT_HOP_TYPE_IP)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
      
        sai_thrift_remove_next_hop(self.client, self.subnet_nhop_24)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        
        sai_thrift_remove_next_hop(self.client, self.subnet_nhop_16)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
     

    def runTest(self):
        try:
            self.test_neighbor_diff_prefix_add_remove_longer()
        finally:
            pass
    
    def tearDown(self):
        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_16)
        super().tearDown()

class NhopDiffPrefixRemoveLongerV6(T0TestBase):
    """
    Verifies 
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        T0TestBase.setUp(self)
          
        self.dev_port1 = self.dev_port_list[1]
        self.ipv6_addr = "2001:0db8::1:10"
        self.mac_addr1  = "00:10:10:10:10:10"
        self.mac_addr2  = "00:20:20:20:20:20"
    
    def test_neighbor_diff_prefix_add_remove_longer_v6(self):
        '''
        Verifies
        '''
        self.nbr_entry_64 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipprefix(self.ipv6_addr + '/64'))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_64,
                dst_mac_address=self.mac_addr1)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        self.subnet_nhop_64 = sai_thrift_create_next_hop(self.client, ip=sai_ipprefix(self.ipv6_addr +'/64'), router_interface_id=self.lag1_rif, type=SAI_NEXT_HOP_TYPE_IP)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        
        self.nbr_entry_128 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipprefix(self.ipv6_addr + '/128'))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_128,
                dst_mac_address=self.mac_addr2)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        self.subnet_nhop_128 = sai_thrift_create_next_hop(self.client, ip=sai_ipprefix(self.ipv6_addr +'/128'), router_interface_id=self.lag1_rif, type=SAI_NEXT_HOP_TYPE_IP)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
      
        sai_thrift_remove_next_hop(self.client, self.subnet_nhop_128)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        
        sai_thrift_remove_next_hop(self.client, self.subnet_nhop_64)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
     

    def runTest(self):
        try:
            self.test_neighbor_diff_prefix_add_remove_longer_v6()
        finally:
            pass
    
    def tearDown(self):
        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_64)
        super().tearDown()

class NhopDiffPrefixRemoveShorter(T0TestBase):
    """
    Verifies 
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        T0TestBase.setUp(self)
          
        self.dev_port1 = self.dev_port_list[1]
        self.ipv4_addr = "10.1.1.10"
        self.mac_addr1  = "00:10:10:10:10:10"
        self.mac_addr2  = "00:20:20:20:20:20"

    def test_neighbor_diff_prefix_add_remove_shorter(self):
        '''
        Verifies
        '''

        self.nbr_entry_24 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipprefix(self.ipv4_addr + '/24'))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_24,
                dst_mac_address=self.mac_addr1,
                no_host_route=True)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        self.subnet_nhop_24 = sai_thrift_create_next_hop(self.client, ip=sai_ipprefix(self.ipv4_addr +'/24'), router_interface_id=self.lag1_rif, type=SAI_NEXT_HOP_TYPE_IP)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        self.nbr_entry_16 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipprefix(self.ipv4_addr + '/16'))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_16,
                dst_mac_address=self.mac_addr2,
                no_host_route=True)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        self.subnet_nhop_16 = sai_thrift_create_next_hop(self.client, ip=sai_ipprefix(self.ipv4_addr +'/16'), router_interface_id=self.lag1_rif, type=SAI_NEXT_HOP_TYPE_IP)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        sai_thrift_remove_next_hop(self.client, self.subnet_nhop_16)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        sai_thrift_remove_next_hop(self.client, self.subnet_nhop_24)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        

    def runTest(self):
        try:
            self.test_neighbor_diff_prefix_add_remove_shorter()
        finally:
            pass
    
    def tearDown(self):
        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_16)
        super().tearDown()


class NhopDiffPrefixRemoveLongerV6(T0TestBase):
    """
    Verifies 
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        T0TestBase.setUp(self)
          
        self.dev_port1 = self.dev_port_list[1]
        self.ipv6_addr = "2001:0db8::1:10"
        self.mac_addr1  = "00:10:10:10:10:10"
        self.mac_addr2  = "00:20:20:20:20:20"
    
    def test_neighbor_diff_prefix_add_remove_longer_v6(self):
        '''
        Verifies
        '''
        self.nbr_entry_64 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipprefix(self.ipv6_addr + '/64'))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_64,
                dst_mac_address=self.mac_addr1)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        self.subnet_nhop_64 = sai_thrift_create_next_hop(self.client, ip=sai_ipprefix(self.ipv6_addr +'/64'), router_interface_id=self.lag1_rif, type=SAI_NEXT_HOP_TYPE_IP)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        
        self.nbr_entry_128 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipprefix(self.ipv6_addr + '/128'))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_128,
                dst_mac_address=self.mac_addr2)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        self.subnet_nhop_128 = sai_thrift_create_next_hop(self.client, ip=sai_ipprefix(self.ipv6_addr +'/128'), router_interface_id=self.lag1_rif, type=SAI_NEXT_HOP_TYPE_IP)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
      
        sai_thrift_remove_next_hop(self.client, self.subnet_nhop_128)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        
        sai_thrift_remove_next_hop(self.client, self.subnet_nhop_64)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
     

    def runTest(self):
        try:
            self.test_neighbor_diff_prefix_add_remove_longer_v6()
        finally:
            pass
    
    def tearDown(self):
        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_64)
        super().tearDown()

class NhopDiffPrefixRemoveShorterV6(T0TestBase):
    """
    Verifies 
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        T0TestBase.setUp(self)
          
        self.dev_port1 = self.dev_port_list[1]
        self.ipv6_addr = "2001:0db8::1:10"
        self.mac_addr1  = "00:10:10:10:10:10"
        self.mac_addr2  = "00:20:20:20:20:20"

    def test_neighbor_diff_prefix_add_remove_shorter_v6(self):
        '''
        Verifies
        '''

        self.nbr_entry_128 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipprefix(self.ipv6_addr + '/128'))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_128,
                dst_mac_address=self.mac_addr1,
                no_host_route=True)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        self.subnet_nhop_128 = sai_thrift_create_next_hop(self.client, ip=sai_ipprefix(self.ipv6_addr +'/128'), router_interface_id=self.lag1_rif, type=SAI_NEXT_HOP_TYPE_IP)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        self.nbr_entry_64 = sai_thrift_neighbor_entry_t(
                rif_id=self.lag1_rif,
                ip_address=sai_ipprefix(self.ipv6_addr + '/64'))
        status = sai_thrift_create_neighbor_entry(
                self.client,
                self.nbr_entry_64,
                dst_mac_address=self.mac_addr2,
                no_host_route=True)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        self.subnet_nhop_64 = sai_thrift_create_next_hop(self.client, ip=sai_ipprefix(self.ipv6_addr +'/64'), router_interface_id=self.lag1_rif, type=SAI_NEXT_HOP_TYPE_IP)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        sai_thrift_remove_next_hop(self.client, self.subnet_nhop_64)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        sai_thrift_remove_next_hop(self.client, self.subnet_nhop_128)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        

    def runTest(self):
        try:
            self.test_neighbor_diff_prefix_add_remove_shorter_v6()
        finally:
            pass
    
    def tearDown(self):
        sai_thrift_remove_neighbor_entry(self.client, self.nbr_entry_64)
        super().tearDown()

