# Unix 系统编程

本文主要内容来自 APUE。

## Unix 基础

### Unix 简介

自 1969 年成立开始，Unix 系统便迅速流行，因为它为各种不同硬件架构的机器**提供了统一的运行环境**。Unix 系统分为两部分，一部分是**程序 (programs) 和服务 (services)** ,它们是供用户使用的，包括 Shell，邮件，文字处理包，源码控制系统等。另一部分是支持这些程序和服务的**操作系统**。

- 1965 年，Bell Telephone Laboratory，通用电气公司以及 MIT 的 MAC计划小组共同开发了 **Multics** 这个新的操作系统。
- Multics 系统的原始版本确实在 GE 645 机器上运行，但因为没有提供预期统一计算服务，再加上发展目标不明确，因此，贝尔实验室结束了对该项目的支持。
- 贝尔实验室的科学家们打算改进它们自己的编程环境，于是，Ken Thompson, Dennis Ritchie 等人起草了一份文件系统 (file system) 设计的白皮书，后来推动了早期 Unix 文件系统的发展。后来再加上进程子系统和一些工具，Unix 就这样诞生了。其名称是相对于 Multics 的复杂而取的，**暗含了 Unix 系统的精简**。
- 第一版使用汇编语言和 B 语言写成。Ritchie 改进了 B 语言，创造了 C 语言，用来生成机器码，声明数据类型，定义数据结构。1973 年，**系统用 C 语言重写**。
- 1974年，汤普逊和里奇合作在 ACM 通信上发表了一篇关于 UNIX 的文章，这是 **UNIX 第一次出现在贝尔实验室以外**。
- 1982年，贝尔实验室综合了 AT&T 开发的中多版本，形成了 **UNIX System Ⅲ**，不久有增加了一些新功能，重新命名为 **UNIX System V**，然而，加州大学伯克利分校开发了 **BSD 4.3**，其作为 UNIX System III 和 V 的替代选择。

![unix-timeline](apue.assets/unix-timeline.svg)

### Unix 系统结构

Unix 将系统视为若干层，其中**内核** (operating system, system kernel or just kernel) 直接与硬件交互，为上层程序提供通用服务并将它们与硬件特性隔离开来。

![Architecture of UNIX Systems](apue.assets/system-structure.png)

其中，系统从底层至高层分别为：

- 内核：操作系统的灵魂及核心。
- 低层程序（low-level）：通过系统调用 (system call) 与内核交互，这些程序包括 shell `sh` 和 editor `vi`，标准系统配置命令 (commands)，以及 `a.out` 这种由 C 编译器生成的可执行文件。
- 应用程序（high-level）：通过对低层程序调用与组合，为用户提供了更好的界面和操作，同时简化了开发。

所有的操作系统都提供多种服务的入口点，由此程序向内核请求服务。各种版本的 Unix 实现都提供良好定义、数量有限、直接进入内核的入口点，这些入口点被称为**系统调用 (system call)**。不同的系统提供了不同的几十、上百个系统调用，具体数字在不同操作系统版本中会不同，

系统调用接口是用 C 语言定义的，Unix 所使用的技术是为每个系统调用在标准 C 库中设置一个具有同样名字的**包装函数**。用户进程用标准 C 代码来调用这些函数，然后这些函数又用系统所要求的技术调用相应的内核服务。

![image-20221111172301732](apue.assets/image-20221111172301732.png)

程序员可以使用的通用库函数在内部实现时可能会调用一个或多个内核的系统调用，但是它们并不是内核的入口点。同时，库函数当然也可以不使用任何内核的系统调用，这样的库函数仅仅是一些标准库为我们准备的用户层面代码而已。因此，系统调用通常提供一种最小接口，而库函数通常提供比较复杂的功能。

实际上，对于用户而言，库函数和系统调用无需区分，都当做底层编程接口即可。例如，进程控制系统调用 (fork, exec 和 wait) 通常由用户应用程序直接调用，然而内存分配系统调用 sbrk 却鲜被直接使用，通常程序员会使用功能更加丰富的 malloc 库函数，而后者的实现中使用了 sbrk 系统调用。但是，我们应当理解库函数可以被替换，系统调用通常是不能被替换的。

### 编程接口

在使用 C 语言编程实现某个功能时候，需要使用操作系统提供的编程接口，Unix 系统提供了如下库供用户使用，包括：

- C 标准库
- 其他库
    - POSIX (Portable Operating System Interface of Unix)
    - Linux Library
    - Windows Library
    - …

编程时首先考虑使用 C 标准库中的接口，这些库保证了最佳的可移植性。C POSIX 库是与标准库同时发展的，它是 POSIX 系统中 C 标准库的规范，作为标准库的超集，其不仅兼容标准库，同时还引入了额外的功能。虽然 POSIX 是为 Unix 标准制定的接口，但对于 Linux、Mac OS X 系统，甚至 Windows 都具有较好的可移植性。

除此之外，最后考虑 Linux 库以及 Windows 库等，除非你确定编写的程序不需要跨平台使用。由于大部分时候我们的代码将会运行在 Linux 内核的机器上，因此有时候想要用到 Linux 内核相关功能，而 POSIX 标准没有涵盖这个接口的话，将不可避免的使用到 Linux 提供的相关库。

- GNU/Linux 是 POSIX 兼容的系统，其使用了 GNU C Library (glibc) 的实现，该实现兼容 C 标准库、POSIX 库等，可以使用 man 手册查阅相关 C 库用法。
- Windows 有自己的头文件，可以在 MSDN 中找到，但也有 POSIX 兼容的版本，例如 Cygwin, MinGW 等。

