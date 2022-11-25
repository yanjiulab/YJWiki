# Unix 网络编程

## 网络编程概述

### 网络通信模型

### 套接字编程接口

tcp

udp

raw

....

### 网络编程头文件

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



## 套接字地址结构

大多数套接字函数都需要一个**指向套接字地址结构的指针作为参数**，每个协议族都定义了自己的套接字地址结构，这些结构名均以 `sockaddr_` 开头。

| 结构体名称         | 功能              | 头文件           |
| ------------------ | ----------------- | ---------------- |
| `sockaddr`         | 通用套接字地址    | `<sys/socket.h>` |
| `sockaddr_storage` | 新通用套接字地址  | `<sys/socket.h>` |
| `sockaddr_in`      | IPv4 套接字地址   | `<netinet/in.h>` |
| `sockaddr_in6`     | IPv6 套接字地址   | `<netinet/in.h>` |
| `sockaddr_un`      | Unix 域套接字地址 | `<sys/un.h>`     |

> 结构体中的 IP 地址和端口结构均是网络序。

### 地址传递与值-结果参数

当往一个套接字函数传递套接字地址时，传递的是指向该结构的一个指针。

```c
struct sockaddr_in serv;
// filling in serv{}
connect(sockfd, (struct sockaddr *)&serv, sizeof(serv));
```

同时，该结构的长度通常也作为一个参数来传递，但其传递方式取决于传递的方向是从内核到进程还是从进程到内核。

- 从进程到内核传递套接字，其参数是结构体的整数大小。内核通过指针和内容大小，便知道从进程复制多少数据。
- 从内核到进程传递套接字，其参数是指向表示该结构大小的整数变量的指针。当函数被调用时，它告诉内核该结构的大小，这样内核写该结构时不会越界；当函数返回时，结构大小又是一个结果，它告诉进程内核在该结构中存储了多少信息。这种类型的参数称为值-结果参数。

![value-result](unp.assets/value-result.png)

当使用值-结果参数时，如果地址结构时固定长度的，那么内核返回值总是固定的，例如 IPv4 是 16 字节，IPv6 是 28 字节。如果是可变套接字结构，那么返回值很可能小于该结构的最大长度。

### 通用套接字地址结构

套接字函数以引用（指针）形式来传递套接字地址参数，需要通用类型指针来支持任何协议族的套接字地址，由于历史因素，当时并没有 `void *` 这种通用类型指针，因此定义了一个通用的套接字地址结构。

```c
struct sockaddr {
    uint8_t sa_len;
    sa_family_t sa_family;  /* address family: AF_XXX value */
    char sa_data[14];       /* protocol specific address */
}
```

**其中，sa_len 结构体长度字段并不是所有的实现都支持，这是 BSD 添加的，用于简化套接字地址结构的处理，但 POSIX 规范并不要求有这个成员。**因此，在 Linux 中定义如下，共计 16 字节。

```c
struct sockaddr
{
    __SOCKADDR_COMMON (sa_);	/* Common data: address family and length.  */
    char sa_data[14];		/* Address data.  */
};
```

其中 `__SOCKADDR_COMMON (sa_)` 是一个宏定义，其定义为 `#define __SOCKADDR_COMMON(sa_prefix) sa_family_t sa_prefix##family`，其中使用了 `##` 连接符，将 `sa_prefix` 和 `family` 进行连接。例如，`__SOCKADDR_COMMON (sa_)` 将会被简单的替换为 ` sa_family_t sa_family`。

### IPv4 地址结构

IPv4 套接字地址结构以 `sockaddr_in` 命名，协议族前缀为 `sin_`，**包含三个主要的结构：协议族 `sin_family`、端口 `sin_port` 以及网络地址 `sin_addr`**，最后的 `sin_zero` 是用来补齐与通用套接字地址结构相比不足的位。

