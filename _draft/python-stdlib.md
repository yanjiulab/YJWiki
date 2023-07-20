# 引言

在 [Python 环境管理](http://yjlab.xyz/article/av2) 中介绍了基本编程环境的搭建，在 [Python 笔记](http://yjlab.xyz/article/av2) 中介绍了 Python 语言的基本使用方法。

本文旨在将笔者日常使用的各种**常用的标准库**代码实现方案收集起来，供快速查阅复用。

> 注意：本文并不花费大量笔墨介绍标准库，而是简明扼要的点出标准库的功能，以及给出几个示例程序。因为随着 Python 官方文档中文版面的不断完善，使得编写标准库的使用教程这件事情变得费力而不讨好。

Python 官方文档已经有标准库教程可以参考。

- [Python 标准库](https://docs.python.org/3/library/index.html)
- [标准库简介 —— 第一部分](https://docs.python.org/3/tutorial/stdlib.html)
- [标准库简介 —— 第二部分](https://docs.python.org/3/tutorial/stdlib2.html)

# 命令行参数

## sys 模块

简单的处理命令行参数可以直接使用 sys 模块中的 `sys.argv`。

```
# demo.py 内容
import sys
print(sys.argv)
# 命令行调用
python demo.py one two three
['demo.py', 'one', 'two', 'three']
```

## argparse 模块

[argparse 模块](https://docs.python.org/zh-cn/3/library/argparse.html#module-argparse)提供了一种更复杂的机制来处理命令行参数。

### 基本用法

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('pos', choices=['c1', 'c2'], help='positional argument')
parser.add_argument('-o', '--opt', help='optional argument')
parser.add_argument('-f', '--flag', dest='bar', action='store_true', help='flag argument')
args = parser.parse_args()
print(args)
```

输出内容

```shell
$ python demo.py -h
usage: demo.py [-h] [-o OPT] [-f] {c1,c2}

positional arguments:
  {c1,c2}            positional argument

optional arguments:
  -h, --help         show this help message and exit
  -o OPT, --opt OPT  optional argument
  -f, --flag         flag argument
$ python demo.py c1 -o foo
Namespace(bar=False, opt='foo', pos='c1')
$ python demo.py c1 -o foo -f
Namespace(bar=True, opt='foo', pos='c1')
```

# 子进程交互

## os 模块

TODO

## subprocess 模块

[subprocess 模块](https://docs.python.org/zh-cn/3/library/subprocess.html) 允许你生成新的进程，连接它们的输入、输出、错误管道，并且获取它们的返回码。此模块打算代替一些老旧的模块与功能，例如 `os.system` 等

### 简单执行

简单执行命令，不需要获取命令输出，可以直接使用 run 函数。此时程序将在控制台输出结果。

```python
import subprocess
subprocess.run('ls -l', shell=True)  # style 1
subprocess.run(['ls', '-l'])  # style 2
```

run 的主要参数是第一个 args 参数，即被用作启动进程的参数。可能是一个列表或字符串，如果是字符串则必须指定 `shell=True`，推荐采用第二种方式，这种方式会减少由于各种 shell 转义和空格引起的错误。

### 捕获输出

如果需要对输出做一定处理，则必须获取输出，可以通过以下两种方式实现。

```python
import subprocess
cmd = ['ip', 'address']
p1 = subprocess.run(cmd, capture_output=True)
p2 = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print(p1.stdout)
print(p2.stdout)
```

可以发现，输出都是字节流，如果需要字符串，则需要指定解码方式或者直接解码输出。

```python
p1 = subprocess.run(cmd, capture_output=True, encoding='utf-8')
p2 = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print(p1.stdout)
print(p2.stdout.decode('utf-8'))
```

### 实时输出

我们使用 ping 命令执行 5 次，发现输出是一下子冒出来的。事实上，上述捕获输出的方式是阻塞的，即子程序返回之后，程序才能捕获到输出，然而如果子程序需要运行很久，那么我们便不能及时的处理输出了。

```python
cmd = ['ping', '-c', '5', 'www.baidu.com']
p = subprocess.run(cmd, capture_output=True, encoding='utf-8')
print(p.stdout)
```

如果需要实时处理输出，则需要 Popen 的帮助。

```python
import subprocess

cmd = ['ping', '-c', '5', 'www.baidu.com']
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding='utf-8')
for line in iter(p.stdout.readline, ''):
    print(line, end='')
p.stdout.close()
print('Done')
```

### 输入参数

有时候，我们的命令会开辟一个新的 shell 或者会接管 shell 的输入和输出。例如，执行 `python` 或 `ssh` 命令，我们会进入一个新的环境，此时我们希望可以在这个新的环境中执行代码，就需要将输入传入子进程中。

如果输入比较简单，那么可以直接指定 input 参数。

```python
import subprocess

# not capture output, just print in console
p = subprocess.run('python', input=b'print("hello world")')

# capture output
p = subprocess.run('python', input=b'print("hello world")', capture_output=True)
print(p.stdout)
```

上述方法实际上是将 input 传入了 Popen 对象中，即：

```python
from subprocess import Popen, PIPE
py = Popen('python', stdin=PIPE, stdout=PIPE)
out, err = py.communicate(b'print("hello world")')
print(out, err)
```

然而，communicate 方法其实也是阻塞的，我们可以直接实时输出。

```python
from subprocess import Popen, PIPE

py = Popen('python', stdin=PIPE, stdout=PIPE)
script = b"""
from datetime import datetime
import time
for i in range(10):
    print(datetime.now())
    time.sleep(1)
"""
py.stdin.write(script)
py.stdin.close()
for line in iter(py.stdout.readline, b''):
    print(line)
py.stdout.close()
print('Done')
```

### 多输入命令

假如我们需要 ssh 到服务器上，然后执行一系列操作，那么上述方式就不好用了，同样，我们需要 Popen 的帮助。

```python
from subprocess import Popen, PIPE

cmd = ['ssh', '-t', 'liyanjiu@yjvps']
ssh = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8')
ssh.stdin.write('ls -al\n')
ssh.stdin.write('uptime\n')
ssh.stdin.write('logout\n')
ssh.stdin.close()
for line in iter(ssh.stdout.readline, ''):
    print(line, end='')
ssh.stdout.close()
print('Done')
```

> 如果需要一个实时的交互式的通信方式，利用 subprocess 模块难以实现，可以寻找更高级的库来完成。

# 时间

TODO

# 函数式编程

TODO

# 数学

TODO

# 日志

[logging 模块](https://docs.python.org/zh-cn/3/library/logging.html) 提供了灵活的日志系统，所有的 Python 模块都可能参与日志输出，包括自己的日志消息和第三方模块的日志消息。

```python
import logging

# create logger and set logger level to debug
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create and set formatter and handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()  # create console handler and set level to debug
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
fh = logging.FileHandler('file.log')  # create file handler and set level to info
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

# add handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')
```

# 对象序列化

## pickle 模块

pickle 模块用于 Python 对象结构的二进制序列化和反序列化。

## json 模块

json 模块用于 Python 对象结构的 JSON 格式（它输出 Unicode 文本，尽管在大多数时候它会接着以 UTF-8 编码）的序列化和反序列化。

# 二进制、编码

## struct 模块

[struct 模块](https://docs.python.org/zh-cn/3/library/struct.html) 用于将字节串解读为打包的二进制数据。

利用 struct 解析一个网络数据包的 MAC 帧头，2048 即是 IP 协议类型号码 0x0800 的网络序大小。

```python
import struct

eth_header = b'\x74\x85\xc4\x11\x20\x01\x0c\x7a\x15\xac\xa7\xab\x08\x00'
eth = struct.unpack('!6s6sH', eth_header)
print(eth)  # (b't\x85\xc4\x11 \x01', b'\x0cz\x15\xac\xa7\xab', 2048)
```

## base64 模块

[base64 模块](https://docs.python.org/zh-cn/3/library/base64.html) 将二进制数据编码为可打印的 ASCII 字符以及将这些编码解码回二进制数据的函数。

```python
import base64

en = base64.b64encode(b'yjlab.xyz')
print(en)  # b'eWpsYWIueHl6'
de = base64.b64decode(b'eWpsYWIueHl6')
print(de)  # b'yjlab.xyz'
```
