# 3.BID-SDK

<a name="RPOky"></a>

**GitHub地址：[https://github.com/caict-4iot-dev/BID-SDK-JAVA](https://github.com/caict-4iot-dev/BID-SDK-JAVA)**

<a name="mzYWs"></a>

## 3.1 简介

2020年2月，中国信通院制定的`BID`方法被纳入`W3C`凭证社区工作组（`Credentials Community Group`）分布式标识（`DID`）规范。`BID`面向实体（包括人、物、组织）和数字对象，可用于拥有者证明其对`BID`的控制权及身份验证功能，而不需要依赖其他外部组织。`BID`标识目前应用于“星火链网”，由公钥经过一系列的算法后编码生成，支持`ed25519`、国密`sm2`、`secp256k1`等常用非对称加密算法生成的公钥；编码算法支持`base58`、 `base64`、`betch32`等常用的编码算法。BID实现了拥有者对标识的自我控制和管理，同时，通过密码学算法实现了隐私保护、安全可靠。

BID-SDK通过API调用的方式提供了“星火链网”公私钥对生成、“星火链网”私钥签名公钥验签、`BID`标识生成、`BID`标识验证等接口，同时还提供了接口使用示例说明，开发者可以调用该SDK方便快捷的生成星火链网公私钥对和`BID`地址，实现`BID`标识合法性的校验及主链的快速接入。中国信通院秉持开源开放的理念，将星火“BID-SDK”面向社区和公众完全开源，助力全行业伙伴提升数据价值流通的效率，实现数据价值转化。<a name="FQBXC"></a>

## 3.2 基本概念介绍

BID开发工具包，主要是为了方便开发者可以快速加入到星火主链的生态建设中，有以下功能：  

- 获取版本号：获取`BID-SDK`版本号。

- BID工具：生成`BID`标识和验证`BID`地址格式的合法性。  

- 公私钥工具：生成星火格式的公私钥、使用星火格式的私钥生成签名、使用星火格式的公钥生成签名。    

- BID标识工具：创建`BID`文档模板、创建`BID`文档、查询`BID`文档、校验`BID`文档。     

## 3.3 参考文档

参考文档：[《BID协议》](https://bid-resolution-protocol-doc.readthedocs.io/zh_CN/latest/)

## 3.4 离线API

### 3.4.1 获取版本号

1. 接口 ` getSdkVersion()`

1. 用途:

   用来获取BID-SDK版本号。

1. 示例

   ```java
       //创建SDK实例
       SDK sdk = new SDK();
       String sdkVersion= sdk.getSdkVersion();
       System.out.println(sdkVersion);
   ```

### 3.4.2 账户生成

1. 接口 ` getBidAndKeyPair()`

1. 用途:

   用来生成一个星火链`BID`地址和对应私钥。

1. 示例

   ```java
       //创建SDK实例
       SDK bidSdk = new SDK();
       KeyPairEntity kaypairEntity = bidSdk.getBidAndKeyPair();
       String publicKey = kaypairEntity.getEncPublicKey();
       String privateKey = kaypairEntity.getEncPrivateKey();
       String bid = kaypairEntity.getEncAddress();
       System.out.println(publicKey);
       System.out.println(privateKey);
       System.out.println(bid);
   ```

### 3.4.3 根据编码类型生成账户

1. 接口 ` getBidAndKeyPair(KeyType)`

1. 用途:

   根据编码类型生成一个星火链`BID`地址和对应私钥。

1. 示例

   ```java
       //创建SDK实例
       SDK bidSdk = new SDK();
       KeyPairEntity kaypairEntity = bidSdk.getBidAndKeyPair(KeyType.ED25519);
       String publicKey = kaypairEntity.getEncPublicKey();
       String privateKey = kaypairEntity.getEncPrivateKey();
       String bid = kaypairEntity.getEncAddress();
       System.out.println(publicKey);
       System.out.println(privateKey);
       System.out.println(bid);
   ```

### 3.4.4 根据编解码类型和ChainCode生成账户

1. 接口 ` getBidAndKeyPair(KeyType,chaincode)`

1. 用途:

   根据编解码类型和`ChainCode`生成星火链`BID`地址和对应私钥。

1. 示例

   ```java
       //创建SDK实例
       SDK bidSdk = new SDK();
       KeyPairEntity kaypairEntity = bidSdk.getBidAndKeyPair(KeyType.SM2,"aa1c" );
       String publicKey = kaypairEntity.getEncPublicKey();
       String privateKey = kaypairEntity.getEncPrivateKey();
       String bid = kaypairEntity.getEncAddress();
       System.out.println(publicKey);
       System.out.println(privateKey);
       System.out.println(bid);
   ```

## 3.5 在线API

### 3.5.1 获取BID文档模板

1. 接口 ` getBIDTemplate()`

1. 用途:

   用来获取一个星火链`BID`文档模板。

1. 示例

   ```java
       //创建SDK实例
       SDK bidSdk = new SDK();
       Result result = sdk.getBIDTemplate();
       System.out.println(result);
   ```

### 3.5.2 创建BID文档

1. 接口 ` createBIDByTemplate(bidDocument)`

1. 用途:

   根据星火链`BID`文档模板创建`BID`文档。

1. 示例

   ```java
        //bid文档
        String request ="{\"bifamount\":0,\"senderAddress\":\"did:bid:efZfEeQAE1jup1H9musAZP1S3PqV3UdF\",\"feeLimit\":1000000,\"BIFAmount\":0,\"bid\":[{\"document\":{\"version\":\"1.0.0\",\"id\":\"did:bid:efWH8wDnogNijNJWiaWJcZ33QSEF9beH\",\"publicKey\":[{\"id\":\"did:bid:efWH8wDnogNijNJWiaWJcZ33QSEF9beH#key-1\",\"type\":\"ED25519\",\"publicKeyHex\":\"b0656631627656f082b438a747164c2c9abbe5dd72a0582bdbf404e959c133b89b723e\",\"controller\":\"did:bid:efWH8wDnogNijNJWiaWJcZ33QSEF9beH\"}],\"authentication\":[\"did:bid:efZfEeQAE1jup1H9musAZP1S3PqV3UdF#key-1\"],\"alsoKnownAs\":[{\"id\":\"did:bid:efWH8wDnogNijNJWiaWJcZ33QSEF9beH\",\"type\":101}],\"extension\":{\"recovery\":[\"did:bid:efWH8wDnogNijNJWiaWJcZ33QSEF9beH#key-2\"],\"ttl\":86400,\"type\":102,\"delegateSign\":{\"signer\":\"did:bid:efWH8wDnogNijNJWiaWJcZ33QSEF9beH#key-1\",\"signatureValue\":\"A897845DAD953A68BCF22F31FC7EE2BB316EDA74D0BA5C02D99FF99981E610E50659D65EB2082D30312E91D677E7CFDAF3773155BBEE330E3C67412786E2BD01\"},\"attributes\":[{\"key\":\"name\",\"desc\":\"名称\",\"value\":\"BID文档\",\"format\":\"text\",\"encrypt\":1}],\"acsns\":[\"acsn\"],\"verifiableCredentials\":[{\"id\":\"did:bid:efWH8wDnogNijNJWiaWJcZ33QSEF9beH\",\"type\":201}]},\"service\":[{\"id\":\"did:bid:efWH8wDnogNijNJWiaWJcZ33QSEF9beH#resolver\",\"type\":\"DIDDecrypt\",\"protocol\":2,\"serverType\":0,\"serviceEndpoint\":\"https://bidresolver.com\"}],\"created\":\"2022-09-09T17:37:19Z\",\"updated\":\"2022-09-09T17:37:19Z\",\"proof\":{\"creator\":\"did:bid:efWH8wDnogNijNJWiaWJcZ33QSEF9beH#key-1\",\"signatureValue\":\"BCB3818AFC60C2121D88A6E6AF9B4FBD4F36931D27428DD72E149EF37E6E5A413787585E7E52BA32CCEA52AC3EB36664FCDAF8EBD02BC116F8875AFF00E28700\"},\"@context\":[\"https://www.w3.org/ns/did/v1\"]}},{\"document\":{\"version\":\"1.0.0\",\"id\":\"did:bid:efgeUN1NrZ8g8emyaxMrpH6yKZvTfar7\",\"publicKey\":[{\"id\":\"did:bid:efgeUN1NrZ8g8emyaxMrpH6yKZvTfar7#key-1\",\"type\":\"ED25519\",\"publicKeyHex\":\"b065668a2dd499847a0e4edec1560e7c10a2366b671a96011461fdcf1455d27e6b5d2a\",\"controller\":\"did:bid:efgeUN1NrZ8g8emyaxMrpH6yKZvTfar7\"}],\"authentication\":[\"did:bid:efZfEeQAE1jup1H9musAZP1S3PqV3UdF#key-1\"],\"alsoKnownAs\":[{\"id\":\"did:bid:efgeUN1NrZ8g8emyaxMrpH6yKZvTfar7\",\"type\":101}],\"extension\":{\"recovery\":[\"did:bid:efgeUN1NrZ8g8emyaxMrpH6yKZvTfar7#key-2\"],\"ttl\":86400,\"type\":102,\"delegateSign\":{\"signer\":\"did:bid:efgeUN1NrZ8g8emyaxMrpH6yKZvTfar7#key-1\",\"signatureValue\":\"DD3CCC07EDB286A4AEC2A2A63562A498C8582EDA3CE779425D86FE46D5F6774EF0831E9F03FCAA579882F20F21FCAD6616D62689D360AC8159F4414F112D2F09\"},\"attributes\":[{\"key\":\"name\",\"desc\":\"名称\",\"value\":\"BID文档\",\"format\":\"text\",\"encrypt\":1}],\"acsns\":[\"acsn\"],\"verifiableCredentials\":[{\"id\":\"did:bid:efgeUN1NrZ8g8emyaxMrpH6yKZvTfar7\",\"type\":201}]},\"service\":[{\"id\":\"did:bid:efgeUN1NrZ8g8emyaxMrpH6yKZvTfar7#resolver\",\"type\":\"DIDDecrypt\",\"protocol\":2,\"serverType\":0,\"serviceEndpoint\":\"https://bidresolver.com\"}],\"created\":\"2022-09-09T17:45:09Z\",\"updated\":\"2022-09-09T17:45:09Z\",\"proof\":{\"creator\":\"did:bid:efgeUN1NrZ8g8emyaxMrpH6yKZvTfar7#key-1\",\"signatureValue\":\"3A6C2D2601CA3A78EA3C736D3D5E93AFF194BF32CC45CE308AFC47854BDDD72A81776F88798B83D56E2770BFDFDBCC3A250D51CDB63C45E34773ED910C2F770F\"},\"@context\":[\"https://www.w3.org/ns/did/v1\"]}}],\"ceilLedgerSeq\":0,\"remarks\":\"creat DDO\",\"privateKey\":\"priSPKhJ59Y6EePWbFybWzNkhPGjJ1ReQBeFk3KgaC2nFz4Nfy\",\"gasPrice\":1000}";
        SDK sdk = SDK.getInstance("http://test.bifcore.bitfactory.cn/");
        Result result = sdk.createBIDByTemplate(request);
        System.out.println(result);
   ```

### 3.5.2 解析BID文档

1. 接口 `resolverBid(bid)`

1. 用途:

   用来查询`BID`文档。

1. 示例

   ```java
      //创建SDK实例
      SDK sdk = SDK.getInstance("http://test-bidresolver.bitfactory.cn");
      String bid="did:bid:efj3FikDU8c7An3SPUoRtEWf2JDg1Hg9";
      Result result = sdk.resolverBid(bid);
      System.out.println(result);
   ```
