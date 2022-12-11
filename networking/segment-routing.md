# Segment Routing

## SR 背景

Segment Routing 是路由领域的一个新宠儿，特别契合于自治网络或集中式控制网络（如 SDN），SR 与 MPLS 和 IPv6 两种技术深度绑定。因此，在学习 SR 之前需要对这两种技术做到基本熟悉。

### 源路由

SR 是一种**源路由协议**（Source Routing），在 RFC 791 中，定义了 IPv4 基本的路由模型是**基于目的地址转发**，对于一个给定数据包，路由器只能根据其目的地址来选择路由（选择下一跳），发送者以及数据包其他字段均不能影响路径转发。然而，IPv4 还规定了**源路由**模式，通过 **IP 选项域**字段来实现发送者对于转发路径的更多控制，这意味着发送者可以为数据包指定转发路径，控制数据包如何到达目的地。例如图中绿色是一条常规路由转发使用的最短路径，红色是源路由选择的转发路径。

![img](segment-routing.assets/SegmentRouting.png)

在 IPv4 中有两种源路由协议，两者均是**在 IP 首部选项域字段存入一个逐跳列表**实现，这个列表也称作**路由数据**。

- **Loose Source and Record Route** (LSRR)：松散是指逐跳列表中的**下一跳节点不需要直接相连**，只需要指定一个大致的转发路径即可。如果两跳不直接相连，则由路由器决定具体转发到哪个节点。
- **Strict Source and Record Route** (SRRR)：严格是指逐跳列表中的**下一跳节点必须是直接相连**的。如果路由器发现逐跳列表里不是直接相连的，则会丢弃该数据。

综上所述，源路由的显著特点是路由在数据包中存储，沿途路由器无需再保存路由表等数据，只需要按照数据包中的指示转发即可，减轻了路由器负担。但与此同时却对数据发送者要求更高，等于是将这部分开销转移了。相对于分布式路由，源路由更适用于集中控制网络，可以通过指定路径更为方便的实现转发优化、流量控制等。但与此同时，源路由也带来了一定的安全问题，因此目前大部分路由器的源路由功能都不会默认开启。

### MPLS 简介

暂时先全放到这里，如果太多考虑单独列出。

### SR 简介







## Overview

段路由（Segment Routing），以下简称 SR。

需要一点IGP的拓展

不需要 LDP 和 RSVP-TE

每个路由器（节点）和每条链路（邻居）都有一个段 ID（Segment Identifier, SID）。

- 节点 SID 是全局唯一的，网络管理员从保留块中为每一个路由器分配一个节点 SID。
- 邻居 SID 是局部唯一的，路由器自动从 SID 保留块之外为路由器每个连接邻居路由器的接口分配一个 邻居 SID。

## Segments

段（segment）是指令的标识符，指令包括转发（forwarding）和服务（service）两种。

### Global and Local Segments

### IGP segments

#### IGP Prefix Segment

包含 IGP 计算出的 IP 地址前缀。Node SID 是一种包含节点的 Loopback 地址的特定格式 Prefix SID。

【图】

#### IGP Adjacency Segment

Adjacency SID：包含路由器与邻居的邻居关系。Adjacency SID 是针对单个路由器局部唯一的。

【图】

#### 组合

【图】

## SR 数据平面

SR 协议数据面

- MPLS
- IPv6

### SR MPLS 数据平面

SR MPLS 数据平面复用已有的 MPLS 数据平面：

- Segment -> label
- Segment list -> label stack

可以使用 PHP 特性和 Explicit-Null 功能。

#### 转发流程

【图-总体图】

-----R1-------------- R2 ---------------- R3 --------- R4

pl --- pl+16004 ------  pl+16004 ----------pl ----------

- push
- swap
- pop
- exp-null

#### SRGB

范围：16000-23999

Label=Prefix-SID index + SRGB range

E.g. Prefix 1.1.1.65/32 with prefix-SID index 65 gets label 16065

建议所有节点 SRGB 相同，不同可以，但没必要。转发时会减去base值看index值。

#### 标签动态分配

label range

- 0-15：special
- 16-15999：static MPLS labels
- 16000-23999：srgb
- 24000-up：dynamic label allocation

大多数 MPLS 应用使用 LSD Label Switching Database 动态分配的标签。

- LDP，RSVP，L2VPN，BGP（LU，VPN），ISIS（Adj-SID），OSPF（Adj-SID），TE（Binding-SID）

## SR IGP 控制平面

使用 IGP 协议来分发 segment

### SR IS-IS 控制平面

- 支持 IPv4、IPv6 协议
- Prefix-SID loopback 接口
- Adj-SID 邻居接口
- Prefix-to-SID mappiing advertisements（mapping server）
- MPLS PHP and Exp-NULL

#### 各种extensions

在 IS-IS 协议中，通过定义一些新的 IS-IS sub-TLV，用于 SR 来通告设备相关的能力和 segments。

| sub-TLVs                       | 解释 |
| ------------------------------ | ---- |
| SR Capability sub-TLV (2)      |      |
| Prefix-SID sub-TLV (3)         |      |
| Prefix-SID sub-TLV (3)         |      |
| Prefix-SID sub-TLV (3)         |      |
| Prefix-SID sub-TLV (3)         |      |
| Adjacency-SID sub-TLV (31)     |      |
| LAN-Adjacency-SID sub-TLV (32) |      |
| Adjacency-SID sub-TLV (31)     |      |
| LAN-Adjacency-SID sub-TLV (32) |      |
| SID/Label Binding TLV (149)    |      |

draft-ietf-isis-segment-routing-extensions-02

### SR OSPF 控制平面

- 支持 IPv4、IPv6 协议
- Prefix-SID loopback 接口
- Adj-SID 邻居接口
- Prefix-to-SID mappiing advertisements（mapping server）
- MPLS PHP and Exp-NULL

#### 【各种Extensions】

draft-ietf-ospf-segment-routing-extensions-02

## 参考

- [https://www.segment-routing.net/](https://www.segment-routing.net/)

- [Introduction to Segment Routing](https://learningnetwork.cisco.com/s/blogs/a0D3i000002SKP6EAO/introduction-to-segment-routing)
- 
