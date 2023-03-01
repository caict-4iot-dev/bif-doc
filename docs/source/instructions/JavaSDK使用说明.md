# 1.Java SDK使用说明

## 1.1 SDK概述

BIF-Core-SDK通过API调用的方式提供了星火链网-底层区块链平台公私钥对生成、星火链网-底层区块链平台私钥签名公钥验签、账号服务、区块服务、交易服务等接口，同时还提供了接口使用示例说明，开发者可以调用该SDK方便快捷的生成星火链网主链的快速接入。中国信通院秉持开源开放的理念，将星火“BID-Core-SDK”面向社区和公众完全开源，助力全行业伙伴提升数据价值流通的效率，实现数据价值转化。

星火链提供了多种语言的`SDK`，包括：`Go SDK`、`Java SDK`、`Nodejs SDK`方便开发者根据需要进行选用。

<img src="../_static/images/image-20211012184224056.png" alt="image-20211012184224056" style="zoom:80%;" />

<center style="font-weight:bold;">图1 BIF-Core-SDK 逻辑架构图</center>

## 1.2  环境准备

### 1.2.1 软件依赖

**java**：版本jdk 1.8.0_202或以下

下载地址：https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html

若已安装，请通过命令查看版本：

```sh
$ java -version
java version "1.8.0_202"
```

### 2.2.2 下载安装

```http
$ git clone -b release/1.0.1  --depth=1 http://github.com/caict-4iot-dev/BIF-Core-SDK.git
```

## 1.3  怎么使用SDK

### 1.3.1 应用demo

