# 基本操作



## 用户和组

用户 (Users) 和组 (Groups) 是一种 GNU/Linux 系统对文件、目录和外设访问控制 (access control) 的机制 (mechanism)，管理员可以微调组成员和权限，以授权和拒绝用户或服务对系统资源的访问。

- 



新安装的 Linux 默认采用超级权限用户登录，也就是 `root`，长时间用 root 账户登录或是在 SSH 服务器上公开它是十分不安全的。Linux/Unix 是完全意义上的**多用户多任务**操作系统，所以推荐的做法是**为大多数任务创建和使用非特权账户，而仅使用 root 账户进行系统管理**。Linux 默认提供了相当简单粗暴的访问控制机制，所以，每一个 Linuxer 都应当十分熟悉用户和组的概念。

用户就是计算机为每个使用者创建的名称，这个名称是一个人获得使用计算机的权限。当然，一个人 (individual)可以有多个账户/用户 (account/user)，只要名字不同即可。但有一些名字是保留的，不可以使用，例如 `root`。

多个用户 (users) 可以组合在一起形成组 (group)，一个组可以包含多个用户，一个用户也可以属于多个组，这是很自然的，因为人在社交中也在不同的场合中扮演不同的角色。

### 权限和所属

Unix 中一切皆文件。 这是很有趣的哲学，意味着**文件 (file)**这一模型，提供了对所有 I/O 资源访问的抽象，包括文档、目录、磁盘、CD-ROM、调制解调器、键盘、打印机、显示器和终端等等，甚至也包括了进程、网络之间的通信。所有文件都通过一致的 API 以提供访问，因此只用同一套简单的命令，就可以读写磁盘、键盘、文档以及网络设备。

GNU/Linux 系统中的每一个文件都从属一个用户（属主）和一个用户组（属组），这称为 **ownership** 机制。另外，还有三种类型的**访问权限 (access permissions)**：读（read）、写（write）、运行（execute）。**我们可以针对文件的属主、属组、而设置相应的访问权限。**用 `ls` 命令长格式看看吧：

```
➜  ~ ls -l /boot/
total 136492
-rw-r--r-- 1 root root  1537997 10月 23 22:44 abi-4.15.0-39-generic
-rw-r--r-- 1 root root   217018 10月 23 22:44 config-4.15.0-39-generic
drwx------ 3 root root    16384 1月   1  1970 efi
drwxr-xr-x 6 root root     4096 11月 15 15:37 grub
-rw-r--r-- 1 root root 55501463 11月 14 14:16 initrd.img-4.15.0-39-generic
-rw-r--r-- 1 root root   182704 1月  28  2016 memtest86+.bin
-rw-r--r-- 1 root root   184380 1月  28  2016 memtest86+.elf
-rw-r--r-- 1 root root   184840 1月  28  2016 memtest86+_multiboot.bin
-rw-r--r-- 1 root root        0 10月 23 22:44 retpoline-4.15.0-39-generic
-rw------- 1 root root  4047147 10月 23 22:44 System.map-4.15.0-39-generic
-rw------- 1 root root  8277752 10月 23 22:59 vmlinuz-4.15.0-39-generic
```

- 第 1 列：文件访问权限
    - 文件类型（1）：目录为 `d`，文件为 `-`。
    - 属主权限（3）
    - 属组用户权限（3）
    - 其他用户权限（3）
- 第 3 列：属主
- 第 4 列：属组

查看用户的属主、属组以及访问权限可以通过 `stat` 命令。例如：
```
➜  ~ stat -c %U /media/liyj/Shared
liyj
➜  ~ stat -c %G /media/liyj/Shared
liyj
➜  ~ stat -c %A /media/liyj/Shared
drwxrwxrwx
```

{% note info %}
stat - display file or file system status
stat 是用来显示文件（默认行为）或文件系统的命令，较常使用的有：
- 直接使用 `stat FILE ...` 显示文件状态，输出使用较为详细的默认格式。
- 通过 `-c` 参数可以指定 format 从而改变 (**c**hange) 文件状态输出格式，format 参数见 manual 手册。
- 通过 `-f` 参数可以显示文件系统的状态。

