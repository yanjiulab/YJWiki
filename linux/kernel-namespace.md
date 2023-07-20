# 内核隔离 - Namespace

## 命名空间简介

Linux Namespace (名称空间，命名空间) 是 Linux 提供的一种**内核级别环境隔离**的方法。该功能对内核资源进行分区，使得一组进程只能看到一组资源，而另一组进程看到另一组不同的资源。我们可以将 Namespace 视为一个盒子，这些盒子内有一些系统资源，具体含有哪些资源完全取决于盒子（命名空间）的类型。从内核版本 5.6 开始，存在 8 种 Namespace。分别为 `Cgroup`，`IPC`，`Network`，`Mount`，`PID`，`User`，`UTS`，`Time`。其中 Time Namespace 在 2020 年 3 月才被加入，在 Linux 内核 5.6 以上的版本才可以看到。因此在下面的例子中暂不讨论 Time Namespace 这种类型。

每个进程都与一个命名空间相关联，并且进程只能查看或使用与该命名空间以及后代命名空间相关的资源。**在任何给定时刻，任何进程 P 都恰好属于每种 Namespace 类型的一个实例。**这样每个进程（或其进程组）可以在每种类型的资源上拥有自己的视图，且只能查看和操作绑定在此命名空间实例的资源。

我们可以看到一个进程所属的 Namespace 实例是哪些，在典型的 Linux 发行版中，它们以文件的形式存在于 `/proc/$pid/ns` 目录下。

```
$ ls -al /proc/$$/ns
total 0
lrwxrwxrwx 1 liyanjiu liyanjiu 0 6月  27 21:00 cgroup -> 'cgroup:[4026531835]'
lrwxrwxrwx 1 liyanjiu liyanjiu 0 6月  27 21:00 ipc -> 'ipc:[4026531839]'
lrwxrwxrwx 1 liyanjiu liyanjiu 0 6月  27 21:00 mnt -> 'mnt:[4026531840]'
lrwxrwxrwx 1 liyanjiu liyanjiu 0 6月  27 21:00 net -> 'net:[4026531992]'
lrwxrwxrwx 1 liyanjiu liyanjiu 0 6月  27 21:00 pid -> 'pid:[4026531836]'
lrwxrwxrwx 1 liyanjiu liyanjiu 0 6月  27 21:00 user -> 'user:[4026531837]'
lrwxrwxrwx 1 liyanjiu liyanjiu 0 6月  27 21:00 uts -> 'uts:[4026531838]'
```

如果打开第二个终端并运行相同的命令，则应该产生完全相同的输出。这是因为进程必须属于某个名称空间，除非我们明确指定哪个名称空间，否则 Linux 会将其添加为默认名称空间的成员。

## 实现与系统调用

命名空间的实现主要涉及三个系统调用：

- `clone()` – 实现线程的系统调用，用来创建一个新的进程，并可以通过设计上述参数设置命名空间。
- `unshare()` – 使某进程脱离某个 Namespace，加入到新建的 Namespace 中。
- `setns()` – 把某进程加入到某个已存在的 Namespace。

其中 unshare() 函数有一个同名包装命令，因此用起来比较简单，下文中使用 `unshare` 命令来进行实验。

以下是各种命名空间

|              类型              |   中文名称   | unshare 参数 |  clone 参数   |                             功能                             |
| :----------------------------: | :----------: | :----------: | :-----------: | :----------------------------------------------------------: |
| UTS (UNIX Time-sharing System) | 主机名和域名 |      -u      | CLONE_NEWUTS  | 使得子进程有独立的主机名和域名，使得该进程在网络上被视作一个独立的节点，而不仅仅是一个进程。 |
|              User              |   用户和组   |      -U      | CLONE_NEWUSER |        使得子进程有独立的用户和组映射，用于权限管理。        |
|             Mount              |    挂载点    |      -m      |  CLONE_NEWNS  |                 使得子进程有独立的文件系统。                 |
|              PID               |              |              |               |                                                              |


### clone 系统调用

clone() 系统调用的基本用法如下：

