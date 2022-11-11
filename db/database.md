# 数据库

## 数据库基础

### SQL 数据库

SQL 数据库又称关系型数据库，基于 SQL 语言实现数据库的操作，典型代表为 MySQL 。

### NoSQL 数据库

NoSQL 数据库又称非关系型数据库，可以大体上分为4个种类：

|                   种类                    |         特性         |  代表   |
| :---------------------------------------: | :------------------: | :-----: |
|             键值（Key-Value）             | 使用方式类似于哈希表 |  Redis  |
|       面向文档（Document-Oriented）       |                      | MongoDB |
| 列存储（Wide Column Store/Column-Family） |                      |  HBase  |
|           面向图 Graph-Oriented           |                      |         |

## MySQL

### MySQL 安装

[MySQL Downloads](https://www.mysql.com/downloads/) 提供了几种版本，包括：

- Oracle MySQL Cloud Service (commercial)
- MySQL Enterprise Edition (commercial)
- MySQL Cluster CGE (commercial)
- MySQL Community Edition (GPL)

作为个人学习使用，选择 GPL 授权的社区版 [MySQL Community Edition](https://dev.mysql.com/downloads/) 已经足够。

MySQL Community 包含了各种组件，例如：

- MySQL Community Server (GPL) 是全球最流行的开源数据库服务器，提供了各种平台的安装方式。
- MySQL Cluster (GPL) 是一个实时的开源事务数据库
- MySQL Router (GPL) 是轻量级中间件，可在您的应用程序和任何后端MySQL服务器之间提供透明路由。
- MySQL Workbench (GPL) 是一套数据库设计可视化程序，通过图形界面设计、管理、记录数据库。
- MySQL Connectors 提供了其他应用程序/编程语言的标准接口驱动
- ...

除此之外还包含了一些针对不同平台的安装向导：

- MySQL on Windows (Installer & Tools) 
- MySQL Yum Repository
- MySQL APT Repository
- MySQL SUSE Repository

### MySQL 存储引擎

MySQL 存储引擎有两种：

- **InnoDB** 是 MySQL 默认的事务型存储引擎，只有在需要它不支持的特性时，才考虑使用其它存储引擎。

- MyISAM 设计简单，数据以紧密格式存储。对于只读数据，或者表比较小、可以容忍修复操作，则依然可以使用它。

### MySQL 索引

索引的目的在于**提高查询效率**，类似于字典的目录。通过索引数据库可以不断的缩小想要获得数据的范围，从而筛选出最终想要的结果。但是索引并不是适用于所有的场合：

- 对于非常小的表、大部分情况下简单的全表扫描比建立索引更高效；
- **对于中到大型的表，索引就非常有效；**
- 但是对于特大型的表，建立和维护索引的代价将会随之增长。这种情况下，需要用到一种技术可以直接区分出需要查询的一组数据，而不是一条记录一条记录地匹配，例如可以使用分区技术。

索引是在**存储引擎层**实现的，而不是在服务器层实现的，所以不同存储引擎具有不同的索引类型和实现。从数据结构的角度来看，支持搜索操作的集合底层可以组织为以下几种数据结构：

- Binary Search Tree
- Red-Black Tree
- B-Tree
- B+Tree
- Hash Table

首先排除二叉查找树，其最坏查找性能为 $O(n)$，而这种最坏场景又很容易在数据库中出现。

B-Tree 指的是 Balance Tree，也就是平衡树。平衡树是一颗查找树，并且所有叶子结点位于同一层。

B+ Tree 是基于 B-Tree 和**叶子结点顺序访问指针**进行实现，它具有 B-Tree 的平衡性，并且通过顺序访问指针来提高区间查询的性能。

在 B+ Tree 中，**一个结点中的 key 从左到右非递减排列**，如果某个指针的左右相邻 key 分别是 keyi 和 keyi+1，且不为 null，则该指针指向结点的所有 key 大于等于 keyi 且小于等于 keyi+1。

B+Tree 的特征为：

- 内部结点不存 data，只存 key（冗余），因此每个结点能够存放更多的 key。
- 外部结点包含所有 key 和 data。
- 叶子结点通过指针链接。

进行查找操作时，首先在根结点进行二分查找，找到一个 key 所在的指针，然后递归地在指针所指向的结点进行查找。直到查找到叶子结点，然后在叶子结点上进行二分查找，找出 key 所对应的 data。

插入删除操作会破坏平衡树的平衡性，因此在插入删除操作之后，需要对树进行一个**分裂、合并、旋转**等操作来维护平衡性。

红黑树等平衡树也可以用来实现索引，但是**文件系统及数据库系统普遍采用 B+ Tree 作为索引结构**，主要有以下两个原因：

1. **更少的查找次数**。在算法分析中，平衡树性能各有千秋，但大致不会差的过于离谱。但问题的关键在于，这些复杂度模型是基于每次相同的操作成本来考虑的，而数据库实现比较复杂，**数据保存在磁盘上**，而为了提高性能，每次又可以把部分数据读入内存来计算，因为我们知道访问磁盘的成本大概是访问内存的十万倍左右。平衡树查找操作的时间复杂度和树高 h 相关，$O(h)=O(\log_d N)$，其中 d 为每个结点的出度。红黑树的出度为 2，而 B-Tree 和 B+Tree 的出度一般都非常大，所以红黑树的树高 h 很明显大，查找的次数也就更多。因此，过高的树导致更多的磁盘 IO 操作，从而影响了效率。
2. **利用磁盘预读特性**。考虑到磁盘 IO 是非常高昂的操作，计算机操作系统做了一些优化，当一次 IO 时，不光把当前磁盘地址的数据，而是把相邻的数据也都读取到内存缓冲区内，因为局部预读性原理告诉我们，当计算机访问一个地址的数据的时候，与其相邻的数据也会很快被访问到。每一次 IO 读取的数据称之为一页 (page)。具体一页有多大数据跟操作系统有关，一般为 4k 或 8k，也就是我们读取一页内的数据时候，实际上才发生了一次 IO，这个理论对于索引的数据结构设计非常有帮助。

## Redis

Redis 是速度非常快的非关系型（NoSQL）内存键值数据库，可以存储键和五种不同类型的值之间的映射。

键的类型只能为字符串，值支持五种数据类型：字符串、列表、集合、散列表、有序集合。

Redis 支持很多特性，例如将内存中的数据持久化到硬盘中，使用复制来扩展读性能，使用分片来扩展写性能。

### Redis 数据类型

| 数据类型 |      可以存储的值      | 操作                                                         |
| :------: | :--------------------: | ------------------------------------------------------------ |
|  STRING  | 字符串、整数或者浮点数 | 对整个字符串或者字符串的其中一部分执行操作<br>对整数和浮点数执行自增或者自减操作 |
|   LIST   |          列表          | 从两端压入或者弹出元素<br>对单个或者多个元素进行修剪，<br>只保留一个范围内的元素 |
|   SET    |        无序集合        | 添加、获取、移除单个元素<br>检查一个元素是否存在于集合中<br>计算交集、并集、差集<br>从集合里面随机获取元素 |
|   HASH   | 包含键值对的无序散列表 | 添加、获取、移除单个键值对<br>获取所有键值对<br>检查某个键是否存在 |
|   ZSET   |        有序集合        | 添加、获取、删除元素<br>根据分值范围或者成员来获取元素<br>计算一个键的排名 |

### 参考

- https://cyc2018.github.io/CS-Notes/#/notes/Redis

## MongoDB

MongoDB 是一个具有可伸缩性和灵活性的**文档数据库 (Document Database)**，具体可以查看 [官网](https://www.mongodb.com)。

### MongoDB 安装

各种平台的安装、运行方式请参考 [Install MongoDB](https://docs.mongodb.com/manual/installation/)。以下仅以 Ubuntu 20.04 平台上安装 MongoDB 社区版为例，大致流程为：

1. 导入包管理系统使用的公钥
2. 创建 apt 源的 list 文件（国内源过慢可以替换阿里源 `http://mirrors.aliyun.com/mongodb/apt/ubuntu`）
3. 更新本地 apt 数据库
4. 安装

```shell
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org
```

### MongoDB 运行

按照以下步骤在系统上运行 MongoDB 社区版：

1. 查看系统 init 管理类型（大部分 Linux 如今采用 systemd 管理服务）
2. 启动 mongodb 服务（如果启动失败请查看官方文档）
3. 查看 mongodb 服务状态
4. （可选，推荐）设为开机启动项
5. （其他）停止 mongodb 服务
6. （其他）重启 mongodb 服务

```
ps --no-headers -o comm 1   # 假设为 systemd
sudo systemctl start mongod
sudo systemctl status mongod
sudo systemctl enable mongod
sudo systemctl stop mongod
sudo systemctl restart mongod
```


mongo 启动失败解决方案：

```
sudo mkdir /var/lib/mongodb
sudo mkdir /var/log/mongodb
sudo chown -R mongodb:mongodb /var/lib/mongodb
chown -R mongodb:mongodb /var/log/mongodb
```

### MongoDB 配置

mongodb 的配置文件为 `/etc/mongodb.conf`。

允许所有 IPv4 以及 IPv6 地址访问：

- 可直接设置 `bindIpAll: true`
- 也可以设置 `bindIp: 0.0.0.0,::`

```
net:
  port: 27017
  bindIp: 0.0.0.0,::
```

### MongoDB 基本概念

| SQL 术语/概念 | MongoDB 术语/概念 | 解释/说明                                |
| ------------- | ----------------- | ---------------------------------------- |
| database      | database          | 数据库                                   |
| table         | collection        | 数据库表/集合                            |
| row           | document          | 数据记录行/文档                          |
| column        | field             | 数据字段/域                              |
| index         | index             | 索引                                     |
| table joins   |                   | 表连接，MongoDB 不支持                   |
| primary key   | primary key       | 主键,MongoDB 自动将 `_id` 字段设置为主键 |

下图表示了传统 SQL 数据库表和 Mongo 数据库集合的表达形式对应关系：

![](database.assets/Figure-1-Mapping-Table-to-Collection-1.png)

### MongoDB 编程接口

MongoDB 官方支持多种编程语言的[驱动库](https://docs.mongodb.com/drivers/)，可以方便开发人员将应用程序连接到数据库。


### 参考

- [mongodb 主从配置及备份](https://www.jianshu.com/p/647ddfd1f5d7)
- [MongoDB 集群搭建 —— 主从模式](https://www.jianshu.com/p/aec4899df434)
- https://blog.csdn.net/pelick/article/details/8644116