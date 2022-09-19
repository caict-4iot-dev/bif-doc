# DNA服务网络接口

## 1.简介

欢迎使用“星火·链网”DNA（数字原生资产）公共服务网络-DNA注册认证平台。

DNA注册认证平台在星火·链网的主链，将基于DNA协议（基于`ERC721`改造的星火链网数字原生资产协议）部署的DNA合约封装为标准化`API`，提供链上注册数字资产、转移数字资产等接口服务，方便客户快速基于星火主链构建数字藏品等链上数字资产应用。<a name="FQBXC"></a>

数字资产注册认证平台提供以下接口类型：

| **接口类型** | **描述**                                             |
| ------------ | ---------------------------------------------------- |
| 账户管理类   | 用于用户账户的管理，包含创建，激活等操作             |
| 集合操作类   | 用于数字资产集合的操作，包含创建，查询等操作         |
| 资产操作类   | 用于数字资产的操作，包含注册，转移，销毁，查询等操作 |

DNA认证服务主要面向的是已有区块链网络提供注册服务的数字资产平台客户，DNA认证服务基于星火主链的公信力为客户提供“星火·链网“DNA数字资产认证，在提高终端用户数字资产安全性的同时，帮助实现统一的资产监管和互认互通。DNA认证服务数据采集采用接口报送的方式，由客户通过认证服务接口自主上报，向【DNA注册认证平台】报送数字资产基础数据及其关联事件数据，完成数字资产认证。

认证后的数字资产，支持用户通过DNA浏览器查询该数字资产详情、历史交易信息及当前持有账户信息。

DNA认证服务的应用方申请及管理需集成到DNA注册认证平台管理端，具体功能需求如下：

| 接口类型             | 服务名称                                                     | 描述                                                         |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 数据资产基础数据     | 数字资产集合信息认证                                         | 集合是一种资产类型的标记，方便认证资产进行分类和管理；实现数字资产认证前必须完成数字资产集合信息认证；不支持更新；支持批量认证，单次不超过100；不上链。 |
| 数字资产认证         | 应用方上传数字资产相关信息，完成数字资产认证；不支持更新；支持批量认证，单次不超过100；部分信息上链，DNABid及metadata hash上链。 |                                                              |
| 数字资产相关事件数据 | 资产转移认证                                                 | 应用方上传认证数字资产转移交易信息，完成资产转移认证；支持批量认证，单次不超过100；不支持更新；同步更新资产owner;不上链； |
| 资产销毁认证         | 应用方上传认证数字资产销毁交易信息，完成资产注销认证；支持批量认证，单次不超过100；不支持更新；同步更新资产owner;不上链 |                                                              |

## 2.接入说明

第一步：创建星火账户及企业认证；安装星火通并完成星火账户创建及企业认证。具体操作指引详见**浏览器插件钱包**章节。

第二步：签署协议及申请准入；完成相关协议签署后邮件联系运营方（邮箱），提交星火账户（BID）、企业认证材料、应用平台资料，获取apiKey及apiSecret。

apiKey开发者的身份ID，可用于获取接入方的调用凭证（access_token），然后通过接口调用凭证再来访问数字资产注册认证平台API。

apiSecret开发者身份ID对应的密钥，配合API_key使用能够获取接口调用凭证，同时为了安全起见这个密钥需要妥善保管。

第三步：接入测试；接入测试环境进行接入测试。

第四步：应用对接；用下发的apiKey/apiSecret接入正式环境，开始使用。

## 3.通用说明

### 3.1通用说明

数字资产注册认证平台API调用遵循HTTP协议，提供生产环境和开发测试环境，接入方式先通过测试环境进行测试验证，接入测试成功后再接入数字资产注册认证平台正式环境。在正式环境发行数字资产需要用户提前至少7个工作日填报发行信息进行备案。

