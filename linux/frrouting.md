# 路由 - FRRouting

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

## FRR 源码编译安装

如果是仅需要使用 FRR，可以通过包管理器（如 Ubuntu 的 apt）安装，这种安装方式比较简单。但大多数情况下 FRR 使用者需要定制功能，或者进行二次开发，此时需要编译安装，本文主要介绍编译安装的方式，总体而言与 Quagga 类似，但依赖安装更为繁琐一些。大致流程如下：

1. 下载源码
2. 更新构建系统
3. 配置 configure 参数
4. make 编译安装

上述步骤命令如下：

```sh
git clone https://github.com/frrouting/frr.git frr
cd frr
./bootstrap.sh
./configure [...]
make [-j] # 根据需求是否开启并行编译加速
make check
sudo make install
```

后文以 Ubuntu 22.04 系统为例，进行详细的描述。

## 安装依赖

在正式安装之前，需要首先安装好依赖。依赖可以分为两类：

1. 安装工具依赖：这些是编译安装时依赖的工具，通过包管理器二进制安装即可。不同的发行版具有不同的安装方式，这一步参考 FRR 开发文档。但 FRR 有些依赖在包管理器中可能没有，或是版本不适配，因此也需要通过源码编译安装。
2. 功能模块依赖：根据 configure 的参数不同，FRR 编译的模块也不同。有些可选的模块，如果不需要编译该功能，也可以不安装对应的依赖。功能模块的依赖主要以源码编译安装为主，个别如果有二进制，也可以进行 apt 等方式安装。

下面列出 FRR 可能用到的需要源码编译的依赖。

```sh
sudo apt-get install git cmake build-essential bison flex libpcre3-dev libev-dev libavl-dev libprotobuf-c-dev protobuf-c-compiler libcmocka0 libcmocka-dev doxygen libssl-dev libssl-dev libssh-dev
```

### libyang

FRR 需要依赖 libyang 2.0 版本以上，libyang 源码安装如下。

```shell
git clone https://github.com/CESNET/libyang.git
cd libyang
mkdir build; cd build
cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr -D CMAKE_BUILD_TYPE:String="Release" ..
make
sudo make install
```

注意：最好指定 `/usr/` 前缀，这样可以避免一些搜索路径的问题。否则默认安装到 `/usr/local` 中。另外如果编译 libyang 失败，则可以通过 apt 安装缺失的工具。

### gRPC

如果需要北向 gRPC 接口需要安装 gRPC 依赖。

sudo apt install -y build-essential autoconf libtool pkg-config

## 配置用户和组

如果需要，可以根据需求配置 FRR 成员和组。如果不想创建这些组和用户，可以直接用 root，因此就不需要本节的配置。

```shell
sudo groupadd -r -g 92 frr
sudo groupadd -r -g 85 frrvty
sudo adduser --system --ingroup frr --home /var/run/frr/ --gecos "FRR suite" --shell /sbin/nologin frr
sudo usermod -a -G frrvty frr
```

## 编译安装

```sh
./configure \
    CFLAGS=-Wl,--copy-dt-needed-entries \
    --prefix=/opt/frr \
    --localstatedir=/var/run/frr \
    --enable-snmp=agentx \
    --enable-multipath=64 \
    --enable-user=root \
    --enable-group=root \
    --enable-fpm \
    --enable-config-rollbacks \
    --enable-sysrepo=yes 
```

使用 GCC 11 编译时，需要加上 `-Wl,--copy-dt-needed-entries` 参数，否则会产生 DSO missing 问题。

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

## FRR 极简安装配置指南

初学者自己学习使用时，推荐安装下文的方式进行安装配置，这样可以对 FRR 有更清晰的认识。首先，安装好各个依赖项，准备好 FRR 源码，就可以开工了。

首先进行配置，这里将 FRR 安装到 `/opt/frr` 目录下，这样的好处是将 FRR 相关的可执行及配置文件集中到一起，否则各种目录将散落到 `/usr/local/` 目录下面。另外，由于是个人使用，所以直接使用 `root:root` 来管理 FRR，简化了了创建用户和组的过程。

```
./configure \
    --enable-user=root \
    --enable-group=root \
    --prefix=/opt/frr/
```

注意：如果需要学习某模块或特性，请详细参考 configure 帮助，因为有一些功能是默认不安装的，因此需要确保你需要的模块安装了，不过大部分情况下，按照上述安装的 FRR 包含了绝大部分常用模块。