```c
/* Internet address.  */
typedef uint32_t in_addr_t;
struct in_addr {
    in_addr_t s_addr;
};

/* Structure describing an Internet socket address.  */
struct sockaddr_in {
    __SOCKADDR_COMMON (sin_);									// 2 字节
    in_port_t sin_port;            /* Port number.  */			// 2 字节
    struct in_addr sin_addr;        /* Internet address.  */	// 4 字节

    /* Pad to size of `struct sockaddr'.  */					// 8 字节
    unsigned char sin_zero[sizeof(struct sockaddr) -
                           __SOCKADDR_COMMON_SIZE -
                           sizeof(in_port_t) -
                           sizeof(struct in_addr)];
};
```

> 或许你会发现，`in_addr` 中 仅仅定义了一个 `in_addr_t` 类型的变量，这就造成了 IPv4 地址存在两种不同的访问方法，例如，定义了套接字地址结构为 serv，那么 `serv.sin_addr` 将按照 `in_addr` 结构体来引用 32 位地址，而 `serv.sin_addr.s_addr` 将按照 `in_addr_t` (通常是一个 32 位整数) 来引用同一个地址，因此，我们必须正确的处理参数。这是具有历史原因的，一开始 `sin_addr` 是一个结构，定义为多种结构的 union，允许访问其中的部分字节，用于早期 IP 地址划分为 A，B，C 的时期，随着子网划分技术和无类地址编排的发展，其它结构被废除，仅仅剩下了一个字段的结构。

### IPv6 地址结构

IPv4 套接字地址结构以 `sockaddr_in`6 命名，协议族前缀为 `sin6_`。

```c
/* IPv6 address */
struct in6_addr {
    union {
        uint8_t __u6_addr8[16];
        uint16_t __u6_addr16[8];
        uint32_t __u6_addr32[4];
    } __in6_u;
#define s6_addr            __in6_u.__u6_addr8
#ifdef __USE_MISC
# define s6_addr16        __in6_u.__u6_addr16
# define s6_addr32        __in6_u.__u6_addr32
#endif
};

/* Structure describing an IPv6 socket address.  */
struct sockaddr_in6 {
    __SOCKADDR_COMMON (sin6_);								// 2 字节
    in_port_t sin6_port;    /* Transport layer port # */	// 2 字节
    uint32_t sin6_flowinfo;    /* IPv6 flow information */	// 4 字节
    struct in6_addr sin6_addr;    /* IPv6 address */		// 16 字节
    uint32_t sin6_scope_id;    /* IPv6 scope-id */			// 4 字节
};
```

## 基本套接字编程

### 字节操作函数

`string.h` 头文件定义了以 `mem` 开头的操作内存字节的函数，在网络编程时，经常使用该系列函数对内存字节进行操作。

| 函数名                | 作用                       |
| --------------------- | -------------------------- |
| `memcpy(dst, src, n)` | 将 src 的 n 字节拷贝到 dst |
| `memset(s, c, n)`     | 将 s 的 n 字节设为 c       |
| `memcmp(s1, s2, n)`   | 比较 s1 和 s2 的 n 字节    |



### 字节序函数

内存存储 16 位整数有两种形式：

- 小端字节序：低序字节存储在起始地址。
- 大端字节序：高序字节存储在起始地址。

![byte-order](unp.assets/byte-order.png)

这两种字节序没有标准可寻，都在系统中使用着。某个系统所使用的字节序称为**主机字节序**（host byte order），网络协议使用的字节序称为**网络字节序**（network byte order）。通常情况下，Linux 系统使用小端字节序，网络协议使用大端字节序，我们只需要在合适的情况下调用字节序转换函数即可。

以下函数包含在头文件  `#include<arpa/inet.h>` 中，其中 `s` 表示 `unsigned short int ` ，`l` 表示  `unsigned long int `。

| 函数名  |           主要功能           |
| :-----: | :--------------------------: |
| `htons` | 16位短整形数据主机序转网络序 |
| `htonl` | 32位长整形数据主机序转网络序 |
| `ntohs` | 16位短整形数据主机序转网络序 |
| `ntohl` | 32位长整形数据主机序转网络序 |

### 地址转换函数

以下函数包含在头文件  `#include<arpa/inet.h>` 中。

|   函数名    |                           主要功能                           |
| :---------: | :----------------------------------------------------------: |
| `inet_aton` | 点分十进制数字符串转换为 32 位网络字节序二进制值 (`struct in_addr`) |
| `inet_ntoa` | 32 位网络字节序二进制值 (`struct in_addr`) 转换为点分十进制数字符串 |
| `inet_pton` |      表达式格式 (presentation) 转换为数值格式 (numeric)      |
| `inet_ntop` |      数值格式 (numeric) 转换为表达式格式 (presentation)      |

### 数据读写函数

## TCP 套接字编程

### 基本函数

|   函数名   |             主要功能              |
| :--------: | :-------------------------------: |
|  `socket`  |            创建套接字             |
|   `bind`   |         为套接字绑定地址          |
| `connect`  |         主动发起 TCP 连接         |
|  `listen`  |      标记该 TCP 套接字为被动      |
|  `accept`  | 从 TCP 连接队列取出一个已完成连接 |
|  `close`   |           关闭 TCP 连接           |
|   `read`   |            TCP 读字节             |
|  `write`   |            TCP 写字节             |
| `recvfrom` |           UDP 接收数据            |
|  `sendto`  |           UDP 发送数据            |