Ø 正式环境域名为：[https://dna.bitfactory.cn](https://dna.bitfactory.cn)

Ø 测试环境域名为：[https://test-dna.bitfactory.cn](https://test-dna.bitfactory.cn)

### 3.2API认证机制

所有API的安全认证一律采用accessToken认证，服务端根据生成算法验证认证字符串的正确性。accessToken需要应用方通过apiKey和apiSecret调用相关平台接口获得，具有时效性，有效时间为2小时，过期后需要重新获取否则会调用接口失败，建议妥善保存并管理。

### 3.3操作指引

l 创建企业的星火账户

![image.png](../images/F08h2sJHaqI7RHXYiAabg.png)

l 获取accessToken

![image.png](../images/VuYa7Ni7o0xKavMsb4lA.png)

l 创建用户的星火账户

![image.png](../images/ENNk4_19K-R5RfaR-AibXw.png)

l 创建数字资产集合

![image.png](../images/I80Sf56CK4xDc8Fp8uCeSA.png)

l 转移/销毁数字资产

![image.png](../images/NoGeJLPFJCnvzam6tU_K_Q.png)

## 4.接口认证及账户管理

### 4.1.获取access token

```http
https://{{url}}/registration/api/v2/getToken
```

**请求方式**

**GET**

**请求参数**

| **字段名** | **类型** | **是否必填** | **描述**                               |
| ---------- | -------- | ------------ | -------------------------------------- |
| apiKey     | string   | 是           | 应用审批通过后，每个应用对应一个apiKey |
| apiSecret  | string   | 是           | apiSecret                              |

**响应参数**

| **字段名**  | **类型** | **是否必填** | **描述**                                                     |
| ----------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode     | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg      | string   |              | 200-OK<br/>400-apiKey必填、apiSecret必填、apiKey或apiSecret不正确<br/>500-服务错误 |
| accessToken | string   |              | 用于B端用户调用接口                                          |

**请求示例：**

![image.png](../images/image-20220916152903875.png)

**响应示例：**

```json
{
    "retCode": 200,
    "retMsg": "ok",
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBcHBJZCI6IjA0OWUyYzI0LWIxODYtNDZlZC04OWQ2LTBjYmMyM2FjMGJiOCIsIkJpZlVzZXJCaWQiOiJkaWQ6YmlkOmVmSjZSM1RqVE1HSkZLTkplOGJCenNKNmlpak5tRVBkIiwiZXhwIjoxNjU2NjczODM5LCJpYXQiOjE2NTY1ODc0Mzl9.4zNysZbpG8IUhNbGgp0oYy0cVM-T-N2J-xJhRc2ie3U"
}
```

### 4.2.生成公私钥

参照**bif-offline-api 2.1章节**

```
http://localhost:8888/bifApi/v1/createAddress
```

**请求方式**

**POST**

**请求参数**

| **字段名** | **类型** | **是否必填** | **描述**                      |
| ---------- | -------- | ------------ | ----------------------------- |
| type       | Int      | 是           | 必填, 加密类型1:ed25519 2:sm2 |

**响应参数**

| **字段名**         | **类型** | **是否必填** | **描述**                                               |
| ------------------ | -------- | ------------ | ------------------------------------------------------ |
| code               | int      |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误 |
| message            | string   |              | 200-OK<br/>400-type必填<br/>500-服务错误               |
| data               | object   |              |                                                        |
| data.encAddress    | string   |              | BID地址                                                |
| data.encPublicKey  | string   |              | 公钥                                                   |
| data.encPrivateKey | string   |              | 私钥                                                   |

**请求示例：**

![image.png](../images/image-20220916161149316.png)

**请求体:**

```json
{
    "keyType":1
}
```

**响应示例：**

```json
{
    "code": 200,
    "data": {
        "encAddress": "did:bid:efdYBMrB1SNjXkV6bLy3w3Hww1Ntv2Up",
        "encPrivateKey": "priSPKpY6TuPUZyCuJeaTpUJ1uRYVycNZmpmCuAxC6EhsjdhNX",
        "encPublicKey": "b065668a006b9f68a9ac94f042161f3f0353ccfab47fa9199b8f1889b7d7659d875aa2"
    },
    "message": "ok"
}
```

### 4.3.构造合约签名交易

参照**bif-offline-api 2.8章节**

```http
http://localhost:8888/bifApi/v1/contract
```

**请求方式**

**POST**

**请求参数**

| **字段名**       | **类型** | **是否必填** | **描述**                                                     |
| ---------------- | -------- | ------------ | ------------------------------------------------------------ |
| senderAddress    | string   | 是           | 交易源账号，即交易的发起方                                   |
| senderPrivateKey | string   | 是           | 交易源账户私钥                                               |
| contractAddress  | string   | 是           | 合约账户地址xxxxxxxxx                                        |
| bifAmount        | int64    | 是           | 转账金额 ，参数为 0                                          |
| feeLimit         | int64    | 是           | 参数为200000000                                              |
| gasPrice         | int64    | 是           | gas费，参数为200                                             |
| nonce            | int64    | 是           | nonce  需要从链上获取，参照接口6.8                           |
| input            | string   | 是           | 待触发的合约的main()入参，为调用上链交易接口的入参数<br/>转移数字资产"input":{"{\"function\":\"safeTransferFrom(address,address,string)\",\"args\":\"fromAddress,toAddress,'tokenBid'\"}} |

**input参数**

| **字段名**  | **类型** | **是否必填** | **描述**                                                     |
| ----------- | -------- | ------------ | ------------------------------------------------------------ |
| tokenBid    | string   | 是           | 数字资产bid，每个数字资产绑定一个主链bid作为唯一识别。调用星火链网接口获取主链bid |
| fromAddress | string   | 是           | 用户数字资产持有者地址,保证都是应用下的账户                  |
| toAddress   | string   | 是           | 用户接收数字资产的地址，保证都是应用下的账户                 |

**响应参数**

| **字段名**         | **类型** | **是否必填** | **描述**                              |
| ------------------ | -------- | ------------ | ------------------------------------- |
| code               | int      |              | 返回状态码，取值：200-成功，其他-错误 |
| message            | string   |              | 错误原因                              |
| data               | object   |              |                                       |
| data.serialization | string   |              | 序列化的交易数据                      |
| data.signData      | string   |              | 交易签名数据                          |
| data.publicKey     | string   |              | 公钥                                  |

**请求示例：**

![image.png](../images/image-20220916154212445.png)

**请求体：**

```json
{
"senderAddress": "did:bid:efQ69GRtQUDR9SngdFKAv4owYyx5Fnko",
"senderPrivateKey":"priSPKi7K3nVAgtdCu9k9hVn4modxzFkd73JGsRrUYJR1T2RxM",
"contractAddress":"did:bid:efAHUyTyhCdUXSxb3znw3Jw4ET24GdCk",
"bifAmount":0, 
"feeLimit":100000000, 
"gasPrice":10,                                 
"nonce":33,  
"input":"{\"function\":\"safeTransferFrom(address,address,string)\",\"args\":\"did:bid:efQ69GRtQUDR9SngdFKAv4owYyx5Fnko,did:bid:ef1L8GBs9mWzeKXGiAZC877WResz6y7,'did:bid:efDtTjWBLkJjtRSJFMfBLNJ6LjnKu1tV'\"}"
}

```

**响应示例**:

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

### 4.4构造合约签名交易

参照**bif-offline-api 2.8章节**

```http
http://localhost:8888/bifApi/v1/contract
```

**请求方式**

**POST**

**请求参数**

| **字段名**       | **类型** | **是否必填** | **描述**                                                     |
| ---------------- | -------- | ------------ | ------------------------------------------------------------ |
| senderAddress    | string   | 是           | 交易源账号，即交易的发起方                                   |
| senderPrivateKey | string   | 是           | 交易源账户私钥                                               |
| contractAddress  | string   | 是           | 合约账户地址xxxxxxxxx                                        |
| bifAmount        | int64    | 是           | 转账金额 ，参数为 0                                          |
| feeLimit         | int64    | 是           | 参数为200000000                                              |
| gasPrice         | int64    | 是           | gas费，参数为200                                             |
| nonce            | int64    | 是           | nonce  需要从链上获取，参照接口6.10                          |
| input            | string   | 是           | 待触发的合约的main()入参，为调用上链交易接口的入参数<br/>销毁数字资产"input":{"{\"function\":\"burn(string)\",\"args\":\"'tokenBid'\"}"} |

input参数

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| tokenBid   | string   | 是           | 数字资产bid，每个数字资产绑定一个主链bid作为唯一识别。调用星火链网接口获取主链bid |

**响应参数**

| **字段名**         | **类型** | **是否必填** | **描述**                              |
| ------------------ | -------- | ------------ | ------------------------------------- |
| code               | int      |              | 返回状态码，取值：200-成功，其他-错误 |
| message            | string   |              | 错误原因                              |
| data               | object   |              |                                       |
| data.serialization | string   |              | 序列化的交易数据                      |
| data.signData      | string   |              | 交易签名数据                          |
| data.publicKey     | string   |              | 公钥                                  |

**请求示例：**

![image-20220916160410728](../images/image-20220916160410728.png)

**请求体：**

```json
{
"senderAddress": "did:bid:efQ69GRtQUDR9SngdFKAv4owYyx5Fnko",
"senderPrivateKey":"priSPKi7K3nVAgtdCu9k9hVn4modxzFkd73JGsRrUYJR1T2RxM",
"contractAddress":"did:bid:efAHUyTyhCdUXSxb3znw3Jw4ET24GdCk",
"bifAmount":0, 
"feeLimit":100000000, 
"gasPrice":10,                                 
"nonce":33,  
"input":"{\"function\":\"burn(string)\",\"args\":\"'did:bid:efDtTjWBLkJjtRSJFMfBLNJ6LjnKu1tV'\"}"
}

```

**响应示例:**

```json
{
    "code": 200,
    "data": {
        "serialization": "0a286469643a6269643a65665136394752745155445239536e6764464b4176346f7759797835466e6b6f1021227f0807527b0a286469643a6269643a65664148557954796843645558537862337a6e77334a7734455432344764436b1a4f7b2266756e6374696f6e223a226275726e28737472696e6729222c2261726773223a22276469643a6269643a65664474546a57424c6b4a6a7452534a464d66424c4e4a364c6a6e4b7531745627227d3080c2d72f380a",
        "signData": "2be1050f4663ebcce8a5afe4d76d83079575742f24842026cedd075a7df5ba81a0caecf2ce9de66bf0a37411fef1e422162c840dd07f7870a0578028fa53c502",
        "publicKey": "b06566d8fb4a6dfbe0d5831e38f621391ad9191626f7e28c13d3a0482c52d5c9607b14"
    },
    "message": "ok"
}
```

## 5.集合操作

### 5.1.创建数字资产集合

```http
https://{url}/registration/api/v2/series/add
```

**请求方式**

**POST**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**            |
| ----------- | -------- | ------------ | ------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口 |

**请求参数**

| **字段名**   | **类型** | **是否必填** | **描述**                             |
| ------------ | -------- | ------------ | ------------------------------------ |
| seriesIssuer | string   | 是           | 集合发行方                           |
| seriesName   | string   | 是           | 集合名称，不超过50个字符             |
| seriesDes    | string   | 否           | 集合描述，不超过200个字符            |
| externalUrl  | string   | 否           | 外部连接，可以展示数字资产相关的网站 |

**响应参数**

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode    | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg     | string   |              | 200-OK<br/>400-accessToken必填、accessToken不正确、accessToken过期、请检查请求参数,请求参数不能为空字符串、集合名称过长，不允许超过30字符、集合名称不允许重复、集合描述不允许超过200个字符<br/>500-服务错误 |
| seriesId   | string   |              | 集合ID                                                       |
| createTime | string   |              | 集合创建时间                                                 |

**请求示例：**

![image-20220916162123988](../images/image-20220916162123988.png)

![image-20220916162029569](../images/image-20220916162029569.png)

**请求体:**

```json
{
"seriesIssuer":"央视",
"seriesName":"央视20220816",
"seriesDes":"萌萌图可爱填写超过",
"externalUrl":"http://www.baidu.com/"
}
```

**响应示例：**

```json
{
    "retCode": 200,
    "retMsg": "ok",
    "seriesId": "0af84ba9-545b-40b3-854a-a94d6bb626d6",
    "createTime": "2022-09-16 16:22:58"
}
```

### **5.2.查询数字资产集合列表**

```http
https://{url}/registration/api/v2/series/list/?pageNum=1&pageSize=20
```

**请求方式**

**GET**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**            |
| ----------- | -------- | ------------ | ------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口 |

**请求参数**

| **字段名** | **类型** | **是否必填** | **描述** |
| ---------- | -------- | ------------ | -------- |
| pageNum    | string   | 是           | 页码     |
| pageSize   | string   | 是           | 数量     |

**响应参数**

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode    | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg     | string   |              | 200-OK<br/>400-accessToken必填、accessToken不正确、accessToken过期<br/>500-服务错误 |
| total      | number   |              | 总数                                                         |
| data       | object[] |              | 应用下的集合列表                                             |

Data结构如下:

| **字段名**   | **类型** | **是否必填** | **描述**                             |
| ------------ | -------- | ------------ | ------------------------------------ |
| seriesIssuer | string   |              | 集合发行方                           |
| seriesName   | string   |              | 集合名称，不超过50个字符             |
| seriesDes    | string   |              | 集合描述，不超过200个字符            |
| externalUrl  | string   |              | 外部连接，可以展示数字资产相关的网站 |
| createTime   | string   |              | 集合创建时间                         |
| appId        | string   |              | 应用id                               |
| seriesId     | string   |              | 集合id                               |

**请求示例：**

![image-20220916163033865](../images/image-20220916163033865.png)

**响应示例：**

```json
{
    "retCode": 200,
    "retMsg": "ok",
    "total": 1,
    "data": [
        {
            "seriesId": "858fae5d-e6de-41b1-9c75-3be9dd4a69cb",
            "appId": "6245b2ea-af5d-49f1-ab6b-5aa8fb401668",
            "seriesIssuer": "发行方公司",
            "seriesName": "并发集合12",
            "seriesDes": "萌萌",
            "externalUrl": "http://www.baidu.com/",
            "createTime": "2022-07-09 19:30:04"
        }
    ]
}
```



### 5.3.查询数字资产集合详情

```http
https://{url}/registration/api/v2/series/{seriesId}
```

**请求方式**

**GET**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**            |
| ----------- | -------- | ------------ | ------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口 |

**请求参数**

| **字段名** | **类型** | **是否必填** | **描述** |
| ---------- | -------- | ------------ | -------- |
| seriesId   | string   | 是           | 集合ID   |

**响应参数**

| **字段名**   | **类型** | **是否必填** | **描述**                                                     |
| ------------ | -------- | ------------ | ------------------------------------------------------------ |
| retCode      | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg       | string   |              | 200-OK<br/>400-accessToken必填、accessToken不正确、accessToken过期、集合id未填写或者集合id错误、集合id不正确、集合id不存在<br/>500-服务错误 |
| seriesIssuer | string   |              | 集合发行方                                                   |
| seriesName   | string   |              | 集合名称，不超过50个字符                                     |
| seriesDes    | string   |              | 集合描述，不超过200个字符                                    |
| externalUrl  | string   |              | 外部连接，可以展示数字资产相关的网站                         |
| createTime   | string   |              | 集合创建时间                                                 |
| appId        | string   |              | 应用id                                                       |
| seriesId     | string   |              | 集合id                                                       |

**请求示例：**

![image-20220916162123988](../images/image-20220916162123988.png)

![image-20220916163411720](../images/image-20220916163411720.png)

**响应示例：**

```json
{
    "retCode": 200,
    "retMsg": "ok",
    "seriesId": "858fae5d-e6de-41b1-9c75-3be9dd4a69cb",
    "appId": "6245b2ea-af5d-49f1-ab6b-5aa8fb401668",
    "seriesIssuer": "发行方公司",
    "seriesName": "并发集合12",
    "seriesDes": "萌萌",
    "externalUrl": "http://www.baidu.com/",
    "createTime": "2022-07-09 19:30:04"
}
```

### 5.4.通过集合ID查询数字资产

```http
https://{url}//registration/api/v2/:seriesId/dna
```

**请求方式**

**GET**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**            |
| ----------- | -------- | ------------ | ------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口 |

**请求参数**

| **字段名** | **类型** | **是否必填** | **描述** |
| ---------- | -------- | ------------ | -------- |
| seriesId   | string   | 是           | 集合ID   |
| pageNum    | string   | 是           | 页码     |
| pageSize   | string   | 是           | 每页条数 |

**响应参数**

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode    | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg     | string   |              | 200-OK<br>400-accessToken必填、accessToken不正确、accessToken过期、请检查请求参数,请求参数不能为空字符串、集合id不存在<br>500-服务错误 |
| total      | number   |              | 总数                                                         |
| data       | object[] |              |                                                              |

Data结构如下:

| **字段名**  | **类型** | **是否必填** | **描述**                                   |
| ----------- | -------- | ------------ | ------------------------------------------ |
| seriesId    | string   |              | 集合ID                                     |
| dnaName     | string   |              | 数字资产名称，不超过50个字符               |
| dnaNumber   | string   |              | 数字资产编号，集合内不重复                 |
| dnaDes      | string   |              | 数字资产描述，不超过200个字符              |
| url         | string   |              | 数字资产 url，建议尺寸：350*350            |
| hash        | string   |              | 数字资产图片哈希值                         |
| displayUrl  | string   |              | 数字资产缩略图url，建议尺寸：85*85         |
| dnaPrice    | number   |              | 数字资产价格                               |
| dnaCategory | string   |              | 资产类型：图片、视频、音频                 |
| extension   | string   |              | 扩展字段，用户自定义，长度不超过1024个字符 |
| tokenBid    | string   |              | 数字资产bid                                |
| createTime  | string   |              | 创建时间                                   |

**请求示例：**

![image-20220916162123988](../images/image-20220916162123988.png)

![image-20220916163839382](../images/image-20220916163839382.png)

**响应示例：**

```json
{
    "retCode": 200,
    "retMsg": "ok",
    "total": 12300,
    "data": [
         {
            "tokenBid": "did:bid:ef7aD319SwD6NNVHHSQ2nDCxUeNzNtSf",
            "dnaNumber": "000008",
            "createTime": "2022-08-23 12:22:22",
            "dnaName": "测试000008",
            "dnaDes": "测试000008号数字资产",
            "displayUrl": "http://ww.baidu.com",
            "seriesId": "3ddfafca-5ec8-455f-a6ee-c5ccacb5aa7d",
            "dnaCategory": "图片",
            "hash": "123",
            "extension": "扩展字符",
            "url": "http://ww.baidu.com",
            "dnaPrice": 199
        }
    ]
}
```

## 6.资产操作

### 6.1.注册数字资产

```http
https://{url}/registration/api/v2/chain/mintDNA
```

**请求方式**

**POST**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**            |
| ----------- | -------- | ------------ | ------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口 |

**请求参数**

| **字段名**  | **类型** | **是否必填** | **描述**                                   |
| ----------- | -------- | ------------ | ------------------------------------------ |
| seriesId    | string   | 是           | 集合ID                                     |
| dnaName     | string   | 是           | 数字资产名称，不超过50个字符               |
| dnaNumber   | string   | 是           | 数字资产编号，集合内不重复                 |
| dnaDes      | string   | 否           | 数字资产描述，不超过200个字符              |
| url         | string   | 是           | 数字资产 url，建议尺寸：350*350            |
| hash        | string   | 是           | 数字资产图片哈希值                         |
| displayUrl  | string   | 是           | 数字资产缩略图url，建议尺寸：85*85         |
| toBid       | string   | 是           | 用户数字资产持有者地址                     |
| dnaPrice    | number   | 是           | 数字资产价格                               |
| dnaCategory | string   | 是           | 资产类型：图片、视频、音频                 |
| extension   | string   | 否           | 扩展字段，用户自定义，长度不超过1024个字符 |

**响应参数**

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode    | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg     | string   |              | 200-OK<br>400-accessToken必填、accessToken不正确、accessToken过期、请检查请求参数,请求参数不能为空字符串、集合ID不正确、集合ID不存在、集合ID重复、数字资产名称不应超过50个字符、数字资产名称编号重复、请输入正确格式的数字资产url、请输入正确格式的数字资产缩略图url<br/>500-服务错误 |
| messageId  | string   |              | 消息id，用于查询处理结果                                     |

**请求示例：**

![image-20220916162123988](../images/image-20220916162123988.png)

![image-20220916164326147](../images/image-20220916164326147.png)

**请求体：**

```json
{
    "seriesId":"{{seriesId}}",
   "dnaName": "测试000008",
    "dnaNumber": "000008",
    "dnaDes": "测试000008号数字资产",
    "url": "http://ww.baidu.com",
    "displayUrl": "http://ww.baidu.com",
    "toBid": "did:bid:ef6tofMj7gv1rMFAPkh6rG4p7oXuXoFv",
    "extension": "扩展字符",
    "hash": "123",
    "dnaPrice": 199,
    "dnaCategory": "图片"
}
```

**响应示例：**

```json
{
    "retCode": 200,
    "retMsg": "ok",
    "messageId": "cd02578529ef4258a301baf8728b7c96"
}
```

### 6.2.批量注册数字资产

```http
https://{url}/registration/api/v2/chain/batchMintDNA
```

**请求方式**

**POST**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**            |
| ----------- | -------- | ------------ | ------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口 |

**请求参数**

| **字段名** | **类型** | **是否必填** | **描述**              |
| ---------- | -------- | ------------ | --------------------- |
| data       | object[] |              | nft列表,长度不超过100 |

Data结构如下:

| **字段名**  | **类型** | **是否必填** | **描述**                                   |
| ----------- | -------- | ------------ | ------------------------------------------ |
| seriesId    | string   | 是           | 集合ID                                     |
| dnaName     | string   | 是           | 数字资产名称，不超过50个字符               |
| dnaNumber   | string   | 是           | 数字资产编号，集合内不重复                 |
| dnaDes      | string   | 否           | 数字资产描述，不超过200个字符              |
| url         | string   | 是           | 数字资产 url，建议尺寸：350*350            |
| hash        | string   | 是           | 数字资产图片哈希值                         |
| displayUrl  | string   | 是           | 数字资产缩略图url，建议尺寸：85*85         |
| toBid       | string   | 是           | 用户数字资产持有者地址                     |
| dnaPrice    | number   | 是           | 数字资产价格，小数点后保留2位              |
| dnaCategory | string   | 是           | 资产类型：图片、视频、音频                 |
| extension   | string   | 否           | 扩展字段，用户自定义，长度不超过1024个字符 |

**响应参数**

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode    | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg     | string   |              | 200-OK<br>400-accessToken必填、accessToken不正确、accessToken过期、请检查请求参数,请求参数不能为空字符串、集合ID不正确、集合ID不存在、集合ID重复、数字资产名称不应超过50个字符、数字资产名称编号重复、请输入正确格式的数字资产url、请输入正确格式的数字资产缩略图url<br/>500-服务错误 |
| messageId  | string   |              | 消息id，用于查询上链状态                                     |

**请求示例：**

![image-20220916162123988](../images/image-20220916162123988.png)

![image-20220916164741621](../images/image-20220916164741621.png)

**请求体：**

```json
{
    "data": [
         {
            "seriesId": "{{seriesId}}",
            "dnaName": "萌萌图可爱填写超过",
            "dnaNumber": "1396",
            "dnaDes": "萌萌图可爱填",
            "url": "http://ww.baidu.com",
            "displayUrl": "http://ww.baidu.com",
            "toBid": "did:bid:efpJ7ySzrVrRsi9kZpoCibmhQmrEJbp1",
            "extension": "萌萌图可爱填写超过个字符萌萌图可",
            "hash": "XMT7BQPcnd6eAxWnvACu",
            "dnaPrice": 1.24,
            "dnaCategory":"图片"
        },
        {
            "seriesId": "{{seriesId}}",
            "dnaName": "brx测试",
            "dnaNumber": "02",
            "dnaDes": "描述2",
            "url": "http://ww.baidu.com",
            "displayUrl": "http://ww.baidu.com",
            "toBid": "did:bid:efpJ7ySzrVrRsi9kZpoCibmhQmrEJbp1",
            "extension": "萌萌图可",
            "hash": "XMT7BQPcnd6eAxWnvACu",
            "dnaPrice": 1.24,
            "dnaCategory":"图片"
        }
          ]
}
```

**响应示例：**

```json
{
    "retCode": 200,
    "retMsg": "ok",
    "messageId": "3407d9b6c4d941c1a51c9b2fe2a66a58"
}
```

### 6.3.转移字资产接口

```http
https://{url}/registration/api/v2/chain/transferDNA
```

**请求方式**

**POST**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**            |
| ----------- | -------- | ------------ | ------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口 |

**请求参数**

| **字段名**    | **类型** | **是否必填** | **描述**                                                     |
| ------------- | -------- | ------------ | ------------------------------------------------------------ |
| tokenBid      | string   | 是           | 数字资产bid，每个数字资产绑定一个主链bid作为唯一识别。调用星火链网接口获取主链bid |
| fromBid       | string   | 是           | 用户数字资产持有者地址,保证都是应用下的账户                  |
| toBid         | string   | 是           | 用户接收数字资产的地址，保证都是应用下的账户                 |
| serialization | string   | 是           | 序列化的交易数据                                             |
| signData      | string   | 是           | 交易签名数据                                                 |
| publicKey     | string   | 是           | 公钥                                                         |

**响应参数**

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode    | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg     | string   |              | 200-OK<br>400-accessToken必填、accessToken不正确、accessToken过期、请检查请求参数,请求参数不能为空字符串、数字资产bid不正确、用户数字资产持有者地址必填、用户数字资产持有者地址不存在、用户数字资产持有者地址不正确、用户接收数字资产的地址不正确<br/>500-服务错误 |
| messageId  | string   |              | 消息id，用于查询处理结果                                     |

**请求示例：**

![image-20220916162123988](../images/image-20220916162123988.png)

![image-20220916165606244](../images/image-20220916165606244.png)

**请求体：**

```json
{
"tokenBid":"did:bid:effDbwjLCPLypvHjGyDfwis3VHaNZmuT",
"fromBid":"did:bid:efyHiBTd4fbavvr86S7a5zFmBvMyAWhR",
"toBid":"did:bid:efULSmsPJDFR23rsjC8XrdfHZPYV62NU",
"serialization":"0a286469643a6269643a6566704a3779537a725672527369396b5a706f4369626d68516d72454a62703110cd0922ef01080752ea010a286469643a6269643a65664148557954796843645558537862337a6e77334a7734455432344764436b1abd017b2266756e6374696f6e223a22736166655472616e7366657246726f6d28616464726573732c616464726573732c737472696e6729222c2261726773223a226469643a6269643a6566704a3779537a725672527369396b5a706f4369626d68516d72454a6270312c6469643a6269643a656657623866786d6163654c656f434a31567359444e47556d4845396a4d33542c276469643a6269643a65665464746f55356f7a36316d4d613573474c486d7a7651415338357263756f27227d3080dac40938c801",
"signData":"068198e33d8783c1b3f723c6b75d5918dcc2fc465e52e4cd75c3180507db833ad44830869ff30ab4276dc14e02fd12ca3075d73df5b9fbfa5f52b5aba5265804",
"publicKey":"b0656658bd49d9e5318078bdf1833fcc750a80377ab635405517fc8c7874613008f50e"
}
```

**响应示例：**

```json
{
    "retCode": 200,
    "retMsg": "ok",
    "messageId": "9c01734d9a864a06b79993d31c0dd967"
}
```

### 6.4.销毁数字资产接口

```http
https://{url}/registration/api/v2/chain/burnDNA
```

**请求方式**

**POST**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**            |
| ----------- | -------- | ------------ | ------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口 |

**请求参数**

| **字段名**    | **类型** | **是否必填** | **描述**                                                     |
| ------------- | -------- | ------------ | ------------------------------------------------------------ |
| tokenBid      | string   | 是           | 数字资产bid，每个数字资产绑定一个主链bid作为唯一识别。调用星火链网接口获取主链bid |
| fromBid       | string   | 是           | 用户数字资产持有者地址                                       |
| serialization | string   | 是           | 序列化的交易数据                                             |
| signData      | string   | 是           | 交易签名数据                                                 |
| publicKey     | string   | 是           | 公钥                                                         |

**响应参数**

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode    | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg     | string   |              | 200-OK400-accessToken必填400-accessToken不正确400-accessToken过期400-请检查请求参数,请求参数不能为空字符串400-数字资产bid不存在400-用户数字资产持有者不正确400-用户数字资产持有者不存在500-服务错误 |
| messageId  | string   |              | 消息id，用于查询处理结果                                     |

**请求示例：**

![image-20220916162123988](../images/image-20220916162123988.png)

![image-20220916170205598](../images/image-20220916170205598.png)

**请求体：**

```json
{
"tokenBid":"did:bid:ef8By2pnXDkCtYePM14s1c4eJFMRwWiY",
"fromBid":"did:bid:efWb8fxmaceLeoCJ1VsYDNGUmHE9jM3T",
"serialization":"0a286469643a6269643a6566704a3779537a725672527369396b5a706f4369626d68516d72454a62703110cd0922ef01080752ea010a286469643a6269643a65664148557954796843645558537862337a6e77334a7734455432344764436b1abd017b2266756e6374696f6e223a22736166655472616e7366657246726f6d28616464726573732c616464726573732c737472696e6729222c2261726773223a226469643a6269643a6566704a3779537a725672527369396b5a706f4369626d68516d72454a6270312c6469643a6269643a656657623866786d6163654c656f434a31567359444e47556d4845396a4d33542c276469643a6269643a65665464746f55356f7a36316d4d613573474c486d7a7651415338357263756f27227d3080dac40938c801",
"signData":"068198e33d8783c1b3f723c6b75d5918dcc2fc465e52e4cd75c3180507db8",
"publicKey":"b0656658bd49d9e5318078bdf1833fcc750a80377ab635405517fc8c7874613008f50e"
}
```

**响应示例：**

```json
{
    "retCode": 200,
    "retMsg": "ok",
    "messageId": "d711f409a48c42299aed1f1cc6672996"
}
```

### 6.5.通过用户bid查询数字资产

```http
https://{url}/registration/api/v2/dna/:userId
```

**请求方式**

**GET**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**            |
| ----------- | -------- | ------------ | ------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口 |

**请求参数**

| **字段名** | **类型** | **是否必填** | **描述**                |
| ---------- | -------- | ------------ | ----------------------- |
| userId     | string   | 是           | 用户在星火主链的bid账户 |
| pageNum    | string   | 是           | 页码                    |
| pageSize   | string   | 是           | 每页条数                |

**响应参数**

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode    | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg     | string   |              | 200-OK<br>400-accessToken必填、accessToken不正确、accessToken过期、请检查请求参数,请求参数不能为空字符串<br/>500-服务错误 |
| total      | number   |              | 总数                                                         |
| data       | object[] |              |                                                              |

Data结构如下:

| **字段名**  | **类型** | **是否必填** | **描述**                                   |
| ----------- | -------- | ------------ | ------------------------------------------ |
| seriesId    | string   |              | 集合ID                                     |
| dnaName     | string   |              | 数字资产名称，不超过50个字符               |
| dnaNumber   | string   |              | 数字资产编号，集合内不重复                 |
| dnaDes      | string   |              | 数字资产描述，不超过200个字符              |
| url         | string   |              | 数字资产 url，建议尺寸：350*350            |
| hash        | string   |              | 数字资产图片哈希值                         |
| displayUrl  | string   |              | 数字资产缩略图url，建议尺寸：85*85         |
| dnaPrice    | number   |              | 数字资产价格                               |
| dnaCategory | string   |              | 资产类型：图片、视频、音频                 |
| extension   | string   |              | 扩展字段，用户自定义，长度不超过1024个字符 |
| tokenBid    | string   |              | 数字资产bid                                |
| createTime  | string   |              | 创建时间                                   |

**请求示例：**

![image-20220916162123988](../images/image-20220916162123988.png)

![image-20220916170534405](../images/image-20220916170534405.png)

 **响应示例：**

```json
{
    "retCode": 200,
    "retMsg": "ok",
    "total": 114000,
    "data": [
        {
            "seriesId": "074b82db-9fed-42da-9b0e-00c579260775",
            "tokenBid": "did:bid:ef5KEkJMzFFFzV1j6Nv5ryj9tf6fs8NM",
            "dnaNumber": "0291b994-d332-41ee-8ce8-1e8da940a01c",
            "createTime": "2022-07-13 05:26:47",
            "dnaName": "brx测试",
            "dnaDes": "描述2",
            "displayUrl": "描述2",
            "dnaCategory": "图片",
            "hash": "XMT7BQPcnd6eAxWnvACu",
            "extension": "萌萌图可",
            "url": "http://ww.baidu.com",
            "dnaPrice": 1.24
        }   
    ]
}
```

### 6.6.查询数字资产详情

```http
https://{url}/registration/api/v2/dnaDetail?tokenBid
```

**请求方式**

**GET**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**            |
| ----------- | -------- | ------------ | ------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口 |

**请求参数**

| **字段名** | **类型** | **是否必填** | **描述**    |
| ---------- | -------- | ------------ | ----------- |
| tokenBid   | string   | 是           | 数字资产bid |

**响应参数**

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode    | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg     | string   |              | 200-OK<br>400-accessToken必填、accessToken不正确、accessToken过期、请检查请求参数,请求参数不能为空字符串、tokenBid不存在<br/>500-服务错误 |
| data       | object   |              | 对应数字资产详情                                             |

Data结构如下：

| **字段名**  | **类型** | **是否必填** | **描述**                                   |
| ----------- | -------- | ------------ | ------------------------------------------ |
| seriesId    | string   |              | 集合ID                                     |
| dnaName     | string   |              | 数字资产名称，不超过50个字符               |
| dnaNumber   | string   |              | 数字资产编号，集合内不重复                 |
| dnaDes      | string   |              | 数字资产描述，不超过500个字符              |
| url         | string   |              | 数字资产 url，建议尺寸：350*350            |
| hash        | string   |              | 数字资产图片哈希值                         |
| displayUrl  | string   |              | 数字资产缩略图url，建议尺寸：85*85         |
| dnaPrice    | number   |              | 数字资产价格                               |
| dnaCategory | string   |              | 资产类型：图片、视频、音频                 |
| extension   | string   |              | 扩展字段，用户自定义，长度不超过1024个字符 |
| tokenBid    | string   |              | 数字资产bid                                |
| createTime  | string   |              | 创建时间                                   |

**请求示例：**

![image-20220916162123988](../images/image-20220916162123988.png)

![image-20220916170855097](../images/image-20220916170855097.png)

**响应示例：**

```json
{
    "retCode": 200,
    "retMsg": "ok",
    "data": {
        "tokenBid": "did:bid:efRDFqF54C89FhQcSnhKyY4CmViMDo5n",
        "dnaNumber": "1111112",
        "createTime": "2022-07-13 16:58:31",
        "dnaName": "预发应用1集合1注册资产01",
        "dnaDes": "描述",
        "url": "http://ww.baidu.com",
        "displayUrl": "http://ww.baidu.com",
        "extension": "扩展字符",
        "hash": "123",
        "dnaPrice": 12,
        "seriesId": "2075affd-181c-4654-a294-e31c580901aa",
        "dnaCategory": "图片"
    }
}
```

### 6.7.查询数字资产操作记录

```http
https://{url}/registration/api/v2/record/:tokenBid
```

**请求方式**

**GET**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**            |
| ----------- | -------- | ------------ | ------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口 |

**请求参数**

| **字段名** | **类型** | **是否必填** | **描述**    |
| ---------- | -------- | ------------ | ----------- |
| tokenBid   | string   | 是           | 数字资产bid |
| pageNum    | string   | 是           | 页码        |
| pageSize   | string   | 是           | 每页条数    |

**响应参数**

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode    | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg     | string   |              | 200-OK<br>400-accessToken必填、accessToken不正确、accessToken过期、请检查请求参数,请求参数不能为空字符串、数字资产bid不存在<br/>500-服务错误 |
| total      | number   |              | 总数                                                         |
| data       | object[] |              |                                                              |

 Data结构如下:

| **字段名**    | **类型** | **是否必填** | **描述**                                                     |
| ------------- | -------- | ------------ | ------------------------------------------------------------ |
| dnaNumber     | string   |              | 数字资产编号，集合内不重复                                   |
| createTime    | string   |              | 数字资产创建时间                                             |
| txHash        | string   |              | 链上操作的hash                                               |
| operation     | number   |              | 数字资产操作类型，0-注册、1-转移、2-销毁、3-冻结、4-metadata |
| fromBid       | string   |              | 用户数字资产持有者地址                                       |
| toBid         | string   |              | 用户接收数字资产的地址                                       |
| operationDate | string   |              | 操作时间                                                     |

**请求示例：**

![image-20220916162123988](../images/image-20220916162123988.png)

![img](../images/RqizhLzGT8T55HQy42W3Fw.png)

响应参数：

```json
{
    "retCode": 200,
    "retMsg": "ok",
    "total": 2,
    "data": [
        {
            "txHash": "83ece7705bd3b358b7427edcf2cb75243e19777d2ca0a3978d86327a410e1ab5",
            "operation": 4,
            "fromBid": "did:bid:efVgVpyFFvG4xkYaEJkHF5bArV167wPv",
            "toBid": "did:bid:efpJ7ySzrVrRsi9kZpoCibmhQmrEJbp1",
            "operationDate": "2022-07-13 16:58:31",
            "dnaNumber": "1111112",
            "createTime": "2022-07-13 16:58:31"
        },
        {
            "txHash": "878c4c520f75622b40829d4f73d7786c82b1a2359dc5a4f8d729ed28e6e87b42",
            "operation": 0,
            "fromBid": "did:bid:efVgVpyFFvG4xkYaEJkHF5bArV167wPv",
            "toBid": "did:bid:efpJ7ySzrVrRsi9kZpoCibmhQmrEJbp1",
            "operationDate": "2022-07-13 16:58:31",
            "dnaNumber": "1111112",
            "createTime": "2022-07-13 16:58:31"
        }
    ]
}
```

### 6.8.查询tokenbid的拥有者

```http
https://{url}/registration/api/v2/chain/tokenOwnerOf/{tokenBid}
```

**请求方式**

**GET**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**            |
| ----------- | -------- | ------------ | ------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口 |

**请求参数**

| **字段名** | **类型** | **是否必填** | **描述**   |
| ---------- | -------- | ------------ | ---------- |
| tokenBid   | string   | 是           | 链账户身份 |

**响应参数**

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode    | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg     | string   |              | 200-OK<br>400-accessToken必填、accessToken不正确、accessToken过期<br/>500-服务错误 |
| bidAddress | string   |              | 返回参数：有结果：[did:bid:ef6tofMj7gv1rMFAPkh6rG4p7oXuXoFv]没结果则为空 |

**请求示例：**

![image-20220916162123988](../images/image-20220916162123988.png)

![image-20220916173029983](../images/image-20220916173029983.png)

**响应示例：**

```json
{
    "retCode": 200,
    "retMsg": "ok",
    "bidAddress": "[did:bid:ef6tofMj7gv1rMFAPkh6rG4p7oXuXoFv]"
}
```

### 6.9.根据消息id获取处理结果

```http
https://{url}/registration/api/v2/chain/message/{messageId}
```

**请求方式**

**GET**

**Header**

| **字段名**  | **类型** | **是否必填** | **描述**            |
| ----------- | -------- | ------------ | ------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口 |

**请求参数**

| **字段名** | **类型** | **是否必填** | **描述**                            |
| ---------- | -------- | ------------ | ----------------------------------- |
| messageId  | string   | 是           | 注册，转移，销毁接口返回的messageId |

**响应参数**

| **字段名** | **类型** | **描述**                                               |
| ---------- | -------- | ------------------------------------------------------ |
| retCode    | number   | 返回状态码，取值：200-成功，400-信息错误，500-服务错误 |
| retMsg     | string   | 200-OK<br>400-不存在的消息id<br>500-服务错误           |
| data       | object   | 资产数据                                               |

data 结构如下:

| **字段名** | **类型** | **描述**                                  |
| ---------- | -------- | ----------------------------------------- |
| state      | number   | 上链状态: 0 -已提交 1-上链失败 2-上链成功 |
| info       | object[] | 资产信息数组                              |
| txHash     | string   | 链上操作的hash                            |

info 结构如下:

| **字段名** | **类型** | **描述**     |
| ---------- | -------- | ------------ |
| seriesId   | string   | 集合id       |
| tokenBid   | string   | 数据资产bid  |
| message    | string   | 错误信息     |
| dnaNumber  | string   | 数据资产编号 |

**请求示例：**

![image-20220916162123988](../images/image-20220916162123988.png)

![image-20220916173345832](../images/image-20220916173345832.png)

**响应示例：**

```json
{
    "retCode": 200,
    "retMsg": "ok",
    "data": {
        "state": 2,
        "info": [
            {
                "seriesId": "0af84ba9-545b-40b3-854a-a94d6bb626d6",
                "tokenBid": "did:bid:efP7EGaAc7dsLyGkNPNDHFDV3GBA7FkD",
                "dnaNumber": "1396",
                "message": ""
            }
        ],
        "txHash": "35c3a00a4fe9ee1d195dbbeac3da7317c7a47cc214f318446ee3badb3370f9d9"
    }
}
```

### 6.10.获取当前地址nonce值

```http
https://{url}/registration/api/v2/chain/nonce
```

**请求方式**

**GET**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**            |
| ----------- | -------- | ------------ | ------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口 |

**请求参数**

| **字段名** | **类型** | **是否必填** | **描述**   |
| ---------- | -------- | ------------ | ---------- |
| userBid    | string   | 是           | 链账户身份 |

**响应参数**

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode    | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg     | string   |              | 200-OK<br>400-accessToken必填、accessToken不正确、accessToken过期、请检查请求参数,请求参数不能为空字符串、userBid不存在<br/>500-服务错误 |
| nonce      | number   |              | nonce值                                                      |

**请求示例：**

![image-20220916162123988](../images/image-20220916162123988.png)

![image-20220916173739518](../images/image-20220916173548824.png)

**响应示例**

```json
{
    "retCode": 200,
    "retMsg": "ok",
    "nonce": 55
}
```

## 7.认证数字资产

### 7.1获取access token

此接口详见**4.1**获取access token部分。

### 7.2数字资产集合信息认证接口

```http
https://{url}/auth/api/v1/series
```

**请求方式**

**POST**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**                  |
| ----------- | -------- | ------------ | ------------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口，通过 |

**请求参数**

| **字段名** | **类型** | **是否必填** | **描述**                        |
| ---------- | -------- | ------------ | ------------------------------- |
| data       | object[] |              | 认证集合列表，集合数量不超过100 |

Data结构如下:

| **字段名**      | **类型** | **是否必填** | **描述**                         |
| --------------- | -------- | ------------ | -------------------------------- |
| seriesName      | String   | 是           | 数字资产集合名称                 |
| seriesIssuer    | String   | 是           | 数字资产集合发行方               |
| externalUrl     | String   | 否           | 该集合对应网站的外部链接         |
| seriesDes       | String   | 否           | 集合描述说明                     |
| seriesId        | Object[] | 是           | 应用方集合id或相互关联的子集合id |
| totalDNA        | Number   | 是           | 集合下发行数字资产数量           |
| asset_contracts | String   | 是           | 与集合关联的合约地址             |

**响应参数**

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode    | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg     | string   |              | 200-OK<br/>400-accessToken必填、accessToken不正确、accessToken过期、请检查请求参数,请求参数不能为空字符串、集合ID重复、集合名称不应超过50个字符、集合名称重复<br/>500-服务错误 |

### 7.3数字资产认证接口

```http
https://{url}/auth/api/v1/dna
```

**请求方式**

**POST**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**                  |
| ----------- | -------- | ------------ | ------------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口，通过 |

**请求参数**

| **字段名** | **类型** | **是否必填** | **描述**                            |
| ---------- | -------- | ------------ | ----------------------------------- |
| data       | object[] |              | 认证数字资产列表，资产数量不超过100 |

Data结构如下:

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| seriesId   | String   | 是           | 资产所属集合id或子集合id                                     |
| dnaName    | String   | 是           | 数字资产名称                                                 |
| dnaNumber  | String   | 是           | 数字资产的编号                                               |
| tokenBid   | String   | 是           | 数字资产Bid                                                  |
| dnaDes     | String   | 否           | 数字资产描述说明                                             |
| dnaType    | string   | 是           | 数字资产类型，0-图片、1-视频、2-音频                         |
| url        | String   | 是           | 数字资产图像的url,建议使用350*350的图像,需支持开放访问       |
| displayUrl | String   | 是           | 数字资产缩略图URL，建议尺寸85*85，需支持开放访问             |
| hash       | String   | 是           | 数字资产图片哈希值                                           |
| mintTime   | String   | 是           | 数字资产链上mint交易时间                                     |
| owner      | String   | 是           | 数字资产所有者，指账户地址；数字资产发生相关交易后，平台更新维护owner信息 |
| dnaPrice   | Number   | 是           | 数字资产发行价格                                             |
| extension  | String   | 否           | 扩展字段，用户自定义，长度不超过1024个字符                   |

**响应参数**

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode    | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg     | string   |              | 200-OK<br/>400-accessToken必填、accessToken不正确、accessToken过期、请检查请求参数,请求参数不能为空字符串、tokenBID重复、资产名称不应超过50个字符、集合ID不存在、请输入正确格式的数字资产url、请输入正确格式的数字资产缩略图url<br/>500-服务错误 |

### 7.4数字资产转移认证接口

```http
https://{url}/auth/api/v1/dna/transfer
```

**请求方式**

**POST**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**                  |
| ----------- | -------- | ------------ | ------------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口，通过 |

**请求参数**

| **字段名** | **类型** | **是否必填** | **描述**                            |
| ---------- | -------- | ------------ | ----------------------------------- |
| data       | object[] |              | 数字资产转移列表，转移记录不超过100 |

Data结构如下:

| **字段名** | **类型** | **是否必填** | **描述**                                                |
| ---------- | -------- | ------------ | ------------------------------------------------------- |
| tokenBid   | String   | 是           | 数字资产BID,每个数字资产绑定一个子链bid作为唯一标识。   |
| fromBid    | String   | 是           | 资产转出的用户地址，每个用户绑定一个子链bid作为唯一标识 |
| toBid      | String   | 是           | 资产转入的用户地址                                      |
| txHash     | String   | 是           | 该交易在链上的交易哈希值                                |
| Time       | String   | 是           | 该交易在链上的确认时间                                  |

**响应参数**

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode    | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg     | string   |              | 200-OK<br/>400-accessToken必填、accessToken不正确、accessToken过期、请检查请求参数,请求参数不能为空字符串、txHash重复（校验同一tokenBid，不同资产可重复）、tokenBID不存在<br/>500-服务错误 |

### 7.5数字资产销毁认证接口

```http
https://{url}/auth/api/v1/dna/destroy
```

**请求方式**

**POST**

**Headers**

| **字段名**  | **类型** | **是否必填** | **描述**                  |
| ----------- | -------- | ------------ | ------------------------- |
| accessToken | string   | 是           | 用于B端用户调用接口，通过 |

**请求参数**

| **字段名** | **类型** | **是否必填** | **描述**                    |
| ---------- | -------- | ------------ | --------------------------- |
| data       | object[] |              | 集合列表，销毁记录不超过100 |

Data结构如下:

| **字段名** | **类型** | **是否必填** | **描述**                                              |
| ---------- | -------- | ------------ | ----------------------------------------------------- |
| tokenBid   | String   | 是           | 数字资产BID,每个数字资产绑定一个子链bid作为唯一标识。 |
| fromBid    | String   | 是           | 数字资产持有用户的地址                                |
| txHash     | string   | 是           | 该交易在链上的交易哈希值                              |
| Time       | string   | 是           | 该交易在链上的确认时间                                |

**响应参数**

| **字段名** | **类型** | **是否必填** | **描述**                                                     |
| ---------- | -------- | ------------ | ------------------------------------------------------------ |
| retCode    | number   |              | 返回状态码，取值：200-成功，400-信息错误，500-服务错误       |
| retMsg     | string   |              | 200-OK<br>400-accessToken必填、accessToken不正确、accessToken过期、请检查请求参数,请求参数不能为空字符串、txHash重复（校验同一tokenBid，不同资产可重复）、tokenBID不存在<br/>500-服务错误 |