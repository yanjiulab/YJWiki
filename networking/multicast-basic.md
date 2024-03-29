# IP 组播路由 - 基础

## 组播简介

传统的 IP 通信有：单播（Unicast）、广播（Broadcast）以及组播（Multicast）。

- 对于单播通信，信息源为每个需要信息的主机都发送一份独立的单播 IP 报文，因此网络中传输的信息量与需要该信息的用户量成正比。
- 对于广播通信，信息源将广播 IP 报文发送给该网段中的所有主机，而不管其是否需要该信息。这样不仅存在信息安全性隐患，而且会造成同一网段中信息泛滥。因此该传输方式不利于与特定对象进行数据交互。
- 对于组播通信，信息源向组播地址发送一份组播 IP 报文，网络中只有需要该数据的主机（请求加入该组的主机）可以接收该数据，其他主机不能收到该数据。因此，组播可以很好的解决广播在“点到多点”的数据传输中的缺点。

组播适用于任何“点到多点”的数据发布，主要包含以下几方面：

- 多媒体、流媒体的应用。
- 培训、联合作业场合的通信。
- 数据仓库、金融应用（股票）。

## 组播网络

组播网络由组播源、组播路由器和组播接收者组成。其中，组播网络至少包含一个组播路由器。组播源向组播路由器发送目的 IP 为组播地址（例如 225.0.0.1）的组播报文，组播接收者向组播路由器发送加入某组播地址（例如 225.0.0.1）的请求，组播路由器负责将组播报文传输到每一个加入该组的接收者。

组播的过程与即时通信中的“群聊”概念类似。

组播术语|描述|类比
:---:|:---:|:---:
组播组|用 IP 组播地址进行标识的一个集合|群聊名
组播源|信息的发送者称为“组播源”，一个组播源可以同时向多个组播组发送数据，多个组播源也可以同时向一个组播组发送报文。组播源通常不需要加入组播组。|群聊中消息发布者不管有没有人能收到数据，只是将信息发布在群聊中。
组播组成员|所有加入某组播组的主机便成为该组播组的成员。组播组中的成员是动态的，主机可以在任何时刻加入或离开组播组。|群成员不管谁发的数据，以及数据怎么发来的，只需要接收到该群聊的所有信息。
组播路由器|支持三层组播功能的路由器或交换机。|即时通信服务器，负责转发数据。

类比完之后，让我们回归正经的组播网络，下图是一个组播网络示意图。

![multicast](multicast.assets/multicast.png)

## 组播地址

为了使组播源和组播组成员进行通信，网络层使用组播 IP 地址作为一个组播群组的标识，因此，当路由器收到目的地址为组播地址的报文时，就会按照组播的流程进行转发。IANA 将 D 类地址空间分配给 IPv4 组播使用。IPv4 地址一共 32 位，D 类地址最高 4 位为 1110，因此地址范围从 224.0.0.0 到 239.255.255.255。

|                         地址范围                         |                             含义                             |
| :------------------------------------------------------: | :----------------------------------------------------------: |
|                  224.0.0.0～224.0.0.255                  | 永久组地址。IANA 为路由协议预留的 IP 地址（也称为保留组地址），用于标识一组特定的网络设备，供路由协议、拓扑查找等使用，不用于组播转发。 |
| 224.0.1.0～231.255.255.255<br>233.0.0.0～238.255.255.255 |                ASM 组播地址，全网范围内有效。                |
|                232.0.0.0～232.255.255.255                |         缺省情况下的 SSM 组播地址，全网范围内有效。          |
|                239.0.0.0～239.255.255.255                | 本地管理组地址，仅在本地管理域内有效。在不同的管理域内重复使用相同的本地管理组地址不会导致冲突。 |

常见的永久组地址包括

|  地址范围  |                   含义                   |
| :--------: | :--------------------------------------: |
| 224.0.0.1  | 网段内所有主机和路由器（等效于广播地址） |
| 224.0.0.2  |              所有组播路由器              |
| 224.0.0.4  |   DVMRP（距离矢量组播路由协议）路由器    |
| 224.0.0.5  |               OSPF 路由器                |
| 224.0.0.9  |               RIP-2 路由器               |
| 224.0.0.13 |                PIM 路由器                |

当数据在本地网络上进行传输时，需要提供链路层地址，在单播中通过 ARP 协议获取对端 MAC 地址，但组播数据传输时，其目的地不是一个具体的接收者，而是一个成员不确定的组，那么如何填写 MAC 地址呢？所以需要一种技术将 IP 组播地址映射为组播 MAC 地址。

IANA 规定，IPv4 组播 MAC 地址的高 24 位为 `0x01005e`，第 25 位为 0，低 23 位为 IPv4 组播地址的低 23 位。由于 IPv4 地址 28 位中只有 23 位被映射到 MAC 地址，因此丢失了 5 位的地址信息，导致一些组播地址被映射到相同的 MAC 地址，网络管理员在分配地址时必须考虑这种情况。

## 服务模型

组播服务模型的分类是针对接收者主机的，对组播源没有区别。组播源发出的组播数据中总是以组播源自己的 IP 地址为报文的源地址，组播组地址为目的地址。

然而，接收者主机接收数据时可以对源进行选择，因此产生了 **任意源组播 ASM**（Any-Source Multicast）和 **特定源组播 SSM**（Source-Specific Multicast）两种服务模型。这两种服务模型使用不同的组播组地址范围。

