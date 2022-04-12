骨干节点接入
=========================

## 前言

​文档目的：指导骨干节点/骨干链接入，包含接入流程、接入内容和开发规范。接入方式**先通过星火·链网超级节点测试网络平台进行测试验证**，接入测试成功后再接入超级节点正式系统。

**测试系统** 超级节点测试网络平台地址：http://test-boss.bitfactory.cn/

**生产系统** 超级节点区块链网络平台地址：https://boss.bitfactory.cn/

## 通用说明

### 名词解释

**API_key** 开发者的身份ID，可用于获取骨干节点的调用凭证（access_token），然后通过接口调用凭证再来访问开放平台API。

**API_secret** 开发者身份ID对应的密钥，配合API_key使用能够获取接口调用凭证，同时为了安全起见这个密钥需要妥善保管。

**accessToken** 所有API接口的调用凭证，通过API_key和API_secret调用相关接口获得，具有时效性，有效时间为2小时， 过期后需要重新获取否则会调用接口失败，因为凭证获取的接口有调用次数限制，所以建议妥善保存并管理。

**AC号** 自治共识域为边界的跨链互通能力（ACSN，Autonomous Consensus System Number），简称共识域号，即AC号，AC号是由四位小写字母和数字组成，代表各区块链在星火·链网中唯一合法身份，是星火·链网体系中区分不同区块链共识区域的代号，用于区块链身份识别及全网寻址功能。

**BID** 区块链上标记某个对象唯一分布式标识。

**publicKey、privateKey** 公钥和私钥是建立在区块链网络上不可缺少的组成部分，链上发起交易都是需要私钥来签名的。私钥可以恢复公钥，但是，仅使用公钥是不可能找到私钥的。

**blob** 星火·链网上交易结构序列化后的十六进制格式，用于执行上链操作。

**backboneNodeBid** 骨干节点BID，成为骨干节点时 可以登录星火链网 业务管理平台查看骨干节点BID。

**gatewayAddress** 网关节点账户bid，骨干节点为下属子链上报信息时，需要使用这个账户发起交易。

**跨链合约** 部署跨链合约后可支持主链积分转移、子链积分转移、数据跨链、智能合约跨链互操作功能。

**网关节点地址** 子链将数据通过链网关账户锚定到国家主链。

**服务商** 是指经有效申请并通过星火市场验证，入驻星火·链网星火市场，并通过星火市场向用户进行在线销售服务的企业。

**应用服务** 是指服务商在星火市场发布的应用类服务，用户购买后可以通过已购服务列表中授权BID后直接访问服务商提供的外部系统或平台。

**开发服务** 是指服务商在星火市场发布的开发类服务，如提供多维度的区块链软件能力、行业解决方案，为企业实现一站式区块链业务赋能。开发服务目前可支持API类和交付类两大分类。

**服务调用剩余时长** 是指用户在星火市场上购买设置按时计费的API类开发服务，在已购服务详情中可以查看该服务的剩余时长。

**服务调用剩余次数** 是指用户在星火市场上购买设置按次计费的API类开发服务，在已购服务详情中可以查看该服务的剩余次数。


## 接入流程

​骨干节点接入主链分为**线上注册申请**和**线下开发**两部分内容，具体流程如下图所示，蓝色标记部分需要骨干节点登录超级节点业务系统进行操作 ：

​![img](../images/main_node_1.png)        

## 接入内容

### 接入内容概述