```c
/* Prototype for the glibc wrapper function */
#define _GNU_SOURCE
#include <sched.h>

int clone(int (*fn)(void *), void *child_stack,
                int flags, void *arg, ...
                /* pid_t *ptid, void *newtls, pid_t *ctid */ );
```

成功时，调用者的进程中将会返回子进程的 thread ID；失败时返回 -1，子进程将不会被创建，同时将会触发 ERROR。

clone() 创建新进程，其行为类似于 fork()，通常使用 glibc 库中的包装函数 clone()，该函数基于 clone 系统调用。与 fork 不同，clone 允许子进程与父进程共享部分执行上下文的参数，例如虚拟地址空间、文件描述符表、信号处理程序等。

fork 是标准的 Unix 系统调用，用来创建进程，而在 Linux 中 clone 可以根据传递的选项创建不同的执行线程，新的执行线程可以遵循 UNIX 进程、POSIX 线程、介于两者之间或完全不同的事物（例如不同的容器）的语义。`pthread_create()` 和 `fork()` 底层实现都使用了 `clone()`。 

通过 clone() 创建的子进程，从调用指向的函数 fn() 开始执行，而 fork() 创建的子进程将会从 fork 的调用点开始执行。当 fn(arg) 函数返回，子进程结束，函数 fn 的返回值就是子进程的退出状态码，子进程同样可以通过调用 exit() 和收到结束信号而显式结束。

child_stack 参数指定了子进程使用的栈，子进程不可以与父进程共享栈空间，由于绝大部分 Linux 的处理器的栈都是向下生长的，因此该参数需要指向栈顶空间。

flags 的最低字节指定了当子进程结束时需要发送给父进程的结束信号。如果该信号不是 SIGCHLD，则父进程在调用 wait() 等待子进程时必须指定 `__WALL` 或 `__WCLONE` 选项；如果未指定，则子进程退出时父进程将不会收到任何信号。

flags 还可以与零个或多个常量进行按位或运算，以指定在调用进程和子进程之间共享的内容，具体的常量可以查看 man 文档。

### unshare 系统调用

TODO

### setns 系统调用

TODO

## UTS Namespace

### 命令

我们使用 `unshare` 命令在一个新的 Namespace 中运行一个 shell 进程。其中 -u 标志告诉它在新的 `UTS` 命名空间中运行 bash。请注意此时我们的新 bash 进程指向不同的 uts 文件，而其他所有文件都保持不变。

```
$ hostname
Lenovo-XiaoXinPro-13
$ sudo unshare -u bash  # run bash in a new UTS namespace.
$ ls -la /proc/$$/ns
total 0
lrwxrwxrwx 1 root root 0 6月  27 21:07 cgroup -> 'cgroup:[4026531835]'
lrwxrwxrwx 1 root root 0 6月  27 21:07 ipc -> 'ipc:[4026531839]'
lrwxrwxrwx 1 root root 0 6月  27 21:07 mnt -> 'mnt:[4026531840]'
lrwxrwxrwx 1 root root 0 6月  27 21:07 net -> 'net:[4026531992]'
lrwxrwxrwx 1 root root 0 6月  27 21:07 pid -> 'pid:[4026531836]'
lrwxrwxrwx 1 root root 0 6月  27 21:07 user -> 'user:[4026531837]'
lrwxrwxrwx 1 root root 0 6月  27 21:07 uts -> 'uts:[4026533065]'
$ hostname
Lenovo-XiaoXinPro-13
$ hostname container
$ hostname
container
$ exit 
$ hostname  
Lenovo-XiaoXinPro-13
```

我们在新的 UTS Namespace 中设置 hostname 为 container，并且不会影响系统中的任何其他进程。

现在我们来思考一个问题：什么是容器？简而言之，**容器是普通的进程，其具有与其他进程不同的 Namespace**。实际上，容器不必为每种类型都属于唯一的命名空间，它可以共享其中的一些。当 `docker run --net=host redis` 执行时，其实告诉docker 不要为 redis 进程创建新的 Network Namespace，并且如我们所见，Linux 将该进程添加为默认 Network Namespace 的成员，就像其他所有常规进程一样没有任何区别。

