# VXLAN

## 简介

VXALN 全称为 Virtual eXtensible Local Area Network，即虚拟扩展局域网。顾名思义，该技术是 VLAN 的扩展。

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

- [RFC7348 - Virtual eXtensible Local Area Network (VXLAN): A Framework for Overlaying Virtualized Layer 2 Networks over Layer 3 Networks](https://datatracker.ietf.org/doc/html/rfc7348)