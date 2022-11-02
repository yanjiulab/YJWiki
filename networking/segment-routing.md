# Segment Routing

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
