# Linux 内核防火墙

## 简介

### netfilter

### nftables

### {ip,ip6,arp,eb}tables

### 内核实现

### netlink

## iptables 架构

```
                    input  --> [local] -->  output

                      ↑                       ↓

--> prerouting --> [Route] --> forward -- > postrouting -->
```



### 表 - table

目前 Linux 内核中有 5 个独立的表，包括：

| 表       | 说明               | 默认链                          |
| -------- | ------------------ | ------------------------------- |
| filter   | 默认表，用于过滤   | INPUT, FORWARD, OUTPUT          |
| nat      | 用于网络地址转换   | PREROUTING, OUTPUT, POSTROUTING |
| mangle   | 对特定数据包的修改 | 所有                            |
| raw      | 用于配置数据包     |                                 |
| security | 用于强制访问控制   |                                 |

大部分情况下，仅需要使用 filter 表和 nat 表，其余表用于更复杂的情况，包括多路由和路由判定。

### 链 - chain

|             |                                           |                            |
| ----------- | ----------------------------------------- | -------------------------- |
| INPUT       | for packets destined  to local  sockets   | 匹配目标 IP 是本机的数据包 |
| FORWARD     | for packets being routed through  the box | 匹配转发数据包             |
| OUTPUT      | for locally-generated packets             | 匹配                       |
| PREROUTING  | incoming packets before routing           |                            |
| POSTROUTING |                                           |                            |



### 规则 - rule

规则包括匹配部分和目标部分：

- 匹配部分（matches）：数据包需要满足的所有条件。
- 目标部分（target）：数据包匹配所有条件后的动作。

匹配部分由各种匹配参数组成，主要包括：

- `-p` ：

- 



目标部分可以是：

- 用户自定义的链：如果条件匹配，跳转到用户定义的链继续处理。如果数据包成功穿过用户链，目标将移动到原始链的下一个规则。
- 内置特定值：如果条件匹配，数据包的动作立刻被决定，并且处理过程会停止。包括 `ACCEPT`，`DROP`，`QUEUE`，`RETURN`。
- 目标扩展：如果条件匹配，可以被终止，也可以不被终止。例如 `REJECT`，`LOG`。

目标使用 `-j, --jump` 或者 `-g, --goto` 选项指定，两者的区别是：

- jump 选项类似于函数跳转返回。如果链 A jump 到用户链 B，执行完用户链 B 或遇到 RETURN 之后，将返回调用链 A，并且继续执行匹配下一条规则。
- goto 选项类似于 goto 语句。如果链 A goto 到用户链 B，执行完用户链 B 或遇到 RETURN 之后，相当于链 A 已经执行完毕，此时将返回调用 A 的前一条链。





## iptables 示例

查看表中所有规则：

```
iptables -nvL
iptables -nvL --line-numbers	# useful for insert,replace and delete a rule
```

在表中**添加/重命名/删除/重置**链：

```
iptables [-t table] -N chain 	# creates a chain in a table

iptables [-t table] -E old-chain new-chain	# Rename the user specified chain to the user supplied name.

iptables [-t table] -X [chain]
iptables -X						# deletes all empty non-default chains in a table
iptables -X [chain_name] 		# deletes the specific empty non-default chains in a table

iptables [-t table] -F [chain]
iptables -F						# flushes all the chains in its current table
iptables -F [chain_name] 		# flushes the specific chain in its current table
```

在链中**增加/插入/替换/删除/查看是否存在**规则：

```
iptables -A chain rule-specification				# append a rule to a chain
iptables -I chain [rulenum] rule-specification		# insert a rule at a specific position on the chain, default is 1, which is the head of the chain.
iptables -R chain rulenum rule-specification		# replacing a rule in the selected chain
iptables -D chain rule-specification				# delete a rule by specification
iptables -D chain rulenum							# delete a rule by number. Rules are numbered starting at 1
iptables -C chain rule-specification				# Check whether a rule matching the specification does exist in the selected chain.
```

链中规则参数：

```
```



## iptables 用法

### 日志记录

LOG 目标可以记录命中规则的数据包，命中之后不会影响原本的转发流程。

在丢弃数据包之前，通过 LOG 目标记录下来

```
iptables -N logdrop
iptables -A logdrop -m limit --limit 5/m --limit-burst 10 -j LOG
iptables -A logdrop -j DROP
```

如果有规则想要记录后丢弃，只需要将动作跳转到 logdrop 链即可。

```
iptables -A INPUT -m conntrack --ctstate INVALID -j logdrop
```

另外，可以使用 `ulogd` 来代替默认的 LOG 目标。