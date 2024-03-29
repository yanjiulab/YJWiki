# 局域网和以太网

局域网 (Local Area Networks, LANs) 是当代所有计算机网络的重要组成部分。如果观察某个广域网 (WAN) 的结构，例如 Internet 或者一个大规模企业网，你会发现，**几乎所有的网络信息资源都集中在局域网 (LAN) 中，广域网只是连接众多 LAN 的传输器。**

## 局域网简介

### LAN 的目的

目前，组建 LAN 的目的大概有三种 (互相不冲突)：

1. 连接计算机，提供局域网内计算机间的数据交换。如：某个企业组成的内网，通过内网公司内的计算机可以进行互相访问。
2. 连接广域网，提供局域网内计算机和 Internet 的连接。组建因特网访问是为了整个 LAN 而不是某个用户。
3. 连接电信网。例如，电话和传输网。

LAN 技术经历了相当长的发展，从共享 LAN 到交换 LAN，技术层出不穷。 如今，LAN 有着小型化的趋势，一种新的网络个域网 (Persona Area Network, PAN) 已经出现，主要用来连接几百米内的个人用户电子设备。

现代 LAN 几乎被一个完整的网络技术系列所统治：**以太网 (Ethernet)**。除了大名鼎鼎的以太网，LAN 还包括**令牌环**、**光纤分布式数据接口 (FDDI)** 和 100VG-AnyLAN (目前已淘汰)。

### LAN 的产生 - 共享介质

在20 世纪 70 年代末，早期 LAN 研究人员的目标是找到一种**简单而又廉价**的方法，连接一个较小区域（比如一栋大楼）内的数百台计算机，使它们成为一个计算机网络。在初期，并不考虑将 LAN 连接到广域网的问题。

而如今，**LAN 最重要的目的之一是连接计算机**，这些计算机在一栋楼中（或彼此很近），通过本地服务器，提供网络用户信息访问功能。同时，**LAN 也提供一种简便的方法将计算机分组连接到广域网 (如 Internet)** ，例如，火车站或家庭 LAN，这种 LAN 的主要目的并不是为了本地用户间彼此进行数据交换，而是使得本地用户可以访问因特网而已。

为了简单化，早期 LAN 的研究人员决定使用**共享数据传输介质 (shared data transmission media)** 。所谓共享介质可以是**无线电信道**，也可以是**同轴电缆**。

20 世纪 70 年代初，夏威夷大学首次使用 ALOHA 无线电网络测试这种技术。所有发送端共用某个频带进行数据传输，这个特殊频带的无线电信道就是一个共享介质。

不久以后，这种思想被用于**有线 LAN**。一个连续段的同轴电缆就如同一个共用的无线介质，所有计算机都连接到这个段，当有一个传送器发送信号时，所有接收器都接受到信号，就好像无线电波一样。例如，一个同轴以太网的星型拓扑大致如下图所示。

![shared-media-star](lan.assets/shared-media-star.png)

在令牌环和 FDDI 中，共享介质同以太网不同，这些网络基于**物理环路的拓扑结构**，每个节点通过电缆与另外两个节点相连，由于任何时候只有一台计算机可以使用环路传送数据，因此，这些电缆是共享的。

![shared-media-ring](lan.assets/shared-media-ring.png)

使用共享介质，优点是**简化了网络节点的操作逻辑**。因为某个时间只能有一次数据传输，就没有缓存、转接节点、流量控制和拥塞控制了。

共享介质的主要缺点是**可延拓性差 (poor scalability)** 。共享介质的利用率超过一定阈值，访问介质的队列开始非线性增加，网络实际上变得不可用。ALOHA 很低，大概是 18%，以太网大约为 30%，令牌环和 FDDI 约为 60%~70%。

目前仍然使用广泛的共享介质局域网有：

- 无线局域网 IEEE 802.11
- 蓝牙个域网
- 使用集线器连接的以太网

### LAN 的发展 - 共享和交换

实际上，20 世纪 80 年代的所有技术都是在物理层使用**共享介质** (shared media) 方法连接计算机。20 世纪 90 年代，LAN 开始引入交换技术。交换 LAN 和共享 LAN 使用的协议是一样的，只是采用**全双工**的工作方式。尽管交换 LAN 十分流行，但共享技术仍然经常用于新旧技术中，**因此，共享和交换并不是替代关系，两种技术是共存的。**

