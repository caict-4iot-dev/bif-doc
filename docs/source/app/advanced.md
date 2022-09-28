# 星火链进阶教程

## 1.nonce管理

星火链网底层区块链平台（下文简称星火链)作为“许可”公有链，拥有一部分的公有属性，使用星火令（类似于以太坊的gas）作为智能合约执行的消耗，同时不同账户之间可以通过交易相互转移星火令，星火链的账户模型设计了连续递增的`nonce`值的方式来防止出现重放攻击。

同一账户的发送的交易需要保证`nonce`值的连续递增，否则交易会因为`nonce`值太小或者太大导致失败。我们推荐用户使用多个已激活的账号做为账号池，随机使用某一未被加锁账号进行交易，交易完成时释放该账号锁，这样可以保证上链交易的成功率和性能。

### 具体方案

<img src="../_static/images/image-20220704175507796.png" alt="image-20220704175507796.png" style="zoom:80%;" />



### 分布式锁之Redisson

使用Redisson框架实现分布式锁。

#### 1.1 加入jar包依赖

```java
<dependency>
   <groupId>org.redisson</groupId>
   <artifactId>redisson</artifactId>
   <version>3.11.0</version>
</dependency>
```

#### 1.2 配置Redisson

```java
public class RedissonManager {
    private static Config config = new Config();
    //声明redisso对象
    private static Redisson redisson = null;
   //实例化redisson
 static{
     config.useSingleServer().setAddress("redis://127.0.0.1:6379");
   //得到redisson对象
 redisson = (Redisson) Redisson.create(config);

}

 //获取redisson对象的方法
    public static Redisson getRedisson(){
 return redisson;
    }
}
```

#### 1.3 锁的获取和释放

```java
public class RedissonLock {
    //从配置类中获取redisson对象
    private static Redisson redisson = RedissonManager.getRedisson();
    private static final String LOCK_TITLE = "redisLock_";
    //加锁
    public static boolean acquire(String lockName){
 //声明key对象
 String key = LOCK_TITLE + lockName;
 //获取锁对象
 RLock mylock = redisson.getLock(key);
 //加锁，并且设置锁过期时间，防止死锁的产生
 mylock.lock(2, TimeUnit.MINUTES);
 System.err.println("======lock======"+Thread.currentThread().getName());
 //加锁成功
 return  true;
    }
    //锁的释放
    public static void release(String lockName){
 //必须是和加锁时的同一个key
 String key = LOCK_TITLE + lockName;
 //获取所对象
 RLock mylock = redisson.getLock(key);
 //释放锁（解锁）
 mylock.unlock();
 System.err.println("======unlock======"+Thread.currentThread().getName());
    }
}
```

#### 1.4 模拟获取分布式锁

