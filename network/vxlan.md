# VXLAN

## 简介

VXALN 全称为 Virtual eXtensible Local Area Network，即虚拟扩展局域网，由 **RFC 7348** 描述。表面上来看，该技术是 VLAN 的扩展，用来解决 802.1q 协议中 VLAN ID 不能超过 4096 个的问题，实际上而言，该解决思路从二层交换网络跳脱出来，VXLAN 在 Layer 3 网络之上构建 Layer 2 网络来完成虚拟化需求，其中 layer 3 网络称为底层网络（underlay），Layer 2 网络称为虚拟网络（overlay），虚拟网络利用底层网络提供的三层转发路径实现二层互通。虽然虚拟网络中的各个节点可能物理上相隔万里，但都可以同其他节点进行局域网般通信，

认为其他节点与自己在同一个局域网中，可以

因此，实际上 VXLAN 更多作为一种隧道技术来讨论。使用三层 UDP 隧道技术来进行拓展。



## 单播（静态泛洪）

BUM 帧复制，静态配置远端 VTEPs 列表

## 术语

| 术语 | 全称                        | 说明                                                         |
| ---- | --------------------------- | ------------------------------------------------------------ |
| FDB  | Forwarding Database Entry   |                                                              |
| NVE  | Network Virtualization Edge |                                                              |
| VTEP | VXLAN Tunnel Endpoint       | VTEP 是 VXLAN 隧道端点，用于 VXLAN 报文的封装和解封装。VTEP 与物理网络相连，分配有物理网络的 IP 地址，该地址与虚拟网络无关。VXLAN 报文中源 IP 地址为本节点的 VTEP 地址，VXLAN 报文中目的 IP 地址为对端节点的 VTEP 地址，一对 VTEP 地址就对应着一个 VXLAN 隧道。 |
| VNI  | VXLAN Network Identifier    | VXLAN 网络标识 VNI 类似 VLAN ID，用于区分 VXLAN 段，不同 VXLAN 段的虚拟机不能直接二层相互通信。 |
| BD   | Bridge Domain               | BD 是 VXLAN 网络中转发数据报文的二层广播域。                 |
| VAP  | Virtual Access Point        | 虚拟接入点 VAP，即 VXLAN 业务接入点，用于接入终端。          |

### VTEP

## Linux kernel tunnel device

This document describes the Linux kernel tunnel device, there is also a separate implementation of VXLAN for Openvswitch.

Unlike most tunnels, a VXLAN is a 1 to N network, not just point to point. A VXLAN device can learn the IP address of the other endpoint either dynamically in a manner similar to a learning bridge, or make use of statically-configured forwarding entries.

The management of vxlan is done in a manner similar to its two closest neighbors GRE and VLAN. Configuring VXLAN requires the version of iproute2 that matches the kernel release where VXLAN was first merged upstream.

1. Create vxlan device:

   ```
   # ip link add vxlan0 type vxlan id 42 group 239.1.1.1 dev eth1 dstport 4789
   ```

This creates a new device named vxlan0. The device uses the multicast group 239.1.1.1 over eth1 to handle traffic for which there is no entry in the forwarding table. The destination port number is set to the IANA-assigned value of 4789. The Linux implementation of VXLAN pre-dates the IANA’s selection of a standard destination port number and uses the Linux-selected value by default to maintain backwards compatibility.

1. Delete vxlan device:

   ```
   # ip link delete vxlan0
   ```

2. Show vxlan info:

   ```
   # ip -d link show vxlan0
   ```

It is possible to create, destroy and display the vxlan forwarding table using the new bridge command.

1. Create forwarding table entry:

   ```
   # bridge fdb add to 00:17:42:8a:b4:05 dst 192.19.0.2 dev vxlan0
   ```

2. Delete forwarding table entry:

   ```
   # bridge fdb delete 00:17:42:8a:b4:05 dev vxlan0
   ```

3. Show forwarding table:

   ```
   # bridge fdb show dev vxlan0
   ```

The following NIC features may indicate support for UDP tunnel-related offloads (most commonly VXLAN features, but support for a particular encapsulation protocol is NIC specific):

> - tx-udp_tnl-segmentation
>
> - - tx-udp_tnl-csum-segmentation
>
>     ability to perform TCP segmentation offload of UDP encapsulated frames
>
> - - rx-udp_tunnel-port-offload
>
>     receive side parsing of UDP encapsulated frames which allows NICs to perform protocol-aware offloads, like checksum validation offload of inner frames (only needed by NICs without protocol-agnostic offloads)

For devices supporting rx-udp_tunnel-port-offload the list of currently offloaded ports can be interrogated with ethtool:

```
$ ethtool --show-tunnels eth0
Tunnel information for eth0:
  UDP port table 0:
    Size: 4
    Types: vxlan
    No entries
  UDP port table 1:
    Size: 4
    Types: geneve, vxlan-gpe
    Entries (1):
        port 1230, vxlan-gpe
```

## 参考

# VXLAN

## 简介



| 简称 | 全称                     | 中文           | 解释                                          |
| ---- | ------------------------ | -------------- | --------------------------------------------- |
| VNI  | VXLAN Network Identifier | VXLAN ID       | 用于区分不同 VXLAN 的标识符，类似于 VLAN ID。 |
| VTEP | VXLAN Tunnel End Point   | VXLAN 隧道端点 | 负责 VXLAN 报文的封装与解封装。               |

## VXLAN 解决的问题

### VLAN

### 多租户

### MAC地址过大

## VXLAN

VXLAN 是一种在 Layer 3 网络之上构建 Layer 2 网络的虚拟化技术，其中 layer 3 网络称为底层网络（underlay），Layer 2 网络称为叠加网络（overlay），Overlay 网络通过封装技术、利用 underlay 网络提供的三层转发路径实现二层互通。

【over 图】

每个 overlay 网络也称为一个 VXLAN 段（VXLAN segment），只有在相同 VXLAN 段中的主机才能直接进行通信。每个 VXLAN 段由一个 24 位的 VNI 标识，这意味着在一个管理域中可以共存多达 $2^{24}$  的 VXLAN 段。

VNI 标识了由主机产生的 MAC 帧的活动范围，VNI 作为外部头，将内部 MAC 帧进行封装后传输。因此，不同 VNI 的 VXLAN 段中流量是隔离的。同时，这也使得不同 VXLAN 段可以使用相同的 MAC 地址。

正是由于封装的特性，VXLAN 也可以称之为三层网络上的二层隧道技术。主机产生的原始帧通过 VTEP 隧道端点，添加 VXLAN 头封装后，通过隧道传输到另一端 VTEP 隧道端点，然后去除 VXLAN 头解封后，传输给目的主机。VTEP 一般在交换机或者服务器上通过软硬件实现，而其中的封装过程对于主机而言是无感的。

【封装过程图】



##  参考

- [RFC7348 - Virtual eXtensible Local Area Network (VXLAN): A Framework for Overlaying Virtualized Layer 2 Networks over Layer 3 Networks](