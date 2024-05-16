# 3 星火链solidity事件

在Solidity智能合约开发中，事件（Event）是一个重要的概念，它允许合约在特定情况下通知外部实体，如前端应用或其他合约。事件机制为合约与外部世界提供了一种通信方式，使得外部实体能够实时获取合约内部状态的变化信息。

事件在智能合约中扮演着至关重要的角色。首先，通过事件，智能合约可以发布重要的状态变更信息，使外部实体能够及时了解合约的最新状态。其次，事件机制使得智能合约更加灵活和可扩展，可以方便地与其他合约或应用进行交互。此外，事件还可以用于触发特定的业务逻辑，实现更复杂的合约功能。

在Solidity中，事件的定义和使用相对简单直观。开发者只需要在合约中声明一个事件，并在适当的时候触发它即可。一旦事件被触发，相关信息就会被记录到区块链上，供外部实体查询和订阅。因此，掌握Solidity合约中的事件订阅技术对于开发高效、安全的智能合约至关重要。

接下来，我们将详细探讨Solidity合约中事件的定义与特性、触发与记录、订阅与监听以及数据处理等方面，帮助读者更好地理解和应用这一技术。

## 3.1 事件定义

### 3.1.1 事件的基本语法结构

在Solidity中，事件的基本语法结构非常简单明了。它们通过`event`关键字进行声明，后面紧跟着事件的名称，以及一个参数列表，用于描述事件触发时传递的数据。这些参数可以是Solidity支持的任何数据类型，包括基础类型（如uint、string等）和复杂类型（如结构体和数组）。

例如，下面是一个简单的Solidity事件定义：

```javascript
event Transfer(  
    address _from,  
    address _to,  
    uint256 _value  
);
```

在这个例子中，`Transfer`事件有三个参数：`_from`表示资金转出方地址，`_to`表示资金转入方地址，`_value`表示转账的金额。

### 3.1.2 事件的参数和类型

事件的参数在定义时指定了数据的类型和结构。Solidity支持多种数据类型作为事件的参数，包括但不限于地址（address）、无符号整数（uint256）、字符串（string）以及用户自定义的类型（如结构体）。

参数的类型决定了事件日志中存储的数据格式和大小。对于简单类型，如uint256，事件日志中会直接存储其数值表示。对于复杂类型，如结构体，事件日志会按照结构的字段顺序和类型存储相应的数据。

在选择事件参数时，开发者需要根据实际应用的需求来确定。一方面，要确保参数能够充分描述事件的内容和上下文；另一方面，也要考虑到存储和传输成本，避免使用过于庞大或复杂的数据结构。

### 3.1.4 事件的索引与非索引参数

在Solidity中，事件的参数可以分为索引参数和非索引参数。索引参数通过在参数前添加`indexed`关键字来标记。索引参数允许外部实体通过特定的值来过滤和查询事件日志。

#### 3.1.4.1 索引参数：

在星火链中，通过indexed标记的参数将出现在log交易的topics中，以事件event Transfer(address indexed from, address indexed to, uint256 indexed tokenId)为例，topic中存放的为事件event的topic，topics中存放的为当前交易的触发的全部topic，即事件topic、from、to即tokenId的值，示例如下：

```json
"operations": [{
"log": {
    "topic": "ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
    "topics": [
    	"ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
        "0000000000000000000000000000000000000000000000000000000000000000",
    	"000000000000000065662316b3958181222dfedf7f943c90d552a4e9dda7fdea",
    	"0000000000000000000000000000000000000000000000000000000000000070"]
    },
    "type": 8
}],
```

#### 3.1.4.2 非索引参数：

以事件event Transfer(address from, address to, uint256 tokenId)为例，topic与topics中仅存放当前事件的event，其数据存储在datas中，示例如下：

```json
"operations": [{
"log": {
	"datas":["0000000000000000000000000000000000000000000000000000000000000000000000000000000065662316b3958181222dfedf7f943c90d552a4e9dda7fdea0000000000000000000000000000000000000000000000000000000000000070"
	]
    "topic": "ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
    "topics": [
    	"ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
    },
    "type": 8
}],
```