```java

/**
 * 获取分布式锁
 */
public class TransactionDemo {
    private static BIFSDK sdk = BIFSDK.getInstance(SampleConstant.SDK_INSTANCE_URL);
    private static Redisson redisson = RedissonManager.getRedisson();

    public static void main(String[] args) {

 //参数
 String senderAddress1="did:bid:efLrPu7LNR4YwA5M1Kfx6BYb1JP7aPKp";
 String senderPrivateKey1="priSPKteVqGoNgtKE68ZjNHAbGJsNvV9nTBkTLMYTGhVjsBY5R";

 String senderAddress2="did:bid:efBdagu8sVkJWEw5kLt1w69bxa85Kuag";
 String senderPrivateKey2="priSPKmCQMrjCcRgV3u2VsYhujf7QsG7Kr6Tgm94AbzCge46d8";
 //账号集合
 List<String> availableAccAddr = new ArrayList<String>();
 availableAccAddr.add(senderAddress1+";"+senderPrivateKey1);
 availableAccAddr.add(senderAddress2+";"+senderPrivateKey2);
 //目的地址
 String destAddress="did:bid:efnVUgqQFfYeu97ABf6sGm3WFtVXHZB2";
 Long feeLimit=1000000L;
 Long gasPrice=100L;
 //交易对象
 BIFGasSendOperation gasSendOperation= new BIFGasSendOperation();
 gasSendOperation.setAmount(1L);
 gasSendOperation.setDestAddress(destAddress);
 while (true) {
     try {
  Thread.sleep(1000);
  new transaction(availableAccAddr,feeLimit,gasPrice,0,gasSendOperation).start();
     }catch (Exception e) {
  e.printStackTrace();
  break;
     }
 }
 System.out.println("END");
    }

    static class transaction extends Thread{
 List<String> availableAccAddr;
 Long feeLimit;
 Long gasPrice;
 BIFBaseOperation operation;
 Integer domainId;
 public transaction(List<String> availableAccAddr,Long feeLimit,Long gasPrice,Integer domainId,BIFBaseOperation operation ) {
     this.availableAccAddr = availableAccAddr;
     this.feeLimit = feeLimit;
     this.gasPrice = gasPrice;
     this.domainId = domainId;
     this.operation = operation;
 }

 @Override
 public void run() {
     //随机获取交易账号
     int index = new Random().nextInt(availableAccAddr.size());
     String senderAddress=availableAccAddr.get(index).split(";")[0];
     String senderPrivateKey=availableAccAddr.get(index).split(";")[1];
     //加锁
     RedissonLock.acquire(senderAddress);
     System.out.println("线程"+ Thread.currentThread().getName() +"获得分布式锁:"+senderAddress);
     try {
  //获取账号nonce值
  Long nonce=0L;
  BIFAccountGetNonceRequest request = new BIFAccountGetNonceRequest();
  request.setAddress(senderAddress);
  RMap<Object, Object> redisHash = redisson.getMap(senderAddress);
  if(!redisHash.isEmpty()){
      //设置过期时间
      redisHash.expire(60, TimeUnit.SECONDS);
      nonce=Long.parseLong(redisHash.get("nonce").toString());
  }else{
      // 调用getNonce接口
      BIFAccountGetNonceResponse response = sdk.getBIFAccountService().getNonce(request);
      if (0 == response.getErrorCode()) {
   nonce=response.getResult().getNonce()+1;
      }
  }
  //序列化交易
  BIFTransactionSerializeRequest serializeRequest = new BIFTransactionSerializeRequest();
  serializeRequest.setSourceAddress(senderAddress);
  serializeRequest.setNonce(nonce);
  serializeRequest.setFeeLimit(feeLimit);
  serializeRequest.setGasPrice(gasPrice);
  serializeRequest.setOperation(operation);
  serializeRequest.setDomainId(domainId);
  // 调用buildBlob接口
  BIFTransactionSerializeResponse serializeResponse = sdk.getBIFTransactionService().BIFSerializable(serializeRequest);
  System.out.println("serializeResponse:"+ JsonUtils.toJSONString(serializeResponse.getResult()));
  if (!serializeResponse.getErrorCode().equals(Constant.SUCCESS)) {
      throw new SDKException(serializeResponse.getErrorCode(), serializeResponse.getErrorDesc());
  }
  String transactionBlob = serializeResponse.getResult().getTransactionBlob();
  System.out.println("transactionBlob:"+transactionBlob);
  //签名交易
  byte[] signBytes = PrivateKeyManager.sign(HexFormat.hexToByte(transactionBlob), senderPrivateKey);
  String publicKey = PrivateKeyManager.getEncPublicKey(senderPrivateKey);
  //提交交易
  BIFTransactionSubmitRequest submitRequest = new BIFTransactionSubmitRequest();
  submitRequest.setSerialization(transactionBlob);
  submitRequest.setPublicKey(publicKey);
  submitRequest.setSignData(HexFormat.byteToHex(signBytes));
  // 调用bifSubmit接口
  BIFTransactionSubmitResponse transactionSubmitResponse = sdk.getBIFTransactionService().BIFSubmit(submitRequest);
  if (transactionSubmitResponse.getErrorCode() == 0) {
      System.out.println(senderAddress+ " ,hash: "+transactionSubmitResponse.getResult().getHash());

      BIFTransactionGetInfoRequest requestHash = new BIFTransactionGetInfoRequest();
      requestHash.setHash(transactionSubmitResponse.getResult().getHash());
      BIFTransactionGetInfoResponse response = sdk.getBIFTransactionService().getTransactionInfo(requestHash);
      int num=0;
      while (response.getErrorCode() != 0) {
   try{
       Thread.sleep(1000);
       response= sdk.getBIFTransactionService().getTransactionInfo(requestHash);
       num++;
       System.out.println("num    "+num);
       if(num>=120){
    break;
       }
   }catch (Exception e) {
       e.printStackTrace();
   }
      }
      while (response.getErrorCode() != 0) {
   try{
       Thread.sleep(300000);
       BIFTransactionCacheRequest cacheRequest=new BIFTransactionCacheRequest();
       cacheRequest.setHash(transactionSubmitResponse.getResult().getHash());
       BIFTransactionCacheResponse responseTxCacheDataHash = sdk.getBIFTransactionService().getTxCacheData(cacheRequest);
       if (responseTxCacheDataHash.getErrorCode() != 0) {
    response= sdk.getBIFTransactionService().getTransactionInfo(requestHash);
    if(response.getErrorCode()!=0){
        break;
    }
       }
   }catch (Exception e) {
       e.printStackTrace();
   }
      }
      if(response.getErrorCode() == 99){ //99：nonce值过小
   // 调用getNonce接口
   BIFAccountGetNonceResponse  nonceResponse = sdk.getBIFAccountService().getNonce(request);
   if (0 == nonceResponse.getErrorCode()) {
       nonce=nonceResponse.getResult().getNonce();
   }
      }
      //更新nonce值
      nonce=nonce+1;
      redisHash.put("nonce",Long.toString(nonce));
      RedissonLock.release(senderAddress);
      System.out.println("线程"+Thread.currentThread().getName()+"释放分布式锁");
  }
     } catch (Exception e) {
  e.printStackTrace();
     }
 }
    }
}

```

