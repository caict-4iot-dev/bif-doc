# 3.Nodejs SDK使用说明

## 3.1 基本概念定义

`SDK`是业务模块与星火链交互的桥梁，提供安全可靠的通信信道。

提供的接口，覆盖离线api、账号管理、合约管理、区块管理、交易管理等场景，满足了不同的业务场景需要。

### 名词解析

+ 账户服务： 提供账户相关的有效性校验、创建与查询接口
+ 合约服务： 提供合约相关的有效性校验、创建与查询接口
+ 交易服务： 提供构建交易及交易查询接口
+ 区块服务： 提供区块的查询接口
+ 账户nonce值： 每个账户都维护一个序列号，用于用户提交交易时标识交易执行顺序的

**注意**：为了保证数字精度，请求参数中的**Number**类型，全都按照**字符串**处理，例如：amount = 500， 那么传递参数时候就将其更改为 amount = '500' 字符串形式。

## 3.2  环境准备

### 3.2.1 软件依赖

nodejs： nodejs 14.0.0+

下载地址：https://nodejs.org/dist/

若已安装，请通过命令查看版本：

```shell
$ node --version
v14.0.0
```

### 3.2.2 下载安装

```sh
$ git clone -b release/1.0.1  --depth=1 https://github.com/caict-4iot-dev/BIF-Core_SDK-JS.git
```

## 3.3  怎么使用SDK

#### 初始化SDK

示例

```go
const BIFCoreSDK = require('bifcore-sdk-nodejs');
const sdk = new BIFCoreSDK({
    host: 'http://test.bifcore.bitfactory.cn' //host为星火链RPC地址
}) 
```

### 3.3.1 SDK 离线API

离线API主要是账户和密码学相关API, 不需要连接星火链网RPC接口也能工作. 主要接口如下:

#### 账户生成

1. 接口 ` key.GetBidAndKeyPair()`

1. 用途:

    用来生成一个星火链bid地址和对应私钥

1. 示例

    ```javascript
        const KeyPairEntity = sdk.keypair.getBidAndKeyPair()
	    const encAddress = KeyPairEntity.encAddress
        const encPublicKey = KeyPairEntity.encPublicKey
        const encPrivateKey = KeyPairEntity.encPrivateKey
        const rawPublicKey = KeyPairEntity.rawPublicKey
        const rawPrivateKey = KeyPairEntity.rawPrivateKey
    ```


#### 加密私钥生成keystore

1. 接口 `generateKeyStore(encPrivateKey,password)`

1. 用途:

    用一个密码来加密保护私钥, 得到一个json表示的keystore, 对应密码不泄露的情况下, 可以公开保存.

1. 示例

    ```javascript
    const  encPrivateKey = 'priSrrstxpMCKMa9G6d41rZ4iwzKbGeqJrXqeWZYXVo2pct24L'
	const  password = 'bif8888'
     //生成密钥存储器
    const keyStore = sdk.keypair.generateKeyStore(encPrivateKey,password)
    ```

### 3.3.2 SDK 在线API

在线API主要用于向星火链上发出交易和查询合约, 需要初始化SDK连接后使用.

#### 账户处理接口

1. 查询账户信息

    1. 接口 `account.getAccountBalance(param)`

    1. 用途:

        用来获取一个账户当前信息

    1. 示例
        ```javascript
            // 初始化请求参数
            let param = {
                address: 'did:bid:eft6d191modv1cxBC43wjKHk85VVhQDc'
            }
            let data = await sdk.account.getAccountBalance(param)
    	    console.log('getAccountBalance() : ',  JSON.stringify(data))
        ```
    
1. 获取账户nonce

    1. 接口 `getNonce(param)`

    1. 用途:

        用来获取一个账户当前nonce值, 有关nonce含义, 请参照星火链开发基础章节.

    1. 示例:
        ```javascript
        	// 初始化请求参数
            let param = {
                address: 'did:bid:eft6d191modv1cxBC43wjKHk85VVhQDc'
            }
            let data = await sdk.account.getNonce(param)
            console.log('getNonce() : ',  JSON.stringify(data))
        ```
    
1. 获取账户余额

    1. 接口 `account.getAccountBalance(param)`

    1. 用途:

        用来获取一个账户当前的XHT余额.

    1. 示例:

        ```javascript
            // 初始化请求参数
            let param = {
                address: 'did:bid:eft6d191modv1cxBC43wjKHk85VVhQDc'
            }
            let data = await sdk.account.getAccountBalance(param)
            console.log('getAccountBalance() : ',  JSON.stringify(data))
        ```

#### Block相关接口

1. 获取当前块高度

    1. 接口 `block.getBlockNumber()`

    1. 用途:

        获取当前链上最新的Block号

    1. 示例:

        ```javascript
            let data = await sdk.block.getBlockNumber()
            console.log('getBlockNumber() : ',  JSON.stringify(data))
        ```
    
1. 获取指定块内的交易列表

    1. 接口 `block.getTransactions(param)`

    1. 用途:

        给定block号,获取该block内的交易列表信息

    1. 示例:

        ```javascript
            // 初始化请求参数
            let param = {
                blockNumber: '1'
            }
            let data = await sdk.block.getTransactions(param)
            console.log('getTransactions() : ',  JSON.stringify(data))
        ```
    
