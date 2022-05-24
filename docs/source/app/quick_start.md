# 快速上手

以Java SDK为例, 在星火链测试网上部署, 调用, 查询一个Javascript智能合约.

## SDK下载

请到<https://github.com/caict-4iot-dev/BIF-Core-SDK>下载java版本的SDK.

## 账号创建

调用JavaSDK接口离线创建一个账户.

```java
import cn.bif.model.crypto.KeyPairEntity;
entity = KeyPairEntity.getBidAndKeyPair();                             //离线创建一个新账号
System.out.printf("BID address %s\n", entity.getEncAddress());          //账户地址, 可以公开
System.out.printf("privatekey %s\n", entity.getEncPrivateKey());      //账户私钥, 请妥善保管
```

## 获取星火令

账户需要拥有星火令才能正常使用星火链功能, 测试网星火令可以通过邮件联系**niefanjie@caict.ac.cn** 获取.

## 初始化SDK

通过配置星火链RPC地址连接SDK到星火链, 本次demo里链接到星火链测试网.

```java
import cn.bif.api.BIFSDK;

public static final String NODE_URL = "http://test.bifcore.bitfactory.cn";  //星火链测试网RPC地址

public staitc BIFSDK sdk = BIFSDK.getInstance(NODE_URL);
```

## 查看账户状态

```java
//构建查看账户请求
BIFAccountGetInfoRequest infoReq = new BIFAccountGetInfoRequest();
//要查看账户的地址
infoReq.setAddress(address);

//发出查询请求
BIFAccountGetInfoResponse infoRsp = sdk.getBIFAccountService().getAccount(infoReq);

if (infoRsp.getErrorCode() == 0) {
    //查询成功
    System.out.println(JsonUtils.toJSONString(infoRsp.getResult()));
} else {
    //查询失败
    System.out.println(infoRsp.getErrorDesc());
}
```

*注意, 新创建的空白账户查询会失败, 需要转入星火令激活才能正常使用.*


正常账户查询返回示例:

```json
{
    "address":"did:bid:efKkF5uKsopAishxkYja4ULRJhrhrJQU",    //账户地址
    "balance":10000000000,                                   //账户余额
    "nonce":0                                                //账户发出的交易计数
}
```

## 合约部署

部署合约分为Javascript、solidity智能合约的部署。

#### Javascript智能合约代码

* Javascript智能合约代码如下:

  ```js
  "use strict";
  
  function queryById(id) {                        //合约内部函数
      let data = Chain.load(id);
      return data;
  }
  
  function query(input) {                         //合约查询入口
      input = JSON.parse(input);
      let id = input.id;
      let object = queryById(id);
      return object;
  }
  
  function main(input) {                          //合约调用入口
      input = JSON.parse(input);
      Chain.store(input.id, input.data);
  }
  
  function init(input) {                          //初始化函数
      return;
  }
  ```

  该合约实现了一个简单的存储功能, 用户可以调用main接口存储自定义Key-Value信息, 然后通过query接口查询已经存入的Key-Value信息.

* 部署合约

  合约编写完毕后, 需要将合约部署到链上, **注意这里需要账户内有足够的XHT**, 部署代码如下:

  ```java
  //部署合约
  
  //合约代码，注意转义
  String contractCode = "\"use strict\";function queryById(id) {    let data = Chain.load(id);    return data;}function query(input) {    input = JSON.parse(input);    let id = input.id;    let object = queryById(id);    return object;}function main(input) {    input = JSON.parse(input);    Chain.store(input.id, input.data);}function init(input) {    return;}";
  
  BIFContractCreateRequest createCReq = new BIFContractCreateRequest();
  
  //创建方地址和私钥
  createCReq.setSenderAddress(address);
  createCReq.setPrivateKey(privateKey);
  
  //合约初始balance，一般为0
  createCReq.setInitBalance(0L);
  
  //合约代码
  createCReq.setPayload(contractCode);
  
  //标记和type，javascript合约type为0
  createCReq.setRemarks("create contract");
  createCReq.setType(0);
  
  //交易耗费上限
  createCReq.setFeeLimit(300000000L);
  
  //调用SDK创建该合约
  BIFContractCreateResponse createCRsp = sdk.getBIFContractService().contractCreate(createCReq);
  
  if (createCRsp.getErrorCode() == 0) {
      System.out.println(JsonUtils.toJSONString(createCRsp.getResult()));
  } else {
      System.out.println(JsonUtils.toJSONString(createCRsp));
  }
  ```

  如果部署成功, 调用返回里会拿到这个交易的HASH.

  ```json
  {
      "hash":"b25567a482e674d79ac5f9b5f6601f27b676dde90a6a56539053ec882a99854f"
  }
  ```