## 2.账号权限管理

场景说明：账号A可授权账号B权利值，通过设定权利值可限制账号B的交易权限，账号B可替账号A完成交易操作。

该操作用于设置账户权限。包括签名者权重列表、交易门限、指定类型交易门限。

```json
"source_address": "adxSn8xpL7c2xkxwbreVCs6EZ7KZbBvtDaLtV",//操作源账户，即操作的执行方--账号A
"set_privilege": {
 "master_weight": "10",//可选，当前账户的自身权力值
 "signers"://可选，需要操作的签名者列表
 [
   {
     "address": "adxSj9kGyXR2YpyxwZVMrnGcLWoG3Hf9qXne8",//需要操作的签名者地址,--账号B
     "weight": 8 //可选，签名者的权力值
   }
 ],
 "tx_threshold": "2",//可选，发起交易需要权力值
 "type_thresholds"://可选，不同操作需要的权力值
 [
   {
     "type": 1,//创建账户操作类型
     "threshold": 8 //可选，该操作需要的权力值
   },
   {
     "type": 2,//发行资产操作类型
     "threshold": 9 //可选该操作需要的权力值
   }
 ]
      }
```

### 初始化SDK

```java
import cn.bif.api.BIFSDK;

BIFSDK sdk = BIFSDK.getInstance("http://test.bifcore.bitfactory.cn");   //星火链测试网RPC地址
```

### 设置账号权限

```java
 // 初始化参数
 String senderAddress = "did:bid:zf2bbxDwdzm4g4fJNTH2ah6gbHu6PdAX2";
 String senderPrivateKey = "priSrrfxxMAvnify3iRtTEW2zy87qo4N4B2gwhXSN4WFbXFJUs";
 String masterWeight = "";
 BIFSigner[] signers = new BIFSigner[1];
 BIFSigner s=new BIFSigner();
 s.setAddress("did:bid:efAsXt5zM2Hsq6wCYRMZBS5Q9HvG2EmK");
 s.setWeight(8L);
 signers[0]=s;

 String txThreshold = "2";
 BIFTypeThreshold[] typeThresholds = new BIFTypeThreshold[1];
 BIFTypeThreshold d=new BIFTypeThreshold();
 d.setThreshold(8L);
 d.setType(1);
 typeThresholds[0]=d;

 BIFAccountSetPrivilegeRequest request = new BIFAccountSetPrivilegeRequest();
 request.setSenderAddress(senderAddress);
 request.setPrivateKey(senderPrivateKey);
 request.setSigners(signers);
 request.setTxThreshold(txThreshold);
 request.setMasterWeight(masterWeight);
 request.setTypeThresholds(typeThresholds);
 request.setRemarks("set privilege");
      
 // 调用 setPrivilege 接口
 BIFAccountSetPrivilegeResponse response = sdk.getBIFAccountService().setPrivilege(request);
 if (response.getErrorCode() == 0) {
     System.out.println(JsonUtils.toJSONString(response.getResult()));
 } else {
     System.out.println(JsonUtils.toJSONString(response));
 }

```

