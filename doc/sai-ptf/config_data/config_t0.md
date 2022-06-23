# Sample T0 Configurations and data  <!-- omit in toc --> 
- [Overriew](#overriew)
- [IP and MAC naming convention](#ip-and-mac-naming-convention)
  - [MAC](#mac)
  - [IP v4](#ip-v4)
  - [IP v4](#ip-v4-1)
- [1. L2 Configurations](#1-l2-configurations)
  - [1.1 FDB Configuration](#11-fdb-configuration)
  - [1.2 VLAN configuration](#12-vlan-configuration)
- [2. L3 configuration](#2-l3-configuration)
  - [2.1 VLAN Interfaces](#21-vlan-interfaces)
  - [2.2 Route Interfaces](#22-route-interfaces)
  - [2.3 Route Configuration](#23-route-configuration)
  - [2.4 Neighbor Configuration](#24-neighbor-configuration)
    - [``tobe remove``  2.3.1 VLAN interfaces route entries](#tobe-remove--231-vlan-interfaces-route-entries)
    - [``tobe remove`` 2.3.2 LAG Route entry](#tobe-remove-232-lag-route-entry)
    - [``tobe remove`` 2.3.3  Tunnel Route entry](#tobe-remove-233--tunnel-route-entry)
  - [``tobe remove`` 2.4 Neighbor Configuration](#tobe-remove-24-neighbor-configuration)
    - [``tobe remove`` 2.4.1 VLAN Neighbors](#tobe-remove-241-vlan-neighbors)
    - [``tobe remove`` 2.4.2 LAG Neighbors](#tobe-remove-242-lag-neighbors)
    - [``tobe remove`` 2.4.3 Tunnel Neighbors](#tobe-remove-243-tunnel-neighbors)
  - [``tobe remove`` 2.5 Next Hops](#tobe-remove-25-next-hops)
    - [``tobe remove`` 2.5.1 Tunnel Next hop](#tobe-remove-251-tunnel-next-hop)
  - [2.6 Tunnel Configuration](#26-tunnel-configuration)
    - [2.6.1 Tunnel loopback:](#261-tunnel-loopback)
    - [2.6.2 Tunnel](#262-tunnel)
    - [2.6.3 Tunnel Term](#263-tunnel-term)
- [3 LAG configuration](#3-lag-configuration)
  - [3.1 LAG Hash Rule](#31-lag-hash-rule)
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
00:01:01:99:02:01~00:01:01:99:02:32
# 99: Server
# 02: EXTRA (Group ID)
```


## IP v4
For IP addresses, we will use different prefix for different role

Format: ROLE.NUM.GROUP_ID.SEQ

- ROLE_NUM
T0: 10.0.0.0
T0 ECMP: 10.0.50.0
T1: 10.1.0.0
T1 ECMP: 10.1.50.0
Server: 192.168.0.0
Server ECMP: 192.168.50.0
Server Remote:192.168.10.0

For example
```
# IP in 
# 2.4.1 VLAN Neighbors
#Group0 (For Vlan10)
192.168.1.1~ 192.168.1.8
#Group1 (ForVlan20)
192.168.2.1~ 192.168.2.8
```

## IP v4
For IP addresses, we will use different prefix for different role

Format: ROLE.NUM.GROUP_ID.SEQ

- ROLE_NUM
T0: fc00:0::
T0 ECMP: fc00:0:50::
T1: fc00:1::
T1 ECMP: fc00:1:50::
Server: fc02::
Server ECMP: fc02:50::
Server Remote:fc02:10::




# 1. L2 Configurations

## 1.1 FDB Configuration

The MAC Table for VLAN L2 forwarding as below
|Name|MAC|PORT|VLAN|HostIf|
|-|-|-|-|-|
|mac0|00:01:01:99:00:00|Port0||Ethernet0|
|mac1-8  |00:01:01:99:01:01 - 00:01:01:99:01:08|Port1-8|10|Ethernet4-Ethernet32|
|mac9-16 |00:01:01:99:02:09 - 00:01:01:99:02:16|Port9-16|20|Ethernet36-Ethernet64|

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
|VLAN ID | VLAN Interface IP v4| VLAN Interface IP v4
|-|-|-|
|10|192.168.1.100|fc02::1:100|
|20|192.168.2.100|fc02::2:100|

## 2.2 Route Interfaces
|Port|Type|
|-|-|
|port0|port|
|port5-8|port|
|port13-16|port|
|Lag1-4|Lag|
|VLAN10|VLAN|
|VLAN20|VLAN|



## 2.3 Route Configuration

|Dest IPv4|Dest IPv6| Next Hop/Group | Next hop IPv4 | Next hop IPv6 | next hop port|
|-|-|-|-|-|-|
|192.168.1.0/24|fc02::1:0/112|Next Hop|192.168.1.100|fc02::1:100|VLAN10|
|192.168.2.0/24|fc02::1:0/112|Next Hop|192.168.2.100|fc02::1:100|VLAN20|
|192.168.11.0/24|fc02::11:0/112|Next Hop|10.1.1.101|fc02::1:101|LAG1|
|192.168.12.0/24|fc02::12:0/112|Next Hop|10.1.2.101|fc02::2:101|LAG2|
|192.168.13.0/24|fc02::13:0/112|Next Hop|10.1.3.101|fc02::3:101|LAG3|
|192.168.14.0/24|fc02::14:0/112|Next Hop|10.1.4.101|fc02::4:101|LAG4|
|192.168.60.0/24|fc02::60:0/112|Next Hop Group|10.1.60.101; 10.1.61.101; 10.1.62.101; 10.1.63.101|fc00:1::60:101; fc00:1::61:101; fc00:1::62:101; fc00:1:63:101|LAG1-4|
|192.168.20.0/24|fc02::20:0/112|Next Hop|192.168.20.100|fc02::20:0/112|Tunnel|
|192.168.30.0/24|fc02::30:0/112|Next Hop|192.168.30.100|fc02::30:0/112|Tunnel|
|192.168.70.0/24|fc02::70:0/112|Next Hop|192.168.70.100|fc02::30:0/112|Tunnel|
|10.0.2.101|fc00::2:100|Next Hop|10.0.2.101|fc02::2:101|Tunnel|
|10.0.3.101|fc00::3:100|Next Hop|10.0.3.101|fc02::3:101|Tunnel|
|10.0.70.100|fc00::70:100|Next Hop Group|10.0.71.101; 10.0.72.101; 10.0.73.101; 10.0.74.101|fc00::71:100; fc00::72:100; fc00::73:100; fc00::74:100|Tunnel|

## 2.4 Neighbor Configuration

|IPv4|IPv6|Port|No_host_route|dest_mac|
|-|-|-|-|-|
|192.168.1.100|fc02::1:100|SVI:VLAN10|No|00:01:01:99:01:a0|
|192.168.2.100|fc02::1:100|SVI:VLAN20|No|00:01:01:99:02:a0|
|10.1.1.100|fc00:1::1:100|LAG:lag1|No|00:01:01:01:01:a0|
|10.1.2.100|fc00:1::2:100|LAG:lag2|No|00:01:01:01:02:a0|
|10.1.3.100|fc00:1::3:100|LAG:lag3|No|00:01:01:01:03:a0|
|10.1.4.100|fc00:1::4:100|LAG:lag4|No|00:01:01:01:04:a0|
|10.0.10.1|fc00::10:1|Tunnel|No|00:01:01:00:10:1|
|10.0.10.2|fc02::10:2|Tunnel|No|00:01:01:00:10:2|
|10.0.2.101|fc02::2:101|Tunnel|Yes|00:01:01:00:2:a1|
|10.0.3.101|fc02::3:101|Tunnel|Yes|00:01:01:00:3:a1|
|10.0.70.101|fc02::70:101|Tunnel|Yes|00:01:01:00:70:a1|
|10.0.71.101|fc02::71:101|Tunnel|Yes|00:01:01:00:71:a1|
|10.0.72.101|fc02::72:101|Tunnel|Yes|00:01:01:00:72:a1|
|10.0.73.101|fc02::73:101|Tunnel|Yes|00:01:01:00:73:a1|
|10.0.74.101|fc02::74:101|Tunnel|Yes|00:01:01:00:74:a1|
|192.168.1.1 ~ 192.168.1.8 |fc02::1:1 - fc02::1:8|Port1-8 | Yes|00:01:01:99:01:01 - 00:01:01:99:01:08|
|192.168.2.9 ~ 192.168.2.16| fc02::2:9 - fc02::2:16|Port9-16| Yes|00:01:01:99:02:09 - 00:01:01:99:02:16|
|192.168.11.1 ~ 192.168.11.10 |fc02::11:1 - fc02::11:10|Tunnel| Yes|00:01:01:99:11:01 - 00:01:01:99:11:10|
|192.168.12.1 ~ 192.168.12.10 |fc02::12:1 - fc02::12:99|Tunnel| Yes|00:01:01:99:12:01 - 00:01:01:99:12:10|
|192.168.13.1 ~ 192.168.13.10 |fc02::13:1 - fc02::13:10|Tunnel| Yes|00:01:01:99:13:01 - 00:01:01:99:13:10|
|192.168.14.1 ~ 192.168.14.10 |fc02::14:1 - fc02::14:10|Tunnel| Yes|00:01:01:99:14:01 - 00:01:01:99:14:10|
|192.168.15.1 ~ 192.168.15.10 |fc02::15:1 - fc02::15:10|Tunnel| Yes|00:01:01:99:15:01 - 00:01:01:99:15:10|
|192.168.60.1 ~ 192.168.60.10 |fc02::60:1 - fc02::60:10|Tunnel| Yes|00:01:01:99:60:01 - 00:01:01:99:60:10|
|192.168.20.1 ~ 192.168.20.10 |fc02::20:1 - fc02::20:10|Tunnel| Yes|00:01:01:99:20:01 - 00:01:01:99:20:10|
|192.168.30.1 ~ 192.168.30.10 |fc02::30:1 - fc02::30:10|Tunnel| Yes|00:01:01:99:30:01 - 00:01:01:99:30:10|
|192.168.70.1 ~ 192.168.70.10 |fc02::70:1 - fc02::70:10|Tunnel| Yes|00:01:01:99:70:01 - 00:01:01:99:70:10|


### ``tobe remove``  2.3.1 VLAN interfaces route entries
|VLAN ID | route IP | Type |
|-|-| - |
|10| 192.168.1.100/24 | Direct Connect|
|20| 192.168.2.100/24 | Direct Connect|
### ``tobe remove`` 2.3.2 LAG Route entry

|LAG ID | route IP | Type | VALUE|
|-|-| - |-|
|1| 10.1.1.100/31 | Direct Connect||
|2| 10.1.2.100/31 | Direct Connect||
|3| 10.1.3.100/31 | Direct Connect||
|1| 192.168.10.1-192.168.10.100| NH|lag1_nb|

### ``tobe remove`` 2.3.3  Tunnel Route entry
|Next Hop Name | Dst route IP |Port|Next Hop Type |
|-|-| - |-|
|tunnel_pipe_nh|remote_pipe_vm|Lag2|SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP|
|tunnel_uniform_nh|remote_uniform_vm|Lag3| SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP|

## ``tobe remove`` 2.4 Neighbor Configuration
### ``tobe remove`` 2.4.1 VLAN Neighbors
|Name|Port|IP|dest_mac|
|-|-|-|-|
|vlan10_nb1-nb8|Port1-8 |192.168.1.1 ~ 192.168.1.8  |00:01:01:99:01:01 - 00:01:01:99:01:08|
|vlan20_nb1-nb8|Port9-16|192.168.2.9 ~ 192.168.2.16 |00:01:01:99:02:09 - 00:01:01:99:02:16|


### ``tobe remove`` 2.4.2 LAG Neighbors

|Name|Port|IP|dest_mac|
|-|-|-|-|
|lag1_nb|lag1| 10.0.1.101 | 02:04:02:01:01:01|


### ``tobe remove`` 2.4.3 Tunnel Neighbors

|Name|Port|IP|dest_mac|
|-|-|-|-|
|lag2_nb|lag2| 10.1.2.101 | 03:04:03:01:03:01|
|lag3_nb|lag3| 10.1.3.101 | 04:04:04:01:04:01|
|remote_pipe_vm|lag2| 192.168.20.1-192.168.20.99| |
|remote_uniform_vm|lag3| 192.168.30.1-192.168.30.99| |


## ``tobe remove`` 2.5 Next Hops
### ``tobe remove`` 2.5.1 Tunnel Next hop

|name|Mode|type|IP|MAC_NAME|MAC|
|-|-|-|-|-|-|
|tunnel_uniform_nh|Uniform|SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP|lag3_nb:10.0.3.101|inner_mac_uniform|04:04:04:01:04:01|
|tunnel_pipe_nh|pipe|SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP|lag2_nb:10.0.2.101|inner_mac_pip| 03:04:03:01:03:01|

## 2.6 Tunnel Configuration
### 2.6.1 Tunnel loopback:
 
|Name|IP|
|-|-|
|Router_lpb_ip_pipe_v4| 10.0.10.1|
|Router_lpb_ip_uniform_v4| 10.0.10.2|
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
|Router_lpb_ip_pipe_v4|pipe_tunnel|10.0.10.1|10.0.2.101| SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2P|
|Router_lpb_ip_uniform_v4|uniform_tunnel|10.0.10.2|10.0.3.101| SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2P|


# 3 LAG configuration

|HostIf|LAG ID|Ports|
|-|-|-|
|Ethernet76-80|lag1|Port17-18|
|Ethernet84-88|lag2|Port19-20|
|Ethernet84-88|lag3|Port21-22|
|Ethernet92|lag4|Port23|
## 3.1 LAG Hash Rule
- Set hash algorithm as SAI_HASH_ALGORITHM_CRC
- Set switch hash attribute as below, which means switch computes hash using the five fields and seed(SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED) as the hash configuration. 
```
SAI_NATIVE_HASH_FIELD_SRC_IP
SAI_NATIVE_HASH_FIELD_DST_IP
SAI_NATIVE_HASH_FIELD_IP_PROTOCOL
SAI_NATIVE_HASH_FIELD_L4_DST_PORT
SAI_NATIVE_HASH_FIELD_L4_SRC_PORT
```