[List of standard header files in C and C++](https://stackoverflow.com/questions/2027991/list-of-standard-header-files-in-c-and-c) 有一份详细的目录可以帮助你了解这些头文件。

### ISO C - 标准库

**C 标准库也称为 ISO C 库**，主要经历了 C89, C99, C11 三个大版本，目前包括 **31** 个头文件。详细说明可以在 [C Standard Library header files](https://en.cppreference.com/w/c/header) 进行查阅。

|         头文件          |                             说明                             |
| :---------------------: | :----------------------------------------------------------: |
|      `<assert.h>`       | [Conditionally compiled macro that compares its argument to zero](https://en.cppreference.com/w/c/error) |
|   `<complex.h>` (C99)   | [Complex number arithmetic](https://en.cppreference.com/w/c/numeric/complex) |
|       `<ctype.h>`       | [Functions to determine the type contained in character data](https://en.cppreference.com/w/c/string/byte) |
|       `<errno.h>`       | [Macros reporting error conditions](https://en.cppreference.com/w/c/error) |
|    `<fenv.h>` (C99)     | [Floating-point environment](https://en.cppreference.com/w/c/numeric/fenv) |
|       `<float.h>`       | [Limits of floating-point types](https://en.cppreference.com/w/c/types/limits#Limits_of_floating_point_types) |
|  `<inttypes.h>` (C99)   | [Format conversion of integer types](https://en.cppreference.com/w/c/types/integer) |
|   `<iso646.h>` (C95)    | [Alternative operator spellings](https://en.cppreference.com/w/c/language/operator_alternative) |
|      `<limits.h>`       | [Ranges of integer types](https://en.cppreference.com/w/c/types/limits) |
|      `<locale.h>`       | [Localization utilities](https://en.cppreference.com/w/c/locale) |
|       `<math.h>`        | [Common mathematics functions](https://en.cppreference.com/w/c/numeric/math) |
|      `<setjmp.h>`       |  [Nonlocal jumps](https://en.cppreference.com/w/c/program)   |
|      `<signal.h>`       |  [Signal handling](https://en.cppreference.com/w/c/program)  |
|  `<stdalign.h>` (C11)   | [`alignas` and `alignof`](https://en.cppreference.com/w/c/types) convenience macros |
|      `<stdarg.h>`       | [Variable arguments](https://en.cppreference.com/w/c/variadic) |
|  `<stdatomic.h>` (C11)  | [Atomic operations](https://en.cppreference.com/w/c/thread#Atomic_operations) |
|   `<stdbit.h>` (C23)    | Macros to work with the byte and bit representations of types |
|   `<stdbool.h>` (C99)   | [Macros for boolean type](https://en.cppreference.com/w/c/types) |
|  `<stdckdint.h>` (C23)  |       macros for performing checked integer arithmetic       |
|      `<stddef.h>`       | [Common macro definitions](https://en.cppreference.com/w/c/types) |
|   `<stdint.h>` (C99)    | [Fixed-width integer types](https://en.cppreference.com/w/c/types/integer) |
|       `<stdio.h>`       |      [Input/output](https://en.cppreference.com/w/c/io)      |
|      `<stdlib.h>`       | General utilities: [memory management](https://en.cppreference.com/w/c/memory), [program utilities](https://en.cppreference.com/w/c/program), [string conversions](https://en.cppreference.com/w/c/string), [random numbers](https://en.cppreference.com/w/c/numeric/random), [algorithms](https://en.cppreference.com/w/c/algorithm) |
| `<stdnoreturn.h>` (C11) | [`noreturn`](https://en.cppreference.com/w/c/language/_Noreturn) convenience macro |
|      `<string.h>`       | [String handling](https://en.cppreference.com/w/c/string/byte) |
|   `<tgmath.h>` (C99)    | [Type-generic math](https://en.cppreference.com/w/c/numeric/tgmath) (macros wrapping math.h and complex.h) |
|   `<threads.h>` (C11)   |   [Thread library](https://en.cppreference.com/w/c/thread)   |
|       `<time.h>`        | [Time/date utilities](https://en.cppreference.com/w/c/chrono) |
|    `<uchar.h>` (C11)    | [UTF-16 and UTF-32 character utilities](https://en.cppreference.com/w/c/string/multibyte) |
|    `<wchar.h>` (C95)    | [Extended multibyte and wide character utilities](https://en.cppreference.com/w/c/string/wide) |
|   `<wctype.h>` (C95)    | [Functions to determine the type contained in wide character data](https://en.cppreference.com/w/c/string/wide) |

### IEEE POSIX

IEEE POSIX 标准定义了接口的规范，而不同的操作系统根据自身平台的特征实现了这些接口。目前包括 **82** 个头文件（包含所有 C99 头文件），头文件详细说明可以在 [IEEE and The Open Group](http://pubs.opengroup.org/onlinepubs/9699919799/nframe.html) 网站中的 [IEEE Std POSIX.1-2017](http://pubs.opengroup.org/onlinepubs/9699919799/toc.htm) 进行查询。

|      头文件      | 说明 |
| :--------------: | :--: |
|     <aio.h>      |      |
|  <arpa/inet.h>   |      |
|    <assert.h>    |      |
|   <complex.h>    |      |
|     <cpio.h>     |      |
|    <ctype.h>     |      |
|    <dirent.h>    |      |
|    <dlfcn.h>     |      |
|    <errno.h>     |      |
|    <fcntl.h>     |      |
|     <fenv.h>     |      |
|    <float.h>     |      |
|    <fmtmsg.h>    |      |
|   <fnmatch.h>    |      |
|     <ftw.h>      |      |
|     <glob.h>     |      |
|     <grp.h>      |      |
|    <iconv.h>     |      |
|   <inttypes.h>   |      |
|    <iso646.h>    |      |
|   <langinfo.h>   |      |
|    <libgen.h>    |      |
|    <limits.h>    |      |
|    <locale.h>    |      |
|     <math.h>     |      |
|   <monetary.h>   |      |
|    <mqueue.h>    |      |
|     <ndbm.h>     |      |
|    <net/if.h>    |      |
|    <netdb.h>     |      |
|  <netinet/in.h>  |      |
| <netinet/tcp.h>  |      |
|   <nl_types.h>   |      |
|     <poll.h>     |      |
|   <pthread.h>    |      |
|     <pwd.h>      |      |
|    <regex.h>     |      |
|    <sched.h>     |      |
|    <search.h>    |      |
|  <semaphore.h>   |      |
|    <setjmp.h>    |      |
|    <signal.h>    |      |
|    <spawn.h>     |      |
|    <stdarg.h>    |      |
|   <stdbool.h>    |      |
|    <stddef.h>    |      |
|    <stdint.h>    |      |
|    <stdio.h>     |      |
|    <stdlib.h>    |      |
|    <string.h>    |      |
|   <strings.h>    |      |
|   <stropts.h>    |      |
|   <sys/ipc.h>    |      |
|   <sys/mman.h>   |      |
|   <sys/msg.h>    |      |
| <sys/resource.h> |      |
|  <sys/select.h>  |      |
|   <sys/sem.h>    |      |
|   <sys/shm.h>    |      |
|  <sys/socket.h>  |      |
|   <sys/stat.h>   |      |
| <sys/statvfs.h>  |      |
|   <sys/time.h>   |      |
|  <sys/times.h>   |      |
|  <sys/types.h>   |      |
|   <sys/uio.h>    |      |
|    <sys/un.h>    |      |
| <sys/utsname.h>  |      |
|   <sys/wait.h>   |      |
|    <syslog.h>    |      |
|     <tar.h>      |      |
|   <termios.h>    |      |
|    <tgmath.h>    |      |
|     <time.h>     |      |
|    <trace.h>     |      |
|    <ulimit.h>    |      |
|    <unistd.h>    |      |
|    <utime.h>     |      |
|    <utmpx.h>     |      |
|    <wchar.h>     |      |
|    <wctype.h>    |      |
|   <wordexp.h>    |      |



### 系统重要文件

TODO

| 文件 | 说明 |
| ---- | ---- |
|      |      |
|      |      |
|      |      |

### 基本系统数据类型

TODO

| 类型      | 说明 |
| --------- | ---- |
| `clock_t` |      |
|           |      |
|           |      |

## 文件

Unix 中一切皆文件。 这是很有趣的哲学，意味着**文件 (file)**这一模型，提供了对所有 I/O 资源访问的抽象，包括文档、目录、磁盘、CD-ROM、调制解调器、键盘、打印机、显示器和终端等等，甚至也包括了进程、网络之间的通信。所有文件都通过一致的 API 以提供访问，因此只用同一套简单的命令，就可以读写磁盘、键盘、文档以及网络设备。

### 文件描述符

对于 Linux 而言，所有的文件都通过文件描述符引用。文件描述符是一个非负整数，当打开或创建一个文件时，内核向进程返回一个文件描述符。

### 文件类型

Unix 文件大部分是普通文件和目录，但也包括其他类型。

|              文件类型               |                   说明                   |
| :---------------------------------: | :--------------------------------------: |
|        普通文件 regular file        |           主要包括文本和二进制           |
|         目录 directory file         | 包含其他文件的名字以及指向这些文件的指针 |
| 字符特殊文件 character special file |             带缓冲访问的设备             |
|    块特殊文件 block special file    |            不带缓冲访问的设备            |
|          FIFO pipe or FIFO          |              进程间通信文件              |
|       符号链接 symbolic file        |              指向另一个文件              |
|            套接字 socket            |              网络进程间通信              |

TODO 

stat 函数

`stat /etc/passwd /etc /run/systemd/journal/dev-log  /dev/tty /dev/sr0 /dev/cdrom | grep -E 'File|Size'` 可以查看各类文件类型 。

### 文件系统



### 文件存储结构

内核使用三种数据结构来表示打开的文件：

1. Every process has an entry in the **process table**. Associated with each file descriptor are
    - The file descriptor flags
    - A pointer to a **file table entry**
2. The kernel maintains a file table for all open files. Each file table entry contains
    - The file status flags for the file, such as read, write, append, sync, and nonblocking
    - The current file offset
    - A pointer to the **v-node table entry** for the file
3. 

### 文件所属及权限

access

umask

chmod

chown

### 文件时间

### 符号链接

### 目录

### 设备特殊文件

## 文件 I/O

| 函数名    | 说明                           | 函数体                                                       | Header     | Return                                              |
| --------- | ------------------------------ | ------------------------------------------------------------ | ---------- | --------------------------------------------------- |
| **open**  | 打开或创建一个文件             | int open(const char *path, int oflag, ... /* mode_t mode */ ); | <fcntl.h>  | fd or -1                                            |
| openat    |                                | int openat(int fd, const char *path, int oflag, ... /* mode_t mode */ ); | <fcntl.h>  | fd or -1                                            |
| creat     | 创建一个文件（不推荐使用）     | int creat(const char* **path, mode_t mode);                  | <fcntl.h>  | fd or -1                                            |
| **close** | 关闭一个打开文件               | int close(int fd);                                           | <unistd.h> | 0 or -1                                             |
| **lseek** | 显式地为一个打开文件设置偏移量 | off_t lseek(int fd, off_t offset, int whence);               | <unistd.h> | offset or -1                                        |
| **read**  | 从打开文件中读数据             | ssize_t read(int fd, void *buf, size_t nbytes);              | <unistd.h> | number of bytes read, 0 if end of file, −1 on error |
| **write** | 向打开文件中写数据             | ssize_t write(int fd, const void *buf, size_t nbytes);       | unistd.h   | number of bytes written if OK, −1 on error          |



| 系统函数  | 描述                                         | 头文件                                                   |
| --------- | -------------------------------------------- | -------------------------------------------------------- |
| dup2      | 复制一个现有的文件描述符                     | <unistd.h>                                               |
| sync      | 保证磁盘上实际文件系统与缓冲区中内容的一致性 | <unistd.h>                                               |
| dup       | 复制一个现有的文件描述符                     | <unistd.h>                                               |
| fsync     | 保证磁盘上实际文件系统与缓冲区中内容的一致性 | <unistd.h>                                               |
| fdatasync | 保证磁盘上实际文件系统与缓冲区中内容的一致性 | <unistd.h>                                               |
| fcntl     | 改变己经打开文件的属性                       | <fcntl.h>                                                |
| ioctl     | I/O操作的杂货箱                              | <unistd.h> in System V <br><sys/ioctl.h> in BSD or Linux |



## 标准 I/O

### 格式化 I/O 输入

C 语言的输入函数家族主要包括三个函数，其区别在于**输入源**不同，分别是

- `scanf`：从标准输入流 `stdin` 读入。
- `fscanf`：从文件流指针 `steam` 读入。
- `sscanf`：从字符串指针 `str` 读入。 

```c
#include <stdio.h>
int scanf(const char *format, ...);
int fscanf(FILE *stream, const char *format, ...);
int sscanf(const char *str, const char *format, ...);
```

输入函数主要构成参数为**格式化字符串**以及**可变参数列表**。其中，格式化字符串包括一系列指令，输入函数将会按照指令的规则来解析输入，并将结果按照顺序存入到指针参数指向的变量中。

实际上，输入函数简单易用。然而，格式化字符串的内容才是其精髓，通过精妙的组合可以实现许多效果。

**格式化字符串**包括一系列**指令**，它们有：

- 一串空白字符：包括空格、换行、制表符等，它们可以匹配输入源中任意数量的空白字符。
- **转换格式符**：由 `%` 开头的字符，将会按照格式匹配输入源，并将结果存储到对应的变量中。
- 常规字符： 除了以上两种字符以外常规的字符，必须精确匹配输入中对应的字符。

因此，输入函数族的处理过程大致如下：

1. 从输入源的第一个位置，尝试匹配第一个指令，如果匹配成功，则进行下一个指令匹配，如果匹配失败，则函数返回。
2. 由于前一个指令已经“消耗了”一定的输入，因此下一个指令将继续匹配剩余输入源。
3. 如果输入不够或者错误，则引发 `input failure` 退出；如果匹配错误，则引发 `match failure` 退出；如果匹配完毕，则函数返回成功匹配的个数。

> 实际上，输入输出真正复杂多变的地方在于转换格式符的规则，详细内容请查阅 man 手册，此文不再一一列出。

**转换说明符**是 `%` 后面的字符，以下是两个不常用但十分有用的说明符号。常用的说明符在示例程序中有展示，不再赘述。

- `%n`：返回到目前为止，匹配消耗的输入字符数，并存储到下一个变量中，该变量类型必须为 int。
- `%[`：匹配一系列非空字符，且字符必须属于方括号集合，如果第一个字符为 `^` 则表示除此之外任何字符。对于如果字符间有 `-` 则表示两字符间所有字符，如果要匹配字符 `]` 或 `-` 本身，则字符 `]` 必须位于 `[` 或 `^`之后，`-`必须位于最后一个，`%[^]0-9-]` 表示匹配除了 `[`、数字 `0` - `9` 以及 `-` 之外所有字符。

以下是标准输入读取示例：

`%[]`：匹配一系列非空字符，且字符必须属于方括号集合，如果第一个字符为 `^` 则表示除此之外任何字符。对于如果字符间有 `-` 则表示两字符间所有字符，如果要匹配字符 `]` 或 `-` 本身，则字符 `]` 必须位于 `[` 或 `^`之后，`-`必须位于最后一个，`%[^]0-9-]` 表示匹配除了 `[`、数字 `0` - `9` 以及 `-` 之外所有字符。

```c
char* p;
int n;
n = scanf("%m[^]0-9-]", &p);
if (n == 1) {
    printf("read: %s\n", p);
    free(p);
} else {
    fprintf(stderr, "No matching characters\n");
}
```

以下是文件读取读取示例：

```c
#include <stdio.h>

int main()
{
    int i;
    unsigned int u;
    unsigned int x;
    float f;
    double lf;
    char s[10] = { '\0' };
    char str[128] = { '\0' };

    FILE* fp = fopen("value.txt", "r");
    int len = fscanf(fp, "%i %u %x %f %s %lf %[^\n]", &i, &u, &x, &f, s, &lf, str);
    printf("len: %d\n", len);
    printf("data: %i %u %x %f %s %lf %s\n", i, u, x, f, s, lf, str);
}
```

以下是字符串读取示例：

`%n`：返回到目前为止，匹配消耗的输入字符数，并存储到下一个变量中，该变量类型必须为 int。

以下代码将文本文件中 x 行 y 列的浮点数读取到二维数组中。

```c
#include <stdio.h>

int main()
{
    int row = 3;
    int column = 4;
    double data[row][column];

    FILE* f = fopen("data.txt", "r");
    if (f == NULL) {
        printf("File can not be read!");
        return 1;
    }

    char line_buffer[1024] = { '\0' };
    int r = 0;
    while (fgets(line_buffer, 1024, f)) {
        int c = 0, offset = 0, len;
        double tmp;
        while (sscanf(line_buffer + offset, "%lf%n", &tmp, &len) != EOF) {
            data[r][c++] = tmp;
            offset += len;
        }
        r++;
    }

    for (int i = 0; i < row; i++) {
        for (int j = 0; j < column; j++) {
            printf("%lf ", data[i][j]);
        }
        printf("\n");
    }

    pclose(f); // 关闭文件
    return 0;
}
```

### 格式化 I/O 输出

C 语言的输入函数家族主要包括五个函数，其区别在于**输出源**不同，分别是

- `printf`：输出至标准输入流 `stdin` 。
- `fprintf`：输出至文件流指针 `steam` 。
- `dprintf`：输出至文件描述符 `fd` 。 
- `sprintf`：输出至字符串指针 `str` 。 
- `snprintf`：输出至字符串指针 `str` 。 

```c
#include <stdio.h>

int printf(const char *format, ...);
int fprintf(FILE *stream, const char *format, ...);
int dprintf(int fd, const char *format, ...);
int sprintf(char *str, const char *format, ...);
int snprintf(char *str, size_t size, const char *format, ...);
```

输出函数主要构成参数为**格式化字符串**以及**可变参数列表**，其中，格式化字符串包括一系列指令，输出函数将会按照指令的规则依次将参数的值格式化输出。

输出函数格式化字符串包括一系列**指令**，它们有：

- 常规字符： 直接输出，不做任何改变。
- **转换格式符** (conversion specifications)：由 `%` 开头的字符，将会按照格式格式化变量，并将结果输出。

**转换格式符**中的**转换说明符** (conversion specifier) 同输入函数一样，但转换格式符提供了一些额外的选项，格式如下：

```
%[flags][field width][precision][length modifier]conversion specifier
```

**标志符号 (flags)** 有四个比较常用：

- `#` ：标准形式，例如十六进制数字会以 `0x` 开头等。
- `0` ：空位补零，默认是空格填充。
- `-` ：左对齐，默认是右对齐。
- `+` ：正数符号显示，默认正数不显示符号。

**宽度 (field width)** 字段使用**非负数字**描述了这个变量占用的**最小宽度**，如果变量的输出结果宽度小于该值，则进行填充。

**精度 (precision)** 使用 `.dig` 表示，dig 为非负数字。精度和宽度有一定冲突。

- 对于整数，指示显示的位数。
- 对于浮点书，指示小数点后位数。
- 对于字符串指示最大显示个数。

**转换说明符**是格式符中最重要的部分，主要包括：

- `d, i` : int 输出为 signed decimal 格式。
- `o, u, x, X` : unsigned int 输出为 unsigned octal/decimal/hex 格式。
- `f` ：double 输出为小数形式，精度表示小数点位数，默认后 6 位。
- `e, E`:  double 输出为科学计数格式。
- `g, G`: double 输出为去除多余 0 格式，精度表示有效数字位数。
- `c`: int 输出为 unsigned char。
- `s`: char * 输出为字符串。
- `p`:  void * 指针输出为十六进制地址。

以下是一个输出示例代码。

```c
#include <stdio.h>

int main() {
    int i = 47;
    double f = 314.1592653;
    char str[] = "hello world";
    printf("i:\tdec: %d, oct: %o, HEX: %#X, hex: %04x\n", i, i, i, i);
    printf("f:\tbasic: %f, e: %.2e, E: %.10E, g: %.8g\n", f, f, f, f);
    printf("c:\t%c\n", i);
    printf("s:\t%s\n", str);
    printf("p:\t%p\n", str);
    return 0;
}
// output:
// i:      dec: 47, oct: 57, HEX: 0X2F, hex: 002f
// f:      basic: 314.159265, e: 3.14e+02, E: 3.1415926530E+02, g: 314.15927
// c:      /
// s:      hello world
// p:      0x7ffc9df49a5c
```



## 进程

### 进程开始

C 语言的程序总是从 main 函数开始执行，main 函数的原型如下：
```
int main(int argc, char *argv[]);
```

- argc 是命令行参数数量
- argv 是参数指针数组

当内核执行一个 C 程序时，需要先执行一个启动程序，该启动程序将**命令行参数**和**环境变量表**传递给 main 函数。

命令行参数可以使用如下方式遍历。

```c
for (i = 0; i < argc; i++)
for (i = 0; argv[i] != NULL; i++)
```

第一个命令行参数是程序名本身。

```c
$ ./echoarg arg1 TEST foo
argv[0]: ./echoarg
argv[1]: arg1
argv[2]: TEST
argv[3]: foo
```

除了命令行参数，每个程序都会接收到一个环境表 (environment list)，这是一个字符指针数组，每个指针指向一个以 null 结束的字符串。全局变量 environ 则指向环境表：`extern char **environ;`。

![image-20221115225220667](apue.assets/image-20221115225220667.png)

环境变量字符串格式为：`name=value`。尽管我们可以直接得到全局变量 environ 指针，但并不直接通过它访问环境变量，而是通过系列函数对变量进行增删查改。

|   函数   | 声明                                                         |
| :------: | ------------------------------------------------------------ |
|  getenv  | char *getenv(const char *name);                              |
|  putenv  | int putenv(char *str);                                       |
|  setenv  | int setenv(const char *name, const char *value, int rewrite); |
| unsetenv | int unsetenv(const char *name);                              |
| clearenv |                                                              |

### 进程终止

有 8 种方式可以终止一个进程，其中前 5 种为正常终止，后 3 种为非正常终止：

1. 从 main 返回
2. 调用 exit
3. 调用 _exti 或 _Exit
4. 最后一个线程从其 start routine 返回
5. 从最后一个线程调用 pthread_exit
6. 调用 abort
7. 接受到一个信号
8. 最后一个线程对取消请求做出响应

exit, _exit, _Exit 三个函数用于正常终止一个进程，其中 _exit, _Exit 直接返回内核，而 exit 先执行一些清理处理，然后返回内核。由于历史原因，exit 总会执行一个标准 I/O 库的清理关闭操作，这会导致所有打开流调用 fclose 函数，使得所有输出缓存中的所有数据都被 flush (写到文件)。

3 个退出函数都带有一个整型参数，称为终止状态。在大部分 Unix 的 shell 中，可以使用 `echo $?` 查看上一条执行语句的终止状态。

进程可以登记 (register) 函数，登记的函数将会在 exit 调用时自动执行，因此这些函数也称为**终止处理程序 (exit handlers)**。登记由调用 **atexit** 来完成。

```
#include <stdlib.h>
int atexit(void (*func)(void));
```

内核使程序唯一执行的方法是调用 exec 函数，进程自愿终止的唯一方法是显式或隐式地 (通过 exit) 调用 _exit 或 _Exit 函数。进程也可非自愿的由一个信号终止。

![image-20221115223432113](apue.assets/image-20221115223432113.png)



### C 程序存储空间布局

TODO

![image-20221118132606791](apue.assets/image-20221118132606791.png)

### 共享库

### 存储空间分配

malloc

### 拓展

setjump,longjmp 

setrlimit

## 进程控制

### 进程标识

进程使用一个非负整数作为其 ID，用于唯一标识进程。进程标识 (PID) 是唯一的，但却可以复用。有两个进程 ID 比较特殊：

- ID 为 0 的进程通常是调度进程，也被称为交换进程 (swapper)，该进程是内核的一部分，并不执行任何磁盘上的程序。
- ID 为 1 的通常是 init 进程。它是一个普通进程，但以超级用户特权运行。

除了常用的 PID，每个进程还有一些其他的标识符，可以通过如下函数获取，头文件为 `unistd.h`。

|          函数          |            说明             |
| :--------------------: | :-------------------------: |
| `pid_t getpid(void);`  |    获取调用进程的进程 ID    |
| `pid_t getppid(void);` | 获取调用进程父进程的进程 ID |
| `uid_t getuid(void);`  |    获取调用进程的用户 ID    |
| `uid_t geteuid(void);` |  获取调用进程的有效用户 ID  |
| `gid_t getgid(void);`  |     获取调用进程的组 ID     |
| `gid_t getegid(void);` |   获取调用进程的有效组 ID   |

### fork 函数

由 fork 创建的新进程被称为子进程 (child process)。一个 fork 函数被调用一次，但返回两次。两次返回的区别是：
- 父进程的返回值则是新建子进程的进程 ID，因为一个进程的子进程可以有多个，并且没有一个函数使一个进程可以获得其所有子进程的进程 ID。
- 子进程的返回值是 0，理由是一个进程只会有一个父进程，所以子进程总是可以调用 getppid 以获得其父进程的进程 ID。

子进程和父进程继续执行 fork 调用之后的指令。**子进程是父进程的副本**。例如，子进程获得父进程数据空间、堆和栈的副本。父进程和子进程并**不共享这些存储空间部分**，父进程和子进程**共享正文段**。

由于在 fork 之后经常跟随着 exec, 而后者又会将所有的运行时内存结构替换掉，所以每次 fork 为子进程创建一个副本可能是不划算的。因此现在很多实现并不执行一个父进程数据段、栈和堆的完全副本.作为替代使用了**写时复制 (Copy-On-Write, COW) **技术，意思是父进程或子进程任何一个试图修改的时候才会创建真正的副本，否则内核只是将权限修改为只读，实际上这些区域还是共享的。

### exec 函数

用 fork 函数创建新的子进程后，子进程往往要调用一种 exec 函数以执行另一个程序。当进程调用一种 exec 函数时，**该进程执行的程序完全替换为新程序**，而新程序则从其 main 函数开始执行。因为**调用 exec 并不创建新进程**，所以前后的进程ID并未改变。exec 只是用磁盘上的一个新程序替换了当前进程的正文段、数据段、堆段和栈段。

有 7 种不同的 exec 函数可供使用，被统称为 exec 函数。他们都在头文件 `unistd.h`，成功返回 0，否则返回 -1。

```c
#include <unistd.h>
int execl(const char *pathname, const char *arg0, ... /* (char *)0 */ );
int execv(const char *pathname, char *const argv[]);
int execle(const char *pathname, const char *arg0, ... /* (char *)0, char *const envp[] */ );
int execve(const char *pathname, char *const argv[], char *const envp[]);
int execlp(const char *filename, const char *arg0, ... /* (char *)0 */ );
int execvp(const char *filename, char *const argv[]);
int fexecve(int fd, char *const argv[], char *const envp[]);
```

几种函数的区别在名字里已经有所暗示：

- 待运行程序名
    - 空：表示取路径名作为参数。
    - p：表示取文件名作为参数，且在 PATH 环境变量中指定的各个目录中搜索。
- 待运行程序参数
    - l：表示以参数列表（list）方式提供。
    - v：表示以数组（vector）方式提供。
- 待运行程序环境表：
    - 空：使用调用进程中的 environ 变量为新程序复制现有的环境。
    - e：表示可以传递一个指向环境字符串指针数组的指针。

在很多 Unix 实现中，这 7 个函数中只有 execve 是**内核的系统调用**。另外 6 个只是库函数，关系如下：

![image-20221115213710326](apue.assets/image-20221115213710326.png)

### clone 系统调用

`clone()` 系统调用的基本用法如下：

```
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

### TODO

- exit
- wait/waitpid/wait3/wait4
- 竞争条件
- 更改用户 ID 和组 ID
- system
- 进程调度
- 进程时间

## 进程关系

### 终端登录、网络登陆、伪终端

父子关系：进程pid--〉父进程，ppid

### 进程组

- 一个或多个进程的集合，有pgid

- 一个组有一个组长进程，该进程的PGID为PID。

### 会话

- 一个或多个进程组的集合，有sid。

- 会话ID = 会话首进程的进程ID = 会话首进程的进程组ID
- 一个会话有一个控制终端
- 建立与控制终端连接的会话首进程为控制进程。
- 几个进程组可分为：一个前台进程组和若干后台进程组
- 终端键入：ctrl+c，发送到前台进程组所有进程
- 创建会话：进程调用 setsid
    - 不是进程组长：变成新会话首进程，成为新进程组组长进程，pgid为pid
    - 已经是进程组长：出错。如要创建，可以fork然后关闭父进程。

### 作业控制

fg、bg

### shell执行程序

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

### 孤儿进程

### BSD实现

### ===

当子进程终止时，父进程得到通知并能取得子进程的退出状态。

终端登录

![login](index/login.png)
![shell](index/shell.png)

进程组

每个进程除了有一进程 ID 之外，还属于一个进程组。进程组是一个或多个进程的集合。
同一进程组中的各进程接收来自同一终端的各种信号。
每个进程组有一个唯一的进程组ID

会话

会话 (session) 是一个或多个进程组的集合。
通常是由 shell 的管道将几个进程编成一组的。

```
$ proc1 | proc2 &
$ proc3 | proc4 | proc5
```

![session-control](index/session-control.png)

1. 该进程变成新会话的会话首进程 (session leader，会话首进程是创建该会话的进程)。此
时，该进程是新会话中的唯一进程。
2. 该进程成为一个新进程组的组长进程。新进程组 ID 是该调用进程的进程 ID。
3. 该进程没有控制终端(下一节讨论控制终端)。如果在调用setsid之前该进程有一个
控制终端，那么这种联系也被切断。


![job-control](index/job-control.png)

## 守护进程（完成）

### 守护进程特征

守护进程（daemon）是一种长期存在的没有控制终端的进程。通常随系统引导时启动，系统关闭时停止。Unix 具有很多守护进程，用来执行日常事务。

使用 `ps -axj` 可以查看系统中各个进程的状态，其中以方括号标识的名字是内核守护进程。守护进程一般以 `d` 字母结尾，例如：

- kthreadd：用来创建其他内核进程。
- kswapd：内存换页守护进程。
- inetd：侦听网络接口，支持各种网络服务请求。
- cron：定时任务。
- ....

### 守护进程规则

首先，创建一个守护进程需要最好遵从**以下基本原则**：

1. 调用 umask
2. 调用 fork，然后使父进程 exit。
3. 调用 setsid 创建一个新会话。
4. 将当前工作目录更改为根目录。
5. 关闭不再需要的文件描述符。
6. 将文件描述符 0，1，2 重写到 `/dev/null`。

其次，守护进程没有控制终端，不能将错误写到标准错误中。每个守护进程将它自己的出错信息写到一个单独的文件中，会导致管理复杂。**因此需要一个集中的守护进程出错记录程序，`syslog` 系统就是一个广泛应用的系统。**

![image-20221119013700706](apue.assets/image-20221119013700706.png)

三种产生日志消息的方法：

- 内核例程可以调用 log 函数。任何一个用户进程通过打开（open）然后读（read）`/dev/klog` 设备就可以读取这些消息。
- 大多数用户进程（守护进程）调用 `syslog` 函数以产生日志消息。
- 其他进程通过 TCP/IP 网络可将日志消息发往 UDP 514 端口。

通常， `syslogd` 守护进程读取所有 3 种格式的日志消息。

最后，**守护进程通常要求是单实例的**。如果同一个守护进程同时有多个实例运行，那么造成重复执行操作，可能引发错误。文件记录和锁机制可以保证一个守护进程只有一个副本在运行。

同时，**守护进程应当遵循以下惯例**：

- 若守护进程使用锁文件，则通常为 `/var/run/[name].pid`。
- 若守护进程支持配置文件，则通常为 `/etc/[name].conf`。
- 若守护进程可用命令行启动，则通常由系统初始化脚本完成，且进程终止时，应当自动重启，可以通过 `/etc/inittab` 中添加 `respawn` 记录项。

### 守护进程示例

```c
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <syslog.h>
#include <unistd.h>

#define LOCKFILE "/var/run/daemon.pid"
#define LOCKMODE (S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH)

int lockfile(int fd) {
    struct flock fl;

    fl.l_type = F_WRLCK;
    fl.l_start = 0;
    fl.l_whence = SEEK_SET;
    fl.l_len = 0;
    return (fcntl(fd, F_SETLK, &fl));
}

int already_running(void) {
    int fd;
    char buf[16];

    fd = open(LOCKFILE, O_RDWR | O_CREAT, LOCKMODE);
    if (fd < 0) {
        syslog(LOG_ERR, "can’t open %s: %s", LOCKFILE, strerror(errno));
        exit(1);
    }
    if (lockfile(fd) < 0) {
        if (errno == EACCES || errno == EAGAIN) {
            close(fd);
            return (1);
        }
        syslog(LOG_ERR, "can’t lock %s: %s", LOCKFILE, strerror(errno));
        exit(1);
    }
    ftruncate(fd, 0);
    sprintf(buf, "%ld", (long)getpid());
    write(fd, buf, strlen(buf) + 1);
    return (0);
}

void daemonize(const char *cmd) {
    int i, fd0, fd1, fd2;
    pid_t pid;
    struct rlimit rl;
    struct sigaction sa;

    /*
     * Clear file creation mask.
     */
    umask(0);

    /*
     * Get maximum number of file descriptors.
     */
    if (getrlimit(RLIMIT_NOFILE, &rl) < 0)
        printf("%s: can't get file limit", cmd);

    /*
     * Become a session leader to lose controlling TTY.
     */
    if ((pid = fork()) < 0)
        printf("%s: can't fork", cmd);
    else if (pid != 0) /* parent */
        exit(0);
    setsid();

    /*
     * Ensure future opens won’t allocate controlling TTYs.
     */
    sa.sa_handler = SIG_IGN;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    if (sigaction(SIGHUP, &sa, NULL) < 0)
        printf("%s: can't ignore SIGHUP", cmd);
    if ((pid = fork()) < 0)
        printf("%s: can't fork", cmd);
    else if (pid != 0) /* parent */
        exit(0);

    /*
     * Change the current working directory to the root so
     * we won’t prevent file systems from being unmounted.
     */
    if (chdir("/") < 0)
        printf("%s: can't change directory to /", cmd);

    /*
     * Close all open file descriptors.
     */
    if (rl.rlim_max == RLIM_INFINITY)
        rl.rlim_max = 1024;
    for (i = 0; i < rl.rlim_max; i++)
        close(i);

    /*
     * Attach file descriptors 0, 1, and 2 to /dev/null.
     */
    fd0 = open("/dev/null", O_RDWR);
    fd1 = dup(0);
    fd2 = dup(0);

    /*
     * Initialize the log file.
     */
    openlog(cmd, LOG_CONS, LOG_DAEMON);
    if (fd0 != 0 || fd1 != 1 || fd2 != 2) {
        syslog(LOG_ERR, "unexpected file descriptors %d %d %d",
               fd0, fd1, fd2);
        exit(1);
    }
}

void reread(void) {
    /* ... */
}

void sigterm(int signo) {
    syslog(LOG_INFO, "got SIGTERM; exiting");
    exit(0);
}

void sighup(int signo) {
    syslog(LOG_INFO, "Re-reading configuration file");
    reread();
}

int main(int argc, char *argv[]) {
    char *cmd;
    struct sigaction sa;

    if ((cmd = strrchr(argv[0], '/')) == NULL)
        cmd = argv[0];
    else
        cmd++;

    /*
     * Become a daemon.
     */
    daemonize(cmd);

    /*
     * Make sure only one copy of the daemon is running.
     */
    if (already_running()) {
        syslog(LOG_ERR, "daemon already running");
        exit(1);
    }

    /*
     * Handle signals of interest.
     */
    sa.sa_handler = sigterm;
    sigemptyset(&sa.sa_mask);
    sigaddset(&sa.sa_mask, SIGHUP);
    sa.sa_flags = 0;
    if (sigaction(SIGTERM, &sa, NULL) < 0) {
        syslog(LOG_ERR, "can't catch SIGTERM: %s", strerror(errno));
        exit(1);
    }
    sa.sa_handler = sighup;
    sigemptyset(&sa.sa_mask);
    sigaddset(&sa.sa_mask, SIGTERM);
    sa.sa_flags = 0;
    if (sigaction(SIGHUP, &sa, NULL) < 0) {
        syslog(LOG_ERR, "can't catch SIGHUP: %s", strerror(errno));
        exit(1);
    }

    /*
     * Proceed with the rest of the daemon.
     */
    /* ... */
    while (1) {
        sleep(10);
    }

    exit(0);
}
```

编译并多次运行上述程序。

```
# gcc daemon.c -o daemon
# ./daemon
# ./daemon
# ./daemon
```

此时 `ps -axj` 查看发现只有一个守护进程被执行了。通常情况下 PPID 为 1，但许多 Linux 发行版中 systemd 会接管 init。

```
PPID     PID    PGID     SID TTY        TPGID STAT   UID   TIME COMMAND
   1    1050    1050    1050 ?             -1 Ss    1000   0:01 /lib/systemd/systemd --user
1050   85898   85897   85897 ?             -1 S        0   0:00 ./daemon
```

最后我们杀死这个进程，并 `cat /var/log/syslog | grep daemon` 查看日志。

```
Nov 19 02:37:38 msi-ryzen3600 daemon: daemon already running
Nov 19 02:38:29 msi-ryzen3600 daemon: message repeated 2 times: [ daemon already running]
Nov 19 02:45:19 msi-ryzen3600 daemon: got SIGTERM; exiting
```

## 信号

### 信号概念

信号是一种软件中断，提供了一种处理异步事件的方法。

每个信号都有一个名字，定义在头文件 `<signal.h>` 中。信号的产生可以由多种方式，例如：

- 某些按键被按下，触发信号。
- 硬件异常（除 0，内存无效等）触发信号。
- 某些条件产生时，触发信号。
- 进程调用函数主动触发信号。

当信号出现时，内核按照以下三种方式之一进行处理。

- 捕捉信号：**通知内核在某种信号发生时，执行用户函数（signal handler）**。
- 执行默认动作：大多数信号的**默认动作是终止进程**。
- 忽略信号：大多数信号都可以被忽略，**但 `SIGKILL` 和 `SIGSTOP` 不能忽略**。

信号具有编号，一般而言用宏定义表示。其中用户可以使用的为 1-31，实时信号一般是内核使用的。

```
 1) SIGHUP	     2) SIGINT	     3) SIGQUIT	     4) SIGILL	     5) SIGTRAP
 6) SIGABRT	     7) SIGBUS	     8) SIGFPE	     9) SIGKILL	    10) SIGUSR1
11) SIGSEGV 	12) SIGUSR2	    13) SIGPIPE	    14) SIGALRM	    15) SIGTERM
16) SIGSTKFLT	17) SIGCHLD 	18) SIGCONT	    19) SIGSTOP	    20) SIGTSTP
21) SIGTTIN 	22) SIGTTOU 	23) SIGURG	    24) SIGXCPU	    25) SIGXFSZ
26) SIGVTALRM	27) SIGPROF 	28) SIGWINCH	29) SIGIO	    30) SIGPWR
31) SIGSYS	    34) SIGRTMIN	35) SIGRTMIN+1	36) SIGRTMIN+2	37) SIGRTMIN+3
38) SIGRTMIN+4	39) SIGRTMIN+5	40) SIGRTMIN+6	41) SIGRTMIN+7	42) SIGRTMIN+8
43) SIGRTMIN+9	44) SIGRTMIN+10	45) SIGRTMIN+11	46) SIGRTMIN+12	47) SIGRTMIN+13
48) SIGRTMIN+14	49) SIGRTMIN+15	50) SIGRTMAX-14	51) SIGRTMAX-13	52) SIGRTMAX-12
53) SIGRTMAX-11	54) SIGRTMAX-10	55) SIGRTMAX-9	56) SIGRTMAX-8	57) SIGRTMAX-7
58) SIGRTMAX-6	59) SIGRTMAX-5	60) SIGRTMAX-4	61) SIGRTMAX-3	62) SIGRTMAX-2
63) SIGRTMAX-1	64) SIGRTMAX
```

大部分 Unix 系统都提供了编号到信号名的映射数组，数组下标为信号编号，数组元素为指向信号名字符串的指针。通常使用 `strsignal` 函数取出其描述内容，类似于 `strerror`。

```c
#include <signal.h>
extern const char *const sys_siglist[];

