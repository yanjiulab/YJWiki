# VPN

## 简介

## 术语

## VPN 层次

以下是 L2 和 L3 VPN 的对比。

| PARAMETER                    | LAYER 2 VPN                                                  | LAYER 3 VPN                                                  |
| :--------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| PHILOSOPHY                   | Layer 2 VPNs 虚拟了数据链路层（2 层），使得物理上相隔甚远的网络看起来就像在同一个局域网中一样。 | Layer 3 VPNs 虚拟了网络层，使得用户的路由器可以在运营商或 Internet 的网络设施基础上，实现三层互联。 |
| TRAFFIC FORWARDING           | VPN 提供商基于用户流量的二层信息进行转发。                   | VPN 提供商基于用户流量的三层信息进行转发。                   |
| SCALABILITY                  | 通常 Layer 2 VPN 可拓展性较差。                              | 通常 Layer 3 VPN 可拓展性较好。                              |
| LAYER 3 CONNECTIVITY         | 同一 VPN 网络中跨地域进行三层互联需要通过用户网络实现，提供商对此无感。 | VPN 用户需要与提供商的网络边缘设备进行三层互联。             |
| SERVICE PROVIDER INVOLVEMENT | 提供商不参与用户网络的 IP 路由。                             | 提供商需要介入用户网络的 IP 路由。                           |
| ROUTING CONTROL              | 当用户需要控制和管理所有的路由及策略时采用该方式。           | 当用户可以分享路由信息给提供商时且不关心策略控制时采用该方式。 |
| EXAMPLES                     | VXLAN, LANE, IPLS, VPLS, EOMPLS, 802.1q Tunnelling           | MPLS VPN, IPSEC P2P                                          |

## VPN 实现模式

目前，VPN 主要有两种实现方式。

### Overlay 模型

VPN 是为了替代物理专用网络而出现，物理专用网络是通过架设或者租用物理线路来实现跨地域的互联。那 VPN 最开始的实现，就是服务提供商（Service provider）向用户提供模拟的线路，用户基于模拟线路来实现跨地域互连，这里的模拟线路也叫做 VC（Virtual circuit）。这种 VPN 的实现方式，就是 overlay 模型。VC 的提供者服务提供商不参与用户网络的组建。用户需要在自己的设备 CPE（Customer Premises Edge）上，建立跨地域的连接。服务提供商的角色如下图所示。

### P2P 模型

peer to peer model：