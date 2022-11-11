# Unix 系统编程

本文主要内容来自 APUE。

进程环境

## ================



# 

## 进程启动和终止

进程启动

exec

进程终止

exit

[图 exec 和 exit]

## 命令行参数

int argc, char * argv[]

## 环境表

extern char ** environ --> char *envp[] ---> 多个 char *

环境指针 环境表 环境字符串

[图]

大多数 Liunx 支持：int argc, char *argv[], char *envp[]

ISO 目前使用 environ 变量

## C 程序存储空间布局

[图]

## 共享库

## 存储空间分配

malloc

## 环境变量

getenv

修改不影响父进程

## 拓展

setjump,longjmp 

setrlimit

# 进程控制

## 进程标识

getpid 等函数

## fork

copy on write

linux 新 clone

posix 调用一个调用线程

## exit

## wait

等待子进程

## 竞争条件

信号机制

## exec

多个函数图

## 用户ID组ID

## system

## 进程调度

nice值

# 进程关系

## 终端登录、网络登陆、伪终端

父子关系：进程pid--〉父进程，ppid

## 进程组

- 一个或多个进程的集合，有pgid

- 一个组有一个组长进程，该进程的PGID为PID。

## 会话

- 一个或多个进程组的集合，有sid。

- 会话ID = 会话首进程的进程ID = 会话首进程的进程组ID
- 一个会话有一个控制终端
- 建立与控制终端连接的会话首进程为控制进程。
- 几个进程组可分为：一个前台进程组和若干后台进程组
- 终端键入：ctrl+c，发送到前台进程组所有进程
- 创建会话：进程调用 setsid
  - 不是进程组长：变成新会话首进程，成为新进程组组长进程，pgid为pid
  - 已经是进程组长：出错。如要创建，可以fork然后关闭父进程。

## 作业控制

fg、bg

## shell执行程序

```shell
@sdnhubvm:~/liyj[18:37]$ ps -o pid,ppid,pgid,sid,comm | cat
  PID  PPID  PGID   SID COMMAND
28247 28242 28247 28247 bash
28813 28247 28813 28247 ps
28814 28247 28813 28247 cat
ubuntu@sdnhubvm:~/liyj[18:37]$ ps -o pid,ppid,pgid,sid,comm | cat &
[1] 28876
ubuntu@sdnhubvm:~/liyj[18:38]$   PID  PPID  PGID   SID COMMAND
28247 28242 28247 28247 bash
28875 28247 28875 28247 ps
28876 28247 28875 28247 cat
```

## 孤儿进程

## BSD实现

# 信号

信号=软件中断，处理异步事件

## 信号概念



信号名字 和 signal.h常量

- 列表

信号的产生

- 终端按键
- 硬件异常：除0，内存无效
- 进程调用kill函数发送信号
- 用户使用kill命令
- 某种软件条件发生，需要通知进程产生信号

信号的处理

- 忽略
- 捕捉信号，执行用户函数
- 执行默认动作

可靠性

- 机制
- 可重入