#include <string.h>
char *strsignal(int sig);
```

如果需要将其输出到标准错误，可以使用 `psignal`，类似于 `perror`。
```c
#include <signal.h>

void psignal(int sig, const char *s);
void psiginfo(const siginfo_t *pinfo, const char *s);
```

以下是一个代码片段示例。

```c
// signal.c
int i = 9;
printf("signal %d : %s\n", i, strsignal(i));
psignal(i, "error");
// result
$ gcc signal.c
$ ./a.out 2>&1
signal 9 : Killed
error: Killed
```

### 信号发送

某些软件/硬件在中断或异常时，或是用户按下某些键位时，内核或驱动将会自动产生信号，发送给相应的进程。除此之外，程序也可以通过**信号发送函数**来主动发送信号。

- `kill` 函数将信号发送给进程或进程组。
- `raise` 函数允许进程将信号发送给自己。

```
#include <signal.h>
int kill(pid_t pid, int signo);
int raise(int signo);
```

`kill` 函数中，pid 参数有以下几种情况：

- pid > 0：发送给进程 pid。
- pid == 0：发送给同一进程组所有进程。
- pid < 0：发送给进程组 pid 的所有进程（发送进程具有权限向其发送信号的进程）。
- pid == -1：发送给所有进程（发送进程具有权限向其发送信号的进程）。

注意：进程将信号发送给另一进程需要权限。

通过 `kill` 命令行工具可以发送信号给指定进程。其格式为

```
kill -<signal> <pid> [...]
```

其中 signal 可以是编号、名称或简写。即： `-9, -SIGKILL or -KILL`。

例如：

```shell
kill -SIGUSR1 18742		# send SIGUSR1
kill -USR2 18742		# send SIGUSR2
kill 18742				# send SIGTERM
kill -9 18742			# send SIGKILL
```

### 信号设置

Unix 中，如果进程没有设置感兴趣的信号，当进程收到信号时，则会使用默认的处理动作。如果进程希望捕获某种信号，则可以使用 `signal` 函数来设置信号处理函数。

```c
#include <signal.h>
void (*signal(int signo, void (*func)(int)))(int);
```

`signal` 函数要求两个参数：

- signo 为感兴趣的信号名。
- func 为信号处理程序指针，表示该信号发生时的动作，
    - 常量 SIG_IGN 表示忽略此信号。
    - 常量 SIG_DFL 表示执行默认动作。
    - 函数地址表示在信号发生时调用该函数。

**信号处理函数要求一个整形参数，并且返回值为 void。**当调用 signal 设置信号处理程序时，返回该函数的指针。简化一下 signal 的声明如下：

```
typedef void Sigfunc(int);
Sigfunc *signal(int signo, Sigfunc *func);
```

以下是一个设置信号的示例：

```c
#include <signal.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

