# 起步

## GO 安装

### Windows

直接官网 next 一路到底。

### Linux

不追求最新版，建议直接使用发行版的包管理器安装。

如果想要特定版本/新版本的 Go，建议使用源码安装。

```
wget -c https://dl.google.com/go/go1.14.2.linux-amd64.tar.gz -O - | sudo tar -xz -C /usr/local
```

Go 将会安装到 `/usr/local/go` 目录下。接着需要将 Go 目录添加到 `$PATH` 环境变量，例如 `/etc/profile`文件（系统范围内安装）或者`$HOME/.profile`文件（当前用户安装）：

```text
export PATH=$PATH:/usr/local/go/bin
```

最后，通过 go 命令验证安装版本成功。

```
$ go version
go version go1.13.8 linux/amd64
```

## Go 命令行工具

Go 安装完之后，便可以使用 `go` 命令行工具来管理 go 代码，基本的命令如下，其他命令后续介绍。

|    命令    |           解释           |
| :--------: | :----------------------: |
| go [help]  |       查看 go 帮助       |
| go version |       查看 go 版本       |
|   go run   |    编译并运行 go 程序    |
|  go build  | 编译 go 程序为可执行文件 |
|   go fmt   |       格式化源文件       |

## GO 开发配置

### 代理配置

Go 安装完毕之后，依照中国特色添加代理。

```
go env -w GO111MODULE=on
go env -w GOPROXY=https://goproxy.io,direct
```

### VS Code 配置

配合 VS Code 编辑器，仅需下载 Go 插件即可使用。

> 注意：需要进行如上代理配置之后，插件方能安装成功。

## Go 示例程序

任意路径下创建 main.go 文件，使用 `go run main.go` 即可编译并运行程序。

```go
package main

import "fmt"

func main() {
    fmt.Printf("Hello, World\n")
}
```

## Go 工程

当项目变大的时候，尤其是引入了第三方包，将不得不处理任何一种编程语言都会遇到的两个问题：

- 如何组织源码？
- 如何管理依赖？

为了解决这个问题，首先需要明白 go 编译运行程序的底层逻辑。

## Go 标准库

## Go 第三方库
