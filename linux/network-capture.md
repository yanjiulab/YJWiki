# 网络抓包工具

## Tcpdump

```sh
tcpdump [option] [proto] [dir] [type]
[type]: host, net, port, portrange
[dir]: src, dst, src or dst
[proto]: ip, ip6, arp, rarp, tcp, udp,icmp, http, ether, wlan
```

命令|功能
:---:|:---:
–i ethxxx/any|抓接口包
-Q [in/out,inout]
--direction=[]|特定流向数据包
-c 1000|捕获1000个包就退出
ether proto 0x0800|根据以太网协议类型抓包
-w xxx.pcap|输出到文件
-r xxx.pcap|读入文件
-v, -vv, -vvv|控制输出详细程度
-x, -xx|控制输出链路层头部
proto[c]|proto为ether,ip,udp,tcp等协议，c为从协议开始第c个字节，从0开始。例如：tcpdump -i eth1 'ether[5]=0x52' -xx

## Wireshark

过滤命令|功能|说明
:---:|:---:|:---:
proto contains xx:xx|抓取proto协议中包含xx:xx 16进制字节序列的数据包|proto 为协议，xx:xx 为任意字节16进制序列，支持组合查找。例如：eth contains 00:04:04 and eth contains 08:13