/* one handler for both signals, argument is signal number */
static void sig_usr(int signo) {
    printf("received %s (%d)\n", strsignal(signo), signo);
}

int main(void) {
    if (signal(SIGUSR1, sig_usr) == SIG_ERR)
        printf("can't catch SIGUSR1");
    if (signal(SIGUSR2, sig_usr) == SIG_ERR)
        printf("can't catch SIGUSR2");
    if (signal(SIGQUIT, sig_usr) == SIG_ERR)
        printf("can't catch SIGQUIT");
    for (;;)
        pause();
}
```

当我们执行时，对于已经设置过的信号，会执行 sig_usr 函数，否则执行默认动作。

```
$ ./sig &										# 启动程序
[1] 17497										# shell 打印作业编号和进程 ID
$ kill -USR1 17497								# 使用 kill 命令向进程发送 USR1 信号
received User defined signal 1 (10)
$ kill -USR2 17497								# 使用 kill 命令向进程发送 USR2 信号
received User defined signal 2 (12)
$ kill 17497									# 使用 kill 命令向进程发送 SIGTERM 信号
[1]+  Terminated              ./sig
```

### 信号可靠性（TODO）

当信号产生时，内核通常在进程表中以某种形式设置一个标志，这个过程称为信号递送（delivery）。在信号产生之后，信号递送之前，这段时间内信号是未知的（pending）。如果在 pending 之间信号重复产生，一般只能递送一次。

```c
int sigpending(sigset_t *set);
```

返回当前进程未知的信号集合。

信号集数据类型可以表示多个信号，信号集的操作函数包括以下五个。

```c
#include <signal.h>
int sigemptyset(sigset_t *set);
int sigfillset(sigset_t *set);
int sigaddset(sigset_t *set, int signo);
int sigdelset(sigset_t *set, int signo);
int sigismember(const sigset_t *set, int signo);
```

分别为：

- 清除信号集中所有信号
- 信号集中包括所有信号
- 在信号集中添加特定信号
- 在信号集中删除特定信号
- 信号集中是否具有特定信号

每个进程都有一个信号屏蔽字（signal mask），表示当前要阻塞传递到该进程的信号集。`sigprocmask` 函数可以检测或更改进程的信号屏蔽字。

### 常用信号说明

以下是信号的具体解释。

|  信号   |             英文解释             |                           信号产生                           | 默认动作 |
| :-----: | :------------------------------: | :----------------------------------------------------------: | -------- |
| SIGSTOP |               stop               |             停止进程但不退出，不可被捕捉或忽略。             |          |
| SIGKILL |           termination            |   系统管理员可以使用该信号杀死任意进程，不可被捕捉或忽略。   |          |
| SIGTERM |           termination            | kill 命令发送系统默认终止信号。程序正常退出，可以做一些清理工作然后优雅退出进程。 |          |
| SIGABRT |   abnormal termination (abort)   |          abort 函数调用时产生此信号，程序异常退出。          |          |
| SIGINT  |   terminal interrupt character   | 用户按中断键（`DEL` 或 `CTRL+C`）时，终端驱动向前台进程组所有进程发送信号。 |          |
| SIGQUIT |     terminal quit character      | 用户按退出键（`CTRL+\`）发送 QUIT 字符时，类似 SIGINT，但会产生core文件。 |          |
| SIGTSTP |     terminal stop character      | 用户按挂起键（`CTRL+Z`）时，终端驱动向前台进程组所有进程发送信号，类似 STOP。 |          |
| SIGCONT |     continue stopped process     |                                                              |          |
|         |                                  |                                                              |          |
| SIGCHLD |    change in status of child     |                                                              |          |
| SIGHUP  |              hangup              |                                                              |          |
| SIGPIPE |  write to pipe with no readers   |                                                              |          |
| SIGPOLL |      pollable event (poll)       |                                                              |          |
| SIGTTIN | background read from control tty |                                                              |          |
| SIGTTOU | background write to control tty  |                                                              |          |
| SIGURG  |    urgent condition (sockets)    |                                                              |          |
| SIGUSR1 |       user-defined signal        |                        用户自定义信号                        |          |
| SIGUSR2 |       user-defined signal        |                        用户自定义信号                        |          |
| SIGFPE  |       arithmetic exception       |                                                              |          |
| SIGABRT |   abnormal termination (abort)   |          abort 函数调用时产生此信号，程序异常退出。          |          |
| SIGALRM |      timer expired (alarm)       |                 time 函数超时时产生此信号。                  |          |

### 信号相关函数

```
#include <unistd.h>
unsigned int alarm(unsigned int seconds);
```



## 线程基础

### 线程简介

典型的 Unix 进程可以看成只有一个控制线程：一个进程在某一时刻只能做一件事情。有了多个控制线程以后，在程序设计时就可以把进程设计成在某一时刻能够做不止一件事，每个线程处理各自独立的任务。

线程带来了很多好处：

- 通过为每种事件类型分配单独的处理线程，可以简化处理异步事件的代码。**每个线程在进行事件处理时可以采用同步编程模式**，同步编程模式要比异步编程模式简单得多。
- 多个进程必须使用操作系统提供的复杂机制才能实现内存和文件描述符的共享，而多个**线程自动地可以访问相同的存储地址空间和文件描述符**。
- 单控制线程情况下，完成多任务只能串行进行。但有多个控制线程时，**相互独立的任务处理就可以交叉进行**，从而提高整个程序的吞吐量。
- 通过使用多线程将处理用户输入输出的部分与其他部分分开，从而改善程序响应时间。

**多线程**代码与**多处理器**或**多核系统**并不是绑定的，尽管多核处理器能够充分发挥多线程的优势。但即使程序运行在单处理器上，也能得到多线程编程模型的好处。所以不管处理器的个数多少，程序都可以通过使用线程得以简化。而且由于某些线程在阻塞的时候还有另外一些线程可以运行，所以多线程程序在单处理器上运行还是可以改善响应时间和吞吐量。

每个线程都包含有表示执行环境所必需的信息，其中包括：进程中标识线程的线程 ID、一组寄存器值、栈、调度优先级和策略、信号屏蔽字、errno 变量以及线程私有数据。一个进程的所有信息对该进程的所有线程都是共享的，包括可执行程序的代码、程序的全局内存和堆内存、栈以及文件描述符。

这里主要讨论 POSIX 线程，即 pthread 线程，头文件为 `<pthread.h>`。

### 线程标识

就像每个进程有一个进程 ID 一样，每个线程也有一个线程 ID。进程 ID 在整个系统中是唯一的，但线程 ID 只有在它所属的进程上下文中才有意义。

- 进程 ID 使用 pid_t 数据类型来表示
- 线程 ID 使用 pthread_t 数据类型来表示

Linux 上 pthread_t 使用 unsigned long int 实现，有时候打印线程 ID 很有用。而其他 Unix 变种系统却不一定，因此打印 ID 代码移植起来需要特别注意。

| 函数                                               | 解释            |
| -------------------------------------------------- | --------------- |
| pthread_t pthread_self(void);                      | 获得自身线程 ID |
| int pthread_equal(pthread_t tid1, pthread_t tid2); | 线程 ID 比较    |

### 线程创建

在传统 Unix 进程模型中，每个进程只有一个控制线程。程序开始运行时，它也是以单进程中的单个控制线程启动的。在创建多个控制线程以前，程序的行为与传统的进程并没有什么区别。

新增的线程可以通过调用 `pthread_create()` 函数创建，执行成功时返回 0，失败时返回错误码。

```
int pthread_create(pthread_t *thread, 
                const pthread_attr_t *attr, 
                void * (*start_routine)(void *), 
                void *arg);
