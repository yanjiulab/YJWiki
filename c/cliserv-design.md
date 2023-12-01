# 服务器网络编程范式

## IO 密集 vs 计算密集

## 范式

范式|解释
:---:|:---:
one thread per connection|每个连接一个线程
one loop per thread|每个线程一个事件循环
multi-acceptor-processes|多 accept 进程模式
multi-acceptor-threads|多 accept 线程模式
one-acceptor-multi-workers|一个 accept 线程和多 worker 线程

### one thread per connection

为每个连接都分配一个线程，因为每个读写都是阻塞的，因此一个 IO 线程只能处理一个 fd，对于客户端尚可接受，对于服务端来说，主线程执行 accept，每一个并发都分配一个 IO 线程，线程过多将会导致巨大的线程上下文切换开销。

应用举例：基本只存在于教学或测试场景，或者并发极少的场合。

### one loop per thread

每个线程都运行一个事件循环，通过 IO 多路复用机制，一个 IO 线程即可监听多个 fd，以现代计算机性能，可处理几十万数量级的 IO 读写。

尽管使用一个线程即可完成工作，但为了充分利用多核处理器特性，也可以创建多个线程，每个线程一个事件循环。注意多线程不一定比单线程更好，还需要结合业务场景判断。

应用举例：redis 使用了单线程的模型。

### multi-acceptor-processes

每个进程里运行一个事件循环，用于 accept 请求，连接的 fd 将加入多路复用中监听读写事件。

多进程的好处是父进程可以通过捕获 SIGCHLD 信号，知道子进程退出了（通常是由于异常崩溃），可以再重新自动重启该进程。因为进程空间的隔离，因此不会影响其他子进程。

应用举例：ngnix 采用了多进程事件循环模型。

### multi-acceptor-threads

多线程事件循环模型与多进程事件循环模型类似，只不过换成了线程，好处是线程间可以共享数据，不需要每个进程一份资源，但同时也带来了线程间同步问题，需要仔细设计。

### one-acceptor-multi-workers

相对于上述多线程事件循环模型中，accept 和 read/write 都在一个线程中，one-acceptor-multi-workers 模型使用一个线程单独监听accept 连接，当连接到来时，选择一个 work_loop 线程，然后通知该线程有新连接到来。选择的过程可以执行轮询、最少连接数、IP 哈希、URL 哈希等负载均衡策略。

应用举例：memcached。
