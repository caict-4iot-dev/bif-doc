# 授权通信数据服务API

## 1. 简介

所谓“授权通信”，即只有经过用户授权才可以通信，未经授权的电话或者短信都将被视作不良信息。星火链网授权通信服务以区块链技术为核心，通过不可逆加密技术存储使用授权及通信凭证，实现企业到网络到终端到用户的端到端语音、短信管控。

通过授权通信数据服务API，可将授权凭证信息上链存储，由于上链交易不是实时进行，可通过接口查询上链状态。同时，主链为每个授权凭证生成凭证BID，后续可通过星火链网统一解析入口，解析该BID详情。

## 2.接入说明

1、本文档用于指导后端开发者对授权通信数据服务的开发。

2、申请应用`api_key`和`api_secret`（联系李瑾（lijin1@caict.ac.cn）获取）。

(注意：`api_key`和`api_secret`相当于用户名和密码，请不要随意泄露)

3、本文档的接口采用 **HTTPS** 加密方式请求。

访问域名：[https://sqtxapi.bitfactory.cn](https://sqtxapi.bitfactory.cn)

## 3.API调用说明

用户通过获取`accessToken`接口获取开发者账户`token`,`token`有效期两小时, 业务接口所有api接口都需要将开发者账户`token`放入请求头部, api具体参数详见接口文档。

## 4.API接口

### 4.1 基础接口

#### 4.1.1 获取accessToken

```json
http请求方式：POST
https://{url}/traf/get/accessToken
{
  "apiKey": "",
  "apiSecret":""
}
```

请求参数说明：

| **字段名** | **类型** | **是否必填** | **描述**       |
| ---------- | :------- | ------------ | -------------- |
| apiKey     | String   | 是           | 开发者账户标识 |
| apiSecret  | String   | 是           | 开发者账户密钥 |

成功的返回JSON数据：

```json
{
    "data": {
       "accessToken":""
    }, 
    "errorCode": 0, 
    "message": "成功"
}
```

响应参数说明：

| **字段名**  | **类型** | **描述**        |
| ----------- | -------- | --------------- |
| accessToken | String   | 开发者账户token |

### 4.2 业务接口

#### 4.2.1 数据链上存储

```json
http请求方式：POST
https://{url}/traf/data/store
{
    "requestNo": "",
    "scene": 1000,
    "data": "{\"mobile\": \"136****1024\",\"appId\": \"did:bid:ef14uPsX7XYLzsU4t2rnRrsK2zfUbFEj\",\"companyBid\": \"did:bid:ef14uPsX7XYLzsU4t2rnRrsK2zfUbFEj\",\"authProtocoHash\": \"da638834453294c3cc51cec148b62838c336bd9f5d11689b183580491bb89286d\",\"authTime\": \"2021-09-26\",\"authDuration\": \"2021-09-26\"}"
}
```

请求参数说明：

| **字段名**           | **类型** | **是否必填** | **描述**                                       |
| -------------------- | :------- | ------------ | ---------------------------------------------- |
| requestNo            | String   | 是           | 请求序号（在开发者APIKey中唯一），推荐使用UUID |
| scene                | int      | 是           | 场景（1000：授权通信数据存储场景）             |
| data                 | String   | 是           | 上传数据（JSON格式字符串）                     |
| data.mobile          | String   | 是           | 加密手机号                                     |
| data.appId           | String   | 是           | 应用bid                                        |
| data.companyBid      | String   | 是           | 企业bid                                        |
| data.authProtocoHash | String   | 是           | 授权协议Hash                                   |
| data.authTime        | String   | 是           | 授权时间                                       |
| data.authDuration    | String   | 是           | 授权过期时间                                   |

成功的返回JSON数据：

```json
{
    "data": {
        "dataBid":"",
        "requestNo":""
    }, 
    "errorCode": 0, 
    "message": "成功"
}
```

响应参数说明：

| **字段名** | **类型** | **描述**                                   |
| ---------- | -------- | ------------------------------------------ |
| dataBid    | String   | 数据链上存储索引BID                        |
| requestNo  | String   | 请求序号（由开发者定义并调用本接口时传入） |

#### 4.2.2 获取数据链上存储状态

```json
http请求方式：POST
https://{url}/traf/data/query/status
{
  "dataBid": "",
  "requestNo":""
}
```

请求参数说明：

| **字段名** | **类型** | **是否必填** | **描述**                                   |
| ---------- | :------- | ------------ | ------------------------------------------ |
| dataBid    | String   | 否           | 数据链上存储索引BID                        |
| requestNo  | String   | 否           | 请求序号（数据存储接口由开发者定义并传入） |

**注意**：`dataBid`、`requestNo`二者不能同时为空。

成功的返回JSON数据：

```json
{
    "data": {
       "status":"",
       "txHash": ""
    }, 
    "errorCode": 0, 
    "message": "成功"
}
```

响应参数说明：

| **字段名** | **类型** | **描述**                                                   |
| ---------- | -------- | ---------------------------------------------------------- |
| status     | String   | 存储状态（0：待处理，1：处理中，2：处理成功，3：处理失败） |
| txHash     | String   | 数据上链交易hash                                           |

#### 4.2.3 获取存储数据详情

```json
http请求方式：POST
https://{url}/traf/data/query/detail
{
  "dataBid": "",
  "requestNo":""
}
```

请求参数说明：

| **字段名** | **类型** | **是否必填** | **描述**                                   |
| ---------- | :------- | ------------ | ------------------------------------------ |
| dataBid    | String   | 否           | 数据链上存储索引BID                        |
| requestNo  | String   | 否           | 请求序号（数据存储接口由开发者定义并传入） |

**注意**：`dataBid`、`requestNo`二者不能同时为空。

成功的返回JSON数据：

```json
{
    "data": {
        "txHash": "",
        "dataBid": "",
        "bidDocument": "\"@context\": [\"https://w3.org/ns/did/v1\"],
    \"authentication\": [\"did:bid:efx1dx9wdRzwy5J68dxhcXN2oaAToPXY#key-1\"],
    \"created\": \"2021-09-26T09:00:21Z\",
    \"extension\": {
      \"attributes\": [{
        \"encrypt\": 0,
        \"format\": \"text\",
        \"value\": \"133****9999\",
        \"key\": \"mobile\",
        \"desc\": \"加密手机号\"
      },{
        \"encrypt\": 0,
        \"format\": \"text\",
        \"value\": \"did:bid:ac01:ef14uPsX7XYLzsU4t2rnRrsK2zfUbFEj\",
        \"key\": \"appId\",
        \"desc\": \"应用id\"
      },{
        \"encrypt\": 0,
        \"format\": \"text\",
        \"value\": \"did:bid:ac01:ef14uPsX7XYLzsU4t2rnRrsK2zfUbFEj\",
        \"key\": \"companyBid\",
        \"desc\": \"企业Bid\"
      },{
        \"encrypt\": 0,
        \"format\": \"text\",
        \"value\": \"da638834453294c3cc51cec148b62838c336bd9f5d11689b183580491bb89286d\",
        \"key\": \"authProtocoHash\",
        \"desc\": \"授权协议hash\"
      },{
        \"encrypt\": 0,
        \"format\": \"text\",
        \"value\": \"2021-09-26\",
        \"key\": \"authTime\",
        \"desc\": \"授权时间\"
      },{
        \"encrypt\": 0,
        \"format\": \"text\",
        \"value\": \"2021-09-26\",
        \"key\": \"authDuration\",
        \"desc\": \"授权过期时间\"
      }],
      \"recovery\": [\"did:bid:efx1dx9wdRzwy5J68dxhcXN2oaAToPXY#key-1\"],
      \"ttl\": 86400,
      \"type\": 102
    },
    \"id\": \"did:bid:efx1dx9wdRzwy5J68dxhcXN2oaAToPXY\",
    \"publicKey\": [{
      \"controller\": \"did:bid:efx1dx9wdRzwy5J68dxhcXN2oaAToPXY\",
      \"id\": \"did:bid:efx1dx9wdRzwy5J68dxhcXN2oaAToPXY#key-1\",
      \"publicKeyHex\": \"b0656629cac2866320b05cc614c2a92c9090d891b7f6d86a9545c715a99254925875cd\",
      \"type\": \"Ed25519\"
    }],
    \"updated\": \"2021-09-26T09:00:21Z\",
    \"version\": \"1.0.0\""
    },
    "errorCode": 0,
    "message": "成功"
}
```

响应参数说明：

| **字段名**  | **类型** | **描述**                 |
| ----------- | -------- | ------------------------ |
| txHash      | JSON     | 数据上链交易hash         |
| dataBid     | String   | 数据链上存储索引BID      |
| bidDocument | String   | 数据链上存储docuemnt文档 |