```

其中参数为：

- 第一个参数为该线程 ID 的指针
- 第二个参数为线程属性
- 第三个参数为该线程执行的任务函数指针
- 第四个参数为任务函数参数指针

以下是一个创建线程代码的简单示例，每个线程简单的打印自身的线程 ID 和 任务 ID 后就退出。

```c
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define NUM_THREADS 5

void *print_hello(void *taskid) {
    printf("Hello World! It's me, thread (tid:%ld) #%ld!\n", pthread_self(), (long) taskid);
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    pthread_t threads[NUM_THREADS];
    int rc;
    long t;
    for (t = 0; t < NUM_THREADS; t++) {
        printf("In main: creating thread %ld\n", t);
        rc = pthread_create(&threads[t], NULL, print_hello, (void *)t);
        if (rc) {
            printf("ERROR; return code from pthread_create() is %d\n", rc);
            exit(-1);
        }
    }

    /* Last thing that main() should do */
    pthread_exit(NULL);
}
```

上述程序输出结果如下，每次输出的结果并不相同。

```
In main: creating thread 0
In main: creating thread 1
Hello World! It's me, thread (tid:140491234883328) #0!
In main: creating thread 2
Hello World! It's me, thread (tid:140491226490624) #1!
In main: creating thread 3
Hello World! It's me, thread (tid:140491218097920) #2!
In main: creating thread 4
Hello World! It's me, thread (tid:140491131713280) #3!
Hello World! It's me, thread (tid:140491209594624) #4!
```

线程也可以传入参数。

```c
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define NUM_THREADS 3