目前，**LAN 交换机**已经十分流行，以至于非网络人员基本也听过交换机的大名。但交换机本质上并没有改变 LAN 共享介质的性质，而是通过将 LAN 划分为不同的**微网段** (microsegment)，其中虽然微网段仍然是共享介质的，但每一个主机都会直接接入交换机的一个端口，因此个人、家庭使用的以太网局域网已经几乎没有共享介质。

## 局域网协议栈

LAN 技术仅仅执行 OSI 模型的最低两层功能，即**物理层**和**数据链路层**功能。

但 LAN 中的节点仍然支持数据链路层之上的协议，这些协议安装在网络节点中并通过它们执行。其实，网络节点的功能与特定 LAN 技术没有关联。网络和传输协议对于 LAN 节点是必须的，因为 LAN 节点要和其他 LAN 节点通信，其路径可能包括 WAN 链路，因此需要有网络层的协议转换，当然，如果能保证通信仅限于单个 LAN，那么应用层可以直接操作数据链路层。但这种受限的通信能力无法满足实际需求，因此，每个连接到 LAN 的计算机都支持整个协议栈。

因此，一种网络协议通过逻辑链路控制层 (LLC) 执行，LAN 中的数据链路层也分为两个子层：

- 逻辑链路控制层 (LLC)：通过**操作系统中的软件模块**执行。
- 介质访问控制层 (MAC)：通过**硬件 (网络适配器)** 和**软件 (网络适配器驱动程序)** 执行。

### MAC 层

主要功能：

- **保证访问共享介质**
- 使用物理层设备的功能在**端节点间传送帧**

共享介质的访问方法有：

- 随机访问 (Random access)，基于分散式 (decentralized)
- 确定访问 (Deterministic access)
  - 令牌传递 (Token passing)，基于分散式 (decentralized)
  - 轮询 (Polling)，通常基于集中式 (centralized)，也可以基于分散式 (decentralized)

帧的传送由 MAC 层执行，与所选访问方式无关。

- 帧格式化 (Frame formatting)。这个阶段，帧字段填满从高层获得的信息，包括源地址和目的地址、用户数据和高层协议代码，创建完成后，计算校验和并放入对应字段。
- 帧传输到介质 (Frame transmission into the medium)。帧创建后，当节点访问共享介质时，MAC 层把帧传送到物理层 。
- 帧接收 (Frame reception)。

### LLC 层

主要功能：

- 建立与它相邻的网络层的接口
- 按预定的可靠性级别确保帧传输

LLC 的接口功能 (interface function) 包括在 MAC 层和网络层之间传送用户和控制数据。

LLC 的第二个功能：**确保可靠的帧传输 (ensuring reliable frame delivery)** 。LLC 协议支持多种操作模式，提供不同的运输服务质量，LLC 向高层提供三种类型的运输服务：

1. LLC1 - 无需发送确认的无连接服务。与 MAC 相似，因此整个 LAN 技术使用**数据报模式**操作，出错后恢复由高层协议执行。**在 TCP/IP 协议栈中，确保可靠数据传送的任务由 TCP 执行，LLC 总工作在 LLC1模式下。**
2. LLC2 - 具有出错和丢失帧恢复功能的面向连接的服务。传输前建立逻辑连接，LLC2 使用滑动窗口算法实现。
3. LLC3 - 带发送确认的无连接服务。LLC1 和 LLC2 的折中，**无需确认连接但要确认接收**。

### IEEE 802.x 标准

IEEE 802委员会负责 **LAN 技术的标准化**，其成果为 IEEE 802.x 标准体系。每个工作组专注于一个领域，并分配一个代号，如 802.x，其中 x 为数字；其下协议命名为 802.xy 协议，y 为英文字母。

![ieee-802-x](lan.assets/ieee-802-x.png)

## 以太网基础

**以太网 (Ethernet) 是当今最常用的 LAN 标准**，同时也是第一个建议使用共享介质进行网络访问的技术。以太网这一术语一开始作为一种传输速率为 **10Mb/s 的数据传输网络标准**而成为 DEC、Intel 和 美国施乐公司的**专用标准**，后来被 IEEE 802.3 工作组标准化，从此成为**国际标准**。随着**传统以太网 (10Mb/s)** 的普及，后续出现了**快速以太网 (100Mb/s)、千兆以太网 (1000Mb/s)、10G以太网 (10000Mb/s)** 。所以，以太网这一术语代表着多重含义。

介质访问控制 (MAC) 作为介质共享算法是任何 LAN 技术中最重要的特性，**以太网使用随机访问方法作为介质共享机制**。

### 以太网类型

