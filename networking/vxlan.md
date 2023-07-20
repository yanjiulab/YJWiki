# 隧道 - VXLAN 协议

## 简介

VXALN 全称为 Virtual eXtensible Local Area Network，即虚拟扩展局域网，由 RFC 7348 描述。表面上来看，该技术是 VLAN 的扩展，用来解决 802.1q 协议中 VLAN ID 不能超过 4096 个的问题，实际上而言，该解决思路从二层交换网络跳脱出来，VXLAN 在 Layer 3 网络之上构建 Layer 2 网络来完成虚拟化需求，其中 layer 3 网络称为底层网络（underlay），Layer 2 网络称为虚拟网络（overlay），虚拟网络利用底层网络提供的三层转发路径实现二层互通。虽然虚拟网络中的各个节点可能物理上相距很远，但都可以同其他节点进行局域网通信，因此 VXLAN 实际上可以看做是一种隧道技术。

总而言之，VXLAN 解决了三个痛点问题：

- VLAN：
- 多租户：
- MAC 地址过大：

## 基本概念

顶层网络/虚拟网络（Overlay）也称为 VXLAN 段（VXLAN segment），只有在相同 VXLAN 段中的主机才能直接进行通信。每个 VXLAN 段由一个 24 位的 VNI 标识，这意味着在一个管理域中可以共存多达 $2^{24}$  的 VXLAN 段。

VNI 标识了由主机产生的 MAC 帧的活动范围，VNI 作为外部头，将内部 MAC 帧进行封装后传输。因此，不同 VNI 的 VXLAN 段中流量是隔离的。同时，这也使得不同 VXLAN 段可以使用相同的 MAC 地址。

正是由于封装的特性，VXLAN 也可以称之为三层网络上的二层隧道技术。主机产生的原始帧通过 VTEP 隧道端点，添加 VXLAN 头封装后，通过隧道传输到另一端 VTEP 隧道端点，然后去除 VXLAN 头解封后，传输给目的主机。VTEP 一般在交换机或者服务器上通过软硬件实现，而其中的封装过程对于主机而言是无感的。

| 术语 |           全称            |       中文       | 说明                                                         |
| :--: | :-----------------------: | :--------------: | ------------------------------------------------------------ |
| VNI  | VXLAN Network Identifier  | VXLAN 网络标识符 | VNI 类似 VLAN ID，处于同一 VXLAN 段的主机才能互相二层通信。  |
| VTEP |   VXLAN Tunnel Endpoint   |  VXLAN 隧道端点  | 隧道端点是用于 VXLAN 报文的封装和解封装。VTEP 与物理网络相连，分配有物理网络的 IP 地址，VXLAN 报文中外部 IP 头中的地址即为 VTEP 地址。 |
| FDB  | Forwarding Database Entry |      转发表      | VXLAN 转发表类似于 MAC 转发表。                              |
|  \   |       VXLAN Gateway       |    VXLAN 网关    | 网关负责不同 VXLAN 之间互相进行通信。                        |

其中转发表结构为：

| VNI  |     MAC 地址      | VTEP IP  |
| :--: | :---------------: | :------: |
|  10  | 01:02:03:04:05:06 | 10.0.0.1 |
| ...  |        ...        |   ...    |

## 转发原理

与其他隧道技术不同，VXLAN 隧道模型是 1 对 N，而不是点对点。VXLAN 设备可以通过类似网桥学习机制来动态学习其他 VXLAN 节点信息，也可以通过静态配置转发表。

### 单播 VM-to-VM 通信

假设同一 VXLAN 网段内两个 VM A 与 B 进行通信，A 向 B 正常发送 MAC 帧。

- VTEP 查看 VM 属于哪个网段，获得该网段 VNI。
- 在该网段范围内，查看转发表是否有该"目的 MAC-VTEP" 表项。
- 若有，则封装数据包发送到该远端 VTEP；否则，丢弃该数据包。
- 远端 VTEP 收到数据包，解封获取内层目的 MAC，确认是否属于该网段。
- 若属于，则转发给该 VM，同时进行“内层源 MAC-外层源 IP” 学习，存储到转发表；若不属于，则丢弃。

### BUM 通信

同一 VXLAN 内主机进行 IP 通信时，主机开始不知道对端主机 MAC 地址，会发送 ARP 请求报文请求对端主机 MAC 地址。在正常二层网络中，该 ARP 请求报文 MAC 为广播 MAC，因此将会发送到同一广播域内所有主机上，目的主机通过单播回复 ARP 响应给发送者，使发送主机学习到对端 MAC 地址。

这个问题可以归类为 BUM (Broadcast, Unknown Unicast, Multicast) 帧转发问题，VXLAN 网络也需要机制来解决该问题，例如

- BUM 帧复制，静态配置远端 VTEPs 列表。
- BGP-EVPN 控制面

## VXLAN 帧格式

内部二层帧通过四层外部头进行 UDP 封装，如下图所示。

