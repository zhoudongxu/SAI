
# Test Group1: Buffer 

## Case1: test_ingress_pg_qos_map
## Case2: test_ingress_pg_config
## Case3: test_ingress_pg_stat_uc
## Case4: test_ingress_headroom_stats_uc
## Case5: test_ingress_overflowed_pkt_recover_uc
## Case6: test_ingress_flow_control_drop_uc
## Case7: test_ingress_pg_qos_map_mc
## Case8: test_ingress_pg_config_mc
## Case9: test_ingress_pg_stat_mc
## Case10: test_ingress_headroom_stats_mc
## Case11: test_ingress_overflowed_pkt_recove_mc
## Case12: test_ingress_flow_control_drop_mc
## Case13: test_create_buffer_pool_numner
## Case14: test_change_ingress_buffer_profile

### Testing Objective 
- test_ingress_pg_qos_map - Verify packet send to the corresponding PG base on the priority group configuration (dscp to tc, tc t0 PG)
- test_ingress_pg_config - Verify if pg can be configured and the data can be retrieve
- test_ingress_pg_stat - Verify buffer pool and ingress priority group releated statictics.
test_ingress_headroom_full_drop - Verify if headroom is filled up (exceed service pool size) then packet is dropped (size and behavior)
- test_ingress_headroom_stats - Verify if headroom is being filled up the related register statictics are changed (Keep sending packet)
- test_ingress_overflowed_pkt_recover - Verify if packets been kept in deferred vector (in mmu) after recovery from congestion, the packets will be sent out as FIFO
- test_ingress_flow_control_drop - Verify if lossless port drop packet when ingress
- test_create_buffer_pool_numner - verify if numbers of ingress and egress buffer pools can be created, Ingress = SAI_SWITCH_ATTR_INGRESS_BUFFER_POOL_NUM, Egress = SAI_SWITCH_ATTR_EGRESS_BUFFER_POOL_NUM.
- test_change_ingress_buffer_profile - verify if change the buffer profile will not break the ingress traffic


For multicast traffic, a single cell can occupy multiple CQEs(cell queue entries, CQEs are control pointers and are used to store the control information for each cell of packet.)

### Case Steps:
test_ingress_pg_stat

1. Config Buffer profile for port0, buffer_reserved_size, buffer_size=buffer_reserved_size*1000, shared_static_th=self.reserved_buf_size=1400,  threshold_mode=SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC, pri_to_pg(prio 0 to pg, with ipg_idx 7), config map PFC_PTIO_TO_PG, set_port_attr
2. send 10000 packet in a thread 
3. check the priority group statictics while sending the packet(Get the max number of the statictics during checking), the statictics include: 
   buffer_pool stats:  SAI_BUFFER_POOL_STAT_CURR_OCCUPANCY_BYTES, SAI_BUFFER_POOL_STAT_WATERMARK_BYTES;
   priority_group_stats: SAI_INGRESS_PRIORITY_GROUP_STAT_CURR_OCCUPANCY_BYTES, SAI_INGRESS_PRIORITY_GROUP_STAT_SHARED_CURR_OCCUPANCY_BYTES,
   SAI_INGRESS_PRIORITY_GROUP_STAT_WATERMARK_BYTES,
   SAI_INGRESS_PRIORITY_GROUP_STAT_PACKETS,
   SAI_INGRESS_PRIORITY_GROUP_STAT_BYTES,
   SAI_INGRESS_PRIORITY_GROUP_STAT_DROPPED_PACKETS
4. Verify the statictics numbers are increased.
**p.s. SAI_QOS_MAP_TYPE_PFC_PRIORITY_TO_PRIORITY_GROUP is not supported by brcm**

test_ingress_static_shared_th_pkt_drop

1. configuration as test_ingress_pg_stat
2. send 10000 packet in a thread
3. check if the SAI_BUFFER_POOL_STAT_WATERMARK_BYTES is the shared_static_th size
4. check SAI_INGRESS_PRIORITY_GROUP_STAT_DROPPED_PACKETS, all the packet dropped

test_ingress_dynamic_shared_th_pkt

1. configuration as test_ingress_pg_stat
2. shared_dynamic_th=10 (2^10),  threshold_mode=SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
3. send 10000 packet in a thread
4. check if the SAI_BUFFER_POOL_STAT_WATERMARK_BYTES is the packet_length size
4. check SAI_INGRESS_PRIORITY_GROUP_STAT_DROPPED_PACKETS, all packet passed

test_watermarker

1. config

# Test Group2: Queue 

## Case1: test_egress_queue_qos_map
## Case2: test_egress_queue_config
## Case3: test_egress_queue_stat_uc
## Case4: test_egress_headroom_stats_uc
## Case5: test_egress_overflowed_pkt_recover_uc
## Case6: test_egress_flow_control_drop_uc
## Case7: test_egress_queue_qos_map_mc
## Case8: test_egress_queue_config_mc
## Case9: test_egress_queue_stat_mc
## Case10: test_egress_headroom_stats_mc
## Case11: test_egress_overflowed_pkt_recove_mc
## Case12: test_egress_flow_control_drop_mc

## Case13: test_change_egress_buffer_profile
## Case14: test_cpu_queue_qos_map
## Case15: test_cpu_queue_config


# Test Group3: QosMap
## Case1: test_dscp_tc_config_check_v4
## Case2: test_diff_dscp_tc_map_diff_port_v4
## Case3: test_one_dscp_tc_map_each_port_v4
## Case4: test_multi_dscp_to_one_tc_v4
## Case5: test_tc_dscp_config_check_v4
## Case6: test_diff_tc_pg_map_diff_port_v4
## Case7: test_one_tc_pg_map_each_port_v4
## Case8: test_multi_tc_to_one_pg_v4
## Case9: test_tc_queue_config_check_v4
## Case10: test_diff_tc_queue_map_diff_port_v4
## Case11: test_one_tc_queue_map_each_port_v4
## Case12: test_multi_tc_to_one_queue_v4
## Case13: test_dscp_tc_config_check_v6
## Case14: test_diff_dscp_tc_map_diff_port_v6
## Case15: test_one_dscp_tc_map_each_port_v6
## Case16: test_multi_dscp_to_one_tc_v6
## Case17: test_tc_dscp_config_check_v6
## Case18: test_diff_tc_pg_map_diff_port_v6
## Case19: test_one_tc_pg_map_each_port_v6
## Case20: test_multi_tc_to_one_pg_v6
## Case21: test_tc_queue_config_check_v6
## Case22: test_diff_tc_queue_map_diff_port_v6
## Case23: test_one_tc_queue_map_each_port_v6
## Case24: test_multi_tc_to_one_queue_v6

