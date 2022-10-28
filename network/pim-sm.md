# PIM-SM

## PIM-SM 协议

- RIB
- MRIB

### 阶段 1：RP Tree

在该阶段，组播接收者只需表明自己感兴趣的组播组即可。

- 组播接收者所在子网会竞选出一个路由器作为该子网 DR（Designated Router），DR 可视为该子网的 PIM 代理，接收者通过向 DR 发送 IGMP/MLD Join/Leave 消息来表明自己是否加入/退出该组播组。
- 当接收者想加入组 G 时，向 DR 发送 IGMP Join 消息。DR 收到接收者发送的对于某个组 G 的 IGMP Join 消息时，便向 RP 发送一个对该组的 PIM Join 消息，即 `(*, G)` Join。该 Join 消息逐跳发送至 RP，沿途每一个 PIM 路由器都会建立 `(*, G)` 表项。当越来越多的接收者加入组 G 时，RP 就形成了一颗以自身为根的组播 G 分发树，即 RP Tree。RPT 也称为共享树，即所有组播源共享该树进行组播组 G 的数据分发。Join 消息将会周期性发送，以保证接收者一直在组中。
- 当接收者想退出组 G 时，向 DR 发送 IGMP Leave 消息。DR 收到接收者发送的对于某个组 G 的 IGMP Leave 消息时，便向 RP 发送一个对该组的 PIM Prune 消息，即 `(*, G)` Prune。Prune （剪枝）消息将会周期性发送，以保证接收者一直不接收该组消息。如果 剪枝消息没有发送，则又会恢复对该接收者的转发。

在该阶段，组播发送者只需要向某组发送组播数据即可。

- 源端 DR 收到组播数据，进行**单播封装**，直接发给 RP。这个过程称为 Registering，封装的数据包称为 PIM Register 消息。
- RP 收到单播数据包，进行**解封**，再沿 RPT 发送给组播接收者。

总结，在 RPT 阶段 ，组播数据将会打包成单播发给 RP，然后再根据组播路由表沿 RPT 发送到接收者。

### 阶段 2：SS Tree

当 RP 从源端 S 接收到一个组 G 的 register 封装组播包时，会向 S 发送一个特定源组播加入消息，即 `(S, G)` Join。该 Join 消息逐跳发送至 S，沿途每一个 PIM 路由器都会建立 `(S, G)` 表项。此后，从 S 发来的 G 组播数据将会根据 `(S, G)` 表项向 RP 转发。

> These data packets may also reach routers with (*,G) state along the path towards the
> RP; if they do, they can shortcut onto the RP tree at this point.  

当 RP 向 S 发送特定源组播加入消息时，组播封装包也在进行。如果数据包开始按照 `(S, G)` 进行转发，则 RP 会收到两份数据包。此时，RP 会丢弃封装数据包，并且向源端 DR 发送 Register-Stop 以表示停止封装不需要的数据包。

总结，在 SST 阶段，组播数据沿着 Source-Specific Tree 发送到 RP，然后再沿 RPT 发送到接收者。如果两个树有交叉，则数据会从 SST 转发至 RPT，从而跳过 RP。

###  阶段 3：SP Tree

虽然 SST 阶段解决了数据包封装解封的问题，但仍然没有完全优化转发路径。相比于直接经过最短路径，数据从组播源到组播接收者，都需要经过 RP ，而这可能会造成走弯路。因此，为了获取更低的时延和更高的带宽利用率，接收端 DR 可以选择将 RPT 切换至 SPT (Source Specific Shortest Path Tree)。

- 首先，接受端 DR 向组播源 S 发送一个 `(S, G)` Join 消息。
- 接着，沿途每一个 PIM 路由器都会建立 `(S, G)` 表项。
- 最后，该 Join 消息逐跳发送至 S 所在子网，或者到达一个已经拥有 `(S, G)` 表项的路由器。

此时，DR 或 DR 上游路由器，又将会收到两份数据，一份来自 RPT，一份来自 SPT。

- 第一次收到 SPT 数据时（他怎么知道是哪里来的？），丢弃从 RPT 发来的数据。
- 向 RP 发送 `(S, G, rpt)` Prune 消息。
- 该消息逐跳传播，告知沿途路由器 S 发往 G 的数据不能再沿此路转发。
- 最终，该消息发送至 RP，或者仍然需要该路径的路由器。

