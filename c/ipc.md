# 进程间通信整理

## 进程间通信

### IPC 简介

### Unix 共享信息模型

### IPC 对象持久性

### IPC 名字和标识

### POSIX IPC

### 管道

### FIFO

### 消息队列

### 同步（TODO）



进程间通信（Inter Process communication, IPC）具有两种基本方式：

- **消息传递（Message Passing）**：不同进程之间通过传递消息来获取信息。
    - 匿名管道 (Anonymous pipe)
    - 命名管道 (Named pipe)
    - 信号 (Signal)
    - 消息队列 (Message queue)
        - POISX
        - System V
    - 网络套接字 (Socket)  
    - Unix 域套接字 (Unix domain socket)、
    - 远程过程调用 (Remote Process Calls, RPCs)
- **同步（Synchronization）**：不同进程之间通过共享对象来获取信息。
    - 共享内存 (Shared memory)
    - 内存映射文件 (Memory-mapped file)

Synchronization

- System V semaphore
- Posix semaphore
- Mutexes and Conditional variable
- Read-write locks


| 方法                                                     | 简述                                                         | 特点                                                         | 适用场景 |
| -------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | -------- |
| 文件 (File)                                              | 存储在磁盘或文件服务器上的记录，可以由多个进程访问。         |                                                              |          |
| 匿名管道 (Anonymous pipe)                                | 使用标准输入和输出构建的单向数据通道，写入管道的写入端的数据由操作系统缓冲在内存，直到从管道的读取端读取数据为止。通过使用相反“方向”上的两个管道可以实现过程之间的双向通信。 | 只能用于父子进程或者兄弟进程之间。                           |          |
| 命名管道 (Named pipe)                                    | 与匿名管道使用标准输入输出进行读写不同，命名管道的读写就像常规文件。 |                                                              |          |
| 信号 (Signal)<br>异步系统陷入 (Asynchronous System Trap) | 从一个进程发送到另一个进程的系统消息，通常不用于传输数据，而是用于远程命令伙伴进程。 | 信号是软件层次上对中断机制的一种模拟，是一种异步通信方式，   |          |
| 消息队列 (Message queue)                                 |                                                              |                                                              |          |
| 套接字 (Socket)                                          |                                                              |                                                              |          |
| Unix 域套接字 (Unix domain socket)                       |                                                              |                                                              |          |
| 共享内存 (Shared memory)                                 | 多个进程被授予对同一块内存的访问权限，该内存块创建了一个共享缓冲区，以使进程之间可以相互通信。 | 由于多个进程共享一段内存，因此需要依靠某种同步机制（如信号量）来达到进程间的同步及互斥。 |          |
| 消息传递 (Message passing)                               |                                                              |                                                              |          |
| 内存映射文件 (Memory-mapped file)                        | 映射到 RAM 的文件，可以通过直接更改内存地址而不是输出到流来修改。这具有与标准文件相同的好处。 |                                                              |          |

## Processes, Threads, and the Sharing of Information

三种共享信息的方式
![share-information](share-information.png)

1. 左侧的两个进程正在**共享驻留在文件系统文件中的某些信息**。要访问此数据，每个进程都**必须经过内核**（读、写等），在更新文件时，**需要某种形式的同步**，既可以保护多个编写者彼此之间，又可以保护一个或多个读取者免受编写者的侵害。
2. 中间的两个进程共享一些驻留在内核中的信息。管道是这种共享类型的一个示例，System V 消息队列和 System V 信号量也是如此。访问共享信息的每个操作都**涉及对内核的系统调用**。
3. 右侧的两个进程具有每个进程可以引用的共享内存区域。一旦每个进程设置了共享内存，这些进程就可以访问共享内存中的数据，而完全**不需要内核**。共享内存的进程**需要某种形式的同步**。

{% note info %}
以上所有的 IPC 技术都不止局限于两个进程。
{% endnote %}

