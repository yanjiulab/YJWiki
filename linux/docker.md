# Docker Usage

## docker 守护进程 (Daemon)

### 启动

systemctl start docker.service

### 开机自启动

systemctl enable docker.service

## 语法

```
Usage:  docker [OPTIONS] COMMAND

A self-sufficient runtime for containers

Management Commands:
  app*        Docker App (Docker Inc., v0.9.1-beta3)
  builder     Manage builds
  buildx*     Docker Buildx (Docker Inc., v0.8.2-docker)
  config      Manage Docker configs
  container   Manage containers
  context     Manage contexts
  image       Manage images
  manifest    Manage Docker image manifests and manifest lists
  network     Manage networks
  node        Manage Swarm nodes
  plugin      Manage plugins
  scan*       Docker Scan (Docker Inc., v0.17.0)
  secret      Manage Docker secrets
  service     Manage services
  stack       Manage Docker stacks
  swarm       Manage Swarm
  system      Manage Docker
  trust       Manage trust on Docker images
  volume      Manage volumes

Commands:
  attach      Attach local standard input, output, and error streams to a running container
  build       Build an image from a Dockerfile
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes to files or directories on a container's filesystem
  events      Get real time events from the server
  exec        Run a command in a running container
  export      Export a container's filesystem as a tar archive
  history     Show the history of an image
  images      List images
  import      Import the contents from a tarball to create a filesystem image
  info        Display system-wide information
  inspect     Return low-level information on Docker objects
  kill        Kill one or more running containers
  load        Load an image from a tar archive or STDIN
  login       Log in to a Docker registry
  logout      Log out from a Docker registry
  logs        Fetch the logs of a container
  pause       Pause all processes within one or more containers
  port        List port mappings or a specific mapping for the container
  ps          List containers
  pull        Pull an image or a repository from a registry
  push        Push an image or a repository to a registry
  rename      Rename a container
  restart     Restart one or more containers
  rm          Remove one or more containers
  rmi         Remove one or more images
  run         Run a command in a new container
  save        Save one or more images to a tar archive (streamed to STDOUT by default)
  search      Search the Docker Hub for images
  start       Start one or more stopped containers
  stats       Display a live stream of container(s) resource usage statistics
  stop        Stop one or more running containers
  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
  top         Display the running processes of a container
  unpause     Unpause all processes within one or more containers
  update      Update configuration of one or more containers
  version     Show the Docker version information
  wait        Block until one or more containers stop, then print their exit codes

```



## 镜像 (image)

### 常用命令

|      功能      |                            命令                             |                             备注                             |
| :------------: | :---------------------------------------------------------: | :----------------------------------------------------------: |
|  列出所有镜像  |            `docker images`<br>`docker image ls`             |                                                              |
|    获取镜像    |                 `docker pull IMG_NAME:TAG`                  |                     默认使用 latest 标签                     |
|    删除镜像    |                  `docker rmi IMG_NAME:TAG`                  |                                                              |
| 从容器更新镜像 | `docker commit -m "DESC" -a "AUTHOR" CONTAINER_ID IMG_NAME` | `docker commit -m "change libc version" -a "liyanjiu" 60118fc51c7c alpine:glibc` |
|    构建镜像    |                `docker build -t IMG_NAME .`                 |                  当前目录下需有 Dockerfile                   |
|  设置镜像标签  |              `docker tag IMG_ID IMG_NAME:TAG`               |                                                              |

### Dockerfile

## 容器 (container)

### 常用命令

|             功能             |                             命令                             |                 备注                 |
| :--------------------------: | :----------------------------------------------------------: | :----------------------------------: |
|           启动容器           |                   `docker run -it alpine`                    |      详细参数见 docker run 章节      |
| 容器文件拷贝（容器到宿主机） |      `docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH`      |                                      |
| 容器文件拷贝（宿主机到容器） |     `docker cp [OPTIONS] SRC_PATH|- CONTAINER:DEST_PATH`     |                                      |
|          重命名容器          | `docker rename OLD NEW`<br>`docker container rename OLD NEW` |                                      |
|     查看容器所有底层信息     |         `docker inspect CONTAINER [-f GO_TEMP_STR]`          | 详细格式字符串见 docker inspect 章节 |

### docker run/exec/attach

docker run -it alpine

- i：交互式操作
- t：终端

docker attach 是将标准输入输出连接到容器。

### docker inspect

| 功能           | 命令                                                     |
| -------------- | -------------------------------------------------------- |
| 查看 IP 地址   | `docker inspect mc -f '{{.NetworkSettings.IPAddress}}'`  |
| 查看 MAC 地址  | `docker inspect mc -f '{{.NetworkSettings.MacAddress}}'` |
| 查看容器进程号 | `docker inspect mc -f '{{.State.Pid}}'`                  |

可以考虑将常用功能抽离为 shell 函数，例如：

```bash
# dip CONTAINER 获取容器 PIM
function dip {
	docker inspect -f '{{.State.Pid}}' $1
}
```



### Q&A

Q：如何查看容器和宿主机的 veth 对应关系？

A：分别在容器和宿主机中使用 `ip link` 查看接口名称和接口序号，其中接口名称格式为 `本地接口名@对端接口序号`。由于 veth 对都是成对创建的，所以每次需要占用 2 个接口序号，因此宿主机中的接口序号和 docker 中的接口序号应当相邻。如果需要确认接口序号，可以使用 `ip -d link show` 查看接口信息，其格式为 `接口序号: 接口名@对端接口序号`。



Q：为何 `ip netns list` 看不到容器对应的 netns？

A：该命令只能查看 `/var/run/netns` 下面的数据，而 docker 把 netns 创建到了其他地方。



Q：如何查看容器对应的 netns ？

A：使用 `ln -s /proc/$PID/ns/net /var/run/netns/CONTAINER` 建立 ip netns 可见的软连接，其中 PID 为容器的 PID，CONTAINER 为容器名或容器 ID。



Q：如何为容器添加新网卡？

A：首先创建网桥，其次使用 `docker network connect BR_NAME CONTAINER` 将容器连接到网桥即可。

## 网络 (network)



### 常用命令

| 功能           | 命令                                       | 备注                                               |
| -------------- | ------------------------------------------ | -------------------------------------------------- |
| 列出所有网桥   | `docker network ls`                        |                                                    |
| 创建网桥       | `docker network create NET type TYPE`      |                                                    |
| 容器连接到网桥 | `docker network connect BR_NAME CONTAINER` | `docker network connect br-lan agitated_lederberg` |



## 问题

Q: alpine 不能执行可执行文件
A: 这是由于 alpine 采用的是 musl.libc 而不是 gcc.libc，但二者是兼容的。
mkdir /lib64 && ln -s /lib/libc.musl-x86_64.so.1 /lib64/ld-linux-x86-64.so.2

