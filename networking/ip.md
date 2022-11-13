# Internet Protocol

IP 协议提供无连接的、尽力而为的服务，是 TCP/IP 网络中的网络层承载协议，也称为 routed 协议。

- 尽力而为即

- *unreliable*. IP provides a **best effort service**, which means there are no guarantees that an IP datagram successfully gets to its destination. 
- *connectionless*. IP does not maintain any state information about successive datagrams.

RFC751定义。
子网的报文如何传送IP。
支持高层协议，主要是TCP和UDP。
无连接协议，不可靠服务，尽力而为的服务策略。

## IPv4 头格式
IP 头格式如下所示：

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|           Total Length        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Time to Live  |    Protocol   |          Header Checksum      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Source Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Destination Address                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Options                 |     Padding   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

- 版本（Version）：4 表示 IPv4，6 表示 IPv6。
- IP 头长度（IHL）：单位为 4 字节，通常 为 5，表示 20 字节。
- 服务类型（ToS）：IP 包“优先级”。
- IP 包总长度（Total Length）：包括 IP 头长度，单位字节。
- 包序号（ID）：按算法生成。
- 标志位（）：
- 段偏移（）：
- 生存时间（TTL）：
- 协议：下一层协议号。
- IP 头校验：
- 源地址：
- 目的地址：

### TOS

TOS 字段主要在以下三个方面进行 tradeoff：

- low-delay
- high-reliability 
- high-throughput 

TOS 8 位含义如下：

- Bits 0-2: Precedence.
- Bit 3: 0 = Normal Delay, 1 = Low Delay.
- Bits 4: 0 = Normal Throughput, 1 = High Throughput.
- Bits 5: 0 = Normal Relibility, 1 = High Relibility.
- Bit 6-7: Reserved for Future Use.  

```
   0     1     2     3     4     5     6     7
+-----+-----+-----+-----+-----+-----+-----+-----+
|    PRECEDENCE   |  D  |  T  |  R  |  0  |  0  |
+-----+-----+-----+-----+-----+-----+-----+-----+
```

Precedence

- 111 - Network Control
- 110 - Internetwork Control
- 101 - CRITIC/ECP
- 100 - Flash Override
- 011 - Flash
- 010 - Immediate
- 001 - Priority
- 000 - Routine  

### IP 头校验

以下是一段 C 语言代码。
```c
uint16_t ip_checksum(uint16_t *pbuf, uint16_t bytes) {
    unsigned int sum;
    unsigned int nwords;
    unsigned short *buf = (unsigned short *) pbuf;
    sum = 0;
    for (nwords = (unsigned int)bytes >> 5; nwords > 0; nwords--) {
        sum += *buf++;
        sum += *buf++;
        sum += *buf++;
        sum += *buf++;
        sum += *buf++;
        sum += *buf++;
        sum += *buf++;
        sum += *buf++;
        sum += *buf++;
        sum += *buf++;
        sum += *buf++;
        sum += *buf++;
        sum += *buf++;
        sum += *buf++;
        sum += *buf++;
        sum += *buf++;
    }

    for (nwords = (unsigned int)(bytes & 0x1f) >> 1; nwords > 0; nwords--) {
        sum += *buf++;
    }

    /* Add left-over byte, if any. */
    if (bytes & 0x01) sum += *buf & (0xff00);

    /* inline ipcom_in_checksum_finish code: */
    while (sum >> 16) {
        sum = (sum & 0xffff) + (sum >> 16);
    }

    return (unsigned short)~(unsigned short)sum;
}
```


## RFC

RFC|标题
---|---
7335|IPv4 Service Continuity Prefix
7249|Internet Numbers Registries
7094|Architectural Considerations of IP Anycast
7020|The Internet Numbers Registry System
6890|Special-Purpose IP Address Registries
6752|Issues with Private IP Addressing in the Internet
6676|Multicast Addresses for Documentation
6598|IANA-Reserved IPv4 Prefix for Shared Address Space
6515|IPv4 and IPv6 Infrastructure Addresses in BGP Updates for Multicast VPN
6346|The Address plus Port (A+P) Approach to the IPv4 Address Shortage
6319|Issues Associated with Designating Additional Private IPv4 Address Space
6308|Overview of the Internet Multicast Addressing Architecture
6306|Hierarchical IPv4 Framework
6269|Issues with IP Address Sharing
6034|Unicast-Prefix-Based IPv4 Multicast Addresses
5889|IP Addressing Model in Ad Hoc Networks
5887|Renumbering Still Needs Work
5771|IANA Guidelines for IPv4 Multicast Address Assignments
5737|IPv4 Address Blocks Reserved for Documentation
5736|IANA IPv4 Special Purpose Address Registry
5735|Special Use IPv4 Addresses
5684|Unintended Consequences of NAT Deployments with Overlapping Address Space
5505|Principles of Internet Host Configuration
4786|Operation of Anycast Services
4632|Classless Inter-domain Routing (CIDR): The Internet Address Assignment and Aggregation Plan
4116|IPv4 Multihoming Practices and Limitations
3927|Dynamic Configuration of IPv4 Link-Local Addresses
3819|Advice for Internet Subnetwork Designers
2908|The Internet Multicast Address Allocation Architecture
2365|Administratively Scoped IP Multicast
2101|IPv4 Address Behaviour Today
2071|Network Reunumbering Overview: Why would I want it and what is it anyway?
2050|Internet Registry IP Allocation Guidelines
2008|Implications of Various Address Allocation Policies for Internet Routing
1918|Address Allocation for Private Internets
1900|Renumbering Needs Work
1878|Variable Length Subnet Table for IPv4
1715|The H Ratio for Address Assignment Efficiency
1546|Host Anycasting Service
1518|An Architecture for IP Address Allocation iwth CIDR
1219|On the assignment of subnet numbers
1042|Standard for transmission of IP datagrams over IEEE 802 networks
791 |Internet Protocol