# 4.C SDK使用说明

## 4.1 基本概念定义

`SDK`是业务模块与星火链交互的桥梁，提供安全可靠的通信信道。

提供的接口，覆盖离线api、账号管理、合约管理、区块管理、交易管理等场景，满足了不同的业务场景需要。

**目前C语言版本的SDK官方不再维护，建议使用Java或者NodeJs版本的SDK。**

## 4.2  环境准备

### 4.2.1 软件依赖

- **cmake**：版本为3.10及以上

  命令查看版本：

  ```sh
  [test@localhost ~]$ cmake --version
  cmake version 3.22.5
  
  CMake suite maintained and supported by Kitware (kitware.com/cmake).
  ```

  如果显示版本太低或者没安装请下载所有要求cmake，可以通过官网源码安装或者对应系统命令安装

- **系统要求**：Linux *2.6*.32内核及以上，支持centos及ubuntu等linux系统。

  gcc：版本为gcc4.4及以上。

  命令查看版本：

  ```sh
  [root@localhost ~]$ gcc -v
  Using built-in specs.
  COLLECT_GCC=gcc
  COLLECT_LTO_WRAPPER=/usr/local/gcc-  8.4.0/build/bin/../libexec/gcc/x86_64-pc-linux-gnu/8.4.0/lto-wrapper
  Target: x86_64-pc-linux-gnu
  Configured with: ./configure -enable-languages=c,c++ -disable-multilib -enable-checking=release --prefix=/home/zhangbo/gcc-8.4.0/build
  Thread model: posix
  gcc version 8.4.0 (GCC)
  ```

### 4.2.2 下载安装

  ```http
$ git clone -b main  --depth=1 https://github.com/caict-4iot-dev/BIF-Core-SDK-C.git
  ```

## 4.3  怎么使用SDK

### 4.3.1 SDK 离线API

离线API主要是账户和密码学相关API, 不需要连接星火链网RPC接口也能工作. 主要接口如下:

#### 账户生成

1. 接口 ` get_bid_and_key_pair(&KeyPairEntity);`

1. 用途:

    用来生成一个星火链bid地址和对应私钥

1. 示例

    ```c
        KeyPairEntity key_pair_entity;
	    memset(&key_pair_entity, 0,sizeof(KeyPairEntity));
    
        int ret = get_bid_and_key_pair(&key_pair_entity);
        key_pair_entity.enc_address;
        key_pair_entity.enc_public_key;
        key_pair_entity.enc_private_key;
        key_pair_entity.raw_public_key;
        key_pair_entity.raw_private_key;
    ```


#### 加密私钥生成keystore

1. 接口 `generate_key_store(char* enc_private_key, char* password, uint64_t n, int p, int r, int version)`

1. 用途:

    用一个密码来加密保护私钥, 得到一个json表示的keystore, 对应密码不泄露的情况下, 可以公开保存.

1. 示例

    ```c
        //私钥
	    char enc_private_key[128] = "priSPKepT8DV8wTAYiAU6LjUPQFqdzN9ndcVPMv9cgNeTBYQ6V";
        //安全密码
        char *password = "12334";
        //版本
	    int version = (int) Math.pow(2, 16);
        //generate_key_store
        KEY_STORE *key_store_temp = generate_key_store(enc_private_key, password, version);
    ```

### 4.3.2 SDK 在线API

在线API主要用于向星火链上发出交易和查询合约, 需要初始化SDK连接后使用.

#### 账户处理接口

1. 查询账户信息

    1. 接口 `BIFAccountGetInfoResponse get_account(BifAccountGetInfoRequest req, const char* url);`

    1. 用途:

        用来获取一个账户当前信息

    1. 示例
        ```c
            // 初始化请求参数
            char bif_url[64] = "http://test.bifcore.bitfactory.cn";
        
            BifAccountGetInfoRequest req_account_base;
            BifAccountResponse *res_account_base;
    	    memset(&req_account_base, 0, sizeof(BifAccountGetInfoRequest));
            strcpy(req_account_base.address, "did:bid:ef2AuAJid1dB22rk3M6vB6cUc1ENnpfEe");
            //获取账户信息接口的函数
            res_account_base = get_account(req_account_base, bif_url);
        	if(res_account_base->baseResponse.code != 0)
                printf("code:%d,msg:%s\n",res_account_base->baseResponse.code,res_account_base->baseResponse.msg);
            else
                printf("%s\n", res_account_base->value);
        
            account_response_release(res_account_base); //释放内存资源
        ```
    