### 查询账号权限

```java
 // 初始化请求参数
 String accountAddress = "did:bid:zf2bbxDwdzm4g4fJNTH2ah6gbHu6PdAX2";
 BIFAccountPrivRequest request = new BIFAccountPrivRequest();
 request.setAddress(accountAddress);
      
 // 调用getAccountPriv接口
 BIFAccountPrivResponse response = sdk.getBIFAccountService().getAccountPriv(request);

 if (response.getErrorCode() == 0) {
     BIFAccountPrivResult result = response.getResult();
     System.out.println(JsonUtils.toJSONString(result));
 } else {
     System.out.println(JsonUtils.toJSONString(response));
 }
```

## 3.合约批量调用

场景说明：用户处理事件过程中涉及多个合约调用、同一合约多次调用时，可使用该接口，保证事务的一致性，同时可减少交易次数，节省交易费用。

该操作用于转移星火令并触发合约。

### 示例

```java
 // 初始化参数
 String senderAddress = "did:bid:ef7zyvBtyg22NC4qDHwehMJxeqw6Mmrh";
 String contractAddress = "did:bid:eftzENB3YsWymQnvsLyF4T2ENzjgEg41";
 String senderPrivateKey = "priSPKr2dgZTCNj1mGkDYyhyZbCQhEzjQm7aEAnfVaqGmXsW2x";
 Long amount = 0L;
 String destAddress1 = KeyPairEntity.getBidAndKeyPair().getEncAddress();
 String destAddress2 = KeyPairEntity.getBidAndKeyPair().getEncAddress();
 String input1 = "{\"method\":\"creation\",\"params\":{\"document\":{\"@context\": [\"https://w3.org/ns/did/v1\"],\"context\": \"https://w3id.org/did/v1\"," +
  "\"id\": \""+destAddress1+"\", \"version\": \"1\"}}}";
 String input2 = "{\"method\":\"creation\",\"params\":{\"document\":{\"@context\": [\"https://w3.org/ns/did/v1\"],\"context\": \"https://w3id.org/did/v1\"," +
  "\"id\": \""+destAddress2+"\", \"version\": \"1\"}}}";

 List<BIFContractInvokeOperation> operations = new ArrayList<BIFContractInvokeOperation>();
 //操作对象1
 BIFContractInvokeOperation operation1=new BIFContractInvokeOperation();
 operation1.setContractAddress(contractAddress);
 operation1.setBIFAmount(amount);
 operation1.setInput(input1);
 //操作对象2
 BIFContractInvokeOperation operation2=new BIFContractInvokeOperation();
 operation2.setContractAddress(contractAddress);
 operation2.setBIFAmount(amount);
 operation2.setInput(input2);

 operations.add(operation1);
 operations.add(operation2);

 BIFBatchContractInvokeRequest request = new BIFBatchContractInvokeRequest();
 request.setSenderAddress(senderAddress);
 request.setPrivateKey(senderPrivateKey);
 request.setOperations(operations);
 request.setRemarks("contract invoke");

 // 调用 bifContractInvoke 接口
 BIFContractInvokeResponse response = sdk.getBIFContractService().batchContractInvoke(request);
 if (response.getErrorCode() == 0) {
     System.out.println(JsonUtils.toJSONString(response.getResult()));
 } else {
     System.out.println(JsonUtils.toJSONString(response));
 }
```

## 4.交易回执

交易回执结构如下：

```json
{
                "actual_fee": 776000, //交易实际花费的费用
                "close_time": 1664352470872350, //交易执行完成的时间
                "error_code": 0, //交易的错误码，0表示交易执行成功，非0表示交易执行失败
                "error_desc": "", //交易的错误描述
                "hash": "0f3477d3a6708168ce7f694a7eaf87129f7373548be0b085d3422809c03ea8d1", //交易hash值
                "ledger_seq": 932290, //交易所在的区块高度
                "signatures": [ //签名列表
                    {
                        "public_key": "b0656670063fd619ae607e39187477eabb70f45a657879af8c7dfe1c0dbb105dbccf23",//公钥
                        "sign_data": "2c212c987688c176e8b444b0e7f977d8c290ccf88a29305aadac2b693ce983827b46842e403703fd0456e23b6121cb242b1610f1926421577ee6714950dd4900" //签名数据
                    }
                ],
                "transaction": { //交易内容，交易类型包括：创建账号/合约、合约调用、星火令转移、设置metadata、设置权限、记录日志
                    .....
                },
                "tx_size": 776 //交易字节数
            }
```

