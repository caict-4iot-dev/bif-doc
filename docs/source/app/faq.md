# FAQ

## 1.节点部署相关

## 2.SDK相关

2.1 连接节点失败

```json
{"error_code":11007,"error_desc":"Failed to connect to the network","result":{"hash":null}}
```

​    确认节点是否运行正常。

2.2 账号余额不足

```java
Account(did:bid:efnVUgqQFfYeu97ABf6sGm3WFtVXHZB2)'s balance(48145674) - base_reserve(0) is not enough for payment (100000000)
```

​     登录服务管理平台，申请星火通。

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

3.1智能合约支持什么语言？

智能合约目前支持JS、Solidity

3.2js合约调用异常

```js
{"contract":"did:bid:efspy6btdcuzP5BH2N899Ycti5Sd7n3z","exception":"SyntaxError: Unexpected token \r in JSON at position 1457","linenum":34,"stack":"SyntaxError: Unexpected token \r in JSON at position 1457\n at JSON.parse (<anonymous>)\n at main (__enable_check_time__:83:22)"}
```

input参数格式校验，需服务JSON规范。

## 4.交易查询

访问星火网区块链浏览器。

测试网：http://test-explorer.bitfactory.cn/

正式网：https://explorer.bitfactory.cn/

## 5.消息订阅

BIF-Core使用websocket接口实现指定账户地址的交易通知，交易使用protobuf结构。