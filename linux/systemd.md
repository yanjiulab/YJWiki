# Systemd

init 是系统启动的第一个进程，同时它是一个从开机到关机期间一直保持持续运行的**守护进程 (daemon process)**，并且作为其他所有进程直接或间接的祖先。init 由内核使用硬编码文件系统启动，如果不能加载将会引发系统崩溃。通常，**init 的进程标识符为 1**。



{% note info %}
这里的 init 指的是广义的 init，代表系统运行的第一个程序，事实上 init 有不同的实现方法，比如通过 `ps` 我们可以看到你的环境中 PID 为 1 的进程到底是什么。可能你看到的进程名不同，但它们可能只是符号链接，比如在笔者 Ubuntu 18.04 LTS 的环境中，可以看到 init 为集成式的 systemd，但名称并不总是显示为 systemd。
{% codeblock lang:sh %}
$ ps p 1    # BSD options, which may be grouped and must not be used with a dash.
  PID TTY    STAT   TIME  COMMAND
   1   ?      Ss    0:05  /sbin/init splash
$ ps -p 1   # UNIX options, which may be grouped and must be preceded by a dash.
  PID TTY          TIME  CMD
   1   ?        00:00:05 systemd
$ ls -al /sbin/init
lrwxrwxrwx 1 root root 20 3月   1 05:03 /sbin/init -> /lib/systemd/systemd
{% endcodeblock %}
{% endnote %}

## Traditional Inits
首先，我们看看传统的 Linux 是如何启动的：
1. 首先 **init 进程 (init process)** 被创建，并作为其他所有进程的祖先，获得进程标识符 1。
2. 接着，init 加载 **启动脚本 (init scripts (or rc))** 并执行，用来确保系统开关机的基础功能，这包括挂载文件系统和执行一些守护进程等。
3. 最后，由 **服务管理器 (service manager)** 对已启动进程进行控制和监督。比如监视到某进程崩溃时重启该进程。

以上几部分组成了**启动系统 (init system)**，其符合 "keep simple, keep stupid" 的 Unix 哲学，每个部分都有自己的任务。

- Inits
    - SysVinit — Traditional System V init.
    - ...
- Init scripts
    - initscripts-fork — Maintained fork of SysVinit scripts in Arch Linux.
    - ...
- Service managers
    - runit — UNIX init scheme with service supervision, a replacement for SysVinit, and other init schemes.
    - ...

## Integrated Inits
不同的 init 有不同的实现，有的包含了类似于启动脚本的东西，有的包含了服务管理器。这些 inits 我们称为**集成式 init (integrated inits)**，

- [systemd](https://wiki.archlinux.org/index.php/Systemd) 
- upstart
- ...

{% note info %}
- Arch Linux only has official support for systemd.
- Ubuntu use systemd after 16.04 LTS, but you can also use upstart instead. 
{% endnote %}

## SysVInit

## systemd
在众多 SysVInit 的替代品中，目前 {% button https://freedesktop.org/wiki/Software/systemd/, systemd, home fa-fw fa-lg %} 占据绝对优势，当前绝大多数 Linux 发行版已经基于新的 systemd，并且保持对 System V 的兼容。但由于 systemd 破坏了 Unix 保持简单的设计哲学等一系列问题，如今仍有很多人反对 systemd。

![architecture](https://upload.wikimedia.org/wikipedia/commons/3/35/Systemd_components.svg)

{% codeblock %}
# systemctl start sshd
# systemctl start sshd.service 
# systemctl stop sshd
# systemctl restart sshd
{% endcodeblock %}

## Resources
- [Init, ArchWiki](https://wiki.archlinux.org/index.php/Category:Init)
- [systemd, ArchWiki](https://wiki.archlinux.org/index.php/systemd)

systemd 是一组命令，包括

| 命令            | 解释 |
| --------------- | ---- |
| systemctl       |      |
| systemd-analyze |      |
| hostnamectl     |      |
| localectl       |      |
| timedatectl     |      |
| loginctl        |      |