### 4.1 创建账号

```json
{
  "source_address":"adxSn8xpL7c2xkxwbreVCs6EZ7KZbBvtDaLtV",//交易源账号，即交易的发起方
  "nonce":2, //交易源账户的nonce值
  "fee_limit" : 1000000, //愿为交易花费的手续费
  "gas_price": 1000,//gas价格(不小于配置的最低值)
  "ceil_ledger_seq": 100, //可选，区块高度限制, 如果大于0，则交易只有在该区块高度之前（包括该高度）才有效
  "metadata":"0123456789abcdef", //可选，用户自定义给交易的备注，16进制格式
  "operations":[
    {
      "type": 1, // 创建账户操作类型
      "source_address": "adxSn8xpL7c2xkxwbreVCs6EZ7KZbBvtDaLtV",//可选，操作源账户，即操作的执行方
      "metadata": "0123456789abcdef",//可选，用户自定义给交易的备注，16进制格式
      "create_account": {
        "dest_address": "adxSgCwYLWoCZnP6s2WXtQCwhxuFxhvsr375z",//待创建的目标账户地址
        "init_balance": 100000,//目标账户的初始化余额
        "priv":  {
          "master_weight": 1,//目标账户拥有的权力值
          "thresholds": {
            "tx_threshold": 1//发起交易需要的权力值
          }
        }
      }
    }
  ]
}
```

### 4.2 创建合约

```json
{
  "source_address":"adxSn8xpL7c2xkxwbreVCs6EZ7KZbBvtDaLtV",//交易源账号，即交易的发起方
  "nonce":2, //交易源账户的nonce值
  "fee_limit" : 1000000, //愿为交易花费的手续费
  "gas_price": 1000,//gas价格(不小于配置的最低值)
  "ceil_ledger_seq": 100, //可选，区块高度限制, 如果大于0，则交易只有在该区块高度之前（包括该高度）才有效
  "metadata":"0123456789abcdef", //可选，用户自定义给交易的备注，16进制格式
  "operations":[
    {
      "type": 1, // 创建账户操作类型
      "source_address": "adxSn8xpL7c2xkxwbreVCs6EZ7KZbBvtDaLtV",//可选，操作源账户，即操作的执行方
      "metadata": "0123456789abcdef",//可选，用户自定义给交易的备注，16进制格式
      "create_account": {
        "contract": { //合约
          "payload": "
                 'use strict';
                 function init(bar)
                 {
                   return;
                 }

                 function main(input)
                 {
                   return;
                 }

                 function query()
                 {
                   return;
                 }
                 "//合约代码
        },
        "init_balance": 100000,  //合约账户初始化资产
        "init_input" : "{\"method\":\"toWen\",\"params\":{\"feeType\":0}}",//可选，合约代码init函数的入参
        "priv": {
          "master_weight": 0,//待创建的合约账户拥有的权力值
          "thresholds": {
            "tx_threshold": 1 //发起交易需要的权力值
          }
        }
      }
    }
  ]
}
```

### 4.3合约调用

```js
{
    "source_address": "did:bid:ef27dchGWy9WY5xVznyPScZ6MP5CATsJF",//交易源账号，即交易的发起方
    "fee_limit": 200000000,//愿为交易花费的手续费
    "gas_price": 200,//gas价格(不小于配置的最低值)
    "nonce": 111028, //交易源账户的nonce值
    "operations": [
      {
        "type": 7,//合约调用类型
        "pay_coin": {
          "dest_address": "did:bid:efMTBwMHE7audr53KyZK5cjw3ysZUXPF", //合约地址
          "input": "{\"function\":\"safeTransferFrom(address,address,string)\",\"args\":\"did:bid:ef27dchGWy9WY5xVznyPScZ6MP5CATsJF,did:bid:efdcPDsvv2RnMwAt5D1PYxMtbGvW8JjT,\u0027did:bid:efdudDHcUc4EXUyW2hTCP9JtRxfiRsDB\u0027\"}" //合约调用方法
        }
      }
    ]
}
```

### 4.4 星火令转移

