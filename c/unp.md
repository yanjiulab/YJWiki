# Unix 网络编程

## 头文件总结

| 头文件         | 标准  | 简介                    | 主要内容                                                     | 应用场景                     |
| -------------- | ----- | ----------------------- | ------------------------------------------------------------ | ---------------------------- |
| `sys/socket.h` | POSIX | 主要套接字库            | 主要套接字的结构体、函数定义。                               | 常规引入                     |
| `sys/un.h`     | POSIX | Unix 域（本地）套接字库 | Unix 域套接字的结构体、函数定义。                            | 需要 Unix 域套接字时引入     |
| `netinet/in.h` | POSIX | 套接字地址结构定义      | 各种套接字地址结构、字节序转换函数等定义。                   | 常规引入                     |
| `netinet/*.h`  | POSIX | Internet 协议族包结构   | 包括主要协议（Ethernet、IP、ARP、IGMP、ICMP、TCP、UDP 等）的包结构以及相关变量函数的定义。 | 需要操作协议头时需要引入     |
| `arpa/inet.h`  | POSIX | Internet 协议族地址转换 | 各种 IP 地址的格式转换函数。                                 | 常规引入                     |
| `strings.h`    | ISO C | 字符串、内存操作        | 各种内存操作，例如内存清零、拷贝等。                         | 常规引入                     |
| `unistd.h`     | ISO C | unix 系统调用接口       | read，write, close，fork，exec 等                            | 常规引入                     |
| `signal.h`     | ISO C | 信号函数                | POSIX 信号相关函数                                           | 需要软件中断时引入           |
| `sys/select`.h | POSIX | IO 复用                 | selec 相关函数                                               | 需要 IO 复用时引入           |
| `poll.h`       | POSIX | IO 复用                 | poll 相关函数                                                | 需要 IO 复用时引入           |
| `fcntl.h`      | POSIX | file control 文件控制   | 各种描述符控制操作                                           | 需要设置描述符控制属性时引入 |
| `netdb.h`      | POSIX | 域名相关                | 与域名和 IP 地址转换相关的函数                               | 需要域名解析时引入           |
|                |       |                         |                                                              |                              |

## 各种函数

`sys/ioctl.h`  POSIX  各种 IO 接口操作函数  获取接口信息、访问路由表、ARP 缓存等函数  



基础库

- [ ] 常用函数封装：wrapper 函数库
  - [ ] wrapper.h
  - [ ] wrap_socket.h
  - [ ] wrap
- [ ] 编程语言封装库：
- [ ] 

## 路由套接字

创建一个路由套接字后，进程可以通过写该套接字，向内核发送命令，通过读自该套接字，从内核接收信息。

### sysctl

使用 sysctl 获取：

- 路由表
- 接口表
- ARP 缓存

注：Linux很多没有

### 接口名字和索引函数

- if_nametoindex()
- if_indextoname()
- if_nameindex()
- if_freenameindex()

    #include <net/if.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <unistd.h>
    
    int
    main(int argc, char *argv[])
    {
        struct if_nameindex *if_ni, *i;
    
        if_ni = if_nameindex();
        if (if_ni == NULL) {
        	perror("if_nameindex");
            exit(EXIT_FAILURE);
        }
        
        for (i = if_ni; ! (i->if_index == 0 && i->if_name == NULL); i++)
        	printf("%u: %s\n", i->if_index, i->if_name);
        
        if_freenameindex(if_ni);
        
        exit(EXIT_SUCCESS);
    }

### 最长掩码匹配实现

路由三要素：

- 目的网段
- 掩码
- 下一跳

注意，没有输出端口

路由通过两种方式进入内核：

- 主机自动发现
- 静态配置
- 路由协议进程

实现算法：

- 哈希表
- trie树
- PC-trie树
- LC-trie树
- 256-way-mtrie树
- LPM





## 实用编程技巧

- 给结构体分配内存：使用 char * buf 初始化一块空间，然后使用 calloc（1，size）将其清空，size为结构体长度，然后使用结构体强制转换进行 buf 赋值操作。

```c
char *buf;
struct rt_msghdr *rtm;
buf = calloc(1, sizeof(struct rt_msghdr));
rtm = (struct rt_msghdr *)buf;
rtm->xxx = xxx;
```

- 结构体指针+1跳过1个结构体的长度。



## 进程间通信

## ioctl - 设备控制

`ioctl` 是 IO Control 的缩写，而 IO 可以理解为广义上的输入输出设备，因此该函数提供了多种对于设备的控制功能。

`ioctl` 基本语法如下：

```c
#include <sys/ioctl.h>
int ioctl(int fd, unsigned long request, ...);
```

其中：

- 第一个参数 fd 表示设备。
- 第二个参数 request 是一个与设备无关的请求码，请求码以宏的形式定义。
- 第三个参数通常是一个“内存变量”，装载着从内核中获取的信息（get 操作），或者要向内核发送的信息（set 操作）。

`ioctl` 中与网络相关的请求可以划分为 6 类：

- 套接字操作
- 文件操作
- 接口操作
- ARP 高速缓存操作
- 路由表操作
- 流系统操作

其中，最为常用的是接口操作，其请求码格式为 `SIOCGIFxxx` 和 `SIOCSIFxxx`，分别表示对于接口的 Get 操作和 Set 操作。