骨干节点需根据本文档及[《BID协议》](https://bid-resolution-protocol-doc.readthedocs.io/zh_CN/v1.9.4/)要求开发接入主链，将骨干节点及其子链信息同步至主链锚定，实现与主链的互联互通，并且在实际业务中应用BID。为实现以上目标，至少需要接入以下内容：

1. 注册申请：包含企业账号注册、获取数字身份、可信认证申请、骨干节点申请、API调用权限申请。该接入内容，需要登录到超级节点业务系统中进行操作。

2. 底层链锚定：包含链基础信息同步、链状态信息同步、链节点信息同步、链节点运行状态同步、链的区块信息同步、交易信息同步、合约信息同步。

3. 底层链业务接入：链应用服务信息同步

4. BID标识应用于实际业务：

- 标识注册、标识解析。
- 将BID标识应用于当前的业务中。由于不同骨干节点/骨干链上业务不同，需和信通院详细沟通，可能需要对骨干链上现有业务进行改造。

**说明**

- **以上4部分内容全部接入后即对接成功，测试环境对接成功后才可接入生产环境。**



### 注册申请

#### 注册企业账号

第一步：访问星火·链网业务系统 注册**企业账户**。（用户想要接入哪个超级节点，就登录该超级节点系统执行申请操作）


第二步：登录后，进入账户中心 获取数字身份

​![img](../images/main_node_4.png)        

第三步：完成企业可信认证申请，申请完成后，等待所属超级节点审核企业可信认证，审核通过后，才能进行下一步申请骨干节点。

说明：测试期间，授权书等资料不需要上传真实文件。

​![img](../images/main_node_5.png)        
​
完成可信认证后，可查看证书：
​

#### 4.2.2 申请骨干节点

准备工作：使用BID-SDK-JAVA线下生成一个网关账户地址（公钥私钥也要保存好），为下一步申请成为骨干节点时配置接入网关地址时使用（可以生成多个）

第一步：申请骨干节点，登录星火·链平台选择业务管理平台，节点管理--节点申请--申请骨干节点； 申请完成后，等待所属超级节点审核；审核通过后才能进行下一步操作。（准备工作中生成的网关地址写到服务器信息的“数据网关BID列表中”）

说明：

- AC号：可自定义，最终以超级节点审核结果为准（超级节点审核时可修改AC号）
- 解析服务网络地址：子链解析服务网络地址（子链开发bid注册解析服务时用到）
- 链架构类型：如链架构类型中，没有子链的链结构类型，可联系信通院同事进行添加


第二步：导出骨干节点账户（地址、私钥）为后续骨干节点向主链发交易时使用

超级节点审核完成后，即生成骨干节点账户，骨干节点相关业务以骨干节点身份开展。

#### 4.2.3 申请API调用权限

申请成为骨干节点后，需要申请API调用权限才可调用API服务。

第一步：申请骨干节点API_key和API_secret，在业务管理平台-开发者管理模块中进行APIKey申请，

​                 ![img](../images/main_node_12.png)        

第二步：申请完成后，等待所属超级节点审核，审核完成后 可以在 APIKey管理里面查询开发者信息。

​                 ![img](../images/main_node_13.png)

### 4.3 底层链锚定

通过该接口由骨干链或子链底层数据锚定至主链，确保数据不可篡改。

包含链基础信息同步、链状态信息同步、链节点信息同步、链的区块信息同步、合约信息同步、交易信息同步。

#### 4.3.1 链基础信息同步

请求参数：

| **字段名**         |    **类型** | **是否必填** | **描述**                                                     |
| :----------------- | ----------: | :----------- | :----------------------------------------------------------- |
| ACSN               |   String(4) | 是           | 子链AC号                                                     |
| name               | String(128) | 是           | 链名称                                                       |
| chainType          |      String | 是           | 链架构类型，10000:星火·链网、10001:Fabric、10002:Ethereum 10003:BubiChain、10004:Quorum，10005：Xuperchain,10006:cita , 10007：FISCO |
| time               |        Long | 是           | 链申请时间/建设时间  （Unix时间戳 毫秒）                     |
| backBoneNodeBid    |  String(64) | 是           | 申请子链的骨干节点BID，bid不带ACSN                           |
| industryType       |   String(1) | 是           | 所属行业类型值，**见行业类型10**                             |
| trafficWarning     |        Long | 是           | 节点网络流量告警值，单位字节                                 |
| trafficOverload    |        Long | 是           | 节点网络流量过载值，单位字节                                 |
| consensus          | String(128) | 是           | 区块链共识机制, 如 POW 或 DPOS 或 DPOS + PBFT （自定义填写） |
| genesisBid         | String(128) | 否           | 创世账户地址                                                 |
| genesisInitValue   |  String(30) | 否           | 创世账户初始化TOKEN数                                        |
| baseReserve        |  String(30) | 否           | 账户最小TOKEN保留数                                          |
| gasPrice           |  String(30) | 否           | 最小TOKEN单价                                                |
| firstReward        |  String(30) | 否           | 首次出块奖励数                                               |
| introduce          |      String | 否           | 区块链介绍                                                   |
| version            |  String(16) | 是           | 区块链版本号                                                 |
| ledgerDB           | String(128) | 是           | 支持的账本数据库类型名称（全小写，英文逗号间隔）             |
| topTps             |     Integer | 是           | 理论tps峰值                                                  |
| organization       | String(256) | 是           | 链的运营机构名称                                             |
| explorerUrl        | String(256) | 否           | 区块链浏览器地址，如：https://explorer.bif.cn               |
| defaultDbType      |  String(20) | 是           | 链上默认账本数据库类型，（规则：全小写，英文逗号间隔，比如leveldb） |
| location           |      Object | 是           | 链的运营机构地理位置                                         |
| location.latitude  |  String(16) | 是           | 地理位置纬度                                                 |
| location.longitude |  String(16) | 是           | 地理位置经度                                                 |
| location.province  |  String(32) | 是           | 省、直辖市、自治区，比如：陕西省                             |
| location.city      |  String(32) | 是           | 城市，比如：西安市                                           |
| location.district  |  String(32) | 是           | 区、市、县，比如：雁塔区                                     |

返回数据：

| **字段名** | **类型** | **描述** |
| :--------- | :------- | :------- |
| errorCode  | Integer  | 错误码   |
| message    | String   | 错误描述 |

示例：

（1）请求示例：

```
http请求方式：POST
https://{url}/v1/chain/info/syn
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcGlLZXkiOiJDcHB0NHRuMFlFZkIyMHJXIiwiaXNzIjoiQklGLUNIQUlOIiwiZXhwIjoxNjIxNTk0NDQ4LCJiaWQiOiJkaWQ6YmlkOmVmMjhwTTlNRzNUR1hHeVdBVzRKcFdDRnNKRGQ1TUJuYyJ9.MxWdV-mwCScUq8QwmTXTaxKli8jvXq1sNVvAYQWWsSo",
   "params": {
    "ACSN": "acc1",
    "name": "营口行业链",
    "chainType" : "10000",
    "time" : 1593338217000,
    "backBoneNodeBid" : "did:bid:hHTsFXTTqQfVH1oThGEKf6iwCK2c31Bes",
    "industryType" : "A",
    "trafficWarning" : 4096,
    "trafficOverload" : 8192,
    "consensus" : "DPOS+PBFT",
    "genesisBid": "did:bid:hHTsFXTTqQfVH1oThGEKf6iwCK2c31Bes",
    "genesisInitValue": 100000000,
    "baseReserve": 10000000,
    "gasPrice": 1000,
    "firstReward": 100000000,
    "introduce": "",
    "version": "1",
    "ledgerDB": "rocksdb,tidb,mysql",
    "topTps": 1000,
    "organization": "信通院",
    "explorerUrl": "https://explore.bif.com",
    "defaultDbType": "",
    "location": {
        "latitude": "29.5",
        "longitude": "113.4",
        "province": "辽宁省",
        "city": "营口市",
        "district": "渝中区"
    }
  }
}

```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```
{
    "errorCode": 0,
    "message": "成功"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```
{
    "errorCode": 940000,
    "message": "系统内部错误"
}
```

#### 链状态信息同步

骨干节点将子链的动态信息同步到主链，需要两步操作：4.3.1获取链动态信息同步交易blob；4.3.2链动态信息同步提交。要求每隔5分钟同步一次数据。

##### 获取子链状态信息同步blob

接口说明：

子链状态信息同步时需要将信息同步到链上

请求参数：

| **字段名**          |   **类型** | **是否必填** | **描述**                                                     |
| :------------------ | ---------: | :----------- | :----------------------------------------------------------- |
| ACSN                |  String(4) | 是           | 链AC号                                                       |
| gatewayAddress      | String(64) | 是           | 数据网关地址（在平台链详情中查看该地址），如：**did:bid:efb8Ehu9SGVCTm2BbvpPiQjzNWo4LQAA** |
| blockHeight         |       Long | 是           | 区块高度                                                     |
| validationNodeCount |       Long | 是           | 参与共识的节点数量                                           |
| totalNodeCount      |       Long | 是           | 节点总数量                                                   |
| systemContractCount |       Long | 是           | 系统合约数量                                                 |
| normalContractCount |       Long | 是           | 普通合约数量                                                 |
| serviceNodeCount    |       Long | 是           | 业务节点个数                                                 |
| txNumber            |       Long | 是           | 总交易数                                                     |
| accountCount        |       Long | 是           | 总账户数                                                     |
| tps                 |       Long | 是           | 平均tps                                                      |
| extra               |     String | 否           | 额外字段                                                     |

返回数据：

| **字段名** | **类型** | **描述** |
| :--------- | :------- | :------- |
| blobId     | String   | blodId   |
| txHash     | String   | 交易hash |
| blob       | String   | blod串   |

示例：

（1）请求示例：

```
http请求方式：POST
https://{url}/v1/chain/status/syn/blob
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcGlLZXkiOiJDcHB0NHRuMFlFZkIyMHJXIiwiaXNzIjoiQklGLUNIQUlOIiwiZXhwIjoxNjIxNTcxMjg0LCJiaWQiOiJkaWQ6YmlkOmVmMjhwTTlNRzNUR1hHeVdBVzRKcFdDRnNKRGQ1TUJuYyJ9.9tTPWasYgCs1yC3qYJYSjCGvd9Syl1mr6G2EVrKeq2E",
  "params": {
    "ACSN": "by01",
    "gatewayAddress": "did:bid:efb8Ehu9SGVCTm2BbvpPiQjzNWo4LQAA",
    "blockHeight": 50003,
    "txNumber": 200000,
    "tps": 101,
    "validationNodeCount":0,
    "totalNodeCount": 0,
    "systemContractCount": 0,
    "normalContractCount": 0,
    "serviceNodeCount": 0,
    "accountCount": 0,
  }
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```
{
  "errorCode": 0,
  "message": "操作成功",
  "data": {
    "blobId": "15",
    "txHash": "d60c15bacbb7f98f00921d5ad17d49fafe0c65ea706d5d4ced25e490ac35e9e0",
    "blob": "0A286469643A6269643A65663477776B727A53564650545A4A627257433439446B416554535169377241101E228304080712286469643A6269643A656662384568753953475643546D32426276705069516A7A4E576F344C51414152D4030A286469643A6269643A6566427070397753676564315A5A72437566426D36374A4C55635255396375321AA7037B226D6574686F64223A227375626D6974426C6F636B486561646572222C22706172616D73223A7B22626C6F636B486561646572223A7B226163636F756E745F747265655F68617368223A22222C22636C6F73655F74696D65223A2231353933333338343030303032303030222C22636F6E73656E7375735F76616C75655F68617368223A22222C22666565735F68617368223A22222C2268617368223A2235323134303538363966626533633132396237383434383232333566616365633435656438653432313666633834653962623665336136386661653430636232222C2270726576696F75735F68617368223A2231323334363966626533633132396237383434383232333566616365633435656438653233313435363537646161313233343131326136386661653430636232222C22736571223A223938222C2274785F636F756E74223A223132222C2276616C696461746F72735F68617368223A22696E7465726E616C436861696E496432222C2276657273696F6E223A22227D2C22636861696E436F6465223A2262793031222C2264796E616D6963496E666F223A7B7D7D7D3080EAADE907"
  }
}
```

b. 接口调用失败，则返回JSON数据示例为：

```
{
    "errorCode": 940000,
    "message": "系统内部错误"
}
```

##### 子链的状态信息提交（上链）

接口说明：

对blob数据进行签名（参考 签名算法 章节），并提交至主链执行上链操作，用于链的状态信息同步提交至主链并上链备案。

请求参数：

| **字段名**           |    **类型** | **是否必填** | **描述**                           |
| :------------------- | ----------: | :----------- | :--------------------------------- |
| blobId               |  String(20) | 是           | Blob序号，通过获取交易Blob接口获取 |
| signerList           |        List | 是           | 签名者列表（注意：需要数据网关签名） |
| signerList.signBlob  | String(128) | 是           | 签名串（数据网关签名）               |
| signerList.publicKey | String(128) | 是           | 签名者公钥（数据网关公钥）           |

返回数据：

| **字段名** | **类型** | **描述**     |
| :--------- | :------- | :----------- |
| txHash     | String   | 链上交易hash |

示例：

（1）请求示例：

```
http请求方式：POST
https://{url}/v1/chain/status/syn/submit
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcGlLZXkiOiJDcHB0NHRuMFlFZkIyMHJXIiwiaXNzIjoiQklGLUNIQUlOIiwiZXhwIjoxNjE5MzQyNDIyLCJiaWQiOiJkaWQ6YmlkOmVmMjhwTTlNRzNUR1hHeVdBVzRKcFdDRnNKRGQ1TUJuYyJ9.3gcQQBqvqtZH1q-TfUiGne68R1TnBcvLAA6nIJ8qDGU",
  "params": {
    "blobId": "1",
    "signerList": [{
      "signBlob": "BDE955FF0A0F52A39E95815962836D13172D6EF92C55A72A97ECCF2CE882E2E2EAC73FA1A624D73C959E18126B4A35947375621D819F539DDC0692EEF0F4D702",
      "publicKey": "b06566086febd16adf6553cc9c000dba5f9f410d34f8541392303561dddc045b15ef4c"
    }]
  }
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```
{
    "errorCode": "0",
    "message": "操作成功",
      "data": {
      "txHash": "083b797ea00204d2c17a9e1bd77cab11385f475da756f76a96b922e4c7b8f7c7"
    }
}
```

b. 接口调用失败，则返回JSON数据示例为：

```
{
    "errorCode": 940000,
    "message": "系统内部错误"
}
```

#### 链节点信息同步

骨干节点将链的信息同步到主链，需要两步操作：4.4.1获取链节点信息同步交易blob；4.4.2链节点信息同步提交。节点有新增和修改时需要同步至主链。

##### 获取链节点信息同步blob

接口说明：

节点信息同步时需要将信息同步到链上

请求参数：

| **字段名**                 | **类型**    | 是否必填 | **描述**                                                     |
| :------------------------- | :---------- | :------- | ------------------------------------------------------------ |
| ACSN                       | String(4)   | 是       | AC号                                                         |
| gatewayAddress             | String(64)  | 是       | 数据网关地址（在平台链详情中查看该地址），如：**did:bid:efb8Ehu9SGVCTm2BbvpPiQjzNWo4LQAA** |
| nodeList                   | List        | 是       | 节点对象集合                                                 |
| nodeList.nodeAddress       | String(128) | 是       | 节点地址（BID格式，即对子链原节点地址映射为BID格式），例如壹诺区块链华东节点地址：adxSdh5znTeNgjLNoX1e4CuHJoC9hDUbgMrtf，需要映射一个新的BID格式: did:bid:ynjr:ef6bRF4FDPzjvatNmFu6YAvegBtcv86r |
| nodeList.name              | String(128) | 是       | 节点名称                                                     |
| nodeList.createTime        | Long        | 是       | 节点申请时间 （Unix时间戳 毫秒）                             |
| nodeList.bindNodeBid       | String(64)  | 是       | 所属骨干节点bid                                              |
| nodeList.owner             | String(64)  | 是       | 该节点归属的企业bid                                          |
| nodeList.location          | Object      | 是       | 节点地理位置                                                 |
| nodeList.location.district | String(32)  | 是       | 区域编码(比如：810008,通过4.13接口获取区域信息 需要获取到县级的编号 ) |
| nodeList.type              | Integer     | 是       | 节点类型：0 业务节点（目前仅支持 业务节点,后续扩展其他类型） |
| nodeList.p2pAddress        | String(64)  | 是       | 节点间p2p通信地址，如：172.10.3.1:49900                      |
| nodeList.serverType        | Integer     | 是       | 服务器类型: 0自建服务器，1云服务                             |
| nodeList.hostIp            | String      | 是       | 节点公网IP，没有公网IP填内网IP                               |
| nodeList.cloudName         | Integer     | 是       | 云类型，0非公有云，1阿里云，2百度云、3金山云、4华为云、5亚马逊云、6微软云、7腾讯云、8京东云、9物理机、100其他云 |
| nodeList.extra             | String      | 否       | 扩展字段                                                     |
| nodeList.extra.nodeType    | Integer     | 否       | 节点类型：0 共识节点  1 观察者节点，当子链架构为cita、fiscobcos时必填 |
| nodeList.extra.group       | String      | 否       | 群组id，当子链架构为fiscobcos、fabric时必填                  |

返回数据：

| **字段名** | **类型** | **描述** |
| :--------- | :------- | :------- |
| blobId     | String   | blodId   |
| txHash     | String   | 交易hash |
| blob       | String   | blod串   |

示例：

（1）请求示例：

```
http请求方式：POST
https://{url}/v1/chain/nodeInfo/syn/blob
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcGlLZXkiOiJDcHB0NHRuMFlFZkIyMHJXIiwiaXNzIjoiQklGLUNIQUlOIiwiZXhwIjoxNjIxNTcxMjg0LCJiaWQiOiJkaWQ6YmlkOmVmMjhwTTlNRzNUR1hHeVdBVzRKcFdDRnNKRGQ1TUJuYyJ9.9tTPWasYgCs1yC3qYJYSjCGvd9Syl1mr6G2EVrKeq2E",
  "params": {
    "ACSN": "ynjr",
    "gatewayAddress": "did:bid:efb8Ehu9SGVCTm2BbvpPiQjzNWo4LQAA",
    "nodeList": [{
      "nodeAddress": "did:bid:ynjr:ef6bRF4FDPzjvatNmFu6YAvegBtcv86r",
      "name": "业务节点1",
      "createTime": 1593338217000,
      "bindNodeBid": "did:bid:by01:WWBVgCnREaLjegUvkpeiY8BaiAojvcv1b",
      "owner": "did:bid:zg01:WWBVgCnREaLjegUvkpeiY8BaiAojvcv11",
      "location": {
        "district": "810008"
      },
      "type": 1,
      "p2pAddress": "127.0.0.1:18001",
      "serverType": 0,
      "hostIp": "192.168.1.12",
      "cloudName": 1
    }]
  }
}