![vxlan-format](vxlan.assets/vxlan-format.png)

其中：

- 外部以太网头：由物理网络决定，VLAN 头是可选的。
- 外部 IP 头：源 IP 为本地 VTEP 地址，目的 IP 为对端 VTEP 地址。
- 外部 UDP 头：目的端口为 VXLAN 端口，默认为 4789。UDP 校验为一般为 0，保证所有包都能正常被 VTEP 接收。
- VXLAN 头：FLAG I 位为 1，其余为 0。

## Linxu 内核实现

### 基本命令

Linux 操作系统上 VXLAN 实现主要来自于 Linux 内核或 Openvswitch。

VXLAN 设备（或称 VTEP）管理可以通过 **iproute2** 命令来完成。

创建 vxlan 设备:

```
# ip link add vxlan0 type vxlan id 42 group 239.1.1.1 dev eth1 dstport 4789
```

删除 vxlan 设备:

```
# ip link delete vxlan0
```

列出 vxlan 信息:

```
# ip -d link show vxlan0
```

VXLAN 表项管理通过 **bridge** 命令来完成：

创建转发表项:

```
# bridge fdb add/append to 00:17:42:8a:b4:05 dst 192.19.0.2 dev vxlan0
```

- 其中，若动作为 add，则重复添加将会报错，如果想要追加 dst 地址，则使用 append 命令，这样一个 MAC 具有多个 VTEP 地址。

删除转发表项:

```
# bridge fdb delete 00:17:42:8a:b4:05 dev vxlan0
```

列出转发表项:

```
# bridge fdb show dev vxlan0
```

### 组播动态转发

通常情况下，VXLAN 数据分发使用组播模式最为方便。

- 通过同一组地址，自动发现其他 VTEP。
- 组播 1 对 N 数据分发模型契合 VXLAN 1 对 N 隧道模型。
- 利用组播分布式特性，无控制面。

首先，创建 vxlan 设备:

```
# ip link add vxlan0 type vxlan id 42 group 239.1.1.1 dev eth1 dstport 4789
```

VXLAN 创建之后，需要为 vxlan0 配置 IP 地址，这样相当于把主机自身挂在 vxlan0 设备上，因此系统会生成路由表，到达该网段的路由出端口为 vxlan0 虚拟接口。

```
# ip addr add 10.0.0.1/24 dev vxlan0
# ip link set vxlan0 up
# ip route show
10.0.0.0/24 dev vxlan0 proto kernel scope link src 10.0.0.1
...
```

此时，假设我们从主机上 ping 10.0.0.2 时，在 vxlan0 接口上可以抓到原始 ARP 帧，在 eth1 上可以抓到 VXLAN 封装的 ARP 包。

![image-20221106164343535](vxlan.assets/image-20221106164343535.png)

若主机上具有虚拟主机，则 VM 可通过网桥与 vxlan0 设备相连，VM 流量通过网桥交换到 VXLAN 设备，进一步封装到远端 VTEP。此时 vxlan0 可以没有 IP 地址。

总的来说，VTEP 类似于一个网桥，远端 VTEP 是虚拟端口：

- VTEP 接收到本机 vxlan0（或经过网桥交换而来）的 BUM 流量时，从物理接口向该 VNI 所属组地址发送 VXLAN 封装帧；
- VTEP 从物理接口接收到流量时，通过源地址学习到“主机 MAC--VTEP IP 地址”映射，并转发给本机或后续网络设备。

### 无组播环境

在有些网络环境中，不具备组播或是组播部署复杂是，可以通过单播来完成 BUM 数据转发。

#### 单播静态泛洪

When the associations of MAC addresses and VTEPs are known, it is possible to pre-populate the FDB and disable learning:

```
# ip link add vxlan0 type vxlan id 42 local 192.168.0.103 dstport 4789
# bridge fdb append 00:00:00:00:00:00 dev vxlan0 dst 192.168.0.101
# bridge fdb append 00:00:00:00:00:00 dev vxlan0 dst 192.168.0.102
```

不需要指定组地址，而是指定 local 本地地址，数据转发时进行转发表：BUM 帧会复制多份，发往所有全 0 MAC 表项的 VTEP 地址。此时 VTEP 仍然会进行源地址学习，生成对应的“MAC-VTEP”表项。注意，此时转发表中的 VTEP 地址必须具有 ARP 表项，VTEP 不会向没有 ARP 表项的目的 VTEP 地址封装数据。

单播静态泛洪是最简单的方式，仅需要一点自动化脚本即可保证所有 VTEP 转发表保持更新，该方式最大的缺点就是远端 VTEP 越多，则复制的份数越多，大型网络中会造成 VXLAN 冗余流量过大。

#### 单播静态 L2 表项

如果事先知道所有主机的 MAC 地址、所有 VTEP 地址，以及二者所属关系，那么在泛洪的基础上，可以预配转发表项并且禁止源地址学习功能。这样 U 帧可以直接转发，但 BM 帧仍然需要全 0 表项泛洪，因此全 0 表项仍然需要保留。

