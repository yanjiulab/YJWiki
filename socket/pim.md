# 网络编程笔记

## 处理协议流程

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
