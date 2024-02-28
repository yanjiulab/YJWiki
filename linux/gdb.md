# GDB

GDB (The GNU Debugger) 是常用的 Linux 调试器。

## 调试文件

对于 C 程序来说，需要在编译时加上 `-g` 参数，保留调试信息，否则不能使用 GDB 进行调试。但如果不是自己编译的程序，并不知道是否带有 `-g` 参数，可以直接启动，然后根据输出来判断是否可调试。

```shell
$ gdb a.out
Reading symbols from a.out...(no debugging symbols found)...done.   # 不可调试。
Reading symbols from a.out...done.                             # 可以调试。
```

## 启动调试

### 调试启动无参程序

最简单的情况是调试一个没有参数的可执行文件，直接启动调试即可。

```shell
$ gdb helloWorld
(gdb)
```

输入 run 命令，即可运行程序。

### 调试带参数程序

调试带参数程序有以下几种方式：

1. 只需要 `run` 的时候带上参数即可。

    ```shell
    $ gdb [program]
    (gdb) run [args1] [args2]
    ....
    ```

2. 使用 `args` 参数，可以在启动 gdb 后设置程序参数和断点后，再正常启动。

    ```shell
    $ gdb [program]
    (gdb) set args [args1] [args2]
    (gdb) b [breakpoint]
    (gdb) run
    ....
    ```

3. 参数启动 gdb，例如 `-q` 是 `a.out` 的参数，使用如下方式启动：

    ```shell
    $ gdb --args ./a.out -q
    ...
    ```

### 调试 core 文件

在 Linux 系统中，如果进程崩溃了，系统内核会捕获到进程崩溃信息，然后将进程的 coredump 信息写入到文件中，能够很大程度上帮助开发者定位问题。可以使用命令 limit -c 查看：

```shell
$ ulimit -c
0
```

结果为 0 表示不生成 coredump 文件。可以进行设置。

```shell
ulimit -c unlimied  # 表示不限制 core 文件大小
ulimit -c 10        # 设置最大大小，单位为块，一块默认为 512 字节
```

coredump 文件的存储路径通过以下命令查看。

```shell
$ cat /proc/sys/kernel/core_pattern
|/usr/share/apport/apport -p%p -s%s -c%c -d%d -P%P -u%u -g%g -- %E
```

Linux 系统中这个文件名默认是 `core`，存储位置与对应的可执行程序在同一目录下，但在 Ubuntu 下 `|` 表示 coredump 文件由后面的脚本接管。可以 `systemctl stop apport.service` 关闭此服务，或者直接重新设置。

```shell
echo  "core-%e-%p-%t" > /proc/sys/kernel/core_pattern
```

可以通过 `kill -3 [pid]` 生成 core 文件。

有了 core 文件后，可以在调试时指定 core 文件调试。

```shell
$ gdb a.out core
(gdb) bt        # 打印错误栈
...
```

### 调试已启动进程

调试已经启动的进程需要首先获取 `ps -ef | grep [appname]` 进程号，假设为 20003。然后使用 `--pid` 参数即可。

```shell
$ gdb --pid 20003
...
```

假设已运行程序没有调试信息，为了节省磁盘空间，已经运行的程序通常没有调试信息。但如果又不能停止当前程序重新启动调试，那怎么办呢？还有办法，那就是同样的代码，再编译出一个带调试信息的版本。然后使用 attach 方式，在 attach 之前，使用 file 命令即可：

```shell
$ gdb
(gdb) file hello
Reading symbols from hello...done.
(gdb) attach 20829
```

## 断点

```shell
(gdb) info breakpoints

(gdb) b test.c:9

(gdb) b printNum

(gdb) break test.c:23 if b==0

(gdb) tbreak test.c:l0  #在第10行设置临时断点

disable  #禁用所有断点
disable bnum #禁用标号为bnum的断点
enable  #启用所有断点
enable bnum #启用标号为bnum的断点
enable delete bnum  #启动标号为bnum的断点，并且在此之后删除该断点

# 断点清除主要用到clear和delete命令。常见使用如下：

clear   #删除当前行所有breakpoints
clear function  #删除函数名为function处的断点
clear filename:function #删除文件filename中函数function处的断点
clear lineNum #删除行号为lineNum处的断点
clear f:lename：lineNum #删除文件filename中行号为lineNum处的断点
delete  #删除所有breakpoints,watchpoints和catchpoints
delete bnum #删除断点号为bnum的断点
```

## 变量查看

GDB 打印时会分配内存，默认为 65536，如果值太大，则打印失败，通过如下命令更改此行为。

```shell
set max-value-size bytes
set max-value-size unlimited
show max-value-size
```

## 单步调试

## 参考

- [在ubuntu中进行core dump调试](https://cloud.tencent.com/developer/article/1559454)