1. 获取账户nonce

    1. 接口 `int get_nonce(BifAccountGetInfoRequest req, const char* url);`

    1. 用途:

        用来获取一个账户当前nonce值, 有关nonce含义, 请参照星火链开发基础章节.

    1. 示例:
        ```c
            // 初始化请求参数     
            char bif_url[64] = "http://test.bifcore.bitfactory.cn";
        
            BifAccountGetInfoRequest req_nonce;
            BifAccountResponse *res_account_base;
            memset(&req_nonce, 0, sizeof(req_nonce));
            req_nonce.domainid = 0;
            memset(req_nonce.address, 0 ,sizeof(req_nonce.address));
            strcpy(req_nonce.address, "did:bid:ef2AuAJid1dB22rk3M6vB6cUc1ENnpfEe");
            res_account_base = get_nonce(req_nonce, bif_url);
            if(res_account_base->baseResponse.code != 0)
                printf("code:%d,msg:%s\n\n",res_account_base->baseResponse.code,res_account_base->baseResponse.msg);
            else
                printf("%s\n\n", res_account_base->value);
            account_response_release(res_account_base); //释放内存资源
        ```
    
1. 获取账户余额

    1. 接口 `BIFAccountGetBalanceResponse get_account_balance(BifAccountGetInfoRequest req, const char* url);`

    1. 用途:

        用来获取一个账户当前的XHT余额。

    1. 示例:

        ```c
            // 初始化请求参数
            char bif_url[64] = "http://test.bifcore.bitfactory.cn";
            //获取账户balance
            BifAccountGetInfoRequest req_account_base;
            BifAccountResponse *res_account_base;
            memset(&req_account_base, 0, sizeof(BifAccountGetInfoRequest));
            strcpy(req_account_base.address, "did:bid:ef2AuAJid1dB22rk3M6vB6cUc1ENnpfEe");
            res_account_base = get_account_balance(req_account_base, bif_url);
            if(res_account_base->baseResponse.code != 0)
                printf("code:%d,msg:%s\n",res_account_base->baseResponse.code,res_account_base->baseResponse.msg);
            else
                printf("%s,balance:%ld\n", res_account_base->value,res_account_base->balance);
            account_response_release(res_account_base); //释放内存资源
        ```

#### Block相关接口

1. 获取当前块高度

    1. 接口 `BifBlockGetNumberResponse *get_block_number(BifBlockGetTransactionsRequest req, const char* url);`

    1. 用途:

        获取当前链上最新的Block号

    1. 示例:

        ```c
            // 初始化请求参数
            char bif_url[64] = "http://test.bifcore.bitfactory.cn"; 
            BifBlockGetTransactionsRequest req;
            BifBlockGetNumberResponse *res;
            memset(&req, 0 ,sizeof(req));    
            req.domainid = 0;
            //查询区块高度
            res = get_block_number(req, bif_url);
            if(res->baseResponse.code != 0)
                printf("code:%d,msg:%s\n",res->baseResponse.code,res->baseResponse.msg);
            else
                printf("get_block_number res:%s,seq:%d\n", res->value,res->block_number);
            block_get_num_response_release(res);
        ```

1. 获取指定块内的交易列表

    1. 接口 `BifBlockGetTransactionsResponse *get_transactions(BifBlockGetTransactionsRequest req, const char* url);`

    1. 用途:

        给定block号,获取该block内的交易列表信息

    1. 示例:

        ```c
            // 初始化请求参数
            char bif_url[64] = "http://test.bifcore.bitfactory.cn"; 
        
            BifBlockGetTransactionsRequest req_tranction;
            BifBlockGetTransactionsResponse *res_tranction;
            memset(&req_tranction, 0, sizeof(BifBlockGetTransactionsRequest));
        
            req_tranction.block_number = 104928;
            res_tranction = get_transactions( req_tranction, bif_url);
            if(res_tranction->baseResponse.code != 0)
                printf("code:%d,msg:%s\n",res_tranction->baseResponse.code,res_tranction->baseResponse.msg);
            else
                printf("res_tranction res:%s\n", res_tranction->value);
            block_info_response_release(res_tranction);
        ```