## UDP 套接字编程

## Unix 域套接字编程

### CS示例

服务端

```c
int sockfd;
char* path = "/tmp/parent";
struct sockaddr_un remoteaddr, localaddr;

sockfd = socket(AF_LOCAL, SOCK_DGRAM, 0);
unlink(path);
bzero(&remoteaddr, sizeof(remoteaddr));
bzero(&localaddr, sizeof(localaddr));

localaddr.sun_family = AF_LOCAL;
strcpy(localaddr.sun_path,path);

bind(sockfd, (struct sockaddr *)&localaddr, sizeof(localaddr));
printf("[main] bind success\n");

int			n;
socklen_t	len;
char		mesg[MAXLINE];

for ( ; ; ) {
    len = sizeof(remoteaddr);
    n = recvfrom(sockfd, mesg, MAXLINE, 0, &remoteaddr, &len);
    printf("[main] recieve %s from server %s\n", (char *)mesg, remoteaddr.sun_path);
    sendto(sockfd, mesg, n, 0, &remoteaddr, len);
    printf("[main] send %s to server %s\n", (char *)mesg, remoteaddr.sun_path);
}
```



## 客户端
{% codeblock lang:c %}
int sockfd;
    char* server_path = "/tmp/parent";
    char* path = "/tmp/child";
    struct sockaddr_un remoteaddr, localaddr;
    
    sockfd = socket(AF_LOCAL, SOCK_DGRAM, 0);
    printf("[child] %d\n",sockfd);
    unlink(path);
    bzero(&remoteaddr, sizeof(remoteaddr));
    bzero(&localaddr, sizeof(localaddr));
    
    localaddr.sun_family = AF_LOCAL;
    strcpy(localaddr.sun_path,path);
    
    bind(sockfd, (struct sockaddr *)&localaddr, sizeof(localaddr));
    printf("[child] bind to %s success\n", path);
    
    remoteaddr.sun_family = AF_LOCAL;
    strcpy(remoteaddr.sun_path, server_path);
    
    int			n;
    socklen_t len = sizeof(remoteaddr);
    char sendbuf[MAXLINE] = {'f', 'u', 'c', 'k', '\0'};
    char recvbuf[MAXLINE];
    
    sendto(sockfd, sendbuf, strlen(sendbuf), 0, &remoteaddr, len);
    printf("[child] send %s to server %s\n", (char *)sendbuf, remoteaddr.sun_path);
    
    n = recvfrom(sockfd, recvbuf, MAXLINE, 0, &remoteaddr, &len);
    
    printf("[child] recieve %s from server %s\n",(char *) recvbuf, remoteaddr.sun_path);
    
    return 0; 
{% endcodeblock %}

# Unix 域数据报客户/服务器实例

## 套接字选项

|    函数名     |        主要功能        |
| :-----------: | :--------------------: |
| `getsockname` | 获取套接字本地协议地址 |
| `getpeername` | 获取套接字对端协议地址 |
| `getsockopt`  |     获取套接字选项     |
| `setsockopt`  |     设置套接字选项     |

## 名字与地址转换

### 域名系统

通常情况下，我们会使用数值地址（32 位 IP 地址）来表示主机，例如 `206.6.22.3`，用数值端口号（16 位数）来表示服务器，例如 80 号端口通常表示主机上的一个 Web 服务器。然而，许多情况下我们应该使用域名来代替地址，因为域名容易记忆又输入方便。因此网络编程需要在地址和域名之间进行转换的函数。

我们知道，域名和 IP 地址转换由 DNS 协议来完成，实际中转换由 DNS 服务器来完成，那么我们编写的代码如何与 DNS 服务器打交道呢？答案是通过解析器（resolver）来完成，解析器代码通常位于系统库函数中，构造应用程序时被 link-editing 到应用程序中。

![resolver](unp.assets/resolver.png)

### netdb

### IPv4 转换函数

### 通用转换函数

以下函数包含在头文件  `#include<netdb.h>` 中。

|     函数名      |                  主要功能                  |
| :-------------: | :----------------------------------------: |
| `gethostbyname` |           根据域名查找 IPv4 地址           |
| `gethostbyaddr` |           根据 IPv4 地址查找域名           |
| `getservbyname` |             根据服务名查找端口             |
| `getservbyport` |             根据端口查找服务名             |
|  `getaddrinfo`  | 根据域名查找 IP 地址<br>根据服务名查找端口 |
|  `getnameinfo`  | 根据 IP 地址查找域名<br>根据端口查找服务名 |

### `gethostbyname` 函数

