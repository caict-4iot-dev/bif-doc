# 星火链开发文档

## 概述

### 什么是星火链

星火·链网-底层区块链平台(BIF-Core)，简称星火链，是中国信息通信研究院基于区块链技术打造的一条许可公有链，是实现“星火·链网”这一国家级区块链与工业互联网协同创新新型基础设施的关键技术.

1. 星火链与联盟链的区别

不同于联盟链,星火链的链上交易需要耗费星火令(XHT),

1. 星火链与比特币,以太坊的区别

星火链采取准入制

### 星火链应用开发须知

1. 星火令XHT

    星火链是星火链的基础单位, 在星火链上发起的交易都需要耗费星火令. 

1. 星火链智能合约

    智能合约指的是部署在区块链上自动执行的代码逻辑，开发者能够利用星火链支持的编程语言，开发一个商业级别的智能合约.
    
    星火链智能合约存储在区块链中，分布在每一个节点上，用户通过交易去触发合约脚本的执行，并把执行的结果写入到区块链中，并通过底层共识功能保证所有数据的一致性.
    
    目前星火链支持javascript, solidity两种语言的智能合约,C++智能合约支持正在研发中.

1. 星火链SDK

    星火链提供了基于多种语言的SDK https://github.com/CAICT-DEV/BIF-Core-SDK, 用来方便开发者程序与链上交互.SDK提供功能包括:

    * 创建账户
    * 查询指定账户的信息
    * 查询交易信息
    * 部署合约
    * 发出交易调用合约,以及查询合约

1. 星火链浏览器

    星火链浏览器提供了对账户, 交易, 合约的查询和跟踪等功能, 可以节省开发者的大量时间和精力. 目前星火链测试网的浏览器地址为: 

    * 主网
    * 测试网: http://test-explorer.bitfactory.cn/ 

1. 星火链RPC地址

    * 主网:
    * 测试网: http://test.bifcore.bitfactory.cn

## 快速上手

接下来以Java SDK为例, 指导开发者在星火链测试网上部署, 调用和查询一个简单的智能合约.

1. 账号创建

    ```

    import cn.bif.model.crypto.KeyPairEntity;

    entity = KeyPairEntity.getBidAndKeyPair();                             //离线创建一个新账号
    System.out.printf("public BID %s\n", entity.getEncAddress());          //账户地址, 可以公开
    System.out.printf("private key %s\n", entity.getEncPrivateKey());      //账户私钥, 请妥善保管
    ```

1. 获取星火令

    测试网星火链可以通过**待定???**获取, 

1. 初始化星火链SDK

    通过配置星火链RPC地址连接SDK到星火链.

    ```
    import cn.bif.api.BIFSDK;

    public static final String NODE_URL = "http://test.bifcore.bitfactory.cn";  //星火链测试网RPC地址

    public staitc BIFSDK sdk = BIFSDK.getInstance(NODE_URL);
    ```

1. 查看账户状态

    ```
    BIFAccountGetInfoRequest infoReq = new BIFAccountGetInfoRequest();
    infoReq.setAddress(publicKey);                                        //要查看账户的地址

    BIFAccountGetInfoResponse infoRsp = sdk.getBIFAccountService().getAccount(infoReq);

    if (infoRsp.getErrorCode() == 0) {
        System.out.println(JsonUtils.toJSONString(infoRsp.getResult()));  //查询失败
    } else {
        System.out.println(infoRsp.getErrorDesc());                       //
    }
    ```

    注意, 新创建的账户查询会失败, 因为没有任何转入转出的交易记录. 成功获取星火令后, 查询账户状态返回应该是:

    ```
    {
        "address":"did:bid:efKkF5uKsopAishxkYja4ULRJhrhrJQU",    //账户地址
        "balance":10000000000,                                   //账户余额
        "nonce":0                                                //账户发出的交易计数
    }
    ```