java sdk应用示例，请参考[ bif-chain-sdk-example](https://github.com/caict-4iot-dev/BIF-Core-SDK/tree/release/1.0.1/bif-chain-sdk-example)

### 1.3.2 SDK 离线API

离线API主要是账户和密码学相关API, 不需要连接星火链网RPC接口也能工作. 主要接口如下:

#### 账户生成

1. 接口 ` KeyPairEntity.getBidAndKeyPair`

1. 用途:

    用来生成一个星火链bid地址和对应私钥

1. 示例

    ```java
    import cn.bif.model.crypto.KeyPairEntity;

       KeyPairEntity keypair = KeyPairEntity.getBidAndKeyPair();
          String encAddress = keypair.getEncAddress();
          String encPublicKey = keypair.getEncPublicKey();
          String encPrivateKey = keypair.getEncPrivateKey();
          byte[] rawPublicKey = keypair.getRawPublicKey();
          byte[] rawPrivateKey = keypair.getRawPrivateKey();
       System.out.println(JsonUtils.toJSONString(keypair))
    ```


#### 加密私钥生成keystore

1. 接口 `KeyStore.generateKeyStore`

1. 用途:

    用一个密码来加密保护私钥, 得到一个json表示的keystore, 对应密码不泄露的情况下, 可以公开保存.

1. 示例

    ```java
    package cn.bif.sdkSamples.encryption.example;

    import cn.bif.common.JsonUtils;
    import cn.bif.module.encryption.crypto.keystore.KeyStore;
    import cn.bif.module.encryption.crypto.keystore.entity.KeyStoreEty;

    import java.util.HashMap;
    import java.util.Map;
    
    public class TestCrypto {
        public static void main(String argv[]) {
            String encPrivateKey = "priSPKqru2zMzeb14XWxPNM1sassFeqyyUZotCAYcvCjhNof7t";
            String password = "bif8888";
            TestKeyStoreWithPrivateKey(encPrivateKey, password);
    
        }
    
        public static void TestKeyStoreWithPrivateKey(String encPrivateKey, String password) {
            try {
                int n = (int) Math.pow(2, 16);
                //生成keystore-1
                KeyStoreEty returEencPrivateKey = KeyStore.generateKeyStore(password,encPrivateKey, 2, 1, 1, n);
                System.out.println(JsonUtils.toJSONString(returEencPrivateKey));
    
                //生成keystore-2
                KeyStoreEty keyStore1 = KeyStore.generateKeyStore(password, encPrivateKey, n);
                System.out.println(JsonUtils.toJSONString(keyStore1));
    
                //从keystore反解出私钥
                String keyStoreStr="{\"address\":\"did:bid:efEScJgGPf54vfU8ciEjjugkJLB4xYzp\",\"aesctr_iv\":\"EEDDD37CEB6864030124142CEB081BCD\",\"cypher_text\":\"7274705F65388E30338A2D69AE2241DBABCF66550C0453BEE30CFA45F02E04D08FAC551B46171531CA067B6E85BC342F43C8\",\"scrypt_params\":{\"n\":16384,\"p\":1,\"r\":8,\"salt\":\"82D37133C13525EDE4EF19DCD692592FC1685B5EDAABA8C943EA2C1AD4596FB3\"},\"version\":2}";
                String privateKey = KeyStore.decipherKeyStore(password, JsonUtils.toJavaObject(keyStoreStr,KeyStoreEty.class));
                System.out.println(privateKey);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    
    }
    ```

### 1.3.3 SDK 在线API

在线API主要用于向星火链上发出交易和查询合约, 需要初始化SDK连接后使用.

#### 初始化SDK

1. 示例

    ```java
    import cn.bif.api.BIFSDK;

    String SDK_INSTANCE_URL="http://test.bifcore.bitfactory.cn";
    BIFSDK sdk = BIFSDK.getInstance(SDK_INSTANCE_URL);   //SDK_INSTANCE_URL为星火链RPC地址
    ```

#### 广播交易

广播交易是指通过广播的方式发起交易。广播交易包括以下步骤：

1. [获取账户nonce值](#获取账户nonce值)

1. [构建操作](#构建操作)

1. [序列化交易](#序列化交易)

1. [签名交易](#签名交易)

1. [提交交易](#提交交易)

   ##### 获取账户nonce值

   开发者可自己维护各个账户`nonce`，在提交完一个交易后，自动为`nonce`值递增1，这样可以在短时间内发送多笔交易，否则，必须等上一个交易执行完成后，账户的`nonce`值才会加1。调用如下：

   ```java
      // 初始化请求参数
      String senderAddress = "did:bid:efqhQu9YWEWpUKQYkAyGevPGtAdD1N6p";
      BIFAccountGetNonceRequest request = new BIFAccountGetNonceRequest();
      request.   setAddress(senderAddress);
      // 调用getNonce接口
      Long nonce=0L;
      BIFAccountGetNonceResponse response = sdk.getBIFAccountService().getNonce(request);
       if (0 == response.getErrorCode()) {
          nonce=response.getResult().getNonce();
          System.out.println("Account nonce:" + response.getResult().getNonce());
       }else {
          System.out.println(JsonUtils.toJSONString(response));
       }
   ```
   
##### 构建操作

这里的操作是指在交易中做的一些动作，便于序列化交易和评估费用。例如，构建创建账号操作(BIFAccountActivateOperation)，接口调用如下：

   ```java
   // 初始化变量
   Long initBalance = ToBaseUnit.ToUGas("0.01");
   String destAddress = "did:bid:ef3LqNzb4ssNf2vqwNwBfqngrA3Sx8yD";
   
   BIFAccountActivateOperation operation = new BIFAccountActivateOperation();
      operation.setDestAddress(destAddress);
      operation.setInitBalance(initBalance);
   ```

##### 序列化交易

该接口用于序列化交易，并生成交易Blob串，便于网络传输。其中nonce和operation是上面接口得到的。调用如下：

   ```java
   // 初始化变量
   String senderAddress = "did:bid:efqhQu9YWEWpUKQYkAyGevPGtAdD1N6p";
   Long gasPrice = 1000L;
   Long feeLimit = ToBaseUnit.ToUGas("0.01");
   
   // 初始化请求参数
   BIFTransactionSerializeRequest serializeRequest = new BIFTransactionSerializeRequest();
      serializeRequest.setSourceAddress(senderAddress);
      serializeRequest.setNonce(nonce + 1);
      serializeRequest.setFeeLimit(feeLimit);
      serializeRequest.setGasPrice(gasPrice);
      serializeRequest.setOperation(operation);
      serializeRequest.setDomainId(0);
   // 调用buildBlob接口
    BIFTransactionSerializeResponse serializeResponse = sdk.getBIFTransactionService().BIFSerializable(serializeRequest);
           if (!serializeResponse.getErrorCode().equals(Constant.SUCCESS)) {
               throw new SDKException(serializeResponse.getErrorCode(), serializeResponse.getErrorDesc());
     }
    String transactionBlob = serializeResponse.getResult().getTransactionBlob();
   
   ```

##### 签名交易

该接口用于交易发起者使用其账户私钥对交易进行签名。其中transactionBlob是上面接口得到的。调用如下：

```java
   // 初始化请求参数
   String senderPrivateKey = "priSPKqru2zMzeb14XWxPNM1sassFeqyyUZotCAYcvCjhNof7t";
   byte[] signBytes = PrivateKeyManager.sign(HexFormat.hexToByte(transactionBlob), senderPrivateKey); 
   
```

##### 提交交易

该接口用于向BIF-Core区块链发送交易请求，触发交易的执行。其中transactionBlob和signBytes是上面接口得到的。调用如下：

   ```java
   // 初始化参数
   String publicKey = PrivateKeyManager.getEncPublicKey(senderPrivateKey);
   BIFTransactionSubmitRequest submitRequest = new BIFTransactionSubmitRequest();
     submitRequest.setSerialization(transactionBlob);
     submitRequest.setPublicKey(publicKey);
     submitRequest.setSignData(HexFormat.byteToHex(signBytes));
        // 调用bifSubmit接口
     BIFTransactionSubmitResponse transactionSubmitResponse =                       sdk.getBIFTransactionService().BIFSubmit(submitRequest);
   //交易hash
   String transactionHash=transactionSubmitResponse.getResult().getHash();
   ```


#### 账户处理接口

1. 查询账户信息

    1. 接口 `BIFAccountGetInfoRequest`

    1. 用途:

        用来获取一个账户当前信息

    1. 示例
        ```java
           // 初始化参数
           String accountAddress = "did:bid:efnVUgqQFfYeu97ABf6sGm3WFtVXHZB2";
           BIFAccountGetInfoRequest request = new BIFAccountGetInfoRequest();
              request.setAddress(accountAddress);
           // 调用getAccount接口
       BIFAccountGetInfoResponse response = sdk.getBIFAccountService().getAccount(request);
        
           if (response.getErrorCode() == 0) {
               System.out.println(JsonUtils.toJSONString(response.getResult()));
           } else {
               System.out.println(JsonUtils.toJSONString(response));
           }
       ```

1. 获取账户nonce

    1. 接口 `BIFAccountGetNonceRequest`

    1. 用途:

        用来获取一个账户当前nonce值, 有关nonce含义, 请参照**星火链开发入门**章节

    1. 示例:
        ```java
           // 初始化参数
           String accountAddress = "did:bid:efnVUgqQFfYeu97ABf6sGm3WFtVXHZB2";
           BIFAccountGetNonceRequest request = new BIFAccountGetNonceRequest();
              request.setAddress(accountAddress);
           BIFAccountGetNonceResponse response = sdk.getBIFAccountService().getNonce(request);
           if (0 == response.getErrorCode()) {
               System.out.println("Account nonce:" + response.getResult().getNonce());
           }else {
               System.out.println(JsonUtils.toJSONString(response));
           }
        ```

1. 获取账户余额

    1. 接口 `BIFAccountGetBalanceRequest`

    1. 用途:

        用来获取一个账户当前的XHT余额.

    1. 示例:

        ```java
           // 初始化参数
           String accountAddress = "did:bid:efzE8AcDgWUeNbgujA5hK3oUeuG9k19b";
           BIFAccountGetBalanceRequest request = new BIFAccountGetBalanceRequest();
           request.setAddress(accountAddress);
        
           BIFAccountGetBalanceResponse response = sdk.getBIFAccountService().getAccountBalance(request);
           if (0 == response.getErrorCode()) {
               System.out.println("Gas balance：" +         ToBaseUnit.ToGas(response.getResult().getBalance().toString()) + "Gas");
           }else {
               System.out.println(JsonUtils.toJSONString(response));
           }
        ```

#### Block相关接口

1. 获取当前块高度

    1. 接口 `getBlockNumber`

    1. 用途:

        获取当前链上最新的Block号

    1. 示例:

        ```java
           BIFBlockGetNumberResponse response = sdk.getBIFBlockService().getBlockNumber();
           System.out.println(JsonUtils.toJSONString(response));
        ```

1. 获取指定块内的交易列表

    1. 接口 `getTransactions(request)`

    1. 用途:

        给定block号,获取该block内的交易列表信息

    1. 示例:

        ```java
           // 初始化参数
           Long blockNumber = 1L;
           BIFBlockGetTransactionsRequest request = new BIFBlockGetTransactionsRequest();
              request.setBlockNumber(blockNumber);
           BIFBlockGetTransactionsResponse response = sdk.getBIFBlockService().getTransactions(request);
              if (0 == response.getErrorCode()) {
                  System.out.println(JsonUtils.toJSONString(response.getResult()));
              } else {
                  System.out.println(JsonUtils.toJSONString(response));
              }
        ```

1. 获取指定块的统计信息

    1. 接口 `getBlockInfo(request)`

    1. 用途:

        给定block号, 查询指定block的信息

    1. 示例:

        ```java
           // 初始化参数
           BIFBlockGetInfoRequest blockGetInfoRequest = new BIFBlockGetInfoRequest();
              blockGetInfoRequest.setBlockNumber(10L);
           BIFBlockGetInfoResponse lockGetInfoResponse =   sdk.getBIFBlockService().getBlockInfo(blockGetInfoRequest);
           if (lockGetInfoResponse.getErrorCode() == 0) {
               BIFBlockGetInfoResult lockGetInfoResult = lockGetInfoResponse.getResult();
               System.out.println(JsonUtils.toJSONString(lockGetInfoResult));
           } else {
               System.out.println(JsonUtils.toJSONString(lockGetInfoResponse));
           }
        ```

1. 查询最新块的信息

    1. 接口 `getBlockLatestInfo`

    1. 用途:

        获取当前最新块的信息.

    1. 示例:

        ```java
           // 初始化参数
           BIFBlockGetLatestInfoResponse lockGetLatestInfoResponse =         sdk.getBIFBlockService().getBlockLatestInfo();
           if (lockGetLatestInfoResponse.getErrorCode() == 0) {
               BIFBlockGetLatestInfoResult lockGetLatestInfoResult = lockGetLatestInfoResponse.getResult();
               System.out.println(JsonUtils.toJSONString(lockGetLatestInfoResult));
           } else {
               System.out.println(JsonUtils.toJSONString(lockGetLatestInfoResponse));
           }
        ```

#### Transaction相关接口

1. 获取指定交易相关信息

    1. 接口 `getTransactionInfo`

    1. 用途:

        获取指定交易的详细信息

    1. 示例:

        ```java
           // 初始化参数
           BIFTransactionGetInfoRequest request = new BIFTransactionGetInfoRequest();
           request.setHash("8f3d53f0dfb5ae652d6ed93ca9512f57c2203fe0ffefdc7649908945ad96a730");
           BIFTransactionGetInfoResponse response = sdk.getBIFTransactionService().getTransactionInfo(request);
           if (response.getErrorCode() == 0) {
               System.out.println(JsonUtils.toJSONString(response.getResult()));
           } else {
               System.out.println(JsonUtils.toJSONString(response));
           }
        ```


1. 提交交易

    1. 接口 `BIFSubmit`

    1. 用途:

        提交交易到星火链网

    1. 示例:

        ```java
           // 初始化参数
           String senderPrivateKey = "priSPKkWVk418PKAS66q4bsiE2c4dKuSSafZvNWyGGp2sJVtXL";
           //序列化交易
           String serialization ="";
           //签名
           byte[] signBytes = PrivateKeyManager.sign(HexFormat.hexToByte(serialization), senderPrivateKey);
           String publicKey = PrivateKeyManager.getEncPublicKey(senderPrivateKey);
           //提交交易
           BIFTransactionSubmitRequest submitRequest = new BIFTransactionSubmitRequest();
              submitRequest.setSerialization(serialization);
              submitRequest.setPublicKey(publicKey);
              submitRequest.setSignData(HexFormat.byteToHex(signBytes));
           // 调用bifSubmit接口
           BIFTransactionSubmitResponse response = sdk.getBIFTransactionService().BIFSubmit(submitRequest);
           if (response.getErrorCode() == 0) {
               System.out.println(JsonUtils.toJSONString(response.getResult()));
           } else {
               System.out.println("error: " + response.getErrorDesc());
           }
        ```

#### 合约相关接口

1. 部署合约

    1. 接口 `contractCreate`

    1. 用途:

        部署合约到星火链上

    1. 示例:

        ```java
            // 初始化参数
           String senderAddress = "did:bid:ef21AHDJWnFfYQ3Qs3kMxo64jD2KATwBz";
           String senderPrivateKey = "priSPKkL8XpxHiRLuNoxph2ThSbexeRUGEETprvuVHkxy2yBDp";
           String payload = "\"use strict\";function init(bar){/*init whatever you want*/return;}function main(input){let para = JSON.parse(input);if (para.do_foo)\n            {\n              let x = {\n                \'hello\' : \'world\'\n              };\n            }\n          }\n          \n          function query(input)\n          { \n            return input;\n          }\n        ";
           Long initBalance = ToBaseUnit.ToUGas("1");
        
           BIFContractCreateRequest request = new BIFContractCreateRequest();
              request.setSenderAddress(senderAddress);
              request.setPrivateKey(senderPrivateKey);
              request.setInitBalance(initBalance);
              request.setPayload(payload);
              request.setRemarks("create contract");
              request.setType(1);
              request.setFeeLimit(10000000000L);
        
           // 调用bifContractCreate接口
           BIFContractCreateResponse response = sdk.getBIFContractService().contractCreate(request);
           if (response.getErrorCode() == 0) {
               System.out.println(JsonUtils.toJSONString(response.getResult()));
           } else {
               System.out.println(JsonUtils.toJSONString(response));
           }
       ```

1. 从部署交易中获取合约地址

    1. 接口 `getContractAddress`

    1. 用途:

        提供部署合约的交易哈希, 返回合约地址

    1. 示例

        ```java
           // 初始化参数
           String hash = "ff6a9d1a0c0011fbb9f51cfb99e4cd5e7c31380046fda3fd6e0daae44d1d4648";
           BIFContractGetAddressRequest request = new BIFContractGetAddressRequest();
           request.setHash(hash);

           // Call getAddress
           BIFContractGetAddressResponse response = sdk.getBIFContractService().getContractAddress(request);
           if (response.getErrorCode() == 0) {
               System.out.println(JsonUtils.toJSONString(response.getResult()));
           } else {
                  System.out.println(JsonUtils.toJSONString(response));
           }
        ```

1. 获取合约相关信息

    1. 接口 `getContractInfo`

    1. 用途:

        指定合约地址, 获取合约相关信息

    1. 示例

        ```java
           //初始化参数
           BIFContractGetInfoRequest request = new BIFContractGetInfoRequest();
           request.setContractAddress("did:bid:efiBacNvVSnr5QxgB282XGWkg4RXLLxL");

           // Call getContractInfo
           BIFContractGetInfoResponse response = sdk.getBIFContractService().getContractInfo(request);
           if (response.getErrorCode() == 0) {
               System.out.println(JsonUtils.toJSONString(response.getResult()));
           } else {
               System.out.println(JsonUtils.toJSONString(response));
           }
        ```

1. 查询合约

    1. 接口 `contractQuery`

    1. 用途:

        调用合约Query接口, 查询合约数据

    1. 示例:

        ```java
           // 初始化参数
           // Contract address 合约地址
           String contractAddress = "did:bid:ef2gAT82SGdnhj87wQWb9suPKLbnk9NP";

           // Init request
           BIFContractCallRequest request = new BIFContractCallRequest();
           request.setContractAddress(contractAddress);

           // Call contractQuery
           BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
           if (response.getErrorCode() == 0) {
               BIFContractCallResult result = response.getResult();
               System.out.println(JsonUtils.toJSONString(result));
           } else {
               System.out.println(JsonUtils.toJSONString(response));
           }  
        ```

1. 调用合约

    1. 接口 `contractInvoke`

    1. 用途:

        在链上发出交易调用合约可写接口

    1. 示例:

        ```java
           // 初始化参数
           String senderAddress = "did:bid:efVmotQW28QDtQyupnKTFvpjKQYs5bxf";
           String contractAddress = "did:bid:ef2gAT82SGdnhj87wQWb9suPKLbnk9NP";
           String senderPrivateKey = "priSPKnDue7AJ42gt7acy4AVaobGJtM871r1eukZ2M6eeW5LxG";
           Long amount = 0L;
        
           BIFContractInvokeRequest request = new BIFContractInvokeRequest();
              request.setSenderAddress(senderAddress);
              request.setPrivateKey(senderPrivateKey);
              request.setContractAddress(contractAddress);
              request.setBIFAmount(amount);
              request.setRemarks("contract invoke");
        
           // 调用 bifContractInvoke 接口
           BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
           if (response.getErrorCode() == 0) {
               System.out.println(JsonUtils.toJSONString(response.getResult()));
           } else {
               System.out.println(JsonUtils.toJSONString(response));
           }
        ```
