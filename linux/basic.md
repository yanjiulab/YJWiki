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

## 内核

### 用户空间与内核的接口

内核通过各种不同的接口把内部信急输出到用户空hl
- 系统调用
- procfs 这是个虚拟文件系统，通常是挂载到 /proc:，允许内核以文件的形式向用户空间输出内部信息，这些文件并没有实际存在于磁盘中，但是可以通过 cat 以及 > shell 重定向运算符写入。
- sysctl /proc/sys 此接口允许用户空间读取或修改内核变量的值。

ioctl 系统调用
- Netlink 套接字 这是网络应用程序与内核通信时最新的首选机制，IPROUTE2 包中大多数命令都使用此接口。对 Linux 而言，Netlink 代表的就是 BSD 世界中的路由套接字 (routing socket)。


## 内核模块
内核模块 (Kernel Module) 是可以根据需要加载和卸载到内核中的代码段，它们扩展了内核的功能，但无需重新引导系统。

通过运行 `lsmod` 来查看哪些模块已经加载到内核中，该模块通过读取文件 `/proc/modules` 获取其信息。内核模块存储在 `/usr/lib/modules/kernel_release` 或者 `/lib/modules/kernel_release`，可以通过 `uname -r` 获取内核的版本。以下是一些常用的命令：

```
$ lsmod                                 # 查看哪些模块已经加载到内核中
$ modinfo module_name                   # 显示有关模块的信息
$ modprobe -c | less                    # 显示所有模块的完整配置
$ modprobe -c | grep module_name        # 显示特定模块的完整配置
$ modprobe --show-depends module_name   # 列出模块的依赖项（包括模块本身）
```

### 内核模块加载

内核可以通过两种模式加载：

**自动加载**：目前大多数 Linux 发行版，udev 会自动处理所有必需的模块加载，因此不需要特别的进行配置。需要加载的内核模块在 `/etc/modules-load.d/` 下的文件中明确列出，以便 systemd 在引导过程中加载它们。每个配置文件均以 `/etc/modules-load.d/<program>.conf` 的样式命名。

**手动加载**：手动加载/卸载内核模块均需要管理员权限。

- 当需要加载 Linux 内核中的标准内核模块时，通过内核模块守护程序 `kmod` 执行 `modprobe` 来加载/卸载模块。`modprobe` 需要模块名称或模块标识符之一的字符串作为参数。
    ```
    $ modprobe module_name		# 加载标准内核模块
    $ modprobe -r module_name	# 卸载标准内核模块
    ```
- 当需要加载自定义内核模块时，通过 `insmod` 来加载模块，通过 `rmmod` 来卸载模块。
    ```
    $ insmod filename [args]    # 不在标准目录下的内核模块，可以通过文件名加载。
    $ rmmod module_name			# 不在标准目录下的内核模块，可以通过文件名卸载。
    ```

### 内核模块编写

[How to use netlink socket to communicate with a kernel module?](https://stackoverflow.com/questions/3299386/how-to-use-netlink-socket-to-communicate-with-a-kernel-module) 有一份示例代码，包括两部分：

- Kernel module
- User program

其中内核模块程序可以通过以下 Makefile 编译链接，然后通过 `insmod hello.ko` 来载入。

```
obj-m = hello.o
KVERSION = $(shell uname -r)
all:
    make -C /lib/modules/$(KVERSION)/build M=$(PWD) modules
clean:
    make -C /lib/modules/$(KVERSION)/build M=$(PWD) clean
```

## 参考

- [SDN handbook](https://tonydeng.github.io/sdn-handbook/)
- [What is the difference between Unix, Linux, BSD and GNU?](https://unix.stackexchange.com/questions/104714/what-is-the-difference-between-unix-linux-bsd-and-gnu)
- [The Linux Kernel documentation](https://www.kernel.org/doc/html/latest/)
- [Netfilter](https://en.wikipedia.org/wiki/Netfilter)
- [a-deep-dive-into-iptables-and-netfilter-architecture](https://www.digitalocean.com/community/tutorials/a-deep-dive-into-iptables-and-netfilter-architecture)
- [POSIX Threads Programming](https://computing.llnl.gov/tutorials/pthreads/)
- [Introduction to Linux interfaces for virtual networking](https://developers.redhat.com/blog/2018/10/22/introduction-to-linux-interfaces-for-virtual-networking/)