1. 获取指定块的统计信息

    1. 接口 `BifBlockGetInfoResponse *get_block_info(BifBlockGetInfoRequest req, const char* url);`

    1. 用途:

        给定block号, 查询指定block的信息.

    1. 示例:

        ```c
            // 初始化请求参数
            char bif_url[64] = "http://test.bifcore.bitfactory.cn"; 
        
            BifBlockGetInfoRequest req_block_get_info;
            BifBlockGetInfoResponse *res_block_get_info;
            memset(&req_block_get_info, 0, sizeof(BifBlockGetInfoRequest));
        
            req_block_get_info.block_number = 11500;
            req_block_get_info.domainid = 0;
            res_block_get_info = get_block_info(req_block_get_info, bif_url);
            if(res_block_get_info->baseResponse.code != 0)
                printf("code:%d,msg:%s\n",res_block_get_info->baseResponse.code,res_block_get_info->baseResponse.msg);
            else
                printf("res_block_get_info res:%s\n", res_block_get_info->value);
            block_info_response_release(res_block_get_info);
        ```

1. 查询最新块的信息

    1. 接口 `BifBlockGetLatestInfoResponse *get_block_latest_info(BifBlockGetLatestInfoRequest req, const char* url);`

    1. 用途:

        获取当前最新块的信息.

    1. 示例:

        ```c
            //初始化请求参数
            char bif_url[64] = "http://test.bifcore.bitfactory.cn"; 
        
            BifBlockGetLatestInfoRequest req_block_get_latest_info;
            BifBlockGetLatestInfoResponse *res_block_get_latest_info;
            memset(&req_block_get_latest_info, 0, sizeof(BifBlockGetLatestInfoRequest));
            req_block_get_latest_info.domainid = 0;
            res_block_get_latest_info = get_block_latest_info(req_block_get_latest_info, bif_url);
            if(res_block_get_latest_info->baseResponse.code != 0)
                printf("code:%d,msg:%s\n",res_block_get_latest_info->baseResponse.code,res_block_get_latest_info->baseResponse.msg);
            else
                printf("res_block_get_latest_info:%s\n", res_block_get_latest_info->value);
            block_info_response_release(res_block_get_latest_info);
        ```

#### Transaction相关接口

1. 获取指定交易相关信息

    1. 接口 `BifTransactionGetInfoResponse *get_transaction_info(BifTransactionGetInfoRequest req, const char* url);`

    1. 用途:

        获取指定交易的详细信息

    1. 示例:

        ```c
            // 初始化请求参数
           char bif_url[64] = "http://test.bifcore.bitfactory.cn";
        
           BifTransactionGetInfoRequest req_transaction_get_info;
           BifTransactionGetInfoResponse *res_transaction_get_info;
           memset(&req_transaction_get_info, 0, sizeof(BifTransactionGetInfoRequest));
           req_transaction_get_info.domainid = 0;
           char hash_data[] = "2f25e770b7ede0966a920cc91503d5354be0b87e2cb3d237869449cd4290101f";
           strcpy(req_transaction_get_info.hash, hash_data);
        
           res_transaction_get_info = get_transaction_info(req_transaction_get_info, bif_url);
           if(res_transaction_get_info->baseResponse.code != 0)
                printf("code:%d,msg:%s\n",res_transaction_get_info->baseResponse.code,res_transaction_get_info->baseResponse.msg);
            else
                printf("%s\n", res_transaction_get_info->value);
            transaction_info_response_release(res_transaction_get_info);
        ```


1. 提交交易

    1. 接口 `BifTransactionSubmitResponse *bif_submit(BifTransactionSubmitRequest req, const char* url);`

    1. 用途:

        提交交易到星火链

    1. 示例:

        ```go
            // 初始化参数
            char bif_url[64] = "http://test.bifcore.bitfactory.cn";
        
            BifTransactionSubmitRequest req_submit;
            BifTransactionSubmitResponse *res_submit;
            memset(&req_submit, 0, sizeof(req_submit));
            
            char public_key[] = "b0656681fe6bbb5ef40fa464b6fb8335da40c6814be2a1fed750228deda2ac2d496e6e";
            char serializa[] = "0a296469643a6269643a6566324175414a69643164423232726b334d3676423663556331454e6e7066456510022234080752300a286469643a6269643a65664e69515045476e68545071614661746f463170397767723135325036384610081a027b7d2a080123456789abcdef30c0843d3801";
            char sign_data[] = "00d337a3bbd669bb8c3fbe96dd1bc0a7f9f15d888da3e065e9fa006954452a709373eec2add701881f4fb67addd31630b1f6fadbf029125c350e95b0df752401";
            strcpy(req_submit.public_key, public_key);
            req_submit.serialization = (char *)malloc(strlen(serializa) + 1);
            memset(req_submit.serialization, 0, strlen(serializa) + 1);
            strcpy(req_submit.serialization, serializa);
            strcpy(req_submit.sign_data, sign_data);
        
            res_submit = bif_submit(req_submit, bif_url);
            if(res_submit->baseResponse.code != 0)
                printf("code:%d,msg:%s\n",res_submit->baseResponse.code,res_submit->baseResponse.msg);
            else
                printf("bif_submit res:%s\n", res_submit->value);
            transaction_submit_response_release(res_submit);
            sdk_free(req_submit.serialization);
        ```