然后进行编译和安装，安装后可以查看 FRR 都生成了哪些文件。

```
# make -j
...

# make install
....

# ls /opt/frr
bin  include  lib  sbin  share
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

RIP 简要配置如下：

```
debug rip events
debug rip packet

router rip
 network 11.0.0.0/8
 network eth0
 route 10.0.0.0/8
 distribute-list private-only in eth0

access-list private-only permit 10.0.0.0/8
access-list private-only deny any
```

### IS-IS 协议

### OSPF 协议

重分布

### BGP 协议

### 调试相关

命令|描述
:---:|:---:
`terminal monitor`|将日志显示在控制台中

## 北向接口 NETCONF

### 依赖库安装

首先需要检查依赖，安装 sysrepo、libnetconf2 和 netopper2 库。

1. 安装 YANG 模型数据库 `sysrepo`。

    ```sh
    git clone https://github.com/sysrepo/sysrepo.git
    mkdir build; cd build
    cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr -DREPO_PATH=/opt/sysrepo/repository -DSR_PLUGINS_PATH=/opt/sysrepo/plugins -DSRPD_PLUGINS_PATH=/opt/sysrepo-plugind/plugins ..
    make
    sudo make install
    ```

2. 安装 NETCONF 协议库 `libnetconf2`。

    ```sh
    git clone https://github.com/CESNET/libnetconf2.git
    cd libnetconf2/
    mkdir build; cd build
    cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr -D CMAKE_BUILD_TYPE:String="Release" ..
    make
    sudo make install
    ```

3. 安装集成套件 `netopeer2`。

    ```sh
    $ git clone https://github.com/CESNET/netopeer2.git
    $ cd netopeer2
    $ mkdir build; cd build
    cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr -D CMAKE_BUILD_TYPE:String="Release" ..
    make
    sudo make install
    ```

### 构建 FRR

依赖安装完毕后，configure 时新增 `--enable-sysrepo=yes` 参数重新构建 FRR。FRR 使用了动态模块加载机制，使能该参数后，将会编译出 sysrepo 的动态链接库，若模块路径，例如 `/opt/frr/lib/frr/modules/` 下查看到 `sysrepo.so` 文件，则表示构建成功。构建成功后，继续执行编译和安装命令即可。

### 配置 sysrepo

安装 FRR 的 YANG 模型到 sysrepo 数据库中。FRR 中 YANG 模型的路径为 `${PREFIX}/share/yang/`，首先把模型都安装到数据库中，其次根据需求更改用户和组。以下是常用命令：

```sh
sudo sysrepoctl --install ${PREFIX}/share/yang/frr-isisd.yang   # install yang model to sysrepo as a module
sudo sysrepoctl -c frr-isisd --owner frr --group frr            # change yang module ownership
sudo sysrepoctl -c :ALL -p 666                                  # change all modules permission to rw-rw-rw-。
sudo sysrepoctl -u examples                                     # uninstall module
sudo sysrepoctl -l                                              # list all module
```

!> 如果出现 install 错误的情况，是因为安装模型中引用了其他的 YANG 模型文件，因此把所有模型按照依赖顺序都安装一遍就行了。以下是安装 frr-ripd 的依赖。

```sh
sudo sysrepoctl --install /opt/frr/share/yang/frr-vrf.yang
sudo sysrepoctl --install /opt/frr/share/yang/ietf-interfaces.yang
sudo sysrepoctl --install /opt/frr/share/yang/frr-interface.yang
sudo sysrepoctl --install /opt/frr/share/yang/frr-filter.yang
sudo sysrepoctl --install /opt/frr/share/yang/frr-route-map.yang 
sudo sysrepoctl --install /opt/frr/share/yang/frr-if-rmap.yang
sudo sysrepoctl --install /opt/frr/share/yang/frr-route-types.yang
sudo sysrepoctl --install /opt/frr/share/yang/frr-bfdd.yang
sudo sysrepoctl --install /opt/frr/share/yang/frr-routing.yang 
sudo sysrepoctl --install /opt/frr/share/yang/ietf-routing-types.yang
sudo sysrepoctl --install /opt/frr/share/yang/frr-nexthop.yang
sudo sysrepoctl --install /opt/frr/share/yang/frr-ripd.yang
```

sysrepo 是基于共享内存的数据库，因此，其全部数据可以在 `/dev/shm` 查看，以 `sr` 开头的即是 sysrepo 数据库相关文件。

在安装时，sysrepo 的库文件指定在 `/opt/sysrepo/repository` 路径下。

```sh
/opt/sysrepo/repository$ tree
.
├── conn                            # 连接目录
│   ├── conn_66.lock                # netconf server 连接
│   └── conn_67.lock                # frr 连接
├── data                            # 数据文件目录
│   ├── frr-bfdd.candidate.perm
│   ├── ...
├── ...
├── sr_main_lock                    # sysrepo 全局文件锁
└── yang                            # 模型目录
    ├── frr-bfdd@2019-05-09.yang
    ├── ...
