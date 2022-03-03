# ioctl



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

