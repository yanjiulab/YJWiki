# TLS/SSL

## TLS 简介

传输层安全协议 (Transport Layer Security, TLS) 及其前身安全套接字层 (Secure Sockets Layer, SSL) 都是旨在为计算机网络提供通信安全性的加密协议，主要目的是在两个或多个通信计算机应用程序之间提供**安全性/隐私性**和**数据完整性**。

TLS 协议的几种版本在 WEB 浏览、电子邮件、即时通讯 (Instant Messaging, IM) 和 IP 语音 (VoIP) 等多种应用程序中被广泛使用。网站可以使用 TLS 来保护其服务器和 Web 浏览器之间的所有通信。

TLS 不能很好的对应 OSI 模型或者 TCP/IP 模型。TLS 运行在某些可靠传输协议（如 TCP）之上，这暗示着它位于传输层之上。它为更高层提供加密，这通常是表示层的功能。但是，**应用程序通常将 TLS 视为传输层**，即使使用 TLS 的应用程序必须**主动控制**发起 TLS 握手以及交换身份验证证书。

### TLS 应用场景
在应用程序设计中，TLS 通常在传输层协议的基础上实现，从而对相关协议的数据进行加密，例如 HTTP、FTP、SMTP、NNTP 和 XMPP。 从历史上看，**TLS 主要用于可靠的传输协议，例如传输控制协议 (TCP)**。但是，它也已通过面向数据报的传输协议来实现，例如用户数据报协议 (UDP) 和数据报拥塞控制协议 (DCCP)，其使用独立术语**数据报传输层安全性 (DTLS)**。

**TLS 的主要用途是用来加密使用 HTTP 协议编码的 Web 浏览器与 Web 服务器之间的万维网流量**，使用 TLS 保护 HTTP 流量的用法构成了 **HTTPS** 协议。

TLS 也可以保护简单邮件传输协议（SMTP），这些应用程序使用公共密钥证书来验证端点的身份。

TLS 也可以用于建立整个网络堆栈的隧道以创建 VPN，OpenVPN 和 OpenConnect 就是这种情况。到目前为止，许多供应商已将 TLS 的加密和身份验证功能与授权结合在一起。自1990年代末以来，在Web浏览器之外创建客户端技术以实现对客户端/服务器应用程序的支持也取得了长足的发展。与传统的 IPsec VPN 技术相比，TLS 在防火墙和 NAT 穿越方面具有一些固有的优势，这使得对大型远程访问人群的管理变得更加容易。

TLS 还是用于保护会话初始协议（SIP）应用程序信令的标准方法。TLS 可用于为与 VoIP 和其他基于 SIP 的应用程序相关的 SIP 信令提供身份验证和加密。

### TLS 发展历史
TLS 从 SSL 发展而来，其间因为安全性问题经历了一系列版本的变迁，一个保证安全性的协议本身存在安全性问题，确实是不容忽视的。不过有一些安全问题不在于 TLS 或 SSL 协议本身，而是其支持的密码协议或客户端实现存在被攻击的漏洞，因此 TLS 协议的安全性也取决于密码和客户端的攻击应对措施。

早期的一些文章可能将 TLS 称为 TLS/SSL，如今 SSL 正在渐渐退出舞台，目前广泛使用的是 TLS 1.2。

|  协议   | 发布时间 |      状态      | 网站支持情况 |
| :-----: | :------: | :------------: | :----------: |
| SSL 1.0 |  未公布  |     未公布     |              |
| SSL 2.0 |  1995年  | 已于2011年弃用 |     1.6%     |
| SSL 3.0 |  1996年  | 已于2015年弃用 |     6.7%     |
| TLS 1.0 |  1999年  | 已于2020年弃用 |    65.0%     |
| TLS 1.1 |  2006年  | 已于2020年弃用 |    75.1%     |
| TLS 1.2 |  2008年  |                |    96.0%     |
| TLS 1.3 |  2018年  |                |    18.4%     |

## TLS 原理

### 加密概念

- 对称加密：密钥可能被截获
- 非对称加密：私钥＋公钥，交换公钥，公钥加密，私钥解密；
- 中间人攻击：截获公钥，替换自己的公钥；
- 数字签名：认证发送者身份 + 数据完整性
- CA：权威机构，用来验证公钥的合法性，并用 CA 私钥签名，生成其数字证书。
- 数字证书 (Digital Certificates)：数字证书包含公钥明文＋数字签名，
- CA 证书：CA 公钥，浏览器用 CA 证书来验证数字证书的合法性，从而得到公钥。

### TLS 加密原理

TLS 协议的基本思路是采用公钥加密法，也就是说，客户端先向服务器端索要公钥，然后用公钥加密信息，服务器收到密文后，用自己的私钥解密。

（1）如何保证公钥不被篡改？

解决方法：将公钥放在数字证书中。只要证书是可信的，公钥就是可信的。

（2）公钥加密计算量太大，如何减少耗用的时间？

解决方法：每一次对话（session），客户端和服务器端都生成一个"对话密钥"（session key），用它来加密信息。由于"对话密钥"是对称加密，所以运算速度非常快，而服务器公钥只用于加密"对话密钥"本身，这样就减少了加密运算的消耗时间。

因此，TLS 协议的基本过程是这样的：

1. 客户端向服务器端索要并验证公钥。
2. 双方协商生成"对话密钥"。
3. 双方采用"对话密钥"进行加密通信。

### TLS 协议架构

TLS 主要分为两层：

- 底层的是 TLS 记录协议 (The TLS Record Protocol)，主要负责使用对称密码对消息进行加密。
- 上层的是 TLS 握手协议 (The TLS Handshaking Protocols)，又具体分为四个协议：
    - 握手协议 (Handshake Protocol) 负责在客户端和服务器端商定密码算法和共享密钥，包括证书认证，是 4 个协议中最最复杂的部分。
    - 密码规格变更协议 (Change Cipher Spec Protocol) 负责向通信对象传达变更密码方式的信号
    - 警告协议 (Alert Protocol) 负责在发生错误的时候将错误传达给对方
    - 应用数据协议 (Application data protocol) 负责将 TLS 承载的应用数据传达给通信对象的协议。

以下重点介绍一下握手协议和记录协议。

## 握手协议

"握手阶段"涉及四次通信，"握手阶段"的所有通信都是明文的。

## 记录协议




## 参考
- [RFC 5246 - TLS v1.2](https://tools.ietf.org/html/rfc5246)
- [RFC 8446 - TLS v1.3](https://tools.ietf.org/html/rfc8446)
- [SSL/TLS工作原理](https://zhuanlan.zhihu.com/p/66029254)
- [Cryptography, Encryption, Hash Functions and Digital Signature](https://medium.com/@ealtili/cryptography-encryption-hash-functions-and-digital-signature-101-298a03eb9462)
- [Is encrypting data with a private key dangerous?](https://security.stackexchange.com/questions/11879/is-encrypting-data-with-a-private-key-dangerous/20362)
- [数字签名](https://www.ruanyifeng.com/blog/2011/08/what_is_a_digital_signature.html)