```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```
{
  "errorCode": 0,
  "message": "操作成功",
  "data": {
    "blobId": "15",
    "txHash": "d60c15bacbb7f98f00921d5ad17d49fafe0c65ea706d5d4ced25e490ac35e9e0",
    "blob": "0A2864696..."
  }
}
```

b. 接口调用失败，则返回JSON数据示例为：

```
{
    "errorCode": 940000,
    "message": "系统内部错误"
}
```

##### 子链节点信息提交（上链）

接口说明：

对blob数据进行签名（参考 签名算法 章节），并提交至主链执行上链操作，用于节点信息同步提交至主链并上链备案。

请求参数：

| **字段名**           |    **类型** | **是否必填** | **描述**                           |
| :------------------- | ----------: | :----------- | :--------------------------------- |
| blobId               |  String(20) | 是           | Blob序号，通过获取交易Blob接口获取 |
| signerList           |        List | 是           | 签名者列表（注意：需要数据网关签名） |
| signerList.signBlob  | String(128) | 是           | 签名串（数据网关签名）               |
| signerList.publicKey | String(128) | 是           | 签名者公钥（数据网关公钥）           |

返回数据：

| **字段名** | **类型** | **描述**     |
| :--------- | :------- | :----------- |
| txHash     | String   | 链上交易hash |

示例：

（1）请求示例：

```
http请求方式：POST
https://{url}/v1/chain/nodeInfo/syn/submit
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9....3gcQQBqvqtZH1q-TfUiGne68R1TnBcvLAA6nIJ8qDGU",
  "params": {
    "blobId": "1",
    "signerList": [{
      "signBlob": "BDE955FF0A0...",
      "publicKey": "b06566086febd16adf6553cc9c000dba5f9f410d34f8541392303561dddc045b15ef4c"
    }]
  }
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```
{
    "errorCode": "0",
    "message": "操作成功",
      "data": {
      "txHash": "083b797ea00204d2c17a9e1bd77cab11385f475da756f76a96b922e4c7b8f7c7"
    }
}
```