随着发展，以太网形成了多种类型，各类以太网的差别主要在**通信速率**和**物理介质规范 (通信媒介，或者说线材)** 。其中，速度从 10 Mbit/s 到 100 Gbit/s，甚至如今 (2018年) 期待的 400 Gbit/s，物理媒介有**同轴电缆、双绞线、光纤**等。**因此，同样的网络协议栈软件可以在大多数以太网上运行。**依据速度，大致可划分为：

- 早期的以太网：以太网的雏形，在公司内部使用，速率为 1Mbps，如今大部分规格已经过时。
- 10Mbps 以太网 (传统以太网)：IEEE 标准化的以太网。
- 100Mbps 以太网 (快速以太网)：IEEE 在 1995 年发表的网络标准，能提供达 100Mbps 的传输速度
- 1Gbps 以太网 (千兆以太网)
- 10Gbps 以太网
- 100Gbps 以太网

尽管类型不同，但从 100BASE-TX 以后，以太网引入了**自动协商** (autonegotiation) 技术，两个通信设备之间可以协商共同的传输参数，例如包括速度和双工模式等，这保证了不断向前发展的协议和标准可以后向兼容 (backward compatible)，提升了网络的健壮性。

使用最多的规范分别是 **10BASE-T**，**100BASE-TX**，和 **1000BASE-T**，均使用**双绞线 (twisted pair cables)** 和 **RJ45 水晶头接口 (8P8C modular connectors, or RJ45)** ，运行速度分别为 10 Mbit/s，100 Mbit/s，和 1 Gbit/s。

光纤以太网 (Fiber optic variants of Ethernet) 在大型网络中也十分常见，旨在提供**更高性能，更好电气性能隔离，长距离通信**的网络。

同时，千兆以太网速度之上的网络，如，10G 以太网，通常与更低速的网络有较大的不同，需要特别关注。对于阅读本文的以太网初学者，不需要过多关注以太网物理层特性 。

### 以太网帧结构

IEEE 802.3 定义的以太网标准提供了 MAC 层帧格式，又因为在 IEEE 802.2 标准中，**MAC 帧必须包含 LLC 层帧**，因此，按照 IEEE 标准，以太网只能使用**一种数据链路层帧**，帧头是 MAC 子层和 LLC 子层帧头的组合。

然而，实际上以太网使用四种帧格式。下列是一些最流行的，IEEE 802.3 委员会的成果：

- **以太网 DIX / 以太网 II (Ethernet II frame, or Ethernet Version 2, or DIX frame)**
- 原始 802.3 (Novell raw IEEE 802.3)
- IEEE 802.3 以太网 (802.3/802.2, or IEEE 802.2 Logical Link Control (LLC) frame)
- 以太网 SNAP (IEEE 802.2 Subnetwork Access Protocol (SNAP) frame)

帧的差异导致不兼容，然而，今天，所有的网络适配器和他们的驱动器、网桥、交换机或路由器都能执行所有用到的以太网帧格式，必要的识别是自动执行的。

![ethernet-frame](lan.assets/ethernet-frame.png)

现在使用最广的是第一种帧头格式，共计 14 字节，包括：

- 目的 MAC 6 字节
- 源 MAC 6 字节
- 类型 2 字节

其中 MAC 地址表示形如 `0c:06:01:03:fb:34`。

### 共享式以太网

早期的以太网（1/10Mbps）使用**同轴电缆**进行传输，所有的通信信号都在**共享介质** (shared media)上传输，即使信息只是想发给其中的一个终端，也需要使用广播的形式发送给线路上的所有电脑，虽然在正常情况下，网络接口卡会滤掉不是发送给自己的信息，但是这带来了以下的缺点：

- 所有的通信共享带宽，**半双工通信**方式，当发送方发送信息时，不仅其他终端不可发送，连真正的接收端也不能发送数据，网络速度慢。
- 共享介质通信需要**介质访问控制协议**来进行协调，决定什么时候由谁进行通信。
- 所有终端都可以接收到信息，**安全性较差**。

如果说速度和安全性是相对可以接受的缺点，那么接入协议就是不可避免的。以太网使用 **CSMA/CD (Carrier-sense multiple access with collision detection)** 协议作为介质访问控制协议。该协议的思路大致是不断对链路进行冲突检测，如果线路空闲，则启动传输；如果线路繁忙，持续等待直到线路空闲。就像在没有主持人的座谈会中，所有的参加者都通过一个共同的介质（空气）来相互交谈。每个参加者在讲话前，都礼貌地等待别人把话讲完。如果两个客人同时开始讲话，那么他们都停下来，分别随机等待一段时间再开始讲话。这时，如果两个参加者等待的时间不同，冲突就不会出现。如果传输失败超过一次，将延迟指数增长后再次尝试。

