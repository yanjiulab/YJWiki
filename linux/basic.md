# 基本操作



## 网络

### 网卡



### IP 转发

查看 IP 转发是否开启

```
# cat /proc/sys/net/ipv4/ip_forward
1
```

永久开启 IP 转发
```
# sysctl -w net.ipv4.ip_forward=1
```

### 防火墙

关闭防火墙

```
# service firewalld stop
# systemctl status firewalld.service 
```