那么新的问题来了？如果一个容器，只有一种 Namespace 是私有的，而其余所有的 Namespace 都是和其他进程共享的，那么它还能称之为容器吗？笔者认为这个问题的答案是肯定的，但结果其实并不是那么重要。通常，容器通过 Namespace 实现**隔离 (isolation)** 的概念，进程共享的 Namespace 和资源的数量越少，则进程越隔离，这才是真正重要的。

### 代码实现

```c
#define _GNU_SOURCE
#include <sched.h>
#include <signal.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define STACK_SIZE (1024 * 1024)

static char child_stack[STACK_SIZE];
char* const child_args[] = {
    "/bin/bash",
    NULL};

int child_main(void* args) {
    printf("Now in child process!\n");
    sethostname("container", 12);
    execv(child_args[0], child_args);
    return 1;
}

int main() {
    printf("Program start...\n");
    int child_pid = clone(child_main, child_stack + STACK_SIZE, CLONE_NEWUTS | SIGCHLD, NULL);
    waitpid(child_pid, NULL, 0);
    printf("Already exit!\n");
    return 0;
}
```

程序的输出结果如下：
```
$ gcc ns_uts.c -o ns_uts
$ sudo ./ns_uts 
Program start...
Now in child process!
root@container:/home/liyanjiu/# hostname
container
root@container:/home/liyanjiu/# exit
exit
Already exit!
liyanjiu@Lenovo-XiaoXinPro-13:~$ hostname
Lenovo-XiaoXinPro-13
```

## User Namespace

### 命令

```
$ unshare -U bash
$ id
uid=65534(nobody) gid=65534(nogroup) 组=65534(nogroup)
$ cat /proc/$$/uid_map  # no output
         0          0 4294967295
```

映射并没有带来权限的升级，它仅仅是作为一种子 Namespace 的授权。 

### 代码实现

## Mount Namespace

## PID Namespace

Linux 中的 `/proc` 目录通常用于暴露由 Linux 本身管理的特殊文件系统（称为 `proc` 文件系统）。Linux 使用它来公开有关系统中正在运行的所有进程的信息，以及设备、中断等其他系统信息。每当我们运行诸如 `ps` 之类的命令来访问有关系统中进程的信息时，它都会寻找该文件系统来获取信息。

换句话说，我们需要启动一个 `proc` 文件系统。

PID Namespace 隔离系统中的进程 ID。一种效果是在不同 PID 名称空间中运行的进程可以具有相同的进程 ID，而不会彼此冲突。

## Network namespace

### 命令

使用 `iproute2` 包的 `ip` 命令可以创建 namespace，默认创建在 `/var/run/netns` 下，但实际上可以在任何地方，例如 `docker` 中的 namespace 在 `/var/run/docker/netns`。

```
ip netns add ns1
ip netns add ns2

tree /var/run/netns/
/var/run/netns/
├── ns1
└── ns2
```

创建 namespace 后，我们可以利用 `ip netns exec` 在其中执行一些命令来确认隔离性：

```
ip netns exec ns1 \
        ip address show
```

接下来创建 veth 对，将 namespace 连接起来

```
ip link add veth1 type veth peer name br-veth1
ip link add veth2 type veth peer name br-veth2
s
ip link set veth1 netns ns1
ip link set veth2 netns ns2
```

现在，namespace 具有另外的接口了，请检查它们是否确实存在：
```
ip netns exec ns1 \
        ip address show
```

设置 IP 地址

```
ip netns exec ns1 \
        ip addr add 192.168.1.11/24 dev veth1

ip netns exec ns2 \
        ip addr add 192.168.1.12/24 dev veth2
```

### 代码实现

## 参考

- [Linux Namespace, Wikipedia](https://en.wikipedia.org/wiki/Linux_namespace)
- [A deep dive into Linux namespaces, UTS](http://ifeanyi.co/posts/linux-namespaces-part-1)
- [A deep dive into Linux namespaces, User](http://ifeanyi.co/posts/linux-namespaces-part-2)
- [A deep dive into Linux namespaces, Mount $ PID](http://ifeanyi.co/posts/linux-namespaces-part-3)
- [docker 容器基础技术：linux namespace 简介](https://cizixs.com/2017/08/29/linux-namespace/)

