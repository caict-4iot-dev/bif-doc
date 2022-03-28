# 星火链Solidity合约开发

Solidity智能合约使用Spark-Evm引擎，脱胎于原生以太坊EVM架构实现。在星火链合约账户中，Solidity编译后生成的opCode指令码会存储到合约账户中，用于合约的执行。

本目录的文档主要介绍在星火链合约平台中支持的 Solidity 合约的特性、语法、功能等。星火链平台支持的solidity语法基本与官方solidity基本一致，目前支持0.4.26版本，可以参考官方文档：<https://solidity.readthedocs.io/en/v0.4.26/>

## 星火链Solidity新特性

### 星火链Solidity语言主要变动

1. **星火链bid地址支持**: 

    星火链solidity address表示的地址，长度为24字节, 以太坊solidity中address表示的地址是20字节。

1. **有效地址检查**:

    在星火链solidity合约内向一个未激活(没有转入转出交易)的地址转账，合约会异常终止；而以太坊对此没有限制。

1. **指令支持**

    星火链上solidity不支持STATICCALL, CALLCODE, SELFDESCTRUCT命令.

1. **链机制不同导致的语言diff**

    星火链上solidity不支持EXTCODEHASH,COINBASE, DIFFICULT指令.

1. **函数递归深度限制**

    星火链solidity函数调用递归深度最大为4层, 以太坊为1024.

### 星火链op支持列表

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

## 星火链Solidity开发基础

### 数据类型

+ **星火链交易支持的数据类型**

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

+ **平台建议使用数据类型**

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

### 星火链Solidity编译器

​由于指令集支持和地址表示法的区别, 星火链提供了专门的编译器来编译星火链Solidity合约. 本章指导开发者使用官方编译器编译星火链智能合约.

1. 镜像下载

    ```shell
    docker pull caictdevelop/bif-solidity:v0.4.26
    ```

2. 选项说明

    镜像下载之后，需要启动镜像进入容器中，可以使用solc --help 来查看此工具支持的参数说明。

    常用选项说明：

    ```bash
    --opcodes            Opcodes of the contracts.
    --bin                Binary of the contracts in hex.
    --abi                ABI specification of the contracts.
    ```

3. 编写测试合约

    用一个最简单的测试合约做例子.

    ```solidity
    pragma solidity ^0.4.26;

    contract test{
        function testfun() public returns(string){
            return "hello world";
        }
    }
    ```

4. 编译合约

    ```shell
    # 启动镜像
    docker run -it caictdevelop/bif-solidity:v0.4.26 /bin/bash
    cd /root/solidity/build/solc
    ./solc --bin test.sol

    ======= test.sol:test =======
    Binary: 
    608060405234801561001057600080fd5b5061013f806100206000396000f300608060405260043610610041576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063031153c214610046575b600080fd5b34801561005257600080fd5b5061005b6100d6565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561009b578082015181840152602081019050610080565b50505050905090810190601f1680156100c85780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b60606040805190810160405280600b81526020017f68656c6c6f20776f726c640000000000000000000000000000000000000000008152509050905600a165627a7a723058201a4c9bfcbee5d683f6e46525cf17db2dd46a6ecf5c3f45cbdd148229639263480029
    ```

5. 部署调用

    后续的合约部署调用流程与javascript合约类似, 可以参见星火链SDK说明.