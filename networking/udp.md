# 传输协议 - UDP

## UDP 简介

用户数据报协议（User Datagram Protocol, UDP）是 OSI 参考模型中一种**无连接**的传输层协议，提供**简单不可靠信息传送服务**。[IETF RFC 768](https://www.rfc-editor.org/rfc/rfc768) 是 UDP 的正式规范，其 IP 报文协议号是 17。与 TCP 相比，UDP 轻量、传输效率高，但是缺少可靠性，通常应用于游戏、流媒体以及 VoIP 等场合。

## 帧格式

UDP 帧格式十分简单，由 8 字节固定包头以及载荷组成。其中 UDP 头格式为：

```
 0      7 8     15 16    23 24    31
+--------+--------+--------+--------+
|   Source Port   |Destination Port |
+--------+--------+--------+--------+
|     Length      |    Checksum     |
+--------+--------+--------+--------+
|          data octets ...
+---------------- ...
```

- 源端口：表示发送进程，非必需情况下可以填零。
- 目的端口：表示特定的互联网服务地址，与 TCP 类似。
- 长度：整个 UDP 包长度（包头长度+数据长度）。
- 校验和：UDP 校验，0 表示不校验。

需要注意的是，**TCP/UDP 校验和同 IP 校验和算法相同**，但 IP 校验只包含首部，而 TCP/UDP 校验包括**伪首部**、**TCP/UDP 首部**与 **TCP/UDP 数据**。伪首部存在的意义在于，TCP/UDP 首部中不包含源地址与目标地址等信息，为了保证校验的有效性，在进行 TCP/UDP 校验和的计算时，需要增加一些 IP 首部信息。伪首部格式如下。

```
0      7 8     15 16    23 24    31
+--------+--------+--------+--------+
|          source address           |
+--------+--------+--------+--------+
|        destination address        |
+--------+--------+--------+--------+
|  zero  |protocol| UDP/TCP length  |
+--------+--------+--------+--------+
```

其中：

- protocol 字段为 TCP/UDP 协议号（TCP 为 6，UDP 为 17）。

- length 字段为 TCP/UDP 头部长度加上数据长度。

?> ICMP 校验和的计算方法同 IP 一样，只不过是对 ICMP 包整个进行校验和，没有伪首部，也不包括 IP 包首部。

## 通信模型

![udp-socket](udp.assets/udp-socket.png)

## QUIC

QUIC（Quick UDP Internet Connection）是谷歌制定的一种基于 UDP 的传输层协议。2021 年 5 月由 IETF 进行了标准化 [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html)。QUIC 为了解决当今传输层和应用层面临的各种需求（包括处理更多的连接，安全性，和低延迟），其设计融合了包括 TCP，TLS，HTTP/2 等协议的特性。

![img](udp.assets/v2-d61a62fdfb08ed3882e1018136ce6b2f_720w.webp)

因此，理解 QUIC 协议需要理解 TCP、TLS、HTTP(S)、HTTP/2 协议过程。
