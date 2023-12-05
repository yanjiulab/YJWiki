# GDB

GDB (The GNU Debugger) 是常用的 Linux 调试器。

## 基本用法

## 高级用法

### 调试进程

调试已经启动的进程使用 `--pid` 参数。

### 调试带参数程序

调试带参数程序需要使用 `args` 参数，可以在启动 gdb 后设置程序参数和断点后，启动。

```sh
gdb [program]
(gdb) set args [args1] [args2]
(gdb) b [breakpoint]
(gdb) run
....
```

或者使用参数启动 gdb，例如 `-q` 是 `a.out` 的参数，使用如下方式启动：

```sh
gdb --args ./a.out -q
```