1. 合约部署

    * 合约代码

        合约开发资料可以参见高级话题部分,这里先用一个示例的javascript合约代码:

        javascript
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

        该合约实现了一个简单的存储功能, 用户可以按照任意key存入和读取数据.

    * 合约部署

        合约编写完毕后, 需要将合约部署到链上, **注意这里需要账户内有足够的XHT**, 部署示例代码如下:

        ```
        //部署合约

        //合约代码，注意转义
        String contractCode = "\"use strict\";function queryById(id) {    let data = Chain.load(id);    return data;}function query(input) {    input = JSON.parse(input);    let id = input.id;    let object = queryById(id);    return object;}function main(input) {    input = JSON.parse(input);    Chain.store(input.id, input.data);}function init(input) {    return;}";

        BIFContractCreateRequest createCReq = new BIFContractCreateRequest();

        //创建方地址和私钥
        createCReq.setSenderAddress(publicKey);
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
            System.out.println(createCRsp.getErrorDesc());
        }
        ```

        如果部署成功, 调用返回里会拿到这个交易的HASH.

        ```
        {
            "hash":"b25567a482e674d79ac5f9b5f6601f27b676dde90a6a56539053ec882a99854f"
        }
        ```

    * 交易信息和合约地址查询

        用SDK查询交易详细信息, 并且可以从中获取到刚创建的合约地址.

        ```
        BIFContractGetAddressRequest cAddrReq = new BIFContractGetAddressRequest();
        cAddrReq.setHash(cTxHash);

        BIFContractGetAddressResponse cAddrRsp = sdk.getBIFContractService().getContractAddress(cAddrReq);
        if (cAddrRsp.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(cAddrRsp.getResult()));
        } else {
            System.out.println(cAddrRsp.getErrorDesc());
        }
        ```

        ```
        {
            "contract_address_infos":[
                {
                    "contract_address":"did:bid:efSvDJivc2A4iqurRkUPzmpT5kB3nkNg",
                    "operation_index":0
                }
            ]
        }
        ```

