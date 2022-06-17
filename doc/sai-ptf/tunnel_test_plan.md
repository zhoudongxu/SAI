# SAI Tunnel Test plan
- [SAI Tunnel Test plan](#sai-tunnel-test-plan)
- [Overriew](#overriew)
- [Test Configuration](#test-configuration)
- [Test Execution](#test-execution)
  - [Test Group1: TTL Pipe Mode](#test-group1-ttl-pipe-mode)
    - [Case1: encap_ttl_set_pipe_mode_v4](#case1-encap_ttl_set_pipe_mode_v4)
    - [Case2: encap_ttl_set_pipe_mode_v6](#case2-encap_ttl_set_pipe_mode_v6)
    - [Case3: decap_ttl_set_pipe_mode_v4](#case3-decap_ttl_set_pipe_mode_v4)
    - [Case4: decap_ttl_set_pipe_mode_v6](#case4-decap_ttl_set_pipe_mode_v6)
    - [Testing Data Packet](#testing-data-packet)
  - [Test Group2: TTL Uniform Mode](#test-group2-ttl-uniform-mode)
    - [Case5: encap_ttl_set_uniform_mode_v4](#case5-encap_ttl_set_uniform_mode_v4)
    - [Case6: encap_ttl_set_uniform_mode_v6](#case6-encap_ttl_set_uniform_mode_v6)
    - [Case7: decap_ttl_set_uniform_mode_v4](#case7-decap_ttl_set_uniform_mode_v4)
    - [Case8: decap_ttl_set_uniform_mode_v6](#case8-decap_ttl_set_uniform_mode_v6)
  - [Test Group3: DSCP in Pipe Mode](#test-group3-dscp-in-pipe-mode)
    - [Case9: encap_dscp_in_pipe_mode_v4](#case9-encap_dscp_in_pipe_mode_v4)
    - [Case10: encap_dscp_in_pipe_mode_v6](#case10-encap_dscp_in_pipe_mode_v6)
    - [Case11: decap_dscp_in_pipe_mode_v4](#case11-decap_dscp_in_pipe_mode_v4)
    - [Case12: decap_dscp_in_pipe_mode_v6](#case12-decap_dscp_in_pipe_mode_v6)
  - [Test Group4: DSCP QoS Map in Pipe Mode](#test-group4-dscp-qos-map-in-pipe-mode)
    - [Case13: encap_dscp_remap_in_pipe_mode_v4](#case13-encap_dscp_remap_in_pipe_mode_v4)
    - [Case14: encap_dscp_remap_in_pipe_mode_v6](#case14-encap_dscp_remap_in_pipe_mode_v6)
    - [Case15: decap_dscp_remap_in_pipe_mode_v4](#case15-decap_dscp_remap_in_pipe_mode_v4)
    - [Case16: decap_dscp_remap_in_pipe_mode_v6](#case16-decap_dscp_remap_in_pipe_mode_v6)
  - [Test Group5: DSCP in Uniform Mode](#test-group5-dscp-in-uniform-mode)
    - [Case17: encap_dscp_remap_in_Uniform_mode_v4](#case17-encap_dscp_remap_in_uniform_mode_v4)
    - [Case18: encap_dscp_remap_in_Uniform_mode_v6](#case18-encap_dscp_remap_in_uniform_mode_v6)
    - [Case19: decap_dscp_remap_in_Uniform_mode_v4](#case19-decap_dscp_remap_in_uniform_mode_v4)
    - [Case20: decap_dscp_remap_in_Uniform_mode_v6](#case20-decap_dscp_remap_in_uniform_mode_v6)
  - [Test Group6: DSCP QOS Map in Uniform Mode](#test-group6-dscp-qos-map-in-uniform-mode)
    - [Case21: encap_dscp_remap_in_Uniform_mode_v4](#case21-encap_dscp_remap_in_uniform_mode_v4)
    - [Case22: encap_dscp_remap_in_Uniform_mode_v6](#case22-encap_dscp_remap_in_uniform_mode_v6)
    - [Case23: decap_dscp_remap_in_Uniform_mode_v4](#case23-decap_dscp_remap_in_uniform_mode_v4)
    - [Case24: decap_dscp_remap_in_Uniform_mode_v6](#case24-decap_dscp_remap_in_uniform_mode_v6)
  - [Test Group7: Test tunnel termination](#test-group7-test-tunnel-termination)
    - [case25:test_tunnel_term_with_correct_Dst_ip](#case25test_tunnel_term_with_correct_dst_ip)
    - [case26:test_tunnel_term_with_error_Dst_ip](#case26test_tunnel_term_with_error_dst_ip)
  - [Todo Test Group7: IPinIP P2MP](#todo-test-group7-ipinip-p2mp)
    - [Case27: test_p2mp_decap_v4](#case27-test_p2mp_decap_v4)
    - [Case27: test_p2mp_encap_v4](#case27-test_p2mp_encap_v4)
    - [Case27: test_p2mp_decap_v6](#case27-test_p2mp_decap_v6)
    - [Case27: test_p2mp_encap_v6](#case27-test_p2mp_encap_v6)
  - [To Do Verify tunnel + ECMP](#to-do-verify-tunnel--ecmp)
# Overriew
The purpose of this test plan is to test the Tunnel function from SAI.


# Test Configuration

For the test configuration, please refer to Tunnel configuration section of the file 
  - [Config_t0](./config_data/config_t0.md)
  
**Note. All the tests will be based on the configuration above, if any additional configuration is required, it will be specified in the Test case.**

# Test Execution

## Test Group1: TTL Pipe Mode
	
### Case1: encap_ttl_set_pipe_mode_v4
### Case2: encap_ttl_set_pipe_mode_v6
### Case3: decap_ttl_set_pipe_mode_v4
### Case4: decap_ttl_set_pipe_mode_v6


### Testing Objective <!-- omit in toc --> 
This verifies if TTL field is user-defined for the outer header on encapsulation and TTL field of the inner header remains the same on decapsulation when using TTL pipe mode.

### Testing Data Packet
```Python
Encap packet:
    input_pkt = simple_tcp_packet(
                eth_dst=ROUTER_MAC,
                eth_src=port1_nb_mac,
                ip_dst=vm_ip_from_lag2_nb,
                ip_src=port1_nb_ip,
                ip_id=108,
                ip_ttl=64)

    inner_pkt = simple_tcp_packet(
                eth_dst=tunnel_nexhop_inner_mac,
                eth_src=ROUTER_MAC,
                ip_dst=vm_ip_from_lag2_nb,
                ip_src=port1_nb_ip,
                ip_id=108,
                ip_ttl=63)

    expect_ipip_pkt = simple_ipv4ip_packet(
                eth_dst=lag2_nb_mac,
                eth_src=ROUTER_MAC,
                ip_id=0,
                ip_src=Router_lpb_ip_pipe,
                ip_dst=lag2_nb_ip,
                ip_ttl=ttl_val,
                inner_frame=inner_pkt['IP'])
Decap packet:
    Expect_pkt = simple_udp_packet(
                eth_dst=port1_nb_mac,
                eth_src=ROUTER_MAC,
                ip_dst=port1_nb_ip
                ip_src=vm_ip_from_port22_nb,
                ip_id=108,
                ip_ttl=50)

    inner_pkt = simple_udp_packet(
                eth_dst=remote_tunnel_nexhop_inner_mac,
                eth_src=remote_ROUTER_MAC,
                ip_dst=port1_nb_ip,
                ip_src=vm_ip_from_lag2_nb,
                ip_id=108,
                ip_ttl=51)

    Input_ipip_pkt = simple_ipv4ip_packet(
                eth_dst=ROUTER_MAC,
                eth_src=lag2_nb_mac,
                ip_dst=Router_lpb_ip_pipe,
                ip_src=lag2_nb_ip 
                ip_id=0,
                ip_ttl=64,
                inner_frame=inner_pkt['IP'])

```

### Test steps: <!-- omit in toc --> 
- encap_ttl_set_pipe_mod
1. Make sure create tunnel_pipe with encap_ttl_val attribute as user defined ttl_val=20, encap_ttl_mode attr with SAI_TUNNEL_TTL_MODE_PIPE_MODEL
2. Generate input packet with ip_ttl field as 64.
3. Send input packet from port1.
4. Create Expected ipinip packet with ip_ttl field in the outer IP header as ttl_val, inner ip_ttl as 63.
5. Recieve ipinip packet from port22, and compare it with the expected ipinip packet.

- decap_ttl_set_pipe
1. Make sure to create a tunnel with decap_ttl_mode attr with SAI_TUNNEL_TTL_MODE_PIPE_MODEL
2. Generate input ipinip packet with ip_ttl field in the outer IP header as 64, and one in the inner IP header as 51.
3. Send packet from port22.
4. Recieve ipinip packet from port1, compare it with the expected packet, expected received packet with ip_ttl field as 50.

## Test Group2: TTL Uniform Mode

### Case5: encap_ttl_set_uniform_mode_v4
### Case6: encap_ttl_set_uniform_mode_v6
### Case7: decap_ttl_set_uniform_mode_v4
### Case8: decap_ttl_set_uniform_mode_v6

### Testing Objective <!-- omit in toc --> 
This verifies the TTL field is preserved end-to-end by copying into the outer header on encapsulation and copying from the outer header on decapsulation,
even if we set tunnel encap_ttl_val attribute.

### Testing Data Packet <!-- omit in toc -->

```Python
Encap packet:
    input_pkt = simple_tcp_packet(
                eth_dst=ROUTER_MAC,
                eth_src=port2_nb_mac,
                ip_dst=vm_ip_from_lag3_nb,
                ip_src=port2_nb_ip,
                ip_id=108,
                ip_ttl=64)

    inner_pkt = simple_tcp_packet(
                eth_dst=tunnel_nexhop_inner_mac,
                eth_src=ROUTER_MAC,
                ip_dst=vm_ip_from_lag3_nb,
                ip_src=port2_nb_ip,
                ip_id=108,
                ip_ttl=63)

    expect_ipip_pkt = simple_ipv4ip_packet(
                eth_dst=lag3_nb_mac,
                eth_src=ROUTER_MAC,
                ip_id=0,
                ip_src=Router_lpb_ip_uniform,
                ip_dst=lag3_nb_ip,
                ip_ttl=63,
                inner_frame=inner_pkt['IP'])
Decap packet:
    Expect_pkt = simple_udp_packet(
                eth_dst=port2_nb_mac,
                eth_src=ROUTER_MAC,
                ip_dst=port2_nb_ip
                ip_src=vm_ip_from_lag3_nb,
                ip_id=108,
                ip_ttl=63)

    inner_pkt = simple_udp_packet(
                eth_dst=remote_tunnel_nexhop_inner_mac,
                eth_src=remote_ROUTER_MAC,
                ip_dst=port2_nb_ip,
                ip_src=vm_ip_from_lag3_nb,
                ip_id=108,
                ip_ttl=50)

    Input_ipip_pkt = simple_ipv4ip_packet(
                eth_dst=ROUTER_MAC,
                eth_src=lag3_nb_mac,
                ip_dst=Router_lpb_ip_uniform,
                ip_src=lag3_nb_ip 
                ip_id=0,
                ip_ttl=64,
                inner_frame=inner_pkt['IP'])

```
### Test steps: <!-- omit in toc -->

- encap_ttl_set_uniform_mode
1. Make sure create tunnel_uniform with encap_ttl_val attribute as user-defined ttl_val=20, 
2. Generate input packet with ip_ttl field as 64.
3. Send input packet from port2.
4. Create expected ipinip packet with ip_ttl field for outer IP header as 63,  inner ip_ttl as 63.
5. Recieve ipinip packet from lag3 port, compare it with expected ipinip packet.

- decap_ttl_set_uniform_mode
1. Make sure to create a tunnel with  decap_ttl_mode attr with SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL
2. Generate input ipinip packet with ip_ttl field in the outer IP header as 64, inner ip_ttl as 50.
3. Send packet from lag3 port.
4. Create the expected received packet with the ip_ttl field as 63.
5. Recieve ipinip packet from port2, and compare it with the expected packet.

## Test Group3: DSCP in Pipe Mode
	
### Case9: encap_dscp_in_pipe_mode_v4
### Case10: encap_dscp_in_pipe_mode_v6
### Case11: decap_dscp_in_pipe_mode_v4
### Case12: decap_dscp_in_pipe_mode_v6

### Testing Objective <!-- omit in toc --> 
This verifies if the DSCP field is user-defined for the outer header on encapsulation and the DSCP field of the inner header remains the same on decapsulation when using DSCP pipe mode.
### Testing Data Packet <!-- omit in toc -->

```Python
Encap packet:
    input_pkt = simple_tcp_packet(
                eth_dst=ROUTER_MAC,
                eth_src=port1_nb_mac,
                ip_dst=vm_ip_from_lag2_nb,
                ip_src=port1_nb_ip,
                ip_id=108,
                ip_dscp=orig_dscp_val,
                ip_ttl=64)

    inner_pkt = simple_tcp_packet(
                eth_dst=tunnel_nexhop_inner_mac,
                eth_src=ROUTER_MAC,
                ip_dst=vm_ip_from_lag2_nb,
                ip_src=port1_nb_ip,
                ip_id=108,
                ip_dscp=orig_dscp_val,
                ip_ttl=63)

    expect_ipip_pkt = simple_ipv4ip_packet(
                eth_dst=plag2_nb_mac,
                eth_src=ROUTER_MAC,
                ip_id=0,
                ip_src=Router_lpb_ip_pipe,
                ip_dst=lag2_nb_ip,
                ip_ttl=64,
                ip_dscp=tunnel_dscp_val,
                inner_frame=inner_pkt['IP'])
Decap packet:
    Expect_pkt = simple_udp_packet(
                eth_dst=port1_nb_mac,
                eth_src=ROUTER_MAC,
                ip_dst=port1_nb_ip
                ip_src=vm_ip_from_lag2_nb,
                ip_id=108,
                ip_dscp=inner_dscp_val)

    inner_pkt = simple_udp_packet(
                eth_dst=remote_tunnel_nexhop_inner_mac,
                eth_src=remote_ROUTER_MAC,
                ip_dst=port1_nb_ip,
                ip_src=vm_ip_from_lag2_nb,
                ip_id=108,
                ip_dscp=inner_dscp_val)

    Input_ipip_pkt = simple_ipv4ip_packet(
                eth_dst=ROUTER_MAC,
                eth_src=lag2_nb_mac,
                ip_dst=Router_lpb_ip_pipe,
                ip_src=lag2_nb_ip 
                ip_id=0,
                ip_dscp=tunnel_dscp_val,
                inner_frame=inner_pkt['IP'])

```

### Test steps: <!-- omit in toc --> 
- encap_dscp_remap_in_pipe_mode:
1. Make sure create tunnel_pipe with encap_dscp_mode attr as SAI_TUNNEL_DSCP_MODE_PIPE_MODEL, encap_dscp_val attribute as user defined ip_dscp=tunnel_dscp_val
2. Generate input packet with DSCP field as orig_dscp_val.
3. Send input packet from port1.
4. Create expected ipinip packet with dscp field in the outer IP header as tunnel_dscp_val, inner dscp as orig_dscp_val.
5. Recieve ipinip packet from lag2 port. Compare it with the expected ipinip packet.


- decap_dscp_remap_in_pipe_mode:
1. Make sure to create tunnel_pipe with decap_dscp_mode attr as SAI_TUNNEL_DSCP_MODE_PIPE_MODEL
2. Generate input ipinip packet with dscp field in the outer IP header as tunnel_dscp_val, inner dscp as inner_dscp_val. 
3. Send input packet from lag2 port.
4. Generate expect packet with dscp field as inner_dscp_val.
5. Recieve decap packet from port1. Compare it with the expected IP packet.

## Test Group4: DSCP QoS Map in Pipe Mode
	
### Case13: encap_dscp_remap_in_pipe_mode_v4
### Case14: encap_dscp_remap_in_pipe_mode_v6
### Case15: decap_dscp_remap_in_pipe_mode_v4
### Case16: decap_dscp_remap_in_pipe_mode_v6

### Testing Objective <!-- omit in toc --> 
This verifies if the DSCP field is user-defined for the outer header on encapsulation and the DSCP field of the inner header remains the same on decapsulation when using DSCP pipe mode.
### Testing Data Packet <!-- omit in toc -->

```Python
Encap packet:
    input_pkt = simple_tcp_packet(
                eth_dst=ROUTER_MAC,
                eth_src=port1_nb_mac,
                ip_dst=vm_ip_from_lag2_nb,
                ip_src=port1_nb_ip,
                ip_id=108,
                ip_dscp=orig_dscp_val,
                ip_ttl=64)

    inner_pkt = simple_tcp_packet(
                eth_dst=tunnel_nexhop_inner_mac,
                eth_src=ROUTER_MAC,
                ip_dst=vm_ip_from_lag2_nb,
                ip_src=port1_nb_ip,
                ip_id=108,
                ip_dscp=rewrite_dscp_val,
                ip_ttl=63)

    expect_ipip_pkt = simple_ipv4ip_packet(
                eth_dst=lag2_nb_mac,
                eth_src=ROUTER_MAC,
                ip_id=0,
                ip_src=Router_lpb_ip_pipe,
                ip_dst=lag2_nb_ip,
                ip_ttl=64,
                ip_dscp=tunnel_dscp_val,
                inner_frame=inner_pkt['IP'])
Decap packet:
    Expect_pkt = simple_udp_packet(
                eth_dst=port1_nb_mac,
                eth_src=ROUTER_MAC,
                ip_dst=port1_nb_ip
                ip_src=vm_ip_from_lag2_nb,
                ip_id=108,
                ip_dscp=rewrite_dscp_val,
                ip_ttl=62)

    inner_pkt = simple_udp_packet(
                eth_dst=remote_tunnel_nexhop_inner_mac,
                eth_src=remote_ROUTER_MAC,
                ip_dst=port1_nb_ip,
                ip_src=vm_ip_from_lag2_nb,
                ip_id=108,
                ip_dscp=orig_dscp_val,
                ip_ttl=63)

    Input_ipip_pkt = simple_ipv4ip_packet(
                eth_dst=ROUTER_MAC,
                eth_src=lag2_nb_mac,
                ip_dst=Router_lpb_ip_pipe,
                ip_src=lag2_nb_ip 
                ip_id=0,
                ip_dscp=tunnel_dscp_val,
                ip_ttl=64,
                inner_frame=inner_pkt['IP'])

```

### Test steps: <!-- omit in toc --> 
- encap_dscp_remap_in_pipe_mode:
1. Make sure create tunnel_pipe with encap_dscp_val attribute as user defined ip_dscp=tunnel_dscp_val
2. Bind port1 with dscp_to_tc_map (orig_dscp_val => tc_map), Bind lag2 port with tc_to_dscp_map(tc_map => rewrite_dscp_val).
3. Generate input packet with dscp field as orig_dscp_val.
4. Send input packet from port1.
5. Create expected ipinip packet with dscp field in outer ip header as tunnel_dscp_val, inner dscp as rewrite_dscp_val. 
6. Recieve ipinip packet from lag2 port. Compare it with expected ipinip packet.
7. Remove  dscp_to_tc_map and tc_to_dscp_map.

- decap_dscp_remap_in_pipe_mode:
1. Make sure create tunnel_pipe with decap_dscp_mode attr as SAI_TUNNEL_DSCP_MODE_PIPE_MODEL, attribute as user defined ip_dscp=tunnel_dscp_val
2. Bind port22 with dscp_to_tc_map (orig_dscp_val => tc_map), Bind lag2 port with tc_to_dscp_map(tc_map => rewrite_dscp_val).
3. Generate input ipinip packet with dscp field in the outer IP header as tunnel_dscp_val, one in the inner IP header as orig_dscp_val. 
4. Send input packet from lag2 port.
5. Generate expect packet with dscp field as rewrite_dscp_val.
6. Recieve decap packet from port1. Compare it with the expected IP packet.
7. Remove  dscp_to_tc_map and tc_to_dscp_map.

## Test Group5: DSCP in Uniform Mode 
	
### Case17: encap_dscp_remap_in_Uniform_mode_v4
### Case18: encap_dscp_remap_in_Uniform_mode_v6
### Case19: decap_dscp_remap_in_Uniform_mode_v4
### Case20: decap_dscp_remap_in_Uniform_mode_v6

### Testing Objective <!-- omit in toc --> 
This verifies the DSCP field is preserved end-to-end by copying into the outer header on encapsulation and copying from the outer header on decapsulation

### Testing Data Packet <!-- omit in toc -->

```Python
Encap packet:
    input_pkt = simple_tcp_packet(
                eth_dst=ROUTER_MAC,
                eth_src=port2_nb_mac,
                ip_dst=vm_ip_from_lag3_nb,
                ip_src=port2_nb_ip,
                ip_id=108,
                ip_dscp=orig_dscp_val)

    inner_pkt = simple_tcp_packet(
                eth_dst=tunnel_nexhop_inner_mac,
                eth_src=ROUTER_MAC,
                ip_dst=vm_ip_from_lag3_nb,
                ip_src=port2_nb_ip,
                ip_id=108,
                ip_dscp=orig_dscp_val)

    expect_ipip_pkt = simple_ipv4ip_packet(
                eth_dst=lag3_nb_mac,
                eth_src=ROUTER_MAC,
                ip_id=0,
                ip_src=Router_lpb_ip_uniform,
                ip_dst=lag3_nb_ip,
                ip_dscp=orig_dscp_val,
                inner_frame=inner_pkt['IP'])
Decap packet:
    Expect_pkt = simple_udp_packet(
                eth_dst=port2_nb_mac,
                eth_src=ROUTER_MAC,
                ip_dst=port2_nb_ip
                ip_src=vm_ip_from_lag3_nb,
                ip_id=108,
                ip_dscp=tunnel_dscp_val)

    inner_pkt = simple_udp_packet(
                eth_dst=remote_tunnel_nexhop_inner_mac,
                eth_src=remote_ROUTER_MAC,
                ip_dst=port2_nb_ip,
                ip_src=vm_ip_from_lag3_nb,
                ip_id=108,
                ip_dscp=orig_dscp_val)

    Input_ipip_pkt = simple_ipv4ip_packet(
                eth_dst=ROUTER_MAC,
                eth_src=lag3_nb_mac,
                ip_dst=Router_lpb_ip_uniform,
                ip_src=lag3_nb_ip 
                ip_id=0,
                ip_dscp=tunnel_dscp_val,
                inner_frame=inner_pkt['IP'])

```

### Test steps: <!-- omit in toc --> 
- encap_dscp_remap_in_uniform_mode:
1. Make sure create tunnel_uniform with encap_dscp_val attribute as user defined ip_dscp=tunnel_dscp_val
2. Generate input packet with dscp field as orig_dscp_val.
3. Send input packet from port2.
4. Create expected ipinip packet with dscp field in outer ip header as rewrite_dscp_val, inner dscp as rewrite_dscp_val.
5. Recieve ipinip packet from lag3 port. Compare it with expected ipinip packet.


- decap_dscp_remap_in_unifrom_mode:
1. Make sure to create tunnel_pipe with decap_dscp_mode attr as SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL
2. Generate input ipinip packet with dscp field in the outer IP header as tunnel_dscp_val, one in the inner IP header as orig_dscp_val. 
3. Send input packet from lag3 port.
4. Generate expect packet with dscp field as tunnel_dscp_val.
5. Recieve decap packet from port2. Compare it with the expected IP packet.


## Test Group6: DSCP QOS Map in Uniform Mode
	
### Case21: encap_dscp_remap_in_Uniform_mode_v4
### Case22: encap_dscp_remap_in_Uniform_mode_v6
### Case23: decap_dscp_remap_in_Uniform_mode_v4
### Case24: decap_dscp_remap_in_Uniform_mode_v6

### Testing Objective <!-- omit in toc --> 
This verifies the DSCP field is preserved end-to-end by copying into the outer header on encapsulation and copying from the outer header on decapsulation, combining with QoS map.

### Testing Data Packet <!-- omit in toc -->

```Python
Encap packet:
    input_pkt = simple_tcp_packet(
                eth_dst=ROUTER_MAC,
                eth_src=port2_nb_mac,
                ip_dst=vm_ip_from_lag3_nb,
                ip_src=port2_nb_ip,
                ip_id=108,
                ip_dscp=orig_dscp_val)

    inner_pkt = simple_tcp_packet(
                eth_dst=tunnel_nexhop_inner_mac,
                eth_src=ROUTER_MAC,
                ip_dst=vm_ip_from_lag3_nb,
                ip_src=port2_nb_ip,
                ip_id=108,
                ip_dscp=rewrite_dscp_val)

    expect_ipip_pkt = simple_ipv4ip_packet(
                eth_dst=lag3_nb_mac,
                eth_src=ROUTER_MAC,
                ip_id=0,
                ip_src=Router_lpb_ip_unifotm,
                ip_dst=lag3_nb_ip,
                ip_dscp=rewrite_dscp_val,
                inner_frame=inner_pkt['IP'])
Decap packet:
    Expect_pkt = simple_udp_packet(
                eth_dst=port2_nb_mac,
                eth_src=ROUTER_MAC,
                ip_dst=port2_nb_ip
                ip_src=vm_ip_from_lag3_nb,
                ip_id=108,
                ip_dscp=rewrite_dscp_val)

    inner_pkt = simple_udp_packet(
                eth_dst=remote_tunnel_nexhop_inner_mac,
                eth_src=remote_ROUTER_MAC,
                ip_dst=port2_nb_ip,
                ip_src=vm_ip_from_lag3_nb,
                ip_id=108,
                ip_dscp=orig_dscp_val)

    Input_ipip_pkt = simple_ipv4ip_packet(
                eth_dst=ROUTER_MAC,
                eth_src=lag3_nb_mac,
                ip_dst=Router_lpb_ip_unifotm,
                ip_src=lag3_nb_ip 
                ip_id=0,
                ip_dscp=tunnel_dscp_val,
                inner_frame=inner_pkt['IP'])

```

### Test steps: <!-- omit in toc --> 
- encap_dscp_remap_in_uniform_mode:
1. Make sure create tunnel_uniform with encap_dscp_mode attr as SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL
2. Bind port1 with dscp_to_tc_map (orig_dscp_val => tc_map), Bind lag3 port with tc_to_dscp_map(tc_map => rewrite_dscp_val).
3. Generate input packet with dscp field as orig_dscp_val
4. Send input packet from port2.
5. Create expected ipinip packet with dscp field in outer ip header as rewrite_dscp_val, inner dscp as rewrite_dscp_val.
6. Recieve ipinip packet from lag3 port. Compare it with expected ipinip packet.
6. Remove  dscp_to_tc_map and tc_to_dscp_map.

- decap_dscp_remap_in_unifrom_mode:
1. Make sure to create tunnel_uniform with decap_dscp_mode attr as SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL
2. Bind lag3 port with dscp_to_tc_map (tunnel_dscp_val => tc_map), Bind port2 with tc_to_dscp_map(tc_map => rewrite_dscp_val).
3. Generate input ipinip packet with dscp field in the outer IP header as tunnel_dscp_val, one in the inner IP header as orig_dscp_val. 
4. Send input packet from lag3 port.
5. Create expect packet with dscp field as rewrite_dscp_val.
6. Recieve decap packet from lag3 port. Compare it with the expected IP packet.
7. Remove  dscp_to_tc_map and tc_to_dscp_map.

## Test Group7: Test tunnel termination
The test group chooses tunnel_uniform tunnel. 

### case25:test_tunnel_term_with_correct_Dst_ip
### case26:test_tunnel_term_with_error_Dst_ip
### Testing Objective <!-- omit in toc --> 
 This verifies if only tunneled packets with destination IP set as
SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_DST_IP are de-encapsulated

### Testing Data Packet  <!-- omit in toc --> 

```Python

    Expect_pkt = simple_udp_packet(
                eth_dst=port2_nb_mac,
                eth_src=ROUTER_MAC,
                ip_dst=port2_nb_ip
                ip_src=vm_ip_from_lag3_nb,
                ip_id=108)

    inner_pkt = simple_udp_packet(
                eth_dst=remote_tunnel_nexhop_inner_mac,
                eth_src=remote_ROUTER_MAC,
                ip_dst=port2_nb_ip,
                ip_src=vm_ip_from_lag3_nb,
                ip_id=108)

    Input_ipip_pkt = simple_ipv4ip_packet(
                eth_dst=ROUTER_MAC,
                eth_src=lag3_nb_mac,
                ip_dst=test_outer_dst_ip_val,
                ip_src=lag3_nb_ip 
                ip_id=0,
                inner_frame=inner_pkt['IP'])

```

### Test steps: <!-- omit in toc --> 
- test_tunnel_term_with_correct_Dst_ip:
 1. set test_outer_dst_ip_val as Router_lpb_ip_uniform, then generate input ipinip packet with ip_dst field for outer header as test_outer_dst_ip_val
 2. Send input packet from lag3 port.
 3. Verify if we can receive decap packet from port2. Compare it with the expected expect packet.
- test_tunnel_term_with_error_Dst_ip:
 1. set test_outer_dst_ip_val as a diffenrent value with Router_lpb_ip_uniform, then generate input ipinip packet with ip_dst field for outer header as test_outer_dst_ip_val
 2. Send input packet from lag3 port.
 3. Verify if packet drop on port2.


## Todo Test Group7: IPinIP P2MP
### Case27: test_p2mp_decap_v4
### Case27: test_p2mp_encap_v4
### Case27: test_p2mp_decap_v6
### Case27: test_p2mp_encap_v6

### Testing Data Packet  <!-- omit in toc -->

## To Do Verify tunnel + ECMP