* 交易信息和合约地址查询

  用SDK查询部署合约的交易详细信息, 可以从中获取到创建的合约地址.

  ```java
  BIFContractGetAddressRequest cAddrReq = new BIFContractGetAddressRequest();
  cAddrReq.setHash(cTxHash);
  
  BIFContractGetAddressResponse cAddrRsp = sdk.getBIFContractService().getContractAddress(cAddrReq);
  if (cAddrRsp.getErrorCode() == 0) {
      System.out.println(JsonUtils.toJSONString(cAddrRsp.getResult()));
  } else {
      System.out.println(cAddrRsp.getErrorDesc());
  }
  ```

  合约部署信息示例如下:

  ```json
  {
      "contract_address_infos":[
          {
              "contract_address":"did:bid:efSvDJivc2A4iqurRkUPzmpT5kB3nkNg",
              "operation_index":0
          }
      ]
  }
  ```

  did:bid:efSvDJivc2A4iqurRkUPzmpT5kB3nkNg即为刚刚创建的合约链上地址.



#### Solidity智能合约代码

* Solidity智能合约代码如下:

  ```solidity
  pragma solidity ^0.4.26;
  
  contract demo  {
  
    mapping(uint256 => string) private _datas;
  
    function queryById(uint256 id) public view returns (string) {                      
      
      return _datas[id];
    }
  
    function setById(uint256 id, string data) public {                      
      
      _datas[id] = data;
    }
  
  }
  ```

  该合约实现了一个简单的存储功能, 用户可以调用setById接口存储自定义Key-Value信息, 然后通过queryById接口查询已经存入的Key-Value信息.

