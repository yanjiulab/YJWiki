# VPN

## L2TP

二层隧道协议L2TP（Layer 2 Tunneling Protocol）是虚拟私有拨号网VPDN（Virtual Private Dial-up Network）隧道协议的一种，扩展了点到点协议PPP（Point-to-Point Protocol）的应用，是远程拨号用户接入企业总部网络的一种重要VPN技术。

## L2TPv3

二层隧道协议第三版L2TPv3(Layer Two Tunneling Protocol - Version 3)是一种二层隧道技术，可以透传多种二层报文（如PPP、Ethernet、HDLC、ATM等），运用于用户侧的二层接入链路在分组交换网络中透明传递。

## GRE

通用路由封装协议GRE（Generic Routing Encapsulation）可以对某些网络层协议（如IPX、ATM、IPv6、AppleTalk等）的数据报文进行封装，使这些被封装的数据报文能够在另一个网络层协议（如IPv4）中传输。

GRE提供了将一种协议的报文封装在另一种协议报文中的机制，是一种三层隧道封装技术，使报文可以通过GRE隧道透明的传输，解决异种网络的传输问题。

## DSVPN

动态智能VPN（Dynamic Smart Virtual Private Network），简称DSVPN，是一种在Hub-Spoke组网方式下为公网地址动态变化的分支之间建立VPN隧道的解决方案。

## IPSec

IPSec（Internet Protocol Security）应运而生。IPSec是对IP的安全性补充，其工作在IP层，为IP网络通信提供透明的安全服务。

## A2A VPN

A2A VPN是Any to Any VPN的简称，是利用组解释域GDOI（Group Domain of Interpretation）协议来集中管理密钥和GDOI安全策略的VPN的一种解决方案。A2A VPN主要用于保护广域网的企业内部业务流量。

以IPSec通道为基础的加密解决方案，可以部署在专线网络中。IPSec是IETF制定的三层隧道加密协议，一直被广泛应用于广域互联分支间的数据加密。它提供了高质量的、可互操作的、基于密码学的安全保证，是一种传统的实现三层VPN的安全技术，特定的通信方之间通过建立IPSec隧道来传输用户的私有数据。

但是，IPSec VPN是一种点到点的隧道技术，主要关注的是数据安全加密，存在如下缺点：

- 企业大量分支间的数据IPSec加密面临N2隧道配置的问题，配置管理复杂，网络扩容能力差。
- IPSec VPN需改变原有路由部署、无法提供更好的QoS处理。
- IPSec VPN无法独立支持组播业务、对智能业务的支持能力差。

综上所述，A2A VPN解决方案应运而生。A2A VPN利用原报文的IP头封装新增的IP头，实现分支间无隧道连接。其通过对密钥和GDOI安全策略的集中管理，简化了网络部署，分布式的分支机构网络既能够大规模扩展，也支持能够确保语音和视频质量的QoS和组播功能。

## BGP/MPLS IP VPN

BGP/MPLS IP VPN是一种L3VPN（Layer 3 Virtual Private Network）。它使用BGP（Border Gateway Protocol）在服务提供商骨干网上发布VPN路由，使用MPLS（Multiprotocol Label Switch）在服务提供商骨干网上转发VPN报文。这里的IP是指VPN承载的是IP（Internet Protocol）报文。

BGP/MPLS IP VPN基于对等体模型，这种模型使得服务提供商和用户可以交换路由，服务提供商转发用户站点间的数据而不需要用户的参与。相比较传统的VPN，BGP/MPLS IP VPN更容易扩展和管理。新增一个站点时，只需要修改提供该站点业务的边缘节点的配置。

BGP/MPLS IP VPN支持地址空间重叠、支持重叠VPN、组网方式灵活、可扩展性好，并能够方便地支持MPLS TE，成为在IP网络运营商提供增值业务的重要手段，因此得到越来越多的应用。

## EVPN

EVPN（Ethernet Virtual Private Network）是一种用于二层网络互联的VPN技术。EVPN技术采用类似于BGP/MPLS IP VPN的机制，通过扩展BGP协议，使用扩展后的可达性信息，使不同站点的二层网络间的MAC地址学习和发布过程从数据平面转移到控制平面。

原有的VXLAN实现方案没有控制平面，是通过数据平面的流量泛洪进行VTEP（VXLAN Tunnel Endpoints）发现和主机信息（包括IP地址、MAC地址、VNI、网关VTEP IP地址）学习的，这种方式导致数据中心网络存在很多泛洪流量。为了解决这一问题，VXLAN引入了EVPN作为控制平面，通过在VTEP之间交换EVPN路由实现VTEP的自动发现、主机信息相互通告等功能，避免了不必要的数据流量泛洪。

EVPN是采用类似于BGP/MPLS IP VPN的机制的VPN技术，在公共网络中传播EVPN路由，在一定程度上保障客户私有数据在公共网络传播的安全性。

在VXLAN网络规模较大时，原有的VXLAN实现方案手工配置比较耗时，通过采用EVPN协议，可以减少人工配置工作量。

## VLL

虚拟租用线路VLL（Virtual Leased Line），又称虚拟专用线路业务VPWS（Virtual Private Wire Service），是对传统租用线业务的仿真，使用IP网络模拟租用线，提供非对称、低成本的数字数据网DDN（Digital Data Network）业务。VLL是建立在MPLS技术上的点对点的二层隧道技术，解决了异种介质不能相互通信的问题。如[图1](mk:@MSITStore:E:\lyj\0-学习\技术手册\AR100, AR120, AR150, AR160, AR200, AR1200, AR2200, AR3200, AR3600 V300R003 产品文档.chm::/dc/dc_fd_vll_1002.html#dc_fd_vll_1002__fig_dc_fd_vll_100201)所示。

## PWE3

端到端伪线仿真PWE3（Pseudo-Wire Emulation Edge to Edge），是一种点到点的MPLS L2VPN技术。它在分组交换网络PSN（Packet Switched Network）中尽可能真实地模仿异步传输ATM（Asynchronous Transfer Mode）、帧中继（FR）、以太网（Ethernet）、低速TDM（Time Division Multiplexing）电路和SONET（Synchronous Optical Network）/SDH（Synchronous Digital Hierarchy）等业务的基本行为和特征。

### VPLS

虚拟专用局域网业务VPLS（Virtual Private LAN Service）是公用网络中提供的一种点到多点的L2VPN（Layer 2 virtual private network）业务，使地域上隔离的用户站点能通过MAN/WAN（Metropolitan Area Network/Wide Area Network）相连，并且使各个站点间的连接效果像在一个LAN（Local Area Network）中一样。它是一种基于MPLS（MultiProtocol Label Switching）网络的二层VPN技术，也被称为透明局域网业务TLS（Transparent LAN Service）。

## VXLAN

RFC定义了VLAN扩展方案VXLAN（Virtual eXtensible Local Area Network，虚拟扩展局域网）。VXLAN采用MAC in UDP（User Datagram Protocol）封装方式，是NVO3（Network Virtualization over Layer 3）中的一种网络虚拟化技术。

