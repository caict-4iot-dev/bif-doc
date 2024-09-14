# 2.Go SDK使用说明

## 2.1 简介

星火链网官方并没有提供Golang语言的SDK，开源社区的开发者贡献了基础版本的Golang语言SDK供大家使用，**官方建议优先选择Java或者Nodejs版本的SDK**。

## 2.2  环境准备

### 2.2.1 软件依赖

**golang** ： 版本为1.16或以上

下载地址：https://golang.org/dl/

若已安装，请通过命令查看版本：

```shell
$ go version
go version go1.16 linux/amd64
```

### 2.2.2 下载安装

```http
$ git clone -b main  --depth=1 http://github.com/caict-4iot-dev/BIF-Core-SDK-Go.git
```

## 2.3  怎么使用SDK

### 2.3.1 SDK 离线API

离线API主要是账户和密码学相关API, 不需要连接星火链网RPC接口也能工作. 主要接口如下:

#### 账户生成

1. 接口 ` key.GetBidAndKeyPair()`

1. 用途:

    用来生成一个星火链bid地址和对应私钥

1. 示例

    ```go
    import (
	"github.com/caict-4iot-dev/BIF-Core-SDK-Go/module/encryption/key"
    )
        
        keyPair, err := GetBidAndKeyPair()
        if err != nil {
            t.Error(err)
    	}
        encAddress := keyPair.GetEncAddress()
        encPublicKey := keyPair.GetEncPublicKey()
        encPrivateKey := keyPair.GetEncPrivateKey()
        rawPublicKey := keyPair.GetRawPublicKey()
        rawPrivateKey := keyPair.GetRawPrivateKey()
    ```


#### 加密私钥生成keystore

1. 接口 `key.GenerateKeyStore(encPrivateKey, password, n, r, p, version)`

1. 用途:

    用一个密码来加密保护私钥, 得到一个json表示的keystore, 对应密码不泄露的情况下, 可以公开保存.

1. 示例

    ```go
    import (
	"github.com/caict-4iot-dev/BIF-Core-SDK-Go/module/encryption/key"
    )
    
        encPrivateKey := "priSPKrR4w6H89kRXaC2XZT5Lmj7XoCoBdvTuv7ySXSCDDGaZZ"
	    password := "123456"
        n := 16384
        r := 8
        p := 1
        version := 32
        encPrivateKey, keyStore := key.GenerateKeyStore(encPrivateKey, password, n, r, p, version)
        dataByte, err := json.Marshal(keyStore)
        if err != nil {
            t.Error(err)
        }
        fmt.Println("encPrivateKey: ", encPrivateKey)
        fmt.Println("keyStore: ", string(dataByte))
    ```

### 2.3.2 SDK 在线API

在线API主要用于向星火链上发出交易和查询合约, 需要初始化SDK连接后使用.

#### 初始化SDK

示例

```go
 url := "http://test.bifcore.bitfactory.cn"
 sdk, err := GetInstance(url)  //SDK_INSTANCE_URL为星火链RPC地址
```

#### 账户处理接口

1. 查询账户信息

    1. 接口 `GetAccount(r request.BIFAccountGetInfoRequest) response.BIFAccountGetInfoResponse`

    1. 用途:

        用来获取一个账户当前信息

    1. 示例
        ```go
            as := GetAccountInstance(SDK_INSTANCE_URL)
            // 初始化请求参数
            accountAddress := "did:bid:ef21AHDJWnFfYQ3Qs3kMxo64jD2KATwBz"
            r := request.BIFAccountGetInfoRequest{
                Address: accountAddress,
    	    }
            res := as.GetAccount(r)
            if res.ErrorCode != 0 {
                t.Error(res.ErrorDesc)
            }
        
            dataByte, err := json.Marshal(res)
            if err != nil {
                t.Error(err)
            }
        
            fmt.Println("res: ", string(dataByte))
        ```

1. 获取账户nonce

    1. 接口 `GetNonce(r request.BIFAccountGetNonceRequest) response.BIFAccountGetNonceResponse`

    1. 用途:

        用来获取一个账户当前nonce值, 有关nonce含义, 请参照星火链开发基础章节.

    1. 示例:
        ```go
            as := GetAccountInstance(SDK_INSTANCE_URL)
            // 初始化请求参数
            accountAddress := "did:bid:ef21AHDJWnFfYQ3Qs3kMxo64jD2KATwBz"
            r := request.BIFAccountGetNonceRequest{
                Address: accountAddress,
            }
            res := as.GetNonce(r)
            if res.ErrorCode != 0 {
                t.Error(res.ErrorDesc)
            }
            
            dataByte, err := json.Marshal(res)
            if err != nil {
                t.Error(err)
            }
            
            fmt.Println("res: ", string(dataByte))
        ```

