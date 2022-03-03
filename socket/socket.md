

# 函数速查表

## 基本函数

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

## 字节序

以下函数包含在头文件  `#include<arpa/inet.h>` 中。

|    函数名     |                           主要功能                           |
| :-----------: | :----------------------------------------------------------: |
| `[x]to[y][t]` | x 和 y 取值为 n 或 h，分别表示主机和网络。 <br> t 取值 s 或 l，表示 16/32 位数据。 |
|  `inet_aton`  | 点分十进制数字符串转换为 32 位网络字节序二进制值 (`struct in_addr`) |
|  `inet_ntoa`  | 32 位网络字节序二进制值 (`struct in_addr`) 转换为点分十进制数字符串 |
|  `inet_pton`  |      表达式格式 (presentation) 转换为数值格式 (numeric)      |
|  `inet_ntop`  |      数值格式 (numeric) 转换为表达式格式 (presentation)      |

## 套接字选项

|    函数名     |        主要功能        |
| :-----------: | :--------------------: |
| `getsockname` | 获取套接字本地协议地址 |
| `getpeername` | 获取套接字对端协议地址 |
| `getsockopt`  |     获取套接字选项     |
| `setsockopt`  |     设置套接字选项     |

## 地址

以下函数包含在头文件  `#include<netdb.h>` 中。

|     函数名      |                  主要功能                  |
| :-------------: | :----------------------------------------: |
| `gethostbyname` |           根据域名查找 IPv4 地址           |
| `gethostbyaddr` |           根据 IPv4 地址查找域名           |
| `getservbyname` |             根据服务名查找端口             |
| `getservbyport` |             根据端口查找服务名             |
|  `getaddrinfo`  | 根据域名查找 IP 地址<br>根据服务名查找端口 |
|  `getnameinfo`  | 根据 IP 地址查找域名<br>根据端口查找服务名 |

# 地址

## `gethostbyname` 函数

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



## `gethostbyaddr` 函数

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

## `getservbyname` 函数

TODO

## `getservbyport` 函数

TODO

## `getaddrinfo` 函数

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

## `getnameinfo` 函数

TODO

# 错误

全局变量 `errno` 