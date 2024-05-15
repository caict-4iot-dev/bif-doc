# 5.Javascript合约介绍

## 5.1 Javascript合约语言

星火链的`JavaScript`智能合约符合`ECMAScript as specified in ECMA-262`标准，运行在V8虚拟机引擎，同时我们针对区块链的性能对V8虚拟机做了优化。

合约的固定结构分为三段。合约上链部署完成后，合约文本会直接存储到合约账户结构中。 

* **初始化接口。**合约的初始化函数是 `init`, 合约部署时自动由虚拟机引擎直接调用`init`进行合约账户数据的初始化。

* **执行接口**。合约执行的入口函数是 `main`函数，`main`中可实现不同的功能接口，并通过参数字符串`input`选择不同接口。`main`内部功能接口可实现合约数据存储相关操作。（写功能）

* **查询接口**。合约查询接口是 `query`函数，`query`中可实现不同的查询功能接口，并通过参数字符串`input`选择不同接口。`query`函数内部功能接口可用于合约账户中数据的读取，禁止进行合约数据存储相关操作。调用过程不需消耗星火令。(只读功能)

下面是一个简单的例子：

```javascript
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

### 5.1.1  内置API

为`JavaScript`智能合约的高效执行，星火链实现了部分预编译`JavaScript`指令，可通过智能合约直接进行调用。

智能合约内提供了全局对象 `Chain` 和 `Utils`, 这两个对象提供了多样的方法和变量，可以获取区块链的一些信息，也可驱动账号发起交易。

详见[星火链JavaScript合约内置API](星火链JavaScript合约内置API.md)。

### 5.1.2 语法限制

区块链上的智能合约需要运行在隔离的沙箱环境，保证其**隔离性、安全性和确定性**，因此我们对原有的JavaScript语法做了以下裁剪：

- 源码开头必须添加 `"use strict;"`

- 判断使用` === `和 `!==`, 禁用 `== `和 `!=` 

- 使用 `+=`,` -=`, 禁用 `++` 和` --` 

- 语句块内使用 `let` 声明变量

- 语句必须以 `;` 结束

- 语句块必须用 `{}` 包括起来，且禁止空语句块

- `for` 的循环变量初始变量需在条件语句块之前声明，每次使用重新赋值

- 禁用 `++` 和 `--`

- 禁止使用 `eval`, `void` 关键字

- 禁止使用 `new` 创建 `Number`, `String`, `Boolean`对象，可以使用其构造调用来获取对象

- 禁止使用的数组关键字创建数组

  ```javascript
  示例：
  let color = new Array(100); //编译报错
  
  //可以使用替代 new Array(100) 语句;
  let color = ["red","black"]; 
  let arr = [1,2,3,4];
  ```

- 禁止使用 `try`, `catch` 关键字，可以使用 `throw` 手动抛出异常

- 禁止使用函数: Data, Random 

- 禁用可能产生随机结果的关键字：

  ```
  "DataView", "decodeURI", "decodeURIComponent", "encodeURI",
  "encodeURIComponent", "Generator","GeneratorFunction", "Intl", "Promise",
  "Proxy", "Reflect", "System", "URIError", "WeakMap", "WeakSet", "Math",
  "Date", "eval", "void", "this", "try", "catch"
  ```

- 堆大小限制: 30Mb

- 栈大小限制: 512Kb

- 执行计步限制: 10240

- 合约字节限制: 256Kb

- 合约函数调用递归深度最大为`4`层，即合约A-->合约B-->合约C-->合约D时交易正常执行，超过调用步长是则执行失败。

### 5.1.3  异常处理

#### 5.1.3.1 主动抛出异常

星火链`Javascript`合约禁用了`try catch`关键字, 但是可以调用`throw`来抛出异常, 当执行遇到`throw`异常时, 该交易判定为失败, 入链扣费但是交易不生效。

#### 5.1.3.2 语法异常

当合约运行中出现未捕获的`JavaScript`异常时，处理规定：

* 本次合约执行失败，合约中做的所有交易都不会生效

* 触发本次合约的这笔交易为失败。错误代码为`151`

- 执行交易失败

  合约中可以执行多个交易，只要有一个交易失败，就会抛出异常，导致整个交易失败

### 5.1.4  注意事项

#### 5.1.4.1 数组处理

Chain对象方法中Chain.store（key,value）的功能是向DB中保存一条数据。其中key的最大长度是`1024Byte`，value的最大长度是`256KB`，超过最大长度会写失败、报错。

超过长度限制的情况常出现在合约中数组，场景如下:

```javascript
//合约中定义了如下结构 
Json::value record{count:0,index:[]};
func addRecord(){
	record[index][index.size] = "new record";
	Chain.store("record",record.toFastString());
}
```

函数addRecord会增加index的记录并保存，当index的长度超过`256KB`时，Chain.store语句会报错。

建议的处理方式是用多个大小固定的数组来代替一个持续增长的大数组。

#### 5.1.4.2 循环处理

虚拟机在执行合约的函数时，有步长限制，最大`1024`。每一次Chain或者utils的对象方法的调用步长加1，因此当一个函数中调用了Chain的对象方法超过`1024`次时，函数会因为超过步长限制而执行失败。

通常出现在循环调用中，场景如下:

```java
func getRecord(){
	for(i=0; i < 5000; i++){
		Chain.load(i,value);
	}
}
```

函数getRecord()中通过一个循环来调用Chain.load，当循环次数大于`1024`时函数报错。

建议的处理是，如果循环的长度会超过步长限制，需要修改函数的逻辑。

## 5.2 Javascript合约工具

### 5.2.1 检测工具

为了方便开发者更规范的、安全的开发合约，在做合约语法检测时候， 星火链提供了针对`JavaScript`智能合约的定制化的校验工具JSLint 做检查。编辑合约时候，首先需要在 `JSLint` 里检测通过，才可以被星火链系统检测为一个合法的合约。

 合约校验工具：[jslint.zip](https://github.com/caict-4iot-dev/BIF-Core-Doc/blob/feature/readthedocs/source/_static/tools/jslint.zip)

<img src="../_static/images/jslint.png"  style="zoom: 80%;" />

### 5.2.2 合约文本压缩

 星火链上部署智能合约消耗的交易费和合约的大小有关，因此可以通过压缩合约来减少部署合约的交易消耗。我们提供了定制化的合约压缩工具`JSMin` 。注意压缩之前保存原合约文档，压缩是不可逆的操作。

 合约压缩工具：[jsmin.zip](https://github.com/caict-4iot-dev/BIF-Core-Doc/blob/feature/readthedocs/source/_static/tools/jsmin.zip)

- 文件解压后可看到 jsmin.bat文件

<img src="../_static/images/jsmin-1.png"  style="zoom: 80%;" />

- 文本编解jsmin.bat，设置待压缩文件名及压缩后文件名，示例中为private.js

```text
jsmin.exe <.\private.js >.\private.min.js
```

- 点击jsmin.bat执行bat文件，即可在配置目录下看到生成好的private.min.js

<img src="../_static/images/jsmin-2.png" style="zoom: 80%;" />