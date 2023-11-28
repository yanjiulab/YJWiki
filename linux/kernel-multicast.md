# Linux 组播

Linux 内核和组播相关的代码：

- `ipmr.c (net/ipv4/ipmr.c)`
- `mroute.h (include/linux/mroute.h)`

## 内核组播表 - MFC

### 信息查看

Linux 内核 MFC (Multicast Forwarding Cache) 存储了组播转发表，通过如下命令可以查看相关表项和接口信息。

```sh
# Check Linux kernel multicast interfaces:
cat /proc/net/dev_mcast

# Check that interface eth0 is forwarding multicast:
cat /proc/sys/net/ipv4/conf/eth0/mc_forwarding

# Check Linux kernel multicast VIFs:
cat /proc/net/ip_mr_vif
Interface      BytesIn  PktsIn  BytesOut PktsOut Flags Local    Remote

# Check Linux kernel MFC:
# Oifs format = vifi:TTL
cat /proc/net/ip_mr_cache
Group    Origin   Iif     Pkts    Bytes    Wrong Oifs

# iproute2 can display the MFC:
ip mroute show
(2.2.2.2, 239.2.2.2)             Iif: eth1       Oifs: eth0

# Display igmp information
cat /proc/net/igmp
Idx     Device    : Count Querier       Group    Users Timer    Reporter
```

## 内核

```c
struct vif_device {
    /* Device we are using */
    struct net_device* dev;

    /* Statistics */
    unsigned long bytes_in, bytes_out;
    unsigned long pkt_in, pkt_out;

    /* Traffic shaping (NI) */
    unsigned long rate_limit;

    /* TTL threshold */
    unsigned char threshold;

    /* Control flags */
    unsigned short flags;

    /* Addresses(remote for tunnels)*/
    __u32 local, remote;

    /* Physical interface index */
    int link;
};

struct mfc_cache {
    /* Next entry on cache line */
    struct mfc_cache* next;

    /* Group the entry belongs to */
    __u32 mfc_mcastgrp;

    /* Source of packet */
    __u32 mfc_origin;

    /* Source interface */
    vifi_t mfc_parent;

    /* Flags on line */
    int mfc_flags;

    union {
        struct {
            unsigned long expires;
            /* Unresolved buffers    */
            struct sk_buff_head unresolved;
        } unres;
        struct {
            unsigned long last_assert;
            int minvif;
            int maxvif;
            unsigned long bytes;
            unsigned long pkt;
            unsigned long wrong_if;
            /* TTL thresholds */
            unsigned char ttls[MAXVIFS];
        } res;
    } mfc_un;
};
```

其中，ttls[MAXVIFS] 数组的值与 vif_table[MAXVIFS] 数组的值是一一对应的，即每个表项都与所有的接口关联。当 IP 包来临时，使用 IP 头中的 TTL 字段进行匹配，来决定是否从该出口转发。

在 `ipmr.c` 中主要用到了三个变量：

- vif 表
- MFC 缓存表
- MFC 未解析队列

```c
/* Devices              */
static struct vif_device vif_table[MAXVIFS];
/* Forwarding cache     */
static struct mfc_cache *mfc_cache_array[MFC_LINES];
/* Queue of unresolved entries */
static struct mfc_cache *mfc_unres_queue;
```

下面介绍内核是如何对这些结构进行管理的。内核中所有的实现都集中于 `ipmr.c` 文件中，内核并不实现路由协议本身，而是供路由协议（例如 pimd 等）调用来管理数据结构。简而言之，每当路由程序要添加或删除路由表项时，它只需向内核发送一条消息来指定相应的操作。为了实现该功能，路由程序必须能够接收
IGMP 数据包，这样 IGMP 包才能够通过内核传递到用户空间中。

路由程序有两种方式可以与内核进行通信：

- `ioctl()` 系统调用
- `setsockopt()` 系统调用

以 pimd 路由程序为例，

```c
struct mfcctl {
    /* Origin of mcast    */
    struct in_addr mfcc_origin;

    /* Group in question    */
    struct in_addr mfcc_mcastgrp;

    /* Where it arrived    */
    vifi_t mfcc_parent;
f
    /* Where it is going    */
    unsigned char mfcc_ttls[MAXVIFS];

    /* pkt count for src-grp */
    unsigned int mfcc_pkt_cnt;
    unsigned int mfcc_byte_cnt;
    unsigned int mfcc_wrong_if;
    int mfcc_expire;
};
```

路由程序使用 `k_chg_mfc()` 函数来向内核下发 MFC， 在 mfcctl 中，mfcc_ttls[MAXVIFS] 数组同 mfc_cache 中 ttls[MAXVIFS] 含义类似，如果需要从该端口转发数据，则将其设为实际接口的 threshold 值，否则设为 0。当内核收到一条 MFC 添加请求时，内核通过 `ipmr_mfc_add()` 函数处理，该函数首先检查是否存在该表项，如果存在则更新其 TTL 的值。如果不存在，则新分配空间存储到 MFC 中。当上述过程完成后，内核还需要转发暂存在 mfc_unres_queue 队列中所有的组播数据。

路由程序使用 `k_del_mfc()` 函数来从内核删除 MFC，当内核收到一条 MFC 删除请求时，内核模式调用 `impr_mfc_delete()` 函数从 MFC 中删除指定的表项。

内核还支持通过 Netfilter 机制注册用户回调函数，使得 MCF 添加、更新、删除时可以插入用户代码。回调函数如下

```c
typedef void nf_nfy_msg(
    unsigned int hook,
    unsigned int msgno,
    const struct net_device* dev,
    void* moreData);
```

```c
#ifdef NF_EVT_HOOK && NF_MCAST_HOOK
    NF_NFY_HOOK(
        PF_INET,
        NF_NFY_IP_MCAST_MSG,
        IPMR_MFC_ADD,
        NULL,
        (void*) c);
#endif
```

其中：hook 为 AF_INET，msgno 表示内核的动作，例如添加 mfc_entry。dev 为当前流程涉及到的网络设备。



## 参考

- [Multicast Routing Code in the Linux Kernel](https://www.linuxjournal.com/article/6070)
