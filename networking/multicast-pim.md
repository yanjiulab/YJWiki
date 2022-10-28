# PIM

## PIM 简介
PIM（Protocol Independent Multicast）称为协议无关组播。这里的**协议无关指的是与单播路由协议无关**，即 PIM 不需要维护专门的单播路由信息。与单播路由通过多种路由协议算法来动态生成路由表项不同， PIM 协议只专注于组成员和组播源状态相关的信息，而选取路径的信息直接从单播路由表获取，这降低了 PIM 协议的复杂性，使其成为应用最广泛的域内组播协议。

在单播路由与转发中，单播报文沿着一条单点到单点的路径传输，路由器只需要考虑报文“需要到达的位置”，即目的地址，就知道从哪个接口转发出去。组播路由与转发则不同。由于组播报文的目的地址为组播地址，只是标识了一组接收者，无法通过目的地址来找到接收者的位置，但是组播报文的“来源位置”，即源地址是确定的。所以组播报文的转发主要是根据其源地址来保证转发路径正确性。

路由器收到一份组播报文后，会根据报文的源地址通过单播路由表查找到达“报文源”的路由，查看到“报文源”的路由表项的出接口是否与收到组播报文的入接口一致。如果一致，则认为该组播报文从正确的接口到达，从而保证了整个转发路径的正确性和唯一性。这个过程就被称为 RPF 检查。这里“正确的接口”通常被称为 RPF 接口，即 RPF 检查通过的接口。

## PIM 协议模式

经过多年发展，PIM 协议目前具有两种模式：
- 协议无关组播密集模式 PIM-DM（PIM-Dense Mode）
- 协议无关组播稀疏模式 PIM-SM（PIM-Sparse Mode）

其中，PIM-SM 按照组播模型不同，又可分为：
- PIM-SM (ASM)：任意源组播，简称 PIM-SM
- PIM-SM (SSM)：特定源组播，简称 PIM-SSM

SSM 模型与 ASM 模型之间的最大差异就是**是否指定了组播源**，PIM 协议模型如下图所示。

|      协议      | 模型分类 |                           适用场景                           |                           工作机制                           |
| :------------: | :------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|     PIM-DM     |   ASM    |        适合规模较小、组播组成员相对比较密集的局域网。        | 通过周期性“扩散-剪枝”维护一棵连接组播源和组成员的单向无环 SPT。 |
| PIM-SM （ASM） |   ASM    |     适合网络中的组成员相对比较稀疏，分布广泛的大型网络。     | 采用接收者主动加入的方式建立组播分发树，需要维护 RP、构建 RPT、注册组播源。 |
| PIM-SM （SSM） |   SSM    | 适合网络中的用户预先知道组播源的位置，直接向指定的组播源请求组播数据的场景。 | 直接在组播源与组成员之间建立 SPT，无需维护 RP、构建 RPT、注册组播源。 |

## PIM 基本概念与术语

TODO
上游下游

## PIM 协议消息格式

PIM 协议消息承载于 IP 协议，协议号为 103。PIM 消息包括两部分：
- PIM 通用头 (PIM Header)
- PIM 消息内容 (PIM Data)

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


不同类型的 PIM 消息具有结构各异的消息内容，除此之外，PIM 消息类型也会影响 IP 头中的目的地址。因此，根据目的 IP 是单播地址还是组播地址，PIM 消息被分为单播消息和组播消息两种。其中，组播消息目的地址为 ALL-PIM-ROUTERS 组（224.0.0.13/IPv4，ff02::d/IPv6），TTL 为 1。

### 编码地址格式
PIM 消息内容中使用了大量的编码的地址格式，为了便于描述消息格式，首先介绍编码地址格式，该地址包括三种：
- 编码单播地址（Encoded-Unicast Address）
- 编码组播地址（Encoded-Group Address）
- 编码组播源地址（Encoded-Source Address）

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
- Group multicast Address（IPv4 为 4 字节）

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

### Join/Prune 消息

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

### Graft 消息
TODO

### Graft-Ack 消息
TODO

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




## PIM DM

PIM DM 协议由 RFC 3973 描述，是一种状态较为简单的协议，一般应用于**组播组成员规模相对较小**、**相对密集**的网络。DM 协议假定网络中的组成员分布非常稠密，每个网段都可能存在组成员。

当有活跃的组播源出现时，DM 致力于将组播源发来的组播报文**扩散（Flooding）**到整个网络的 PIM 路由器上，从而形成一棵以某组播源为根，以众多接收者为叶子的组播转发树。然而这颗组播转发树太过庞大，对于一个 PIM 路由器，如果某接口下游已经没有接收者，实际上已经无需再向该接口继续扩散，因此组播路由器会进行**剪枝（Prune）**操作，这样可以降低无效的网络流量。倘若被裁剪掉的分支由于下游路由器上有新的组成员加入，而希望重新恢复转发状态时，则进行**嫁接（Graft）**机制主动恢复其对组播报文的转发。

综上所述，PIM-DM 通过周期性的进行“扩散、剪枝、嫁接”，来构建并维护了若干棵**连接组播源和组成员的单向无环源最短路径树（Source Specific Shortest Path Tree, SPT）**，这些树以组播转发表的形式保存，每棵树对应了组播转发表的其中一个表项。

除此之外，PIM-DM 的关键工作机制包括邻居发现、扩散、剪枝、嫁接、断言和状态刷新。其中，扩散、剪枝、嫁接是构建SPT的主要方法。


(RFC 3973)
### Upstream

The Upstream(S,G) state machine for sending Prune, Graft, and Join
messages is given below. There are three states.
- Forwarding (F) This is the starting state of the Upsteam(S,G) state machine. The state machine is in this state if it just started or if oiflist(S,G) != NULL.
- Pruned (P) The set, olist(S,G), is empty. The router will not forward data from S addressed to group G.
- AckPending (AP)

three state-machine-specific timers:
- GraftRetry Timer (GRT(S,G)) ：如果上游没有回复 GA，则 GRT 超时，重发 G 报文，GRT 复位。若收到 GA，则取消 GRT。
- Override Timer (OT(S,G))：收到来自上游的剪枝报文，如果下游出口不空，则需要启动 OT，OT超时时发送 Join 报文以恢复上游对自己的转发。
- Prune Limit Timer (PLT(S,G))：如果上游已经时 P 状态，则 PLT 超时之前，为了限制 LAN 中的 P 报文数量，将不允许发送 P 报文。

### Downstream

The Prune(S,G) Downstream state machine for receiving Prune, Join and Graft messages on interface I is given below
- NoInfo(NI)
- PrunePending(PP)
- Pruned(P)

two timers:
- PrunePending Timer (PPT(S,G,I))：超时后真正剪枝，进入 P 状态，同时启动 PT
- Prune Timer (PT(S,G,I))：PT 超时后重新恢复转发，进入 NI 状态。可以使用 SR 报文一直刷新 PT，让下游一直不能恢复转发。（TODO思考why）