#### 合约相关接口

1. 部署合约

    1. 接口 `BifContractGetInfoResponse *contract_create(BifContractCreateRequest req, const char* url);`

    1. 用途:

        部署合约到星火链上

    1. 示例:

        ```c
            // 初始化请求参数
            char bif_url[64] = "http://test.bifcore.bitfactory.cn";
        
            //创建合约example
            BifContractGetInfoResponse *res_create_contract;
            BifContractCreateRequest req_create_contract;
            memset(&req_create_contract, 0, sizeof(BifContractCreateRequest));
            char payload[] =
              	"\"use strict\";function queryBanance1(address)\r\n{return \" 		test query "
              "private contract\";}\r\nfunction create1(input)\r\n{let key = "
              "\"private_tx_\"+input.id;let value = \"set private id "
              "\"+input.id;Chain.store(key,value);}\r\nfunction "
              "init(input)\r\n{return;}\r\nfunction "
              "main(input)\r\n{return;}\r\nfunction query1(input)\r\n{let key = "
              "\"private_tx_\"+input.id;let data = Chain.load(key);return data;}";
            input_sds_initialize(&req_create_contract.payload,
                               payload); // 初始化赋值请求中sds类型变量接口
            req_create_contract.gas_price = 10;
            req_create_contract.fee_limit = 100000000;
        
            strcpy(req_create_contract.private_key,
                 "priSPKir4tnCmj6wmBxyaL2ZuAF5TKpf81mYRv4LbeGTGWRjrr");
            strcpy(req_create_contract.sender_address,
                 "did:bid:ef2AuAJid1dB22rk3M6vB6cUc1ENnpfEe");
            req_create_contract.contract_type = 0;
            req_create_contract.init_balance = 100000000;
        
            res_create_contract = contract_create(req_create_contract, bif_url);
            if (res_create_contract->baseResponse.code != 0)
            	printf("code:%d,msg:%s\n", res_create_contract->baseResponse.code,res_create_contract->baseResponse.msg);
            else
            	printf("%s\n", res_create_contract->value);
            contract_info_response_release(res_create_contract);
            contract_sds_request_release(req_create_contract.payload);
        ```

1. 从部署交易中获取合约地址

    1. 接口 `BIFContractGetAddressResponse get_contract_address(BIFContractGetAddressRequest);`

    1. 用途:

        提供部署合约的交易哈希, 返回合约地址

    1. 示例

        ```c
            // 初始化请求参数
            char bif_url[64] = "http://test.bifcore.bitfactory.cn";
        
            BifContractGetAddressRequest req_contract_addr;
            BifContractGetInfoResponse *res_contract_addr;
            memset(&req_contract_addr, 0 ,sizeof(BifContractGetAddressRequest));
            //hash根据实际节点交易生成的值即可
            char hash_test[] = "2f25e770b7ede0966a920cc91503d5354be0b87e2cb3d237869449cd4290101f";
            strcpy(req_contract_addr.hash, hash_test);
            res_contract_addr = get_contract_address(req_contract_addr, bif_url);
        
            if(res_contract_addr->baseResponse.code != 0)
                printf("code:%d,msg:%s\n",res_contract_addr->baseResponse.code,res_contract_addr->baseResponse.msg);
            else
                printf("get_contract_address:%s\n", res_contract_addr->value);
            contract_info_response_release(res_contract_addr);
        ```

