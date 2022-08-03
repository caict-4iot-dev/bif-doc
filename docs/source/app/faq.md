# FAQ

## 1.节点部署相关

### 1.1 节点启动失败相关问题

#### 1.1.1 启动镜像时端口被占用失败

​    在宿主机上先执行命令：lsof -i:27002，根据查出的PID然后执行kill -9 PID确保端口可映射使用即可继续，如下图所示：

<img src="D:\gitHup\bif-doc\docs\source\_static\images\2022-08-01-16-16-20.png"/>

#### 1.1.2 部署节点运行时p2p，共识等公网不通导致同步数据失败

a.进入docker镜像容器中查看服务错误日志
	vi ./log/bif-err.log
	看到日志文件中有很多关于p2p的链接失败日志信息如含有Got a network failed event 信息。

<img src="D:\gitHup\bif-doc\docs\source\_static\images\2022-07-29-18-10-04.png"/>

b.通过请求http://宿主机ip:27002/getLedger查看部署节点的区块高度是否变化以及和测试网差别是否很大判断节点运行是否正常。

以上任一方法失败代表网络不通，及时通知运维处理公网问题。

### 1.2 节点运行以后服务异常问题：

#### 1.2.1节点进程启动后被kill导致服务停止

    先在宿主机docker ps查看启动的容器ID
    再执行docker exec -it 容器ID/容器NAME /bin/bash进入容器，通过上面的查看进程章节查看进程是否存在
    如果不存在执行nohup ./bin/bif &启动服务
    详细步骤截图已在上述进镜像启动服务相关章节

#### 1.2.2 测试网节点版本升级导致版本差别数据不同步

   通过章节 **4）查看区块同步高度**，查询本节点与测试网区块高度是一直不同步。

  分别请求http://宿主机ip:27002/Hello以及http://test.bifcore.bitfactory.cn/Hello接口，查看节点以及测试网返回的chain_version。

详细返回值格式以及操作如下图：

<img src="D:\gitHup\bif-doc\docs\source\_static\images\2022-08-01-10-35-47.png"/>

综上所述的两点如果区块高度一直不同步并且版本不一致则此时需要进行升级节点版本，根据测试网接口返回的chain_version在宿主机重新执行第一步的拉取命令如docker pull caictdevelop/bif-core:v1.2.1-4重新升级部署即可(最后的:v1.2.1-4就是拼接的上述接口返回的测试网中版本号保持一致即可，所有升级部署如最开始步骤，区别在于此处版本号不同，具体不在赘述)。

#### 1.2.3 机器磁盘满导致服务异常

查看磁盘信息看/dev相关最大的盘符的size以及used字段的值如果一样并且Use占比100%,代表磁盘空间已满导致服务异常需要扩容

```shell
#执行df -h命令
df -h
```

<img src="D:\gitHup\bif-doc\docs\source\_static\images\2022-07-29-18-31-27.png"/>

根据上述查看部署节点的区块高度以及测试网高度一直差别很大并且不在同步了或者上述的问题排查后再查看bif进程已不存在了

## 2.SDK相关

2.1 连接节点失败

```json
{"error_code":11007,"error_desc":"Failed to connect to the network","result":{"hash":null}}
```

​    确认节点是否运行正常,以及配置地址是否正确。

2.2 账号余额不足

```java
Account(did:bid:efnVUgqQFfYeu97ABf6sGm3WFtVXHZB2)'s balance(48145674) - base_reserve(0) is not enough for payment (100000000)
```

​     参照快速上手-获取星火令章节。

2.3 nonce值错误

```java
Transaction nonce(4) too small, the account(did:bid:efBdagu8sVkJWEw5kLt1w69bxa85Kuag) nonce is (5)
```

​    当前nonce=5的基础上+1，发起下一笔交易。

2.4 交易池中存在一笔完全相同的交易（交易hash)一致，则直接插入失败

```json
Received duplicate transaction message. The transaction's source address is did:bid:efnVUgqQFfYeu97ABf6sGm3WFtVXHZB2, and hash is d0cd3c87
```

2.5 某个源账户发的交易，nonce相同，其它参数存在差异（计算出的tx hash不同),则会比较两笔交易的gasprice，如果B>=1.1A ，则用B交易替换A交易；如果B < 1.1A，则提示Drop the transaction to...

```json
Drop the transaction to insert queue because of low fee
```

2.6 权限不足、私钥不正确

```
Transaction(0f3c99381b7bca967bcad2b55d396ff33b375c9aea1cda024f7b705aea1a2e5c) signature weight is not enough
```

## 3.智能合约相关

3.1 智能合约支持什么语言？

智能合约目前支持JS、Solidity

3.2 js合约调用异常

```js
{"contract":"did:bid:efspy6btdcuzP5BH2N899Ycti5Sd7n3z","exception":"SyntaxError: Unexpected token \r in JSON at position 1457","linenum":34,"stack":"SyntaxError: Unexpected token \r in JSON at position 1457\n at JSON.parse (<anonymous>)\n at main (__enable_check_time__:83:22)"}
```

input参数格式校验，需校验JSON规范。

## 4.交易查询

访问星火网区块链浏览器。

测试网：http://test-explorer.bitfactory.cn/

正式网：https://explorer.bitfactory.cn/

* 查询示例：

  <img src="D:/gitHup/bif-doc/docs/source/_static/images/image-20220729095900368.png" alt="image-20220729095900368.png" style="zoom:80%;" />

## 5.消息订阅

BIF-Core使用websocket接口实现指定账户地址的交易通知，交易使用protobuf结构。