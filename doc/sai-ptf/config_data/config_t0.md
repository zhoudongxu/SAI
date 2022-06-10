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
  - [2.4 Neighbor Configuration](#24-neighbor-configuration)
    - [2.4.1 VLAN Neighbors](#241-vlan-neighbors)
    - [2.4.2 LAG Neighbors](#242-lag-neighbors)
# Overriew
This document describes the sample configuration data.

**Note: This configuration focused on T0 topology.**

# IP and MAC naming convention
In this configuration, we mapped the IP and MAC address into different part of this configuration as below.

## MAC
For MAC addres, we can use differnt section in MAC address to map different title number.
The pattern is
```
L1_NUM:L2_NUM:L3_NUM:ROLE:EXTRA:SEQ
ROLE: T1=1, Server=99
```

For example:
For the MAC address in FDB configuration.

```
#VLAN 10, Server MAC
01:01:00:99:10:01~01:01:00:99:10:32
# FDB Configuration is 1.1, then first two sections is 01:01
# 99: Server
# 10: VLAN

#T0 Ports MAC
01:01:00:00:00:01~01:01:00:00:00:32
```

For the VLAN Neighbor(Server) MAC
```
02:04:01:00:99:01~02:04:01:00:99:32
```

## IP
For Mac address, we will use different IP subnet for different device role(only for T0, T1 and server), and map different number in L3 sub-title within second and third IP sections.

Format: ROLE_NUM+L3_SUB_NUM.L3_SUB2_NUM.EXTRA.SEQ

- Subnet
T0: 10.0.0.0/24
T1: 20.0.0.0/24
Server: 30.0.0.0/24

For example
```
#2.1 VLAN Interface
#T0 Host interfaces
11.0.0.1~11.0.0.32

#2.3.1 VLAN interfaces route entries
#VLAN 10
33.1.10.1~33.1.10.32
#VLAN 20
33.1.20.1~33.1.20.32
## 33.1 = 30(Server) + 3(Title No.), 1(Title No.)
## 10= VLAN 10, 20=VLAN 20
```




# 1. L2 Configurations

## 1.1 FDB Configuration

The MAC Table for VLAN L2 forwarding as below
|Name|MAC|PORT|VLAN|HostIf|
|-|-|-|-|-|
|mac0|01:01:00:99:00:01|Port0||Ethernet0|
|mac1-8  |01:01:00:99:10:01 - 01:01:00:99:10:08|Port1-8|10|Ethernet4-Ethernet32|
|mac9-16 |01:01:00:99:20:09 - 01:01:00:99:20:16|Port9-16|20|Ethernet36-Ethernet64|
|mac17-mac31 |01:01:00:99:00:17 - 01:01:00:99:00:31|Port17-31||Ethernet68-Ethernet124|

## 1.2 VLAN configuration

|HostIf|VLAN ID|Ports|Tag mode|
|-|-|-|-|
|Ethernet0||Port0||
|Ethernet4-32|10|Port1-8|Untag|
|Ethernet36-72|20|Port9-16|Untag|


# 2. L3 configuration

Host interface IP
|Port|VLAN Interface IP| 
|-|-|
|port0|10.0.0.100|
|port1-31|10.0.0.1-10.0.0.31|

## 2.1 VLAN Interfaces
|VLAN ID | VLAN Interface IP| 
|-|-|
|10|11.0.10.1|
|20|11.0.20.1|

## 2.2 LAG configuration

|HostIf|LAG ID|Ports|
|-|-|-|
|Ethernet76-80|lag1|Port17-18|
|Ethernet84-88|lag2|Port19-20|

### 2.2.1 LAG Hash Rule
- Set hash alogrithm as SAI_HASH_ALGORITHM_CRC
- Set switch hash attribute as below, which mean switch computes hash value  using the five fields of packet. 
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
|10| 34.1.10.100/24 | Direct Connect|
|20| 34.1.20.100/24 | Direct Connect|
### 2.3.2 LAG Route entry

|LAG ID | route IP | Type |
|-|-| - |
|1| 24.2.1.100/24 | Direct Connect|
|2| 24.2.2.100/24 | Direct Connect|

## 2.4 Neighbor Configuration
### 2.4.1 VLAN Neighbors
|Name|Port|IP|dest_mac|
|-|-|-|-|
|vlan10_nb1-nb8|Port1-8| 34.1.10.1 ~ 34.1.10.8 | 02:04:01:99:10:01 - 02:04:01:99:10:08|
|vlan20_nb1-nb8|Port9-16|34.1.20.9 ~ 34.1.20.16 |02:04:01:99:20:09 - 02:04:01:99:20:16 |


### 2.4.2 LAG Neighbors

|Name|Port|IP|dest_mac|
|-|-|-|-|
|lag1_nb1-nb8|lag1| 24.2.1.1 ~ 24.2.1.99 | 02:04:02:01:01:01 - 02:04:02:01:01:99|
|lag2_nb1|lag2|24.2.2.1 ~ 24.2.2.99 | 02:04:02:01:02:01 - 02:04:02:01:02:99|






