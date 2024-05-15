

# 3.Solidity合约介绍

## 3.1 星火链Solidity合约语言

在星火链合约账户中，`Solidity`编译后生成的`opCode`指令码会存储到合约账户中，用于合约的执行。

本节主要介绍在星火链中支持的 `Solidity` 合约的特性、语法、功能等。星火链平台支持的`Solidity`语法基本与官方`Solidity`基本一致，目前支持`0.4.26`和`0.8.21`两个版本，**官方建议使用高版本编译器**。

solidity官方文档：

<https://docs.soliditylang.org/en/v0.8.21/>

### 3.1.1 与标准Solidity合约的区别

1. **星火链bid地址支持**: 

   星火链`solidity`中 `address`表示的地址，长度为`24`字节，以太坊`solidity`中`address`表示的地址是20字节。

1. **指令支持**

   星火链上`solidity`不支持`SELFDESCTRUCT`命令。

1. **链机制不同导致的语言差异**

   星火链上`solidity`不支持`EXTCODEHASH`，`DIFFICULT`指令。

## 3.2 星火链Solidity合约开发工具

### 3.1.1 Solidity编译器

<a id="solidity_solc"></a>

由于指令集支持和地址表示法的区别, 星火链提供了专用编译器来编译星火链`Solidity`合约. 本节指导开发者使用官方编译器编译星火链智能合约。

npm包地址：https://www.npmjs.com/package/@bifproject/solc-bif 

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

   ![image-20240326091913209](..\_static\images\image-20240326091913209.png)

2. 编写测试合约

   用一个最简单的测试合约做例子.

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

   执行成功后结果如下，没有Error信息，警告可以忽略

   ![image-20240514155457977](C:\Users\zhang\AppData\Roaming\Typora\typora-user-images\image-20240514155457977.png)

执行完后会生成两个文件：

```
test_sol_test.abi
test_sol_test.bin
```

接下来就可以使用SDK在星火链上部署调用合约了，详细步骤见[使用SDK快速体验星火链](../quickstart/使用SDK快速体验星火链.md#deploy_solidity)。

### 3.1.2 ABI编解码工具

由于指令集支持和地址表示法的区别, 星火链提供了专门的ABI编解码工具对合约的参数进行编解码.

1. ethereumjs-abi

   星火链提供了专用的abi编解码工具[ethereumjs-abi](https://www.npmjs.com/package/@bifproject/ethereumjs-abi)

2. SDK

   星火链的SDK支持solidity合约abi编解码功能，见[SDK abi编解码]()

3. 离线API

   星火链的离线API服务支持调用本地API接口实现abi编解码功能，见[离线API abi编解码接口]()

### 3.1.3 Openzeppelin 合约模板

OpenZeppelin是一套用Solidity语言编写, 基于EVM架构的**智能合约模板库**。

### 3.1.4 Remix 合约IDE



### 3.1.5 Hardhat

待开放。

## 3.3 星火链Solidity合约开发详细示例



2. 选项说明

    镜像下载之后，需要启动镜像进入容器中，可以使用`solc --help` 来查看此工具支持的参数说明。

    常用选项说明：

    ```bash
    --opcodes            Opcodes of the contracts.
    --bin                Binary of the contracts in hex.
    --abi                ABI specification of the contracts.
    ```

3. 编写测试合约

    用一个最简单的测试合约做例子.

    ```js
    
    ```
    
4. 编译合约

    ```js
    # 启动镜像
    docker run -it caictdevelop/bif-solidity:v0.4.26 /bin/bash
    cd /root/solidity/build/solc
    ./solc --bin test.sol
    
    ======= test.sol:test =======
    Binary: 
    608060405234801561001057600080fd5b5061013f8061002060003960
    00f300608060405260043610610041576000357c010000000000000000
    0000000000000000000000000000000000000000900463ffffffff1680
    63031153c214610046575b600080fd5b34801561005257600080fd5b50
    61005b6100d6565b604051808060200182810382528381815181526020
    0191508051906020019080838360005b8381101561009b578082015181
    840152602081019050610080565b50505050905090810190601f168015
    6100c85780820380516001836020036101000a03191681526020019150
    5b509250505060405180910390f35b6060604080519081016040528060
    0b81526020017f68656c6c6f20776f726c640000000000000000000000
    000000000000000000008152509050905600a165627a7a723058201a4c
    9bfcbee5d683f6e46525cf17db2dd46a6ecf5c3f45cbdd148229639263
    480029
    ```

5. 部署调用

    后续的合约部署调用流程参见**快速入门-4.快速接入星火链**章节。