总结，在 SPT 阶段，数据从 S 到接收者经过最短路径传输。此时 RP 仍然会接收到 S 的数据，但是并不会沿着 RPT 发送到接收者。从接收者的角度来看，这就是最终的组播分发树状态。

## PIM-SSM 协议

PIM Source Specific Multicast 服务模型是 PIM-SM 服务模型的子集，也可称为 SM 的特殊模式。

IGMPv3 允许接收者只接收从指定源 S 发出的 G 组播数据。在这种情况下，接收端 DR 将会直接跳过向 RP 发送 `(*, G)` Join 消息而直接向 S 发送 `(S, G)` Join 消息，这个阶段称为指定源组播模式（PIM-SM/SSM）。PIM-SSM 使用 232.0.0.0 to 232.255.255.255 IP 地址。

相反的，IGMPv3 允许接收者只拒绝从指定源 S 发出的 G 组播数据。在这种情况下，接收端 DR 将会照常向 RP 发送 `(*, G)` Join 消息，但是却紧跟一个 `(S, G, rpt)` Prune 消息。

## RP Discovery

## PIM 协议状态机

RFC 4601 定义了 PIM 协议的状态机，称为 TIB (Tree Information Base)。然而大多数实现并没有完全按照 TIB 来设计，而是依靠维护组播路由表来完成 PIM 协议的交互。

- 初始态
- `(*,*,RP)`
- `(*,G)`
- `(S,G)`
- `(S,G,rpt)`

### 初始态

```
For each interface:
    • Effective Override Interval
    • Effective Propagation Delay
    • Suppression state: One of {"Enable", "Disable"}
    Neighbor State:
      For each neighbor:
        • Information from neighbor’s Hello
        • Neighbor’s GenID.
        • Neighbor Liveness Timer (NLT)
    Designated Router (DR) State:
        • Designated Router’s IP Address
        • DR’s DR Priority
```

### `(*,*,RP)`

```
For every RP, a router keeps the following state:
    (*,*,RP) state:
        For each interface:
          PIM (*,*,RP) Join/Prune State:
            • State: One of {"NoInfo" (NI), "Join" (J), "Prune-Pending" (PP)}
            • Prune-Pending Timer (PPT)
            • Join/Prune Expiry Timer (ET)
        Not interface specific:
          Upstream (*,*,RP) Join/Prune State:
            • State: One of {"NotJoined(*,*,RP)", "Joined(*,*,RP)"}
          • Upstream Join/Prune Timer (JT)
          • Last RPF Neighbor towards RP that was used
```



### `(*,G)`

```
For every group G, a router keeps the following state:
  (*,G) state:
    For each interface:
        Local Membership:
        	State: One of {"NoInfo", "Include"}
        PIM (*,G) Join/Prune State:
            • State: One of {"NoInfo" (NI), "Join" (J), "Prune-Pending" (PP)}
            • Prune-Pending Timer (PPT)
            • Join/Prune Expiry Timer (ET)
        (*,G) Assert Winner State
        	• State: One of {"NoInfo" (NI), "I lost Assert" (L), "I won Assert"
        (W)}
            • Assert Timer (AT)
            • Assert winner’s IP Address (AssertWinner)
            • Assert winner’s Assert Metric (AssertWinnerMetric)
    Not interface specific:
      Upstream (*,G) Join/Prune State:
    	• State: One of {"NotJoined(*,G)", "Joined(*,G)"}
      • Upstream Join/Prune Timer (JT)
      • Last RP Used
      • Last RPF Neighbor towards RP that was used
```



### `(S,G)`

```
For every source/group pair (S,G), a router keeps the following state:
  (S,G) state:
      For each interface:
        Local Membership:
        	State: One of {"NoInfo", "Include"}
        PIM (S,G) Join/Prune State:
            • State: One of {"NoInfo" (NI), "Join" (J), "Prune-Pending" (PP)}
            • Prune-Pending Timer (PPT)
            • Join/Prune Expiry Timer (ET)
        (S,G) Assert Winner State
            • State: One of {"NoInfo" (NI), "I lost Assert" (L), "I won Assert" (W)}
            • Assert Timer (AT)
            • Assert winner’s IP Address (AssertWinner)
            • Assert winner’s Assert Metric (AssertWinnerMetric)
      Not interface specific:
        Upstream (S,G) Join/Prune State:
        	• State: One of {"NotJoined(S,G)", "Joined(S,G)"}
        • Upstream (S,G) Join/Prune Timer (JT)
        • Last RPF Neighbor towards S that was used
        • SPTbit (indicates (S,G) state is active)
        • (S,G) Keepalive Timer (KAT)
        Additional (S,G) state at the DR:
            • Register state: One of {"Join" (J), "Prune" (P), "Join-Pending" (JP), "NoInfo" (NI)}
            • Register-Stop timer
        Additional (S,G) state at the RP:
        	• PMBR: the first PMBR to send a Register for this source with the Border bit set.
```



