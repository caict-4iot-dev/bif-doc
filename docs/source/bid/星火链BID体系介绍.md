# 1.星火链BID体系介绍

星火标识`BID`(`Blockchain-based Identifier`, `BID`)，`BID`标识是基于`W3C DID`标准开发的新型分布式标识，任意实体可自主生成星火标识，不需要中心化注册机构就可以实现全球唯一性，具有**分布式、自主管理、隐私保护和安全易用**等特点，同时根据算法的不同，`BID`支持`39-57`位**变长编码**方式，有效适应各种业务场景，兼容各类设备。

`BID`主要包含以下方面：**BID标识符**、**BID文档**、**BID解析协议**、**基于BID的数字凭证**：

- `BID`标识符：

  - 是基于新型分布式标识符`DID`规范的一种方法，任意实体可自主生成`BID`，不需要中心化注册机构就可以实现全球唯一性；
  - **去中心化、互通**

- `BID`文档： 

  -  `BID`标识符只是表示一个身份的标识符，不包含身份的信息。而`BID`文档就是用于描述身份详细信息的文档，一个`BID`标识符关联到一个`BID`文档。`BID`标识符具体解析为`BID`文档，`BID`文档内包括`BID`标识符和公钥详细信息(持有者、加密算法、密钥状态等)，以及`BID`持有者的其他非隐私属性描述等；
  -  **信息承载**

- `BID`解析协议：

  -  星火·标识深耕物联网领域，自主构建了`BID`解析协议，优化了海量物联网设备的接入场景，同时支持`DID`解析器，为星火·链网智能设备自主交互奠定了基础；
  -  **互通**

- 基于`BID`的数字凭证：

  - 提供了一种规范来描述实体所具有的某些属性。`BID`持有者，可以通过可验证声明，向其他实体证明自己的某些属性是可信的。结合数字签名和零知识证明等密码学技术，可以使得声明更加安全可信，并进一步保障用户隐私不被侵犯；

  - **隐私**

    <img src="../_static/images/145747023-aa985f24-2ef2-4e08-b7ea-c9fa898dc6ec.png"/>

## 1.1 规范

<span id="bid">星火标识编码规范如下：</span>

<img src="../_static/images/144978971-1e240d08-2569-4777-8c94-21c2681766d7.png"/>

由前缀`Prefix`、共识码（`AC号`）、加密类型、编码类型、后缀组成。

## 1.2 实现

- [BID标识符](https://bif-doc.readthedocs.io/zh_CN/2.0.0/bid/BID%E6%A0%87%E8%AF%86%E7%AC%A6.html)
- [BID文档](https://bif-doc.readthedocs.io/zh_CN/2.0.0/bid/BID%E6%96%87%E6%A1%A3.html)
- [BID解析协议](https://bid-resolution-protocol-doc.readthedocs.io/zh_CN/latest/doc/%E6%98%9F%E7%81%AB%C2%B7%E9%93%BE%E7%BD%91BID%E5%8D%8F%E8%AE%AE.html#id5)
- [BID数字身份服务](https://bif-doc.readthedocs.io/zh_CN/2.0.0/bid/%E6%95%B0%E5%AD%97%E8%BA%AB%E4%BB%BD%E6%9C%8D%E5%8A%A1.html)

## 1.3 其他说明

- [BID-SDK](https://bif-doc.readthedocs.io/zh_CN/2.0.0/bid/BID-SDK.html)

- [浏览器插件钱包](https://bif-doc.readthedocs.io/zh_CN/2.0.0/bid/%E6%B5%8F%E8%A7%88%E5%99%A8%E6%8F%92%E4%BB%B6%E9%92%B1%E5%8C%85.html)

- [BID标识查询服务](https://bif-doc.readthedocs.io/zh_CN/2.0.0/bid/BID%E6%A0%87%E8%AF%86%E6%9F%A5%E8%AF%A2.html)