1. 获取账户余额

    1. 接口 `GetAccountBalance(r request.BIFAccountGetBalanceRequest) response.BIFAccountGetBalanceResponse`

    1. 用途:

        用来获取一个账户当前的XHT余额.

    1. 示例:

        ```go
            as := GetAccountInstance(SDK_INSTANCE_URL)
            // 初始化请求参数
            accountAddress := "did:bid:ef21AHDJWnFfYQ3Qs3kMxo64jD2KATwBz"
            r := request.BIFAccountGetBalanceRequest{
                Address: accountAddress,
            }
            res := as.GetAccountBalance(r)
            if res.ErrorCode != 0 {
                t.Error(res.ErrorDesc)
            }
            
            dataByte, err := json.Marshal(res)
            if err != nil {
                t.Error(err)
            }
            
            fmt.Println("res: ", string(dataByte))
        ```

#### Block相关接口

1. 获取当前块高度

    1. 接口 `GetBlockNumber() response.BIFBlockGetNumberResponse`

    1. 用途:

        获取当前链上最新的Block号

    1. 示例:

        ```go
            bs := GetBlockInstance(SDK_INSTANCE_URL)
            res := bs.GetBlockNumber()
            if res.ErrorCode != 0 {
                t.Error(res.ErrorDesc)
            }
            
            fmt.Println("blockNumber:", res.Result.Header.BlockNumber)
        ```

1. 获取指定块内的交易列表

    1. 接口 `GetTransactions(r request.BIFBlockGetTransactionsRequest) response.BIFBlockGetTransactionsResponse`

    1. 用途:

        给定block号,获取该block内的交易列表信息

    1. 示例:

        ```go
            bs := GetBlockInstance(SDK_INSTANCE_URL)
            var r request.BIFBlockGetTransactionsRequest
            r.BlockNumber = 617247
            res := bs.GetTransactions(r)
            if res.ErrorCode != 0 {
                t.Error(res.ErrorDesc)
            }
            
            fmt.Printf("result: %+v \n", res.Result)
        ```

1. 获取指定块的统计信息

    1. 接口 `GetBlockInfo(r request.BIFBlockGetInfoRequest) response.BIFBlockGetInfoResponse`

    1. 用途:

        给定block号, 查询指定block的信息.

    1. 示例:

        ```go
            bs := GetBlockInstance(SDK_INSTANCE_URL)
            var r request.BIFBlockGetInfoRequest
            r.BlockNumber = 617247
            res := bs.GetBlockInfo(r)
            if res.ErrorCode != 0 {
                t.Error(res.ErrorDesc)
            }
            
            fmt.Printf("result: %+v \n", res.Result)
        ```

1. 查询最新块的信息

    1. 接口 `GetBlockLatestInfo() response.BIFBlockGetLatestInfoResponse`

    1. 用途:

        获取当前最新块的信息.

    1. 示例:

        ```go
            bs := GetBlockInstance(SDK_INSTANCE_URL)
            res := bs.GetBlockLatestInfo()
            if res.ErrorCode != 0 {
                t.Error(res.ErrorDesc)
            }
            
            fmt.Printf("result: %+v \n", res.Result)
        ```

#### Transaction相关接口

1. 获取指定交易相关信息

    1. 接口 `GetTransactionInfo(r request.BIFTransactionGetInfoRequest) response.BIFTransactionGetInfoResponse`

    1. 用途:

        获取指定交易的详细信息

    1. 示例:

        ```go
            ts := GetTransactionInstance(SDK_INSTANCE_URL)
            var r request.BIFTransactionGetInfoRequest
            r.Hash = "2c0a445f603bdef7e4cfe5f63650f201cda3315b7c560edb79e3fcef611c5f8e"
            res := ts.GetTransactionInfo(r)
            if res.ErrorCode != 0 {
                t.Error(res.ErrorDesc)
            }
            
            dataByte, err := json.Marshal(res)
            if err != nil {
                t.Error(err)
            }
            
            fmt.Println("res: ", string(dataByte))
        ```


1. 提交交易

    1. 接口 `BIFSubmit(r request.BIFTransactionSubmitRequest) response.BIFTransactionSubmitResponse`

    1. 用途:

        提交交易到星火链

    1. 示例:

        ```go
            submitRequest := request.BIFTransactionSubmitRequest{
                Serialization: hex.EncodeToString(blob),
                SignData:      hex.EncodeToString(signData),
                PublicKey:     pubKey,
            }
            
            res := ts.BIFSubmit(submitRequest)
            if res.ErrorCode != 0 {
                t.Error(res.ErrorDesc)
            }
            
            dataByte, err = json.Marshal(res)
            if err != nil {
                t.Error(err)
            }
            
            fmt.Println("res: ", string(dataByte))
        ```

#### 合约相关接口