### 3.1.5 事件的匿名性

在Solidity中，事件（event）是智能合约与外部实体（如前端应用程序或其他合约）进行通信的一种方式。事件可以被监听，并在满足特定条件时触发，以便通知外部实体合约内部发生的状态变化，在solidity中事件可以是匿名的，也可以是非匿名的。

#### 3.1.5.1 **匿名事件**：

匿名事件在Solidity中通过使用`anonymous`关键字进行定义。这意味着事件在触发时不会附带事件签名（即事件名称）作为topic。由于没有事件名称作为标识，外部实体在监听这类事件时不能通过事件名称进行筛选，而只能通过合约地址或其他参数来识别。匿名事件的使用成本相对较低，但牺牲了通过事件名称进行筛选的灵活性。

```javascript
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;  
  
contract AnonymousEventExample {  
    event LogMessage(bool) anonymous;  
  
    function sendMessage(string memory _message) public {  
        emit LogMessage(false);  
    }  
}
```

在这个例子中，`LogMessage`事件被标记为`anonymous`。当`sendMessage`函数被调用时，会触发`LogMessage`事件，但事件签名（即`LogMessage`这个名称）不会作为topic被包含在内。**监听这个事件的外部实体只能通过合约地址来识别事件，即topic为触发event的合约源地址**。

```
"transaction": {
				"nonce": 1,
				"operations": [{
					"log": {
						"datas": ["0000000000000000000000000000000000000000000000000000000000000000"],
						"topic": "00000000000000006566160527d4e44fa8c45494b87e633f8ee528deaabc0e74"
					},
					"type": 8
				}],
				"source_address": "did:bid:ef6ydyTQ2cb3pFGeT4qC97D93NJADKCX"
			},
```

#### 3.1.5.2 **非匿名事件**：

非匿名事件在Solidity中则不会使用`anonymous`关键字。当非匿名事件被触发时，事件签名（即事件名称）会作为topic（这个签名topic是通过将事件名称及其参数类型进行keccak哈希得到的）的一部分被包括在内。这使得外部实体可以通过事件名称来筛选和识别事件，增加了灵活性。

下面是一个非匿名事件的例子：

