# Sample T0 Configurations and data  <!-- omit in toc --> 
- [Overriew](#overriew)
- [IP and MAC naming convention](#ip-and-mac-naming-convention)
  - [MAC](#mac)
  - [IP](#ip)
- [1. L2 Configurations](#1-l2-configurations)
  - [1.1 FDB Configuration](#11-fdb-configuration)
  - [1.2 VLAN configuration](#12-vlan-configuration)
- [2. L3 configuration](#2-l3-configuration)
  - [2.1 VLAN Interfaces](#21-vlan-interfaces)
  - [2.2 LAG configuration](#22-lag-configuration)
    - [2.2.1 LAG Hash Rule](#221-lag-hash-rule)
  - [2.3 Route Configuration](#23-route-configuration)
    - [2.3.1 VLAN interfaces route entries](#231-vlan-interfaces-route-entries)
    - [2.3.2 LAG Route entry](#232-lag-route-entry)
    - [2.3.3  Tunnel Route entry](#233--tunnel-route-entry)
  - [2.4 Neighbor Configuration](#24-neighbor-configuration)
    - [2.4.1 VLAN Neighbors](#241-vlan-neighbors)
    - [2.4.2 LAG Neighbors](#242-lag-neighbors)
    - [2.4.3 Tunnel Neighbors](#243-tunnel-neighbors)
  - [2.5 Next Hops](#25-next-hops)
    - [2.5.1 Tunnel Next hop](#251-tunnel-next-hop)
  - [2.6 Tunnel Configuration](#26-tunnel-configuration)
    - [2.6.1 Tunnel loopback:](#261-tunnel-loopback)
    - [2.6.2 Tunnel](#262-tunnel)
    - [2.6.3 Tunnel Term](#263-tunnel-term)
# Overriew
This document describes the sample configuration data.

**Note: This configuration focused on T0 topology.**

# IP and MAC naming convention
In this configuration, we mapped the IP and MAC address into different parts of this configuration as below.

## MAC
For MAC addresses, we can use different sections in the MAC addresses to map different title numbers.
The pattern is
```
L1_NUM:L2_NUM:L3_NUM:ROLE:EXTRA:SEQ
ROLE: T1=1, Server=99
```

For example:
For the MAC address in ``1.1 FDB Configuration``.
```
#Server MAC
01:01:00:99:02:01~01:01:00:99:02:32
# 99: Server
# 02: EXTRA (Group ID)
```


## IP
For IP addresses, we will use different prefix for different role

Format: ROLE.NUM.GROUP_ID.SEQ

- ROLE_NUM
T0: 10.0.0.0
T1: 10.0.0.0
Server: 192.168.0.0

For example
```
# IP in 
# 2.4.1 VLAN Neighbors
#Group0 (For Vlan10)
192.168.1.1~ 192.168.1.8
#Group1 (ForVlan20)
192.168.2.1~ 192.168.2.8
```




# 1. L2 Configurations

## 1.1 FDB Configuration

The MAC Table for VLAN L2 forwarding as below
|Name|MAC|PORT|VLAN|HostIf|
|-|-|-|-|-|
|mac0|01:01:00:99:00:00|Port0||Ethernet0|
|mac1-8  |01:01:00:99:01:01 - 01:01:00:99:01:08|Port1-8|10|Ethernet4-Ethernet32|
|mac9-16 |01:01:00:99:02:09 - 01:01:00:99:02:16|Port9-16|20|Ethernet36-Ethernet64|

## 1.2 VLAN configuration

|HostIf|VLAN ID|Ports|Tag mode|
|-|-|-|-|
|Ethernet4-32|10|Port1-8|Untag|
|Ethernet36-72|20|Port9-16|Untag|


# 2. L3 configuration

Host interface IP
|Port|Interface IP| 
|-|-|
|port0|10.0.0.100|

## 2.1 VLAN Interfaces
|VLAN ID | VLAN Interface IP| 
|-|-|
|10|192.168.1.100|
|20|192.168.2.100|

## 2.2 LAG configuration

|HostIf|LAG ID|Ports|
|-|-|-|
|Ethernet76-80|lag1|Port17-18|
|Ethernet84-88|lag2|Port19-20|
|Ethernet84-88|lag3|Port21-22|
### 2.2.1 LAG Hash Rule
- Set hash algorithm as SAI_HASH_ALGORITHM_CRC
- Set switch hash attribute as below, which means switch computes hash using the five fields and seed(SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED) as the hash configuration. 
```
SAI_NATIVE_HASH_FIELD_SRC_IP
SAI_NATIVE_HASH_FIELD_DST_IP
SAI_NATIVE_HASH_FIELD_IP_PROTOCOL
SAI_NATIVE_HASH_FIELD_L4_DST_PORT
SAI_NATIVE_HASH_FIELD_L4_SRC_PORT
```

## 2.3 Route Configuration

### 2.3.1 VLAN interfaces route entries
|VLAN ID | route IP | Type |
|-|-| - |
|10| 192.168.1.100/24 | Direct Connect|
|20| 192.168.2.100/24 | Direct Connect|
### 2.3.2 LAG Route entry

|LAG ID | route IP | Type | VALUE|
|-|-| - |-|
|1| 10.0.1.100/31 | Direct Connect||
|2| 10.0.2.100/31 | Direct Connect||
|1| 192.168.10.1-192.168.10.100| NH|lag1_nb|

### 2.3.3  Tunnel Route entry
|Next Hop Name | Dst route IP |Next Hop Type |
|-|-| - |-|
|tunnel_pipe_nh|vm_ip_from_lag2_nb: 192.192.1.1| SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP|
|tunnel_uniform_nh|vm_ip_from_lag3_nb: 192.192.1.2| SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP|

## 2.4 Neighbor Configuration
### 2.4.1 VLAN Neighbors
|Name|Port|IP|dest_mac|
|-|-|-|-|
|vlan10_nb1-nb8|Port1-8 |192.168.1.1 ~ 192.168.1.8  |01:01:00:99:01:01 - 01:01:00:99:01:08|
|vlan20_nb1-nb8|Port9-16|192.168.2.9 ~ 192.168.2.16 |01:01:00:99:02:09 - 01:01:00:99:02:16 |


### 2.4.2 LAG Neighbors

|Name|Port|IP|dest_mac|
|-|-|-|-|
|lag1_nb|lag1| 10.0.1.101 | 02:04:02:01:01:01|


### 2.4.3 Tunnel Neighbors

|Name|Port|IP|dest_mac|
|-|-|-|-|
|lag2_nb|lag2| 10.0.2.101 | 03:04:03:01:03:01|
|lag3_nb|lag3| 10.0.3.101 | 04:04:04:01:04:01|
|lag2_remote_nb|lag2| 192.168.20.1-192.168.20.99| 03:04:03:99:30:01-03:04:03:99:30:99|
|lag3_remote_nb|lag3| 192.168.30.1-192.168.30.99 | 04:04:04:99:40:01-03:04:03:99:40:99|


## 2.5 Next Hops
### 2.5.1 Tunnel Next hop

|name|Mode|type|IP|MAC_NAME|MAC|
|-|-|-|-|-|-|
|tunnel_uniform_nh|Uniform|SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP|lag3_nb:10.0.3.101|inner_mac_uniform|04:04:04:01:04:01|
|tunnel_pipe_nh|pipe|SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP|lag2_nb:10.0.2.101|inner_mac_pip| 03:04:03:01:03:01|

## 2.6 Tunnel Configuration
### 2.6.1 Tunnel loopback:
 
|Name|IP|
|-|-|
|Router_lpb_ip_pipe_v4| 10.10.10.1|
|Router_lpb_ip_uniform_v4| 10.10.10.2|
|Router_lpb_ip_pipe_v6| 2001:0db8::10:1|
|Router_lpb_ip_uniform_v6| 2001:0db8::10:2|


### 2.6.2 Tunnel

|Name|Mode|underlay_interface|overlay_interface|
|-|-|-|-|
|pipe_tunnel|pipe|Router_lpb_ip_pipe_v4/v6||
|uniform_tunnel|uniform|Router_lpb_ip_uniform_v4/v6||

- Tunnel_pipe_attr:

Create tunnel_pipe with these attributes below,

|Attribute Name|Value|
|-|-|
|encap_ttl_mode|SAI_TUNNEL_TTL_MODE_PIPE_MODEL| 
|encap_ttl_val|ttl_val| 
|decap_ttl_mode|SAI_TUNNEL_TTL_MODE_PIPE_MODEL| 
|encap_dscp_mode|SAI_TUNNEL_DSCP_MODE_PIPE_MODEL| 
|encap_dscp_vale|tunnnel_dscp_val| 
|decap_dscp_mode|SAI_TUNNEL_DSCP_MODE_PIPE_MODEL| 

- Tunnel_uniform_attr:

Create tunnel_Uniform with these attributes below,

|Attribute Name|Value|
|-|-|
|encap_ttl_mode|SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL| 
|decap_ttl_mode|SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL| 
|encap_dscp_mode|SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL| 
|decap_dscp_mode|SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL|


### 2.6.3 Tunnel Term

|name|tunnel|dst_ip|src_ip|type|
|-|-|-|-|-|
|Router_lpb_ip_pipe_v4|pipe_tunnel|10.10.10.1|10.0.2.101| SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2P|
|Router_lpb_ip_uniform_v4|uniform_tunnel|10.10.10.2|10.0.3.101| SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2P|
