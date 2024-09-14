

# 2.Solidity合约介绍

## 2.1 星火链Solidity合约语言

在星火链合约账户中，`Solidity`编译后生成的`opCode`指令码会存储到合约账户中，用于合约的执行。

本节主要介绍在星火链中支持的 `Solidity` 合约的特性、语法、功能等。星火链平台支持的`Solidity`语法基本与官方`Solidity`基本一致，目前支持`0.4.26`和`0.8.21`两个版本，**官方建议使用高版本编译器**。

solidity官方文档：

<https://docs.soliditylang.org/en/v0.8.21/>

### 2.1.1 与标准Solidity合约的区别

1. **星火链bid地址支持**：

   星火链`solidity`中 `address`表示的地址，长度为`24`字节，以太坊`solidity`中`address`表示的地址是20字节。

1. **指令支持**：

   星火链上`solidity`不支持`SELFDESCTRUCT`命令。

1. **链机制不同导致的语言差异**：

   星火链上`solidity`不支持`EXTCODEHASH`，`DIFFICULT`指令。

### 2.1.2 合约事件

<a id="event"></a>

在Solidity智能合约开发中，事件（Event）是一个重要的概念，它允许合约在特定情况下通知外部实体，如前端应用或其他合约。事件机制为合约与外部世界提供了一种通信方式，使得外部实体能够实时获取合约内部状态的变化信息。

星火链的Solidity智能合约同样支持合约事件，详细介绍见[Solidity合约事件](./Solidity合约事件介绍.md)。

## 2.2 星火链Solidity合约开发工具

### 2.1.1 Solidity编译器

<a id="solidity_solc"></a>

由于指令集支持和地址表示法的区别, 星火链提供了专用编译器来编译星火链`Solidity`合约. 本节指导开发者使用官方编译器编译星火链智能合约。

npm包地址：[https://www.npmjs.com/package/@bifproject/solc-bif](https://www.npmjs.com/package/@bifproject/solc-bif) 。

1. 下载

   需要电脑上安装nodejs 且版本号>=10.0.0

   ```bash
   npm i -g @bifproject/solc-bif
   npm i -g bs58
   ```

   验证是否安装成功,执行下面的命令不报错

   ```shell
   solcjs --help
   ```

   <img src="..\_static\images\image-20240326091913209.png" style="zoom:100%;" />

2. 编写测试合约

   用一个最简单的测试合约做例子。

   ```
   pragma solidity 0.8.21;
   
   contract test{
       function testfun() public returns(string){
           return "hello world";
       }
   }
   ```

3. 编译合约

   ​	执行编译命令：

   ```shell
   solcjs --bin --abi test.sol
   ```

   执行成功后结果如下，没有Error信息，警告可以忽略。

   <img src="..\_static\images\image-20240514155457977.png"  style="zoom:100%;" />

执行完后会生成两个文件：

```
test_sol_test.abi
test_sol_test.bin
```

接下来就可以使用SDK在星火链上部署调用合约了，详细步骤见[使用SDK快速体验星火链](../quickstart/使用SDK快速体验星火链.md#deploy_solidity)。

### 2.1.2 ABI编解码工具

由于指令集支持和地址表示法的区别, 星火链提供了专门的ABI编解码工具对合约的参数进行编解码。

1. ethereumjs-abi

   星火链提供了专用的abi编解码工具[ethereumjs-abi](https://www.npmjs.com/package/@bifproject/ethereumjs-abi)。

3. 离线API

   星火链的离线API服务支持调用本地API接口实现abi编解码功能，见[离线API abi编解码接口](../instructions/离线API服务使用说明.md)。

### 2.1.3 Openzeppelin 合约模板

OpenZeppelin是一套用Solidity语言编写, 基于EVM架构的**智能合约模板库**。星火链根据许可有的特性，提供了自己的Opnezeppelin合约模板。开发者可以基于星火链的Openzeppelin合约模板开发DAPP, 详见[OpenZeppelin合约模板](./Openzeppelin合约模板.md)。

### 2.1.4 Remix 合约IDE

`Remix` 是用于智能合约开发的Web端集成开发环境 (IDE)。由于其操作简单、功能强大，成为智能合约开发者的首选开发工具，在区块链，特别是以太坊生态中有举足轻重的地位。**Remix合约IDE星火插件**是基于`Remix` IDE的星火链插件，基于此插件，开发者可以更加直观、便捷地在星火链上开发、测试和部署智能合约。详见[Remix IDE 介绍](../RemixIDE星火插件.md)。

### 2.1.5 Hardhat

待开放。