其topic为 keccak(LogMessage(address,string) 

```
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;  
  
contract NonAnonymousEventExample {  
    event LogMessage(address sender, string message);  
  
    function sendMessage(string memory _message) public {  
        emit LogMessage(msg.sender, _message);  
    }  
}
```

在这个例子中，`LogMessage`事件没有被标记为`anonymous`，因此当`sendMessage`函数被调用并触发`LogMessage`事件时，事件签名（即`LogMessage`这个名称）会作为topic的一部分被包括在事件日志中。这使得监听这个事件的外部实体可以通过事件名称来过滤和识别它。

```
"transaction": {
				"nonce": 1,
				"operations": [{
					"log": {
						"datas": ["0000000000000000656603fa16b1755f81c74889ff6a0d9f7992f7e13ef02e170000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000d2768656c6c6f20776f726c642700000000000000000000000000000000000000"],
						"topic": "df2f43000ad262ff927c671ed83129f9054af075e5d3add03a2ba7116e719a51",
						"topics": ["df2f43000ad262ff927c671ed83129f9054af075e5d3add03a2ba7116e719a51"]
					},
					"type": 8
				}],
				"source_address": "did:bid:efP1HqibpuM9Zss4BBihQ5zm1vR8vRb"
			},
```

​	总结来说，匿名事件和非匿名事件的主要区别在于事件签名是否作为topic被包括在事件日志中。匿名事件的使用成本更低，但牺牲了通过事件名称筛选的灵活性；非匿名事件则提供了更多的筛选选项，但可能伴随着稍高的使用成本。在选择使用哪种类型的事件时，应根据具体的应用场景和需求进行权衡。

## 3.2 事件触发与记录

### 3.2.1 何时触发事件

在Solidity智能合约中，事件的触发通常发生在合约内部状态发生变化时，或者是合约需要通知外部实体某个特定操作已经执行完成时。事件的触发是由合约中的函数或方法调用来实现的。

具体而言，当合约执行一个包含`emit`关键字的语句时，就会触发相应的事件。`emit`关键字后面跟着的是事件的名称以及传递给事件的参数值。这些参数值将作为事件数据被记录到区块链上。

例如，在一个代币合约中，当发生转账操作时，可以触发一个`Transfer`事件来通知外部实体转账的详细信息。这个事件可以在转账函数中被触发，如下所示：

```javascript
function transfer(address _to, uint256 _value) public returns (bool) {  
    // 转账逻辑...  
    emit Transfer(msg.sender, _to, _value);  
    return true;  
}
```

在上面的代码中，当`transfer`函数被调用时，如果转账逻辑成功执行，就会通过`emit Transfer`语句触发`Transfer`事件，并将转账的发起者（`msg.sender`）、接收者（`_to`）和转账金额（`_value`）作为参数传递给事件。

### 3.2.2  事件触发后的记录方式

在星火链中，日志作为一种交易类型，与普通交易一起被打包进区块并永久存储。下面将以 event LogMessage(address sender, string message) 事件为例说明，星火链中事件交易格式如下：

```
{
	"error_code": 0,
	"result": {
		"total_count": 1,
		"transactions": [{
			"actual_fee": 0,
			"close_time": 1710390854953942,
			"error_code": 0,
			"error_desc": "",
			"hash": "66187df91825ed1063a64536154447cb87f95f28ace940c2b9f8a685fc187500",
			"ledger_seq": 11744,
			"transaction": {
				"nonce": 1,
				"operations": [{
					"log": {
						"datas": ["0000000000000000656603fa16b1755f81c74889ff6a0d9f7992f7e13ef02e170000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000d2768656c6c6f20776f726c642700000000000000000000000000000000000000"],
						"topic": "df2f43000ad262ff927c671ed83129f9054af075e5d3add03a2ba7116e719a51",
						"topics": ["df2f43000ad262ff927c671ed83129f9054af075e5d3add03a2ba7116e719a51"]
					},
					"type": 8
				}],
				"source_address": "did:bid:efVSDRupqq853ErUNptYwACbWVGY8jzk"
			},
			"trigger": {
				"transaction": {
					"hash": "dac9b135f7ca4fe8a23e31fd268f62c186ae8f8597e9e303cc700ab156ffa493"
				}
			},
			"tx_size": 484
		}]
	}
}
```

其中，trigger中的hash为触发当前日志交易的原始hash，用于在区块链网络中溯源查找触发者。当前交易和普通交易（合约部署、合约调用、转账）一样，可直接通过交易hash进行检索查询。

operations内部为触发的log数据：

1. **topic**为事件，即LogMessage事件的topic。
2. datas为事件携带的数据信息，即address、 string。
3. topics为当前交易触发的topics，详见事件的索引与非索引参数。

### 3.2.3  事件的存储位置

在星火链中，事件作为一种特殊交易类型，与普通交易类型数据一同存储，可通过指定交易hash直接查询到事件记录。

## 3.3 事件的订阅与监听

### 3.3.1 订阅事件的基本概念

在Solidity智能合约中，事件提供了一种机制，使得外部实体（如DApp前端、后端服务或第三方应用）能够实时地获取到合约状态的变化信息。为了接收这些事件通知，外部实体需要订阅相关的事件。

订阅事件意味着外部实体向区块链网络表达了对某个或某些特定事件的关注，并请求在这些事件发生时接收通知。一旦事件被触发并记录在区块链上，订阅了该事件的外部实体就能够通过查询区块链或监听事件流来获取到这些事件数据。

通过订阅事件，外部实体可以实时地了解智能合约的执行情况，如转账、投票结果、数据更新等，并根据这些信息执行相应的操作，如更新用户界面、触发回调、执行进一步的数据处理等。

### 3.3.2 星火链网监听solidity合约事件

在星火链网中，提供了合约事件订阅功能。详细使用见[订阅服务使用示例说明](../instructions/订阅服务使用说明.md)。