```json
{
  "fee_limit": 10253000,//愿为交易花费的手续费
  "gas_price": 1000,//gas价格(不小于配置的最低值)
  "nonce": 110, //交易源账户的nonce值
  "operations": [
    {
      "pay_coin": {
        "amount": 1000000000, //转账金额
        "dest_address": "did:bid:ef3LqNzb4ssNf2vqwNwBfqngrA3Sx8yD" //目的地址
      },
      "type": 7// 交易操作类型
    }
  ],
  "source_address": "did:bid:ef249EXxmYEuvazPM5Qr77H5xN18Zba3f"//交易源账号，即交易的发起方
}
```



### 4.5 设置metadata

```json
{
  "source_address":"adxSn8xpL7c2xkxwbreVCs6EZ7KZbBvtDaLtV",//交易源账号，即交易的发起方
  "nonce":2, //交易源账户的nonce值
  "fee_limit" : 1000000, //愿为交易花费的手续费
  "gas_price": 1000,//gas价格(不小于配置的最低值)
  "ceil_ledger_seq": 100,//可选，区块高度限制, 如果大于0，则交易只有在该区块高度之前（包括该高度）才有效
  "metadata":"0123456789abcdef",//可选，用户自定义给交易的备注，16进制格式
  "operations":[
    {
      "type": 4,//设置 metadata 操作类型
      "source_address": "adxSn8xpL7c2xkxwbreVCs6EZ7KZbBvtDaLtV",//可选，操作源账户，即操作的执行方
      "metadata": "0123456789abcdef",//可选，用户自定义给交易的备注，16进制格式
      "set_metadata": {
        "key": "abc",//metadata关键字
        "value": "hello abc!",//metadata内容
        "version": 0 //可选，metadata版本号
      }
    }
  ]
}
```

### 4.6 设置权限

```json
{
  "source_address":"adxSn8xpL7c2xkxwbreVCs6EZ7KZbBvtDaLtV",//交易源账号，即交易的发起方
  "nonce":2, //交易源账户的nonce值
  "fee_limit" : 1000000, //愿为交易花费的手续费
  "gas_price": 1000,//gas价格(不小于配置的最低值)
  "ceil_ledger_seq": 100,//可选，区块高度限制, 如果大于0，则交易只有在该区块高度之前（包括该高度）才有效
  "metadata":"0123456789abcdef",//可选，用户自定义给交易的备注，16进制格式
  "operations":[
    {
      "type": 9,//设置权限操作类型
      "source_address": "adxSn8xpL7c2xkxwbreVCs6EZ7KZbBvtDaLtV",//可选，操作源账户，即操作的执行方
      "metadata": "0123456789abcdef",//可选，用户自定义给交易的备注，16进制格式
      "set_privilege": {
        "master_weight": "10",//可选，当前账户的自身权力值
        "signers"://可选，需要操作的签名者列表
        [
          {
            "address": "adxSj9kGyXR2YpyxwZVMrnGcLWoG3Hf9qXne8",//需要操作的签名者地址
            "weight": 8 //可选，签名者的权力值
          }
        ],
        "tx_threshold": "2",//可选，发起交易需要权力值
        "type_thresholds"://可选，不同操作需要的权力值
        [
          {
            "type": 1,//创建账户操作类型
            "threshold": 8 //可选，该操作需要的权力值
          },
          {
            "type": 2,//发行资产操作类型
            "threshold": 9 //可选该操作需要的权力值
          }
        ]
      }
    }
  ]
}
```

### 4.7 记录日志

```json
{
  "transaction": {
    "nonce": 511546,
    "operations": [
      {
        "log": {
          "datas": [
            "{\"data\":\"\",\"topics\":[\"ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef\",\"00000000000000006566ee21773c3a96a1440a669dee46e40ca3b1d28caa5e70\",\"0000000000000000656686e34bc4e3a92a07cf162c463518a9491f0c4ad56aca\",\"0000000000000000000000000000000000000000000000000000000000061131\"]}"
          ],//日志内容
          "topic": "evmLog_dced48d56925087f9883d7d9b66e71f8ea93681adc4b0d8a64771928202f74a0"// 日志主题
        },
        "type": 8 //记录日志操作类型
      }
    ],
    "source_address": "did:bid:efMTBwMHE7audr53KyZK5cjw3ysZUXPF"
  }
}   
```