### `(S,G,rpt)`

```
For every source/group pair (S,G) for which a router also has (*,G) state, it also keeps the
following state:
  (S,G,rpt) state:
    For each interface:
    	Local Membership:
    		State: One of {"NoInfo", "Exclude"}
    	PIM (S,G,rpt) Join/Prune State:
            • State: One of {"NoInfo", "Pruned", "Prune-Pending"}
            • Prune-Pending Timer (PPT)
            • Join/Prune Expiry Timer (ET)
    Not interface specific:
    	Upstream (S,G,rpt) Join/Prune State:
    		• State: One of {"RPTNotJoined(G)", "NotPruned(S,G,rpt)", "Pruned(S,G,rpt)"}
    		• Override Timer (OT)
```





## PIM 数据包格式

PIM 控制消息承载于 IP 协议，协议号为 103。PIM 消息分为两种：

- 单播：
  - Register 消息
  - Register-Stop 消息
  - Candidate-RP-Advertisement 消息
- 组播：目的地址为 ALL-PIM-ROUTERS 组（224.0.0.13/IPv4，ff02::d/IPv6），TTL 为 1。
  - Hello 消息
  - ....

### PIM 通用头

PIM 消息头如下所示，共计 4 字节（4b+4b+8b+16b=32b=4B）。

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|PIM Ver|  Type |   Reserved    |            Checksum           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

其中，类型字段解释如下。

| 类型          | 值   | 组播模式     | 目的地址                              |
|:-------------:|:----:| ----------- | ------------------------------------ |
| Hello         | 0    |             | Multicast to ALL-PIM-ROUTERS         |
| Register      | 1    |             | Unicast to RP                        |
| Register-Stop | 2    |             | Unicast to source of Register packet |
| Join/Prune    | 3    |             | Multicast to ALL-PIM-ROUTERS         |
| Bootstrap     | 4    |             | Multicast to ALL-PIM-ROUTERS         |
| Assert        | 5    |             | Multicast to ALL-PIM-ROUTERS         |
| Graft         | 6    | PIM-DM only | Unicast to RPF’(S)                   |
| Graft-Ack     | 7    | PIM-DM only | Unicast to source of Graft packet    |
| C-RP-Adv      | 8    |             | Unicast to Domain’s BSR              |

### 编码地址格式

Encoded-Unicast Address 格式如下：

```
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Addr Family | Encoding Type | Unicast Address
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+...
```

- Addr Family  （1 字节）
- Encoding Type  （1 字节）
- Unicast Address  （IPv4 为 4 字节）

Encoded-Group Address 格式如下：

```
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Addr Family | Encoding Type |B| Reserved |Z|    Mask Len      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Group multicast Address
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+...
```

- Addr Family  （1 字节）
- Encoding Type  （1 字节）
- [B]idirectional PIM  
- Reserved 
- Admin Scope [Z]one  
- Mask Len  
- Group multicast Address    （IPv4 为 4 字节）

Encoded-Source Address 格式如下：

```
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Addr Family | Encoding Type | Rsrvd |S|W|R|     Mask Len      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Source Address
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-...
```

- Addr Family  （1 字节）
- Encoding Type  （1 字节）
- Encoding Type
- Reserved
  Transmitted as zero, ignored on receipt.
- S The Sparse bit is a 1-bit value, set to 1 for PIM-SM. It is used for PIM version 1
  compatibility.
- W The WC (or WildCard) bit is a 1-bit value for use with PIM Join/Prune messages (see
  Section 4.9.5.1).
- R The RPT (or Rendezvous Point Tree) bit is a 1-bit value for use with PIM Join/Prune
  messages (see Section 4.9.5.1). If the WC bit is 1, the RPT bit MUST be 1.
- Mask Len
  The mask length field is 8 bits. The value is the number of contiguous one bits left
  justified used as a mask which, combined with the Source Address, describes a source
  subnet. The mask length MUST be equal to the mask length in bits for the given
  Address Family and Encoding Type (32 for IPv4 native and 128 for IPv6 native). A
  router SHOULD ignore any messages received with any other mask length.
- Source Address
  The source address.  

