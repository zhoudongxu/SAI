
# Test Group1: Buffer 

## Case1: test_ingress_pg_stat
## Case2: test_ingress_static_shared_th_pkt_drop
## Case3: test_ingress_dynamic_shared_th_pkt
## Case4: test_watermarker_pkt_larger_than_reserved
## Case5: test_watermarker_pkt_less_than_reserved

### Testing Objective 
test_ingress_pg_stat - Verify buffer pool and ingress priority group releated statictics.
test_ingress_static_th_drop - Verify if drop the packet when packet length exceed the static shared threshold

### Case Steps:
test_ingress_pg_stat

1. Config Buffer profile for port0, buffer_reserved_size, buffer_size=buffer_reserved_size, shared_static_th=self.reserved_buf_size,  threshold_mode=SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC, pri_to_pg(prio 0 to pg, with ipg_idx 7), config map PFC_PTIO_TO_PG, set_port_attr
2. send 10000 packet and check the count, SAI_BUFFER_POOL_STAT_CURR_OCCUPANCY_BYTES, SAI_INGRESS_PRIORITY_GROUP_STAT_CURR_OCCUPANCY_BYTES, SAI_INGRESS_PRIORITY_GROUP_STAT_SHARED_CURR_OCCUPANCY_BYTES, they should be increased (get the largest count)