* 部署合约

  合约编写完毕后, 需要将合约部署到链上, **注意这里需要账户内有足够的XHT**, 部署代码如下:

  solidity智能合约和Javascript智能合约的部署，区别在于：

  type的设置：0代表Javascript智能合约，1代表solidity智能合约。

  setPayload时，设置的不是solidity智能合约代码本身，而是对合约代码进行编译之后，得到的bytecode中的object值。可以参考[星火链Solidity编译器](https://bif-doc.readthedocs.io/zh_CN/latest/app/solidity.html#id5)章节。

  ```java
  //部署合约
  
  //合约代码，注意转义
  String contractCode = "608060405234801561001057600080fd5b5061031a806100206000396000f30060806040526004361061004c576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063794bde4814610051578063baf8baab146100c4575b600080fd5b34801561005d57600080fd5b506100c260048036038101908080359060200190929190803590602001908201803590602001908080601f016020809104026020016040519081016040528093929190818152602001838380828437820191505050505050919291929050505061016a565b005b3480156100d057600080fd5b506100ef60048036038101908080359060200190929190505050610195565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561012f578082015181840152602081019050610114565b50505050905090810190601f16801561015c5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b806000808481526020019081526020016000209080519060200190610190929190610249565b505050565b60606000808381526020019081526020016000208054600181600116156101000203166002900480601f01602080910402602001604051908101604052809291908181526020018280546001816001161561010002031660029004801561023d5780601f106102125761010080835404028352916020019161023d565b820191906000526020600020905b81548152906001019060200180831161022057829003601f168201915b50505050509050919050565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061028a57805160ff19168380011785556102b8565b828001600101855582156102b8579182015b828111156102b757825182559160200191906001019061029c565b5b5090506102c591906102c9565b5090565b6102eb91905b808211156102e75760008160009055506001016102cf565b5090565b905600a165627a7a7230582075ed105ec168ecd3a86662e29c88feeda3d3efc52352668732787710747da4090029";
  
  BIFContractCreateRequest createCReq = new BIFContractCreateRequest();
  
  //创建方地址和私钥
  createCReq.setSenderAddress(address);
  createCReq.setPrivateKey(privateKey);
  
  //合约初始balance，一般为0
  createCReq.setInitBalance(0L);
  
  //合约代码
  createCReq.setPayload(contractCode);
  
  //标记
  createCReq.setRemarks("create contract");
  //type，javascript合约type为0，solidity合约type为1
  createCReq.setType(1);
  
  //交易耗费上限
  createCReq.setFeeLimit(300000000L);
  
  //调用SDK创建该合约
  BIFContractCreateResponse createCRsp = sdk.getBIFContractService().contractCreate(createCReq);
  
  if (createCRsp.getErrorCode() == 0) {
      System.out.println(JsonUtils.toJSONString(createCRsp.getResult()));
  } else {
      System.out.println(JsonUtils.toJSONString(createCRsp));
  }
  ```

  如果部署成功, 调用返回里会拿到这个交易的HASH.

  ```json
  {
      "hash":"7cbc5345f80d250c0086bb04f974c9f648345f3d8d86f074907e07f1cc02615a"
  }
  ```

* 交易信息和合约地址查询

  用SDK查询部署合约的交易详细信息, 可以从中获取到创建的合约地址.

  ```java
  BIFContractGetAddressRequest cAddrReq = new BIFContractGetAddressRequest();
  cAddrReq.setHash(cTxHash);
  
  BIFContractGetAddressResponse cAddrRsp = sdk.getBIFContractService().getContractAddress(cAddrReq);
  if (cAddrRsp.getErrorCode() == 0) {
      System.out.println(JsonUtils.toJSONString(cAddrRsp.getResult()));
  } else {
      System.out.println(cAddrRsp.getErrorDesc());
  }
  ```

  合约部署信息示例如下:

  ```json
  {
      "contract_address_infos":[
          {
              "contract_address":"did:bid:efhYR8gf3jputq3hmT2meFdF4HzbwMzW",
              "operation_index":0
          }
      ]
  }
  ```

  did:bid:efSvDJivc2A4iqurRkUPzmpT5kB3nkNg即为刚刚创建的合约链上地址.





## 合约调用

#### Javascript智能合约的合约调用:

合约成功部署并且获取到合约地址后, 就可以通过SDK发送交易调用合约接口, 我们存储一个Key-Value对到合约里:

调用合约input如下

```json
{
    "id":"test",
    "data": "test"
}
```

调用合约代码如下:

```java
//转义后input
String input = "{\"id\":\"test\", \"data\": \"test\"}";

BIFContractInvokeRequest cIvkReq = new BIFContractInvokeRequest();

//调用者地址和私钥
cIvkReq.setSenderAddress(publicKey);
cIvkReq.setPrivateKey(privateKey);

//合约地址
cIvkReq.setContractAddress(cAddr);

//调用交易XHT金额
cIvkReq.setBIFAmount(0L);

//标记
cIvkReq.setRemarks("contract invoke");

//调用input
cIvkReq.setInput(input);

BIFContractInvokeResponse cIvkRsp = sdk.getBIFContractService().contractInvoke(cIvkReq);
if (cIvkRsp.getErrorCode() == 0) {
    System.out.println(JsonUtils.toJSONString(cIvkRsp.getResult()));
} else {
    System.out.println(cIvkRsp.getErrorDesc());
}
```

调用成功后，我们会得到调用交易的HASH：

```json
{
    "hash":"c79835265e908f7f06d4fc2c61ef3fd046ae5252675e4671271bd921ad8fde89"
}
```





#### Solidity智能合约的合约调用:

合约成功部署并且获取到合约地址后, 就可以通过SDK发送交易调用合约接口, 我们存储一个Key-Value对到合约里:

调用合约input如下

```json
{
    "id":123,
    "data": "abc"
}
```

调用合约代码如下:

```java
//转义后input
String input = "{\"function\":\"setById(uint256,string)\", \"args\":\"123,'abc'\"}";

BIFContractInvokeRequest cIvkReq = new BIFContractInvokeRequest();

//调用者地址和私钥
cIvkReq.setSenderAddress(publicKey);
cIvkReq.setPrivateKey(privateKey);

//合约地址
cIvkReq.setContractAddress(cAddr);

//调用交易XHT金额
cIvkReq.setBIFAmount(0L);

//设置费用上限
request.setFeeLimit(100000000L);
request.setGasPrice(10L);

//标记
cIvkReq.setRemarks("contract invoke");

//调用input
cIvkReq.setInput(input);

BIFContractInvokeResponse cIvkRsp = sdk.getBIFContractService().contractInvoke(cIvkReq);
if (cIvkRsp.getErrorCode() == 0) {
    System.out.println(JsonUtils.toJSONString(cIvkRsp.getResult()));
} else {
    System.out.println(cIvkRsp.getErrorDesc());
}
```

调用成功后，我们会得到调用交易的HASH：

```json
{
    "hash":"0606cc9e910028bb5918bcf79934d02c81665c6819d6f5ee51b99f3ce95b5f82"
}
```



## 查询合约

#### Javascript智能合约的合约查询:

不同于调用合约, 查询合约为只读操作, 因此不需要发出上链交易和耗费gas, 这里我们查询刚刚设置的key, 查询input为:

```json
{
    "id":"test"
}
```

Java查询代码如下:

```java
BIFContractCallRequest cCallReq = new BIFContractCallRequest();             //查询请求

String callInput = "{\"id\":\"test\"}";                                     //查询input

cCallReq.setContractAddress(cAddr);
cCallReq.setInput(callInput);

BIFContractCallResponse cCallRsp = sdk.getBIFContractService().contractQuery(cCallReq); //查询

if (cCallRsp.getErrorCode() == 0) {
    System.out.println(JsonUtils.toJSONString(cCallRsp.getResult()));
} else {
    System.out.println(cCallRsp.getErrorDesc());
}
```

查询的返回如下:

```json
{
    "query_rets":[
        {
            "result":
                {
                    "type":"string",
                    "value":"test"
                }
        }
    ]
}
```



#### Solidity智能合约的合约查询:

不同于调用合约, 查询合约为只读操作, 因此不需要发出上链交易和耗费gas, 这里我们查询刚刚设置的key, 查询input为:

```json
{
    "id":123
}
```

Java查询代码如下:

```java
BIFContractCallRequest cCallReq = new BIFContractCallRequest();             //查询请求

String callInput = "{\"function\":\"queryById(uint256)\",\"args\":123,\"return\":\"returns(string)\"}";                                     //查询input

cCallReq.setContractAddress(cAddr);
cCallReq.setInput(callInput);

BIFContractCallResponse cCallRsp = sdk.getBIFContractService().contractQuery(cCallReq); //查询

if (cCallRsp.getErrorCode() == 0) {
    System.out.println(JsonUtils.toJSONString(cCallRsp.getResult()));
} else {
    System.out.println(cCallRsp.getErrorDesc());
}
```

查询的返回如下:

```json
{
    "query_rets":[
        {
            "result":{
                "data":"[abc]",
            }
        }
    ]
}
```





## 接下来

至此我们就完成了一个链上javascript合约从部署到操作的全过程, 有关合约的更高阶开发和星火链体系模型, 请参见后续专栏.