b. 接口调用失败，则返回JSON数据示例为：

```
{
    "errorCode": 940000,
    "message": "系统内部错误"
}
```

#### 链节点运行状态同步

接口说明：

骨干节点将链下节点运行状态到主链。（每隔5分钟同步一次）

请求参数：

| 字段名                                   | 类型        | 是否必填 | 描述                                                         |
| :--------------------------------------- | :---------- | :------- | ------------------------------------------------------------ |
| ASCN                                     | String(4)   | 是       | AC号                                                         |
| nodeRunningList                          | List        | 是       | 运行状态信息对象                                             |
| nodeRunningList.nodeAddress              | String(64)  | 是       | 节点地址（BID格式，即对子链原节点地址映射为BID格式），例如壹诺区块链华东节点地址：adxSdh5znTeNgjLNoX1e4CuHJoC9hDUbgMrtf，需要映射一个新的BID格式: did:bid:ynjr:ef6bRF4FDPzjvatNmFu6YAvegBtcv86r |
| nodeRunningList.status                   | Integer     | 是       | 节点运行状况，1：正常， 2：故障                              |
| nodeRunningList.delay                    | Long        | 是       | 节点响应时延, 单位毫秒                                       |
| nodeRunningList.upTraffic                | Long        | 是       | 上行流量, 单位字节                                           |
| nodeRunningList.downTraffic              | Long        | 是       | 下行流量, 单位字节                                           |
| nodeRunningList.latestBlockHeight        | Long        | 是       | 最新区块高度                                                 |
| nodeRunningList.latestBlockHash          | String(128) | 是       | 最新区块哈希                                                 |
| nodeRunningList.latestTxNum              | Long        | 是       | 最新交易总量                                                 |
| nodeRunningList.latestAccountNum         | Long        | 是       | 最新账户总数                                                 |
| nodeRunningList.unblockedTxNum           | Long        | 是       | 实时未打包交易数                                             |
| nodeRunningList.cpuUsage                 | Integer     | 是       | 节点处理器使用率，为百分数整数，如78%请填写78                |
| nodeRunningList.memoryUsage              | Integer     | 是       | 节点内存使用率，为百分数整数，如78%请填写78                  |
| nodeRunningList.diskUsage                | Integer     | 是       | 节点磁盘使用率，为百分数整数，如78%请填写78                  |
| nodeRunningList.memoryUsed               | Long        | 是       | 节点内存占用，单位字节，比如：占用3G，请填写 3221225472      |
| nodeRunningList.diskUsed                 | Long        | 是       | 节点磁盘占用总大小，单位字节，比如：占用3G，请填写3221225472 |
| nodeRunningList.ledgerDBUsed             | Long        | 是       | 节点的账本数据库磁盘占用大小，单位字节，比如：占用3G，请填写 3221225472 |
| nodeRunningList.accountDBUsed            | Long        | 是       | 节点的账户数据库磁盘占用大小，单位字节，比如：占用3G，请填写 3221225472 |
| nodeRunningList.kvDBUsed                 | Long        | 是       | 节点的kv数据库磁盘占用大小，单位字节，比如：占用3G，请填写 3221225472 |
| nodeRunningList.loadavg                  | Long        | 是       | 一分钟内的系统平均负载值，由于原始值为保留2位小数的浮点值，这里扩大100提供整数,如，原始值是20.88 请填写 2088 |
| nodeRunningList.diskRead                 | Long        | 是       | 磁盘实时读取速度，单位字节每秒，如：3M/s 请填写 3145728      |
| nodeRunningList.diskWrite                | Long        | 是       | 磁盘实时写入速度，单位字节每秒，如：3M/s 请填写 3145728      |
| nodeRunningList.tcpCount                 | Integer     | 是       | tcp链接总数                                                  |
| nodeRunningList.time                     | Long        | 是       | 节点状态上报的时间戳，目前节点每分钟上报一次信息             |
| nodeRunningList.extra                    | String      | 否       | 额外数据，（数据格式JSON字符串）                             |
| nodeRunningList.extra.group              | String      | 否       | 群组，当子链架构为xuperchain时必填                           |
| nodeRunningList.nodeFaultList            | List        | 否       | 节点故障数据，节点运行状况发生变化时必填，如正常状态更新为故障状态，需要提供故障产生记录，如故障状态更新为正常状态，需要提供故障恢复记录，列表为同步时间间隔内的增量记录 |
| nodeRunningList.nodeFaultList.id         | String(32)  | 是       | 上报数据索引号（子链上唯一，建议用UUID再进行MD5运算生成的字符串） |
| nodeRunningList.nodeFaultList.time       | Long        | 是       | 故障发生时间(Unix时间戳 毫秒）                               |
| nodeRunningList.nodeFaultList.type       | Integer     | 是       | 标示产生或者恢复日志，1：产生， 2：恢复                      |
| nodeRunningList.nodeFaultList.faultType  | Integer     | 是       | 故障类型，1：区块停止产生， 2：节点已宕机                    |
| nodeRunningList.nodeFaultList.faultLevel | Integer     | 是       | 故障等级，1：严重 2：一般 3：轻微，                          |

返回数据：

| **字段名** | **类型** | **描述** |
| :--------- | :------- | :------- |
| errorCode  | Integer  | 错误码   |
| message    | String   | 错误描述 |

示例：

（1）请求示例：

```
http请求方式：POST
https://{url}/v1/chain/nodeRunningStatus/syn
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcGlLZXkiOiJDcHB0NHRuMFlFZkIyMHJXIiwiaXNzIjoiQklGLUNIQUlOIiwiZXhwIjoxNjIxNTEzODE4LCJiaWQiOiJkaWQ6YmlkOmVmMjhwTTlNRzNUR1hHeVdBVzRKcFdDRnNKRGQ1TUJuYyJ9.kqeuSumhvdHLnrvw0WkWxrY3Cy6bThVKBmv7h2-a1po",
  "params": {
    "ASCN": "ynjr",
    "nodeRunningList": [{
      "nodeAddress": "did:bid:ynjr:ef6bRF4FDPzjvatNmFu6YAvegBtcv86r",
      "status": 1,
      "delay": 300,
      "upTraffic": 10000,
      "downTraffic": 1000,
      "latestBlockHeight": 1000,
      "latestBlockHash": "71a4abdc812bb6d94c56e3a2a849250747a76dbab5559f6fc89338876d4b879f",
      "latestTxNum": 1000,
      "latestAccountNum": 1000,
      "unblockedTxNum": 1000,
      "cpuUsage": 10,
      "memoryUsage": 30,
      "diskUsage": 5,
      "memoryUsed": 1048576,
      "diskUsed": 104857600,
      "ledgerDBUsed": 1024,
      "accountDBUsed": 100,
      "kvDBUsed": 1024,
      "loadavg": 70,
      "diskRead": 1024,
      "diskWrite": 1024,
      "tcpCount": 10,
      "time": 1593338217000,
      "extra": "{}",
      "nodeFaultList": [{
            "id": "c4ca4238a0b923820dcc509a6f75849b",
            "time": 1593338217000,
            "type": 2,
            "faultType": 1,
            "faultLevel": 2
        }]
    }]
  }
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```
{
    "errorCode": "0",
    "message": "操作成功"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```
{
    "errorCode": 940000,
    "message": "系统内部错误"
}
```

#### 链的区块信息同步

骨干节点将链的区块信息同步到主链锚定，需要两步操作：4.6.1获取链的区块信息同步blob ；4.6.2链的区块信息提交（上链）。（要求每隔5分钟同步一次数据。）

##### 获取链的区块信息同步blob

接口说明：

获取链的区块信息同步blob

请求参数：

| **字段名**                  |    **类型** | 是否必填 | **描述**                                                     |
| :-------------------------- | ----------: | :------- | ------------------------------------------------------------ |
| ACSN                        |   String(4) | 是       | AC号                                                         |
| gatewayAddress              |  String(64) | 是       | 数据网关地址（在平台链详情中查看该地址），如：**did:bid:efb8Ehu9SGVCTm2BbvpPiQjzNWo4LQAA** |
| blockList                   |        List | 是       | 区块头信息列表                                               |
| blockList.height            |        Long | 是       | 区块高度                                                     |
| blockList.nodeAddress       |  String(64) | 是       | 出块节点地址（BID格式，即对子链原节点地址映射为BID格式），例如壹诺区块链华东节点地址：adxSdh5znTeNgjLNoX1e4CuHJoC9hDUbgMrtf，需要映射一个新的BID格式: did:bid:ynjr:ef6bRF4FDPzjvatNmFu6YAvegBtcv86r |
| blockList.nodeName          | String(128) | 是       | 出块节点名称                                                 |
| blockList.txNum             |        Long | 是       | 区块交易数                                                   |
| blockList.preBlockHash      |  String(64) | 否       | 上一个区块hash                                               |
| blockList.blockHash         |  String(64) | 是       | 区块hash                                                     |
| blockList.time              |        Long | 是       | 区块生成时间(Unix时间戳 毫秒)                                |
| blockList.size              |        Long | 是       | 区块大小，单位字节                                           |
| blockList.internalChainId   | String(128) | 否       | 标记链内子链id，用于兼容channel字段(Fabric链)、chainID字段(XuperChain链)、grpId字段(FISCO BCOS链)等，需要全局唯一且不可修改，默认为空字符串 |
| blockList.extra             |      Object | 否       | 扩展字段                                                     |
| blockList.extra.channelName |      String | 否       | 通道名称，当子链架构为fabric时必填                           |
| blockList.extra.chainName   |      String | 否       | 平行链名称，当子链架构为xuperchain时必填                     |

返回数据：

| **字段名** | **类型** | **描述**     |
| :--------- | :------- | :----------- |
| blobId     | String   | blodId       |
| txHash     | String   | 链上交易hash |
| blod       | String   | blod串       |

示例：

（1）请求示例：

```
http请求方式：POST
https://{url}/v1/chain/block/syn/blob

{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...9tTPWasYgCs1yC3qYJYSjCGvd9Syl1mr6G2EVrKeq2E",
  "params": {
    "ACSN": "ynjr",
    "gatewayAddress": "did:bid:efb8Ehu9SGVCTm2BbvpPiQjzNWo4LQAA",
    "blockList": [{
      "height": 98,
      "nodeAddress": "did:bid:ynjr:ef6bRF4FDPzjvatNmFu6YAvegBtcv86r",
      "nodeName": "节点2",
      "txNum": 12,
      "preBlockHash": "123469fbe3c129b784482235facec45ed8e23145657daa1234112a68fae40cb2",
      "blockHash": "521405869fbe3c129b784482235facec45ed8e4216fc84e9bb6e3a68fae40cb2",
      "time": 1593338400002,
      "size": 1282,
      "internalChainId":"internalChainId2",
      "extra":"extra2"
    }]
  }
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```
{
  "errorCode": 0,
  "message": "操作成功",
  "data": {
    "blobId": "15",
    "txHash": "d60c15bacbb7f98f00921d5ad17d49fafe0c65ea706d5d4ced25e490ac35e9e0",
    "blob": "0A286469643A626..."
  }
}
```

b. 接口调用失败，则返回JSON数据示例为：

```
{
    "errorCode": 940000,
    "message": "系统内部错误"
}
```

##### 链的区块信息提交（上链）

接口说明：

对blob数据进行签名（参考 签名算法 章节），并提交至主链执行上链操作，用于子链的区块信息提交至主链并上链存储

请求参数：

| **字段名**           |    **类型** | **是否必填** | **描述**                           |
| :------------------- | ----------: | :----------- | :--------------------------------- |
| blobId               |  String(20) | 是           | blobId(4.6.1返回blobId)            |
| signerList           |        List | 是           | 签名者列表（注意：需要数据网关签名） |
| signerList.signBlob  | String(128) | 是           | 签名串（数据网关签名）               |
| signerList.publicKey | String(128) | 是           | 签名者公钥（数据网关公钥）           |

返回数据：

| **字段名** | **类型** | **描述**     |
| :--------- | :------- | :----------- |
| txHash     | String   | 链上交易hash |

示例：

（1）请求示例：

```
http请求方式：POST
https://{url}/v1/chain/block/syn/submit
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcGlLZXkiOiJDcHB0NHRuMFlFZkIyMHJXIiwiaXNzIjoiQklGLUNIQUlOIiwiZXhwIjoxNjE5MzQyNDIyLCJiaWQiOiJkaWQ6YmlkOmVmMjhwTTlNRzNUR1hHeVdBVzRKcFdDRnNKRGQ1TUJuYyJ9.3gcQQBqvqtZH1q-TfUiGne68R1TnBcvLAA6nIJ8qDGU",
  "params": {
    "blobId": "3",
    "signerList": [{
      "signBlob": "4D47D46AA467C8DF8FD1D60374D9D2378AC536612C3B84E1AC9BA4EA55E10810482EC634EADED63A389F82573AB1E055698189F7497DF23C5E32CF26A7D8270F",
      "publicKey": "b06566086febd16adf6553cc9c000dba5f9f410d34f8541392303561dddc045b15ef4c"
    }]
  }
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```
{
    "errorCode": "0",
    "message": "操作成功",
      "data": {
      "txHash": "083b797ea00204d2c17a9e1bd77cab11385f475da756f76a96b922e4c7b8f7c7"
    }
}
```

b. 接口调用失败，则返回JSON数据示例为：

```
{
    "errorCode": 940000,
    "message": "系统内部错误"
}
```

#### 交易信息同步

接口说明：

用于将子链的交易上报到主链（要求每隔5分钟同步一次，将5分钟内的交易都同步上来）

请求参数：

| **字段名**             |      **类型** | **是否必填** | **描述**                                                     |
| :--------------------- | ------------: | :----------- | :----------------------------------------------------------- |
| ACSN                   |     String(4) | 是           | AC号                                                         |
| txList                 |          List | 是           | 交易列表                                                     |
| txList.hash            |    String(64) | 是           | 交易hash                                                     |
| txList.content         |        String | 是           | 交易内容 JSON字符串 或者交易内容hash                         |
| txList.time            |          Long | 是           | 交易时间（Unix时间戳 毫秒）                                  |
| txList.height          |          Long | 是           | 交易高度                                                     |
| txList.status          |     String(2) | 是           | 交易状态，0成功，1失败                                       |
| txList.txSign          | String(65535) | 是           | 交易签名                                                     |
| txList.contractBid     |   String(128) | 否           | 合约地址，合约调用交易为调用的合约地址，非合约调用交易留空   |
| txList.size            |          Long | 是           | 交易大小，单位字节                                           |
| txList.internalChainId |   String(128) | 否           | 链内子链id，默认留空。如Fabric链填写channel，XuperChain链填写chainID，FISCO链填写grpId |
| txList.extra           |        String | 否           | 额外数据                                                     |

返回数据：

| **字段名** | **类型** | **描述** |
| :--------- | :------- | :------- |
| errorCode  | Integer  | 错误码   |
| message    | String   | 错误描述 |

示例：

（1）请求示例：

```
http请求方式：POST
https://{url}/v1/chain/tx/syn

{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcGlLZXkiOiJDcHB0NHRuMFlFZkIyMHJXIiwiaXNzIjoiQklGLUNIQUlOIiwiZXhwIjoxNjIxNTEzODE4LCJiaWQiOiJkaWQ6YmlkOmVmMjhwTTlNRzNUR1hHeVdBVzRKcFdDRnNKRGQ1TUJuYyJ9.kqeuSumhvdHLnrvw0WkWxrY3Cy6bThVKBmv7h2-a1po",
  "params": {
    "ACSN":"by01",
    "txList": [{
      "hash": "71a4abdc812bb6d94c56e3a2a849250747a76dbab5559f6fc89338876d4b879f",
      "content": "a6f9f1e8a18674ac915932e1d700b12b676d22b542f952d0d0f96517f9f5f806",
      "time": 1593338217000,
      "height": 10,
      "status":"0",
      "txSign":"{sign:1234}",
      "contractBid":"0",
      "size":100,
      "internalChainId": "",
      "extra": "123"
    }]
  }
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```
{
    "errorCode": "0",
    "message": "操作成功"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```
{
    "errorCode": 940000,
    "message": "系统内部错误"
}
```

#### 合约信息同步

骨干节点将合约信息同步到主链，便于备案审查。需要两步操作：4.8.1获取合约信息同步blob ；4.8.2合约信息同步提交（上链）。要求每隔5分钟同步一次数据。

##### 获取合约信息同步blob

接口说明：

获取合约信息同步blob。

请求参数：

| **字段名**                             |    **类型** | 是否必填 | **描述**                                                     |
| :------------------------------------- | ----------: | :------- | ------------------------------------------------------------ |
| ACSN                                   |   String(4) | 是       | 链AC号                                                       |
| gatewayAddress                         |  String(64) | 是       | 数据网关地址（在平台链详情中查看该地址），如：**did:bid:efb8Ehu9SGVCTm2BbvpPiQjzNWo4LQAA** |
| smartContractList                      |        List | 是       | 合约列表                                                     |
| smartContractList.ownerAddress         |  String(64) | 是       | 合约拥有人BID（BID格式）                                     |
| smartContractLis.contractAddress       |  String(64) | 是       | 合约地址（BID格式，即对子链原合约地址映射为BID格式），例如原合约地址：adxSBrVVtaWZVuGxGGPZCmyna7C6dKo3WVXd4，需要映射一个新的BID格式: did:bid:ynjr:did:bid:efv7DynieC5sF1UoKAthKTfUCkuzaBfR |
| smartContractList.time                 |        Long | 是       | 合约创建时间（Unix时间戳 毫秒）                              |
| smartContractList.name                 | String(128) | 否       | 合约名称                                                     |
| smartContractList.contractType         |     Integer | 是       | 合约类型，0 :普通合约， 1：主子链管理系统合约， 2：DPOS系统合约 3：部署系统合约 4：认证系统合约 5：隐私保护系统合约 6：跨链系统合约 7：BID注册合约 |
| smartContractList.industryType         |   String(2) | 是       | 行业类型，参考 10证件及行业类型                              |
| smartContractList.payload              |    String() | 是       | 合约代码                                                     |
| smartContractList.vm                   |  String(16) | 是       | 合约引擎                                                     |
| smartContractList.internalChainId      | String(128) | 否       | 标记链内子链id，如Fabric链填写channel，XuperChain链填写chainID，FISCO链填写grpId等，需要全局唯一且不可修改，默认为空字符串 |
| smartContractList.version              |  String(16) | 是       | 合约版本                                                     |
| smartContractList.extra                |      String | 否       | 扩展字段,json字符串                                          |
| smartContractList.extra.identification |      String | 否       | 链码标识，当子链架构为fabric时必填                           |
| smartContractList.extra.nodeCnt        |        Long | 否       | 安装节点数，当子链架构为fabric时必填                         |
| smartContractList.extra.channelCnt     |        Long | 否       | 部署通道数，当子链架构为fabric时必填                         |
| smartContractList.extra.address        |      String | 否       | 合约地址，当子链架构为xuperchain时必填                       |
| smartContractList.extra.creator        |      String | 否       | 合约创建账号，当子链架构为xuperchain时必填                   |
| smartContractList.extra.type           |      String | 否       | 合约类型， wasm合约、native合约，当子链架构为xuperchain时必填 |
| smartContractList.extra.chainName      |      String | 否       | 平行链名称，当子链架构为xuperchain时必填                     |

返回数据：

| **字段名** | **类型** | **描述** |
| :--------- | :------- | :------- |
| blobId     | String   | blodId   |
| txHash     | String   | 交易hash |
| blob       | String   | blob串   |

示例：

（1）请求示例：

```
http请求方式：POST
https://{url}/v1/chain/contract/syn/blob
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcGlLZXkiOiJDcHB0NHRuMFlFZkIyMHJXIiwiaXNzIjoiQklGLUNIQUlOIiwiZXhwIjoxNjIxNTcxMjg0LCJiaWQiOiJkaWQ6YmlkOmVmMjhwTTlNRzNUR1hHeVdBVzRKcFdDRnNKRGQ1TUJuYyJ9.9tTPWasYgCs1yC3qYJYSjCGvd9Syl1mr6G2EVrKeq2E",
  "params": {
    "ACSN": "ynjr",
    "gatewayAddress": "did:bid:efb8Ehu9SGVCTm2BbvpPiQjzNWo4LQAA",
    "smartContractList": [{
      "ownerAddress":"did:bid:efPGyex2nVvTJZPg8RzdtzEqF5UWCzdL22",
      "contractAddress": "did:bid:ynjr:efv7DynieC5sF1UoKAthKTfUCkuzaBfR",
      "time": 1593338217002,
      "name": "部署系统合约2",
      "contractType": 2,
      "industryType": "A",
      "payload": "'use strict'; function init(){return;}  function main(){return;}",
      "vm": "v2",
      "version":"1.0.2",
      "extra":"extra2",
      "internalChainId":"internalChainId2"
    }]
  }
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```
{
  "errorCode": 0,
  "message": "操作成功",
  "data": {
    "blobId": "15",
    "txHash": "d60c15bacbb7f98f00921d5ad17d49fafe0c65ea706d5d4ced25e490ac35e9e0",
    "blob": "0A286469643A6269643A..."
  }
}
```

b. 接口调用失败，则返回JSON数据示例为：

```
{
    "errorCode": 940000,
    "message": "系统内部错误"
}
```

##### 合约信息同步提交（上链）

接口说明：

对blob数据进行签名（参考 签名算法 章节），并提交至主链执行上链操作，用于子链合约信息同步提交至主链并上链存储

请求参数：

| **字段名**           |    **类型** | **是否必填** | **描述**                           |
| :------------------- | ----------: | :----------- | :--------------------------------- |
| blobId               |  String(20) | 是           | blobId                             |
| signerList           |        List | 是           | 签名者列表（注意：需要数据网关签名） |
| signerList.signBlob  | String(128) | 是           | 签名串（数据网关签名）               |
| signerList.publicKey | String(128) | 是           | 签名者公钥（数据网关公钥）           |

返回数据：

| **字段名** | **类型** | **描述** |
| :--------- | :------- | :------- |
| txHash     | String   | 交易hash |

示例：

（1）请求示例：

```
http请求方式：POST
https://{url}/v1/chain/contract/syn/submit
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcGlLZXkiOiJDcHB0NHRuMFlFZkIyMHJXIiwiaXNzIjoiQklGLUNIQUlOIiwiZXhwIjoxNjE5MzQyNDIyLCJiaWQiOiJkaWQ6YmlkOmVmMjhwTTlNRzNUR1hHeVdBVzRKcFdDRnNKRGQ1TUJuYyJ9.3gcQQBqvqtZH1q-TfUiGne68R1TnBcvLAA6nIJ8qDGU",
  "params": {
    "blobId": "4",
    "signerList": [{
      "signBlob": "5EC044231995FD4AF61CCA0AA7BA2479021509E48F3E3C061ED3CDB1CFECC79FCFE1BD28571236E55F72BA1260A8707CAF2D1D104D79A9218EBCCA9225066B06",
      "publicKey": "b06566086febd16adf6553cc9c000dba5f9f410d34f8541392303561dddc045b15ef4c"
    }]
  }
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```
{
    "errorCode": "0",
    "message": "操作成功",
      "data": {
      "txHash": "083b797ea00204d2c17a9e1bd77cab11385f475da756f76a96b922e4c7b8f7c7"
    }
}
```

b. 接口调用失败，则返回JSON数据示例为：

```
{
    "errorCode": 940000,
    "message": "系统内部错误"
}
```

#### 更新子链信息

##### 获取更新子链blob

接口说明：

提交更新子链的材料，获取更新子链的blob数据（blob是星火·链网上交易结构序列化后的十六进制格式），用于执行更新信息上链

请求参数：

| 字段名                            | 类型         | 是否必填 | 描述                                                         |
| --------------------------------- | ------------ | -------- | ------------------------------------------------------------ |
| backboneNodeBid                   | String(64)   | 是       | 骨干节点bid                                                  |
| ACSN                              | String(8)    | 是       | 要进行修改的链的链码                                         |
| contacts                          | object       | 否       | 联系人对象                                                   |
| contacts.name                     | string(20)   | 否       | 联系人姓名                                                   |
| contacts.phoneNum                 | string(12)   | 否       | 联系人电话                                                   |
| contacts.mail                     | string(30)   | 否       | 联系人邮箱                                                   |
| chainInfo                         | object       | 否       | 要进行修改的链信息对象                                       |
| chainInfo.industry                | string(4)    | 否       | 链行业类型（见第10节行业类型）                               |
| chainInfo.name                    | string(30)   | 否       | 子链名称                                                     |
| chainInfo.architectureId          | string(10)   | 否       | 链架构id： 链架构 10000:BIF-CORE、10001:Fabric、10002:Ethereum、 10003:BubiChain、10004:Quorum、10005：Xuperchain、10006:cita 、 10007：FISCO、10008：其他 |
| chainInfo.genesisAmount           | string(30)   | 否       | 创世账户token总数                                            |
| chainInfo.unit                    | string(32)   | 否       | token单位                                                    |
| chainInfo.precision               | String(30)   | 否       | token精度                                                    |
| chainInfo.baseReserve             | string(30)   | 否       | token保留数                                                  |
| chainInfo.feeGasPrice             | string(30)   | 否       | 最低燃料单价                                                 |
| chainInfo.rewardInitValue         | string(30)   | 否       | 出块奖励                                                     |
| chainInfo.genesisSlogan           | string(1024) | 否       | 子链slogan                                                   |
| chainInfo.description             | string(1024) | 否       | 子链介绍                                                     |
| chainInfo.gatewayNodeList         | Array        | 否       | 数据网关列表（需要填写主链的BID）                            |
| chainInfo.gatewayCrossList        | Array        | 否       | 跨链网关列表（需要填写主链的BID。建议数据网关和跨链网关使用不同的BID账号，否则开发者在多个服务中并发交易时，可能出现交易上链失败问题） |
| system                            | object       | 否       | 链系统信息                                                   |
| system.visitUrl                   | string(255)  | 否       | 子链入口                                                     |
| system.publicStatus               | string(2)    | 否       | 开发许可                                                     |
| resolveServiceList                | Object       | 否       | 解析服务对象列表                                             |
| resolveServiceList.ipv4[i].ip     | String(64)   | 否       | IPv4地址                                                     |
| resolveServiceList.ipv4[i].port   | String(5)    | 否       | 服务端口                                                     |
| resolveServiceList.ipv4[i].remark | String(128)  | 否       | 备注信息                                                     |
| resolveServiceList.ipv6[i].ip     | String(64)   | 否       | IPv6地址                                                     |
| resolveServiceList.ipv6[i].port   | String(5)    | 否       | 服务端口                                                     |
| resolveServiceList.ipv6[i].remark | String(128)  | 否       | 备注信息                                                     |
| resolveServiceList.url[i].address | String(255)  | 否       | URL地址，HTTP,HTTPS开始，不支持IP，以"/"为结尾               |
| resolveServiceList.url[i].remark  | String(128)  | 否       | 备注信息                                                     |

返回数据：

| **字段名** | **类型** | **描述**     |
| ---------- | -------- | ------------ |
| blobId     | String   | blobId       |
| txHash     | String   | 链上交易hash |
| blob       | String   | blob串       |

示例：

（1）请求示例：

```
http请求方式：POST
https://{url}/v1/chain/update/blob
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcGlLZXkiOiJDcHB0NHRuMFlFZkIyMHJXIiwiaXNzIjoiQklGLUNIQUlOIiwiZXhwIjoxNjE5MzQyNDIyLCJiaWQiOiJkaWQ6YmlkOmVmMjhwTTlNRzNUR1hHeVdBVzRKcFdDRnNKRGQ1TUJuYyJ9.3gcQQBqvqtZH1q-TfUiGne68R1TnBcvLAA6nIJ8qDGU",
  "params": {
    "backboneNodeBid":"did:bid:ef28pM9MG3TGXGyWAW4JpWCFsJDd5MBnc",
    "ACSN":"by01",
    "contacts":{
      "name":"dongzhiwei",
      "phoneNum":"15555555555",
      "mail":"dongzhiwei@qq.com"
    },
    "chainInfo":{
      "architectureId": "10000",
      "industry": "A",
      "name": "openapi测试链",
      "genesisAmount": "123",
      "unit": "unit",
      "precision": "1",
      "baseReserve": "100",
      "feeGasPrice": "1000",
      "rewardInitValue": "10000",
      "genesisSlogan": "genesisSlogan",
      "description": "description",
      "gatewayNodeList":["did:bid:ef248yRNC7XjBepsy631wV42q8RW96nX", "did:bid:efixsfN3agXnM8JVWa7Hh9PmAi3EuirM"],
      "gatewayCrossList":[""did:bid:ef448yRNC7XjBepsy631wV42q8RW96nX", "did:bid:efixsfN7agXnM8JVWa7Hh9PmAi3EuirM""],
    },
    "system":{
      "visitUrl": "http://www.baidu.com",
      "publicStatus": "0"
    },
    "resolveServiceList":{
      "ipv4": [{
        "ip": "192.168.1.1",
        "port": "18122",
        "remark": "4444"
      },
        {
          "ip": "192.168.2.2",
          "port": "18122",
          "remark": "55555"
        }
      ],
      "ipv6": [{
        "ip": "1111:0410:0000:1234:FB00:1400:5000:45FF",
        "port": "18122",
        "remark": "aaa"
      },
        {
          "ip": "2222:0410:0000:1234:FB00:1400:5000:45FF",
          "port": "18122",
          "remark": "bbb"
        }
      ],
      "url": [{
        "address": "",
        "remark": ""
      }]
    }
  }
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```
{
 "data":{
  "blobId": "232975729572",
  "txHash": "985ac10a6cda2f4b6c910f11bffed35fa504e53125c045d1fbbade6b335da50",
 "blob":"A296469643A..."
 }, 
 "errorCode": 0,
 "message": "操作成功"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```
{
    "errorCode": 940000,
    "message": "系统内部错误"
}
```

##### 更新子链提交交易（上链）

接口说明：

对blob数据进行签名（参考 签名算法 章节），并提交至主链执行上链操作；上链完成后由超级节点对更新信息进行审核。

请求参数：

用于将更新子链流程提交至主链并上链存储，请示参数由3.11.1接口中获取，参数如下：

| **字段名**           | **类型**    | **是否必填** | **描述**                         |      |
| -------------------- | ----------- | ------------ | -------------------------------- | ---- |
| blobId               | String(19)  | 是           | blobID                           |      |
| signerList           | List        | 是           | 签名者列表（骨干节点签名）       |      |
| signerList.signBlob  | String(128) | 是           | 签名串（骨干节点对blob进行签名） |      |
| signerList.publicKey | String(128) | 是           | 签名者公钥（骨干节点公钥）       |      |

返回数据：

（1）成功：

返回的交易哈希

| **字段名** | **类型** | **描述**     |
| ---------- | -------- | ------------ |
| txHash     | String   | 链上交易hash |
| errorCode  | int      | 0            |
| message    | String   | 成功         |

（2）失败：

说明调用接口失败，请参考错误码执行下一步操作。

| **字段名** | **类型** | **描述**                 |
| ---------- | -------- | ------------------------ |
| errorcode  | int      | 错误码，如940000         |
| message    | String   | 错误信息，如系统内部错误 |

示例：

（1）提交获取到的更新子链blob数据，示例如下：

```
http请求方式：POST
https://{url}/v1/chain/update/submit
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcGlLZXkiOiJDcHB0NHRuMFlFZkIyMHJXIiwiaXNzIjoiQklGLUNIQUlOIiwiZXhwIjoxNjE5MjU2OTEwLCJiaWQiOiJkaWQ6YmlkOmVmaXV5cXVHV1R2UkVzWTltclZvS1ZoRmU1Wkp4WmRSIn0.0nUb20tqYIhcD-cS_a6YCGFM9AwZDyB7x_MFeIQv_Pc",
  "params": {
    "blobId": "144",
    "blob":"",
    "signerList": [{
      "signBlob": "5DFE2A2136B49321DDB7F5E83B23B27BE3E05FBCE8240782EE75BF592D53C7EEFEDF1D7CCA33FC8FE972E94FA67E3D083E58DFCC81E4DF78DC3B910341413701",
      "publicKey": "b065660ae694d678de4d648e04f4b86247fae59cef3590da8370664a520d9aaaaf1de3"
    }]
  }
}
```

（2）返回结果示例：

a. 成功：

接口调用成功，则返回JSON数据示例如下：

```
{
  "data":{
        "txHash": "985ac10a6cda2f4b6c910f11bffed35fa504e53125c045d1fbbade6b335da50"
  }, 
  "errorCode": "0",
  "message": "操作成功"
}
```

b. 接口调用失败，则返回JSON数据示例为：

```
{
    "errorCode": 940000,
    "message": "系统内部错误"
}
```





#### 获取区域信息

接口说明：

用于获取区域信息（省、市、县）

请求参数：

| **字段名** |  **类型** | **是否必填** | **描述**                                                     |
| :--------- | --------: | :----------- | :----------------------------------------------------------- |
| pcode      | String(8) | 否           | 父级编码(为空获取所有省、通过省的编号获取到下面市的编号、通过市获取县的编号) |

返回数据：

| **字段名**         | **类型** | **描述** |
| :----------------- | :------- | :------- |
| errorCode          | Integer  | 错误码   |
| message            | String   | 错误描述 |
| areaList.name      | String   | 区域名称 |
| areaList.adcode    | String   | 区域编码 |
| areaList.longitude | String   | 经度     |
| areaList.latitude  | String   | 纬度     |

示例：

（1）请求示例：

```
http请求方式：POST
https://{url}/v1/bid/area/info/list
{
    "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcGlLZXkiOiJDcHB0NHRuMFlFZkIyMHJXIiwiaXNzIjoiQklGLUNIQUlOIiwiZXhwIjoxNjIxNTk0NDQ4LCJiaWQiOiJkaWQ6YmlkOmVmMjhwTTlNRzNUR1hHeVdBVzRKcFdDRnNKRGQ1TUJuYyJ9.MxWdV-mwCScUq8QwmTXTaxKli8jvXq1sNVvAYQWWsSo",
    "params": {
        "pcode":"510000"
    }
}
```

（2）返回结果示例：

a. 接口调用成功，则返回JSON数据示例为：

```
{
  "errorCode": 0,
  "message": "操作成功",
  "data": {
    "areaList": [
      {
        "name": "巴中市",
        "adcode": "511900",
        "longitude": "106.753669",
        "latitude": "31.858809"
      },
      {
        "name": "成都市",
        "adcode": "510100",
        "longitude": "104.065735",
        "latitude": "30.659462"
      },
      {
        "name": "广元市",
        "adcode": "510800",
        "longitude": "105.829757",
        "latitude": "32.433668"
      },
      {
        "name": "南充市",
        "adcode": "511300",
        "longitude": "106.082974",
        "latitude": "30.795281"
      },
      {
        "name": "德阳市",
        "adcode": "510600",
        "longitude": "104.398651",
        "latitude": "31.127991"
      },
      {
        "name": "绵阳市",
        "adcode": "510700",
        "longitude": "104.741722",
        "latitude": "31.46402"
      },
      {
        "name": "遂宁市",
        "adcode": "510900",
        "longitude": "105.571331",
        "latitude": "30.513311"
      },
      {
        "name": "资阳市",
        "adcode": "512000",
        "longitude": "104.641917",
        "latitude": "30.122211"
      },
      {
        "name": "广安市",
        "adcode": "511600",
        "longitude": "106.633369",
        "latitude": "30.456398"
      },
      {
        "name": "内江市",
        "adcode": "511000",
        "longitude": "105.066138",
        "latitude": "29.58708"
      },
      {
        "name": "达州市",
        "adcode": "511700",
        "longitude": "107.502262",
        "latitude": "31.209484"
      },
      {
        "name": "眉山市",
        "adcode": "511400",
        "longitude": "103.831788",
        "latitude": "30.048318"
      },
      {
        "name": "自贡市",
        "adcode": "510300",
        "longitude": "104.773447",
        "latitude": "29.352765"
      },
      {
        "name": "泸州市",
        "adcode": "510500",
        "longitude": "105.443348",
        "latitude": "28.889138"
      },
      {
        "name": "宜宾市",
        "adcode": "511500",
        "longitude": "104.630825",
        "latitude": "28.760189"
      },
      {
        "name": "乐山市",
        "adcode": "511100",
        "longitude": "103.761263",
        "latitude": "29.582024"
      },
      {
        "name": "攀枝花市",
        "adcode": "510400",
        "longitude": "101.716007",
        "latitude": "26.580446"
      },
      {
        "name": "凉山彝族自治州",
        "adcode": "513400",
        "longitude": "102.258746",
        "latitude": "27.886762"
      },
      {
        "name": "雅安市",
        "adcode": "511800",
        "longitude": "103.001033",
        "latitude": "29.987722"
      },
      {
        "name": "阿坝藏族羌族自治州",
        "adcode": "513200",
        "longitude": "102.221374",
        "latitude": "31.899792"
      },
      {
        "name": "甘孜藏族自治州",
        "adcode": "513300",
        "longitude": "101.963815",
        "latitude": "30.050663"
      }
    ]
  }
}

```

b. 接口调用失败，则返回JSON数据示例为：

```
{
    "errorCode": 940000,
    "message": "系统内部错误"
}
```



### 底层链业务接入

 

#### 链应用服务信息同步

接口说明：

子链应用服务信息同步到主链（要求每5分钟同步一次。将5分钟内的子链应用服务信息同步上来）

请求参数：

| **字段名**     |   **类型** | **是否必填** | **描述**                                                     |
| :------------- | ---------: | :----------- | :----------------------------------------------------------- |
| ACSN           |  String(4) | 是           | 子链AC号                                                     |
| businessType   |    Integer | 是           | 业务类型：1溯源，2存证，3供应链金融 20 其他                  |
| dataType       |    Integer | 是           | 数据类型： 当业务类型为溯源时，1-溯源产品记录、2-生产环节记录； 当业务类型为存证时，1-存证作品记录、2-作品权利列表、3-作品侵权列表； 当业务类型为供应链金融时，1-参与主体记录、2-供应链金融流程记录 |
| dataList       |      Array | 是           | 数据数组                                                     |
| dataList.key   | String(64) | 是           | 记录ID，用于标记同步的某条数据                               |
| dataList.time  |       Long | 是           | 毫秒级时间戳，用于数据查询时排序                             |
| dataList.value |     Object | 是           | 业务数据对象，具体结构详见后表                               |

##### 1） 溯源类应用服务同步数据

 1.1）**同步溯源产品记录**：

```
http请求方式：POST
https://{url}/v1/chain/appService/info/syn
{
    "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcGlLZXkiOiJDcHB0NHRuMFlFZkIyMHJXIiwiaXNzIjoiQklGLUNIQUlOIiwiZXhwIjoxNjE5MzQyNDIyLCJiaWQiOiJkaWQ6YmlkOmVmMjhwTTlNRzNUR1hHeVdBVzRKcFdDRnNKRGQ1TUJuYyJ9.3gcQQBqvqtZH1q-TfUiGne68R1TnBcvLAA6nIJ8qDGU",
    "params": {
        "ACSN": "cc11",
        "businessType": 1,
        "dataType": 1,
        "dataList": [{
            "key": "{key}",
            "time": 1593338217000,
            "value": {
                "name": "名称",
                "type": "名称",
                "num": "123",
                "creator": "123",
                "time": 1593338217000,
                "picture": ""
            }
        }]
    }
}
```

业务数据对象：溯源类产品记录核心字段说明

| **字段名** | **类型** | **是否必填** | **描述**                 |
| :--------- | -------: | :----------- | :----------------------- |
| name       |   String | 是           | 产品名称                 |
| type       |   String | 是           | 业务类型                 |
| time       |  Integer | 是           | 毫秒级时间戳，生成时间   |
| num        |   String | 是           | 产品信息编号，子链上唯一 |
| creator    |   String | 是           | 创建用户                 |
| picture    |   String | 是           | 产品图片                 |