```
# ip link add vxlan0 type vxlan id 42 local 192.168.0.103 dstport 4789 nolearning
```

```
# bridge fdb append 00:00:00:00:00:00 dev vxlan0 dst 192.168.0.101
# bridge fdb append 00:00:00:00:00:00 dev vxlan0 dst 192.168.0.102
# bridge fdb append 50:54:33:00:00:09 dev vxlan0 dst 192.168.0.101
# bridge fdb append 50:54:33:00:00:0a dev vxlan0 dst 192.168.0.102
```

[BGP EVPN](https://tools.ietf.org/html/rfc7432) with [FRR](https://github.com/FRRouting/frr) is an example of this strategy (see “[VXLAN: BGP EVPN with FRR](https://vincent.bernat.ch/en/blog/2017-vxlan-bgp-evpn)” for additional information).

#### 单播静态 L3 表项

在上述基础上，如果还知道所有主机的 IP 地址（适用于容器网络），可以通过配置 ARP 表项来完成 ARP 地址学习，这样可以避免使用全 0 MAC 地址，也能进一步减少 ARP 广播流量。

```
# ip link add vxlan0 type vxlan id 42 local 192.168.0.103 dstport 4789 nolearning proxy
# ip neigh add 10.0.0.2 lladdr 50:54:33:00:00:09 dev vxlan0
# ip neigh add 10.0.0.3 lladdr 50:54:33:00:00:0a dev vxlan0
# bridge fdb append 50:54:33:00:00:09 dev vxlan0 dst 192.168.0.101
# bridge fdb append 50:54:33:00:00:0a dev vxlan0 dst 192.168.0.102
```

这种方式不再需要复制，但不适用于组播场景。

#### 单播动态 L3 表项

Linux 可以监控程序 L2 或 L3 是否表项缺少。

```
# ip link add vxlan0 type vxlan id 42 local 192.168.0.103 dstport 4789 nolearning proxy l2miss l3miss
# ip neigh add 10.0.0.2 lladdr 50:54:33:00:00:09 dev vxlan0
# ip neigh add 10.0.0.3 lladdr 50:54:33:00:00:0a dev vxlan0
# bridge fdb append 50:54:33:00:00:09 dev vxlan0 dst 192.168.0.101
# bridge fdb append 50:54:33:00:00:0a dev vxlan0 dst 192.168.0.102
```

当缺少表项时，ip 命令会使用 `NETLINK_ROUTE` 协议向监听  `AF_NETLINK` 的套接字发送通告，这个套接字必须绑定到 `RTNLGRP_NEIGH` 组。使用以下命令可以解析出该通告。

```
# ip monitor neigh dev vxlan100
miss 10.0.0.2 STALE
miss lladdr 50:54:33:00:00:0a STALE
```

其中：

- 第一条通告表示缺少该 IP 的 MAC 地址
- 第二条通告表示缺少该 MAC 的 VTEP 地址

通过这种机制，我们可以编写程序，监听 `RTNLGRP_NEIGH` 通告消息，然后向某个"中心注册站"发送查询获取最新的表项对应关系，然后使用如下命令动态配置转发表。

```
# ip neigh replace 10.0.0.2 lladdr 50:54:33:00:00:09 dev vxlan0 nud reachable
# bridge fdb replace 50:54:33:00:00:09 dst 192.168.0.101 dev vxlan0 dynamic
```

其中，nud 和 dynamic 表示该配置不是永久性的，具有标准的超时时间。

这种方式适合于容器网络，并且具有某个中心注册站的环境。但这种方式在第一次数据通信引入了一点时延，同时也不适用于组播或者广播环境。

### 总结

综上所述，没有一种解决方案适合所有的情况，但是如果满足以下条件，就应该考虑使用**组播**模式：

- 底层网络具有组播环境；
- 虚拟网络需要组播和广播通信；
- 事先无法获取 L2 和 L3 表项。

当组播模式不可用时，考虑优先使用**单播静态 L2 表项**，因为该方式具有一种通用解决方式 **BGP EVPN**：其中 BGP 协议作为控制面，用来分发 VTEP 地址和对应的 FDB 表项。协议具体实现可以参考 [FRR](https://github.com/FRRouting/frr)。

如果是容器环境下，IP 和 MAC 地址很容易提前获取，则可以考虑基于中心注册站并取消源地址学习，使用**单播静态/动态 L3 表项** 实现 VXLAN 网络配置，将会更加安全、高效。

## 参考

- [RFC7348 - Virtual eXtensible Local Area Network (VXLAN): A Framework for Overlaying Virtualized Layer 2 Networks over Layer 3 Networks](https://datatracker.ietf.org/doc/html/rfc7348)
- [VXLAN & Linux](https://vincent.bernat.ch/en/blog/2017-vxlan-linux)

- [VXLAN: BGP EVPN with FRR](https://vincent.bernat.ch/en/blog/2017-vxlan-bgp-evpn)
