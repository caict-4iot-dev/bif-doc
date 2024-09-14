# 6.离线API服务使用说明

离线API主要是账户和密码学相关API, 不需要连接星火链网RPC接口也能工作。具体部署操作、接口调用如下:

## 6.1 部署服务

### 6.1.1 获取镜像

```
docker pull caictdevelop/web3-api:latest 
```

### 6.1.2 启动服务

```sh
docker run -d -p 8888:8888 --name web3-api --restart always caictdevelop/web3-api:latest
```

### 6.1.3 查询服务

```sh
docker ps 

CONTAINER ID   IMAGE                                 COMMAND   CREATED          STATUS          PORTS                    NAMES
7fab57f360a2   caictdevelop/web3-api:latest   "./app"   31 seconds ago   Up 29 seconds   0.0.0.0:8888->8888/tcp   web3-api
```

### 6.1.4 停止服务

```
docker rm -f web3-api
```



## 6.2 接口服务

### 6.2.1 本地账号生成

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

```
http请求方式：POST
https://{url}/web3Api/v1/createAddress
{
    "key_type":1
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

### 6.2.2 根据私钥获取账号

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

```
http请求方式：POST
https://{url}/web3Api/v1/getAddressByPrivateKey
{
   "private_key":"priSPKi7K3nVAgtdCu9k9hVn4modxzFkd73JGsRrUYJR1T2RxM"
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

### 6.2.3 根据公钥获取账号

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

```
http请求方式：POST
https://{url}/web3Api/v1/getAddressByPublicKey
{
    "public_key": "b06566d8fb4a6dfbe0d5831e38f621391ad9191626f7e28c13d3a0482c52d5c9607b14"
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

### 6.2.4 星火私钥转原生私钥

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

```
http请求方式：POST
https://{url}/web3Api/v1/getRawPrivateKey
{
    "enc_private_key": "priSrrgL1JPpgKBCdjoyf8E4dRfaF2NYTKmqnSWKfTfhj8ngLc"
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

### 6.2.5 星火公钥转原生公钥

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

```
http请求方式：POST
https://{url}/web3Api/v1/getRawPublicKey
{
    "enc_public_key": "b06566424ea71b348ebad4eecac7497227607f2cc3bc128d6248e742faf30ec149e2ed"
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

### 6.2.6 根据星火公钥获取加密方式

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

```
http请求方式：POST
https://{url}/web3Api/v1/getEncryptionTypeByPubK
{
    "enc_public_key": "b07a6604ecaf086d04ae03c2b790647570c7b6267ee79c385f5fda8c635c61d7af2d02a0d517c302c9260def75d354f369386947f6fc149628e9541c64453298754db19f"
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

### 6.2.7 原生私钥转星火私钥

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

```
http请求方式：POST
https://{url}/web3Api/v1/getEncPrivateKeyByRaw
{
    "key_type": 2,
    "raw_private_key": "270e2630f429cd5b8ddd76c605245a2814f08255f27e9810418801b5a0b804a5"
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

### 6.2.8 原生公钥转星火公钥

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

```
http请求方式：POST
https://{url}/web3Api/v1/getEncPublicKeyByRaw
{
    "key_type": 1,
    "raw_public_key": "424ea71b348ebad4eecac7497227607f2cc3bc128d6248e742faf30ec149e2ed"
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

### 6.2.9 构造合约签名交易

请求参数：

| 字段名           | 类型   | 是否必填 | 描述                                                         |
| ---------------- | ------ | -------- | ------------------------------------------------------------ |
| senderAddress    | string | 必填     | 交易源账号，即交易的发起方                                   |
| senderPrivateKey | string | 必填     | 交易源账户私钥                                               |
| contractAddress  | string | 必填     | 合约账户地址                                                 |
| input            | string | 必填     | 待触发的合约的main()入参                                     |
| nonce            | Long   | 必填     | 账户交易序列号                                               |
| feeLimit         | Long   | 选填     | 交易花费的手续费(单位是glowstone)，1 星火令(XHT) = 10^8 星火萤(glowstone)，默认1000000L |
| bifAmount        | Long   | 选填     | 转账金额,大小限制[0, Long.MAX_VALUE]                         |
| GasPrice         | Long   | 选填     | 打包费用 (单位是glowstone)，1 星火令(XHT) = 10^8 星火萤(glowstone)，默认100L |

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

```
http请求方式：POST
https://{url}/web3Api/v1/sign
{
    "message": "0A286469643A6269643A65667839724845656832566F565348465941553839794C4B61636E7A576E55521080C0AAC2A2EFF88A02225F080712286469643A6269643A65667839724845656832566F565348465941553839794C4B61636E7A576E555252310A286469643A6269643A65666868334C673642686B51395A59386F5636557379564E3869727A6E3847691080D0DBC3F4022260080712286469643A6269643A65667839724845656832566F565348465941553839794C4B61636E7A576E555252320A286469643A6269643A6566736869414147394876546A6D5631714C557969396E6A486B32536A3858771080A0E5B9C2910130C094FF0438E807680170F3C002",
    "private_key": "priSPKnzBozLx1wWZoFFSGnnZZL4RJukXnTXrRygYLfyiYPfws"
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

### 6.2.10 签名

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

```
http请求方式：POST
https://{url}/web3Api/v1/verifySign
{
    "serialization": "0a286469643a6269643a6566323563324e544555696a3779726d574c3668354d72697a6267434270636e100022c401080122bf0112b401080012af012275736520737472696374223b2066756e6374696f6e20696e697428626172297b72657475726e3b7d2066756e6374696f6e206d61696e28696e707574297b6c65742070617261203d204a534f4e2e706172736528696e707574293b696628706172612e646f5f666f6f297b6c65742078203d207b2768656c6c6f27203a2027776f726c64277d3b7d7d2066756e6374696f6e20717565727928696e707574297b72657475726e20696e7075743b7d1a041a02080128012a04323032343080c2d72f380a",
        "sign_data": "a3c3283384979e4f7496dff1ba927e26a71b8a3f32d0f95b394b03dd8784aa9f78dd13fff60df96868dd154a9b72ce624ac4443a179af3de399f798f0a00e10a",
        "public_key": "b065667b44623c57e6464418eb001a548f06361321756d64b99a938f46b095a12358ac"
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

### 6.2.11 验签

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

```
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

### 6.2.12 数据反序列化

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

```
http请求方式：POST
https://{url}/web3Api/v1/deserialization
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



### 6.2.13 根据abi对合约返回结果的解码

请求参数：

| 字段名        | 类型   | 是否必填 | 描述6                                    |
| ------------- | ------ | -------- | ---------------------------------------- |
| abi           | string | 必填     | abi字符串                                |
| hex_data      | string | 必填     | 需要解码的十六进制字符串                 |
| function_name | string | 非必填   | 调用合约方法名（如果是构造函数参数为""） |

响应参数：

| 字段名          | 类型   | 描述               |
| --------------- | ------ | ------------------ |
| code            | int    | 成功200 ,失败非200 |
| message         | string | 错误信息           |
| data            | object |                    |
| data.ecode_data | string | 解码后信息         |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/web3Api/v1/contractAbiDecode
{
    "abi": "[{\"constant\":true,\"inputs\":[{\"name\":\"id\",\"type\":\"uint256\"}],\"name\":\"queryAllById\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"},{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"id\",\"type\":\"uint256\"}],\"name\":\"queryAdById\",\"outputs\":[{\"name\":\"\",\"type\":\"address\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"getStaticArray\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256[3]\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"id\",\"type\":\"uint256\"},{\"name\":\"data\",\"type\":\"address\"}],\"name\":\"setAdById\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"id\",\"type\":\"uint256\"},{\"name\":\"data\",\"type\":\"string\"}],\"name\":\"setById\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"id\",\"type\":\"uint256\"}],\"name\":\"queryById\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"exampleFunction\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"},{\"name\":\"\",\"type\":\"uint256\"},{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"name\":\"staticArray\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"}]",
    "hex_data": "0x000000000000000065661d87e26a357114234b22e89747d85556b2b559b5296c",
    "function_name": "queryAdById"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
  "code": 200,
  "data": {
    "ecode_data": "did:bid:ef91sQXEXVfPFQXRZpgA3Rs1pTNbZndq"
  },
  "message": "ok"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```json
{
  "code": 500,
  "data": "",
  "message": "hex_data不能为空"
}
```

### 6.2.14 根据abi对合约入参进行编码

请求参数：

| 字段名        | 类型   | 是否必填 | 描述           |
| ------------- | ------ | -------- | -------------- |
| abi           | string | 必填     | abi字符串      |
| params        | object | 必填     | 合约入参       |
| function_name | string | 必填     | 调用合约方法名 |

响应参数：

| 字段名           | 类型   | 描述                   |
| ---------------- | ------ | ---------------------- |
| code             | int    | 成功200 ,失败非200     |
| message          | string | 错误信息               |
| data             | object |                        |
| data.decode_data | string | 编码后的十六进制字符串 |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/web3Api/v1/contractAbiEncode
{
    "abi": "[{\"constant\":true,\"inputs\":[{\"name\":\"id\",\"type\":\"uint256\"}],\"name\":\"queryAllById\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"},{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"id\",\"type\":\"uint256\"}],\"name\":\"queryAdById\",\"outputs\":[{\"name\":\"\",\"type\":\"address\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"getStaticArray\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256[3]\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"id\",\"type\":\"uint256\"},{\"name\":\"data\",\"type\":\"address\"}],\"name\":\"setAdById\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"id\",\"type\":\"uint256\"},{\"name\":\"data\",\"type\":\"string\"}],\"name\":\"setById\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"id\",\"type\":\"uint256\"}],\"name\":\"queryById\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"exampleFunction\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"},{\"name\":\"\",\"type\":\"uint256\"},{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"name\":\"staticArray\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"}]",
    "function_name": "setById",
    "params": {
        "id": 4010,
        "data": "testEncode"
    }
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
  "code": 200,
  "data": {
    "decode_data": "0x794bde480000000000000000000000000000000000000000000000000000000000000faa0000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000a74657374456e636f646500000000000000000000000000000000000000000000"
  },
  "message": "ok"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```json
{
  "code": 500,
  "data": "",
  "message": "function_name不能为空"
}
```

### 6.2.15 根据合约事件签名编码成topic

请求参数：

| 字段名          | 类型   | 是否必填 | 描述     |
| --------------- | ------ | -------- | -------- |
| event_signature | string | 必填     | 事件签名 |

响应参数：

| 字段名     | 类型   | 描述               |
| ---------- | ------ | ------------------ |
| code       | int    | 成功200 ,失败非200 |
| message    | string | 错误信息           |
| data       | object |                    |
| data.topic | string | 合约事件topic      |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/web3Api/v1/topicEncode
{
    "event_signature":"TransferWithIndex(uint256,address)"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
  "code": 200,
  "data": {
    "topic": "b81f980583c4edb08f6484c384df2eb0744137be515288a171a840fe42616ce6"
  },
  "message": "ok"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```json
{
  "code": 500,
  "data": "",
  "message": "event_signature不能为空"
}
```

### 6.2.16 根据abi和topic解码出事件签名

请求参数：

| 字段名 | 类型   | 是否必填 | 描述      |
| ------ | ------ | -------- | --------- |
| abi    | string | 必填     | abi字符串 |
| topic  | string | 必填     | 事件topic |

响应参数：

| 字段名               | 类型   | 描述               |
| -------------------- | ------ | ------------------ |
| code                 | int    | 成功200 ,失败非200 |
| message              | string | 错误信息           |
| data                 | object |                    |
| data.event_signature | string | 合约事件签名       |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/web3Api/v1/topicAbiDecode
{
    "abi": "[{\"constant\":true,\"inputs\":[{\"name\":\"id\",\"type\":\"uint256\"}],\"name\":\"queryAdById\",\"outputs\":[{\"name\":\"\",\"type\":\"address\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"id\",\"type\":\"uint256\"},{\"name\":\"data\",\"type\":\"address\"}],\"name\":\"setAdById\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"id\",\"type\":\"uint256\"},{\"name\":\"data\",\"type\":\"address\"}],\"name\":\"setAdById2\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"_ad\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"_value\",\"type\":\"uint256\"}],\"name\":\"Transfer\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":true,\"name\":\"_id\",\"type\":\"uint256\"},{\"indexed\":true,\"name\":\"_address\",\"type\":\"address\"}],\"name\":\"TransferWithIndex\",\"type\":\"event\"}]",
    "topic": "b81f980583c4edb08f6484c384df2eb0744137be515288a171a840fe42616ce6"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
  "code": 200,
  "data": {
    "event_signature": "TransferWithIndex(uint256,address)"
  },
  "message": "ok"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```json
{
  "code": 500,
  "data": "",
  "message": "topic不能为空"
}
```

### 6.2.17 构造账户激活签名交易

请求参数：

| 字段名             | 类型   | 是否必填 | 描述                                                         |
| ------------------ | ------ | -------- | ------------------------------------------------------------ |
| source_address     | string | 必填     | 交易源账号，即交易的发起方                                   |
| source_private_key | string | 必填     | 交易源账户私钥                                               |
| dest_address       | string | 必填     | 目标账户地址                                                 |
| nonce              | Long   | 选填     | 账户交易序列号,默认0                                         |
| nonce_type         | Long   | 选填     | nonce类型，0：自增，nonce 1：随机nonce，默认0                |
| block_number       | Long   | 选填     | 当前区块高度                                                 |
| fee_limit          | Long   | 选填     | 交易花费的手续费(单位是glowstone)，默认1000000L              |
| init_balance       | Long   | 选填     | 初始化星火令，单位glowstone，1 星火令(XHT) = 10^8 星火萤(glowstone)，大小[0, Long.MAX_VALUE] |
| gas_price          | Long   | 选填     | 打包费用 (单位是glowstone)，默认100L                         |
| remarks            | string | 选填     | 用户自定义给交易的备注，16进制格式，长度[0,256k]             |

响应参数：

| 字段名             | 类型   | 描述               |
| ------------------ | ------ | ------------------ |
| code               | int    | 成功200 ,失败非200 |
| message            | string | 错误信息           |
| data               | object |                    |
| data.serialization | string | 交易序列化信息     |
| data.public_key    | string | 交易源账户公钥     |
| data.sign_data     | string | 签名数据           |
| data.hash          | string | 交易hash(离线)     |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/web3Api/v1/accountCreate
{
    "source_address": "did:bid:efx9rHEeh2VoVSHFYAU89yLKacnzWnUR",
    "source_private_key": "priSPKnzBozLx1wWZoFFSGnnZZL4RJukXnTXrRygYLfyiYPfwS",
    "dest_address": "did:bid:efAHUyTyhCdUXSxb3znw3Jw4ET24GdCk",
    "init_balance": 1,
    "fee_limit": 100000000,
    "gas_price": 10,
    "nonce": 7,
    "nonce_type": 1,
    "block_number": 1790,
    "remarks": "2024"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
  "code": 200,
  "data": {
    "serialization": "0a286469643a6269643a65667839724845656832566f565348465941553839794c4b61636e7a576e55521080a0d2ee869bb0f9072238080122340a286469643a6269643a65664148557954796843645558537862337a6e77334a7734455432344764436b1a0608011a02080128012a04323032343080c2d72f380a6801708a18",
    "hash": "9ebf12c32af8168821c239b7de0bed0309edf073f1d0f96f0b660b109e2fe952",
    "sign_data": "0ab810004029c4715cfdf417bae6d4c6ebb64684270bf6fdec6b242a4b12e433c213f2464d872f5d0e662420b38fbba39a6833ed8d7902baa8585343033fc50c",
    "public_key": "b065660d65034a65d014e057baf5f4cf2d265a5f5510cbd733cd1784458d7a122a4934"
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

### 6.2.18 构造setMetadatas签名交易

请求参数：

| 字段名             | 类型    | 是否必填 | 描述                                             |
| ------------------ | ------- | -------- | ------------------------------------------------ |
| source_address     | string  | 必填     | 交易源账号，即交易的发起方                       |
| source_private_key | string  | 必填     | 交易源账户私钥                                   |
| key                | string  | 必填     | metadata的关键词，长度限制[1, 1024]              |
| value              | string  | 必填     | metadata的内容，长度限制[1, 256000]              |
| version            | Long    | 选填     | metadata的版本                                   |
| delete_flag        | Boolean | 选填     | 是否删除metadata                                 |
| nonce              | Long    | 选填     | 账户交易序列号，默认0                            |
| nonce_type         | Long    | 选填     | nonce类型，0：自增，nonce 1：随机nonce，默认0    |
| block_number       | Long    | 选填     | 当前区块高度                                     |
| fee_limit          | Long    | 选填     | 交易花费的手续费(单位是glowstone)，默认1000000L  |
| gas_price          | Long    | 选填     | 打包费用 (单位是glowstone)，默认100L             |
| remarks            | string  | 选填     | 用户自定义给交易的备注，16进制格式，长度[0,256k] |

响应参数：

| 字段名             | 类型   | 描述               |
| ------------------ | ------ | ------------------ |
| code               | int    | 成功200 ,失败非200 |
| message            | string | 错误信息           |
| data               | object |                    |
| data.serialization | string | 交易序列化信息     |
| data.public_key    | string | 交易源账户公钥     |
| data.sign_data     | string | 签名数据           |
| data.hash          | string | 交易hash(离线)     |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/web3Api/v1/setMetadata
{
    "source_address": "did:bid:efx9rHEeh2VoVSHFYAU89yLKacnzWnUR",
    "source_private_key": "priSPKnzBozLx1wWZoFFSGnnZZL4RJukXnTXrRygYLfyiYPfwS",
    "key": "did:bid20240220",
    "value": "20240220",
    "version": 1,
    "delete_flag": false,
    "fee_limit": 100000000,
    "gas_price": 10,
    "nonce": 0,
    "nonce_type": 1,
    "block_number": 1790,
    "remarks": "2024"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
  "code": 200,
  "data": {
    "serialization": "0a286469643a6269643a65667839724845656832566f565348465941553839794c4b61636e7a576e55521080a0d2eeae9db0f907222108043a1d0a0f6469643a62696432303234303232301208323032343032323018012a04323032343080c2d72f380a680170d61b",
    "hash": "ce11e19269babd68e3b2446de8195738042560836db8a8af60eba756fb7e34f6",
    "sign_data": "f32804322155f464ac443a62e3e197de765bc700374f9ba349930c3106f949da5c293c9f9b0924733e8874d2940c625c165388a9568ce8759c472af6c2c2340f",
    "public_key": "b065660d65034a65d014e057baf5f4cf2d265a5f5510cbd733cd1784458d7a122a4934"
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

### 6.2.19 构造setPrivilege签名交易

请求参数：

| 字段名                    | 类型     | 是否必填 | 描述                                             |
| ------------------------- | -------- | -------- | ------------------------------------------------ |
| source_address            | string   | 必填     | 交易源账号，即交易的发起方                       |
| source_private_key        | string   | 必填     | 交易源账户私钥                                   |
| master_weight             | string   | 选填     | 交易源账号权重                                   |
| signers                   | Object[] | 选填     | 签名者权重列表                                   |
| signers[i].address        | string   | 必填     | 签名者区块链账户地址，signers填写情况下则必填    |
| signers[i].weight         | Long     | 选填     | 为签名者设置权重值                               |
| tx_threshold              | string   | 选填     | 交易门限，大小限制[0, Long.MAX_VALUE]            |
| type_threshold            | Object[] | 选填     | 指定类型交易门限                                 |
| typeThreshold[].type      | Long     | 必填     | 操作类型，txThreshold填写情况下必须大于0         |
| typeThreshold[].threshold | Long     | 选填     | 门限值，大小限制[0, Long.MAX_VALUE]              |
| nonce                     | Long     | 选填     | 账户交易序列号，默认0                            |
| nonce_type                | Long     | 选填     | nonce类型，0：自增，nonce 1：随机nonce，默认0    |
| block_number              | Long     | 选填     | 当前区块高度                                     |
| fee_limit                 | Long     | 选填     | 交易花费的手续费(单位是glowstone)，默认1000000L  |
| gas_price                 | Long     | 选填     | 打包费用 (单位是glowstone)，默认100L             |
| remarks                   |          | 选填     | 用户自定义给交易的备注，16进制格式，长度[0,256k] |

响应参数：

| 字段名             | 类型   | 描述               |
| ------------------ | ------ | ------------------ |
| code               | int    | 成功200 ,失败非200 |
| message            | string | 错误信息           |
| data               | object |                    |
| data.serialization | string | 交易序列化信息     |
| data.public_key    | string | 交易源账户公钥     |
| data.sign_data     | string | 签名数据           |
| data.hash          | string | 交易hash(离线)     |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/web3Api/v1/setPrivilege
{
    "source_address": "did:bid:efx9rHEeh2VoVSHFYAU89yLKacnzWnUR",
    "source_private_key": "priSPKnzBozLx1wWZoFFSGnnZZL4RJukXnTXrRygYLfyiYPfwS",
    "signers": [
        {
            "address": "did:bid:efQ69GRtQUDR9SngdFKAv4owYyx5Fnko",
            "weight": 100
        }
    ],
    "tx_threshold": "100",
    "type_threshold": [
        {
            "type": 1,
            "threshold": 50
        }
    ],
    "master_weight": "100",
    "fee_limit": 100000000,
    "gas_price": 10,
    "nonce": 33,
    "nonce_type": 1,
    "block_number": 1790,
    "remarks": "2024"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
  "code": 200,
  "data": {
    "serialization": "0a286469643a6269643a65667839724845656832566f565348465941553839794c4b61636e7a576e55521080a0d2eebda3b0f90722420809623e0a03313030122c0a286469643a6269643a65665136394752745155445239536e6764464b4176346f7759797835466e6b6f10641a033130302204080110322a04323032343080c2d72f380a680170c61d",
    "hash": "e2d7a40df0fc6f8db5b5539d9d90f28043ab02bfce9069d6c45d65f698c4dfa6",
    "sign_data": "b3f336ca6aa78e8c8c1d4fdbbb7c4ed11de7957288c1d1a46af70b40d80caae04cd894c86703e48b6ac95c6642465ee0ce0cfc1c12d3de62f77fe25d0137410e",
    "public_key": "b065660d65034a65d014e057baf5f4cf2d265a5f5510cbd733cd1784458d7a122a4934"
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

### 6.2.20 构造合约创建签名交易

请求参数：

| 字段名             | 类型   | 是否必填 | 描述                                             |
| ------------------ | ------ | -------- | ------------------------------------------------ |
| source_address     | string | 必填     | 交易源账号，即交易的发起方                       |
| source_private_key | string | 必填     | 交易源账户私钥                                   |
| init_balance       | Long   | 必填     | 合约账户地址                                     |
| type               | Long   | 选填     | 合约的类型，默认是0 , 0: javascript，1 :evm 。   |
| payload            | string | 必填     | 对应语种的合约代码                               |
| init_input         | string | 选填     | 合约代码中init方法的入参                         |
| nonce              | Long   | 选填     | 账户交易序列号，默认0                            |
| nonce_type         | Long   | 选填     | nonce类型，0：自增，nonce 1：随机nonce，默认0    |
| block_number       | Long   | 选填     | 当前区块高度                                     |
| fee_limit          | Long   | 选填     | 交易花费的手续费(单位是glowstone)，默认1000000L  |
| gas_price          | Long   | 选填     | 打包费用 (单位是glowstone)，默认100L             |
| remarks            |        | 选填     | 用户自定义给交易的备注，16进制格式，长度[0,256k] |

响应参数：

| 字段名             | 类型   | 描述               |
| ------------------ | ------ | ------------------ |
| code               | int    | 成功200 ,失败非200 |
| message            | string | 错误信息           |
| data               | object |                    |
| data.serialization | string | 交易序列化信息     |
| data.public_key    | string | 交易源账户公钥     |
| data.sign_data     | string | 签名数据           |
| data.hash          | string | 交易hash(离线)     |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/web3Api/v1/contractCreate
{
    "source_address": "did:bid:efx9rHEeh2VoVSHFYAU89yLKacnzWnUR",
    "source_private_key": "priSPKnzBozLx1wWZoFFSGnnZZL4RJukXnTXrRygYLfyiYPfwS",
    "init_balance": 0,
    "type": 0,
    "payload": "'use strict';function getStr(params) {  var key = params.key;  return Chain.load(key);  }function saveStr(params) {  var key = params.key;  var val = params.val;  Chain.store(key, val);}function init(input_str) {    var input = JSON.parse(input_str);    saveStr(input);}function main(input_str) {  var input = JSON.parse(input_str);  var params = input.params;  if (input.method === \"saveStr\") {     saveStr(params);  }}function query(input_str) {  var input = JSON.parse(input_str);  var object = {}; if (input.method === \"getStr\") {    object = getStr(input.params);  } else {    throw '<unidentified operation type>';  }  return JSON.stringify(object);}",
    "init_input": "{\"key\":\"description\", \"val\":\"hello\"}",
    "fee_limit": 100000000,
    "gas_price": 10,
    "nonce": 33,
    "nonce_type": 1,
    "block_number": 1790,
    "remarks": "2024"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
  "code": 200,
  "data": {
    "serialization": "0a286469643a6269643a65667839724845656832566f565348465941553839794c4b61636e7a576e55521080a0d2ecc7a5b0f90722c705080122c2051293051290052775736520737472696374273b66756e6374696f6e2067657453747228706172616d7329207b2020766172206b6579203d20706172616d732e6b65793b202072657475726e20436861696e2e6c6f6164286b6579293b20207d66756e6374696f6e207361766553747228706172616d7329207b2020766172206b6579203d20706172616d732e6b65793b20207661722076616c203d20706172616d732e76616c3b2020436861696e2e73746f7265286b65792c2076616c293b7d66756e6374696f6e20696e697428696e7075745f73747229207b2020202076617220696e707574203d204a534f4e2e706172736528696e7075745f737472293b202020207361766553747228696e707574293b7d66756e6374696f6e206d61696e28696e7075745f73747229207b202076617220696e707574203d204a534f4e2e706172736528696e7075745f737472293b202076617220706172616d73203d20696e7075742e706172616d733b202069662028696e7075742e6d6574686f64203d3d3d2022736176655374722229207b20202020207361766553747228706172616d73293b20207d7d66756e6374696f6e20717565727928696e7075745f73747229207b202076617220696e707574203d204a534f4e2e706172736528696e7075745f737472293b2020766172206f626a656374203d207b7d3b2069662028696e7075742e6d6574686f64203d3d3d20226765745374722229207b202020206f626a656374203d2067657453747228696e7075742e706172616d73293b20207d20656c7365207b202020207468726f7720273c756e6964656e746966696564206f7065726174696f6e20747970653e273b20207d202072657475726e204a534f4e2e737472696e67696679286f626a656374293b7d1a041a02080132247b226b6579223a226465736372697074696f6e222c202276616c223a2268656c6c6f227d2a04323032343080c2d72f380a6801708c1a",
    "hash": "efd1e49901b563d1bde834bf9539e760dfb079307387f0e8dfe149e38a07400a",
    "sign_data": "754df0d30651032ba3b628fb06b6147c6de0ae9670f66537a0420cbb24a3d3a20d7f3141cf1bcd28d1c88b9e7b1878377d958cafa1d9fdb66ac40300abe36001",
    "public_key": "b065660d65034a65d014e057baf5f4cf2d265a5f5510cbd733cd1784458d7a122a4934"
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

### 6.2.21 构造合约调用签名交易

请求参数：

| 字段名             | 类型   | 是否必填 | 描述                                             |
| ------------------ | ------ | -------- | ------------------------------------------------ |
| source_address     | string | 必填     | 交易源账号，即交易的发起方                       |
| source_private_key | string | 必填     | 交易源账户私钥                                   |
| contract_address   | string | 必填     | 合约账户地址                                     |
| input              | string | 必填     | 待触发的合约的main()入参                         |
| nonce              | Long   | 选填     | 账户交易序列号，默认0                            |
| nonce_type         | Long   | 选填     | nonce类型，0：自增，nonce 1：随机nonce，默认0    |
| block_number       | Long   | 选填     | 当前区块高度                                     |
| fee_limit          | Long   | 选填     | 交易花费的手续费(单位是glowstone)，默认1000000L  |
| bif_amount         | Long   | 选填     | 转账金额,大小限制[0, Long.MAX_VALUE]             |
| gas_price          | Long   | 选填     | 打包费用 (单位是glowstone)，默认100L             |
| remarks            |        | 选填     | 用户自定义给交易的备注，16进制格式，长度[0,256k] |

响应参数：

| 字段名             | 类型   | 描述               |
| ------------------ | ------ | ------------------ |
| code               | int    | 成功200 ,失败非200 |
| message            | string | 错误信息           |
| data               | object |                    |
| data.serialization | string | 交易序列化信息     |
| data.public_key    | string | 交易源账户公钥     |
| data.sign_data     | string | 签名数据           |
| data.hash          | string | 交易hash(离线)     |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/web3Api/v1/contractInvoke
{
    "source_address": "did:bid:efx9rHEeh2VoVSHFYAU89yLKacnzWnUR",
    "source_private_key": "priSPKnzBozLx1wWZoFFSGnnZZL4RJukXnTXrRygYLfyiYPfwS",
    "contract_address": "did:bid:efAHUyTyhCdUXSxb3znw3Jw4ET24GdCk",
    "bif_amount": 0,
    "fee_limit": 100000000,
    "gas_price": 10,
    "nonce": 7,
    "nonce_type": 1,
    "block_number": 1790,
    "input": "{\"function\":\"safeTransferFrom(address,address,string)\",\"args\":\"did:bid:efQ69GRtQUDR9SngdFKAv4owYyx5Fnko,did:bid:ef1L8GBs9mWzeKXGiAZC877WResz6y7,'did:bid:efDtTjWBLkJjtRSJFMfBLNJ6LjnKu1tV'\"}"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
  "code": 200,
  "data": {
    "serialization": "0a286469643a6269643a65667839724845656832566f565348465941553839794c4b61636e7a576e55521080a0d2feae95b0f90722ee01080752e9010a286469643a6269643a65664148557954796843645558537862337a6e77334a7734455432344764436b1abc017b2266756e6374696f6e223a22736166655472616e7366657246726f6d28616464726573732c616464726573732c737472696e6729222c2261726773223a226469643a6269643a65665136394752745155445239536e6764464b4176346f7759797835466e6b6f2c6469643a6269643a6566314c38474273396d577a654b584769415a43383737575265737a3679372c276469643a6269643a65664474546a57424c6b4a6a7452534a464d66424c4e4a364c6a6e4b7531745627227d3080c2d72f380a680170f618",
    "hash": "f8d592c3fef3f84f78fa37eab3901ec1a57106e7e87ddd5d41974c46864db2eb",
    "sign_data": "4acad5e5bec325fb5e3ca0415e3a456a334e7aa0549540a870d23775899646f0afa74415eaa0d11aae7565a2b47b174a5c4e7d63a4369a922527c8950ffc0405",
    "public_key": "b065660d65034a65d014e057baf5f4cf2d265a5f5510cbd733cd1784458d7a122a4934"
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

### 6.2.22 构造转账签名交易

请求参数：

| 字段名             | 类型   | 是否必填 | 描述                                             |
| ------------------ | ------ | -------- | ------------------------------------------------ |
| source_address     | string | 必填     | 交易源账号，即交易的发起方                       |
| source_private_key | string | 必填     | 交易源账户私钥                                   |
| dest_address       | string | 必填     | 合约账户地址                                     |
| amount             | Long   | 必填     | 待触发的合约的main()入参                         |
| nonce              | Long   | 选填     | 账户交易序列号，默认0                            |
| nonce_type         | Long   | 选填     | nonce类型，0：自增，nonce 1：随机nonce，默认0    |
| block_number       | Long   | 选填     | 当前区块高度                                     |
| fee_limit          | Long   | 选填     | 交易花费的手续费(单位是glowstone)，默认1000000L  |
| gas_price          | Long   | 选填     | 打包费用 (单位是glowstone)，默认100L             |
| remarks            | string | 选填     | 用户自定义给交易的备注，16进制格式，长度[0,256k] |

响应参数：

| 字段名             | 类型   | 描述               |
| ------------------ | ------ | ------------------ |
| code               | int    | 成功200 ,失败非200 |
| message            | string | 错误信息           |
| data               | object |                    |
| data.serialization | string | 交易序列化信息     |
| data.public_key    | string | 交易源账户公钥     |
| data.sign_data     | string | 签名数据           |
| data.hash          | string | 交易hash(离线)     |

示例：

（1）请求示例：

```plain
http请求方式：POST
https://{url}/web3Api/v1/gasSend
{
    "source_address": "did:bid:efx9rHEeh2VoVSHFYAU89yLKacnzWnUR",
    "source_private_key": "priSPKnzBozLx1wWZoFFSGnnZZL4RJukXnTXrRygYLfyiYPfwS",
    "dest_address": "did:bid:efx9rHEeh2VoVSHFYAU89yLKacnzWnUR",
    "amount": 1,
    "fee_limit": 100000000,
    "gas_price": 10,
    "nonce": 33,
    "nonce_type": 1,
    "block_number": 1790,
    "remarks": "2024"
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```json
{
  "code": 200,
  "data": {
    "serialization": "0a286469643a6269643a65667839724845656832566f565348465941553839794c4b61636e7a576e55521080a0d2ec8faab0f90722300807522c0a286469643a6269643a65667839724845656832566f565348465941553839794c4b61636e7a576e555210012a04323032343080c2d72f380a680170f117",
    "hash": "2b5aa26b1df987124bdc8e28aa843d6a7217a30492b602adb37319726685e2c2",
    "sign_data": "98d6477054895bf0a8c13066c5a517a448b757c98b866ee0fca1b62dd80527a00fcc88092d7af14285bb1bac970a49d8d2afa1d97336a4cb42cd73cdcd75a304",
    "public_key": "b065660d65034a65d014e057baf5f4cf2d265a5f5510cbd733cd1784458d7a122a4934"
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

## 6.3.响应码

| 序号 | 响应码  | 描述                                                |
| ---- | ------- | --------------------------------------------------- |
| 1    | 200     | 成功                                                |
| 2    | 400/500 | 参数异常                                            |
| 3    | 11002   | Invalid source address                              |
| 4    | 11003   | Invalid dest address                                |
| 5    | 11004   | Init balance must be between 0 and Long.MAX_VALUE   |
| 6    | 11005   | Source address cannot be equal to destAddress       |
| 7    | 11011   | The length of key must be between 1 and 1024        |
| 8    | 11012   | The length of value must be between 0 and 256000    |
| 9    | 11013   | The version must be equal to or greater than 0      |
| 10   | 11014   | The length of remarks must be between 0 and 256000  |
| 11   | 11015   | Master weight must be between 0 and Long.MAX_VALUE  |
| 12   | 11016   | Invalid signer address                              |
| 13   | 11017   | Signer weight must be between 0 and Long.MAX_VALUE  |
| 14   | 11018   | Tx threshold must be between 0 and Long.MAX_VALUE   |
| 15   | 11019   | Type of  type threshold is invalid                  |
| 16   | 11020   | Type threshold must be between 0 and Long.MAX_VALUE |
| 17   | 11024   | Amount must be between 0 and Long.MAX_VALUE         |
| 18   | 11026   | Bif amount must be between 0 and Long.MAX_VALUE     |
| 19   | 11037   | Invalid contract address                            |
| 20   | 11040   | Source address cannot be equal to contract address  |
| 21   | 11044   | Payload cannot be empty                             |
| 22   | 11045   | Input cannot be empty                               |
| 23   | 11047   | Invalid contract type                               |
| 24   | 11048   | Nonce must be between 1 and Long.MAX_VALUE          |
| 25   | 11049   | Gas price must be between 0 and Long.MAX_VALUE      |
| 26   | 11050   | Fee limit must be between 0 and Long.MAX_VALUE      |
| 27   | 11051   | Operations cannot be empty                          |
| 28   | 11057   | Invalid private Key                                 |
| 29   | 20000   | System error                                        |