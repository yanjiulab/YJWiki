# IP

## 命令基本格式

常用的选项如下：

|     选项      |                解释                |
| :-----------: | :--------------------------------: |
| -n[etns] name | 在命名空间 name 中执行后续 ip 命令 |
|               |                                    |
|               |                                    |

常用的子命令如下：

|   子命令   | 解释 |
| :--------: | :--: |
|  ip link   |      |
| ip address |      |
|  ip netns  |      |
|            |      |



### ip link 子命令

ip link 命令用来配置网络设备，常用命令基本格式如下：

```
ip link add ...
ip link delete ...
ip link set ...
ip link show ...
ip link help ...
```

## bridge - 网桥

bridge 设备即网桥（交换机），是 Linux 内核使用纯软件实现的虚拟交换机，有着和物理交换机相同的功能，例如二层交换，MAC 地址学习等。因此，bridge 更确切的叫法应该是 Linux 内核虚拟交换机。需要注意的是，Linux 平台上还有其他用户层虚拟交换机软件，例如 Open vSwitch 等，以下使用网桥指代 bridge 设备。

使用 `ip` 命令即可操作网桥，另一种方式是通过 `brctl` 命令，但需要额外安装 `bridge-utils` ，本文使用 `ip` 命令完成对网桥的所有操作。

首先创建一个网桥 br0。

```
ip link add br0 type bridge
```

然后创建两个命名空间，并创建两个 veth 设备。

```
# create network namespace
ip netns add ns1
ip netns add ns2

# create two veth pairs and move interfaces to network namespace
ip link add veth-ns1-br type veth peer name veth-ns1
ip link add veth-ns2-br type veth peer name veth-ns2
ip link set veth-ns1 netns ns1
ip link set veth-ns2 netns ns2

# set all interfaces up 
ip link set veth-ns1-br up
ip link set veth-ns2-br up
ip -n ns1 link set veth-ns1 up
ip -n ns2 link set veth-ns2 up

# assign IP to interfaces
ip -n ns1 address add 10.0.0.1/24 dev veth-ns1
ip -n ns2 address add 10.0.0.2/24 dev veth-ns2
```

将接口添加到网桥之前，必须保证其状态为 up，通过设置接口的 master 属性即可将其添加到网桥。

````
ip link set veth-ns1-br master br0
ip link set veth-ns2-br master br0
````

因此，通过网桥两个容器可以互相通信。

```
+------------------+     +------------------+
|       ns1        |     |       ns2        |
|                  |     |                  |
|    10.0.0.1/24   |     |    10.0.0.2/24   |
+---+(veth-ns1)+---+     +---+(veth-ns2)+---+
         +                          +        
         |                          |        
         +                          +        
+-+(veth-ns1-br)+-----------+(veth-ns2-br)+-+
|               Linux bridge                |
+-------------------------------------------+            
```

通过设置 nomaster 将接口从网桥移除。

```
ip link set veth-ns1-br nomaster
ip link set veth-ns2-br nomaster
```

删除网桥 br0 命令为。

```
ip link delete br0 type bridge
```

需要注意的是，在网桥创建成功后，Linux 会自动在默认命名空间创建一个与网桥同名的接口，通过 `ip link` 命令即可查看到。这也是令初学者迷惑的一点，实际上，这仅仅是创建的同名接口，而不是网桥本身。

```
5: br0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 1a:9c:fb:2d:be:21 brd ff:ff:ff:ff:ff:ff
```

网桥作为一个二层设备不需要配置 IP，但是网桥通过默认命名空间的同名接口，自动将本机协议栈挂在网桥上。这样网桥上挂载的命名空间（容器）就可以同主机进行通信，进而通过内核路由访问到外部网络。

```
route: default gw 10.0.0.3/24
+------------------+     +------------------+
|       ns1        |     |       ns2        |
|                  |     |                  |
|    10.0.0.1/24   |     |    10.0.0.2/24   |
+---+(veth-ns1)+---+     +---+(veth-ns2)+---+
         +                          +        
         |                          |        
         +                          +        
+-+(veth-ns1-br)+-----------+(veth-ns2-br)+-+
|               Linux bridge                |
+-----------------(br0)---------------------+
                    |                        
+-----------------(br0)---------------------+
|              10.0.0.3/24                  |
|        default network namespace          |
|       (Linux Kernel IP Forwarding)        |
|              10.0.1.1/24                  |
+---------------(enp0s3)--------------------+
```



## veth - 虚拟以太网对

veth 设备总是成对出现的，两个设备一端连接内核协议栈，另一端两个设备彼此相连。一个设备收到协议栈的数据发送请求后，会将数据发送到另一个设备上去。

```
+----------------------------------------------------------------+
|                                                                |
|       +------------------------------------------------+       |
|       |             Newwork Protocol Stack             |       |
|       +------------------------------------------------+       |
|              ↑               ↑               ↑                 |
|..............|...............|...............|.................|
|              ↓               ↓               ↓                 |
|        +----------+    +-----------+   +-----------+           |
|        |   eth0   |    |   veth0   |   |   veth1   |           |
|        +----------+    +-----------+   +-----------+           |
|192.168.1.11  ↑               ↑               ↑                 |
|              |               +---------------+                 |
|              |         192.168.2.11     192.168.2.1            |
+--------------|-------------------------------------------------+
               ↓
         Physical Network
```

veth 设备单独使用并没有任何用处，因为两个设备挂在同一个协议栈上。

veth 设备常用的功能是用来连接两个网络命名空间，这样两个设备挂在两个协议栈之下，使得两个网络命名空间中的设备可以互相通信。其流程为：

1. 创建 veth 设备对。
2. 将其中一个设备移动到另一个网络命名空间内。
3. 在网络命名空间中启动设备。

```
ip link add <p1-name> type veth peer name <p2-name>
ip link set <p2-name> netns <p2-namespace>
ip link set <p1-name> up
ip -n[etns] <p2-namespace> link set <p2-name> up
```

这样内核协议栈便可以和网络命名空间（容器）内协议栈连接，后续可以根据需求配置 IP 地址进行通信。

以上只能连接两个网络命名空间，如果需要多个网络命名空间相连，可以通过 veth 设备将各个命名空间与网桥相连，使得多个网络命名空间（容器）可以进行通信。

```
ip link add <p1-name> type veth peer name <p2-name>
...
```