1. 获取指定块的统计信息

    1. 接口 `block.getBlockInfo(param)`

    1. 用途:

        给定block号, 查询指定block的信息.

    1. 示例:

        ```javascript
            // 初始化请求参数
            let param = {
                blockNumber: '61360'
            }
            let data = await sdk.block.getBlockInfo(param)
            console.log('getBlockInfo() : ',  JSON.stringify(data))
        ```
    
1. 查询最新块的信息

    1. 接口 `block.getBlockLatestInfo()`

    1. 用途:

        获取当前最新块的信息.

    1. 示例:

        ```javascript
            let data = await sdk.block.getBlockLatestInfo()
            console.log('getBlockLatestInfo() : ',  JSON.stringify(data))
        ```

#### Transaction相关接口

1. 获取指定交易相关信息

    1. 接口 `transaction.getTransactionInfo(param)`

    1. 用途:

        获取指定交易的详细信息

    1. 示例:

        ```javascript
            // 初始化请求参数
            let param = {
                hash: '0390905e5970f1bf262b37fc11d7b2b4b5e28d9a33006584c4940c60fd283518'
            }
            let data = await sdk.transaction.getTransactionInfo(param)
            console.log('getTransactionInfo() : ',  JSON.stringify(data))
        ```


1. 提交交易

    1. 接口 `transaction.submitTrans(serialization,signData)`

    1. 用途:

        提交交易到星火链网

    1. 示例:

        ```javascript
           // 初始化参数
            let serialization = ''
            let privateKey = 'priSPKqYp19ghxeCykHUrepLRkCRD3a2a9y5MJGF8Kc4qfn2aK'
            // sign serialization
            let signData = sdk.transaction.signTransSerialization([ privateKey ]
            ,serialization)
            console.log('signData : ',  signData)
            //  submit transaction
            let transactionInfo = await sdk.transaction.submitTrans(
                serialization,
                signData
            })
            console.log('BIFSubmit() : ',  JSON.stringify(transactionInfo))
        ```

#### 合约相关接口

1. 部署合约

    1. 接口 `contract.createContract(param)`

    1. 用途:

        部署合约到星火链上

    1. 示例:

        ```javascript
            // 初始化请求参数
            let param = {
                sourceAddress:'did:bid:efQMuPahc3zm7abBUBfj22xZokhZ7rED',
                privateKey:'priSPKqSR8vTVJ1y8Wu1skBNWMHPeu8nkaerZNKEzkRq3KJix4',
                payload:"\"use strict\";function init(bar){/*init whatever you want*/return;}function main(input){let para = JSON.parse(input);if (para.do_foo)\n            {\n              let x = {\n                \'hello\' : \'world\'\n              };\n            }\n          }\n          \n          function query(input)\n          { \n            return input;\n          }\n        ",
                initBalance:'1',
                remarks:'create account',
                type:'0',
                feeLimit:'100100000',
                gasPrice:'',
                ceilLedgerSeq:'',
                initInput:''
            }
            let data = await sdk.contract.createContract(param)
            console.log('createContract() : ',  JSON.stringify(data))
        ```
    
1. 从部署交易中获取合约地址

    1. 接口 `contract.getContractAddress(param)`

    1. 用途:

        提供部署合约的交易哈希, 返回合约地址

    1. 示例

        ```javascript
            // 初始化请求参数
            let param = {
                hash: '59228dfa8fcd1e65b918dbe30096302f3a4b136d2762200029ed397496f96ada'
            }
            let data = await sdk.contract.getContractAddress(param)
            console.log('getContractAddress() : ',  JSON.stringify(data))
        ```
    
1. 获取合约相关信息

    1. 接口 `contract.getContractInfo(param)`

    1. 用途:

        指定合约地址, 获取合约相关信息.

    1. 示例

        ```javascript
            // 初始化请求参数
            let param = {
                contractAddress: 'did:bid:efL7d2Ak1gyUpU4eiM3C9oxvbkhXr4Mu'
            }
            let data = await sdk.contract.getContractInfo(param)
            console.log('getContractInfo() : ',  JSON.stringify(data))
        ```
    
1. 查询合约

    1. 接口 `contract.contractQuery(param)`

    1. 用途:

        调用合约Query接口, 查询合约数据

    1. 示例:

        ```javascript
            // 初始化请求参数
        	let param = {
                sourceAddress:'',
                contractAddress:'did:bid:efL7d2Ak1gyUpU4eiM3C9oxvbkhXr4Mu',
                input:'',
                feeLimit: '',
                gasPrice: ''
             }
            let data = await sdk.contract.contractQuery(param)
            console.log('contractQuery() : ',  JSON.stringify(data))
        ```
    
1. 调用合约

    1. 接口 `contract.contractInvoke(param)`

    1. 用途:

        在链上发出交易调用合约可写接口

    1. 示例:

        ```javascript
            // 初始化请求参数
        	let param = {
                sourceAddress:'did:bid:efQMuPahc3zm7abBUBfj22xZokhZ7rED',
                privateKey:'priSPKqSR8vTVJ1y8Wu1skBNWMHPeu8nkaerZNKEzkRq3KJix4',
                contractAddress:'did:bid:efL7d2Ak1gyUpU4eiM3C9oxvbkhXr4Mu',
                ceilLedgerSeq:'',
                feeLimit:'',
                gasPrice: '',
                remarks:'contractInvoke',
                amount:'0',
                input:''
             }
            let data = await sdk.contract.contractInvoke(param)
            console.log('contractInvoke() : ',  JSON.stringify(data))
        ```