```

!> 后续启动 FRR 或 netopper2-server 后，二者连接到 sysrepo 时 conn 会有相应连接产生。

### 启动 FRR

如果需要调试，可以单独启动 ripd 进程，启动时选择 sysrepo 模块，并且在前台打印。

```sh
sudo ripd -M sysrepo --log=stdout
```

如果使用脚本启动，则在 `daemon` 配置中指定启动参数，效果相同。

启动后，进入 `vtysh` 后，通过 `show modules` 命令，可以查看 sysrepo 是否加载成功。或者通过查看日志信息确认是否加载成功。

```plain
frr# show modules
Module information for ripd:
Module Name  Version                   Description

libfrr       9.0.1                     libfrr core module
ripd         9.0.1                     ripd daemon
frr_sysrepo  9.0.1                     FRR sysrepo integration module
        from: /opt/frr/lib/frr/modules/sysrepo.so
pid: 383788
```

为了便于查看北向接口的信息，可以添加以下配置，并开启 monitor。

```plain
frr# debug northbound libyang 
frr# debug northbound callbacks 
frr# debug northbound notifications 
frr# debug northbound events 
terminal monitor
```

### 启动 NETCONF 服务器

安装好 netopper2 后，后台启动 NETCONF 服务端。

```sh
sudo netopeer2-server -d &
```

!> 如果启动时输出以下错误信息，重新 `make install` 即可。这是因为改动了 sysrepo 的某些文件。重新安装会将 sysrepo 中所有的特性启动。

```sh
[ERR]: NP: Module "ietf-netconf" feature "writable-running" not enabled in sysrepo.
[ERR]: NP: Server init failed.
```

### NETCONF 客户端

TODO：编写 python 客户端

编写 NETCONF 客户端脚本，进行配置管理。脚本使用 Python 编写，依赖 ncclient 库，可以通过 `apt install -y python3-ncclient` 进行安装。

```sh
sudo ./netconf-edit.py 127.0.0.1
sudo ./netconf-get-config.py 127.0.0.1
<?xml version="1.0" encoding="UTF-8"?><data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"><isis xmlns="http://frrouting.org/yang/isisd"><instance><area-tag>testnet</area-tag><is-type>level-1</is-type></instance></isis></data>
```

`netconf-edit.py` 脚本内容如下：

```py
#! /usr/bin/env python3
#
# Change the running configuration using edit-config
# and the test-option provided by the :validate capability.
#
# $ sudo ip vrf exec testnet ./netconf-edit.py 10.254.254.7

import sys, os, warnings
warnings.simplefilter("ignore", DeprecationWarning)
from ncclient import manager

def demo(host):
    snippet = """
      <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <isis xmlns="http://frrouting.org/yang/isisd">
          <instance>
            <area-tag>testnet</area-tag>
            <is-type>level-1</is-type>
          </instance>
        </isis>
      </config>"""

    with manager.connect(host=host, port=830, username="root", password='vagrant', hostkey_verify=False) as m:
        assert(":validate" in m.server_capabilities)
        m.edit_config(target='running', config=snippet,
                      test_option='test-then-set')

if __name__ == '__main__':
    demo(sys.argv[1])
```

`netconf-get-config.py` 脚本内容如下：

```py
#! /usr/bin/env python3
#
# Get the running configuration.
#
# $ sudo ip vrf exec testnet ./netconf-get-config.py 10.254.254.7

import sys, os, warnings
warnings.simplefilter("ignore", DeprecationWarning)
from ncclient import manager

def demo(host):
    with manager.connect(host=host, port=830, username="root", password='vagrant', hostkey_verify=False) as m:
        c = m.get_config(source='running').data_xml
        print(c)