尽管 Unix 系统中的进程概念已经使用了很长时间，但是给定进程中的多个线程的概念相对较新。Posix.1 线程标准（称为Pthreads）于 1995 年获得批准。从 IPC 的角度来看，同一进程中的所有线程共享相同的全局变量，这使得共享内存的概念称为线程模型的固有属性，正因如此，多个线程访问这些全局变量必须使用同步手段，事实上，同步虽然不是明确的 IPC 形式，但与许多形式的 IPC 一起使用来控制对某些共享数据的访问。

IPC 对象的持久化

| 持久化方式                | 生存周期                                  |
| ------------------------- | ----------------------------------------- |
| process-persistent IPC    | 直到打开 IPC 对象的最后一个进程关闭该对象 |
| kernel-persistent IPC     | 直到内核重启或 IPC 对象被显式删除         |
| filesystem-persistent IPC | 直到 IPC 对象被显式删除。                 |

> 没有任何一种 IPC 是使用文件系统持久化的，但确实是有一些 IPC 依赖于文件系统的实现。文件提供了文件系统的持久化属性，但 IPC 通常不使用这种方式，大多数 IPC 对象在内核重启之后就会消失，这是因为进程在重启之后也会消失，进程都消失了，IPC 也失去了意义。同时，使用文件系统持久化可能会降低 IPC 的性能，然而 IPC 的设计目标就是高性能，否则为何不直接使用文件进行信息传递呢？


## 命名空间 (Name Space)

当不相关的进程使用 IPC 交换信息时，IPC 对象必须具有某种形式的**名称或标识符**，这样一个进程可以创建 IPC 对象，而其他进程可以定位到相同的 IPC 对象。**某种类型的 IPC 所有可能的名字集合称为它的命名空间**。

When two unrelated processes use some type of IPC to exchange information between
themselves; the IPC object must have a name or identifier of some form so that one
process (often a server)can create the IPC object and other processes (oftenone or more
clients) can specify that same IPC object.

## 例子

1. File server
2. Producer-consumer
3. Sequence-number-increment

## 总结

IPC 分为四种主要的方式:

1. message passing (pipes, FIFOs, message queues),
2. synchronization(mutexes, condition variables, read-write locks, semaphores),
3. shared memory (anonymous, named)
4. procedure calls (Solaris doors, Sun RPC)

IPC 的持久化方式有：进程持久化、内核持久化、文件系统持久化。

IPC 通过自己的命名空间来标识 IPC 对象，以便该对象被其他进程和线程所使用。

- 一些没有名字
- 一些使用文件系统中的名字
- 其他类型的名字


# IPC 分类

## Posix IPC

## System V IPC

# Message Passing

## Pipes and FIFOs

p 73

## Posix Message Queues

p126

## System V Message Queues

p155

# Synchronization

## Mutexes and Conditional

p174

## Read-Write Locks

p192

## Record Locking

p216

## Posix Semaphores

p278

## System V Semaphores

p300

# Shared Memory

p322

## Posix Shared Memory

p342

## System V Shared Memory

p351

# 管道

# 消息队列

**消息队列 (Message Queue)是存储在内核中并由消息队列标识符标识的消息的链接表**。以下消息队列简称队列，消息队列标识符简称队列 ID。

msgget()|创建一个新队列
ftok()|用于产生一个唯一的键
msgget()|创建一个新队列或打开一个现有队列，返回其队列 ID。
msgsnd()|将新消息添加到队列尾端。
msgrcv()|从队列中取出消息，不一定以 FIFO 的方式取消息，也可以按消息队类型字段取消息。
msgctl()|对队列执行多种操作，主要用于销毁队列。

# 共享内存


# 参考

- UNIX Network Programming - volume 2 IPC, by Richard Stevens
- [IPC using Message Queues](https://www.geeksforgeeks.org/ipc-using-message-queues/)
- [How do I read a string entered by the user in C?](https://stackoverflow.com/questions/4023895/how-do-i-read-a-string-entered-by-the-user-in-c)
- 