```c
#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv)
{
    char* hostname = NULL;
    struct hostent* hptr = NULL;
    char ip[16] = { '\0' };

    while (--argc > 0) {
        hostname = *++argv;
        if ((hptr = gethostbyname(hostname)) == NULL) {
            printf("Error for host %s: %s\n", hostname, hstrerror(h_errno));
            exit(1);
        }

        printf("Official hostname: %s\n", hptr->h_name);
        for (char** palias = hptr->h_aliases; *palias != NULL; palias++) {
            printf("\tAlias name: %s\n", *palias);
        }
        if (hptr->h_addrtype == AF_INET) {
            for (char** paddr = hptr->h_addr_list; *paddr != NULL; paddr++) {
                printf("\tIPv4 address: %s\n", inet_ntop(hptr->h_addrtype, *paddr, ip, sizeof(ip)));
            }
        } else {
            printf("Unknow address type\n");
        }
    }

    return 0;
}
```

测试：

```
$ ./test_gethostbyname dns.google
Official hostname: dns.google
        IPv4 address: 8.8.8.8
        IPv4 address: 8.8.4.4
```



### `gethostbyaddr` 函数

```c
#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv)
{
    char* ipv4 = NULL; // input
    struct hostent* hptr = NULL;
    struct in_addr sa = { 0 };

    while (--argc > 0) {
        ipv4 = *++argv;

        if (inet_pton(AF_INET, ipv4, &sa) <= 0) {
            printf("input error\n");
            exit(1);
        }

        if ((hptr = gethostbyaddr(&sa, 4, AF_INET)) == NULL) {
            printf("Error for ip %s: %s\n", ipv4, hstrerror(h_errno));
            exit(1);
        }
        printf("IPv4 addr: %s\n", ipv4);
        printf("Official hostname: %s\n", hptr->h_name);
    }

    return 0;
}
```

测试

```
$ ./test_gethostbyaddr 8.8.8.8
IPv4 addr: 8.8.8.8
Official hostname: dns.google
```

### `getservbyname` 函数

TODO

### `getservbyport` 函数

TODO

### `getaddrinfo` 函数

名字到地址，以及服务到端口

```c
#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv)
{
    struct addrinfo* result = NULL;
    struct addrinfo* ptr = NULL;
    struct addrinfo hints = { 0 };
    hints.ai_family = PF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags |= AI_CANONNAME;

    char* host = NULL;

    while (--argc > 0) {
        host = *++argv;

        int n;
        if ((n = getaddrinfo(host, NULL, &hints, &result)) != 0) {
            perror("getaddrinfo");
            printf("getaddrinfo: %s\n", gai_strerror(n));
            exit(1);
        }
        printf("Host: %s\n", host);

        for (ptr = result; ptr != NULL; ptr = ptr->ai_next) {
            char addrstr[INET6_ADDRSTRLEN];
            void* p = NULL;
            inet_ntop(ptr->ai_family, ptr->ai_addr->sa_data, addrstr, sizeof(addrstr));

            switch (ptr->ai_family) {
            case AF_INET:
                p = &((struct sockaddr_in*)ptr->ai_addr)->sin_addr;
                break;
            case AF_INET6:
                p = &((struct sockaddr_in6*)ptr->ai_addr)->sin6_addr;
                break;
            }

            inet_ntop(ptr->ai_family, p, addrstr, sizeof(addrstr));
            printf("IPv%d address: %s (%s)\n", ptr->ai_family == AF_INET6 ? 6 : 4,
                addrstr, ptr->ai_canonname);

            printf("flag: %d\n", ptr->ai_flags);
            printf("protocol: %d\n", ptr->ai_protocol);
            printf("socket type: %d\n", ptr->ai_socktype);
            printf("addr len: %d\n", ptr->ai_addrlen);
        }

        freeaddrinfo(result);
    }
}
```

### `getnameinfo` 函数

TODO

### 打包我们自己的函数



## Unix I/O 模型

- 阻塞 IO
- 非阻塞 IO 往往耗费大量 CPU 时间
- IO Multiplexing (Event-driven IO) 与在多线程中使用阻塞式 IO 极为相似
- Sigal-driven IO 开启套接字的信号驱动式 IO 功能，并通过sigaction 安装一个信号处理函数
- 异步IO Asynchronous IO 信号驱动式 IO 是由内核通知我们何时可以启动一个 IO 操作，而异步 IO 模型是由内核通知我们 IO 操作何时完成。aio_read

