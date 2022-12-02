# Quagga



# FRRouting

## 源码构建安装

以 CentOS 8 系统为例，其余操作系统请参考官方文档。

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
sudo dnf install cmake pcre2-devel	# libyang's dependencies
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

### 配置

#### 成员组配置

首先，根据需求配置 FRR 成员和组。

```shell
sudo groupadd -g 92 frr
sudo groupadd -r -g 85 frrvty
sudo useradd -u 92 -g 92 -M -r -G frrvty -s /sbin/nologin -c "FRR FRRouting suite" -d /var/run/frr frr
```

#### 编译选项配置

其次，根据需求对 `./configure` 命令选择适当的参数。 

```shell

```

### 编译安装

配置完毕之后，可以进行编译、检查、安装过程。

```shell
make [-j]	# 根据需求是否开启并行编译加速
make check
sudo make install
```

### 创建配置文件

#### 普通配置

创建各种配置文件

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

#### 守护进程配置

安装守护进程配置文件到相关安装目录中。

```shell
sudo install -p -m 644 tools/etc/frr/daemons /etc/frr/
sudo chown frr:frr /etc/frr/daemons
```

编辑 `/etc/frr/daemons ` 文件，根据需求选择启动相应的守护进程，yes 表示启动该进程，默认为 no 不启动。

### 相关系统配置

#### 开启 IP 转发

创建文件 `/etc/sysctl.d/90-routing-sysctl.conf `，填入以下内容：

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

#### FRR 服务配置

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

## 基本使用

### 交互方式

FRR 提供了多种方式与用户进行交互。

#### VTY

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

#### VTY Shell

`vtysh` 为**所有**守护进程提供了一个统一交互前端。**默认安装并启动**，通过 configure 参数中使用 `--disable-vtysh` 选项可以关闭该特性。

`vtysh` 通过 Unix 域套接字 `/var/run/frr` 与守护进程通信，因此需要确保用户对该目录具有操作权限。

有两种方式可以配置 FRR：

1. 独立式配置：每个守护进程有一个配置文件，名称为：`[daemon-name]d.conf`。
2. 集成式配置（推荐使用）：所有守护进程共同一个配置文件，名称为 `frr.conf` 。

若要使用集成式配置，需要在 `vtysh.conf` 中进行配置。

```shell
service integrated-vtysh-config		# vtysh 配置永远只写入 frr.conf
no service integrated-vtysh-config	# vtysh 配置不会写入 frr.conf，而是写入独立配置文件。
Neither option present (default)	# 默认行为。若 frr.conf 存在则写入；否则写入独立配置文件。
```

#### 北向 gRPC

gRPC 通过 YANG 北向接口为**所有**守护进程提供了一个统一交互前端。由于处在实验阶段**默认不安装**，通过 configure 参数中使用 `--enable-grpc` 选项可以开启该特性。

配置 FRR 守护进程监听 gRPC 端口（默认 50051）需要在守护进程配置文件中配置 `-M grpc:PORT` 参数，例如：

```shell
bfdd_options=" --daemon -A 127.0.0.1 -M grpc"		# 使用默认端口
isisd_options=" --daemon -A 127.0.0.1 -M grpc:PORT"	# 使用自定义端口
```

### 配置文件

| 文件                  | 含义                   | 说明                                                         |
| --------------------- | ---------------------- | ------------------------------------------------------------ |
| `/etc/frr/daemons`    | 守护进程初始化配置文件 | 默认 FRR 不会启动任何守护进程，需要将进程值改为 yes 才能启动。 |
| `/etc/frr/vtysh.conf` | 交互式 Shell 配置文件  | 不会随着 save 命令更新，需要管理员手动配置。                 |
| `/etc/frr/frr.conf`   | 守护进程集成式配置文件 | 所有进程在启动时首先检查是否存在该文件，若存在则不会启动独立配置文件。 |
| `/etc/frr/XXXd.conf`  | 守护进程独立式配置文件 | 例如 `zebra.conf`，`bgpd.conf`，目前已经被集成式配置文件替代。 |

## 命令



## 软件实现

### 系统架构

FRR 使用一系列守护进程共同构建路由表，每个进程实现一种协议，所有进程通过中间守护进程 `zebra` 与路由信息进行交互。

【图】

### 内核接口

FRR 主要通过 Netlink 套接字与内核进行通信，其余方式包括：

| 方式                     | 说明                                                         |
| ------------------------ | ------------------------------------------------------------ |
| ioctl                    | 较为底层的传统方式，可读写内核信息。                         |
| sysctl                   | 软件程序，通过 MIB 语法可查询内核信息，不可写。              |
| proc filesystem          | 特殊文件系统，简单易用，用于获取内核信息。                   |
| routing socket / Netlink | 内核异步通信方式，通过 Netlink 套接字（BSD 上是路由套接字）读写内核信息。 |

### 支持协议

- OSPF
- BGP
- ...

## RIP 协议

### 

## IS-IS 协议

## OSPF 协议

## BGP 协议

## PIM 协议

### 处理协议流程

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

## 帧类型

## 工具函数

char* packet_kind(proto, type, code)