1. 获取合约相关信息

    1. 接口 `BifContractCheckValidResponse *get_contract_info(BifContractCheckValidRequest req, const char* url);`

    1. 用途:

        指定合约地址, 获取合约相关信息.

    1. 示例

        ```c
            // 初始化请求参数
            char bif_url[64] = "http://test.bifcore.bitfactory.cn";
        
            BifContractCheckValidRequest req_contract_info;
            BifContractCheckValidResponse *res_contract_info;
            memset(&req_contract_info,0,sizeof(BifContractCheckValidRequest));
            req_contract_info.domainid = 0;
            strcpy(req_contract_info.contract_address, "did:bid:efoyBUQzHSCeCj3VQk4uSxiZW9GRYcJv");
            res_contract_info = get_contract_info(req_contract_info, bif_url);
        
            if(res_contract_info->baseResponse.code != 0)
                printf("code:%d,msg:%s\n",res_contract_info->baseResponse.code,res_contract_info->baseResponse.msg);
            else
                printf("get_contract_info:%s\n", res_contract_info->value);
            contract_valid_response_release(res_contract_info);
        ```

1. 查询合约

    1. 接口 `BifContractGetInfoResponse *contract_query(BifContractCallRequest req, const char* url);`

    1. 用途:

        调用合约Query接口, 查询合约数据

    1. 示例:

        ```c
            // 初始化请求参数
            char bif_url[64] = "http://test.bifcore.bitfactory.cn";
        
            BifContractGetInfoResponse *res_contract_query;
            BifContractCallRequest req_contract_query;
            memset(&req_contract_query, 0, sizeof(BifContractCallRequest));
            char init_input[] =
              "{\"function\":\"queryBanance(string)\",\"args\":\"did:bid:"
              "efoyBUQzHSCeCj3VQk4uSxiZW9GRYcJv\",\"return\":\"returns(string)\"}";
        
            input_sds_initialize(&req_contract_query.input,
                               init_input); // 初始化赋值给sds类型的变量接口
            strcpy(req_contract_query.contract_address,
                 "did:bid:efoyBUQzHSCeCj3VQk4uSxiZW9GRYcJv");
            strcpy(req_contract_query.source_address,
                 "did:bid:ef2AuAJid1dB22rk3M6vB6cUc1ENnpfEe");
        
            res_contract_query = contract_query(req_contract_query, bif_url);
            if (res_contract_query->baseResponse.code != 0)
            	printf("code:%d,msg:%s\n", res_contract_query->baseResponse.code,res_contract_query->baseResponse.msg);
            else
            	printf("%s\n", res_contract_query->value);
            contract_info_response_release(res_contract_query);
            // 释放请求体中sds类型的内存变量
            contract_sds_request_release(req_contract_query.input);
        ```
    
1. 调用合约

    1. 接口 `BifContractGetInfoResponse *contract_invoke(BifContractInvokeRequest req, const char* url);`

    1. 用途:

        在链上发出交易调用合约可写接口

    1. 示例:

        ```c
            // 初始化请求参数
            char bif_url[64] = "http://test.bifcore.bitfactory.cn";
        
            BifContractGetInfoResponse *res_contract_invoke;
            BifContractInvokeRequest req_contract_invoke;
            memset(&req_contract_invoke, 0, sizeof(BifContractInvokeRequest));
            char init_input[] =
              "{\"function\":\"queryBanance(string)\",\"args\":\"did:bid:"
              "efoyBUQzHSCeCj3VQk4uSxiZW9GRYcJv\",\"return\":\"returns(string)\"}";
            input_sds_initialize(&req_contract_invoke.input,
                               init_input); // 初始化赋值给sds类型的变量接口
           // 根据实际部署节点的合约地址等测试信息
            strcpy(req_contract_invoke.contract_address,
                 "did:bid:efoyBUQzHSCeCj3VQk4uSxiZW9GRYcJv");
            strcpy(req_contract_invoke.sender_address,
                 "did:bid:ef2AuAJid1dB22rk3M6vB6cUc1ENnpfEe");
            strcpy(req_contract_invoke.private_key,
                 "priSPKir4tnCmj6wmBxyaL2ZuAF5TKpf81mYRv4LbeGTGWRjrr");
            strcpy(req_contract_invoke.remarks, "test1234");
            req_contract_invoke.amount = 0;
        
            res_contract_invoke = contract_invoke(req_contract_invoke, bif_url);
            if (res_contract_invoke->baseResponse.code != 0)
            	printf("code:%d,msg:%s\n", res_contract_invoke->baseResponse.code,
           res_contract_invoke->baseResponse.msg);
            else
            	printf("%s\n", res_contract_invoke->value);
            contract_info_response_release(res_contract_invoke);
            // 释放请求体中sds类型的内存变量
            contract_sds_request_release(req_contract_invoke.input);
        ```