1. 合约调用

    合约成功部署并且获取到地址后, 就可以调用合约的main函数, 这里我们存储一个值到合约里:

    ```
    {
        "id":"test",
        "data": "test"
    }
    ```

    合约调用的代码如下:

    ```
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

    ```
    {
        "hash":"c79835265e908f7f06d4fc2c61ef3fd046ae5252675e4671271bd921ad8fde89"
    }
    ```

1. 查询合约

    不同于调用合约, 查询合约为只读操作, 因此不需要发出上链交易和耗费gas, 这里我们查询刚刚设置的key, 查询input为:
    ```
    {
        "id":"test"
    }
    ```

    Java查询代码如下:

    ```
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

    ```
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

至此我们就完成了一个链上javascript合约从部署到操作的全过程, 有关合约的更高阶开发和星火链体系模型, 请参见高级话题

## 高级话题

### 帐号

星火链帐号的定义如下:

```
message Account
{
    string address = 1;
    int64  nonce = 2;
    AccountPrivilege priv = 3;
    bytes metadatas_hash = 4;
    bytes assets_hash = 5;
    Contract contract = 6;
    int64 balance = 7;
}
```

这里对其中几个主要项的解释如下:

1. address 

    账户地址

1. nonce

    从0开始的数字, 代表该账户发起过的交易数量, 同时用来防止签名重放攻击, 每当该账号执行一笔交易后，该账号的序号就会加1，无论该交易成功还是失败.当你用一个账号发起交易时，要在该交易中指定一个nonce值，交易中的这个nonce值必须比当前账号的nonce大1, 当一个账号被新建时，它的nonce为0.

1. contract

    如果该字段不为空, 则该账户为合约账户.

1. balance

    账户余额, 注意:每个账户至少要保留0.1XHT余额.

### 交易

星火链上的交易包含的主要元素如下:

1. source

    交易发出地址, 由该地址来支付本次交易耗费的星火令.

1. nonce

    交易序号, 同一个source下的所有交易必须具有唯一的nonce序号, 并且交易只能按照nonce从小到大按序入链, 中间不能有空.

1. fee_limit

    该交易的费用上限, 防止因为不可预知原因或者bug,导致交易耗费过多超出预期. 当一个交易花费超过fee_limit时, 交易失败, 但是耗费的fee不会返还.

1. gas_price

    交易的gas价格, 详细参见**费用**章节

### 交易耗费计算和检查

星火链上的所有交易都需要耗费XHT, 耗费的计算公式为gas * gas_price.

1. gas

    gas用来表示单个交易的计算成本, 对于javascript合约, 每种交易类型的gas耗费固定, 对于solidity合约, 交易gas耗费是实际执行的各个op(操作码)的gas耗费之和.

2. gas_price

    gas_price指用户愿意为每单位gas支付的XHT数量, 由用户自己在发出交易时指定.

星火链上每个区块的交易打包时, 会根据gas_price价格排序, gas_price越高的交易会排在前面优先执行. 同时每笔交易在打包前, 会检查下账户费用是否满足以下条件

1. 账户balance - 账户最低reserve_balance > fee_limit

2. 账户balance - 账户最低reserve_balance > gas * gas_price, 注意这里对于javascript合约, 如果该条件不满足, 交易直接不予入链. 但对于EVM合约, 会实时消耗XHT到余额不足时交易失败, 耗费的fee不会返还.


### Javascript合约开发

1. 星火链Javascript智能合约规范

    JavaScript智能合约是一段 JavaScript 代码，标准(ECMAScript as specified in ECMA-262)，使用Spark-V8引擎。

    合约结构分为如下三段。合约上链部署完成后，合约文本会直接存储到合约账户结构中。 

    合约的初始化函数是 `init`, 合约部署时自动由虚拟机引擎直接调用init进行合约账户数据的初始化。

    合约执行的入口函数是 `main`函数，main中可实现不同的功能接口，并通过参数字符串input选择不同接口。main函数入口仅支持合约调用者以**星火交易**方式进行调用，内部功能接口可实现合约数据存储相关操作。（可实现读写功能）

    合约查询接口是 `query`函数，query中可实现不同的查询功能接口，并通过参数字符串input选择不同接口。query函数入口仅支持合约调用者以**查询接口**进行调用，内部功能接口可用于合约账户中数据的读取，禁止进行合约数据存储相关操作。调用过程不需消耗星火令。(只读功能)

    下面是一个简单的例子：

    ```
    "use strict";
    function init(input)
    {
    /*init whatever you want*/
    return;
    }

    function main(input)
    {
    let para = JSON.parse(input);
    if (para.do_foo)
    {
        let x = {
        'hello' : 'world'
        };
    }
    }

    function query(input)
    { 
    return input;
    }
    ```

    除此之外, 星火链javascript合约对javascript语法也做了一些限定:

    * 源码开头必须添加 "use strict;".

    * 使用 === 和 !==, 禁用 == 和 != .

    * 使用 +=, -=, 禁用 ++ 和 -- .

1. 星火区块链 API

    为星火链JavaScript智能合约的高效执行，星火链实现了部分预编译JavaScript指令，可通过智能合约直接进行调用。

    智能合约内提供了全局对象 `Chain` 和 `Utils`, 这两个对象提供了多样的方法和变量，可以获取区块链的一些信息，也可驱动账号发起交易。

    * Chain对象方法列表

        | 方法                                                      | 说明                       |
        | --------------------------------------------------------- | -------------------------- |
        | Chain.load(metadata_key)                                  | 获取合约账号的metadata信息 |
        | Chain.store(metadata_key, metadata_value)                 | 存储合约账号的metadata信息 |
        | Chain.del(metadata_key)                                   | 删除合约账号的metadata信息 |
        | Chain.getBlockHash(offset_seq)                            | 获取区块信息               |
        | Chain.tlog(topic,args...)                                 | 输出交易日志               |
        | Chain.getAccountMetadata(account_address, metadata_key)   | 获取指定账号的metadata信息 |
        | Chain.getBalance(address)                                 | 获取账号coin amount        |
        | Chain.getAccountPrivilege(account_address)                | 获取某个账号的权限信息     |
        | Chain.getContractProperty(contract_address)               | 获取合约账号属性           |
        | Chain.payCoin(address, amount[, input], [, metadata])     | 转账                       |
        | Chain.delegateCall(contractAddress, input)                | 委托调用                   |
        | Chain.delegateQuery(contractAddress, input)               | 委托查询                   |
        | Chain.contractCall(contractAddress, asset, amount, input) | 调用合约                   |


    - Chain对象方法详细说明

        - 获取合约账号的metadata信息

        `Chain.load(metadata_key);`

        即可得到本合约账号中自定数据的abc的值。

        | 参数         | 说明          |
        | ------------ | ------------- |
        | metadata_key | metadata的key |

        ```
        let value = Chain.load('abc');
        /*
            权限：只读
            返回：成功返回字符串，如 'values', 失败返回false
        */
        
        ```

        - 存储合约账号的metadata信息

        `Chain.store(metadata_key, metadata_value);`

        | 参数           | 说明              |
        | -------------- | ----------------- |
        | metadata_key   | metadata的key     |
        | metadata_value | metadata 的 value |

        ```
        Chain.store('abc', 'values');
        /*
            权限：可写
            返回：成功返回true, 失败抛异常
        */
        
        ```

        - 删除合约账号的metadata信息

        `Chain.del(metadata_key);`

        即可删除本合约账号中自定数据的abc的值。

        | 参数         | 说明          |
        | ------------ | ------------- |
        | metadata_key | metadata的key |

        ```
        Chain.del('abc');
        /*
            权限：可写
            返回：成功返回true, 失败抛异常
        */
        
        ```

        - 获取区块信息

        `Chain.getBlockHash(offset_seq);`

        | 参数       | 说明                                     |
        | ---------- | ---------------------------------------- |
        | offset_seq | 距离最后一个区块的偏移量，范围：[0,1024) |

        ```
        let ledger = Chain.getBlockHash(4);
        /*
            权限：只读
            返回：成功返回字符串，如 'c2f6892eb934d56076a49f8b01aeb3f635df3d51aaed04ca521da3494451afb3'，失败返回 false
        */
        
        ```

        - 输出交易日志

        `Chain.tlog(topic,args...);`

        tlog会产生一笔交易写在区块上。

        | 参数    | 说明                                                         |
        | ------- | ------------------------------------------------------------ |
        | topic   | 日志主题，必须为字符串类型,参数长度(0,128]                   |
        | args... | 最多可以包含5个参数，参数类型可以是字符串、数值或者布尔类型,每个参数长度(0,1024] |

        ```
        Chain.tlog('transfer',sender +' transfer 1000',true);
        /*
            权限：可写
            返回：成功返回 true，失败抛异常
        */
        ```

        - 获取指定账号的metadata

        `Chain.getAccountMetadata(account_address, metadata_key);`

        | 参数            | 说明          |
        | --------------- | ------------- |
        | account_address | 账号地址      |
        | metadata_key    | metadata的key |

        ```
        let value = Chain.getAccountMetadata('did:bid:efAsXt5zM2Hsq6wCYRMZBS5Q9HvG2EmK', 'abc');
        
        /*
            权限：只读
            返回：成功返回字符串，如 'values', 失败返回false
        */
        ```

        - 获取账号coin amount

        `Chain.getBalance(address);`

        | 参数    | 说明     |
        | ------- | -------- |
        | address | 账号地址 |

        ```
        let balance = Chain.getBalance('did:bid:efAsXt5zM2Hsq6wCYRMZBS5Q9HvG2EmK');
        /*
            权限：只读
            返回：字符串格式数字 '9999111100000'
        */
        ```

        - 获取某个账号的权限信息

        `Chain.getAccountPrivilege(account_address);`

        | 参数            | 说明     |
        | --------------- | -------- |
        | account_address | 账号地址 |

        ```
        let privilege = Chain.getAccountPrivilege('did:bid:efAsXt5zM2Hsq6wCYRMZBS5Q9HvG2EmK');
        
        /*
            权限：只读
            返回：成功返回权限json字符串如'{"master_weight":1,"thresholds":{"tx_threshold":1}}'，失败返回 falses
        */
        ```

        - 获取合约账号属性

        `Chain.getContractProperty(contract_address);`

        | 参数             | 说明     |
        | ---------------- | -------- |
        | contract_address | 合约地址 |

        ```
        let value = Chain.getContractProperty('did:bid:efAsXt5zM2Hsq6wCYRMZBS5Q9HvG2EmK');
        
        /*
            权限：只读
            返回：成功返回JSON对象，如 {"type":0, "length" : 416},  type 指合约类型， length 指合约代码长度，如果该账户不是合约则，length 为0.
            失败返回false
        */
        ```

        - 转账

        `Chain.payCoin(address, amount[, input], [, metadata]);`

        | 参数     | 说明                                                         |
        | -------- | ------------------------------------------------------------ |
        | address  | 发送星火令的目标地址                                             |
        | amount   | 发送星火令的数量                                                 |
        | input    | 可选，合约参数，如果用户未填入，默认为空字符串               |
        | metadata | 可选，转账备注，显示为十六进制字符串，需要转换为明文 |

        ​		注意，如果提供metadata参数，那么也必须提供input参数，否则内置接口无法区分该参数是谁，因为两者都是可选的。如果没有input，可以传入空字符串**""**占位,以防止内置接口将metadata参数误认为inut参数。

        ```
        Chain.payCoin("did:bid:efAsXt5zM2Hsq6wCYRMZBS5Q9HvG2EmK", "10000", "", "vote reward");
        /*
            权限：可写
            返回：成功返回 true，失败抛异常  
        */
        ```

        - 委托调用

        `Chain.delegateCall(contractAddress, input);`

        | 参数            | 说明             |
        | --------------- | ---------------- |
        | contractAddress | 被调用的合约地址 |
        | input           | 调用参数         |

        `Chain.delegateCall` 函数会触发被调用的合约`main`函数入口，并且把当前合约的执行环境赋予被调用的合约。如合约A委托调用合约B，即执行B(main入口)的代码，读写A的数据。

        ```
        let ret = Chain.delegateCall('did:bid:efAsXt5zM2Hsq6wCYRMZBS5Q9HvG2EmK'，'{}');
        /*
            权限：可写
            返回：成功会返回被委托者合约main函数执行的结果，失败抛出异常
        */
        
        ```

        - 委托查询

        `Chain.delegateQuery(contractAddress, input);`

        | 参数            | 说明             |
        | --------------- | ---------------- |
        | contractAddress | 被调用的合约地址 |
        | input           | 调用参数         |

        `Chain.delegateQuery` 函数会触发被调用的合约`query`函数入口，且把当前合约的执行环境赋予被调用的合约。如合约A委托查询合约B，即执行B(query入口)的代码，读取A的数据。

        ```
        let ret = Chain.delegateQuery('did:bid:efAsXt5zM2Hsq6wCYRMZBS5Q9HvG2EmK'，"");
        /*
            权限：只读
            返回：调用成功则返回JSON对象 {"result":"4"}，其中 result 字段的值即查询的具体结果，调用失败返回JSON对象 {"error":true} 。
        */
        
        ```

        - 调用合约

        `Chain.contractCall(contractAddress, asset, amount, input);`

        | 参数            | 说明                       |
        | --------------- | -------------------------- |
        | contractAddress | 被调用的合约地址           |
        | asset           | 仅支持传入true，代表星火令 |
        | amount          | 星火令数量                 |
        | input           | 调用参数                   |

        `Chain.contractCall` 函数会触发被调用的合约`main`函数入口。

        ```
        let ret = Chain.contractCall('did:bid:efAsXt5zM2Hsq6wCYRMZBS5Q9HvG2EmK'，true, toBaseUnit("10"), "");
        /*
            权限：可写
            返回：如果目标账户为普通账户，则返回true，
                 如果目标账户为合约，成功会返回被委托者合约main函数执行的结果，
                 调用失败则抛出异常
        */
        
        ```

        - 查询合约

        `Chain.contractQuery(contractAddress, input);`

        | 参数            | 说明             |
        | --------------- | ---------------- |
        | contractAddress | 被调用的合约地址 |
        | input           | 调用参数         |

        `Chain.contractQuery` 会调用合约的查询接口。

        ```
        let ret = Chain.contractQuery('did:bid:efAsXt5zM2Hsq6wCYRMZBS5Q9HvG2EmK'，"");
        /*
            权限：只读
            返回：调用成功则返回JSON对象 {"result":"xxx"}，其中 result 字段的值即查询的具体结果，调用失败返回JSON对象 {"error":true}。
        */
        
        ```

        - 创建合约

        `Chain.contractCreate(balance, type, code, input);`

        | 参数        | 说明                                   |
        | ----------- | -------------------------------------- |
        | balance     | 字符串类型，转移给被创建的合约的星火令 |
        | type        | 整型，0代表javascript                  |
        | code        | 字符串类型， 合约代码                  |
        | input：init | init函数初始化参数                     |

        `Chain.contractCreate` 创建合约。

        ```
        let ret = Chain.contractCreate(toBaseUnit("10"), 0, "'use strict';function init(input){return input;} function main(input){return input;} function query(input){return input;} ", "");
        /*
            权限：可写
            返回：创建成功返回合约地址字符串，失败则抛出异常
        */
        
        ```



| 变量                     | 描述                         |
| ------------------------ | ---------------------------- |
| Chain.block.timestamp    | 当前区块的时间戳             |
| Chain.block.number       | 当前区块高度                 |
| Chain.tx.initiator       | 交易的发起者                 |
| Chain.tx.sender          | 交易的触发者                 |
| Chain.tx.gasPrice        | 交易的星火令价格             |
| Chain.tx.hash            | 交易hash值                   |
| Chain.tx.feeLimit        | 交易的限制费用               |
| Chain.msg.initiator      | 消息的发起者                 |
| Chain.msg.sender         | 消息的触发者                 |
| Chain.msg.nonce          | 本次交易消息发起者的nonce值  |
| Chain.msg.operationIndex | 触发本次合约调用的操作的序号 |
| Chain.thisAddress        | 当前合约账号的地址           |

+ 区块信息 Chain.block
  + 当前区块时间戳

    `Chain.block.timestamp`

    当前交易执行时候所在的区块时间戳。

  + 当前区块高度

    `Chain.block.number`

    当前交易执行时候所在的区块高度。

+ 交易 Chain.tx

  交易是用户签名的那笔交易信息。

  + 交易的发起者

    `Chain.tx.initiator`

     交易最原始的发起者，即交易的费用付款者。

  + 交易的触发者

    `Chain.tx.sender`

    交易最原始的触发者，即交易里触发合约执行的操作的账户。
    例如某账号发起了一笔交易，该交易中有个操作是调用合约Y（该操作的source_address是x），那么合约Y执行过程中，sender的值就是x账号的地址。

  ```
  let bar = Chain.tx.sender;
  /*
  那么bar的值是x的账号地址。
  */
  ```

  + 交易的星火令价格

    `Chain.tx.gasPrice`

    交易签名里的星火令价格。

  + 交易的哈希值

    `Chain.tx.hash`

    交易的hash值

  + 交易的限制费用

    `Chain.tx.feeLimit`

+ 消息 Chain.msg

  消息是在交易里触发智能合约执行产生的信息。在触发的合约执行的过程中，交易信息不会被改变，消息会发生变化。例如在合约中调用`contractCall`，`contractQuery`的时候，消息会变化。

  + 消息的发起者

    `Chain.msg.initiator`

    本消息的原始的发起者账号。

  + 消息的触发者

    `Chain.msg.sender`

    本次消息的触发者账号。

    例如某账号发起了一笔交易，该交易中有个操作是调用合约Y（该操作的source_address是x），那么合约Y执行过程中，sender的值就是x账号的地址。

  ```
  let bar = Chain.msg.sender;
  /*
  那么bar的值是x的账号地址。
  */
  ```

  + 本次交易里的发起者的nonce值

    `Chain.msg.nonce`。即`Chain.msg.initiator`账号的 nonce值。

  + 触发本次合约调用的操作的序号

    `Chain.msg.operationIndex`

    该值等于触发本次合约的操作的序号。

    例如某账号A发起了一笔交易tx0，tx0中第0（从0开始计数）个操作是给某个合约账户转移星火令（调用合约），那么`Chain.msg.operationIndex`的值就是0。

  ```
  let bar = Chain.msg.operationIndex;
  /* bar 是一个非负整数*/
  ```

+ 当前合约账号的地址

  `Chain.thisAddress`

  该值等于该合约账号的地址。

  例如账号x发起了一笔交易调用合约Y，本次执行过程中，该值就是Y合约账号的地址。

  ```
  let bar = Chain.msg.thisAddress;
  /*
  bar的值是Y合约的账号地址。
  */
  ```


    | API | 含义 | 用法 |
    | --- | --- | --- |
    | getBalance | | |
    | storageStore| | |
    | storageLoad | | |
    | stroageDel | | | 
    | int64Add | | | 
    | int64Sub | | | 
    | int64Mul | | |
    | int64Div | | |
    | int64Mod | | |
    | int64Compare | | |
    | toBaseUnit | | |


1. 异常处理

    - 主动抛出异常

        星火链Javascript合约禁用了try catch关键字, 但是可以调用throw来抛出异常, 当执行遇到throw异常时, 该交易判定为失败, 入链扣费但是交易不生效.

    - JavaScript异常

    当合约运行中出现未捕获的JavaScript异常时，处理规定：

    * 本次合约执行失败，合约中做的所有交易都不会生效。

    * 触发本次合约的这笔交易为失败。错误代码为`151`。

    - 执行交易失败

        合约中可以执行多个交易，只要有一个交易失败，就会抛出异常，导致整个交易失败

1. javascript合约限制

    由于区块链智能合约的执行机制原因, 星火链对javascript智能合约也做了如下的限制:

    * 堆大小限制: 30Mb
    * 栈大小限制: 512Kb
    * 执行计步限制: 10240
    * 执行时间限制: 1s
    * 合约字节限制: 256Kb
    * 去除函数: Data, Random 
    * 禁用关键字: 
        ```
        "DataView", "decodeURI", "decodeURIComponent", "encodeURI", "encodeURIComponent", "Generator","GeneratorFunction", "Intl", "Promise", "Proxy", "Reflect", "System", "URIError", "WeakMap", "WeakSet", "Math", "Date", "eval", "void", "this", "try", "catch"
        ```





### Solidity合约开发
​
Solidity智能合约使用Spark-Evm引擎，脱胎于原生以太坊EVM架构实现。在星火链合约账户中，Solidity编译后生成的opCode指令码会存储到合约账户中，用于合约的执行。

本目录的文档主要介绍在星火链合约平台中支持的 Solidity 合约的特性、语法、功能等。星火链平台支持的solidity语法基本与官方solidity基本一致，目前支持0.4.26版本，可以参考官方文档: https://solidity.readthedocs.io/en/v0.4.26/


1. 星火链Solidity与以太坊Solidity的区别

    * 星火链平台solidity对address关键字进行了重新开发，address表示的合约地址或账户地址，长度为24字节；而官方solidity中address表示的地址是20字节。
    * 在星火链链平台上，如果尝试在合约内向一个不存在的地址转账，合约会异常终止；而在以太坊官方 Solidity 合约内向不存在的地址转账时，系统会自动以该地址创建账户。
    * 星火链平台中，solidity不支持STATICCALL指令。
    * 星火链平台中，solidity不支持CALLCODE指令。
    * 星火链平台中，solidity不支持SELFDESTRUCT指令。
    * 星火链平台中，合约账户无codehash，solidity不支持EXTCODEHASH指令。
    * 星火链平台中，区块中未保存出块人信息，solidity不支持COINBASE指令。
    * 星火链平台中，无难度值概念，solidity不支持DIFFICULT指令。
    * 星火链平台中，自定义实现了STOI64CHECK指令。
    * 星火链EVM引擎处理交易时，使用星火令消耗上限+异常退出（递归深度，栈，内存）+超时。需要指定当前交易接受的最大星火令，执行合约时，按照具体指令扣减星火令。当星火令不足时，合约执行结束。
    * 当递归深度超过配置的最大深度时，合约执行结束。此处为兼容星火链框架，合约递归深度未使用以太坊原始最大递归深度1024，合约最大递归深度为4层。

2. 星火链EVM指令集比较

    | 指令表         | 星火链是否支持 | 以太坊是否支持 |
    | -------------- | -------------- | -------------- |
    | CREATE2        | 否             | 是             |
    | CREATE         | 是             | 是             |
    | DELEGATECALL   | 是             | 是             |
    | STATICCALL     | 否             | 是             |
    | CALL           | 是             | 是             |
    | CALLCODE       | 否             | 是             |
    | RETURN         | 是             | 是             |
    | REVERT         | 是             | 是             |
    | SELFDESTRUCT   | 否             | 是             |
    | STOP           | 是             | 是             |
    | MLOAD          | 是             | 是             |
    | MSTORE         | 是             | 是             |
    | MSTORE8        | 是             | 是             |
    | SHA3           | 是             | 是             |
    | LOG0           | 是             | 是             |
    | LOG1           | 是             | 是             |
    | LOG2           | 是             | 是             |
    | LOG3           | 是             | 是             |
    | LOG4           | 是             | 是             |
    | EXP            | 是             | 是             |
    | ADD            | 是             | 是             |
    | MUL            | 是             | 是             |
    | SUB            | 是             | 是             |
    | DIV            | 是             | 是             |
    | SDIV           | 是             | 是             |
    | MOD            | 是             | 是             |
    | SMOD           | 是             | 是             |
    | NOT            | 是             | 是             |
    | LT             | 是             | 是             |
    | GT             | 是             | 是             |
    | SLT            | 是             | 是             |
    | SGT            | 是             | 是             |
    | EQ             | 是             | 是             |
    | ISZERO         | 是             | 是             |
    | AND            | 是             | 是             |
    | OR             | 是             | 是             |
    | XOR            | 是             | 是             |
    | BYTE           | 是             | 是             |
    | SHL            | 是             | 是             |
    | SHR            | 是             | 是             |
    | SAR            | 是             | 是             |
    | ADDMOD         | 是             | 是             |
    | MULMOD         | 是             | 是             |
    | SIGNEXTEND     | 是             | 是             |
    | ADDRESS        | 是             | 是             |
    | ORIGIN         | 是             | 是             |
    | BALANCE        | 是             | 是             |
    | CALLER         | 是             | 是             |
    | CALLVALUE      | 是             | 是             |
    | CALLDATALOAD   | 是             | 是             |
    | CALLDATASIZE   | 是             | 是             |
    | RETURNDATASIZE | 是             | 是             |
    | CODESIZE       | 是             | 是             |
    | EXTCODESIZE    | 是             | 是             |
    | CALLDATACOPY   | 是             | 是             |
    | RETURNDATACOPY | 是             | 是             |
    | EXTCODEHASH    | 否             | 是             |
    | CODECOPY       | 是             | 是             |
    | EXTCODECOPY    | 是             | 是             |
    | GASPRICE       | 是             | 是             |
    | BLOCKHASH      | 是             | 是             |
    | COINBASE       | 否             | 是             |
    | TIMESTAMP      | 是             | 是             |
    | NUMBER         | 是             | 是             |
    | DIFFICULTY     | 否             | 是             |
    | GASLIMIT       | 是             | 是             |
    | CHAINID        | 是             | 是             |
    | SELFBALANCE    | 是             | 是             |
    | POP            | 是             | 是             |
    | PUSHC          | 否             | 是             |
    | PUSH1/32       | 是             | 是             |
    | JUMP           | 是             | 是             |
    | JUMPI          | 是             | 是             |
    | JUMPC          | 否             | 是             |
    | JUMPCI         | 否             | 是             |
    | DUP1/16        | 是             | 是             |
    | SWAP1/16       | 是             | 是             |
    | SLOAD          | 是             | 是             |
    | SSTORE         | 是             | 是             |
    | PC             | 是             | 是             |
    | MSIZE          | 是             | 是             |
    | GAS            | 是             | 是             |
    | JUMPDEST       | 是             | 是             |
    | INVALID        | 是             | 是             |

3. 合约数据类型

    **基本类型：**

    uint\<M>：M 位的无符号整数，0 < M <= 256、M % 8 == 0。例如：uint32，uint8，uint256。

    int\<M>：以 2 的补码作为符号的 M 位整数，0 < M <= 256、M % 8 == 0。

    uint、int：uint256、int256 各自的同义词。在计算和 函数选择器 中，通常使用 uint256 和 int256。

    bool：等价于 uint8，取值限定为 0 或 1 。在计算和 函数选择器 中，通常使用 bool。

    bytes\<M>：M 字节的二进制类型，0 < M <= 32。

    byte：等价于bytes1。

    bytes：动态大小的字节序列。

    string：动态大小的 unicode 字符串，通常呈现为 UTF-8 编码。

    **一维数组：**

    type[M]\(type=uint/int/address) 有 M 个元素的定长数组，M >= 0，数组元素为给定类型。

    **二维数组：**

    type[][]\(type=uint/int)

    **平台建议使用数据类型**

    | 数据类型             | 参考样例                   | 合约内部是否支持 | 输入参数是否支持 |
    | -------------------- | -------------------------- | ---------------- | ---------------- |
    | bool                 | bool a = true              | 是               | 是               |
    | uint                 | uint a = 1                 | 是               | 是               |
    | uint8 ~ uint256      | uint8 a = 1                | 是               | 是               |
    | int                  | int a = 1                  | 是               | 是               |
    | int8 ~ int256        | int8 a = 1                 | 是               | 是               |
    | bytes                | bytes a = “test”           | 是               | 是               |
    | bytes1 ~ bytes32     | bytes1 a = “a”             | 是               | 是               |
    | string               | string a = “test”          | 是               | 是               |
    | int[]                | int256[] a = [1,2,3,4,5]   | 是               | 是               |
    | uint[]               | uint256[] a = [1,2,3,4,5]  | 是               | 是               |
    | bytes1[] ~ bytes32[] | bytes4[] asd = new bytes4; | 是               | 否               |
    | string[]             | string[] a = [“adbc”,”dg”] | 是               | 否               |
    | enum                 | enum a {a,b,c}             | 是               | 否               |
    | struct               | struct a { string name;}   | 是               | 否               |

1. Solidity合约编译

    星火链合约平台支持 Solidity 智能合约，由于Spark-Evm中存在的特性，不能使用以太坊提供的编译器编译处理Solidity合约 ，因此我们提供了星火链Solidity的编译工具docker镜像。

    * 镜像下载

        ```
        docker pull caictdevelop/bif-solidity:v0.4.26
        ```

    * 使用solc
    
        镜像下载之后，需要启动镜像进入容器中，可以使用solc --help 来查看此工具支持的参数说明。

        常用选项说明：

        ```
        --opcodes            Opcodes of the contracts.
        --bin                Binary of the contracts in hex.
        --abi                ABI specification of the contracts.
        ```

    * 编译合约

        * 启动镜像

            ```
            # docker相关操作需要root权限
            docker run -it caictdevelop/bif-solidity:v0.4.26 /bin/bash
            ```

        * 编写合约test.sol

            ```
            pragma solidity ^0.4.26;

            contract test{
                function testfun() public returns(string){
                    return "hello world";
                }
            }
            ```

        * 编译合约

            ```
            #cd /root/solidity/build/solc
            #./solc --bin test.sol

            ======= test.sol:test =======
            Binary: 
            60806040523480156100105760...
            ```

1. solidity合约部署

    使用星火solidity工具编译合约后, 使用Java SDK将合约部署到链上.

    ```
    public void contractCreate() {
        // 初始化参数
        String senderAddress = "did:bid:efuEAGFPJMsojwPGKzjD8vZX1wbaUrVV";
        String senderPrivateKey = "priSPKkAwBP7w1ajzwp16hNBHvz5psKsksmgZDapcaebzxCS42";
        String payload = "608060405234801561001057600080fd5b50610444806...";

        Long initBalance = ToBaseUnit.ToUGas("0.01");

        BIFContractCreateRequest request = new BIFContractCreateRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setInitBalance(initBalance);
        request.setPayload(payload);
        request.setMetadata("create contract");
        request.setType(1);
        // 调用BIFContractCreate接口
        BIFContractCreateResponse response = sdk.getBIFContractService().contractCreate(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JSON.toJSONString(response.getResult(), true));
        } else {
            System.out.println("error:      " + response.getErrorDesc());
        }
    }
    ```


1. solidity合约调用

    调用星火链Solidity合约时, 可以直接用命名字符串形式调用指定接口, 星火链会将的input编译成字节码然后调用solidity合约.

    ```
    {
        "function":"xxx",//待调用函数声明 入setKey(int256,string)，仅包含函数名（形参类型）
        "args":{ 
            "xxx":""//待调用合约的参数，多个参数使用“，”分隔
        }
    }
    ```

    示例Java SDK代码如下：

    ```
    public void contractInvokeByGas() {
        // 初始化参数
        String senderAddress = "did:bid:efuEAGFPJMsojwPGKzjD8vZX1wbaUrVV";
        String contractAddress = "did:bid:efrVoaxEQo9sDqQmv9BCnDstyu1FDTHE";
        String senderPrivateKey = "priSPKkAwBP7w1ajzwp16hNBHvz5psKsksmgZDapcaebzxCS42";
        Long amount = 1000L;

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setMetadata("contract invoke");
        request.setInput("{\"function\":\"setKey(int256,string)\",\"args\":\"123,'hello world'\"}");
        // 调用 BIFContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JSON.toJSONString(response.getResult(), true));
        } else {
            System.out.println("error:      " + response.getErrorDesc());
        }
    }
    ```