1. 部署合约

    1. 接口 `ContractCreate(r request.BIFContractCreateRequest) response.BIFContractCreateResponse`

    1. 用途:

        部署合约到星火链上

    1. 示例:

        ```go
            bs := GetContractInstance(SDK_INSTANCE_URL)
            var r request.BIFContractCreateRequest
            senderAddress := "did:bid:efzewQxg38x2Tmb1cpxSC1ZWwMZUxUeV"
            senderPrivateKey := "priSPKhTMRa7SsQLc4wXUDrEZW5wSeKN68Xy5LuCYQmndS75SZ"
            payload := "\"use strict\"; function init(bar){return;} function main(input){let para = JSON.parse(input);if(para.do_foo){let x = {'hello' : 'world'};}} function query(input){return input;}"
            r.SenderAddress = senderAddress
            r.PrivateKey = senderPrivateKey
            r.Metadata = "create contract"
            r.Payload = payload
            r.InitBalance = 1
            r.Type = 0
            r.InitBalance = 1
            r.FeeLimit = 10000000000
        
            res := bs.ContractCreate(r)
            if res.ErrorCode != 0 {
                t.Error(res.ErrorDesc)
            }
            
            dataByte, err := json.Marshal(res)
            if err != nil {
                t.Error(err)
            }
            
            fmt.Println("res: ", string(dataByte))
        ```

1. 从部署交易中获取合约地址

    1. 接口 `GetContractAddress(r request.BIFContractGetAddressRequest) response.BIFContractGetAddressResponse`

    1. 用途:

        提供部署合约的交易哈希, 返回合约地址

    1. 示例

        ```go
            bs := GetContractInstance(SDK_INSTANCE_URL)
            var r request.BIFContractGetAddressRequest
            r.Hash = "ff6a9d1a0c0011fbb9f51cfb99e4cd5e7c31380046fda3fd6e0daae44d1d4648"
            res := bs.GetContractAddress(r)
            if res.ErrorCode != 0 {
                t.Error(res.ErrorDesc)
            }
            
            dataByte, err := json.Marshal(res)
            if err != nil {
                t.Error(err)
            }
            
            fmt.Println("res: ", string(dataByte))
        ```

1. 获取合约相关信息

    1. 接口 `GetContractInfo(r request.BIFContractGetInfoRequest) response.BIFContractGetInfoResponse`

    1. 用途:

        指定合约地址, 获取合约相关信息.

    1. 示例

        ```go
            bs := GetContractInstance(SDK_INSTANCE_URL)
            var r request.BIFContractGetInfoRequest
            r.ContractAddress = "did:bid:efWVypEKTQoVTunsdBDw8rp4uoG5Lsy5"
            res := bs.GetContractInfo(r)
            if res.ErrorCode != 0 {
                t.Error(res.ErrorDesc)
            }
            
            dataByte, err := json.Marshal(res)
            if err != nil {
                t.Error(err)
            }
            
            fmt.Println("res: ", string(dataByte))
        ```

1. 查询合约

    1. 接口 `ContractQuery(r request.BIFContractCallRequest) response.BIFContractCallResponse`

    1. 用途:

        调用合约Query接口, 查询合约数据

    1. 示例:

        ```go
            bs := GetContractInstance(SDK_INSTANCE_URL)
            var r request.BIFContractCallRequest
            r.ContractAddress = "did:bid:efWVypEKTQoVTunsdBDw8rp4uoG5Lsy5"
            res := bs.ContractQuery(r)
            if res.ErrorCode != 0 {
                t.Error(res.ErrorDesc)
            }
    
            dataByte, err := json.Marshal(res)
            if err != nil {
                t.Error(err)
            }
            
            fmt.Println("res: ", string(dataByte))
        ```
    
1. 调用合约

    1. 接口 `ContractInvoke(r request.BIFContractInvokeRequest) response.BIFContractInvokeResponse`

    1. 用途:

        在链上发出交易调用合约可写接口

    1. 示例:

        ```go
            bs := GetContractInstance(SDK_INSTANCE_URL)
            var r request.BIFContractInvokeRequest
            senderAddress := "did:bid:efzewQxg38x2Tmb1cpxSC1ZWwMZUxUeV"
            contractAddress := "did:bid:efWVypEKTQoVTunsdBDw8rp4uoG5Lsy5"
            senderPrivateKey := "priSPKhTMRa7SsQLc4wXUDrEZW5wSeKN68Xy5LuCYQmndS75SZ"
            
            r.SenderAddress = senderAddress
            r.PrivateKey = senderPrivateKey
            r.ContractAddress = contractAddress
            r.BIFAmount = 1
            r.Metadata = "contract invoke"
    
            res := bs.ContractInvoke(r)
            if res.ErrorCode != 0 {
                t.Error(res.ErrorDesc)
            }
            
            dataByte, err := json.Marshal(res)
            if err != nil {
                t.Error(err)
            }
            
            fmt.Println("res: ", string(dataByte))
        ```