### Hello 消息

Hello 消息采用 TLV 构建，其格式如下

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|PIM Ver|  Type |   Reserved    |            Checksum           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          OptionType           |           OptionLength        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                          OptionValue                          |
|                              ...                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                               .                               |
|                               .                               |
|                               .                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          OptionType           |           OptionLength        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                          OptionValue                          |
|                              ...                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

其中包括：

- Holdtime TLV
  - Type=1
  - Length=2
  - Holdtime=全 0 表示立即删除邻居；全 1 表示永不超时；默认为 Hello 周期的 3 倍（105 秒）。

- DR Priority
  - Type=19
  - Length=4
  - DR Priority=4 字节整型

### Register 消息

TODO

S --> RP

### Register-Stop 消息

TODO

RP -> S

### Join/Prune  消息

加入剪枝消息发往上游组播源或者 RP。其中，加入消息用于构建 RPT 或者 SPT，剪枝消息用于删除路径。

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|PIM Ver|  Type |   Reserved    |            Checksum           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      Upstream Neighbor Address (Encoded-Unicast format)       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|    Reserved   |   Num groups  |            Holdtime           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Multicast Group Address 1 (Encoded-Group format)      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Number of Joined Sources    |  Number of Pruned Sources     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Joined Source Address 1 (Encoded-Source format)      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                               .                               |
|                               .                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Joined Source Address n (Encoded-Source format)      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Pruned Source Address 1 (Encoded-Source format)      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                               .                               |
|                               .                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Pruned Source Address n (Encoded-Source format)      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                               .                               |
|                               .                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Multicast Group Address m (Encoded-Group format)      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Number of Joined Sources    |  Number of Pruned Sources     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Joined Source Address 1 (Encoded-Source format)      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                               .                               |
|                               .                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Joined Source Address n (Encoded-Source format)      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Pruned Source Address 1 (Encoded-Source format)      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                               .                               |
|                               .                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Pruned Source Address n (Encoded-Source format)      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

- Unicast Upstream Neighbor Address：上游邻居单播地址



### Bootstrap 消息

```
0 1 2 3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|PIM Ver| Type |N| Reserved | Checksum |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Fragment Tag | Hash Mask Len | BSR Priority |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| BSR Address (Encoded-Unicast format) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Group Address 1 (Encoded-Group format) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| RP Count 1 | Frag RP Cnt 1 | Reserved |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| RP Address 1 (Encoded-Unicast format) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| RP1 Holdtime | RP1 Priority | Reserved |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| RP Address 2 (Encoded-Unicast format) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| RP2 Holdtime | RP2 Priority | Reserved |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| . |
| . |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| RP Address m (Encoded-Unicast format) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| RPm Holdtime | RPm Priority | Reserved |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Group Address 2 (Encoded-Group format) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| . |
| . |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Group Address n (Encoded-Group format) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| RP Count n | Frag RP Cnt n | Reserved |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| RP Address 1 (Encoded-Unicast format) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| RP1 Holdtime | RP1 Priority | Reserved |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| RP Address 2 (Encoded-Unicast format) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| RP2 Holdtime | RP2 Priority | Reserved |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| . |
| . |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| RP Address m (Encoded-Unicast format) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| RPm Holdtime | RPm Priority | Reserved |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Assert 消息

PIM 路由器在接收到邻居路由器发送的相同组播报文后，会以组播的方式向本网段的所有 PIM 路由器发送 Assert 报文，其中目的地址为永久组地址 224.0.0.13。

```
0 1 2 3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|PIM Ver| Type | Reserved | Checksum |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Group Address (Encoded-Group format) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Source Address (Encoded-Unicast format) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|R| Metric Preference |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Metric |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```



### C-RP-Adv 消息

C−RPs 周期性向 BSR 发送单播 Candidate-RP-Advertisement 消息。

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|PIM Ver|  Type |   Reserved    |             Checksum          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Prefix Count |   Priority    |             Holdtime          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|              RP Address (Encoded-Unicast format)              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|             Group Address 1 (Encoded-Group format)            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                               .                               |
|                               .                               |
|                               .                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|             Group Address n (Encoded-Group format)            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

其中:
- Prefix Count 表示消息中该 C-RP 通告的组地址数量，不能为 0。
- RP Address 表示该 C-RP 单播地址。
- Holdtime 表示该通告有效期，一般设为 2.5 倍 C-RP-ADV 消息周期。


## 参考
- RFC 7761 4601
- RFC 5059