详细用法请查阅 manual 手册。
{% endnote %}

其中 rwx 分别代表了 可读，可写，可执行，有相应权限则写明字母，若无相应权限，则用 `-` 代替。如上述 `grub` 目录 root 用户有读、写、执行权限，而 root 组所有用户以及其他用户，均只有读、执行权限。

通过 find 命令可以查找属于某个用户或某个组的文件
- find / -grup *groupname*
- find / -group *groupnumber*
- find / -user *user*

文件的属主、属组可以通过 `chown` 命令更改。文件的权限可以通过 `chmod` 命令修改。

详情参见：`chown(1)`、`chmod(1)`、[Linux 文件权限](https://www.linux.com/learn/understanding-Linux-file-permissions)。

### 信息存储
| File           | Purpose                                              | 解释                 |
| -------------- | ---------------------------------------------------- | -------------------- |
| `/etc/passwd`  | User account information                             | 用户账户信息         |
| `/etc/shadow`  | Secure user account information                      | 用户账户安全信息     |
| `/etc/group`   | Defines the groups to which users belong             | 群组账户信息         |
| `/etc/gshadow` | Contains the shadowed information for group accounts | 群组账户安全信息     |
| `/etc/sudoers` | List of who can run what by sudo                     | 可以运行 sudo 的用户 |
| `/home/*`      | Home directories                                     | 家目录               |

本地用户信息存储在 `/etc/passwd` 文件中，一行代表一个用户，每行分七个部分，用英文冒号“:”分开：
```
account:password:UID:GID:GECOS:directory:shell
```
- `account` 是用户名，需要遵循标准 *Nix 命名准则。
- `password` 是用户密码。
{% note warning %}
`/etc/passwd` 对所有人可读，存储密码（无论是否通过哈希运算等方式加密）是不安全的，因此在 password 字段，用一个占位符 `x` 代替，加密过的密码储存在 `/etc/shadow` 文件，该文件对普通用户限制访问，shadow 这个名字也表示了密码被阴影笼罩住了。:p
{% endnote %}
- `UID` 是用户ID，在 Arch 中，第一个非 root 用户的默认 UID 是 1000，后续创建的用户 UID 也应大于1000。
- `GID` 是用户首要组的 ID，组的 ID 在 `/etc/group` 文件中。
- `GECOS` 是可选的注释字段，通常记录用户全名。
- `directory` 用于登录命令设置 `$HOME` 环境变量。
- `shell` 是用户默认登录的shell，通常是Bash。

本地群组信息存储在 `/etc/group` 文件中，一行代表一个群组，每行分四个部分，用英文冒号“:”分开：
```
group:password:GID:user_list
```
- `group` 是群组名称。
- `password` 是群组密码，同用户安全信息机制相同，加密过的密码储存在 `/etc/gshadow` 文件中。
- `GID` 是群组 ID，是一个整数。
- `user_list` 是群组中的用户成员，用逗号分割，群组可能是该用户的首要组，也可能是附加组；若此项为空，则表示该群组成员仅有一个，且用户名同组名相同。

## 用户管理
- 使用 `who` 或 `users` 命令，可以查看目前已登陆的用户。
- 以 root 执行 `passwd -Sa`，可以查看系统上的用户。

### `useradd` 创建用户
```
# useradd -m -g initial_group -G additional_groups -s login_shell username
```
- `-m/--create-home`：创建用户家目录 `/home/username`。
- `-g/--gid`：设置用户初始组的名称或数字 ID。**如果设置此项，则组必须存在；如果不设置此项，将会根据`/etc/login.defs` 中的 `USERGROUPS_ENAB` 变量设置，默认行为是创建与用户名相同的组名，GID 等于 UID。**
- `-G/--groups`：该用户要加入的其他组列表，用逗号分割，不加空格。**如果不设置，用户只加入初始组。**
- `-s/--shell`：用户默认登录 shell 的路径。默认为 sh 或 bash。有时候需要禁止某些用户执行登录动作，例如用来执行系统服务的用户。将 shell 设置成 `/usr/bin/nologin` 就可以禁止用户登录。

为了确保能够登录，shell 路径应当在 `/etc/shells` 列表中，否则 `pam_shell` 将会拒绝登录。也不要使用 `/usr/bin/bash` 来代替 `/bin/bash`，除非已经在 `/etc/shells` 中合理配置。

新创建的用户记得用 `passwd username` 来设置密码。

使用如下命令创建一个登录用户 test1，并设置密码。为该用户：创建用户目录 test1；默认创建同名群组 test1；默认不添加附加组；使用默认 shell。
```
# useradd -m test1 
# passwd test1
```

查看创建的用户，验证以上参数的结果：
```
~ cat /etc/passwd | grep test1
test1:x:1001:1001::/home/test1:/bin/sh
~ cat /etc/group | grep test1
test1:x:1001:
~ ls /home
liyj  test1
```

不同的系统用户可以为进程、守护进程提供更安全的管控目录及文件的访问。使用如下命令创建一个**非登录，无 home 目录的系统用户。（可以加入 -U 参数创建一个和用户名相同的群组，并自动将用户加入它）**
```
# useradd -r -s /usr/bin/nologin username
```

### `usermod` 更改用户信息
| 作用               | 命令                                       | 注释                                                         |
| ------------------ | ------------------------------------------ | ------------------------------------------------------------ |
| 更改用户登录名称   | `# usermod -l newname oldname`             | 仅更改用户名字，不更改主目录名称，更不更改同步创建的组名     |
| 更改用户主目录     | `# usermod -d /my/new/home -m username`    | 自动创建新目录，并移动内容。                                 |
| 将用户加入群组     | `# usermod -aG additional_groups username` | 支持加入多个群组，用逗号分隔。**如果省略 `-a` 参数，该用户会离开没有列在群组的其它群组。** |
| 设置注释           | `# usermod -c "Comment" username`          | 也可以使用 `# chfn username` 启动交互式模式设置。            |
| 改变用户登录 shell | `# usermod -s /bin/bash username`          |                                                              |

更具体内容，请参阅 `man usermod`。

### `userdel` 删除用户
```
# userdel -r username
```

## 群组管理
- 使用 `groups user` 查看用户群组关系，如果 user 省略，默认查看当前用户的群组关系。另外，通过 `id user` 可以看到更详细的信息，如 UID 和 GID。
- 列出系统上所有群组：`cat /etc/group`

### 增删群组
```
# groupadd group # 创建新的组
# groupdel group # 删除用户组
```

### `gpasswd` 增删群组成员
```
# gpasswd -a user group # 将用户添加到组
# gpasswd -d user group # 将用户从组中移除
```

### `groupmod` 更改信息
更改用户所属的组名，不变更GID：
```
# groupmod -n newname oldname
```


### 交互式脚本
除了上述的命令，还有一些以交互方式执行的脚本，这些脚本后台调用上述命令，更加易用。这些脚本的命名方式采用**动作＋对象**，而不是**对象＋动作**，这些脚本包括：
- `adduser`, `addgroup` - add a user or group to the system
    - Add a normal user
    - Add a system user
    - Add a user group
    - Add a system group
    - Add an existing user to an existing group
- `deluser`, `delgroup` - remove a user or group from the system
    - Remove a normal user
    - Remove a group
    - Remove a user from a specific group

例如：使用 `adduser` 可以以交互的方式执行 `useradd`, `chfn` 和 `passwd`。

更多的使用方式查阅手册。

### 总结

1. Unix 系统中一切皆文件。
2. 访问权限 (permission) 说的是文件 (files) 和用户 (users) 之间的联系。
    - 通过 `chown` 改变文件的属主和属组。
    - 通过 `chmod` 改变文件对于属主用户，属组用户以及其他用户的访问权限。
3. 成员关系 (ownership) 说的是用户 (users) 和 群组 (groups) 之间的联系。一个用户可以属于多个群组，一个群组也可以包含多个用户。
4. 用户和群组信息存储在 `/etc/{passwd, group}` 中，其中的加密信息以影子文件的形式存储在 `/etc/{shadow, gshadow}` 中。
4. 用户和群组的管理可以用**基础命令**来管理，基础命令命名方式为**对象＋动作**，例如：
    - useradd, groupadd
    - usermod, groupmod
    - userdel, groupdel
5. 为用户添加密码使用 `passwd`，为群组增减成员使用 `gpasswd`。
5. 用户和群组的管理还可以用**构建于基础命令上的脚本**来管理，脚本的命名方式为**动作＋对象**，例如：
    - adduser, addgroup
    - deluser, delgroup

     

## 归档和压缩

Unix 程序设计的其中一条哲学为：一个程序应当只做一件事，并做好它。日常我们经常说的压缩文件其实包含了两个过程：

1. 建档 (Archiving)：将多个文件**打包**成一个档案/目录(archive file)，或将其**拆包**。例如 `tar` 。
2. 压缩 (Compression)：将档案**压缩**成占用空间更小的文件，或将其**解压**。例如 `gzip`。

所以，压缩过程实际上是：**首先建立档案文件，然后压缩它**。

### 归档工具
归档工具的作用是：只生成档案文件。归档工具有很多，如 `GNU tar`，`ar`等，这里仅仅介绍一下 tar ，因为在日常使用中，基本用它最多。

tar 的常用命令为：`tar cfv archive.tar /etc`，但我相信你第一次看肯定记不住，因为这条命令进行了高度简化，原命令可以写成：`tar --create --file archive.tar --verbose /etc`。它其实包含三个参数，可以按照如下方式记忆：
- c (create)：**创建**
- f (file)：**文件**（archive.tar），
- v (verbose)：文件的**详细**内容为（/etc）。

同理，解包命令 `tar xfv archive.tar` 也就很容易记忆了，其中 `x` 代表 e**x**tract 。

注意，上条命令代表将 archive.tar 文件解包到当前目录下，如果要将其解压到特定的目录下，需要加入 `-C` 参数，其意义为**Change Directory**。完整命令为：`tar xfv archive.tar -C /path/to/what/you/want`，更详细的用法参阅手册。

### 压缩工具
在 Unix 系统中，常用的三种压缩格式如下：

| 名称    | 拓展名       | 与 tar 连用时的拓展名   |
| ------- | ------------ | ----------------------- |
| `bzip2` | `.bz2, .bz`  | `.tbz2, .tbz, .tar.bz2` |
| `gzip`  | `.gz, .z`    | `.tgz, .taz, .tar.gz`   |
| `xz`    | `.xz, .lzma` | `.txz, .tlz, .tar.xz`   |

**使用方法也比较统一，默认执行压缩动作，通过 `-d` 指示解压动作。**

| 名称    | 压缩         | 解压                | 解压到标准输出设备 |
| ------- | ------------ | ------------------- | ------------------ |
| `bzip2` | `bzip2 file` | `bzip2 -d file.bz2` | `bzcat file.bz2`   |
| `gzip`  | `gzip file`  | `gzip -d file.gz`   | `zcat file.gz`     |
| `xz`    | `xz file`    | `xz -d file.xz`     | `xzcat file.xz`    |

### tar 命令
事实上，说 tar 仅是打包工具是不准确的，因为 tar 命令可以具有**压缩参数**。通过选择压缩选项可以同时完成两个阶段，在实际使用中也是如此。

tar 难以记忆的点主要有两方面：
- 参数风格
- 压缩格式对应的参数

事实上，tar 分为 BSD tar 和 GNU tar 两种，主要区别在于参数前有没有 `-`：
- BSD 风格**没有** `-`
- GNU 风格有 `-`

总体来说两种风格都可以使用，GNU 风格更新一点，混用问题也不大。但是有一个点需要特别注意，**如果使用带有 `-` 的风格，那么最后一个参数必须为 `f`**，这是因为这种风格的代码参数解析时，将 f 后面的参数作为了**文件名**；然而 BSD 风格的参数解析没有这个问题。

当建立一个压缩包的时候，**两者均支持使用 `-a` 参数来自动创建压缩包 (compressed archive)，并依据其文件扩展名选择对应的压缩程序**。另外，tar 针对不同的压缩格式提供了定制的参数，如
- xz 的 `-J`
- gzip 的 `-z`
- bzip2 的 `-j` 

推荐使用 a 参数，代表 auto compress，不仅使用方便，又能**降低命令记忆负担**。

当解包一个被 bzip2，compress，gzip，lzip，lzma 或 xz压缩过的包的时候，两种 tar 工具均**自动进行解压缩**，再拆包。所不同的是，BSD tar **基于格式**识别压缩文件的格式，而 GNU tar 仅是**基于文件后缀猜测**压缩文件格式。

综上所述：笔者个人习惯于选择 BSD 风格，常用例子如下：

```
tar cvf archive.tar /etc            # 创建包 archive.tar，其内容为 /etc 目录
tar cvf archive.tar a.txt b.c       # 创建包 archive.tar，其内容为 a.txt b.c 
tar cavf archive.tar.gz /etc        # 创建压缩包，需要什么压缩格式就写什么后缀
tar xvf archive.tar.gz              # 解压包 archive 到当前目录（自动选择压缩工具）
tar xvf archive.tar.bz2 -C /opt/    # 解压包 archive 到指定目录（自动选择压缩工具）
```

### 其他命令
虽然 Unix 设计的哲学是简单，但**打包后压缩**或**解压后拆包**应该是对用户无感的，用户只关注结果！如下是日常生活中用到的三种压缩格式对应的工具

| 名称  | 命令           | 拓展名 | 描述                       |
| ----- | -------------- | ------ | -------------------------- |
| `7z`  | `7z`           | `.7z`  | 较为小众，但很易用的工具。 |
| `RAR` | `rar`, `unrar` | `.rar` | 格式和工具都是专有的。     |
| `ZIP` | `zip`, `unzip` | `.zip` | 在 Windows 系统上常用。    |

常用命令如下，其中 7z 和 rar 都不约而同的使用了 **`a` (add) 指示打包并压缩，`x` (extract) 指示解压并拆包**，对于 zip 文件则采用了 unzip 来解包，更加方便。

| 名称         | 压缩                      | 解压          | 列出内容         |
| ------------ | ------------------------- | ------------- | ---------------- |
| `7z`         | `7z a a.7z file1 file2`   | `7z x a.7z`   | `7z l a.7z`      |
| `rar`        | `rar a a.rar file1 file2` | `rar x a.rar` | `rar l a.rar`    |
| `zip, unzip` | `zip a.zip file1 file2`   | `unzip a.zip` | `unzip -l a.zip` |

### 总结
- 利用 tar 打包， `cfv` 分别代表 create file verbose， `xfv` 的 x 代表 extract(抽取) 。
- 使用 tar 打包时候还可以压缩，增加参数 a 并 写明包后缀，如 `archive.tar.gz`，tar 可以自动依据后缀选择对应压缩程序对所选文件/目录进行压缩打包。
- tar 支持自动解包常用的压缩包格式。如不支持，先解压，再解包。
- 有一些工具仅支持压缩，其命令格式大致为：命令 + 文件。默认压缩，使用 `-d` 参数指示解压。
- 有一些工具支持打包并压缩，大部分用 `a` 指示打包并压缩， 用 `x` 指示解压并拆包。

以上均是一些浅显的规律，目的是减少记忆负担。**在拿不准命令如何使用的时候，千万 `man` 一下。**本文编写时，笔者曾多次查阅 man page 以获取信息和验证。

## 网络相关配置

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
