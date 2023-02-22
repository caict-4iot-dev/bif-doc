# 5.离线API服务使用说明

离线API主要是账户和密码学相关API, 不需要连接星火链网RPC接口也能工作。具体操作、接口如下:

## 5.1 部署服务

### 5.1.1 获取镜像

```shell
docker pull caictdevelop/bif-offline-api:v1.0.0 
```

### 5.1.2 启动服务

```sh
docker run -d -p 8888:8888 --name bif-offline-api --restart always caictdevelop/bif-offline-api:v1.0.0
```

### 5.1.3 查询服务

```sh
docker ps 

CONTAINER ID   IMAGE                                 COMMAND   CREATED          STATUS          PORTS                    NAMES
7fab57f360a2   caictdevelop/bif-offline-api:v1.0.0   "./app"   31 seconds ago   Up 29 seconds   0.0.0.0:8888->8888/tcp   bif-offline-api
```

## 5.2 接口服务

### 5.2.1 本地账号生成

请求参数：

| 字段名  | 类型 | 是否必填 | 描述                       |
| ------- | ---- | -------- | -------------------------- |
| keyType | int  | 必填     | 加密类型,1:ed25519 , 2:sm2 |

响应参数：

| 字段名             | 类型   | 描述               |
| ------------------ | ------ | ------------------ |
| code               | int    | 成功200 ,失败非200 |
| message            | string | 错误信息           |
| data               | object |                    |
| data.encAddress    | string | 账号地址           |
| data.encPublicKey  | string | 星火公钥           |
| data.encPrivateKey | string | 星火私钥           |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/bifApi/v1/createAddress
{
    "keyType":1
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
    "code": 200,
    "data": {
        "encAddress": "did:bid:efNs6DGRwnaWvdBqp6PVLFJQzL5rxYeF",
        "encPrivateKey": "priSPKnS7DVESZGYbjc6tqYfzN4R74E6DXzgzD5RMt5VDj2ftA",
        "encPublicKey": "b065664e71b940a91737a9136df9081b03262c43e94ba517820fe14cb9fad79d6395fc"
    },
    "message": "ok"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```json
{
    "code": 500,
    "data": "",
    "message": "type值必须是1或者2"
}
```

### 5.2.2 根据私钥获取账号

请求参数：

| 字段名     | 类型   | 是否必填 | 描述     |
| ---------- | ------ | -------- | -------- |
| privateKey | string | 必填     | 星火私钥 |

响应参数：

| 字段名             | 类型   | 描述               |
| ------------------ | ------ | ------------------ |
| code               | int    | 成功200 ,失败非200 |
| message            | string | 错误信息           |
| data               | object |                    |
| data.encAddress    | string | 账号地址           |
| data.encPublicKey  | string | 星火公钥           |
| data.encPrivateKey | string | 星火私钥           |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/bifApi/v1/getAddressByPrivateKey
{
   "privateKey":"priSPKi7K3nVAgtdCu9k9hVn4modxzFkd73JGsRrUYJR1T2RxM"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
    "code": 200,
    "data": {
        "encAddress": "did:bid:efQ69GRtQUDR9SngdFKAv4owYyx5Fnko",
        "encPrivateKey": "priSPKi7K3nVAgtdCu9k9hVn4modxzFkd73JGsRrUYJR1T2RxM",
        "encPublicKey": "b06566d8fb4a6dfbe0d5831e38f621391ad9191626f7e28c13d3a0482c52d5c9607b14"
    },
    "message": "ok"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```json
{
    "code": 500,
    "data": "",
    "message": "private key (***) is invalid"
}
```

### 5.2.3 根据公钥获取账号

请求参数：

| 字段名    | 类型   | 是否必填 | 描述     |
| --------- | ------ | -------- | -------- |
| publicKey | string | 必填     | 星火公钥 |

响应参数：

| 字段名            | 类型   | 描述               |
| ----------------- | ------ | ------------------ |
| code              | int    | 成功200 ,失败非200 |
| message           | string | 错误信息           |
| data              | object |                    |
| data.encAddress   | string | 账号地址           |
| data.encPublicKey | string | 星火公钥           |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/bifApi/v1/getAddressByPublicKey
{
    "publicKey": "b06566d8fb4a6dfbe0d5831e38f621391ad9191626f7e28c13d3a0482c52d5c9607b14"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
    "code": 200,
    "data": {
        "encAddress": "did:bid:efQ69GRtQUDR9SngdFKAv4owYyx5Fnko",
        "encPublicKey": "b06566d8fb4a6dfbe0d5831e38f621391ad9191626f7e28c13d3a0482c52d5c9607b14"
    },
    "message": "ok"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```json
{
    "code": 500,
    "data": "",
    "message": "public key (***) is invalid, please check"
}
```

### 5.2.4 星火私钥转原生私钥

请求参数：

| 字段名        | 类型   | 是否必填 | 描述     |
| ------------- | ------ | -------- | -------- |
| encPrivateKey | string | 必填     | 星火私钥 |

响应参数：

| 字段名             | 类型   | 描述                       |
| ------------------ | ------ | -------------------------- |
| code               | int    | 成功200 ,失败非200         |
| message            | string | 错误信息                   |
| data               | object |                            |
| data.keyType       | int    | 加密类型,1:ed25519 , 2:sm2 |
| data.rawPrivateKey | string | 原生私钥                   |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/bifApi/v1/getRawPrivateKey
{
     "encPrivateKey": "priSrrgL1JPpgKBCdjoyf8E4dRfaF2NYTKmqnSWKfTfhj8ngLc"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
    "code": 200,
    "data": {
        "keyType": 2,
        "rawPrivateKey": "270e2630f429cd5b8ddd76c605245a2814f08255f27e9810418801b5a0b804a5"
    },
    "message": "ok"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```json
{
    "code": 500,
    "data": "",
    "message": "private key (****) is invalid"
}
```

### 5.2.5 星火公钥转原生公钥

请求参数：

| 字段名       | 类型   | 是否必填 | 描述     |
| ------------ | ------ | -------- | -------- |
| encPublicKey | string | 必填     | 星火公钥 |

响应参数：

| 字段名            | 类型   | 描述               |
| ----------------- | ------ | ------------------ |
| code              | int    | 成功200 ,失败非200 |
| message           | string | 错误信息           |
| data              | object |                    |
| data.rawPublicKey | string | 原生公钥           |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/bifApi/v1/getRawPublicKey
{
    "encPublicKey": "b06566424ea71b348ebad4eecac7497227607f2cc3bc128d6248e742faf30ec149e2ed"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
    "code": 200,
    "data": {
        "rawPublicKey": "424ea71b348ebad4eecac7497227607f2cc3bc128d6248e742faf30ec149e2ed"
    },
    "message": "ok"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```json
{
    "code": 500,
    "data": "",
    "message": "endPublicKey 无效"
}
```

### 5.2.6 根据星火公钥获取加密方式

请求参数：

| 字段名       | 类型   | 是否必填 | 描述     |
| ------------ | ------ | -------- | -------- |
| encPublicKey | string | 必填     | 星火公钥 |

响应参数：

| 字段名       | 类型   | 描述                   |
| ------------ | ------ | ---------------------- |
| code         | int    | 成功200 ,失败非200     |
| message      | string | 错误信息               |
| data         | object |                        |
| data.keyType | string | 加密类型,ed25519 / sm2 |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/bifApi/v1/getEncryptionTypeByPubK
{
    "encPublicKey": "b06566424ea71b348ebad4eecac7497227607f2cc3bc128d6248e742faf30ec149e2ed"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
    "code": 200,
    "data": {
        "keyType": "SM2"
    },
    "message": "ok"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```json
{
    "code": 500,
    "data": "",
    "message": "endPublicKey 无效"
}
```

### 5.2.7 原生私钥转星火私钥

请求参数：

| 字段名        | 类型   | 是否必填 | 描述                       |
| ------------- | ------ | -------- | -------------------------- |
| keyType       | int    | 必填     | 加密类型,1:ed25519 , 2:sm2 |
| rawPrivateKey | string | 必填     | 原生私钥                   |

响应参数：

| 字段名             | 类型   | 描述                       |
| ------------------ | ------ | -------------------------- |
| code               | int    | 成功200 ,失败非200         |
| message            | string | 错误信息                   |
| data               | object |                            |
| data.keyType       | int    | 加密类型,1:ed25519 , 2:sm2 |
| data.encPrivateKey | string | 星火私钥                   |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/bifApi/v1/getEncPrivateKeyByRaw
{
    "keyType":2,
    "rawPrivateKey": "270e2630f429cd5b8ddd76c605245a2814f08255f27e9810418801b5a0b804a5"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
    "code": 200,
    "data": {
        "encPrivateKey": "priSrrgL1JPpgKBCdjoyf8E4dRfaF2NYTKmqnSWKfTfhj8ngLc",
        "keyType": 2
    },
    "message": "ok"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```json
{
    "code": 500,
    "data": "",
    "message": "type值必须是1或者2"
}
```

### 5.2.8 原生公钥转星火公钥

请求参数：

| 字段名       | 类型   | 是否必填 | 描述                        |
| ------------ | ------ | -------- | --------------------------- |
| keyType      | int    | 必填     | 加密类型，1:ed25519 , 2:sm2 |
| rawPublicKey | string | 必填     | 原生公钥                    |

响应参数：

| 字段名            | 类型   | 描述                        |
| ----------------- | ------ | --------------------------- |
| code              | int    | 成功200 ,失败非200          |
| message           | string | 错误信息                    |
| data              | object |                             |
| data.keyType      | int    | 加密类型，1:ed25519 , 2:sm2 |
| data.encPublicKey | string | 星火公钥                    |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/bifApi/v1/getEncPublicKeyByRaw
{
    "keyType":1,
    "rawPublicKey": "424ea71b348ebad4eecac7497227607f2cc3bc128d6248e742faf30ec149e2ed"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
    "code": 200,
    "data": {
        "encPublicKey": "b06566424ea71b348ebad4eecac7497227607f2cc3bc128d6248e742faf30ec149e2ed",
        "keyType": 1
    },
    "message": "ok"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```json
{
    "code": 500,
    "data": "",
    "message": "endPublicKey 无效"
}
```

### 5.2.9 构造合约签名交易

请求参数：

| 字段名           | 类型   | 是否必填 | 描述                                     |
| ---------------- | ------ | -------- | ---------------------------------------- |
| senderAddress    | string | 必填     | 交易源账号，即交易的发起方               |
| senderPrivateKey | string | 必填     | 交易源账户私钥                           |
| contractAddress  | string | 必填     | 合约账户地址                             |
| input            | string | 必填     | 待触发的合约的main()入参                 |
| nonce            | Long   | 必填     | 账户交易序列号                           |
| feeLimit         | Long   | 选填     | 交易花费的手续费(单位是PT)，默认1000000L |
| bifAmount        | Long   | 选填     | 转账金额,大小限制[0, Long.MAX_VALUE]     |
| GasPrice         | Long   | 选填     | 打包费用 (单位是PT)，默认100L            |

响应参数：

| 字段名             | 类型   | 描述               |
| ------------------ | ------ | ------------------ |
| code               | int    | 成功200 ,失败非200 |
| message            | string | 错误信息           |
| data               | object |                    |
| data.serialization | string | 交易序列化信息     |
| data.publicKey     | string | 交易源账户公钥     |
| data.signData      | string | 签名数据           |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/bifApi/v1/contract
{
	"senderAddress": "did:bid:efQ69GRtQUDR9SngdFKAv4owYyx5Fnko",
	"senderPrivateKey":"priSPKi7K3nVAgtdCu9k9hVn4modxzFkd73JGsRrUYJR1T2RxM",
	"contractAddress":"did:bid:efAHUyTyhCdUXSxb3znw3Jw4ET24GdCk",
	"bifAmount":0, 
	"feeLimit":100000000, 
	"gasPrice":10,                                 
	"nonce":33,  
	"input":"	{\"function\":\"safeTransferFrom(address,address,string)\",\"args\":\"did:bid:efQ69GRtQUDR9SngdFKAv4owYyx5Fnko,did:bid:ef1L8GBs9mWzeKXGiAZC877WResz6y7,'did:bid:efDtTjWBLkJjtRSJFMfBLNJ6LjnKu1tV'\"}"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
    "code": 200,
    "data": {
        "serialization": "0a286469643a6269643a65665136394752745155445239536e6764464b4176346f7759797835466e6b6f102122ee01080752e9010a286469643a6269643a65664148557954796843645558537862337a6e77334a7734455432344764436b1abc017b2266756e6374696f6e223a22736166655472616e7366657246726f6d28616464726573732c616464726573732c737472696e6729222c2261726773223a226469643a6269643a65665136394752745155445239536e6764464b4176346f7759797835466e6b6f2c6469643a6269643a6566314c38474273396d577a654b584769415a43383737575265737a3679372c276469643a6269643a65664474546a57424c6b4a6a7452534a464d66424c4e4a364c6a6e4b7531745627227d3080c2d72f380a",
        "signData": "70b2ce583fb15b1e67e67e76ab3cfe491e819dbcfa3120946b98648be2f319961e3f148efc49c37dae8a6b71c17ac3c11a20caf58fa26513f86b0d4b209d7a09",
        "publicKey": "b06566d8fb4a6dfbe0d5831e38f621391ad9191626f7e28c13d3a0482c52d5c9607b14"
    },
    "message": "ok"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```json
{
    "code": 500,
    "data": "",
    "message": "*********"
}
```

### 5.2.10 签名

请求参数：

| 字段名     | 类型   | 是否必填 | 描述         |
| ---------- | ------ | -------- | ------------ |
| message    | string | 必填     | 待签名的信息 |
| privateKey | string | 必填     | 签名账户私钥 |

响应参数：

| 字段名             | 类型   | 描述               |
| ------------------ | ------ | ------------------ |
| code               | int    | 成功200 ,失败非200 |
| message            | string | 错误信息           |
| data               | object |                    |
| data.serialization | string | 签名的信息         |
| data.publicKey     | string | 星火公钥           |
| data.signData      | string | 签名数据           |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/bifApi/v1/sign
{
	"message": "0a286469643a6269643a65665136394752745155445239536e6764464b4176346f7759797835466e6b6f101f22ee01080752e9010a286469643a6269643a65664148557954796843645558537862337a6e77334a7734455432344764436b1abc017b2266756e6374696f6e223a22736166655472616e7366657246726f6d28616464726573732c616464726573732c737472696e6729222c2261726773223a226469643a6269643a65665136394752745155445239536e6764464b4176346f7759797835466e6b6f2c6469643a6269643a6566314c38474273396d577a654b584769415a43383737575265737a3679372c276469643a6269643a65664474546a57424c6b4a6a7452534a464d66424c4e4a364c6a6e4b7531745627227d3080c2d72f3814",
	"privateKey":"priSPKi7K3nVAgtdCu9k9hVn4modxzFkd73JGsRrUYJR1T2RxM"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
    "code": 200,
    "data": {
        "serialization": "0a286469643a6269643a65665136394752745155445239536e6764464b4176346f7759797835466e6b6f101f22ee01080752e9010a286469643a6269643a65664148557954796843645558537862337a6e77334a7734455432344764436b1abc017b2266756e6374696f6e223a22736166655472616e7366657246726f6d28616464726573732c616464726573732c737472696e6729222c2261726773223a226469643a6269643a65665136394752745155445239536e6764464b4176346f7759797835466e6b6f2c6469643a6269643a6566314c38474273396d577a654b584769415a43383737575265737a3679372c276469643a6269643a65664474546a57424c6b4a6a7452534a464d66424c4e4a364c6a6e4b7531745627227d3080c2d72f3814",
        "publicKey": "b06566d8fb4a6dfbe0d5831e38f621391ad9191626f7e28c13d3a0482c52d5c9607b14",
        "signData": "5c95d1ddc5fbf24439e4849034b863deb68c4681cf6dbc9d6b7a9d0b5ea6fbbe6a3933619099a0be29dfb4ceaaf614cba0582853fa48420a5b7dd81e28e44c04"
    },
    "message": "ok"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```json
{
    "code": 500,
    "data": "",
    "message": "*********"
}
```

### 5.2.11 验签

请求参数：

| 字段名        | 类型   | 是否必填 | 描述         |
| ------------- | ------ | -------- | ------------ |
| serialization | string | 必填     | 签名的信息   |
| publicKey     | string | 必填     | 签名账户公钥 |
| signData      | string | 必填     | 签名数据     |

响应参数：

| 字段名          | 类型    | 描述               |
| --------------- | ------- | ------------------ |
| code            | int     | 成功200 ,失败非200 |
| message         | string  | 错误信息           |
| data            | object  |                    |
| data.verifySign | Boolean | 验签结果           |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/bifApi/v1/verifySign
{
    "serialization": "0a286469643a6269643a65665136394752745155445239536e6764464b4176346f7759797835466e6b6f101f22ee01080752e9010a286469643a6269643a65664148557954796843645558537862337a6e77334a7734455432344764436b1abc017b2266756e6374696f6e223a22736166655472616e7366657246726f6d28616464726573732c616464726573732c737472696e6729222c2261726773223a226469643a6269643a65665136394752745155445239536e6764464b4176346f7759797835466e6b6f2c6469643a6269643a6566314c38474273396d577a654b584769415a43383737575265737a3679372c276469643a6269643a65664474546a57424c6b4a6a7452534a464d66424c4e4a364c6a6e4b7531745627227d3080c2d72f3814",
     "signData": "22909a4bf1b0d310705eff9f736dd8755927c8f5d43d75d8602cd4097f08a6c7ea5cc824036679daf48a69910957f6d9ef7eabfe994c38391c2258aa07793b09",
     "publicKey": "b06566d8fb4a6dfbe0d5831e38f621391ad9191626f7e28c13d3a0482c52d5c9607b14"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
    "code": 200,
    "data": {
        "verifySign": true
    },
    "message": "ok"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```json
{
    "code": 500,
    "data": "",
    "message": "*******"
}
```

### 5.2.12 数据反序列化

请求参数：

| 字段名        | 类型   | 是否必填 | 描述           |
| ------------- | ------ | -------- | -------------- |
| serialization | string | 必填     | 交易序列化数据 |

响应参数：

| 字段名             | 类型   | 描述               |
| ------------------ | ------ | ------------------ |
| code               | int    | 成功200 ,失败非200 |
| message            | string | 错误信息           |
| data               | object |                    |
| data.SourceAddress | string | 交易源账号         |
| data.FeeLimit      | Long   | 交易花费的手续费   |
| data.GasPrice      | Long   | 打包费用           |
| data.Nonce         | Long   | 账户交易序列号     |
| data.ChainId       | Long   | 链码               |
| data.Operations    | object | 交易内容           |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/bifApi/v1/deserialization
{
    "serialization":"0a286469643a6269643a65665136394752745155445239536e6764464b4176346f7759797835466e6b6f102122ee01080752e9010a286469643a6269643a65664148557954796843645558537862337a6e77334a7734455432344764436b1abc017b2266756e6374696f6e223a22736166655472616e7366657246726f6d28616464726573732c616464726573732c737472696e6729222c2261726773223a226469643a6269643a65665136394752745155445239536e6764464b4176346f7759797835466e6b6f2c6469643a6269643a6566314c38474273396d577a654b584769415a43383737575265737a3679372c276469643a6269643a65664474546a57424c6b4a6a7452534a464d66424c4e4a364c6a6e4b7531745627227d3080c2d72f380a"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
    "code": 200,
    "data": {
        "ChainId": 0,
        "FeeLimit": 100000000,
        "GasPrice": 10,
        "Nonce": 33,
        "Operations": [
            {
                "type": 7,
                "pay_coin": {
                    "dest_address": "did:bid:efAHUyTyhCdUXSxb3znw3Jw4ET24GdCk",
                    "input": "{\"function\":\"safeTransferFrom(address,address,string)\",\"args\":\"did:bid:efQ69GRtQUDR9SngdFKAv4owYyx5Fnko,did:bid:ef1L8GBs9mWzeKXGiAZC877WResz6y7,'did:bid:efDtTjWBLkJjtRSJFMfBLNJ6LjnKu1tV'\"}"
                }
            }
        ],
        "SourceAddress": "did:bid:efQ69GRtQUDR9SngdFKAv4owYyx5Fnko"
    },
    "message": "ok"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```json
{
    "code": 500,
    "data": "",
    "message": "Invalid serialization"
}
```

#### 