|      对比      |          任意源组播 ASM          |           特定源组播 SSM           |
| :------------: | :------------------------------: | :--------------------------------: |
|    提供服务    |     仅针对组地址提供组播分发     | 针对特定源和组的绑定数据流提供服务 |
| 主机加入组播组 | 可以接收到任意源发送到该组的数据 |   只会收到指定源发送到该组的数据   |
|    组播地址    |  组地址必须在整个组播网络中唯一  |      组地址和组播源对保持唯一      |

## 组播协议族

在 IP 组播传输模型中，发送者不关心接收者所处的位置，只要将数据发送到约定的目的地址，剩下的工作就交给网络去完成。尽管组播源只需要发送数据即可，但仍然有几点需要注意：

- 目的 IP 地址为合理的组播 IP 地址，不要使用预留的地址。
- 目的 MAC 地址需要由 IP 地址映射成正确的组播 MAC 地址。
- TTL 合理设置（至少大于 1）保证组播转发时不会被丢弃。

网络中的组播设备必须收集接收者的信息，并按照正确的路径实现组播报文的转发和复制。因此，在组播的发展过程中，形成了一套完整的协议来完成此任务。

### IPv4 协议族

组播组管理协议（Internet Group Management Protocol, IGMP）是负责 IPv4 组播成员管理的协议，运行在组播网络中的最后一段，即三层网络设备与用户主机相连的网段内。IGMP 协议在主机端实现组播组成员加入与离开，在上游的三层设备中实现组成员关系的维护与管理，同时支持与上层组播路由协议的信息交互。到目前为止，IGMP 有三个版本：IGMPv1、IGMPv2 和 IGMPv3。所有 IGMP 版本都支持 ASM 模型。IGMPv3 可以直接应用于 SSM 模型。

IGMP 侦听协议（IGMP Snooping）可以使二层设备，通过侦听上游的三层设备和用户主机之间发送的 IGMP 报文来建立组播数据报文的二层转发表，管理和控制组播数据报文的转发，进而有效抑制组播数据在二层网络中扩散。

协议无关组播协议（Protocol Independent Multicast, PIM）作为一种 IPv4 网络中的组播路由协议，主要用于将网络中的组播数据流发送到有组播数据请求的组成员所连接的组播设备上，从而实现组播数据的路由查找与转发。PIM 协议包括稀疏模式（Sparse Mode, PIM-SM）和密集模式（Dense Mode, PIM-DM）。PIM-SM 适合规模较大、组成员相对比较分散的网络；PIM-DM 适合规模较小、组播组成员相对比较集中的网络。在 PIM-DM 模式下不需要区分 ASM 模型和 SSM 模型。在 PIM-SM 模式下根据数据和协议报文中的组播地址区分 ASM 模型和 SSM 模型：如果在 SSM 组播地址范围内，则按照 PIM-SM 在SSM 中的实现流程进行处理。PIM-SSM 不但效率高，而且简化了组播地址分配流程，特别适用于对于特定组只有一个特定源的情况。如果在 ASM 组播地址范围内，则按照 PIM-SM 在 ASM 中的实现流程进行处理。

组播源发现协议（Multicast Source Discovery Protocol, MSDP）是为了解决多个 PIM-SM 域之间的互连的一种域间组播协议，用来发现其他 PIM-SM 域内的组播源信息，将远端域内的活动信源信息传递给本地域内的接收者，从而实现组播报文的跨域转发。只有 PIM-SM 使用 ASM 模型时，才需要使用 MSDP。

组播边界网关协议（MultiProtocol Border Gateway Protocol）实现了跨 AS 域的组播转发。适用于组播源与组播接收者在不同 AS 域的场景。

### IPv6 协议族

组播侦听者发现协议 MLD（Multicast Listener Discovery, MLD） 是负责 IPv6 组播成员管理的协议，运行在组播网络中的最后一段，即三层组播设备与用户主机相连的网段内。MLD 协议在主机端实现组播组成员加入与离开，在三层设备上实现组成员关系的维护与管理，同时支持与组播路由协议的信息交互。到目前为止，MLD 有两个版本：MLDv1 和 MLDv2。MLDv2 版本可以直接应用于 SSM 模型，而 MLDv1 则需要通过使用 SSM Mapping 机制来支持 SSM 模型。MLD 可以理解为 IGMP 的 IPv 6版本。两者的实现方式具有类比性，如 MLDv1 可以类比 IGMPv2，MLDv2 可以类比 IGMPv3。

PIM（IPv6）作为一种 IPv6 网络中的组播路由协议，主要用于将网络中的组播数据流引入到有组播数据请求的组成员所连接的交换机上，从而实现组播数据流的路由查找与转发。

MLD Snooping 协议可以使交换机工作在二层时，通过侦听上游的三层设备和用户主机之间发送的 MLD 报文来建立组播数据报文的 IPv6 二层转发表，管理和控制组播数据报文的转发，进而有效抑制组播数据在二层网络中扩散。MLD Snooping Proxy 功能在 MLD Snooping 的基础上使交换机代替上游三层设备向下游主机发送查询报文和代替下游主机向上游设备发送 MLD Report 和 Done 报文，这样能够有效的节约上游设备和本设备之间的带宽。MLD Snooping 可以理解为 IGMP Snooping 的 IPv6 版本。