- https://eklitzke.org/blocking-io-nonblocking-io-and-epoll
The multiplexing approach to concurrency is what I call “asynchronous I/O”. Sometimes people will call this same approach “nonblocking I/O”, which I believe comes from a confusion about what “nonblocking” means at the systems programming level. I suggest reserving the term “nonblocking” for referring to whether or not file descriptors are actually in nonblocking mode or not.

### 阻塞式 I/O

fork、线程、

### 非阻塞式 I/O

### I/O 复用

基于事件的并发针对两方面问题：
1. 多线程应用中，正确处理并发很有难度，忘记加锁、死锁和其他烦人的问题会发生。
2. 开发者无法控制多线程在某一时刻的调度。程序员只是创建了线程，然后就依赖操作系统能够合理的调度。在某些时候操作系统的调度不是最优的。

### 编程模型

### 异步 I/O

## I/O 复用

## ioctl - 设备控制

`sys/ioctl.h`  POSIX  各种 IO 接口操作函数  获取接口信息、访问路由表、ARP 缓存等函数  

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

### 接口操作

`ifconf` structure

```c
/*
 * Structure used in SIOCGIFCONF request.
 * Used to retrieve interface configuration
 * for machine (useful for programs which
 * must know all networks accessible).
 */
struct ifconf {
    int ifc_len; /* size of buffer	*/
    union {
        char __user *ifcu_buf;
        struct ifreq __user *ifcu_req;
    } ifc_ifcu;
};
#define ifc_buf ifc_ifcu.ifcu_buf /* buffer address	*/
#define ifc_req ifc_ifcu.ifcu_req /* array of structures */
```



`ifreq` structure

```c
/*
 * Interface request structure used for socket
 * ioctl's.  All interface ioctl's must have parameter
 * definitions which begin with ifr_name.  The
 * remainder may be interface specific.
 */
struct ifreq {
#define IFHWADDRLEN 6
    union {
        char ifrn_name[IFNAMSIZ]; /* if name, e.g. "en0" */
    } ifr_ifrn;

    union {
        struct sockaddr ifru_addr;
        struct sockaddr ifru_dstaddr;
        struct sockaddr ifru_broadaddr;
        struct sockaddr ifru_netmask;
        struct sockaddr ifru_hwaddr;
        short ifru_flags;
        int ifru_ivalue;
        int ifru_mtu;
        struct ifmap ifru_map;
        char ifru_slave[IFNAMSIZ]; /* Just fits the size */
        char ifru_newname[IFNAMSIZ];
        void __user *ifru_data;
        struct if_settings ifru_settings;
    } ifr_ifru;
};
#define ifr_name ifr_ifrn.ifrn_name           /* interface name 	*/
#define ifr_hwaddr ifr_ifru.ifru_hwaddr       /* MAC address 		*/
#define ifr_addr ifr_ifru.ifru_addr           /* address		*/
#define ifr_dstaddr ifr_ifru.ifru_dstaddr     /* other end of p-p lnk	*/
#define ifr_broadaddr ifr_ifru.ifru_broadaddr /* broadcast address	*/
#define ifr_netmask ifr_ifru.ifru_netmask     /* interface net mask	*/
#define ifr_flags ifr_ifru.ifru_flags         /* flags		*/
#define ifr_metric ifr_ifru.ifru_ivalue       /* metric		*/
#define ifr_mtu ifr_ifru.ifru_mtu             /* mtu			*/
#define ifr_map ifr_ifru.ifru_map             /* device map		*/
#define ifr_slave ifr_ifru.ifru_slave         /* slave device		*/
#define ifr_data ifr_ifru.ifru_data           /* for use by interface	*/
#define ifr_ifindex ifr_ifru.ifru_ivalue      /* interface index	*/
#define ifr_bandwidth ifr_ifru.ifru_ivalue    /* link bandwidth	*/
#define ifr_qlen ifr_ifru.ifru_ivalue         /* Queue length 	*/
#define ifr_newname ifr_ifru.ifru_newname     /* New name		*/
#define ifr_settings ifr_ifru.ifru_settings   /* Device/proto settings*/
```



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

```
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
```

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

## 广播

## 组播

## 原始套接字

## 数据链路套接字

## C/S 架构程序设计范式

## 网络编程技巧

- 给结构体分配内存：使用 char * buf 初始化一块空间，然后使用 calloc（1，size）将其清空，size为结构体长度，然后使用结构体强制转换进行 buf 赋值操作。结构体指针+1跳过1个结构体的长度。

```c
char *buf;
struct rt_msghdr *rtm;
buf = calloc(1, sizeof(struct rt_msghdr));
rtm = (struct rt_msghdr *)buf;
rtm->xxx = xxx;
```

- TODO

## 参考