在共享式以太网中，中继器和集线器 (repeaters and hubs) 可以进行物理拓扑的延伸，其区别是：

- 中继器进行物理信号的放大，用来解决同轴电缆最大传输距离限制问题。
- 集线器淘汰了同轴电缆，可以方便的将多个网段点对点地连起来，使得网络更加可靠，接线更加方便。

?> 目前共享式以太网已经很少见。

### 交换式以太网

为了解决共享式以太网的缺点，交换式以太网逐步发展。共享式以太网的标准拓扑结构为**总线型拓扑**，但当前的高速以太网 (100BASE-T、1000BASE-T标准) 为了减少冲突，将能提高的网络速度和使用效率最大化，使用交换机 (Switch) 来进行网络连接和组织。如此一来，以太网的拓扑结构就成了**星型**。

![image-20221130232144528](lan.assets/image-20221130232144528.png)

交换式以太网的好处是：

- 物理层采用双绞线 (twisted pair cables) 进行**全双工通信**，包括 10BASE-T，100BASE-TX，和 1000BASE-T 规格，运行速度分别为 10 Mbit/s，100 Mbit/s，和 1 Gbit/s，不再是共享介质通信，因此实际上也不需要 CSMA/CD 协议，但协议仍然保留了该算法。
- 交换机采用**端口学习机制**转发数据帧，而不是简单的广播。

这种交换机称之为“**傻瓜交换机**”，交换机通电后会自动建立一个端口地址表，也叫 MAC 地址表，它会记录一个设备 MAC 地址机和交换机端口的映射关系。当收到报文后，交换机在 MAC 地址表中查找数据帧中的目的 MAC 地址，如果找到就将该帧转发到该端口，如果找不到，就从其他所有端口（除了该数据入端口）广播。在数据转发时，交换机对数据帧进行自动的源 MAC 地址学习，将“数据帧源 MAC - 交换机接收该帧的端口” 加入 MAC 地址表。

?> 傻瓜交换机傻瓜的含义也代表了它能做的事情有限，但可以应付简单交换场景。

### 高级交换以太网

在交换式以太网中，端口学习机制几乎是傻瓜交换机唯一的算法。随着组网需求的复杂，交换机的功能日益复杂，其不仅可以处理二层帧，还会处理三层报文，从而完成更复杂的功能。因此，业界一般称处理二层帧的交换机称为“**二层交换机**”，能够处理三层报文的交换机称为“**三层交换机**”，由二/三层交换机组成的复杂网络可能是**树型**的，本文称之为高级交换以太网。我们在下文中将会详细介绍相关的高级特性。

?> 目前大部分商用交换机（例如华为、思科交换机）都具备处理复杂二/三层报文的能力，因此可以说如今大部分以太网是高级交换网络。

## 以太网高级特性

### 广播风暴问题

以太交换机对广播包的处理，是不管从哪个端口收到广播包，都完整地复制一份**转发**到其他端口（除接收到的端口外），此时如果网络中具有环路，则广播报文在环路中不断复制并转发，数据量指数上升，最终导致交换机瘫痪，该问题称为“**广播风暴**”。

解决广播风暴有多种办法，例如：

- 合理规划，避免成环。但单节点损坏会导致网络部分瘫痪，适用于断网几天都没多大损失的场景，可以慢慢修复。
- 使用链路聚合协议。有些场景对于可靠性要求很高，需要将多个冗余链路聚合到一起形成一条链路，从而规避掉环路问题。
- 使用虚拟局域网将网络分隔成多个小网络。通过将网络规模减小，从而降低网络风暴产生的影响。
- 使用 STP 协议打破环路。STP 是一种较为通用的技术，但 STP 浪费链路，且收敛时间长。
- 使用三层技术构建网络。从根本上解决该问题，但对于设备要求比较高。

可以说，广播风暴是网络设计中遇到的第一个问题，有多种方式可以解决它，但需要结合具体情况分析。

### STP 生成树协议

TODO

### 802.1Q VLAN 协议

TODO

### 链路聚合

TODO

## WLAN

**Wi-Fi**又称“无线热点”或“无线网络”，是一种基于 **IEEE 802.11** 标准的无线局域网技术实现。

## 蓝牙网络

## 其他局域网技术

### 令牌环

TODO

### FDDI

TODO
