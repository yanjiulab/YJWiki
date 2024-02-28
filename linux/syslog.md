# SYSLOG

## 简介

## rsyslogd

rsyslogd 的配置文件为 `/etc/rsyslog.conf`，该文件会加载 `/etc/rsyslog.d/` 目录下的所有配置文件，其默认配置为 `50-default.conf`。

```shell
ls /var/log/ | grep syslog
syslog          # 当前日志文件
syslog.1        # 最近一次日志文件
syslog.2.gz     # 更旧的压缩日志
syslog.3.gz     # 更旧的压缩日志
syslog.4.gz     # 更旧的压缩日志
```

日志滚动更新设置文件为 `/etc/logrotate.conf`。

## C program

```c
#include <syslog.h>

int main(int argc, char* argv[]) {
    syslog(LOG_INFO, "hello syslog.\n");
    return 0;
}
```

查看 `/var/log/syslog` 文件，即可看到输出。

```shell
tail /var/log/syslog
...
Jan  8 16:14:08 liyj-virtual-machine a.out: hello syslog.
...
```

##
