# FRRouting

## Quagga 简介

[Quagga](https://www.nongnu.org/quagga/) 是一个 Unix 系统路由软件，提供了许多路由协议的实现，是 FRRouting 的前身，目前已经停止更新，其最新版本停留在 1.2.3，大部分相关开发人员转入 FRRouting 项目，不过 Quagga 仍然可以在 [Github](https://github.com/Quagga/quagga) 上进行下载并使用。

Quagga 支持的路由协议包括：

- 单播路由：BGP4, BGP4+, OSPFv2, OSPFv3, RIPv1, RIPv2, and RIPng as well as very early support for IS-IS.

- 组播路由：PIM-SSM

### Quagga 架构

quagga 架构包括内核、zebra 守护进程、路由模块守护进程三部分。其中 zebra 模块与内核进行交互、维护路由表等，同时提供 `zserv` API 供路由模块使用。

```
+----+  +----+  +-----+  +-----+
|bgpd|  |ripd|  |ospfd|  |zebra|
+----+  +----+  +-----+  +-----+
                            |
+---------------------------|--+
|                           v  |
|  UNIX Kernel  routing table  |
|                              |
+------------------------------+
```

### Quagga 安装

相较于 FRRouting，Quagga 的安装方式较为简单。

```
cd quagga-master # 进入安装目录
./bootstrap   # 部署准备
./configure   # 相关环境配置
make clean   # (可选) 清理二进制文件
make    # 编译构建软件
make install  # 将编译好的文件复制到安装目录
```

在上述步骤中，configure 时可以进行参数设置，更改软件的默认配置。其中，主要的选项包括：

| 目的                     | 参数                     | 解释                                                         |
| ------------------------ | ------------------------ | ------------------------------------------------------------ |
| 关闭某特性或不构建某模块 | `--disable-xxx`          | 其中 xxx 为 ipv6 或 ripd 等。需要使用 disable 指定的行为，默认行为为开启。 |
| 构建某模块               | `--enable-xxx`           | 其中 xxx 为 pimd 等。需要使用 enable 指定的行为，默认行为为关闭。 |
| 指定安装目录             | `--prefix=prefix`        | 默认为 `/usr/local/`                                         |
| 指定配置文件目录         | `--sysconfdir=dir`       | 默认为 `$prefix/etc/`                                        |
| 指定状态文件目录         | `--localstatedir=dir`    | 默认为 `/var/run/`                                           |
| 更改用户为 root          | `--enable-user=root`     | 默认为 quagga                                                |
| 更改组为 root            | `--enable-group=root`    | 默认为 quagga                                                |
| 指定交叉编译平台         | `--host=arm-linux`       | 默认为 linux-gnu                                             |
| 指定交叉编译器           | `CC=aarch-linux-gnu-gcc` | 默认为 gcc                                                   |

### Quagga 交互

用户可以通过 VTY 接口同 Quagga 守护进程交互，在 `/etc/services` 添加如下进行使用。

```
zebrasrv      2600/tcp    # zebra service
zebra         2601/tcp    # zebra vty
ripd          2602/tcp    # RIPd vty
ripngd        2603/tcp    # RIPngd vty
ospfd         2604/tcp    # OSPFd vty
bgpd          2605/tcp    # BGPd vty
ospf6d        2606/tcp    # OSPF6d vty
ospfapi       2607/tcp    # ospfapi
isisd         2608/tcp    # ISISd vty
pimd          2611/tcp    # PIMd vty
nhrpd         2612/tcp    # nhrpd vty
```

## FRR 简介

FRRouting（以下简称 FRR）目前仍然在不断更新中，从使用者角度而言，Quagga 与 FRR 使用基本差别不大，特别是两者都支持的协议，其配置使用基本一致。因此，下文中关于 FRR 的配置介绍，绝大部分都适用于 Quagga，关于更多信息详见[官网](http://docs.frrouting.org/en/latest/index.html)。

## FRR 安装

以 CentOS 8 系统为例，其余操作系统请参考官方文档。总体而言与 Quagga 类似，但依赖安装更为繁琐一些。

### 安装依赖

```shell
sudo dnf install --enablerepo=PowerTools git autoconf pcre-devel automake libtool make readline-devel texinfo net-snmp-devel pkgconfig groff pkgconfig json-c-devel pam-devel bison flex python2-pytest c-ares-devel python2-devel libcap-devel elfutils-libelf-devel libunwind-devel
```

> 如果提示没有 Powertools 库，需要先安装 dnf-plugins-core 并启用 PowerTools 库。

```shell
sudo dnf install dnf-plugins-core
sudo dnf config-manager --set-enabled powertools
```

查看是否启用 PowerTools 库。

```shell
$ dnf repolist
repo id                                                  repo name
appstream                                                CentOS Linux 8 - AppStream
baseos                                                   CentOS Linux 8 - BaseOS
extras                                                   CentOS Linux 8 - Extras
powertools                                               CentOS Linux 8 - PowerTools
```

> 如果提示无法找到 libunwind ，可以跳过安装不影响 FRR 功能使用。

FRR 需要依赖 libyang 2.0 版本以上，libyang 源码安装如下。

```shell
sudo dnf install cmake pcre2-devel # libyang's dependencies
git clone https://github.com/CESNET/libyang.git
cd libyang
git checkout v2.0.0
mkdir build; cd build
cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr -D CMAKE_BUILD_TYPE:String="Release" ..
make
sudo make install
```

### 获取源码

通过 git 获取源码，并且进行初始化。

```shell
git clone https://github.com/frrouting/frr.git frr
cd frr
./bootstrap.sh
```

### 环境配置

首先，根据需求配置 FRR 成员和组。

```shell
sudo groupadd -g 92 frr
sudo groupadd -r -g 85 frrvty
sudo useradd -u 92 -g 92 -M -r -G frrvty -s /sbin/nologin -c "FRR FRRouting suite" -d /var/run/frr frr
```

其次，根据需求对 `./configure` 命令选择适当的参数。 这部分类似于 Quagga。

### 编译安装

配置完毕之后，可以进行编译、检查、安装过程。

```shell
make [-j] # 根据需求是否开启并行编译加速
make check
sudo make install
```

## FRR 配置

### 守护进程配置

安装守护进程配置文件到相关安装目录中。

```shell
sudo install -p -m 644 tools/etc/frr/daemons /etc/frr/
sudo chown frr:frr /etc/frr/daemons
```

编辑 `/etc/frr/daemons` 文件，根据需求选择启动相应的守护进程，yes 表示启动该进程，默认为 no 不启动。

### 服务配置

FRR 服务如下，在 `/etc/services` 添加如下进行使用。安装后会有默认设置，具体以该文件中的端口为准。

```
zebrasrv      2600/tcp                 # zebra service
zebra         2601/tcp                 # zebra vty
ripd          2602/tcp                 # RIPd vty
ripngd        2603/tcp                 # RIPngd vty
ospfd         2604/tcp                 # OSPFd vty
bgpd          2605/tcp                 # BGPd vty
ospf6d        2606/tcp                 # OSPF6d vty
ospfapi       2607/tcp                 # ospfapi
isisd         2608/tcp                 # ISISd vty
babeld        2609/tcp                 # BABELd vty
nhrpd         2610/tcp                 # nhrpd vty
pimd          2611/tcp                 # PIMd vty
ldpd          2612/tcp                 # LDPd vty
eigprd        2613/tcp                 # EIGRPd vty
bfdd          2617/tcp                 # bfdd vty
fabricd       2618/tcp                 # fabricd vty
vrrpd         2619/tcp                 # vrrpd vty
```

### systemd 配置

安装服务

```shell
sudo install -p -m 644 tools/frr.service /usr/lib/systemd/system/frr.service
```

注册服务

```shell
sudo systemctl preset frr.service
```

服务自启动

```shell
sudo systemctl enable frr
```

启动服务

```shell
sudo systemctl start frr
```

### 相关系统配置

- 开启 IP 转发

创建文件 `/etc/sysctl.d/90-routing-sysctl.conf`，填入以下内容：

```shell
# Sysctl for routing
#
# Routing: We need to forward packets
net.ipv4.conf.all.forwarding=1
net.ipv6.conf.all.forwarding=1
```

加载配置文件。

```shell
sudo sysctl -p /etc/sysctl.d/90-routing-sysctl.conf
```

### 其他配置

如果需要，有时候可以手动创建各种配置文件。

```shell
sudo mkdir /var/log/frr
sudo mkdir /etc/frr
sudo touch /etc/frr/zebra.conf
sudo touch /etc/frr/bgpd.conf
sudo touch /etc/frr/ospfd.conf
sudo touch /etc/frr/ospf6d.conf
sudo touch /etc/frr/isisd.conf
sudo touch /etc/frr/ripd.conf
sudo touch /etc/frr/ripngd.conf
sudo touch /etc/frr/pimd.conf
sudo touch /etc/frr/nhrpd.conf
sudo touch /etc/frr/eigrpd.conf
sudo touch /etc/frr/babeld.conf
sudo chown -R frr:frr /etc/frr/
sudo touch /etc/frr/vtysh.conf
sudo chown frr:frrvty /etc/frr/vtysh.conf
sudo chmod 640 /etc/frr/*.conf
```

## FRR 基本使用

FRR 提供了多种方式与用户进行交互。

### VTY 接口

VTY 表示 Virtual TeletYpe Interface (Virtual Terminal  Interface ) ，即虚拟终端接口，用于用户与守护进程进行交互。通过 **telnet** 协议，用户可以向**某个**特定守护进程发送命令。

!> 要使用 VTY 接口，必须设置 VTY 密码。

```
% telnet localhost 2601
Trying 127.0.0.1...
Connected to localhost.
...
Password: XXXXX
Router> ?
...
Router> enable
Password: XXXXX
Router# configure terminal
Router(config)# interface eth0
Router(config-if)# ip address 10.0.0.1/8
Router(config-if)# ^Z
Router#
```

其中：

- `>` 为只读模式，仅允许执行部分命令。
- `#` 为读写模式，通过 enable 进入。

### VTY Shell

`vtysh` 为**所有**守护进程提供了一个统一交互前端。**默认安装并启动**，通过 configure 参数中使用 `--disable-vtysh` 选项可以关闭该特性。

`vtysh` 通过 Unix 域套接字 `/var/run/frr` 与守护进程通信，因此需要确保用户对该目录具有操作权限。

有两种方式可以配置 FRR：

1. 独立式配置：每个守护进程有一个配置文件，名称为：`[daemon-name]d.conf`。
2. 集成式配置（推荐使用）：所有守护进程共同一个配置文件，名称为 `frr.conf` 。

若要使用集成式配置，需要在 `vtysh.conf` 中进行配置。

```shell
service integrated-vtysh-config  # vtysh 配置永远只写入 frr.conf
no service integrated-vtysh-config # vtysh 配置不会写入 frr.conf，而是写入独立配置文件。
Neither option present (default) # 默认行为。若 frr.conf 存在则写入；否则写入独立配置文件。
```

在终端中即可启动 vtysh。

```
root@msi-ryzen3600:/home/liyanjiu# vtysh

Hello, this is FRRouting (version 8.1).
Copyright 1996-2005 Kunihiro Ishiguro, et al.

msi-ryzen3600#
```

### 北向 gRPC

gRPC 通过 YANG 北向接口为**所有**守护进程提供了一个统一交互前端。由于处在实验阶段**默认不安装**，通过 configure 参数中使用 `--enable-grpc` 选项可以开启该特性。

配置 FRR 守护进程监听 gRPC 端口（默认 50051）需要在守护进程配置文件中配置 `-M grpc:PORT` 参数，例如：

```shell
bfdd_options=" --daemon -A 127.0.0.1 -M grpc"  # 使用默认端口
isisd_options=" --daemon -A 127.0.0.1 -M grpc:PORT" # 使用自定义端口
```

### 配置文件总结

在 Quagga 中，我们习惯于使用独立的配置文件，然而 FRR 提倡使用集成式配置文件。

| 文件                  | 含义                   | 说明                                                         |
| --------------------- | ---------------------- | ------------------------------------------------------------ |
| `/etc/frr/vtysh.conf` | 交互式 Shell 配置文件  | 不会随着 save 命令更新，需要管理员手动配置。                 |
| `/etc/frr/daemons`    | 守护进程初始化配置文件 | 默认 FRR 不会启动任何守护进程，需要将进程值改为 yes 才能启动。 |
| `/etc/frr/frr.conf`   | 守护进程集成式配置文件 | 所有进程在启动时首先检查是否存在该文件，**若存在则不会启动独立配置文件**。 |
| `/etc/frr/XXXd.conf`  | 守护进程独立式配置文件 | 例如 `zebra.conf`，`bgpd.conf`，**目前已经被集成式配置文件替代**。 |

目前，笔者的相关配置如下。

`/etc/frr/vtysh.conf` 内容如下：

```
service integrated-vtysh-config
```

`/etc/frr/frr.conf` 内容如下：

```
frr version 8.1
frr defaults traditional
password frr
hostname msi-ryzen3600
log syslog informational
service integrated-vtysh-config
```

`/etc/frr/daemon` 中：

> The watchfrr, zebra and staticd daemons are always started.

## FRR 基本命令

无论是 VTY Shell 还是 VTY 命令行接口，进入之后分为两种模式：

- 终端模式：主要用于查看状态或者进行通用设置。
  - 只读模式：使用 `>` 标识。
  - 读写模式：使用 `#` 标识，
- 配置模式：进行网络和路由功能配置，是核心部分，使用 `(config)#` 标识，括号中的内容表示当前配置层级。

### 终端模式命令

通过 VTY Shell 登录和通过 VTY 命令行接口登录，终端模式命令有所差别。通过 `?` 可以获取当前可键入命令列表。以下是常用的命令。

|         命令         |                         解释                         |
| :------------------: | :--------------------------------------------------: |
| configure [terminal] |                     进入配置模式                     |
|      quit/exit       |               退出当前模式并返回上一级               |
|    write terminal    |                     显示当前配置                     |
|      write file      |                保存当前配置到配置文件                |
|         list         | 列出所有命令详细列表，由于内容过于详细反而不太常用。 |
|         who          |              显示当前登录 vty 会话用户               |
|       **show**       |        **显示当前状态命令，包含众多子命令。**        |

### 配置模式命令

在读写模式下，通过 `configure [terminal]` 命令进入配置模式。以下是基本配置命令，详细的路由配置由各个路由协议功能模块分别提供。

|             命令             |               解释               |
| :--------------------------: | :------------------------------: |
|           hostname           |          设置路由器名字          |
|      password PASSWORD       |      设置 vty 接口登录密码       |
|   enable password PASSWORD   |    设置 vty 接口读写模式密码     |
|       log stdout LEVEL       |         设置标准输出日志         |
| log file [FILENAME [LEVEL]]  |           设置文件日志           |
|      log syslog [LEVEL]      |         设置 syslog 日志         |
| exec-timeout MINUTE [SECOND] | 设置退出超时时间（没有设置成功） |

### 守护进程参数

守护进程启动时可以传入参数，从而进行一些设置。具体查看 `--help`，一般情况下用不到。

## FRR 软件实现

### 系统架构

FRR 使用一系列守护进程共同构建路由表，每个进程实现一种协议，所有进程通过中间守护进程 `zebra` 与路由信息进行交互。

```
+----+  +----+  +-----+  +----+  +----+  +----+  +-----+
|bgpd|  |ripd|  |ospfd|  |ldpd|  |pbrd|  |pimd|  |.....|
+----+  +----+  +-----+  +----+  +----+  +----+  +-----+
     |       |        |       |       |       |        |
+----v-------v--------v-------v-------v-------v--------v
|                                                      |
|                         Zebra                        |
|                                                      |
+------------------------------------------------------+
       |                    |                   |
       |                    |                   |
+------v------+   +---------v--------+   +------v------+
|             |   |                  |   |             |
| *NIX Kernel |   | Remote dataplane |   | ........... |
|             |   |                  |   |             |
+-------------+   +------------------+   +-------------+
```

### 内核接口

FRR 主要通过 Netlink 套接字与内核进行通信，所有方式包括：

| 方式                         | 说明                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| ioctl                        | 较为底层的传统方式，可读写内核信息。                         |
| sysctl                       | 软件程序，通过 MIB 语法可查询内核信息，不可写。              |
| proc filesystem              | 特殊文件系统，简单易用，用于获取内核信息。                   |
| **routing socket / Netlink** | 内核异步通信方式，通过 Netlink 套接字（BSD 上是路由套接字）读写内核信息。 |

### 支持协议

FRR 支持众多协议，下文对常用协议从两方面进行描述：

- 如何配置使用该协议
- 协议/源码角度分析

## FRR 协议配置

### Zebra 协议

zebra is an IP routing manager. It provides kernel routing table updates, interface lookups, and redistribution of routes between different routing protocols.

### RIP 协议

### IS-IS 协议

### OSPF 协议

### BGP 协议

## FRR 源码分析

### 架构分析

### 基础工具

### PIM 协议

以 PIM 为例

pim.h
数值、结构体定义

pim.c

1. 创建协议套接字（注册回调）
2. 接收函数
3. 处理函数（抽离到单独的文件中处理）
4. 发送函数

> 函数名称建议使用格式 action_proto_subproto()

```c
void init_pim()
    -> register pim_read()
void pim_read(f, rfd)
    -> accept_pim()
void accept_pim(recvlen)
    src = ip->ip_src.s_addr;
    dst = ip->ip_dst.s_addr;
    pim  = (pim_header_t *) (pim_recv_buf + iphdrlen);
    pimlen = recvlen - iphdrlen;
    -> receive_pim_hello(src, dst, (char *) (pim), pimlen)
    -> receive_pim_join_prune(src, dst, (char *) (pim), pimlen);
    -> receive_pim_assert(src, dst, (char *) (pim), pimlen);
    -> receive_pim_graft(src, dst, (char *) (pim), pimlen, pim->pim_type);
void send_pim(buf, src, dst, type, datalen)
    global sendbuf
    prepare ip header
    prepare pim hearder
    -> send_pim_unicast() 
    -> send_pim_multicast()
```

> 建议 accept_proto 函数带上地址层层传递，方便后续协议处理源地址和目的地址！！

pim_proto.c

```c
int receive_pim_hello(src, dst, pim_message, datalen)
    -> cksum 校验
    -> find_vif_direct(src) 校验端口是不是合法
    -> parse_pim_hello() Get the Holdtime (in seconds) from the message. Return if error.
    -> 
```

char* packet_kind(proto, type, code)

## FRR debug

### FRR debug 相关命令

### 日志

可以指定 frr 的 log 文件

### terminal monitor

### GDB

单独启动 bgpd 进程时，需要指定配置文件

```shell
gdb --args bgpd -f config_file arg1 arg2 arg3
```

需要调试多线程时