if __name__ == '__main__':
    demo(sys.argv[1])
```

上述脚本的 username 和 password 换位自己主机的用户名和密码。

### CLI 示例



```sh
liyj-virtual-machine(config-router)# no route 10.0.1.0/24
2023-12-05 14:49:09.825 [DEBG] ripd: [W7XQT-PM3RC] nb_config_diff: {
  "frr-ripd:ripd": {
    "@": {
      "yang:operation": "none"
    },
    "instance": [
      {
        "vrf": "default",
        "static-route": [
          "10.0.1.0/24"
        ],
        "@static-route": [
          {
            "yang:operation": "delete"
          }
        ]
      }
    ]
  }
}

2023-12-05 14:49:09.825 [DEBG] ripd: [SWK28-M149C] northbound callback: event [validate] op [destroy] xpath [/frr-ripd:ripd/instance[vrf='default']/static-route[.='10.0.1.0/24']] value [10.0.1.0/24]
2023-12-05 14:49:09.825 [DEBG] ripd: [SWK28-M149C] northbound callback: event [prepare] op [destroy] xpath [/frr-ripd:ripd/instance[vrf='default']/static-route[.='10.0.1.0/24']] value [10.0.1.0/24]
2023-12-05 14:49:09.825 [DEBG] ripd: [SWK28-M149C] northbound callback: event [apply] op [destroy] xpath [/frr-ripd:ripd/instance[vrf='default']/static-route[.='10.0.1.0/24']] value [10.0.1.0/24]
liyj-virtual-machine(config-router)# route 10.0.1.0/24
2023-12-05 14:49:32.501 [DEBG] ripd: [W7XQT-PM3RC] nb_config_diff: {
  "frr-ripd:ripd": {
    "@": {
      "yang:operation": "none"
    },
    "instance": [
      {
        "vrf": "default",
        "static-route": [
          "10.0.1.0/24"
        ],
        "@static-route": [
          {
            "yang:operation": "create"
          }
        ]
      }
    ]
  }
}

2023-12-05 14:49:32.501 [DEBG] ripd: [SWK28-M149C] northbound callback: event [validate] op [create] xpath [/frr-ripd:ripd/instance[vrf='default']/static-route[.='10.0.1.0/24']] value [10.0.1.0/24]
2023-12-05 14:49:32.501 [DEBG] ripd: [SWK28-M149C] northbound callback: event [prepare] op [create] xpath [/frr-ripd:ripd/instance[vrf='default']/static-route[.='10.0.1.0/24']] value [10.0.1.0/24]
2023-12-05 14:49:32.501 [DEBG] ripd: [SWK28-M149C] northbound callback: event [apply] op [create] xpath [/frr-ripd:ripd/instance[vrf='default']/static-route[.='10.0.1.0/24']] value [10.0.1.0/24]
```

## FRR 源码分析

### 架构分析

### 命令行

```c
static int ospf_config_write(struct vty *vty);
static struct cmd_node ospf_node = {
    .name = "ospf",
    .node = OSPF_NODE,
    .parent_node = CONFIG_NODE,
    .prompt = "%s(config-router)# ",
    .config_write = ospf_config_write,
};
```

ospf_config_write() 负责将配置的命令写回配置文件。

## RIP 源码分析

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

## OSPF 源码分析

### 核心数据结构

OSPF LSDB 数据库结构定义如下：

```c
/* OSPF LSDB structure. */
struct ospf_lsdb {
    struct {
        unsigned long count;
        unsigned long count_self;
        unsigned int checksum;
        struct route_table *db;
    } type[OSPF_MAX_LSA];
    unsigned long total;
#define MONITOR_LSDB_CHANGE 1 /* XXX */
#ifdef MONITOR_LSDB_CHANGE
    /* Hooks for callback functions to catch every add/del event. */
    int (*new_lsa_hook)(struct ospf_lsa *);
    int (*del_lsa_hook)(struct ospf_lsa *);
#endif /* MONITOR_LSDB_CHANGE */
};
```

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

## FRR 源码 - 模块加载

## FRR 源码 - 北向接口

初始化函数

```c
nb_init(master, di->yang_modules, di->n_yang_modules, true);

void nb_init(struct event_loop *tm,
         const struct frr_yang_module_info *const modules[],
         size_t nmodules, bool db_enabled)
```

yang_module 是