struct thread_data {
    int task_id;
    char *name;
};

struct thread_data thread_data_array[NUM_THREADS];

void *print_hello(void *threadarg) {
    struct thread_data *my_data;
    long taskid;
    char *name;
    my_data = (struct thread_data *)threadarg;
    taskid = my_data->task_id;
    name = my_data->name;
    printf("Hello World! It's me, thread #%ld, my name is %s!\n", taskid, name);
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    pthread_t threads[NUM_THREADS];
    char *thread_names[NUM_THREADS];
    thread_names[0] = "Alice";
    thread_names[1] = "Bob";
    thread_names[2] = "Tom";

    int rc;
    long t;

    for (t = 0; t < NUM_THREADS; t++) {
        thread_data_array[t].task_id = t;
        thread_data_array[t].name = thread_names[t];
        printf("In main: creating thread #%ld\n", t);
        rc = pthread_create(&threads[t], NULL, print_hello,
                            (void *)&thread_data_array[t]);
        if (rc) {
            printf("ERROR; return code from pthread_create() is %d\n", rc);
            exit(-1);
        }
    }

    /* Last thing that main() should do */
    pthread_exit(NULL);
}
```

上述程序输出结果如下，每次输出的结果并不相同。

```
In main: creating thread #0
In main: creating thread #1
Hello World! It's me, thread #0, my name is Alice!
In main: creating thread #2
Hello World! It's me, thread #1, my name is Bob!
Hello World! It's me, thread #2, my name is Tom!
```

### 线程等待

如果进程中的任意线程调用了exit, Exit 或者 _exit，那么**整个进程就会终止**。单个线程可以通过 3 种方式退出，因此可以在不终止整个进程的情况下，停止它的控制流。

- 线程可以简单地从启动例程中返回，返回值是线程的退出码。
- 线程可以被同一进程中的其他线程取消。
- 线程调用 pthread_exit() 函数。

```
void pthread_exit(void *retval);
```

通过 pthread_exit() 函数终止调用线程，并且如果该线程是 joinable 的话，还可以通过 retval 返回值给同进程的其他线程。注意 retval 指针指向的值不能存在于栈中，因为线程结束后栈会被销毁。

**当进程的所有的线程都终止后，则进程退出**。因此 main 线程最后应该调用 pthread_exit() 明确指出退出主线程，如若不然，main 将会隐式的调用 exit，从而退出整个进程，从而导致其他线程被终止。

```
int pthread_join(pthread_t thread, void **retval);
```

pthread_join() 使得调用线程将一直阻塞，直到指定的线程调用 pthread_exit()、从启动线程中返回或者被取消。

如果对线程的返回值并不感兴趣，那么可以把 retval 指针设置为 NULL。在这种情况下，调用 pthread_join() 函数可以等待指定的线程终止，但并不获取线程的终止状态。

### 线程特征

### 线程 API 总结

| 函数                                               | 解释                                     |
| -------------------------------------------------- | ---------------------------------------- |
| pthread_t pthread_self(void);                      | 获得自身线程 ID                          |
| int pthread_equal(pthread_t tid1, pthread_t tid2); | 线程 ID 比较                             |
| void pthread_exit(void *retval);                   | 退出调用线程，并可能传出返回值到其他线程 |

| 函数                                                         | 解释     |
| ------------------------------------------------------------ | -------- |
| int pthread_create(pthread_t *thread, const pthread_attr_t *attr, void * (*start_routine)(void *), void *arg); | 线程创建 |
| int pthread_join(pthread_t thread, void **retval);           | 线程等待 |



## 线程同步

### 同步概念

并发编程的一个基本问题：我们总是希望原子式 (atomic) 的执行一系列指令。但由于处理器的中断，我们总是做不到。能够直接解决这个问题的一个办法就是使用锁。程序员在源代码中加锁，放在需要保护的关键区 (critical sections) 周围，保证这些关键部分代码能够像单条原子指令一样执行。

对于 `balance = balance + 1;` 这行代码来讲，尽管看起来只有一行，但编译后却产生多条指令，这是一个读-改-写模式，

**更新共享变量**是一种典型的关键代码段。尽管在源代码层次看起来只有一行，但编译后却产生多条指令，这是一个读-改-写模式，在其中任意一步发生线程调度，都可能造成错误的结果。

```
balance = balance + 1;
```

其他的关键区还可能是：为共享的链表增加一个元素，或对共享结构的复杂更新操作。

锁的解决思路如下：
{% codeblock lang:c %}
lock_t mutex; // some globally-allocated lock ’mutex’
...
lock(&mutex);
balance = balance + 1;
unlock(&mutex);
{% endcodeblock %}

锁就是一个变量，这个变量主要保存了锁在某一时刻的状态，它
- 要么是**可用的**，表示没有线程持有锁，
- 要么是**被占用的**，表示有一个线程持有锁，并且正处于关键区。

lock 和 unlock 的语义十分简单：
- lock() 尝试获取锁，如果没有其他线程持有该锁，则该线程获取锁，并进入关键区。
- unlock() 由持有锁的线程调用，一旦被释放，锁就变为可用状态。

锁为程序员提供了最小的调度控制，使得程序员可以获得一些控制权，通过给关键区加锁，**保证关键区内代码只有一个线程活跃**，因此将原本由操作系统调度的混乱状态变得可控。

# Pthread 锁互斥锁
POSIX 库将锁称之为互斥量 (mutual exclusion, mutex)，有时也叫 Pthread 锁，被用来提供线程之间的互斥。

使用起来也十分简单，大致代码如下：
{% codeblock lang:c %}
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER; 

pthread_mutex_lock(&lock);
balance = balance + 1;
pthread_mutex_unlock(&lock); 
{% endcodeblock %}

# 锁的实现和性能
我们已经从程序员的角度，对锁如何工作有了一定的理解。那如何实现一个锁呢？我们需要什么**硬件**支持？需要什么**操作系统**的支持？

在实现锁之前，我们应该首先明确目标，为了评价锁是否能工作（并工作得好），我们应该先设立一些标准。
- 第一是锁的基本任务，即提供**互斥 (mutual exclusion)**。锁是否能够有效阻止多个线程进入关键区？
- 第二是**公平性 (fairness)**。当锁可用时，是否每一个竞争线程有公平的机会抢到锁？从线程角度看就是，是否有竞争锁的线程由于一直无法竞争到锁而饿死。
- 最后是**性能 (performance)**。使用锁之后增加的时间开销有多少，不同的场景有何区别？

# 基于硬件的锁
在本节中，我们仅用硬件支持，看看能实现到什么程度？

## 控制中断
最早提供的互斥解决方案之一，就是在关键区关闭中断，这个解决方案是为单处理器系统开发的。

{% codeblock lang:c %}
void lock() {
    DisableInterrupts();
}
void unlock() {
    EnableInterrupts();
}
{% endcodeblock %}

既然由于是中断导致线程的切换，那我们就解决掉中断。很好，既然解决不了问题，就解决提出问题的人。

假设我们运行在这样一个单处理器系统上。通过在进入临界区之前关闭中断（使用特殊的硬件指令），可以保证临界区的代码不会被中断，从而原子地执行。结束之后，我们重新打开中断（同样通过硬件指令），程序正常运行。

这种方法简单，但却存在许多问题，主要包括：
1. 要求我们允许所有调用线程执行特权操作（打开关闭中断），并信任这种机制不会被滥用。无条件的信任一个用户程序是一个糟糕的选择。
2. 这种方案不支持多处理器。
3. 关闭中断导致中断丢失，可能会导致严重的系统问题。例如磁盘或者网络刚好来了数据，请求中断怎么办？

## 自旋锁 - 一次失败的尝试
首先我们实现一个锁，**用一个变量标记锁是否被持有**。

{% codeblock lang:c %}
typedef struct lock_t { int flag; } lock_t;

void init(lock_t *mutex) {
    // 0 -> lock is available, 1 -> held
    mutex->flag = 0;
}

void lock(lock_t *mutex) {
while (mutex->flag == 1) // TEST the flag
    ; // spin-wait (do nothing)
    mutex->flag = 1; // now SET it!
}

void unlock(lock_t *mutex) {
    mutex->flag = 0;
}
{% endcodeblock %}

首先看互斥性，很明显可以分析出，该方法不满足互斥性。如果 Thread 1 在进入 lock 之后，设置 flag 为 1 之前被中断调度，那么由于此时 flag 仍然为 0，则其他线程同样可以进入 lock。

## 基于 Test-And-Set 的自旋锁
造成上述结果的原因是 test-and-set 这个过程不是原子的！基于这种概念，一些系统提供了一种最简单的硬件支持是测试并设置指令 (test-and-set instruction)，也叫作原子交换 (atomic exchange)。在 x86 上是 xchg 原子交换指令。我们用如下的 C 代码片段来定义 test-and-set 指令做了什么。

{% codeblock lang:c %}
int TestAndSet(int *old_ptr, int new) {
    int old = *old_ptr; // fetch old value at old_ptr
    *old_ptr = new; // store 'new' into old_ptr
    return old; // return the old value
} 
{% endcodeblock %}

test-and-set 指令做了下述事情。它返回 old_ptr 指向的旧值，同时更新为 new 的新值。当然，关键是这些代码原子地执行。因此我们之前的锁可以变为以下内容，其实只有 lock() 部分做了一点修改：

{% codeblock lang:c %}
typedef struct lock_t { int flag; } lock_t;

void init(lock_t *mutex) {
    // 0 -> lock is available, 1 -> held
    mutex->flag = 0;
}

void lock(lock_t *mutex) {
while (TestAndSet(&lock->flag, 1) == 1)
    ; // spin-wait (do nothing)
}

void unlock(lock_t *mutex) {
    mutex->flag = 0;
}
{% endcodeblock %}

通过 test-and-set 指令，我们已经实现了一把最简单的**自旋锁 (spin lock)**。竞争锁的线程在 CPU 周期内一直自旋，直到锁可用。

**自旋锁在单 CPU 的情况下需要抢占式的调度器**，即不断通过时钟中断一个线程，运行其他线程。否则，自旋锁在单 CPU 上无法使用，因为一个自旋的线程永远不会放弃 CPU。

我们来分析一下这个锁：

首先是互斥性，由于 test-and-set 指令，不难分析，在 lock 的过程要么线程进入关键区并设置 flag 为 1，要么一直等待自旋，直到 flag 为 0。

下一个标准是公平性，自旋锁对于等待线程的公平性如何呢？能够保证一个等待线程会进入临界区吗？答案是**自旋锁不提供任何公平性保证**。实际上，自旋的线程在竞争条件下可能会永远自旋。

最后是性能，性能可以分为两方面考虑：
- 在单 CPU 的情况下，性能开销相当大。假设 N 个线程有一个进入关键区，则竞争锁的 N-1 个线程都会在放弃 CPU 之前自旋一个时间片。
- 在多 CPU 上，自旋锁性能不错。假设线程 A 在 CPU 1，线程 B 在 CPU 2 竞争同一个锁。线程 A（CPU 1）占有锁时，线程 B 竞争锁就会自旋（在 CPU 2 上）。然而，临界区一般都很短，因此很快锁就可用，然后线程 B 获得锁。自旋等待其他处理器上的锁，并没有浪费很多 CPU 周期，因此效果不错。

## 基于 Compare-And-Swap 的自旋锁
某些系统提供了另一个硬件原语，名为 CAS。以下是这条指令的 C 语言伪代码。

{% codeblock lang:c %}
int CompareAndSwap(int *ptr, int expected, int new) {
    int actual = *ptr;
    if (actual == expected)
        *ptr = new;
    return actual;
} 
{% endcodeblock %}

有了 CAS 指令，就可以实现一个锁，类似于用 TAS 那样。例如，我们只要用下面的代码替换 lock() 函数即可实现一个自旋锁，其余代码不变。

{% codeblock lang:c %}
void lock(lock_t *lock) {
    while (CompareAndSwap(&lock->flag, 0, 1) == 1)
    ; // spin
} 
{% endcodeblock %}

{% note info %}
CAS 比 TAS 更强大，但就实现一个简单的自旋锁方面，两者是等价的。
{% endnote %}

## 基于 LL-SC 的自旋锁
一些平台提供了实现临界区的一对指令。例如 MIPS 架构中，链接加载（load-linked）和条件式存储（store-conditional）可以用来配合使用，实现其他并发结构。

{% codeblock Load Linkd and Stroe conditional lang:c %}
int LoadLinked(int *ptr) {
    return *ptr;
}
int StoreConditional(int *ptr, int value) {
    if (no one has updated *ptr since the LoadLinked to this address) {
        *ptr = value;
        return 1; // success!
    } else {
        return 0; // failed to update
    }
} 
{% endcodeblock %}

Load-Linked 指令和典型加载指令类似，关键区别来自 Store-Conditional 指令，只有上一次加载的地址在期间都没有更新时，才会成功，（同时更新刚才 Load-Linked 的地址的值）。成功时，Store-Conditional 返回 1，并将 ptr 指向的值更新为 value。失败时，返回 0，并且不会更新值。

我们可以用链接加载和条件存储指令改写我们的 lock() 函数。

{% codeblock lang:c %}
void lock(lock_t *lock) {
    while (1) {
        while (LoadLinked(&lock->flag) == 1)
        ; // spin until it's zero
        if (StoreConditional(&lock->flag, 1) == 1)
        return; // if set-it-to-1 was a success: all done
                // otherwise: try it all over again
    }
}
void unlock(lock_t *lock) {
    lock->flag = 0;
}
{% endcodeblock %}

一个线程调用 lock()，执行了链接的加载指令，返回 0。在执行条件式存储之前，中断产生了，另一个线程进入 lock 的代码，也执行链接式加载指令，同样返回 0。现在，两个线程都执行了链接式加载指令，将要执行条件存储。重点是只有一个线程能够成功更新标志为 1，从而获得锁；第二个执行条件存储的线程会失败（因为另一个线程已经成功执行了条件更新），必须重新尝试获取锁。

## 基于 Fetch-And-Add 的自旋锁
最后一个硬件原语是获取并增加（fetch-and-add）指令，它能原子地返回特定地址的旧值，并且让该值自增一。获取并增加的 C 语言伪代码如下：

我们使用 fetch-and-add 指令可以实现一个 ticket 锁。

{% codeblock lang:c %}
int FetchAndAdd(int *ptr) {
    int old = *ptr;
    *ptr = old + 1;
    return old;
}

typedef struct lock_t {
    int ticket;
    int turn;
} lock_t;

void lock_init(lock_t *lock) {
    lock->ticket = 0;
    lock->turn = 0;
}

void lock(lock_t *lock) {
    int myturn = FetchAndAdd(&lock->ticket);
    while (lock->turn != myturn)
    ; // spin
}

void unlock(lock_t *lock) {
    FetchAndAdd(&lock->turn);
} 
{% endcodeblock %}

不是用一个值，这个解决方案使用了 ticket 和 turn 变量来构建锁。基本操作也很简单：如果线程希望获取锁，首先对一个 ticket 值执行一个原子的获取并相加指令。这个值作为该线程的“turn”（顺位，即 myturn）。根据全局共享的 lock->turn 变量，当某一个线程的（myturn== turn）时，则轮到这个线程进入临界区。unlock 则是增加 turn，从而下一个等待线程可以进入临界区。

ticket 锁的过程类似于**排队**，每个竞争的线程 lock() 相当于入队，而 unlock() 相当于出队。不同于之前的方法：本方法能够**保证所有线程都能抢到锁**。只要一个线程获得了 ticket 值，最终一定会被调度。


## 总结：自旋过多
基于硬件的锁简单（只有几行代码）而且有效，这也是任何好的系统或者代码的特点。但是某些场景下，这些解决方案会效率低下。

如何让锁不会不必要地自旋，浪费 CPU 时间？只有硬件支持是不够的。我们还需要操作系统支持！

# 基于硬件和 OS 的锁
通过基于硬件的锁，有没有发现，每一个线程无论处于获取锁或是竞争锁的状态，都在不停的运行。

通过操作系统的支持，我们可以给线程定义状态：
- 运行 (Running)：线程可以执行并正在执行，该线程此时获得 CPU 时间片。
- 就绪 (Ready)：线程可以执行，但由于线程调度机制，此时并没有获取 CPU 时间片。
- 阻塞 (Blocked)：线程不可以执行，因此也不参与线程调度，需要被唤醒后才能重新参与线程调度。

## yield 系统调用：让出替代自旋
硬件支持让我们有了很大的进展：我们已经实现了有效、公平（通过 ticket 锁）的锁。但是，问题仍然存在：如果临界区的线程发生上下文切换，其他线程只能一直自旋，等待被中断的（持有锁的）进程重新运行。有什么好办法？

第一种简单友好的方法就是，**在要自旋的时候放弃 CPU 时间片**。在这种方法中，我们假定操作系统提供原语 yield()，线程可以调用它主动放弃 CPU，从而让其他线程运行。

{% codeblock lang:c %}
void lock() {
    while (TestAndSet(&flag, 1) == 1)
        yield(); // give up the CPU
}
{% endcodeblock %}

线程可以处于 3 种状态之一（运行、就绪和阻塞）。yield() 系统调用能够让运行 (running) 态变为就绪 (ready) 态，从而允许其他线程运行。因此，线程让出本质上是线程**取消调度 (deschedules)** 了它自己。

考虑在单 CPU 上运行两个线程。在这个例子中，基于 yield 的方法十分有效。如果许多线程（例如 100 个）反复竞争一把锁，则竞争线程将会一直处于 run-and-yield 模式，虽然比自旋好多了，但也浪费了不少时间在上下文切换的场景上。

更糟的是，我们还没有考虑饿死的问题。一个线程可能一直处于让出的循环，而其他线程反复进出临界区。

## 使用队列：睡眠替代自旋
前面一些方法的真正问题是存在太多的偶然性。调度程序决定如何调度。如果调度不合理，线程或者一直自旋（第一种方法），或者立刻让出 CPU（第二种方法）。无论哪种方法，都可能造成浪费或饿死。

因此，我们必须显式地施加某种控制，决定锁释放时谁能抢到锁。为了做到这一点，我们需要操作系统的更多支持，并需要一个**队列**来保存等待锁的线程。

简单起见，我们利用 Solaris 提供的支持，它提供了两个调用
- park() 能够让调用线程睡眠
- unpark(threadID) 则会唤醒 threadID 标识的线程

可以用这两个调用来实现锁，**让调用者在获取不到锁时睡眠，在锁可用时被唤醒**。

{%  codeblock lang:c %}
typedef struct lock_t {
    int flag;
    int guard;
    queue_t *q;
} lock_t;

void lock_init(lock_t *m) {
    m->flag = 0;
    m->guard = 0;
    queue_init(m->q);
}

void lock(lock_t *m) {
    while (TestAndSet(&m->guard, 1) == 1)
        ;  // acquire guard lock by spinning
    if (m->flag == 0) {
        m->flag = 1;  // lock is acquired
        m->guard = 0;
    } else {
        queue_add(m->q, gettid());
        m->guard = 0;
        park();
    }
}

void unlock(lock_t *m) {
    while (TestAndSet(&m->guard, 1) == 1)
        ;  // acquire guard lock by spinning
    if (queue_empty(m->q))
        m->flag = 0;  // let go of lock; no one wants it
    else
        unpark(queue_remove(m->q));  // hold lock (for next thread!)
    m->guard = 0;
}
{% endcodeblock %}

这种解决方案中存在一个问题，假如在 park() 调用之前，刚好遇到该线程 park()，这时切换到另一个线程（比如持有锁的线程），如果该线程随后释放了锁。那当第一个线程重新获得时间片后，接下来又会执行一个 park()，因此可能会永远睡下去。这种问题有时称为**唤醒/等待竞争 (wakeup/waiting race)**。为了避免这种情况，我们需要额外的工作。

## Linux 系统实现 - 两段锁
例如，Linux 提供了 futex，它类似于 Solaris 的接口，但提供了更多内核功能。具体来说，每个 futex 都关联一个特定的物理内存位置，也有一个事先建好的内核队列。调用者通过 futex 调用（见下面的描述）来睡眠或者唤醒。

具体来说有两个调用：
- 调用 futex_wait(address, expected) 时，如果 address 处的值等于 expected，就会让调线程睡眠。否则，调用立刻返回。
- 调用 futex_wake(address) 唤醒等待队列中的一个线程。

{% codeblock lang:c %}
void mutex_lock(int *mutex) {
    int v;
    /* Bit 31 was clear, we got the mutex (this is the fastpath) */
    if (atomic_bit_test_set(mutex, 31) == 0) return;
    atomic_increment(mutex);
    while (1) {
        if (atomic_bit_test_set(mutex, 31) == 0) {
            atomic_decrement(mutex);
            return;
        }
        /* We have to wait now. First make sure the futex value
        we are monitoring is truly negative (i.e. locked). */
        v = *mutex;
        if (v >= 0) continue;
        futex_wait(mutex, v);
    }
}
void mutex_unlock(int *mutex) {
    /* Adding 0x80000000 to the counter results in 0 if and only if
    there are not other interested threads */
    if (atomic_add_zero(mutex, 0x80000000)) return;
    /* There are other threads waiting for this mutex,
    wake one of them up. */
    futex_wake(mutex);
}
{% endcodeblock %}
这段代码利用一个整数，同时记录锁**是否被持有**（整数的最高位），以及**等待者的个数**（整数的其余所有位）。因此，如果锁是负的，它就被持有（因为最高位被设置，该位决定了整数的符号）。这段代码的有趣之处还在于，它展示了如何优化常见的情况，即没有竞争时：只有一个线程获取和释放锁，所做的工作很少（获取锁时测试和设置的原子位运算，释放锁时原子的加法）。

Linux 采用的这种古老的锁方案多年来不断被采用，现在也称为**两段锁 (two-phase lock)**。两阶段锁意识到自旋可能很有用，尤其是在很快就要释放锁的场景。因此，两阶段锁的第一阶段会先自旋一段时间，希望它可以获取锁。但是，如果第一个自旋阶段没有获得锁，第二阶段调用者会睡眠，直到锁可用。上文的 Linux 锁就是这种锁，不过只自旋一次；更常见的方式是在循环中自旋固定的次数，然后使用 futex 睡眠。

# 线程锁总结
通过锁的方式可以实现关键区的原子性，评价一个锁的指标至少包括互斥性和公平性。

仅通过**硬件原子原语**的支持，我们可以实现简单的**自旋锁**，自旋锁在多 CPU 的情况下性能不错，但过多的自旋总是浪费宝贵的 CPU 时间片。

通过借助**操作系统系统调用**的支持，我们可以实现更有效率的锁，其中：
- 通过 **yield 系统调用**可以显式让竞争线程在自旋时切换，节省 CPU 时间，但会导致频繁切换线程上下文的问题，或者线程反复让出 CPU 时间片而最终饿死自己。这种方式本质上是让线程在 running 和 ready 之间反复切换。
- 通过借助 **wait/wake 函数和队列**，可以让竞争线程在自旋时睡眠，并加入一个睡眠队列，通过逐个唤醒竞争线程来让竞争线程获得 CPU 时间片。这种方式本质上是让线程在 running 和 ready 状态之外还可以处于 block 状态，由于 block 线程不参与线程调度，因此节省了时间片。



### =====

int pthread_mutex_lock(pthread_mutex_t *mutex);
int pthread_mutex_trylock(pthread_mutex_t *mutex);
int pthread_mutex_unlock(pthread_mutex_t *mutex);
int pthread_mutex_init(pthread_mutex_t *restrict mutex, const pthread_mutexattr_t *restrict attr);
int pthread_mutex_destroy(pthread_mutex_t *mutex);

### 条件变量

很多情况下，线程需要检查某一条件满足之后，才会继续运行。



int pthread_cond_wait(pthread_cond_t *restrict cond, pthread_mutex_t *restrict mutex);
int pthread_cond_timedwait(pthread_cond_t *restrict cond, pthread_mutex_t *restrict mutex, const struct timespec *restrict abstime);
int pthread_cond_signal(pthread_cond_t *cond);

### 死锁

为什么发生死锁？
- 循环依赖
- 封装

产生死锁的条件：
1. 互斥：线程对于需要的资源互斥的访问
2. 持有并等待：线程持有了资源，同时又在等待其他资源
3. 非抢占：线程获得的资源，不能被抢占
4. 循环等待：线程之间存在一个环路，环路上每个线程都额外持有一个资源，而这个资源又是下一个线程要申请的。

若 4 个条件任何一个没有满足，则死锁不会产生。

预防死锁的方法：每个策略都设法阻止某一个条件，从而解决死锁问题。
| 阻止的条件 | 策略                                          | 优点                                                    | 缺点                                                         |
| ---------- | --------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------ |
| 循环等待   | 获取锁时提供一个全局加锁顺序 (total ordering) | 最实用 (常用)                                           | 顺序的保证需要细致的锁策略，可能会被粗心的程序员忽略         |
| 持有并等待 | 原子的抢占锁                                  | 简单，只需要一个额外的抢锁的锁                          | 需要一次抢到所有锁，降低了并发                               |
| 非抢占     | 获取不到所有的资源时，便释放拥有的资源        | 许多线程库提供了灵活的接口，例如可以使用 trylock() 函数 | 可能导致活锁 (大家都抢不到所有锁，系统一直在运行这段代码) ，可以通过引入随机等待时间降低重复干扰 |
| 互斥       | 通过硬件指令实现无等待数据结构                | 比较高级                                                | 实现复杂                                                     |

除了死锁预防，某些场景更适合死锁避免。我们需要了解**全局信息**，包括不同线程在运行中对锁的需求情况，从而使得后续的调度中能够避免产生死锁。

## 线程控制

## 进程间通信

## 命名空间

