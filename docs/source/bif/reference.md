# 4.智能合约示例

本节为星火链智能合约的示例。

## ERC20合约

本节描述通过星火链网实现并部署`ERC20`智能合约。

`ERC20`可以简单理解成以太坊上的一个代币协议，所有基于以太坊开发的代币合约都遵守这个协议。有关`ERC20`标准可以参考[官方文档](https://theethereum.wiki/w/index.php/ERC20_Token_Standard)。

### 说明

+ **合约接口**

| 接口                                                | 返回值  | 描述                                                         |
| --------------------------------------------------- | ------- | ------------------------------------------------------------ |
| name()                                              | string  | 代币名称获取                                                 |
| symbol()                                            | string  | 代币符号获取                                                 |
| totalSupply()                                       | uint256 | 发行方总代币金额获取                                         |
| transfer(address to,uint256 value)                  | 无      | 代币转移接口，从自己（创建交易者）账号发送`_value`个代币到 `_to`账号 |
| allowance(address,address)                          | 无      | 账号所有者操作列表                                           |
| transferFrom(address from,address to,uint256 value) | 无      | 账号之间代币交易转移<br />from 发送者地址<br />to 接收者地址<br />value 转移数额 |
| approve(address spender,uint256 value)              | 无      | 设置某个地址（合约）可以创建交易者名义花费的代币数，允许发送者`_spender` 花费不多于 `_value` 个代币 |
| burn(uint256 value)                                 | 无      | 销毁我（创建交易者）账户中指定个代币                         |
| burnFrom(address from, uint256 value)               | 无      | 销毁用户账户中指定个代币                                     |

### Solidity 合约

- **合约文件**

  ```javascript
  pragma solidity ^0.4.26;
  
  contract TokenERC20 {
      string public name; // ERC20标准
      string public symbol; // ERC20标准
      uint8 public decimals = 2;  // ERC20标准，decimals 可以有的小数点个数，最小的代币单位。18 是建议的默认值
      uint256 public totalSupply; // ERC20标准 总供应量
  
      // 用mapping保存每个地址对应的余额 ERC20标准
      mapping (address => uint256) public balanceOf;
      // 存储对账号的控制 ERC20标准
      mapping (address => mapping (address => uint256)) public allowance;
  
      // 事件，用来通知客户端交易发生 ERC20标准
      event Transfer(address indexed from, address indexed to, uint256 value);
  
      // 事件，用来通知客户端代币被消费 ERC20标准
      event Burn(address indexed from, uint256 value);
  
      /**
       * 初始化构造
       */
      function TokenERC20(uint256 initialSupply, string tokenName, string tokenSymbol) public {
          totalSupply = initialSupply * 10 ** uint256(decimals);  // 供应的份额，份额跟最小的代币单位有关，份额 = 币数 * 10 ** decimals。
          balanceOf[msg.sender] = totalSupply;                // 创建者拥有所有的代币
          name = tokenName;                                   // 代币名称
          symbol = tokenSymbol;                               // 代币符号
      }
  
      /**
       * 代币交易转移的内部实现
       */
      function _transfer(address _from, address _to, uint _value) internal {
          // 确保目标地址不为0x0，因为0x0地址代表销毁
          require(_to != 0x0);
          // 检查发送者余额
          require(balanceOf[_from] >= _value);
          // 确保转移为正数个
          require(balanceOf[_to] + _value > balanceOf[_to]);
  
          // 以下用来检查交易，
          uint previousBalances = balanceOf[_from] + balanceOf[_to];
          // Subtract from the sender
          balanceOf[_from] -= _value;
          // Add the same to the recipient
          balanceOf[_to] += _value;
          Transfer(_from, _to, _value);
  
          // 用assert来检查代码逻辑。
          assert(balanceOf[_from] + balanceOf[_to] == previousBalances);
      }
  
      /**
       *  代币交易转移
       *  从自己（创建交易者）账号发送`_value`个代币到 `_to`账号
       * ERC20标准
       * @param _to 接收者地址
       * @param _value 转移数额
       */
      function transfer(address _to, uint256 _value) public {
          _transfer(msg.sender, _to, _value);
      }
  
      /**
       * 账号之间代币交易转移
       * ERC20标准
       * @param _from 发送者地址
       * @param _to 接收者地址
       * @param _value 转移数额
       */
      function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
          require(_value <= allowance[_from][msg.sender]);     // Check allowance
          allowance[_from][msg.sender] -= _value;
          _transfer(_from, _to, _value);
          return true;
      }
  
      /**
       * 设置某个地址（合约）可以创建交易者名义花费的代币数。
       *
       * 允许发送者`_spender` 花费不多于 `_value` 个代币
       * ERC20标准
       * @param _spender The address authorized to spend
       * @param _value the max amount they can spend
       */
      function approve(address _spender, uint256 _value) public
      returns (bool success) {
          allowance[msg.sender][_spender] = _value;
          return true;
      }
  
      /**
       * 销毁我（创建交易者）账户中指定个代币
       *-非ERC20标准
       */
      function burn(uint256 _value) public returns (bool success) {
          require(balanceOf[msg.sender] >= _value);   // Check if the sender has enough
          balanceOf[msg.sender] -= _value;            // Subtract from the sender
          totalSupply -= _value;                      // Updates totalSupply
          Burn(msg.sender, _value);
          return true;
      }
  
      /**
       * 销毁用户账户中指定个代币
       *-非ERC20标准
       * Remove `_value` tokens from the system irreversibly on behalf of `_from`.
       *
       * @param _from the address of the sender
       * @param _value the amount of money to burn
       */
      function burnFrom(address _from, uint256 _value) public returns (bool success) {
          require(balanceOf[_from] >= _value);                // Check if the targeted balance is enough
          require(_value <= allowance[_from][msg.sender]);    // Check allowance
          balanceOf[_from] -= _value;                         // Subtract from the targeted balance
          allowance[_from][msg.sender] -= _value;             // Subtract from the sender's allowance
          totalSupply -= _value;                              // Update totalSupply
          Burn(_from, _value);
          return true;
      }
  }
  ```

#### 合约部署

调用合约创建方法部署合约,solidity合约编译参考[星火链Solidity编译器](https://bif-doc.readthedocs.io/zh_CN/latest/app/solidity.html#id5)

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        String payload = "608060405260028060006101000a81548160ff021916908360ff1602179055503480156200002c57600080fd5b506040516200115138038062001151833981018060405281019080805190602001909291908051820192919060200180518201929190505050600260009054906101000a900460ff1660ff16600a0a8302600381905550600354600460003377ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508160009080519060200190620000e99291906200010c565b508060019080519060200190620001029291906200010c565b50505050620001bb565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106200014f57805160ff191683800117855562000180565b8280016001018555821562000180579182015b828111156200017f57825182559160200191906001019062000162565b5b5090506200018f919062000193565b5090565b620001b891905b80821115620001b45760008160009055506001016200019a565b5090565b90565b610f8680620001cb6000396000f3006080604052600436106100af576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806306fdde03146100b4578063095ea7b31461014457806318160ddd146101ad57806323b872dd146101d8578063313ce5671461026557806342966c681461029657806370a08231146102db57806379cc67901461033657806395d89b411461039f578063a9059cbb1461042f578063dd62ed3e14610480575b600080fd5b3480156100c057600080fd5b506100c96104ff565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156101095780820151818401526020810190506100ee565b50505050905090810190601f1680156101365780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34801561015057600080fd5b50610193600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff1690602001909291908035906020019092919050505061059d565b604051808215151515815260200191505060405180910390f35b3480156101b957600080fd5b506101c261063a565b6040518082815260200191505060405180910390f35b3480156101e457600080fd5b5061024b600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff169060200190929190803577ffffffffffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050610640565b604051808215151515815260200191505060405180910390f35b34801561027157600080fd5b5061027a61078d565b604051808260ff1660ff16815260200191505060405180910390f35b3480156102a257600080fd5b506102c1600480360381019080803590602001909291905050506107a0565b604051808215151515815260200191505060405180910390f35b3480156102e757600080fd5b50610320600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff1690602001909291905050506108b8565b6040518082815260200191505060405180910390f35b34801561034257600080fd5b50610385600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff169060200190929190803590602001909291905050506108d0565b604051808215151515815260200191505060405180910390f35b3480156103ab57600080fd5b506103b4610b1e565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156103f45780820151818401526020810190506103d9565b50505050905090810190601f1680156104215780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34801561043b57600080fd5b5061047e600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050610bbc565b005b34801561048c57600080fd5b506104e9600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff169060200190929190803577ffffffffffffffffffffffffffffffffffffffffffffffff169060200190929190505050610bcb565b6040518082815260200191505060405180910390f35b60008054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156105955780601f1061056a57610100808354040283529160200191610595565b820191906000526020600020905b81548152906001019060200180831161057857829003601f168201915b505050505081565b600081600560003377ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008577ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055506001905092915050565b60035481565b6000600560008577ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003377ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205482111515156106dd57600080fd5b81600560008677ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003377ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282540392505081905550610782848484610bf0565b600190509392505050565b600260009054906101000a900460ff1681565b600081600460003377ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054101515156107f857600080fd5b81600460003377ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282540392505081905550816003600082825403925050819055503377ffffffffffffffffffffffffffffffffffffffffffffffff167fcc16f5dbb4873280815c1ee09dbd06736cffcc184412cf7a71a0fdb75d397ca5836040518082815260200191505060405180910390a260019050919050565b60046020528060005260406000206000915090505481565b600081600460008577ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020541015151561092857600080fd5b600560008477ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003377ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205482111515156109c357600080fd5b81600460008577ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828254039250508190555081600560008577ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003377ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282540392505081905550816003600082825403925050819055508277ffffffffffffffffffffffffffffffffffffffffffffffff167fcc16f5dbb4873280815c1ee09dbd06736cffcc184412cf7a71a0fdb75d397ca5836040518082815260200191505060405180910390a26001905092915050565b60018054600181600116156101000203166002900480601f016020809104026020016040519081016040528092919081815260200182805460018160011615610100020316600290048015610bb45780601f10610b8957610100808354040283529160200191610bb4565b820191906000526020600020905b815481529060010190602001808311610b9757829003601f168201915b505050505081565b610bc7338383610bf0565b5050565b6005602052816000526040600020602052806000526040600020600091509150505481565b6000808377ffffffffffffffffffffffffffffffffffffffffffffffff1614151515610c1b57600080fd5b81600460008677ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205410151515610c7157600080fd5b600460008477ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205482600460008677ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205401111515610d0f57600080fd5b600460008477ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054600460008677ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205401905081600460008677ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828254039250508190555081600460008577ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825401925050819055508277ffffffffffffffffffffffffffffffffffffffffffffffff168477ffffffffffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a380600460008577ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054600460008777ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205401141515610f5457fe5b505050505600a165627a7a72305820e735129ac22be6cb94fe5d44fa5136dd19407dcce05da3b8aea9aefc42b5ef3f0029";
        Long initBalance = ToBaseUnit.ToUGas("0.01");
        String input ="{\"function\":\"TokenERC20(uint256,string,string)\",\"args\":\"1,'solidity Token','https://gateway.pinata.cloud/ipfs/QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/6476'\"}";
        BIFContractCreateRequest request = new BIFContractCreateRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setInitBalance(initBalance);
        request.setPayload(payload);
        request.setRemarks("create contract");
        request.setType(1);
        request.setGasPrice(10L);
        request.setFeeLimit(111549500L);
        request.setInitInput(input);

        // 调用bifContractCreate接口
        BIFContractCreateResponse response = sdk.getBIFContractService().contractCreate(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

交易hash：`0f28496d48e07c39f5dcb4ccca854753a49eb7917a4d3a962095e562f79c58ca`

根据交易hash获取合约地址

```java
        // 合约部署返回值hash
        String hash = "0f28496d48e07c39f5dcb4ccca854753a49eb7917a4d3a962095e562f79c58ca";
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

合约地址：`did:bid:efRkydCV4xT5qwbwpRRAW5gyvr7Ep7os`

#### 合约调用

根据生成的合约地址进行合约调用操作

##### 代币转移

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:efRkydCV4xT5qwbwpRRAW5gyvr7Ep7os";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input = "{\"function\":\"transfer(address,uint256)\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i,2\"}";

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setGasPrice(10L);
        request.setRemarks("contract invoke");
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 代币交易转移

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:efRkydCV4xT5qwbwpRRAW5gyvr7Ep7os";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String input="{\"function\":\"transferFrom(address,address,uint256 )\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i,did:bid:efdvn6cS5TZgiM5ffVN9HQh3y72raYtm,3\"}";

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setGasPrice(10L);
        request.setRemarks("contract invoke");
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 授权

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:efRkydCV4xT5qwbwpRRAW5gyvr7Ep7os";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String input="{\"function\":\"approve(address,uint256)\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i,3\"}";

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setGasPrice(10L);
        request.setRemarks("contract invoke");
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 销毁指定个代币

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:efRkydCV4xT5qwbwpRRAW5gyvr7Ep7os";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String input="{\"function\":\"burn(uint256)\",\"args\":\"3\"}";

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setGasPrice(10L);
        request.setRemarks("contract invoke");
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 销毁用户账户指定个代币

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:efRkydCV4xT5qwbwpRRAW5gyvr7Ep7os";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String input="{\"function\":\"burnFrom(address,uint256)\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i,1\"}";

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setGasPrice(10L);
        request.setRemarks("contract invoke");
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

#### 合约查询

##### 查询name

```java
        // 初始化参数
        String contractAddress = "did:bid:efRkydCV4xT5qwbwpRRAW5gyvr7Ep7os";
        String input  = "{\"function\":\"name()\",\"return\":\"returns(string)\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询symbol

```java
        // 初始化参数
        String contractAddress = "did:bid:efRkydCV4xT5qwbwpRRAW5gyvr7Ep7os";
        String input  = "{\"function\":\"symbol()\",\"return\":\"returns(string)\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询totalSupply

```java
        // 初始化参数
        String contractAddress = "did:bid:efRkydCV4xT5qwbwpRRAW5gyvr7Ep7os";
        String input  = "{\"function\":\"totalSupply()\",\"return\":\"returns(uint256)\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 账号所有者操作列表

```java
        // 初始化参数
        String contractAddress = "did:bid:efRkydCV4xT5qwbwpRRAW5gyvr7Ep7os";
        String input  = "{\"function\":\"allowance(address,address)\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i,did:bid:efdvn6cS5TZgiM5ffVN9HQh3y72raYtm\",\"return\":\"returns(uint256)\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

## ERC721合约

本节描述通过星火链网实现并部署`ERC721`智能合约。

相比于`ERC20`，`ERC721`是非同质化代币，也就意味着每个Token都是不一样的，都有自己的唯一性和独特价值，当然这也就意味着它们是不可分割的。有关`ERC721`标准可以参考[官方文档](https://eips.ethereum.org/EIPS/eip-721)。

### 说明

- **合约接口**

| 接口                                                         | 返回值  | 描述                                                         |
| ------------------------------------------------------------ | ------- | ------------------------------------------------------------ |
| name()                                                       | string  | 代币名称获取                                                 |
| symbol()                                                     | string  | 代币符号获取                                                 |
| tokenURI()                                                   | 无      | 根据tokenid 去查询的，通常为一个json字符串，描述了 NFT的图片、介绍等详细信息。 |
| balanceOf(address _owner)                                    | uint256 | 获取 用户_ owner 所有NFT代币的数量                           |
| ownerOf(uint256_tokenId)                                     | address | 查询拥有tokenID号为 _tokenId 的NFT的 所属者owner的地址       |
| transferFrom(address _from, address _to, uint256 _tokenId)   | 无      | 将tokenID 为 _tokenId 的NFT 从 _from地址的用户 转移到 _to地址的用户 |
| safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes data ) | 无      | 安全地将tokenID 为 _tokenId 的NFT 从 _from地址的用户 转移到 _to地址的用户, 并携带 data数据；安全地是指：需要判断 _to的地址，是合约账户地址，还是用户账户地址。若为合约地址，该这个合约必须实现ERC721TokenReceiver接口。 |
| safeTransferFrom(address _from, address _to, uint256 _tokenId) | 无      | 安全地将tokenID 为 _tokenId 的NFT 从 _from地址的用户 转移到 _to地址的用户 |
| approve(address _approved, uint256 _tokenId)                 | 无      | 授权， _tokenId的拥有者 将_tokenId对应的 NFT 授权给 _approved 去操作 |
| getApproved (uint256 _tokenId)                               | address | 获取 某个账户取得了_tokenId对应代币的授权                    |
| setApprovalForAll(address _operator, bool _approved)         | 无      | 将自己所有的NFT 授权 给 _operator 用户。_ approved 为true时，代表授权，为false时，代表取消授权 |
| isApprovedForAll(address _owner, address _operator)          | bool    | 查询_operator 是否拥有了 _owner所有NFT的 授权。              |

### Solidity合约

- **合约文件**

  ```javascript
  pragma solidity ^0.4.26;
  
  contract XHERC721  {
  
      address public fundation; // 管理员  
      
      // 代币名称
      string private _name;
  
      // 代币符号
      string private _symbol;
  
      // NFT 属于哪个账户的
      mapping(uint256 => address) private _tokens;
  
      // 账户有 几个NFT
      mapping(address => uint256) private _balanceOf;
  
      // 授权集合
      mapping(uint256 => address) private _allowances;
  
      // Mapping from owner to operator approvals 全部 NFT 的授权集合
      mapping(address => mapping(address => bool)) private _isAllApproved;
  
      
      // 三个事件
      event Transfer(address indexed _from, address indexed _to, uint256 indexed _tokenId);
      event Approval(address indexed _owner, address indexed _approved, uint256 indexed _tokenId);
      event ApprovalForAll(address indexed _owner, address indexed _operator, bool _approved);
  
      /**
       * 初始化构造
       */
      function XHERC721(string memory name_, string memory symbol_) public {
          _name = name_;
          _symbol = symbol_;
  	    fundation = msg.sender; 
      }  
  
      modifier onlyFundation() {
          require(msg.sender == fundation);
          _;
      }
  
      // 可选
      function name() public view returns (string memory) {
          return _name;
      }
      function symbol() public view returns (string memory) {
          return _symbol;
      }
      
      //function url() virtual public view returns (uint8);
  
      // 必须实现 ----  9个方法
      function balanceOf(address owner) public view returns (uint256) {
          require(owner != address(0), "ERC721: balance query for the zero address");
          return _balanceOf[owner];
      }
  
      // 代币的地址
      function ownerOf(uint256 tokenId) public view returns (address) {
          address owner = _tokens[tokenId];
          require(owner != address(0), "ERC721: owner query for nonexistent token");
          return owner;
      }
  
      /**
       * 创建NFT。
       * @param to 接收方
       * @param tokenId 代币的标识符
       */
      function mint(address to, uint256 tokenId) public onlyFundation {
          require(to != address(0), "ERC721: mint to the zero address");
          require(!_exists(tokenId), "ERC721: token already minted");
  
          _balanceOf[to] += 1;
          _tokens[tokenId] = to;
  
          emit Transfer(address(0), to, tokenId);
      }
      
      function _burn(uint256 tokenId) internal {
          address owner = XHERC721.ownerOf(tokenId);
  
          // Clear approvals
          _approve(address(0), tokenId);
  
          _balanceOf[owner] -= 1;
          delete _tokens[tokenId];
  
          emit Transfer(owner, address(0), tokenId);
      }
      
      function transferFrom(
          address from,
          address to,
          uint256 tokenId
      ) public {
          require(_isApprovedOrOwner(msg.sender, tokenId), "ERC721: transfer caller is not owner nor approved");
          _transfer(from, to, tokenId);
      }
      
      /**
       * 从地址转账。合约调用方须是经过_from授权的账户
       * @param from 发送方
       * @param to 接收方
       * @param tokenId 代币的标识符
       */
      function _transfer(
          address from,
          address to,
          uint256 tokenId
      ) internal {
          require(XHERC721.ownerOf(tokenId) == from, "ERC721: transfer from incorrect owner");
          require(to != address(0), "ERC721: transfer to the zero address");
  
          _approve(address(0), tokenId);
  
          _balanceOf[from] -= 1;
          _balanceOf[to] += 1;
          _tokens[tokenId] = to;
  
          emit Transfer(from, to, tokenId);
      }
  
      // 要实现转账，先实现授权。
      function safeTransferFrom(
          address from,
          address to,
          uint256 tokenId
      ) public {
          safeTransferFrom(from, to, tokenId, "");
      }
      
      function safeTransferFrom(
          address from,
          address to,
          uint256 tokenId,
          bytes memory _data
      ) public {
          require(_isApprovedOrOwner(msg.sender, tokenId), "ERC721: transfer caller is not owner nor approved");
          _safeTransfer(from, to, tokenId, _data);
      }
      
      function _safeTransfer(
          address from,
          address to,
          uint256 tokenId,
          bytes memory _data
      ) internal {
          _transfer(from, to, tokenId);
      }
  
  
      /**
       * 授权
       * @param to 接受授权的账户地址
       * @param tokenId 代币的标识符
       */
      function approve(address to, uint256 tokenId) public  {
          address owner = XHERC721.ownerOf(tokenId);
          require(to != owner, "ERC721: approval to current owner");
  
          require(
              msg.sender == owner || isApprovedForAll(owner, msg.sender),
              "ERC721: approve caller is not owner nor approved for all"
          );
  
          _approve(to, tokenId);
      }
      
      function _approve(address to, uint256 tokenId) internal {
          _allowances[tokenId] = to;
          emit Approval(XHERC721.ownerOf(tokenId), to, tokenId);
      }
  
      /**
       * 查看接受授权的账户地址
       * @param tokenId 代币的标识符
       */
      function getApproved(uint256 tokenId) public view  returns (address) {
          require(_exists(tokenId), "ERC721: approved query for nonexistent token");
  
          return _allowances[tokenId];
      }
  
      
      function _exists(uint256 tokenId) internal view returns (bool) {
          return _tokens[tokenId] != address(0);
      }
  
      /**
       * 拥有者将其所有NFT进行全部授权
       * @param operator 接受授权的账户地址
       * @param approved 是否授权
       */
      function setApprovalForAll(address operator, bool approved) public {
          _setApprovalForAll(msg.sender, operator, approved);
      }
     
      function _setApprovalForAll(
          address owner,
          address operator,
          bool approved
      ) internal {
          require(owner != operator, "ERC721: approve to caller");
          _isAllApproved[owner][operator] = approved;
          emit ApprovalForAll(owner, operator, approved);
      }
      
      function isApprovedForAll(address owner, address operator) public view returns (bool) {
  
          require(owner != address(0), "_owner can not be empty!");
          require(operator != address(0), "_operator can not be empty!");
  
          return  _isAllApproved[owner][operator];
      }
  
          
      function _isApprovedOrOwner(address spender, uint256 tokenId) internal view returns (bool) {
          require(_exists(tokenId), "ERC721: operator query for nonexistent token");
          address owner = XHERC721.ownerOf(tokenId);
          return (spender == owner || getApproved(tokenId) == spender || isApprovedForAll(owner, spender));
      }
  
  }
  ```

#### 合约部署

调用合约创建方法部署合约，solidity合约编译参考[星火链Solidity编译器](https://bif-doc.readthedocs.io/zh_CN/latest/app/solidity.html#id5)

```java
       // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        String payload = "60806040523480156200001157600080fd5b5060405162001eed38038062001eed8339810180604052810190808051820192919060200180518201929190505050816001908051906020019062000058929190620000c2565b50806002908051906020019062000071929190620000c2565b50336000806101000a81548177ffffffffffffffffffffffffffffffffffffffffffffffff021916908377ffffffffffffffffffffffffffffffffffffffffffffffff160217905550505062000171565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106200010557805160ff191683800117855562000136565b8280016001018555821562000136579182015b828111156200013557825182559160200191906001019062000118565b5b50905062000145919062000149565b5090565b6200016e91905b808211156200016a57600081600090555060010162000150565b5090565b90565b611d6c80620001816000396000f3006080604052600436106100db576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806306fdde03146100e0578063081812fc14610170578063095ea7b3146101e557806323b872dd1461023657806340c10f19146102ab57806342842e0e146102fc5780636352211e1461037157806370a08231146103e657806395d89b4114610441578063a22cb465146104d1578063b09f126614610524578063b88d4fde146105b4578063d28d88521461066f578063e0a9be75146106ff578063e985e9c51461075e575b600080fd5b3480156100ec57600080fd5b506100f56107e1565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561013557808201518184015260208101905061011a565b50505050905090810190601f1680156101625780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34801561017c57600080fd5b5061019b60048036038101908080359060200190929190505050610883565b604051808277ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b3480156101f157600080fd5b50610234600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050610967565b005b34801561024257600080fd5b506102a9600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff169060200190929190803577ffffffffffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050610b37565b005b3480156102b757600080fd5b506102fa600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050610beb565b005b34801561030857600080fd5b5061036f600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff169060200190929190803577ffffffffffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050610e95565b005b34801561037d57600080fd5b5061039c60048036038101908080359060200190929190505050610eb6565b604051808277ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b3480156103f257600080fd5b5061042b600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff169060200190929190505050610fcf565b6040518082815260200191505060405180910390f35b34801561044d57600080fd5b506104566110f2565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561049657808201518184015260208101905061047b565b50505050905090810190601f1680156104c35780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b3480156104dd57600080fd5b50610522600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff169060200190929190803515159060200190929190505050611194565b005b34801561053057600080fd5b506105396111a3565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561057957808201518184015260208101905061055e565b50505050905090810190601f1680156105a65780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b3480156105c057600080fd5b5061066d600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff169060200190929190803577ffffffffffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290505050611241565b005b34801561067b57600080fd5b506106846112f7565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156106c45780820151818401526020810190506106a9565b50505050905090810190601f1680156106f15780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34801561070b57600080fd5b50610714611395565b604051808277ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34801561076a57600080fd5b506107c7600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff169060200190929190803577ffffffffffffffffffffffffffffffffffffffffffffffff1690602001909291905050506113be565b604051808215151515815260200191505060405180910390f35b606060018054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156108795780601f1061084e57610100808354040283529160200191610879565b820191906000526020600020905b81548152906001019060200180831161085c57829003601f168201915b5050505050905090565b600061088e826115bb565b1515610928576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252602c8152602001807f4552433732313a20617070726f76656420717565727920666f72206e6f6e657881526020017f697374656e7420746f6b656e000000000000000000000000000000000000000081525060400191505060405180910390fd5b6005600083815260200190815260200160002060009054906101000a900477ffffffffffffffffffffffffffffffffffffffffffffffff169050919050565b600061097282610eb6565b90508077ffffffffffffffffffffffffffffffffffffffffffffffff168377ffffffffffffffffffffffffffffffffffffffffffffffff1614151515610a46576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260218152602001807f4552433732313a20617070726f76616c20746f2063757272656e74206f776e6581526020017f720000000000000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b8077ffffffffffffffffffffffffffffffffffffffffffffffff163377ffffffffffffffffffffffffffffffffffffffffffffffff161480610a8e5750610a8d81336113be565b5b1515610b28576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260388152602001807f4552433732313a20617070726f76652063616c6c6572206973206e6f74206f7781526020017f6e6572206e6f7220617070726f76656420666f7220616c6c000000000000000081525060400191505060405180910390fd5b610b328383611633565b505050565b610b4133826116fc565b1515610bdb576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260318152602001807f4552433732313a207472616e736665722063616c6c6572206973206e6f74206f81526020017f776e6572206e6f7220617070726f76656400000000000000000000000000000081525060400191505060405180910390fd5b610be6838383611844565b505050565b6000809054906101000a900477ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff163377ffffffffffffffffffffffffffffffffffffffffffffffff16141515610c5257600080fd5b600077ffffffffffffffffffffffffffffffffffffffffffffffff168277ffffffffffffffffffffffffffffffffffffffffffffffff1614151515610cff576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260208152602001807f4552433732313a206d696e7420746f20746865207a65726f206164647265737381525060200191505060405180910390fd5b610d08816115bb565b151515610d7d576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252601c8152602001807f4552433732313a20746f6b656e20616c7265616479206d696e7465640000000081525060200191505060405180910390fd5b6001600460008477ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282540192505081905550816003600083815260200190815260200160002060006101000a81548177ffffffffffffffffffffffffffffffffffffffffffffffff021916908377ffffffffffffffffffffffffffffffffffffffffffffffff160217905550808277ffffffffffffffffffffffffffffffffffffffffffffffff16600077ffffffffffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60405160405180910390a45050565b610eb18383836020604051908101604052806000815250611241565b505050565b6000806003600084815260200190815260200160002060009054906101000a900477ffffffffffffffffffffffffffffffffffffffffffffffff169050600077ffffffffffffffffffffffffffffffffffffffffffffffff168177ffffffffffffffffffffffffffffffffffffffffffffffff1614151515610fc6576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260298152602001807f4552433732313a206f776e657220717565727920666f72206e6f6e657869737481526020017f656e7420746f6b656e000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b80915050919050565b60008077ffffffffffffffffffffffffffffffffffffffffffffffff168277ffffffffffffffffffffffffffffffffffffffffffffffff16141515156110a3576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252602a8152602001807f4552433732313a2062616c616e636520717565727920666f7220746865207a6581526020017f726f20616464726573730000000000000000000000000000000000000000000081525060400191505060405180910390fd5b600460008377ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050919050565b606060028054600181600116156101000203166002900480601f01602080910402602001604051908101604052809291908181526020018280546001816001161561010002031660029004801561118a5780601f1061115f5761010080835404028352916020019161118a565b820191906000526020600020905b81548152906001019060200180831161116d57829003601f168201915b5050505050905090565b61119f338383611b69565b5050565b60028054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156112395780601f1061120e57610100808354040283529160200191611239565b820191906000526020600020905b81548152906001019060200180831161121c57829003601f168201915b505050505081565b61124b33836116fc565b15156112e5576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260318152602001807f4552433732313a207472616e736665722063616c6c6572206973206e6f74206f81526020017f776e6572206e6f7220617070726f76656400000000000000000000000000000081525060400191505060405180910390fd5b6112f184848484611d2f565b50505050565b60018054600181600116156101000203166002900480601f01602080910402602001604051908101604052809291908181526020018280546001816001161561010002031660029004801561138d5780601f106113625761010080835404028352916020019161138d565b820191906000526020600020905b81548152906001019060200180831161137057829003601f168201915b505050505081565b6000809054906101000a900477ffffffffffffffffffffffffffffffffffffffffffffffff1681565b60008077ffffffffffffffffffffffffffffffffffffffffffffffff168377ffffffffffffffffffffffffffffffffffffffffffffffff161415151561146c576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260188152602001807f5f6f776e65722063616e206e6f7420626520656d70747921000000000000000081525060200191505060405180910390fd5b600077ffffffffffffffffffffffffffffffffffffffffffffffff168277ffffffffffffffffffffffffffffffffffffffffffffffff1614151515611519576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252601b8152602001807f5f6f70657261746f722063616e206e6f7420626520656d70747921000000000081525060200191505060405180910390fd5b600660008477ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008377ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff16905092915050565b60008077ffffffffffffffffffffffffffffffffffffffffffffffff166003600084815260200190815260200160002060009054906101000a900477ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff1614159050919050565b816005600083815260200190815260200160002060006101000a81548177ffffffffffffffffffffffffffffffffffffffffffffffff021916908377ffffffffffffffffffffffffffffffffffffffffffffffff160217905550808277ffffffffffffffffffffffffffffffffffffffffffffffff166116b283610eb6565b77ffffffffffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b92560405160405180910390a45050565b600080611708836115bb565b15156117a2576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252602c8152602001807f4552433732313a206f70657261746f7220717565727920666f72206e6f6e657881526020017f697374656e7420746f6b656e000000000000000000000000000000000000000081525060400191505060405180910390fd5b6117ab83610eb6565b90508077ffffffffffffffffffffffffffffffffffffffffffffffff168477ffffffffffffffffffffffffffffffffffffffffffffffff16148061182a57508377ffffffffffffffffffffffffffffffffffffffffffffffff1661180e84610883565b77ffffffffffffffffffffffffffffffffffffffffffffffff16145b8061183b575061183a81856113be565b5b91505092915050565b8277ffffffffffffffffffffffffffffffffffffffffffffffff1661186882610eb6565b77ffffffffffffffffffffffffffffffffffffffffffffffff1614151561191d576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260258152602001807f4552433732313a207472616e736665722066726f6d20696e636f72726563742081526020017f6f776e657200000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b600077ffffffffffffffffffffffffffffffffffffffffffffffff168277ffffffffffffffffffffffffffffffffffffffffffffffff16141515156119f0576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260248152602001807f4552433732313a207472616e7366657220746f20746865207a65726f2061646481526020017f726573730000000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b6119fb600082611633565b6001600460008577ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825403925050819055506001600460008477ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282540192505081905550816003600083815260200190815260200160002060006101000a81548177ffffffffffffffffffffffffffffffffffffffffffffffff021916908377ffffffffffffffffffffffffffffffffffffffffffffffff160217905550808277ffffffffffffffffffffffffffffffffffffffffffffffff168477ffffffffffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60405160405180910390a4505050565b8177ffffffffffffffffffffffffffffffffffffffffffffffff168377ffffffffffffffffffffffffffffffffffffffffffffffff1614151515611c15576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260198152602001807f4552433732313a20617070726f766520746f2063616c6c65720000000000000081525060200191505060405180910390fd5b80600660008577ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008477ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055508177ffffffffffffffffffffffffffffffffffffffffffffffff168377ffffffffffffffffffffffffffffffffffffffffffffffff167f17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c3183604051808215151515815260200191505060405180910390a3505050565b611d3a848484611844565b505050505600a165627a7a72305820229cc76b26c780cc5b5e0eafc5252d8ebce476526b28d6016709cbba2e6a58ee0029";
        Long initBalance = ToBaseUnit.ToUGas("0.01");
        String input="{\"function\":\"XHERC721(string,string)\",\"args\":\"'solidity Token','https://gateway.pinata.cloud/ipfs/QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/6476'\"}";
        BIFContractCreateRequest request = new BIFContractCreateRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setInitBalance(initBalance);
        request.setPayload(payload);
        request.setRemarks("create contract");
        request.setType(1);
        request.setGasPrice(10L);
        request.setFeeLimit(111549500L);
        request.setInitInput(input);

        // 调用bifContractCreate接口
        BIFContractCreateResponse response = sdk.getBIFContractService().contractCreate(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

交易hash：`9ddb2162353f09bedaa2c04932d7687e7675d9f82a9ba65c30a067f23618431b`

根据交易hash获取合约地址

```java
         // 合约部署返回值hash
        String hash = "9ddb2162353f09bedaa2c04932d7687e7675d9f82a9ba65c30a067f23618431b";
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

合约地址：`did:bid:efnm6ukPFx6wnEnMAWHV8LQMi5tiQgQu`

#### 合约调用

根据生成的合约地址进行合约调用操作

##### 铸造

```java
       // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:efnm6ukPFx6wnEnMAWHV8LQMi5tiQgQu";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input = "{\"function\":\"mint(address,uint256)\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i,2\"}";

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setGasPrice(10L);
        request.setRemarks("contract invoke");
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 转移

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:efnm6ukPFx6wnEnMAWHV8LQMi5tiQgQu";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input ="{\"function\":\"transferFrom(address,address,uint256)\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i,did:bid:efyhF492WhCEnXqSCjgQV6yUA2uPeAY3,2\"}";
        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 安全转移（携带 data）

```java
       // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:efnm6ukPFx6wnEnMAWHV8LQMi5tiQgQu";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input ="{\"function\":\"safeTransferFrom(address,address,uint256,bytes)\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i,did:bid:efyhF492WhCEnXqSCjgQV6yUA2uPeAY3,3,'safe transfer from'\"}";
        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 安全转移

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:efnm6ukPFx6wnEnMAWHV8LQMi5tiQgQu";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input ="{\"function\":\"safeTransferFrom(address,address,uint256)\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i,did:bid:efyhF492WhCEnXqSCjgQV6yUA2uPeAY3,4\"}";

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 授权

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:efnm6ukPFx6wnEnMAWHV8LQMi5tiQgQu";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input ="{\"function\":\"approve(address,uint256)\",\"args\":\"did:bid:efdvn6cS5TZgiM5ffVN9HQh3y72raYtm,5\"}";
        
        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 授权所有

```java
        //初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:efnm6ukPFx6wnEnMAWHV8LQMi5tiQgQu";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input ="{\"function\":\"setApprovalForAll(address,bool)\",\"args\":\"did:bid:efdvn6cS5TZgiM5ffVN9HQh3y72raYtm,1\"}";

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

#### 合约查询

##### 查询name

```java
        // 初始化参数
        String contractAddress = "did:bid:efnm6ukPFx6wnEnMAWHV8LQMi5tiQgQu";
        String input  = "{\"function\":\"name()\",\"return\":\"returns(string)\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询tokenId所属者

```java
        // 初始化参数
        String contractAddress = "did:bid:efnm6ukPFx6wnEnMAWHV8LQMi5tiQgQu";
        String input  =  "{\"function\":\"ownerOf(uint256)\",\"args\":\"1\",\"return\":\"returns(address)\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
       
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询代币数量

```java
        // 初始化参数
        String contractAddress = "did:bid:efnm6ukPFx6wnEnMAWHV8LQMi5tiQgQu";
        String input  = "{\"function\":\"balanceOf(address)\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i\",\"return\":\"returns(uint256)\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询授权地址

```java
        // 初始化参数
        String contractAddress = "did:bid:efnm6ukPFx6wnEnMAWHV8LQMi5tiQgQu";
        String input  = "{\"function\":\"getApproved(uint256)\",\"args\":\"5\",\"return\":\"returns(address)\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询是否被授权所有

```java
        // 初始化参数
        String contractAddress = "did:bid:efnm6ukPFx6wnEnMAWHV8LQMi5tiQgQu";
        String input  ="{\"function\":\"isApprovedForAll(address,address)\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i,did:bid:efdvn6cS5TZgiM5ffVN9HQh3y72raYtm\",\"return\":\"returns(bool)\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询symbol

```java
        // 初始化参数
        String contractAddress = "did:bid:efnm6ukPFx6wnEnMAWHV8LQMi5tiQgQu";
        String input  = "{\"function\":\"symbol()\",\"return\":\"returns(string)\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

### JavaScript合约

- **合约文件**

  ```javascript
  'use strict';
  const FUNDATION = "_fundation";
  const NAME = "_name";
  const SYMBOL = "_symbol";
  const TOKENURI = "_tokenUri";
  const BALANCEOF = "_balanceOf";
  var TOKENS = "_tokens";
  const ALLOWANCES = "_allowances";
  const ISALLAPPROVED = "_isAllApproved";
  const ALLTOKENS = "_allTokens";
  const ALLTOKENSINDEX = "_allTokensIndex";
  const OWNEDTOKENSINDEX = "_ownedTokensIndex";
  const OWNEDTOKENS = "_ownedTokens";
  const sender_g = Chain.msg.sender;
  const chainCode_g = Chain.chainCode;
  function isContractOwner() {
      var owner = Chain.load(FUNDATION);
      if (Chain.msg.sender === owner) {
          return true;
      } else {
          Utils.log("onlyFundation can call this method!");
          return false;
      }
  }
  function _setTokenURI(newuri) {
      Chain.store(TOKENURI, newuri);
  }
  function setTokenURI(params) {
      if (isContractOwner() === false) {
          Utils.log('setTokenURI' + Chain.msg.sender);
          return;
      }
      var tokenUri = params.tokenUri;
      _setTokenURI(tokenUri);
  }
  function init(input_str) {
      var input = JSON.parse(input_str);
      var params = input.params;
      Utils.log('input_str: (' + input_str + ').');
      if (params.name === undefined || params.symbol === undefined || params.tokenUri === undefined || !params.name.length || !params.symbol.length || !params.tokenUri.length) {
          Utils.assert(false, "DNA721: init  params is invalid, please check!");
      }
      Chain.store(NAME, params.name);
      Chain.store(SYMBOL, params.symbol);
      _setTokenURI(params.tokenUri);
      Chain.store(FUNDATION, sender_g);
      return;
  }
  function name() {
      return Chain.load("_name");
  }
  function symbol() {
      return Chain.load("_symbol");
  }
  function _exists(tokenId) {
      var tokens = {};
      var dataToken = JSON.parse(Chain.load(TOKENS));
      if (dataToken) {
          tokens = dataToken;
      }
      if (tokens[tokenId] !== undefined) {
          return true;
      } else {
          return false;
      }
  }
  function tokenURI(params) {
      var tokenId = params.tokenId;
      Utils.assert(Utils.addressCheck(tokenId), "DNA721: tokenURI for params: tokenId is invalid bid address");
      Utils.log('tokenId: ' + params.tokenId);
      Utils.assert(_exists(tokenId), "DNA721: URI query for nonexistent token");
      var tokenUri = Chain.load(TOKENURI);
      if (tokenUri.length > 0) {
          return tokenUri + tokenId;
      }
      return "";
  }
  function balanceOf(params) {
      var owner = params.owner;
      Utils.assert(Utils.addressCheck(owner), "DNA721: balanceOf query for params: owner is invalid bid address");
      var balances = {};
      var data = JSON.parse(Chain.load(BALANCEOF));
      if (data) {
          balances = data;
      }
      if (balances[owner] !== undefined) {
          return balances[owner];
      } else {
          return 0;
      }
  }
  function _ownerOf(tokenId) {
      var tokens = {};
      var dataToken = JSON.parse(Chain.load(TOKENS));
      if (dataToken) {
          tokens = dataToken;
      }
      var owner = "";
      if (tokens[tokenId] !== undefined) {
          owner = tokens[tokenId];
      }
      Utils.assert(owner.length !== 0, "DNA721: owner query for nonexistent token");
      return owner;
  }
  function ownerOf(params) {
      var tokenId = params.tokenId;
      Utils.assert(Utils.addressCheck(tokenId), "DNA721: ownerOf for params: tokenId is invalid bid address");
      return _ownerOf(tokenId);
  }
  function _addTokenToOwnerEnumeration(to, tokenId) {
      var ownedTokens = {};
      var data = JSON.parse(Chain.load(OWNEDTOKENS));
      if (data) {
          ownedTokens = data;
      }
      var ownedTokensIndex = {};
      var dataIndex = JSON.parse(Chain.load(OWNEDTOKENSINDEX));
      if (dataIndex) {
          ownedTokensIndex = dataIndex;
      }
      if (ownedTokens[to] !== undefined) {
          ownedTokensIndex[tokenId] = ownedTokens[to].length;
      } else {
          ownedTokens[to] = [];
          ownedTokensIndex[tokenId] = 0;
      }
      ownedTokens[to].push(tokenId);
      Chain.store(OWNEDTOKENS, JSON.stringify(ownedTokens));
      Chain.store(OWNEDTOKENSINDEX, JSON.stringify(ownedTokensIndex));
  }
  function _addTokenToAllTokensEnumeration(tokenId) {
      var allTokens = [];
      var dataAll = JSON.parse(Chain.load(ALLTOKENS));
      if (dataAll) {
          allTokens = dataAll;
      }
      var allTokensIndex = {};
      var data = JSON.parse(Chain.load(ALLTOKENSINDEX));
      if (data) {
          allTokensIndex = data;
      }
      allTokensIndex[tokenId] = allTokens.length;
      allTokens.push(tokenId);
      Chain.store(ALLTOKENS, JSON.stringify(allTokens));
      Chain.store(ALLTOKENSINDEX, JSON.stringify(allTokensIndex));
  }
  function _removeTokenFromOwnerEnumeration(from, tokenId) {
      var ownedTokens = {};
      var data = JSON.parse(Chain.load(OWNEDTOKENS));
      if (data) {
          ownedTokens = data;
      } else {
          Utils.assert(false, "DNA721: removeTokenFromOwnerEnumeration ownedTokens is null");
      }
      var ownedTokensIndex = {};
      var dataIndex = JSON.parse(Chain.load(OWNEDTOKENSINDEX));
      if (dataIndex) {
          ownedTokensIndex = dataIndex;
      }
      var lastTokenIndex = ownedTokens[from].length - 1;
      var tokenIndex = ownedTokensIndex[tokenId];
      if (tokenIndex !== lastTokenIndex) {
          var lastTokenId = ownedTokens[from][lastTokenIndex];
          ownedTokens[from][tokenIndex] = lastTokenId;
          ownedTokensIndex[lastTokenId] = tokenIndex;
      }
      ownedTokens[from].length = ownedTokens[from].length - 1;
      Chain.store(OWNEDTOKENS, JSON.stringify(ownedTokens));
      Chain.store(OWNEDTOKENSINDEX, JSON.stringify(ownedTokensIndex));
  }
  function mint(params) {
      if (isContractOwner() === false) {
          Utils.log('mint' + Chain.msg.sender);
          return;
      }
      var to = params.to;
      var tokenId = params.tokenId;
      Utils.log('mint-params: ' + params);
      Utils.assert(Utils.addressCheck(to), "DNA721: mint to is not bid address");
      Utils.assert(Utils.addressCheck(tokenId), "DNA721: mint tokenId is not bid address");
      Utils.assert(!_exists(tokenId), "DNA721: token already minted");
      var balances = {};
      var data = JSON.parse(Chain.load(BALANCEOF));
      if (data) {
          balances = data;
      }
      if (balances[to] !== undefined) {
          var temp = balances[to];
          balances[to] = temp + 1;
      } else {
          balances[to] = 1;
      }
      var tokens = {};
      var dataToken = JSON.parse(Chain.load(TOKENS));
      if (dataToken) {
          tokens = dataToken;
      }
      tokens[tokenId] = to;
      Chain.store(BALANCEOF, JSON.stringify(balances));
      Chain.store(TOKENS, JSON.stringify(tokens));
      _addTokenToOwnerEnumeration(to, tokenId);
      _addTokenToAllTokensEnumeration(tokenId);
      Chain.tlog('Transfer', '', to, tokenId);
  }
  function __setApproved(tokenId, to) {
      var allowances = {};
      var data = JSON.parse(Chain.load(ALLOWANCES));
      if (data) {
          allowances = data;
      }
      allowances[tokenId] = to;
      Chain.store(ALLOWANCES, JSON.stringify(allowances));
  }
  function _approve(to, tokenId) {
      __setApproved(tokenId, to);
      Chain.tlog('Approval', _ownerOf(tokenId), to, tokenId);
  }
  function _getApproved(tokenId) {
      Utils.assert(_exists(tokenId), "DNA721: approved query for nonexistent token");
      var allowances = {};
      var data = JSON.parse(Chain.load(ALLOWANCES));
      if (data) {
          allowances = data;
      }
      if (allowances[tokenId] !== undefined) {
          return allowances[tokenId];
      } else {
          return "";
      }
  }
  function getApproved(params) {
      var input = params;
      return _getApproved(input.tokenId);
  }
  function __getIsAllApproved(owner, to) {
      var allApproved = {};
      var data = JSON.parse(Chain.load(ISALLAPPROVED));
      if (data) {
          allApproved = data;
      }
      if (allApproved[owner] === undefined) {
          return false;
      }
      return allApproved[owner][to];
  }
  function _isApprovedForAll(owner, operator) {
      Utils.assert(Utils.addressCheck(owner), "DNA721: _isApprovedForAll params: owner is invalid bid address");
      Utils.assert(Utils.addressCheck(operator), "DNA721: _isApprovedForAll params: operator is invalid bid address");
      return __getIsAllApproved(owner, operator);
  }
  function isApprovedForAll(params) {
      var input = params;
      return _isApprovedForAll(input.owner, input.operator);
  }
  function __setAllApproved(owner, to, isAllApproved) {
      var allApproved = {};
      var data = JSON.parse(Chain.load(ISALLAPPROVED));
      if (data) {
          allApproved = data;
      }
      var inner_allApproved = {};
      if (allApproved[owner] === undefined) {
          allApproved[owner] = inner_allApproved;
      }
      Utils.log("allApproved:" + allApproved);
      allApproved[owner][to] = isAllApproved;
      Utils.log("allApproved after:" + allApproved);
      Chain.store(ISALLAPPROVED, JSON.stringify(allApproved));
  }
  function _setApprovalForAll(owner, operator, isApproved) {
      Utils.assert(Utils.addressCheck(owner), "DNA721: _setApprovalForAll params: owner is invalid bid address");
      Utils.assert(Utils.addressCheck(operator), "DNA721: _setApprovalForAll params: operator is invalid bid address");
      Utils.assert(owner !== operator, "DNA721: approve to caller");
      __setAllApproved(owner, operator, isApproved);
      Chain.tlog('ApprovalForAll', owner, operator, isApproved);
  }
  function setApprovalForAll(params) {
      return _setApprovalForAll(sender_g, params.operator, params.isApproved);
  }
  function _transfer(from, to, tokenId, data_params) {
      Utils.log('_ownerOf(tokenId): (' + _ownerOf(tokenId) + ').');
      Utils.log('from: (' + from + ').');
      Utils.assert(Utils.addressCheck(from), "DNA721: transfer params: from is invalid bid address");
      Utils.assert(Utils.addressCheck(to), "DNA721: transfer params: to is invalid bid address");
      Utils.assert(Utils.addressCheck(tokenId), "DNA721: transfer params: tokenId is invalid bid address");
      Utils.assert(_ownerOf(tokenId) === from, "DNA721: transfer from incorrect owner");
      _approve('', tokenId);
      var balances = {};
      var data = JSON.parse(Chain.load(BALANCEOF));
      if (data) {
          balances = data;
      }
      if (balances[from] !== undefined) {
          var temp = balances[from];
          balances[from] = temp - 1;
      }
      if (balances[to] !== undefined) {
          var tempTo = balances[to];
          balances[to] = tempTo + 1;
      } else {
          balances[to] = 1;
      }
      var tokens = {};
      var dataToken = JSON.parse(Chain.load(TOKENS));
      if (dataToken) {
          tokens = dataToken;
      }
      tokens[tokenId] = to;
      Chain.store(BALANCEOF, JSON.stringify(balances));
      Chain.store(TOKENS, JSON.stringify(tokens));
      _removeTokenFromOwnerEnumeration(from, tokenId);
      _addTokenToOwnerEnumeration(to, tokenId);
      Chain.tlog('Transfer', from, to, tokenId);
  }
  function _isApprovedOrOwner(spender, tokenId) {
      Utils.log("_exists(tokenId): " + _exists(tokenId));
      Utils.assert(_exists(tokenId), "DNA721: operator query for nonexistent token");
      var owner = _ownerOf(tokenId);
      Utils.log("owner: " + owner);
      Utils.log("_getApproved(tokenId): " + _getApproved(tokenId));
      Utils.log("_isApprovedForAll(owner, spender): " + _isApprovedForAll(owner, spender));
      return (spender === owner || _getApproved(tokenId) === spender || _isApprovedForAll(owner, spender));
  }
  function approve(params) {
      var input = params;
      Utils.assert(Utils.addressCheck(input.to), "DNA721: approve params: to is invalid bid address");
      Utils.assert(Utils.addressCheck(input.tokenId), "DNA721: approve params: tokenId is invalid bid address");
      var owner = _ownerOf(input.tokenId);
      Utils.assert(input.to !== owner, "DNA721: approval to current owner");
      Utils.log("approve-sender_g:" + sender_g + "  owner:" + owner);
      Utils.assert(sender_g === owner || _isApprovedForAll(owner, sender_g), "DNA721: approve caller is not owner nor approved for all");
      _approve(input.to, input.tokenId);
  }
  function transferFrom(params) {
      var input = params;
      Utils.assert(_isApprovedOrOwner(sender_g, input.tokenId), "DNA721: transfer caller is not owner nor approved");
      _transfer(input.from, input.to, input.tokenId, "");
  }
  function safeTransferFrom(params) {
      var from = params.from;
      var to = params.to;
      var tokenId = params.tokenId;
      var data = params.data;
      Utils.assert(_isApprovedOrOwner(sender_g, tokenId), "DNA721: transfer caller is not owner nor approved");
      _transfer(from, to, tokenId, data);
  }
  function totalSupply() {
      var allTokens = [];
      var dataAll = JSON.parse(Chain.load(ALLTOKENS));
      if (dataAll) {
          allTokens = dataAll;
      }
      return allTokens.length;
  }
  function tokenByIndex(params) {
      var index = params.index;
      Utils.assert(index % 1 === 0, "DNA721 tokenByIndex: your index should be int");
      Utils.assert(index >= 0, "DNA721 tokenByIndex: your index <= 0");
      Utils.assert(index < totalSupply(), "DNA721 tokenByIndex: global index out of bounds");
      var allTokens = [];
      var dataAll = JSON.parse(Chain.load(ALLTOKENS));
      if (dataAll) {
          allTokens = dataAll;
      }
      return allTokens[index];
  }
  function tokenOfOwnerByIndex(params) {
      var owner = params.owner;
      var index = params.index;
      Utils.assert(index % 1 === 0, "DNA721 tokenOfOwnerByIndex: your index should be int");
      Utils.assert(Utils.addressCheck(owner), "DNA721: tokenOfOwnerByIndex params: owner is invalid bid address");
      Utils.assert(index >= 0, "DNA721 tokenOfOwnerByIndex: your index <= 0");
      Utils.assert(index < balanceOf(params), "DNA721 Enumerable: owner index out of bounds");
      var ownedTokens = {};
      var data = JSON.parse(Chain.load(OWNEDTOKENS));
      if (data) {
          ownedTokens = data;
      }
      return ownedTokens[owner][index];
  }
  function main(input_str) {
      var input = JSON.parse(input_str);
      if (input.method === 'mint') {
          mint(input.params);
      } else if (input.method === 'transferFrom') {
          transferFrom(input.params);
      } else if (input.method === 'safeTransferFrom') {
          safeTransferFrom(input.params);
      } else if (input.method === 'approve') {
          approve(input.params);
      } else if (input.method === 'setApprovalForAll') {
          setApprovalForAll(input.params);
      } else {
          throw '<Main interface passes an invalid operation type>';
      }
  }
  function query(input_str) {
      var input = JSON.parse(input_str);
      var object = {};
      if (input.method === 'name') {
          object = name();
      } else if (input.method === 'symbol') {
          object = symbol();
      } else if (input.method === 'tokenURI') {
          object = tokenURI(input.params);
      } else if (input.method === 'totalSupply') {
          object = totalSupply();
      } else if (input.method === 'tokenByIndex') {
          object = tokenByIndex(input.params);
      } else if (input.method === 'tokenOfOwnerByIndex') {
          object = tokenOfOwnerByIndex(input.params);
      } else if (input.method === 'balanceOf') {
          object = balanceOf(input.params);
      } else if (input.method === 'ownerOf') {
          object = ownerOf(input.params);
      } else if (input.method === 'isApprovedForAll') {
          object = isApprovedForAll(input.params);
      } else if (input.method === 'getApproved') {
          object = getApproved(input.params);
      } else {
          throw '<unidentified operation type>';
      }
      return JSON.stringify(object);
  }
  ```

#### 合约部署

调用合约创建方法部署合约

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        String payload = "'use strict';const FUNDATION=\"_fundation\";const NAME=\"_name\";const SYMBOL=\"_symbol\";const TOKENURI=\"_tokenUri\";const BALANCEOF=\"_balanceOf\";var TOKENS=\"_tokens\";const ALLOWANCES=\"_allowances\";const ISALLAPPROVED=\"_isAllApproved\";const ALLTOKENS=\"_allTokens\";const ALLTOKENSINDEX=\"_allTokensIndex\";const OWNEDTOKENSINDEX=\"_ownedTokensIndex\";const OWNEDTOKENS=\"_ownedTokens\";const sender_g=Chain.msg.sender;const chainCode_g=Chain.chainCode;function isContractOwner(){var owner=Chain.load(FUNDATION);if(Chain.msg.sender===owner){return true;}else{Utils.log(\"onlyFundation can call this method!\");return false;}}function _setTokenURI(newuri){Chain.store(TOKENURI,newuri);}function setTokenURI(params){if(isContractOwner()===false){Utils.log('setTokenURI'+Chain.msg.sender);return;}var tokenUri=params.tokenUri;_setTokenURI(tokenUri);}function init(input_str){var input=JSON.parse(input_str);var params=input.params;Utils.log('input_str: ('+input_str+').');if(params.name===undefined||params.symbol===undefined||params.tokenUri===undefined||!params.name.length||!params.symbol.length||!params.tokenUri.length){Utils.assert(false,\"DNA721: init  params is invalid, please check!\");}Chain.store(NAME,params.name);Chain.store(SYMBOL,params.symbol);_setTokenURI(params.tokenUri);Chain.store(FUNDATION,sender_g);return;}function name(){return Chain.load(\"_name\");}function symbol(){return Chain.load(\"_symbol\");}function _exists(tokenId){var tokens={};var dataToken=JSON.parse(Chain.load(TOKENS));if(dataToken){tokens=dataToken;}if(tokens[tokenId]!==undefined){return true;}else{return false;}}function tokenURI(params){var tokenId=params.tokenId;Utils.assert(Utils.addressCheck(tokenId),\"DNA721: tokenURI for params: tokenId is invalid bid address\");Utils.log('tokenId: '+params.tokenId);Utils.assert(_exists(tokenId),\"DNA721: URI query for nonexistent token\");var tokenUri=Chain.load(TOKENURI);if(tokenUri.length>0){return tokenUri+tokenId;}return\"\";}function balanceOf(params){var owner=params.owner;Utils.assert(Utils.addressCheck(owner),\"DNA721: balanceOf query for params: owner is invalid bid address\");var balances={};var data=JSON.parse(Chain.load(BALANCEOF));if(data){balances=data;}if(balances[owner]!==undefined){return balances[owner];}else{return 0;}}function _ownerOf(tokenId){var tokens={};var dataToken=JSON.parse(Chain.load(TOKENS));if(dataToken){tokens=dataToken;}var owner=\"\";if(tokens[tokenId]!==undefined){owner=tokens[tokenId];}Utils.assert(owner.length!==0,\"DNA721: owner query for nonexistent token\");return owner;}function ownerOf(params){var tokenId=params.tokenId;Utils.assert(Utils.addressCheck(tokenId),\"DNA721: ownerOf for params: tokenId is invalid bid address\");return _ownerOf(tokenId);}function _addTokenToOwnerEnumeration(to,tokenId){var ownedTokens={};var data=JSON.parse(Chain.load(OWNEDTOKENS));if(data){ownedTokens=data;}var ownedTokensIndex={};var dataIndex=JSON.parse(Chain.load(OWNEDTOKENSINDEX));if(dataIndex){ownedTokensIndex=dataIndex;}if(ownedTokens[to]!==undefined){ownedTokensIndex[tokenId]=ownedTokens[to].length;}else{ownedTokens[to]=[];ownedTokensIndex[tokenId]=0;}ownedTokens[to].push(tokenId);Chain.store(OWNEDTOKENS,JSON.stringify(ownedTokens));Chain.store(OWNEDTOKENSINDEX,JSON.stringify(ownedTokensIndex));}function _addTokenToAllTokensEnumeration(tokenId){var allTokens=[];var dataAll=JSON.parse(Chain.load(ALLTOKENS));if(dataAll){allTokens=dataAll;}var allTokensIndex={};var data=JSON.parse(Chain.load(ALLTOKENSINDEX));if(data){allTokensIndex=data;}allTokensIndex[tokenId]=allTokens.length;allTokens.push(tokenId);Chain.store(ALLTOKENS,JSON.stringify(allTokens));Chain.store(ALLTOKENSINDEX,JSON.stringify(allTokensIndex));}function _removeTokenFromOwnerEnumeration(from,tokenId){var ownedTokens={};var data=JSON.parse(Chain.load(OWNEDTOKENS));if(data){ownedTokens=data;}else{Utils.assert(false,\"DNA721: removeTokenFromOwnerEnumeration ownedTokens is null\");}var ownedTokensIndex={};var dataIndex=JSON.parse(Chain.load(OWNEDTOKENSINDEX));if(dataIndex){ownedTokensIndex=dataIndex;}var lastTokenIndex=ownedTokens[from].length-1;var tokenIndex=ownedTokensIndex[tokenId];if(tokenIndex!==lastTokenIndex){var lastTokenId=ownedTokens[from][lastTokenIndex];ownedTokens[from][tokenIndex]=lastTokenId;ownedTokensIndex[lastTokenId]=tokenIndex;}ownedTokens[from].length=ownedTokens[from].length-1;Chain.store(OWNEDTOKENS,JSON.stringify(ownedTokens));Chain.store(OWNEDTOKENSINDEX,JSON.stringify(ownedTokensIndex));}function mint(params){if(isContractOwner()===false){Utils.log('mint'+Chain.msg.sender);return;}var to=params.to;var tokenId=params.tokenId;Utils.log('mint-params: '+params);Utils.assert(Utils.addressCheck(to),\"DNA721: mint to is not bid address\");Utils.assert(Utils.addressCheck(tokenId),\"DNA721: mint tokenId is not bid address\");Utils.assert(!_exists(tokenId),\"DNA721: token already minted\");var balances={};var data=JSON.parse(Chain.load(BALANCEOF));if(data){balances=data;}if(balances[to]!==undefined){var temp=balances[to];balances[to]=temp+1;}else{balances[to]=1;}var tokens={};var dataToken=JSON.parse(Chain.load(TOKENS));if(dataToken){tokens=dataToken;}tokens[tokenId]=to;Chain.store(BALANCEOF,JSON.stringify(balances));Chain.store(TOKENS,JSON.stringify(tokens));_addTokenToOwnerEnumeration(to,tokenId);_addTokenToAllTokensEnumeration(tokenId);Chain.tlog('Transfer','',to,tokenId);}function __setApproved(tokenId,to){var allowances={};var data=JSON.parse(Chain.load(ALLOWANCES));if(data){allowances=data;}allowances[tokenId]=to;Chain.store(ALLOWANCES,JSON.stringify(allowances));}function _approve(to,tokenId){__setApproved(tokenId,to);Chain.tlog('Approval',_ownerOf(tokenId),to,tokenId);}function _getApproved(tokenId){Utils.assert(_exists(tokenId),\"DNA721: approved query for nonexistent token\");var allowances={};var data=JSON.parse(Chain.load(ALLOWANCES));if(data){allowances=data;}if(allowances[tokenId]!==undefined){return allowances[tokenId];}else{return\"\";}}function getApproved(params){var input=params;return _getApproved(input.tokenId);}function __getIsAllApproved(owner,to){var allApproved={};var data=JSON.parse(Chain.load(ISALLAPPROVED));if(data){allApproved=data;}if(allApproved[owner]===undefined){return false;}return allApproved[owner][to];}function _isApprovedForAll(owner,operator){Utils.assert(Utils.addressCheck(owner),\"DNA721: _isApprovedForAll params: owner is invalid bid address\");Utils.assert(Utils.addressCheck(operator),\"DNA721: _isApprovedForAll params: operator is invalid bid address\");return __getIsAllApproved(owner,operator);}function isApprovedForAll(params){var input=params;return _isApprovedForAll(input.owner,input.operator);}function __setAllApproved(owner,to,isAllApproved){var allApproved={};var data=JSON.parse(Chain.load(ISALLAPPROVED));if(data){allApproved=data;}var inner_allApproved={};if(allApproved[owner]===undefined){allApproved[owner]=inner_allApproved;}Utils.log(\"allApproved:\"+allApproved);allApproved[owner][to]=isAllApproved;Utils.log(\"allApproved after:\"+allApproved);Chain.store(ISALLAPPROVED,JSON.stringify(allApproved));}function _setApprovalForAll(owner,operator,isApproved){Utils.assert(Utils.addressCheck(owner),\"DNA721: _setApprovalForAll params: owner is invalid bid address\");Utils.assert(Utils.addressCheck(operator),\"DNA721: _setApprovalForAll params: operator is invalid bid address\");Utils.assert(owner!==operator,\"DNA721: approve to caller\");__setAllApproved(owner,operator,isApproved);Chain.tlog('ApprovalForAll',owner,operator,isApproved);}function setApprovalForAll(params){return _setApprovalForAll(sender_g,params.operator,params.isApproved);}function _transfer(from,to,tokenId,data_params){Utils.log('_ownerOf(tokenId): ('+_ownerOf(tokenId)+').');Utils.log('from: ('+from+').');Utils.assert(Utils.addressCheck(from),\"DNA721: transfer params: from is invalid bid address\");Utils.assert(Utils.addressCheck(to),\"DNA721: transfer params: to is invalid bid address\");Utils.assert(Utils.addressCheck(tokenId),\"DNA721: transfer params: tokenId is invalid bid address\");Utils.assert(_ownerOf(tokenId)===from,\"DNA721: transfer from incorrect owner\");_approve('',tokenId);var balances={};var data=JSON.parse(Chain.load(BALANCEOF));if(data){balances=data;}if(balances[from]!==undefined){var temp=balances[from];balances[from]=temp-1;}if(balances[to]!==undefined){var tempTo=balances[to];balances[to]=tempTo+1;}else{balances[to]=1;}var tokens={};var dataToken=JSON.parse(Chain.load(TOKENS));if(dataToken){tokens=dataToken;}tokens[tokenId]=to;Chain.store(BALANCEOF,JSON.stringify(balances));Chain.store(TOKENS,JSON.stringify(tokens));_removeTokenFromOwnerEnumeration(from,tokenId);_addTokenToOwnerEnumeration(to,tokenId);Chain.tlog('Transfer',from,to,tokenId);}function _isApprovedOrOwner(spender,tokenId){Utils.log(\"_exists(tokenId): \"+_exists(tokenId));Utils.assert(_exists(tokenId),\"DNA721: operator query for nonexistent token\");var owner=_ownerOf(tokenId);Utils.log(\"owner: \"+owner);Utils.log(\"_getApproved(tokenId): \"+_getApproved(tokenId));Utils.log(\"_isApprovedForAll(owner, spender): \"+_isApprovedForAll(owner,spender));return(spender===owner||_getApproved(tokenId)===spender||_isApprovedForAll(owner,spender));}function approve(params){var input=params;Utils.assert(Utils.addressCheck(input.to),\"DNA721: approve params: to is invalid bid address\");Utils.assert(Utils.addressCheck(input.tokenId),\"DNA721: approve params: tokenId is invalid bid address\");var owner=_ownerOf(input.tokenId);Utils.assert(input.to!==owner,\"DNA721: approval to current owner\");Utils.log(\"approve-sender_g:\"+sender_g+\"  owner:\"+owner);Utils.assert(sender_g===owner||_isApprovedForAll(owner,sender_g),\"DNA721: approve caller is not owner nor approved for all\");_approve(input.to,input.tokenId);}function transferFrom(params){var input=params;Utils.assert(_isApprovedOrOwner(sender_g,input.tokenId),\"DNA721: transfer caller is not owner nor approved\");_transfer(input.from,input.to,input.tokenId,\"\");}function safeTransferFrom(params){var from=params.from;var to=params.to;var tokenId=params.tokenId;var data=params.data;Utils.assert(_isApprovedOrOwner(sender_g,tokenId),\"DNA721: transfer caller is not owner nor approved\");_transfer(from,to,tokenId,data);}function totalSupply(){var allTokens=[];var dataAll=JSON.parse(Chain.load(ALLTOKENS));if(dataAll){allTokens=dataAll;}return allTokens.length;}function tokenByIndex(params){var index=params.index;Utils.assert(index%1===0,\"DNA721 tokenByIndex: your index should be int\");Utils.assert(index>=0,\"DNA721 tokenByIndex: your index <= 0\");Utils.assert(index<totalSupply(),\"DNA721 tokenByIndex: global index out of bounds\");var allTokens=[];var dataAll=JSON.parse(Chain.load(ALLTOKENS));if(dataAll){allTokens=dataAll;}return allTokens[index];}function tokenOfOwnerByIndex(params){var owner=params.owner;var index=params.index;Utils.assert(index%1===0,\"DNA721 tokenOfOwnerByIndex: your index should be int\");Utils.assert(Utils.addressCheck(owner),\"DNA721: tokenOfOwnerByIndex params: owner is invalid bid address\");Utils.assert(index>=0,\"DNA721 tokenOfOwnerByIndex: your index <= 0\");Utils.assert(index<balanceOf(params),\"DNA721 Enumerable: owner index out of bounds\");var ownedTokens={};var data=JSON.parse(Chain.load(OWNEDTOKENS));if(data){ownedTokens=data;}return ownedTokens[owner][index];}function main(input_str){var input=JSON.parse(input_str);if(input.method==='mint'){mint(input.params);}else if(input.method==='transferFrom'){transferFrom(input.params);}else if(input.method==='safeTransferFrom'){safeTransferFrom(input.params);}else if(input.method==='approve'){approve(input.params);}else if(input.method==='setApprovalForAll'){setApprovalForAll(input.params);}else{throw'<Main interface passes an invalid operation type>';}}function query(input_str){var input=JSON.parse(input_str);var object={};if(input.method==='name'){object=name();}else if(input.method==='symbol'){object=symbol();}else if(input.method==='tokenURI'){object=tokenURI(input.params);}else if(input.method==='totalSupply'){object=totalSupply();}else if(input.method==='tokenByIndex'){object=tokenByIndex(input.params);}else if(input.method==='tokenOfOwnerByIndex'){object=tokenOfOwnerByIndex(input.params);}else if(input.method==='balanceOf'){object=balanceOf(input.params);}else if(input.method==='ownerOf'){object=ownerOf(input.params);}else if(input.method==='isApprovedForAll'){object=isApprovedForAll(input.params);}else if(input.method==='getApproved'){object=getApproved(input.params);}else{throw'<unidentified operation type>';}return JSON.stringify(object);}";
        Long initBalance = ToBaseUnit.ToUGas("0.01");
        String input="{\"params\":{\"name\":\"xinghuo space nft\",\"symbol\":\"symbol\",\"tokenUri\":\"https://gateway.pinata.cloud/ipfs/QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/6476\"}}";
        BIFContractCreateRequest request = new BIFContractCreateRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setInitBalance(initBalance);
        request.setPayload(payload);
        request.setRemarks("create contract");
        request.setType(0);
        request.setGasPrice(10L);
        request.setFeeLimit(111549500L);
        request.setInitInput(input);

        // 调用bifContractCreate接口
        BIFContractCreateResponse response = sdk.getBIFContractService().contractCreate(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

交易hash：`70ccb01e4d7e52df80f60b2c14de01d54be998377b4151ab152627d457051f2e`

根据交易`hash`获取合约地址

```java
        // 合约部署返回hash值
        String hash = "70ccb01e4d7e52df80f60b2c14de01d54be998377b4151ab152627d457051f2e";
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

合约地址：`did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9`

#### 合约调用

根据生成的合约地址进行合约调用操作

##### 铸造

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input = "{\"method\":\"mint\",\"params\":{\"to\":\"did:bid:ef21SesYy12yP9Pq24KQun3Xkk684gDuk\",\"tokenId\":\"did:bid:efvGbC617rnwabdxL4JxjnqGzqU97hhm\"}}";
        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setGasPrice(10L);
        request.setRemarks("contract invoke");
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 转移

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input ="{\"method\":\"transferFrom\",\"params\":{\"from\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i\",\"to\":\"did:bid:efDr1MFqET4kP2CnNJmYhXGdR6LTJmAt\",\"tokenId\":\"did:bid:efFasH3xkvS3fGsn72SqxZkrmreiuNzy\"}}";
        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
    
```

##### 安全转移（携带 data）

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input ="{\"method\":\"safeTransferFrom\",\"params\":{\"from\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i\",\"to\":\"did:bid:ef296hUUmhM8fgH9Gg7dyY3MH7P1tkpJU\",\"tokenId\":\"did:bid:efFasH3xkvS3fGsn72SqxZkrmreiuNzw\",\"data\":\"safe transfer with data\"}}";
        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 安全转移

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input ="{\"method\":\"safeTransferFrom\",\"params\":{\"from\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i\",\"to\":\"did:bid:ef296hUUmhM8fgH9Gg7dyY3MH7P1tkpJU\",\"tokenId\":\"did:bid:efFasH3xkvS3fGsn72SqxZkrmreiuNzk\"}}";

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
    
```

##### 授权

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input ="{\"method\":\"approve\",\"params\":{\"to\": \"did:bid:efDr1MFqET4kP2CnNJmYhXGdR6LTJmAt\",\"tokenId\":\"did:bid:ef25TXpxdvBQBngVABEhd64MJHhFsg6bu\"}}";

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 授权所有

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input ="{\"method\":\"setApprovalForAll\",\"params\":{\"operator\":\"did:bid:efHSbC7AedduvEG5hbtUio4mZmzwGhse\",\"isApproved\":false}}";

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
    
```

#### 合约查询

##### 查询name

```js
        // 初始化参数
        String contractAddress = "did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9";
        String input  = "{\"method\": \"name\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        //request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询tokenId所属者

```js
        // 初始化参数
        String contractAddress = "did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9";
        String input  =  "{\"method\":\"ownerOf\",\"params\":{\"tokenId\": \"did:bid:efvGbC617rnwabdxL4JxjnqGzqU97xxx\"}}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);

        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询代币数量

```js
        // 初始化参数
        String contractAddress = "did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9";
        String input  = "{\"method\":\"balanceOf\",\"params\":{\"owner\": \"did:bid:ef21SesYy12yP9Pq24KQun3Xkk684gDuk\"}}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        //request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询授权地址

```js
        // 初始化参数
        String contractAddress = "did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9";
        String input  = "{\"method\":\"getApproved\",\"params\":{\"tokenId\": \"did:bid:efvGbC617rnwabdxL4JxjnqGzqU97hhm\"}}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        //request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询是否被授权所有

```js
        // 初始化参数
        String contractAddress = "did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9";
        String input  ="{\"method\":\"isApprovedForAll\",\"params\":{\"owner\": \"did:bid:efHSbC7AedduvEG5hbtUio4mZmzwGhse\",\"operator\":\"did:bid:efYoXTEiQrKTUdoLiLsBDGneGtFMJRqM\"}}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        //request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询symbol

```js
        // 初始化参数
        String contractAddress = "did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9";
        String input  = "{\"method\": \"symbol\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        //request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询tokenUri

```js
        // 初始化参数
        String contractAddress = "did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9";
        String input  = "{\"method\":\"tokenURI\",\"params\":{\"tokenId\":\"did:bid:efvGbC617rnwabdxL4JxjnqGzqU97hhm\"}}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        //request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询totalSupply

```js
        // 初始化参数
        String contractAddress = "did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9";
        String input  = "{\"method\":\"totalSupply\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        //request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询tokenByIndex

```js
        // 初始化参数
        String contractAddress = "did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9";
        String input  = "{\"method\":\"tokenByIndex\",\"params\":{\"index\": 0}}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        //request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询tokenOfOwnerByIndex

```js
        // 初始化参数
        String contractAddress = "did:bid:ef67D5MHeB5go4Abp1dZRTnGoBXi6Pp9";
        String input  = "{\"method\":\"tokenOfOwnerByIndex\",\"params\":{\"owner\":\"did:bid:efDr1MFqET4kP2CnNJmYhXGdR6LTJmAt\", \"index\":0}}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        //request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##  ERC1155合约

本节描述通过星火链网实现并部署`ERC1155`智能合约。

`ERC1155`在一定程度上融合了`ERC-20`和`ERC-721`的功能。其主要用途包括了发行同质化代币和非同质化代币。同质化代币是指：能像`ERC-20`一样发布各样的代币类型；与此同时，`ERC-1155`标准更是能够发行NFT，且能基于一个合约同时发行多个NFT，有关`ERC1155`标准可以参考[官方文档](https://eips.ethereum.org/EIPS/eip-1155)。


### 合约说明

- **合约接口**

  注意：在实现转账功能时，如果接收方的地址没有拥有者，或者是一个合约地址，那么NFT被转出去之后，就意味着该NFT以后将没有流通的功能了。因此转账的时候，要慎重。若是合约地址，可以采取安全转账的方式，根据`ERC165`的方式判断该合约是否实现了onERC1155Received接口，若是没有实现，则智能合约的执行将被中止，若实现了，说明该合约遵守了`ERC1155`合约的标准，确保以后NFT可以进行流通，则转账继续。目前，在星火链网上实现的非同质化代币智能合约模板仅提供基础的功能，并没有提供安全转账的功能。
  
  | 接口                                                         | 返回值    | 描述                                                         |
  | ------------------------------------------------------------ | --------- | ------------------------------------------------------------ |
  | uri (uint256 _id)                                            | string    | 根据 _id 去查询的，通常为一个json字符串，描述了 NFT的图片、介绍等详细信息 |
  | safeTransferFrom(address _from, address _to, uint256 _id, uint256 _value, bytes calldata _data) ; | 无        | 代币转移接口，从 _from 账号发送  _value 个标识为 _id的代币到  _to 账号 |
  | safeBatchTransferFrom(address _from, address _to, uint256[] calldata _ids, uint256[] calldata _values, bytes calldata _data) | 无        | 批量代币转移接口，从 _from 账号发送  _values[i] 个标识为 _ids[i] 的代币到  _to 账号。_values  和 _ids数组需要长度一致。 |
  | balanceOf(address _owner, uint256 _id)                       | uint256   | 查询_owner 账户所持有的 标识为 _id 的代币 的数量             |
  | balanceOfBatch(address[] calldata _owners, uint256[] calldata _ids) | uint256[] | 查询 _owners[i]  账户所持有的 标识为  _ids[i]  的代币 的数量。_owners 和 _ids 数组需要长度一致。 |
  | setApprovalForAll(address , bool)                            | 无        | 设置授权                                                     |
  | isApprovedForAll(address , address)                          | bool      | 查询某个账户是否授权给某个账户                               |
  | onERC1155Received(address _operator, address _from, uint256 _id, uint256 _value, bytes calldata _data) | bytes4    | 在 safe转账下，具备接收NFT功能的智能合约必须实现该接口。     |
  | onERC1155BatchReceived(address _operator, address _from, uint256[] calldata _ids, uint256[] calldata _values, bytes calldata _data) | bytes4    | 在 safe批量转账下，具备接收NFT功能的智能合约必须实现该接口。 |

### Solidity合约

- **合约文件**

  ```javascript
  pragma solidity ^0.4.26;
  
  contract ERC1155 {
  
      // Mapping from token ID to account balances （某个代币 -- 某个账户地址 -- 金额）
      mapping(uint256 => mapping(address => uint256)) private _balances;
  
      // Mapping from account to operator approvals （账户地址A ---- 对账户地址B是否进行了授权） 
      mapping(address => mapping(address => bool)) private _operatorApprovals;
  
      // 链下的资源链接，用于记录保存token的具体介绍信息   https://token-cdn-domain/{id}.json
      string private _uri;
  
      // 单个转账时的事件
      event TransferSingle(address indexed operator, address indexed from, address indexed to, uint256 id, uint256 value);
      // 批量转账时的事件
      event TransferBatch( address indexed operator, address indexed from, address indexed to, uint256[] ids, uint256[] values
      );
      // 授权时的事件
      event ApprovalForAll(address indexed account, address indexed operator, bool approved);
      // 更新uri时的事件
      event URI(string value, uint256 indexed id);
      
      address public fundation; // 管理员
  
      modifier onlyFundation() {
          require(msg.sender == fundation);
          _;
      }
  
      /**
       * 初始化构造
       */
      function TokenERC1155(string memory uri_) public {
          fundation = msg.sender;    
          _setURI(uri_);                         
      }
      
      constructor(string memory uri_) {
          fundation = msg.sender;    
          _setURI(uri_);
      }
  
      function uri(uint256) public view  returns (string memory) {
          return _uri;
      }
  
      /**
       * 查询单个账户的余额
       * @param account 查询的账户地址
       * @param id 代币的标识符
       */
      function balanceOf(address account, uint256 id) public view returns (uint256) {
          require(account != address(0), "ERC1155: balance query for the zero address");
          return _balances[id][account];
      }
    
      /**
       * 批量查询多个账户的余额
       * @param accounts 查询的账户地址 数组
       * @param ids 代币的标识符 数组
       */
      function balanceOfBatch(address[] memory accounts, uint256[] memory ids)
          public
          view    
          returns (uint256[] memory)
      {
          require(accounts.length == ids.length, "ERC1155: accounts and ids length mismatch");
  
          uint256[] memory batchBalances = new uint256[](accounts.length);
  
          for (uint256 i = 0; i < accounts.length; ++i) {
              batchBalances[i] = balanceOf(accounts[i], ids[i]);
          }
  
          return batchBalances;
      }
  
      /**
       * 详见 _setApprovalForAll
       */
      function setApprovalForAll(address operator, bool approved) public {
          _setApprovalForAll(msg.sender, operator, approved);
      }
  
      /**
       * 查询账户是否授权给 某个账户
       * @param account 需要查询的账户地址
       * @param operator 授权的账户地址
       */
      function isApprovedForAll(address account, address operator) public view  returns (bool) {
          return _operatorApprovals[account][operator];
      }
  
      /**
       * 详见 _safeTransferFrom
       */
      function safeTransferFrom(
          address from,
          address to,
          uint256 id,
          uint256 amount,
          bytes memory data
      ) public  {
          require(
              from == msg.sender || isApprovedForAll(from, msg.sender),
              "ERC1155: caller is not owner nor approved"
          );
          _safeTransferFrom(from, to, id, amount, data);
      }
  
      /**
       * 详见 _safeBatchTransferFrom
       */
      function safeBatchTransferFrom(
          address from,
          address to,
          uint256[] memory ids,
          uint256[] memory amounts,
          bytes memory data
      ) public  {
          require(
              from == msg.sender || isApprovedForAll(from, msg.sender),
              "ERC1155: transfer caller is not owner nor approved"
          );
          _safeBatchTransferFrom(from, to, ids, amounts, data);
      }
  
      /**
       * 从from账户，转账 amount 个 token为id的资产到to账户。
       * @param from 转账的发送账户地址
       * @param to 转账的接收账户地址
       * @param id token的标识符
       * @param amount 转账的数量     
       * @param data 转账的信息
       */
      function _safeTransferFrom(
          address from,
          address to,
          uint256 id,
          uint256 amount,
          bytes memory data
      ) internal {
          require(to != address(0), "ERC1155: transfer to the zero address");
  
          address operator = msg.sender;
          uint256 fromBalance = _balances[id][from];
          require(fromBalance >= amount, "ERC1155: insufficient balance for transfer");
          _balances[id][from] = fromBalance - amount;
          _balances[id][to] += amount;
  
          emit TransferSingle(operator, from, to, id, amount);
      }
  
      /**
       * 从from账户批量转账资产到to账户。
       * @param from 转账的发送账户地址
       * @param to 转账的接收账户地址
       * @param ids token的标识符数组
       * @param amounts 转账的数量数组     
       * @param data 转账的信息
       */
      function _safeBatchTransferFrom(
          address from,
          address to,
          uint256[] memory ids,
          uint256[] memory amounts,
          bytes memory data
      ) internal {
          require(ids.length == amounts.length, "ERC1155: ids and amounts length mismatch");
          require(to != address(0), "ERC1155: transfer to the zero address");
  
          address operator = msg.sender;
          for (uint256 i = 0; i < ids.length; ++i) {
              uint256 id = ids[i];
              uint256 amount = amounts[i];
  
              uint256 fromBalance = _balances[id][from];
              require(fromBalance >= amount, "ERC1155: insufficient balance for transfer");
              _balances[id][from] = fromBalance - amount;
              _balances[id][to] += amount;
          }
  
          emit TransferBatch(operator, from, to, ids, amounts);
      }
    
      function _setURI(string memory newuri) internal {
          _uri = newuri;
      }
  
     /**
       * 铸造代币
       * @param to 接收账户地址
       * @param id token的标识符
       * @param amount 转账的数量     
       * @param data 转账的信息
       */
      function mint (
          address to,
          uint256 id,
          uint256 amount,
          bytes memory data
      ) onlyFundation public {
          require(to != address(0), "ERC1155: mint to the zero address");
  
          address operator = msg.sender;
          _balances[id][to] += amount;
          emit TransferSingle(operator, address(0), to, id, amount);
      }
  
     /**
       * 批量铸造代币
       * @param to 接收账户地址
       * @param ids token的标识符数组
       * @param amounts 转账的数量数组  
       * @param data 转账的信息
       */
      function mintBatch(
          address to,
          uint256[] memory ids,
          uint256[] memory amounts,
          bytes memory data
      ) onlyFundation public {
          require(to != address(0), "ERC1155: mint to the zero address");
          require(ids.length == amounts.length, "ERC1155: ids and amounts length mismatch");
  
          address operator = msg.sender;
  
          for (uint256 i = 0; i < ids.length; i++) {
              _balances[ids[i]][to] += amounts[i];
          }
          emit TransferBatch(operator, address(0), to, ids, amounts);
      }
  
      /**
       * 为账户下所有的资产设置授权
       * @param owner 需要授权的账户
       * @param operator 接受授权的账户
       * @param approved 是否授权
       */
      function _setApprovalForAll(
          address owner,
          address operator,
          bool approved
      ) internal {
          require(owner != operator, "ERC1155: setting approval status for self");
          _operatorApprovals[owner][operator] = approved;
          emit ApprovalForAll(owner, operator, approved);
      } 
  }
  ```

#### 合约部署

调用合约创建方法部署合约，solidity合约编译参考[星火链Solidity编译器](https://bif-doc.readthedocs.io/zh_CN/latest/app/solidity.html#id5)

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        String payload = "60806040523480156200001157600080fd5b5060405162002056380380620020568339810180604052810190808051820192919050505033600360006101000a81548177ffffffffffffffffffffffffffffffffffffffffffffffff021916908377ffffffffffffffffffffffffffffffffffffffffffffffff1602179055506200009981620000a0640100000000026401000000009004565b506200016b565b8060029080519060200190620000b8929190620000bc565b5050565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f10620000ff57805160ff191683800117855562000130565b8280016001018555821562000130579182015b828111156200012f57825182559160200191906001019062000112565b5b5090506200013f919062000143565b5090565b6200016891905b80821115620001645760008160009055506001016200014a565b5090565b90565b611edb806200017b6000396000f3006080604052600436106100ad576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168062949608146100b2578062fdd58e1461011b5780630e89341c146101805780631f7fdffa146102265780632eb2c2d6146103395780634e1273f414610470578063731133e91461056e578063a22cb4651461060f578063e0a9be7514610662578063e985e9c5146106c1578063f242432a14610744575b600080fd5b3480156100be57600080fd5b50610119600480360381019080803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290505050610809565b005b34801561012757600080fd5b5061016a600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff1690602001909291908035906020019092919050505061085e565b6040518082815260200191505060405180910390f35b34801561018c57600080fd5b506101ab60048036038101908080359060200190929190505050610992565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156101eb5780820151818401526020810190506101d0565b50505050905090810190601f1680156102185780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34801561023257600080fd5b50610337600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff1690602001909291908035906020019082018035906020019080806020026020016040519081016040528093929190818152602001838360200280828437820191505050505050919291929080359060200190820180359060200190808060200260200160405190810160405280939291908181526020018383602002808284378201915050505050509192919290803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290505050610a36565b005b34801561034557600080fd5b5061046e600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff169060200190929190803577ffffffffffffffffffffffffffffffffffffffffffffffff1690602001909291908035906020019082018035906020019080806020026020016040519081016040528093929190818152602001838360200280828437820191505050505050919291929080359060200190820180359060200190808060200260200160405190810160405280939291908181526020018383602002808284378201915050505050509192919290803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290505050610ddf565b005b34801561047c57600080fd5b506105176004803603810190808035906020019082018035906020019080806020026020016040519081016040528093929190818152602001838360200280828437820191505050505050919291929080359060200190820180359060200190808060200260200160405190810160405280939291908181526020018383602002808284378201915050505050509192919290505050610ed5565b6040518080602001828103825283818151815260200191508051906020019060200280838360005b8381101561055a57808201518184015260208101905061053f565b505050509050019250505060405180910390f35b34801561057a57600080fd5b5061060d600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff1690602001909291908035906020019092919080359060200190929190803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290505050611024565b005b34801561061b57600080fd5b50610660600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff169060200190929190803515159060200190929190505050611261565b005b34801561066e57600080fd5b50610677611270565b604051808277ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b3480156106cd57600080fd5b5061072a600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff169060200190929190803577ffffffffffffffffffffffffffffffffffffffffffffffff16906020019092919050505061129a565b604051808215151515815260200191505060405180910390f35b34801561075057600080fd5b50610807600480360381019080803577ffffffffffffffffffffffffffffffffffffffffffffffff169060200190929190803577ffffffffffffffffffffffffffffffffffffffffffffffff1690602001909291908035906020019092919080359060200190929190803590602001908201803590602001908080601f016020809104026020016040519081016040528093929190818152602001838380828437820191505050505050919291929050505061133e565b005b33600360006101000a81548177ffffffffffffffffffffffffffffffffffffffffffffffff021916908377ffffffffffffffffffffffffffffffffffffffffffffffff16021790555061085b81611434565b50565b60008077ffffffffffffffffffffffffffffffffffffffffffffffff168377ffffffffffffffffffffffffffffffffffffffffffffffff1614151515610932576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252602b8152602001807f455243313135353a2062616c616e636520717565727920666f7220746865207a81526020017f65726f206164647265737300000000000000000000000000000000000000000081525060400191505060405180910390fd5b60008083815260200190815260200160002060008477ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905092915050565b606060028054600181600116156101000203166002900480601f016020809104026020016040519081016040528092919081815260200182805460018160011615610100020316600290048015610a2a5780601f106109ff57610100808354040283529160200191610a2a565b820191906000526020600020905b815481529060010190602001808311610a0d57829003601f168201915b50505050509050919050565b600080600360009054906101000a900477ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff163377ffffffffffffffffffffffffffffffffffffffffffffffff16141515610aa157600080fd5b600077ffffffffffffffffffffffffffffffffffffffffffffffff168677ffffffffffffffffffffffffffffffffffffffffffffffff1614151515610b74576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260218152602001807f455243313135353a206d696e7420746f20746865207a65726f2061646472657381526020017f730000000000000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b83518551141515610c13576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260288152602001807f455243313135353a2069647320616e6420616d6f756e7473206c656e6774682081526020017f6d69736d6174636800000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b339150600090505b8451811015610cc4578381815181101515610c3257fe5b906020019060200201516000808784815181101515610c4d57fe5b90602001906020020151815260200190815260200160002060008877ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825401925050819055508080600101915050610c1b565b8577ffffffffffffffffffffffffffffffffffffffffffffffff16600077ffffffffffffffffffffffffffffffffffffffffffffffff168377ffffffffffffffffffffffffffffffffffffffffffffffff167f4a39dc06d4c0dbc64b70af90fd698a233a518aa5d07e595d983b8c0526c8f7fb8888604051808060200180602001838103835285818151815260200191508051906020019060200280838360005b83811015610d80578082015181840152602081019050610d65565b50505050905001838103825284818151815260200191508051906020019060200280838360005b83811015610dc2578082015181840152602081019050610da7565b5050505090500194505050505060405180910390a4505050505050565b3377ffffffffffffffffffffffffffffffffffffffffffffffff168577ffffffffffffffffffffffffffffffffffffffffffffffff161480610e275750610e26853361129a565b5b1515610ec1576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260328152602001807f455243313135353a207472616e736665722063616c6c6572206973206e6f742081526020017f6f776e6572206e6f7220617070726f766564000000000000000000000000000081525060400191505060405180910390fd5b610ece858585858561144e565b5050505050565b606080600083518551141515610f79576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260298152602001807f455243313135353a206163636f756e747320616e6420696473206c656e67746881526020017f206d69736d61746368000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b8451604051908082528060200260200182016040528015610fa95781602001602082028038833980820191505090505b509150600090505b845181101561101957610ff28582815181101515610fcb57fe5b906020019060200201518583815181101515610fe357fe5b9060200190602002015161085e565b828281518110151561100057fe5b9060200190602002018181525050806001019050610fb1565b819250505092915050565b6000600360009054906101000a900477ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff163377ffffffffffffffffffffffffffffffffffffffffffffffff1614151561108e57600080fd5b600077ffffffffffffffffffffffffffffffffffffffffffffffff168577ffffffffffffffffffffffffffffffffffffffffffffffff1614151515611161576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260218152602001807f455243313135353a206d696e7420746f20746865207a65726f2061646472657381526020017f730000000000000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b3390508260008086815260200190815260200160002060008777ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825401925050819055508477ffffffffffffffffffffffffffffffffffffffffffffffff16600077ffffffffffffffffffffffffffffffffffffffffffffffff168277ffffffffffffffffffffffffffffffffffffffffffffffff167fc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f628787604051808381526020018281526020019250505060405180910390a45050505050565b61126c3383836118f1565b5050565b600360009054906101000a900477ffffffffffffffffffffffffffffffffffffffffffffffff1681565b6000600160008477ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008377ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff16905092915050565b3377ffffffffffffffffffffffffffffffffffffffffffffffff168577ffffffffffffffffffffffffffffffffffffffffffffffff1614806113865750611385853361129a565b5b1515611420576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260298152602001807f455243313135353a2063616c6c6572206973206e6f74206f776e6572206e6f7281526020017f20617070726f766564000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b61142d8585858585611add565b5050505050565b806002908051906020019061144a929190611e0a565b5050565b6000806000806000865188511415156114f5576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260288152602001807f455243313135353a2069647320616e6420616d6f756e7473206c656e6774682081526020017f6d69736d6174636800000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b600077ffffffffffffffffffffffffffffffffffffffffffffffff168977ffffffffffffffffffffffffffffffffffffffffffffffff16141515156115c8576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260258152602001807f455243313135353a207472616e7366657220746f20746865207a65726f20616481526020017f647265737300000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b339450600093505b87518410156117d35787848151811015156115e757fe5b906020019060200201519250868481518110151561160157fe5b90602001906020020151915060008084815260200190815260200160002060008b77ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050818110151515611705576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252602a8152602001807f455243313135353a20696e73756666696369656e742062616c616e636520666f81526020017f72207472616e736665720000000000000000000000000000000000000000000081525060400191505060405180910390fd5b81810360008085815260200190815260200160002060008c77ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508160008085815260200190815260200160002060008b77ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825401925050819055508360010193506115d0565b8877ffffffffffffffffffffffffffffffffffffffffffffffff168a77ffffffffffffffffffffffffffffffffffffffffffffffff168677ffffffffffffffffffffffffffffffffffffffffffffffff167f4a39dc06d4c0dbc64b70af90fd698a233a518aa5d07e595d983b8c0526c8f7fb8b8b604051808060200180602001838103835285818151815260200191508051906020019060200280838360005b8381101561188e578082015181840152602081019050611873565b50505050905001838103825284818151815260200191508051906020019060200280838360005b838110156118d05780820151818401526020810190506118b5565b5050505090500194505050505060405180910390a450505050505050505050565b8177ffffffffffffffffffffffffffffffffffffffffffffffff168377ffffffffffffffffffffffffffffffffffffffffffffffff16141515156119c3576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260298152602001807f455243313135353a2073657474696e6720617070726f76616c2073746174757381526020017f20666f722073656c66000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b80600160008577ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008477ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055508177ffffffffffffffffffffffffffffffffffffffffffffffff168377ffffffffffffffffffffffffffffffffffffffffffffffff167f17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c3183604051808215151515815260200191505060405180910390a3505050565b600080600077ffffffffffffffffffffffffffffffffffffffffffffffff168677ffffffffffffffffffffffffffffffffffffffffffffffff1614151515611bb3576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260258152602001807f455243313135353a207472616e7366657220746f20746865207a65726f20616481526020017f647265737300000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b33915060008086815260200190815260200160002060008877ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050838110151515611cae576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252602a8152602001807f455243313135353a20696e73756666696369656e742062616c616e636520666f81526020017f72207472616e736665720000000000000000000000000000000000000000000081525060400191505060405180910390fd5b83810360008087815260200190815260200160002060008977ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508360008087815260200190815260200160002060008877ffffffffffffffffffffffffffffffffffffffffffffffff1677ffffffffffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825401925050819055508577ffffffffffffffffffffffffffffffffffffffffffffffff168777ffffffffffffffffffffffffffffffffffffffffffffffff168377ffffffffffffffffffffffffffffffffffffffffffffffff167fc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f628888604051808381526020018281526020019250505060405180910390a450505050505050565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f10611e4b57805160ff1916838001178555611e79565b82800160010185558215611e79579182015b82811115611e78578251825591602001919060010190611e5d565b5b509050611e869190611e8a565b5090565b611eac91905b80821115611ea8576000816000905550600101611e90565b5090565b905600a165627a7a723058202cb08bc70ce945f31ffb6297d360209caf45707bdb90f8264980ffa0385f90a40029";
        Long initBalance = ToBaseUnit.ToUGas("0.01");
        String input=
        "{\"function\":\"ERC1155(string)\",\"args\":\"'https://gateway.pinata.cloud/ipfs/QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/6476'\"}"
        BIFContractCreateRequest request = new BIFContractCreateRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setInitBalance(initBalance);
        request.setPayload(payload);
        request.setRemarks("create contract");
        request.setType(1);
        request.setGasPrice(10L);
        request.setFeeLimit(111549500L);
        request.setInitInput(input);

        // 调用bifContractCreate接口
        BIFContractCreateResponse response = sdk.getBIFContractService().contractCreate(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

交易hash：`920f982fa02d338cd7436ba6613e9825fdd7e97f5bf379e63dd366c9732847df`

根据交易hash获取合约地址

```java
        // 合约部署返回值hash
        String hash = "920f982fa02d338cd7436ba6613e9825fdd7e97f5bf379e63dd366c9732847df";
        BIFContractGetAddressRequest request = new BIFContractGetAddressRequest();
        request.setHash(hash);
        request.setDomainId(0);

        // Call getAddress
        BIFContractGetAddressResponse response = sdk.getBIFContractService().getContractAddress(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

合约地址：`did:bid:ef2AmWpsF2EaQfJjff3BPt8YNRsrt4van`

#### 合约调用

根据生成的合约地址进行合约调用操作

##### 铸造

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:ef2AmWpsF2EaQfJjff3BPt8YNRsrt4van";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String input="{\"function\":\"mint(address,uint256,uint256,bytes)\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i,1,10,'DNA 1155'\"}";

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
		request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 批量铸造

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:ef2AmWpsF2EaQfJjff3BPt8YNRsrt4van";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input="{\"function\":\"mintBatch(address,uint256[],uint256[],bytes)\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i,[2,3],[10,100],'DNA 1155'\"}";

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 安全转移

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:ef2AmWpsF2EaQfJjff3BPt8YNRsrt4van";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String input="{\"function\":\"safeTransferFrom(address,address,uint256,uint256,bytes)\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i,did:bid:efdvn6cS5TZgiM5ffVN9HQh3y72raYtm,1,1,'safe transfer from'\"}";
        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 批量安全转移

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:ef2AmWpsF2EaQfJjff3BPt8YNRsrt4van";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input = "{\"function\":\"safeBatchTransferFrom(address,address,uint256[],uint256[],bytes)\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i,did:bid:efdvn6cS5TZgiM5ffVN9HQh3y72raYtm,[2,3],[1,1],'safe transfer from'\"}";
        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 授权所有

```java
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:ef2AmWpsF2EaQfJjff3BPt8YNRsrt4van";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String input ="{\"function\":\"setApprovalForAll(address,bool)\",\"args\":\"did:bid:efdvn6cS5TZgiM5ffVN9HQh3y72raYtm,1\"}";

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

#### 合约查询

##### 查询代币数量

```java
        // 初始化参数
        String contractAddress = "did:bid:ef2AmWpsF2EaQfJjff3BPt8YNRsrt4van";
        String input  = "{\"function\":\"balanceOf(address,uint256)\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i,2\",\"return\":\"returns(uint256)\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 批量查询代币数量

```java
        // 初始化参数
        String contractAddress = "did:bid:ef2AmWpsF2EaQfJjff3BPt8YNRsrt4van";
        String input  ="{\"function\":\"balanceOfBatch(address[],uint256[])\",\"args\":\"[did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i],[2]\",\"return\":\"returns(uint256[])\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询是否被授权所有

```java
        // 初始化参数
        String contractAddress = "did:bid:ef5r2WoTsUd6fAUKQtLvpvf39aM48hn7";
        String input = "{\"function\":\"isApprovedForAll(address,address)\",\"args\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i,did:bid:efdvn6cS5TZgiM5ffVN9HQh3y72raYtm\",\"return\":\"returns(bool)\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询Uri

```java
        // 初始化参数
        String contractAddress = "did:bid:ef5r2WoTsUd6fAUKQtLvpvf39aM48hn7";
        String input="{\"function\":\"uri(uint256)\",\"args\":\"5\",\"return\":\"returns(string)\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

### JavaScript合约

- **合约文件**

  ```javascript
  'use strict';
  const FUNDATION = "_fundation";
  const NAME = "_name";
  const SYMBOL = "_symbol";
  const URI = "_uri";
  const ALLTOKENS = "_allTokens";
  const BALANCES = "_balances";
  const OPERATORAPPROVALS = "_operatorApprovals";
  const sender_g = Chain.msg.sender;
  const chainCode_g = Chain.chainCode;
  function isContractOwner() {
    var owner = Chain.load(FUNDATION);
    if (Chain.msg.sender === owner) {
      return true;
    } else {
      Utils.log("onlyFundation can call this method!");
      return false;
    }
  }
  function _setURI(newuri) {
    Chain.tlog('URI', newuri);
    Chain.store(URI, newuri);
  }
  function setURI(params) {
    if (isContractOwner() === false) {
      Utils.log('setURI' + Chain.msg.sender);
      return;
    }
    var uri = params.uri;
    _setURI(uri);
  }
  function init(input_str) {
    var input = JSON.parse(input_str);
    var params = input.params;
    Utils.log('input_str: (' + input_str + ').');
    if (params.name === undefined || params.symbol === undefined || params.uri === undefined || !params.name.length || !params.symbol.length || !params.uri.length) {
      Utils.assert(false, "DNA1155: init  params is invalid, please check!");
    }
    Chain.store(NAME, params.name);
    Chain.store(SYMBOL, params.symbol);
    _setURI(params.uri);
    Chain.store(FUNDATION, sender_g);
  }
  function name() {
    return Chain.load(NAME);
  }
  function symbol() {
    return Chain.load(SYMBOL);
  }
  function _exists(tokenId) {
    var tokens = {};
    var dataToken = JSON.parse(Chain.load(ALLTOKENS));
    if (dataToken) {
      tokens = dataToken;
    }
    if (tokens[tokenId] === undefined || tokens[tokenId] === 0) {
      return false;
    } else {
      return true;
    }
  }
  function _uri(tokenId) {
    Utils.log('tokenId: ' + tokenId);
    Utils.assert(_exists(tokenId), "DNA1155: URI query for nonexistent token");
    var uri = Chain.load(URI);
    if (uri.length > 0) {
      return uri + tokenId;
    }
    return "";
  }
  function uri(params) {
    var tokenId = params.tokenId;
    Utils.assert(Utils.addressCheck(tokenId), "DNA1155: uri params: tokenId is invalid bid address");
    return _uri(tokenId);
  }
  function _getBalanceOf(id, account) {
    var balances = {};
    var data = JSON.parse(Chain.load(BALANCES));
    if (data) {
      balances = data;
    }
    var inner_balances = {};
    if (balances[id] === undefined) {
      balances[id] = inner_balances;
    }
    if (balances[id][account] === undefined) {
      return 0;
    }
    return balances[id][account];
  }
  function _setBalanceOfForKey(id, account, value) {
    var balances = {};
    var data = JSON.parse(Chain.load(BALANCES));
    if (data) {
      balances = data;
    }
    var inner_balances = {};
    if (balances[id] === undefined) {
      balances[id] = inner_balances;
    }
    balances[id][account] = value;
    Utils.log("balances:" + balances);
    Chain.store(BALANCES, JSON.stringify(balances));
  }
  function balanceOf(params) {
    var account = params.account;
    var id = params.id;
    Utils.assert(Utils.addressCheck(account), "DNA1155: balanceOf params: owner is invalid bid address");
    Utils.assert(Utils.addressCheck(id), "DNA1155: balanceOf params: tokenId is invalid bid address");
    return _getBalanceOf(id, account);
  }
  function balanceOfBatch(params) {
    var accounts = params.accounts;
    var ids = params.ids;
    Utils.assert(accounts.length === ids.length, "ERC1155: accounts and ids length mismatch");
    var batchBalances = [];
    var i = 0;
    for (i = 0; i < accounts.length; i += 1) {
      Utils.assert(Utils.addressCheck(accounts[i]), "DNA1155: balanceOfBatch params: owner is invalid bid address");
      Utils.assert(Utils.addressCheck(ids[i]), "DNA1155: balanceOfBatch params: tokenId is invalid bid address");
      batchBalances[i] = _getBalanceOf(ids[i], accounts[i]);
    }
    return JSON.stringify(batchBalances);
  }
  function __setAllApproved(owner, to, isAllApproved) {
    var allApproved = {};
    var data = JSON.parse(Chain.load(OPERATORAPPROVALS));
    if (data) {
      allApproved = data;
    }
    var inner_allApproved = {};
    if (allApproved[owner] === undefined) {
      allApproved[owner] = inner_allApproved;
    }
    allApproved[owner][to] = isAllApproved;
    Utils.log("allApproved:" + allApproved);
    Chain.store(OPERATORAPPROVALS, JSON.stringify(allApproved));
  }
  function _setApprovalForAll(owner, operator, isApproved) {
    Utils.assert(owner !== operator, "ERC1155: setting approval status for self");
    __setAllApproved(owner, operator, isApproved);
    Chain.tlog('ApprovalForAll', owner, operator, isApproved);
  }
  function setApprovalForAll(params) {
    var operator = params.operator;
    var isApproved = params.isApproved;
    Utils.assert(Utils.addressCheck(operator), "ERC1155: setApprovalForAll params: operator is invalid bid address");
    _setApprovalForAll(sender_g, operator, isApproved);
  }
  function __getIsAllApproved(owner, to) {
    var allApproved = {};
    var data = JSON.parse(Chain.load(OPERATORAPPROVALS));
    if (data) {
      allApproved = data;
    }
    var inner_allApproved = {};
    if (allApproved[owner] === undefined) {
      allApproved[owner] = inner_allApproved;
    }
    if (allApproved[owner][to] === undefined) {
      return false;
    }
    return allApproved[owner][to];
  }
  function _isApprovedForAll(owner, operator) {
    Utils.assert(Utils.addressCheck(owner), "ERC1155: _isApprovedForAll params: owner is invalid bid address");
    Utils.assert(Utils.addressCheck(operator), "ERC1155: _isApprovedForAll params: operator is invalid bid address");
    return __getIsAllApproved(owner, operator);
  }
  function isApprovedForAll(params) {
    var account = params.account;
    var operator = params.operator;
    return _isApprovedForAll(account, operator);
  }
  function _safeTransferFrom(from, to, id, amount, data) {
    Utils.assert(to.length > 0, "ERC1155: transfer to the zero address");
    var operator = sender_g;
    var fromBalance = _getBalanceOf(id, from);
    Utils.assert(fromBalance >= amount, "ERC1155: insufficient balance for transfer");
    _setBalanceOfForKey(id, from, fromBalance - amount);
    var toBalance = _getBalanceOf(id, to);
    _setBalanceOfForKey(id, to, toBalance + amount);
    Chain.tlog('TransferSingle', operator, from, to, id, amount);
  }
  function _checkAmount(amount) {
    Utils.assert(amount !== undefined, "ERC1155: params: amount must have a value");
    Utils.assert(amount > 0, "ERC1155: params: amount must > 0");
    Utils.assert(amount % 1 === 0, "ERC1155 params: your amount should be int");
  }
  function safeTransferFrom(params) {
    var from = params.from;
    var to = params.to;
    var id = params.id;
    var amount = params.amount;
    var data = params.data;
    Utils.assert(Utils.addressCheck(from), "ERC1155: safeTransferFrom params: from is invalid bid address");
    Utils.assert(Utils.addressCheck(to), "ERC1155: safeTransferFrom params: to is invalid bid address");
    Utils.assert(Utils.addressCheck(id), "ERC1155: safeTransferFrom params: id is invalid bid address");
    _checkAmount(amount);
    Utils.assert(from === sender_g || _isApprovedForAll(from, sender_g), "ERC1155: caller is not owner nor approved");
    _safeTransferFrom(from, to, id, amount, data);
  }
  function _safeBatchTransferFrom(from, to, ids, amounts, data) {
    Utils.assert(ids.length === amounts.length, "ERC1155:  ids and amounts length mismatch");
    Utils.assert(to.length > 0, "ERC1155:  transfer to the zero address");
    var operator = sender_g;
    var i = 0;
    var id;
    var amount;
    var fromBalance;
    var toBalance;
    for (i = 0; i < ids.length; i += 1) {
      id = ids[i];
      amount = amounts[i];
      _checkAmount(amount);
      fromBalance = _getBalanceOf(id, from);
      Utils.assert(fromBalance >= amount, "ERC1155:  insufficient balance for transfer");
      _setBalanceOfForKey(id, from, fromBalance - amount);
      toBalance = _getBalanceOf(id, to);
      _setBalanceOfForKey(id, to, toBalance + amount);
    }
    Chain.tlog('TransferBatch', operator, from, to, JSON.stringify(ids), JSON.stringify(amounts));
  }
  function safeBatchTransferFrom(params) {
    var from = params.from;
    var to = params.to;
    var ids = params.ids;
    var amounts = params.amounts;
    var data = params.data;
    Utils.assert(Utils.addressCheck(from), "ERC1155: safeBatchTransferFrom params: from is invalid bid address");
    Utils.assert(Utils.addressCheck(to), "ERC1155: safeBatchTransferFrom params: to is invalid bid address");
    var i = 0;
    for (i = 0; i < ids.length; i += 1) {
      Utils.assert(Utils.addressCheck(ids[i]), "ERC1155: safeBatchTransferFrom params: id is invalid bid address");
    }
    Utils.assert(from === sender_g || _isApprovedForAll(from, sender_g), "ERC1155: caller is not owner nor approved");
    _safeBatchTransferFrom(from, to, ids, amounts, data);
  }
  function _addTokenToAllTokensEnumeration(tokenId, amount) {
    var allTokens = {};
    var dataAll = JSON.parse(Chain.load(ALLTOKENS));
    if (dataAll) {
      allTokens = dataAll;
    }
    var counter = 0;
    if (allTokens[tokenId] === undefined) {
      allTokens[tokenId] = counter;
    }
    allTokens[tokenId] += amount;
    Chain.store(ALLTOKENS, JSON.stringify(allTokens));
  }
  function mint(params) {
    if (isContractOwner() === false) {
      Utils.log('mint' + Chain.msg.sender);
      return;
    }
    var to = params.to;
    var id = params.id;
    var amount = params.amount;
    var data = params.data;
    Utils.assert(Utils.addressCheck(to), "ERC1155: mint params: to is invalid bid address");
    Utils.assert(Utils.addressCheck(id), "ERC1155: mint params: id is invalid bid address");
    _checkAmount(amount);
    var operator = sender_g;
    var toBalance = _getBalanceOf(id, to);
    _setBalanceOfForKey(id, to, toBalance + amount);
    _addTokenToAllTokensEnumeration(id, amount);
    Chain.tlog('TransferSingle', operator, "", to, id, amount);
  }
  function mintBatch(params) {
    if (isContractOwner() === false) {
      Utils.log('mint' + Chain.msg.sender);
      return;
    }
    var to = params.to;
    var ids = params.ids;
    var amounts = params.amounts;
    var data = params.data;
    Utils.assert(Utils.addressCheck(to), "ERC1155: mintBatch params: to is invalid bid address");
    Utils.assert(ids.length === amounts.length, "ERC1155: ids and amounts length mismatch");
    Utils.log('mintBatch-ids: (' + ids + ').');
    Utils.log('mintBatch-amounts: (' + amounts + ').');
    var operator = sender_g;
    var i = 0;
    var toBalance;
    for (i = 0; i < ids.length; i += 1) {
      Utils.assert(Utils.addressCheck(ids[i]), "ERC1155: mintBatch params: id is invalid bid address");
      _checkAmount(amounts[i]);
      toBalance = _getBalanceOf(ids[i], to);
      _setBalanceOfForKey(ids[i], to, toBalance + amounts[i]);
      _addTokenToAllTokensEnumeration(ids[i], amounts[i]);
    }
    Chain.tlog('TransferBatch', operator, "", to, JSON.stringify(ids), JSON.stringify(amounts));
  }
  function _totalSupply(tokenId) {
    var allTokens = {};
    var dataAll = JSON.parse(Chain.load(ALLTOKENS));
    if (dataAll) {
      allTokens = dataAll;
    }
    var counter = 0;
    if (allTokens[tokenId] === undefined) {
      allTokens[tokenId] = counter;
    }
    return allTokens[tokenId];
  }
  function totalSupply(params) {
    var tokenId = params.tokenId;
    Utils.assert(Utils.addressCheck(tokenId), "ERC1155: totalSupply params: tokenId is invalid bid address");
    return _totalSupply(tokenId);
  }
  function main(input_str) {
    var input = JSON.parse(input_str);
    if (input.method === 'mint') {
      mint(input.params);
    } else if (input.method === 'mintBatch') {
      mintBatch(input.params);
    } else if (input.method === 'safeTransferFrom') {
      safeTransferFrom(input.params);
    } else if (input.method === 'safeBatchTransferFrom') {
      safeBatchTransferFrom(input.params);
    } else if (input.method === 'setApprovalForAll') {
      setApprovalForAll(input.params);
    } else if (input.method === 'setURI') {
      setURI(input.params);
    } else {
      throw '<Main interface passes an invalid operation type>';
    }
  }
  function query(input_str) {
    var input = JSON.parse(input_str);
    var object = {};
    if (input.method === 'name') {
      object = name();
    } else if (input.method === 'symbol') {
      object = symbol();
    } else if (input.method === 'uri') {
      object = uri(input.params);
    } else if (input.method === 'totalSupply') {
      object = totalSupply(input.params);
    } else if (input.method === 'balanceOf') {
      object = balanceOf(input.params);
    } else if (input.method === 'balanceOfBatch') {
      object = balanceOfBatch(input.params);
    } else if (input.method === 'isApprovedForAll') {
      object = isApprovedForAll(input.params);
    } else {
      throw '<unidentified operation type>';
    }
    return JSON.stringify(object);
  }
  ```

#### 合约部署

调用合约创建方法部署合约

```js
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        String payload = "'use strict';const FUNDATION=\"_fundation\";const NAME=\"_name\";const SYMBOL=\"_symbol\";const URI=\"_uri\";const ALLTOKENS=\"_allTokens\";const BALANCES=\"_balances\";const OPERATORAPPROVALS=\"_operatorApprovals\";const sender_g=Chain.msg.sender;const chainCode_g=Chain.chainCode;function isContractOwner(){var owner=Chain.load(FUNDATION);if(Chain.msg.sender===owner){return true;}else{Utils.log(\"onlyFundation can call this method!\");return false;}}function _setURI(newuri){Chain.tlog('URI',newuri);Chain.store(URI,newuri);}function setURI(params){if(isContractOwner()===false){Utils.log('setURI'+Chain.msg.sender);return;}var uri=params.uri;_setURI(uri);}function init(input_str){var input=JSON.parse(input_str);var params=input.params;Utils.log('input_str: ('+input_str+').');if(params.name===undefined||params.symbol===undefined||params.uri===undefined||!params.name.length||!params.symbol.length||!params.uri.length){Utils.assert(false,\"DNA1155: init  params is invalid, please check!\");}Chain.store(NAME,params.name);Chain.store(SYMBOL,params.symbol);_setURI(params.uri);Chain.store(FUNDATION,sender_g);}function name(){return Chain.load(NAME);}function symbol(){return Chain.load(SYMBOL);}function _exists(tokenId){var tokens={};var dataToken=JSON.parse(Chain.load(ALLTOKENS));if(dataToken){tokens=dataToken;}if(tokens[tokenId]===undefined||tokens[tokenId]===0){return false;}else{return true;}}function _uri(tokenId){Utils.log('tokenId: '+tokenId);Utils.assert(_exists(tokenId),\"DNA1155: URI query for nonexistent token\");var uri=Chain.load(URI);if(uri.length>0){return uri+tokenId;}return\"\";}function uri(params){var tokenId=params.tokenId;Utils.assert(Utils.addressCheck(tokenId),\"DNA1155: uri params: tokenId is invalid bid address\");return _uri(tokenId);}function _getBalanceOf(id,account){var balances={};var data=JSON.parse(Chain.load(BALANCES));if(data){balances=data;}var inner_balances={};if(balances[id]===undefined){balances[id]=inner_balances;}if(balances[id][account]===undefined){return 0;}return balances[id][account];}function _setBalanceOfForKey(id,account,value){var balances={};var data=JSON.parse(Chain.load(BALANCES));if(data){balances=data;}var inner_balances={};if(balances[id]===undefined){balances[id]=inner_balances;}balances[id][account]=value;Utils.log(\"balances:\"+balances);Chain.store(BALANCES,JSON.stringify(balances));}function balanceOf(params){var account=params.account;var id=params.id;Utils.assert(Utils.addressCheck(account),\"DNA1155: balanceOf params: owner is invalid bid address\");Utils.assert(Utils.addressCheck(id),\"DNA1155: balanceOf params: tokenId is invalid bid address\");return _getBalanceOf(id,account);}function balanceOfBatch(params){var accounts=params.accounts;var ids=params.ids;Utils.assert(accounts.length===ids.length,\"ERC1155: accounts and ids length mismatch\");var batchBalances=[];var i=0;for(i=0;i<accounts.length;i+=1){Utils.assert(Utils.addressCheck(accounts[i]),\"DNA1155: balanceOfBatch params: owner is invalid bid address\");Utils.assert(Utils.addressCheck(ids[i]),\"DNA1155: balanceOfBatch params: tokenId is invalid bid address\");batchBalances[i]=_getBalanceOf(ids[i],accounts[i]);}return JSON.stringify(batchBalances);}function __setAllApproved(owner,to,isAllApproved){var allApproved={};var data=JSON.parse(Chain.load(OPERATORAPPROVALS));if(data){allApproved=data;}var inner_allApproved={};if(allApproved[owner]===undefined){allApproved[owner]=inner_allApproved;}allApproved[owner][to]=isAllApproved;Utils.log(\"allApproved:\"+allApproved);Chain.store(OPERATORAPPROVALS,JSON.stringify(allApproved));}function _setApprovalForAll(owner,operator,isApproved){Utils.assert(owner!==operator,\"ERC1155: setting approval status for self\");__setAllApproved(owner,operator,isApproved);Chain.tlog('ApprovalForAll',owner,operator,isApproved);}function setApprovalForAll(params){var operator=params.operator;var isApproved=params.isApproved;Utils.assert(Utils.addressCheck(operator),\"ERC1155: setApprovalForAll params: operator is invalid bid address\");_setApprovalForAll(sender_g,operator,isApproved);}function __getIsAllApproved(owner,to){var allApproved={};var data=JSON.parse(Chain.load(OPERATORAPPROVALS));if(data){allApproved=data;}var inner_allApproved={};if(allApproved[owner]===undefined){allApproved[owner]=inner_allApproved;}if(allApproved[owner][to]===undefined){return false;}return allApproved[owner][to];}function _isApprovedForAll(owner,operator){Utils.assert(Utils.addressCheck(owner),\"ERC1155: _isApprovedForAll params: owner is invalid bid address\");Utils.assert(Utils.addressCheck(operator),\"ERC1155: _isApprovedForAll params: operator is invalid bid address\");return __getIsAllApproved(owner,operator);}function isApprovedForAll(params){var account=params.account;var operator=params.operator;return _isApprovedForAll(account,operator);}function _safeTransferFrom(from,to,id,amount,data){Utils.assert(to.length>0,\"ERC1155: transfer to the zero address\");var operator=sender_g;var fromBalance=_getBalanceOf(id,from);Utils.assert(fromBalance>=amount,\"ERC1155: insufficient balance for transfer\");_setBalanceOfForKey(id,from,fromBalance-amount);var toBalance=_getBalanceOf(id,to);_setBalanceOfForKey(id,to,toBalance+amount);Chain.tlog('TransferSingle',operator,from,to,id,amount);}function _checkAmount(amount){Utils.assert(amount!==undefined,\"ERC1155: params: amount must have a value\");Utils.assert(amount>0,\"ERC1155: params: amount must > 0\");Utils.assert(amount%1===0,\"ERC1155 params: your amount should be int\");}function safeTransferFrom(params){var from=params.from;var to=params.to;var id=params.id;var amount=params.amount;var data=params.data;Utils.assert(Utils.addressCheck(from),\"ERC1155: safeTransferFrom params: from is invalid bid address\");Utils.assert(Utils.addressCheck(to),\"ERC1155: safeTransferFrom params: to is invalid bid address\");Utils.assert(Utils.addressCheck(id),\"ERC1155: safeTransferFrom params: id is invalid bid address\");_checkAmount(amount);Utils.assert(from===sender_g||_isApprovedForAll(from,sender_g),\"ERC1155: caller is not owner nor approved\");_safeTransferFrom(from,to,id,amount,data);}function _safeBatchTransferFrom(from,to,ids,amounts,data){Utils.assert(ids.length===amounts.length,\"ERC1155:  ids and amounts length mismatch\");Utils.assert(to.length>0,\"ERC1155:  transfer to the zero address\");var operator=sender_g;var i=0;var id;var amount;var fromBalance;var toBalance;for(i=0;i<ids.length;i+=1){id=ids[i];amount=amounts[i];_checkAmount(amount);fromBalance=_getBalanceOf(id,from);Utils.assert(fromBalance>=amount,\"ERC1155:  insufficient balance for transfer\");_setBalanceOfForKey(id,from,fromBalance-amount);toBalance=_getBalanceOf(id,to);_setBalanceOfForKey(id,to,toBalance+amount);}Chain.tlog('TransferBatch',operator,from,to,JSON.stringify(ids),JSON.stringify(amounts));}function safeBatchTransferFrom(params){var from=params.from;var to=params.to;var ids=params.ids;var amounts=params.amounts;var data=params.data;Utils.assert(Utils.addressCheck(from),\"ERC1155: safeBatchTransferFrom params: from is invalid bid address\");Utils.assert(Utils.addressCheck(to),\"ERC1155: safeBatchTransferFrom params: to is invalid bid address\");var i=0;for(i=0;i<ids.length;i+=1){Utils.assert(Utils.addressCheck(ids[i]),\"ERC1155: safeBatchTransferFrom params: id is invalid bid address\");}Utils.assert(from===sender_g||_isApprovedForAll(from,sender_g),\"ERC1155: caller is not owner nor approved\");_safeBatchTransferFrom(from,to,ids,amounts,data);}function _addTokenToAllTokensEnumeration(tokenId,amount){var allTokens={};var dataAll=JSON.parse(Chain.load(ALLTOKENS));if(dataAll){allTokens=dataAll;}var counter=0;if(allTokens[tokenId]===undefined){allTokens[tokenId]=counter;}allTokens[tokenId]+=amount;Chain.store(ALLTOKENS,JSON.stringify(allTokens));}function mint(params){if(isContractOwner()===false){Utils.log('mint'+Chain.msg.sender);return;}var to=params.to;var id=params.id;var amount=params.amount;var data=params.data;Utils.assert(Utils.addressCheck(to),\"ERC1155: mint params: to is invalid bid address\");Utils.assert(Utils.addressCheck(id),\"ERC1155: mint params: id is invalid bid address\");_checkAmount(amount);var operator=sender_g;var toBalance=_getBalanceOf(id,to);_setBalanceOfForKey(id,to,toBalance+amount);_addTokenToAllTokensEnumeration(id,amount);Chain.tlog('TransferSingle',operator,\"\",to,id,amount);}function mintBatch(params){if(isContractOwner()===false){Utils.log('mint'+Chain.msg.sender);return;}var to=params.to;var ids=params.ids;var amounts=params.amounts;var data=params.data;Utils.assert(Utils.addressCheck(to),\"ERC1155: mintBatch params: to is invalid bid address\");Utils.assert(ids.length===amounts.length,\"ERC1155: ids and amounts length mismatch\");Utils.log('mintBatch-ids: ('+ids+').');Utils.log('mintBatch-amounts: ('+amounts+').');var operator=sender_g;var i=0;var toBalance;for(i=0;i<ids.length;i+=1){Utils.assert(Utils.addressCheck(ids[i]),\"ERC1155: mintBatch params: id is invalid bid address\");_checkAmount(amounts[i]);toBalance=_getBalanceOf(ids[i],to);_setBalanceOfForKey(ids[i],to,toBalance+amounts[i]);_addTokenToAllTokensEnumeration(ids[i],amounts[i]);}Chain.tlog('TransferBatch',operator,\"\",to,JSON.stringify(ids),JSON.stringify(amounts));}function _totalSupply(tokenId){var allTokens={};var dataAll=JSON.parse(Chain.load(ALLTOKENS));if(dataAll){allTokens=dataAll;}var counter=0;if(allTokens[tokenId]===undefined){allTokens[tokenId]=counter;}return allTokens[tokenId];}function totalSupply(params){var tokenId=params.tokenId;Utils.assert(Utils.addressCheck(tokenId),\"ERC1155: totalSupply params: tokenId is invalid bid address\");return _totalSupply(tokenId);}function main(input_str){var input=JSON.parse(input_str);if(input.method==='mint'){mint(input.params);}else if(input.method==='mintBatch'){mintBatch(input.params);}else if(input.method==='safeTransferFrom'){safeTransferFrom(input.params);}else if(input.method==='safeBatchTransferFrom'){safeBatchTransferFrom(input.params);}else if(input.method==='setApprovalForAll'){setApprovalForAll(input.params);}else if(input.method==='setURI'){setURI(input.params);}else{throw'<Main interface passes an invalid operation type>';}}function query(input_str){var input=JSON.parse(input_str);var object={};if(input.method==='name'){object=name();}else if(input.method==='symbol'){object=symbol();}else if(input.method==='uri'){object=uri(input.params);}else if(input.method==='totalSupply'){object=totalSupply(input.params);}else if(input.method==='balanceOf'){object=balanceOf(input.params);}else if(input.method==='balanceOfBatch'){object=balanceOfBatch(input.params);}else if(input.method==='isApprovedForAll'){object=isApprovedForAll(input.params);}else{throw'<unidentified operation type>';}return JSON.stringify(object);}";
        Long initBalance = ToBaseUnit.ToUGas("0.01");
        String input="{\"params\":{\"name\":\"xinghuo space nft 1155\",\"symbol\":\"DNA\",\"uri\":\"https://gateway.pinata.cloud/ipfs/QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/6476\"}}";
        BIFContractCreateRequest request = new BIFContractCreateRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setInitBalance(initBalance);
        request.setPayload(payload);
        request.setRemarks("create contract");
        request.setType(0);
        request.setGasPrice(10L);
        request.setFeeLimit(111549500L);
        request.setInitInput(input);

        // 调用bifContractCreate接口
        BIFContractCreateResponse response = sdk.getBIFContractService().contractCreate(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

交易hash：`837b909351f35918e8d20622577f65e6caa95c7e4023694b6b731fb91adb1be2`

根据交易hash获取合约地址

```js
        // 合约部署返回值hash
        String hash = "837b909351f35918e8d20622577f65e6caa95c7e4023694b6b731fb91adb1be2";
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

合约地址：`did:bid:ef22LxGioBy5bUNYVkdbvo4U46RKXgkir`

#### 合约调用

根据生成的合约地址进行合约调用操作

##### 铸造

```js
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:ef22LxGioBy5bUNYVkdbvo4U46RKXgkir";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input = "{\"method\":\"mint\",\"params\":{\"to\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i\",\"id\":\"did:bid:ef29yYZGjWo4ZhwfkmGg7qrNyqa5BCQPc\",\"amount\":5,\"data\":\"1155 JS\"}}";
        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setGasPrice(10L);
        request.setRemarks("contract invoke");
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 批量铸造

```js
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:ef22LxGioBy5bUNYVkdbvo4U46RKXgkir";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input="{\"method\":\"mintBatch\",\"params\":{\"to\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i\",\"ids\":[\"did:bid:zf23wR1NxfzTY6qRjo1zs8TjPnW6SHVsc\",\"did:bid:zf23wR1NxfzTY6qRjo1zs8TjPnW6SHVsc\",\"did:bid:zf2AHtw8YGgKPCyye2GMu56Wtjngvfdbg\"],\"amounts\":[1,1,2],\"data\":\"1155 JS\"}}";

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 安全转移

```js
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:ef22LxGioBy5bUNYVkdbvo4U46RKXgkir";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input ="{\"method\":\"safeTransferFrom\",\"params\":{\"from\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i\",\"to\":\"did:bid:ef296hUUmhM8fgH9Gg7dyY3MH7P1tkpJU\",\"id\":\"did:bid:ef29yYZGjWo4ZhwfkmGg7qrNyqa5BCQPc\",\"amount\":5,\"data\":\"safe transfer with data\"}}";
        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 批量安全转移

```js
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:ef22LxGioBy5bUNYVkdbvo4U46RKXgkir";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input ="{\"method\":\"safeBatchTransferFrom\",\"params\":{\"from\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i\",\"to\":\"did:bid:ef296hUUmhM8fgH9Gg7dyY3MH7P1tkpJU\",\"ids\":[\"did:bid:zf23wR1NxfzTY6qRjo1zs8TjPnW6SHVsc\",\"did:bid:zf2AHtw8YGgKPCyye2GMu56Wtjngvfdbg\"],\"amounts\":[1,2],\"data\":\"safe transfer with data\"}}";
        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 授权所有

```js
        // 初始化参数
        String senderAddress = "did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i";
        String contractAddress = "did:bid:ef22LxGioBy5bUNYVkdbvo4U46RKXgkir";
        String senderPrivateKey = "priSPKnpkx9TJZpZvGmdtUkJAEo2rW3cG9Bdxz2DUtjruiUxrn";
        Long amount = 0L;
        String  input ="{\"method\":\"setApprovalForAll\",\"params\":{\"operator\":\"did:bid:efHSbC7AedduvEG5hbtUio4mZmzwGhse\",\"isApproved\":true}}";

        BIFContractInvokeRequest request = new BIFContractInvokeRequest();
        request.setSenderAddress(senderAddress);
        request.setPrivateKey(senderPrivateKey);
        request.setContractAddress(contractAddress);
        request.setBIFAmount(amount);
        request.setRemarks("contract invoke");
        request.setGasPrice(10L);
        request.setInput(input);

        // 调用 bifContractInvoke 接口
        BIFContractInvokeResponse response = sdk.getBIFContractService().contractInvoke(request);
        if (response.getErrorCode() == 0) {
            System.out.println(JsonUtils.toJSONString(response.getResult()));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

#### 合约查询

##### 查询代币数量

```js
        // 初始化参数		
        String contractAddress = "did:bid:ef22LxGioBy5bUNYVkdbvo4U46RKXgkir";
        String input  = "{\"method\":\"balanceOf\",\"params\":{\"account\":\"did:bid:ef296hUUmhM8fgH9Gg7dyY3MH7P1tkpJU\",\"id\":\"did:bid:zf23wR1NxfzTY6qRjo1zs8TjPnW6SHVsc\"}}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        //request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 批量查询代币数量

```js
        // 初始化参数
        String contractAddress = "did:bid:ef22LxGioBy5bUNYVkdbvo4U46RKXgkir";
        String input  = "{\"method\":\"balanceOfBatch\",\"params\":{\"accounts\":[\"did:bid:ef21SesYy12yP9Pq24KQun3Xkk684gDuk\",\"did:bid:ef21SesYy12yP9Pq24KQun3Xkk684gDuk\"],\"ids\":[\"did:bid:efTMqg6qLb1pT34NdLjCXKwAxnCd5ELr\",\"did:bid:zf2AHtw8YGgKPCyye2GMu56Wtjngvfdbg\"]}}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        //request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询是否被授权所有

```js
        // 初始化参数
        String contractAddress = "did:bid:ef22LxGioBy5bUNYVkdbvo4U46RKXgkir";
        String input  ="{\"method\":\"isApprovedForAll\",\"params\":{\"account\":\"did:bid:efHqeHDdu6CxteYXxsPtFKdPbqTJd85i\",\"operator\":\"did:bid:efHSbC7AedduvEG5hbtUio4mZmzwGhse\"}}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        //request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询name

```js
        // 初始化参数	
        String contractAddress = "did:bid:ef22LxGioBy5bUNYVkdbvo4U46RKXgkir";
        String input  = "{\"method\": \"name\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        //request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询symbol

```js
        // 初始化参数
        String contractAddress = "did:bid:ef22LxGioBy5bUNYVkdbvo4U46RKXgkir";
        String input  = "{\"method\": \"symbol\"}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        //request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询tokenUri

```js
        // 初始化参数
        String contractAddress = "did:bid:ef22LxGioBy5bUNYVkdbvo4U46RKXgkir";
        String input  = "{\"method\":\"uri\",\"params\":{\"tokenId\":\"did:bid:zf2AHtw8YGgKPCyye2GMu56Wtjngvfdbg\"}}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        //request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

##### 查询totalSupply

```js
        // 初始化参数
        String contractAddress = "did:bid:ef22LxGioBy5bUNYVkdbvo4U46RKXgkir";
        String input  = "{\"method\":\"totalSupply\",\"params\":{\"tokenId\":\"did:bid:efzZLfWLnz1Apfxp2vZe1z34GuTtriPa\"}}";
        // Init request
        BIFContractCallRequest request = new BIFContractCallRequest();
        request.setContractAddress(contractAddress);
        //request.setDomainId(0);
        request.setInput(input);

        // Call contractQuery
        BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
        if (response.getErrorCode() == 0) {
            BIFContractCallResult result = response.getResult();
            System.out.println(JsonUtils.toJSONString(result));
        } else {
            System.out.println(JsonUtils.toJSONString(response));
        }
```

## 工业互联网标识合约

本节描述通过星火链网实现并部署工业互联网标识智能合约。

工业互联网标识映射的信息资源是具有唯一性的功能，对比传统互联网的DNS功能作用，可以通过标识代表映射具体某资源，而星火链工业互联网标识合约是基于星火链网主链，将各顶级`GHR`、二级`SHR`以及企业`LHS`的数据维护在主链账本中，通过自主身份体系和BID，实现对其所辖数据的自管理。

### 合约说明

标识合约是由`JavaScript`语言开发，在链上由V8虚拟机引擎解释执行。

标识合约有`GHR`（顶级节点），`SHR`（二级节点），`LHS`（企业节点）三种类型，在链上部署合约后即生成对应的合约账户，用户就可以根据合约接口分别进行注册，修改，删除以及查询的操作，其中注册，修改以及删除操作需要有白名单权限才可以操作，所以必须在部署发行到链上后，先进行白名单设置在进行后续接口调用操作。

+ 合约接口说明

  | 合约函数          | 说明       |
  | ----------------- | ---------- |
  | createZidData     | 创建标识   |
  | modifyZidData     | 修改标识   |
  | queryZidRecord    | 查询标识   |
  | removeZidData     | 删除标识   |
  | setAuditWhitelist | 设置白名单 |

+ **合约示例**

  ```javascript
  'use strict';
  
  
  //ZID  data操作
  const ZidOp = {
      'INS'                : '0',      //insert
      'DEL'                : '1',      //delete
      'MOD'                : '2',       //modify
  	'QUERY'				 : '3'       //query
  };
  
  const ZID_RECORD_PRE = 'zidrecord';
  const GHR_ZID_INIT = 'ghr_zid_init';
  const SHR_ZID_INIT = 'shr_zid_init';
  const LHS_ZID_INIT = 'lhs_zid_init';
  
  /*
      ***********************************
                  事件定义
      ***********************************
  */
  //白名单设置
  const TLOG_SET_WT = 'tlog_set_wt';
  
  //创建标识事件
  const TLOG_ZID_CREATE_CONTRACT_ADDRESS = 'tlog_zid_create_contract_address';
  
  //修改标识事件
  const TLOG_ZID_MODIFY_CONTRACT_ADDRESS = 'tlog_zid_modify_contract_address';
  
  //删除标识事件
  const TLOG_ZID_REMOVE_CONTRACT_ADDRESS = 'tlog_zid_remove_contract_address';
  
  
  /*
      ***********************************
                  权限控制
      ***********************************
  */
  function isValidator(addr){
      return Chain.isValidator(addr);
  }
  
  function getWhiteKey(addr){
      return 'wk-' + addr;
  }
    
  function checkInAuditWhitelist(addr) {
      const res = Chain.load(getWhiteKey(addr));
      return res !== false;
  }
  
  function getKey(first, second, third = ''){
      return (third === '') ? (first + '_' + second) : (first + '_' + second + '_' + third);
  }
  
  function loadObj(key){
  	let data = Chain.load(getKey(ZID_RECORD_PRE,key));
  	return JSON.parse(data);
  }
  
  /* 
      函数名称：setAuditWhitelist()
      函数描述：白名单注册接口；该接口需要验证者账户调用
      调用方式：main
      参数：
          caller_address         待操作白名单账户
          addFlag         操作
      返回值：无
  */
  function setAuditWhitelist(paramObj) {
      Utils.assert(paramObj.caller_address !== undefined, 'Param obj has no caller_address');
      Utils.assert(paramObj.addFlag !== undefined, 'Param obj has no addFlag');
  
      Utils.assert(Utils.addressCheck(paramObj.caller_address), `The caller_address(${paramObj.caller_address}) is invalid`);
      Utils.assert(typeof paramObj.addFlag === 'boolean', `The addFlag(${paramObj.addFlag}) is invalid`);
  
      //isValidator check
      Utils.assert(isValidator(Chain.msg.sender), `The caller_address(${Chain.msg.sender}) is not validator`);
      
      if (paramObj.addFlag === true) {
          Utils.assert(loadObj(getWhiteKey(paramObj.caller_address)) === false, `The account(${paramObj.caller_address}) is already in whitelist`);
          Chain.store(getWhiteKey(paramObj.caller_address), '');
      } else {
          Chain.del(getWhiteKey(paramObj.caller_address));
      }
  
      Chain.tlog(TLOG_SET_WT, Chain.msg.sender, paramObj.caller_address, `${paramObj.addFlag}`);
  }
  
  function createZidValue(key, value){
      Chain.store(getKey(ZID_RECORD_PRE, key), JSON.stringify(value));
  }
  
  function deleteZidValue(key){
      Chain.del(getKey(ZID_RECORD_PRE,key));
  }
  
  function modifyZidValue(key, value) {
      deleteZidValue(key);
      createZidValue(key, value);
  } 
  
  function queryZidRecord(paramObj){
      Utils.assert(paramObj.zid !== undefined, 'Param obj has no zid');
  	
      return loadObj(paramObj.zid);
  }
  /* 
      函数名称：createZidData()
      函数描述：创建标识;
  
      调用方式：main
      参数：
          zid             标识
          value        	标识值数组
  		index			标识值索引
  		type			标识类型
  		data			标识数据结构
  		format			数据格式
  		value			标识值
  		ttl				ttl值
  		ttlType			ttl类型
  		timestamp		时间戳
  		references		引用
  		adminRead		管理员可读
  		adminWrite		管理员可写
  		publicRead		公共可读
  		publicWrite		公共可写
      返回值：
          无
  */
  function createZidData(paramObj) {
      //check param
      Utils.assert(paramObj.zid !== undefined, 'Param obj has no zid');
      Utils.assert(paramObj.value[0].index !== undefined, 'Param obj has no index');
      Utils.assert(paramObj.value[0].type !== undefined, 'Param obj has no type');
      Utils.assert(paramObj.value[0].data.format !== undefined, 'Param obj has no format');
  	Utils.assert(paramObj.value[0].data.value !== undefined, 'Param obj has no data value');
  	Utils.assert(paramObj.value[0].ttl !== undefined, 'Param obj has no ttl');
  	Utils.assert(paramObj.value[0].ttlType !== undefined, 'Param obj has no ttl');
  	Utils.assert(paramObj.value[0].timestamp !== undefined, 'Param obj has no timestamp');
  
      //检测操作权限
      Utils.assert(checkInAuditWhitelist(Chain.msg.sender), `The address(${Chain.msg.sender}) checkInAuditWhitelist error`);
  	
  	//判断对应zid是否已存在
  	Utils.assert(loadObj(paramObj.zid) === false, 'createZidData exist of zid:' + paramObj.zid);
  	
  	let regiRecord = {  
  	    'value': [{
  		'index': paramObj.value[0].index,
  		'type': paramObj.value[0].type,
  		'data': {
  			'format': paramObj.value[0].data.format,
  			'value': paramObj.value[0].data.value
  		},
  		'ttl': paramObj.value[0].ttl,
  		'ttlType': paramObj.value[0].ttlType,
  		'timestamp': paramObj.value[0].timestamp,
  		'references': paramObj.value[0].references,
  		'adminRead': paramObj.value[0].adminRead,
  		'adminWrite': paramObj.value[0].adminWrite,
  		'publicRead': paramObj.value[0].publicRead,
  		'publicWrite': paramObj.value[0].publicWrite
  	}]
      };
  	
      createZidValue(paramObj.zid, regiRecord);
  	Chain.tlog(TLOG_ZID_CREATE_CONTRACT_ADDRESS, 'zid data record', 'create', paramObj.zid);
  }
  
  function removeZidData(paramObj) {
  	//check param
  	Utils.assert(paramObj.zid !== undefined, 'Param obj has no zid');
  	if(paramObj.opFlag === ZidOp.DEL)
  	{
  		 //检测操作权限
  		Utils.assert(checkInAuditWhitelist(Chain.msg.sender), `The address(${Chain.msg.sender}) checkInAuditWhitelist error`);
  		
  		deleteZidValue(paramObj.zid);
  		Chain.tlog(TLOG_ZID_REMOVE_CONTRACT_ADDRESS, 'zid data record', 'remove', paramObj.zid);
  	}
  }
  
  function modifyZidData(paramObj) {
  	//check param
      Utils.assert(paramObj.zid !== undefined, 'Param obj has no zid');
  	Utils.assert(paramObj.opFlag !== undefined, 'Param obj has no opFlag');
      Utils.assert(paramObj.value[0].index !== undefined, 'Param obj has no index');
      Utils.assert(paramObj.value[0].type !== undefined, 'Param obj has no type');
      Utils.assert(paramObj.value[0].data.format !== undefined, 'Param obj has no format');
  	Utils.assert(paramObj.value[0].data.value !== undefined, 'Param obj has no data value');
  	Utils.assert(paramObj.value[0].ttl !== undefined, 'Param obj has no ttl');
  	Utils.assert(paramObj.value[0].ttlType !== undefined, 'Param obj has no ttl');
  	Utils.assert(paramObj.value[0].timestamp !== undefined, 'Param obj has no timestamp');
  	
      //检测操作权限
      Utils.assert(checkInAuditWhitelist(Chain.msg.sender), `The address(${Chain.msg.sender}) checkInAuditWhitelist error`);
  	
  	//判断对应zid是否已存在
  	Utils.assert(loadObj(paramObj.zid) === false, 'modifyZidData exist of zid:' + paramObj.zid);
  	if(paramObj.opFlag === ZidOp.MOD)
  	{
  		let modifyRecord = {  
  	    'value': [{
  		'index': paramObj.value[0].index,
  		'type': paramObj.value[0].type,
  		'data': {
  			'format': paramObj.value[0].data.format,
  			'value': paramObj.value[0].data.value
  		},
  		'ttl': paramObj.value[0].ttl,
  		'ttlType': paramObj.value[0].ttlType,
  		'timestamp': paramObj.value[0].timestamp,
  		'references': paramObj.value[0].references,
  		'adminRead': paramObj.value[0].adminRead,
  		'adminWrite': paramObj.value[0].adminWrite,
  		'publicRead': paramObj.value[0].publicRead,
  		'publicWrite': paramObj.value[0].publicWrite
  		}]
  		};
  	
  		modifyZidValue(paramObj.zid, modifyRecord);
  		Chain.tlog(TLOG_ZID_MODIFY_CONTRACT_ADDRESS, 'zid data record', 'modify', paramObj.zid);
  		
  	}
  }
  /*
      ***********************************
                  调用入口
      ***********************************
  */
  
  function init(input){
  	let inputObj = JSON.parse(input);
      if (inputObj.type === GHR_ZID_INIT){
          Chain.store(GHR_ZID_INIT, 'TRUE');
      }
  	else if(inputObj.type === SHR_ZID_INIT)
  	{
  		Chain.store(SHR_ZID_INIT, 'TRUE');
  	}
      else if(inputObj.type === LHS_ZID_INIT)
  	{
  		Chain.store(LHS_ZID_INIT, 'TRUE');
  	}
      return;
  }
  
  function main(input){
      let funcList = {
          //验证者账户设置白名单
          'setAuditWhitelist' : setAuditWhitelist,
          //标识功能接口
          'createZidData' : createZidData,
          'modifyZidData' : modifyZidData,
          'removeZidData' : removeZidData
      };
      let inputObj = JSON.parse(input);
      Utils.assert(funcList.hasOwnProperty(inputObj.method) && typeof funcList[inputObj.method] === 'function', 'Cannot find func:' + inputObj.method);
      funcList[inputObj.method](inputObj.params);
  }
  
  function query(input){
      let result = {};
      let inputObj = JSON.parse(input);
      if (inputObj.method === 'queryZidRecord'){
          result = queryZidRecord(inputObj.params);
      }
      return JSON.stringify(result);
  }
  ```

###  合约部署

运行链节点服务之后就可以部署合约到链上，生成对应的合约账户，合约账户可以后续进行合约管理，部署合约是通过调用SDK接口。

+ **GHR合约部署**

  ```java
  // 初始化参数
  String senderAddress = "did:bid:efuEAGFPJMsojwPGKzjD8vZX1wbaUrVV";
  String senderPrivateKey = "priSPKnDue7AJ42gt7acy4AVaobGJtM871r1eukZ2M6eeW5LxG";
  //ghr合约压缩后的代码
  String payload = "'use strict';const ZidOp=				{'INS':'0','DEL':'1','MOD':'2','QUERY':'3'};const    ZID_RECORD_PRE='zidrecord';const GHR_ZID_INIT='ghr_zid_init';const TLOG_SET_WT='tlog_set_wt';";
  Long initBalance = ToBaseUnit.ToUGas("0.01");
  
  BIFContractCreateRequest request = new BIFContractCreateRequest();
  request.setSenderAddress(senderAddress);
  request.setPrivateKey(senderPrivateKey);
  request.setInitBalance(initBalance);
  request.setPayload(payload);
  request.setInitInput("{\"type\":\"ghr_zid_init\"}");
  request.setMetadata("create ghr contract");
  
  // 调用BIFContractCreate接口
  BIFContractCreateResponse response = sdk.getBIFContractService().contractCreate(request);
  if (response.getErrorCode() == 0) {
      System.out.println(JSON.toJSONString(response.getResult(), true));
  } else {
      System.out.println("error:      " + response.getErrorDesc());
  }
  ```

  其中`payload`参数即是对应合约源码压缩(参照**Javascript合约说明-合约开发工具**章节)后的值，`input`参数里的类型填写对应的类型值即可。

  合约部署完后返回对应的hash值，可以根据hash查询对应详细交易信息。

+ **SHR合约部署**

  只需要将`setInitInput`的合约类型换成`SHR`的即可。

  ```java
  // 初始化参数
  String senderAddress = "did:bid:efuEAGFPJMsojwPGKzjD8vZX1wbaUrVV";
  String senderPrivateKey = "priSPKnDue7AJ42gt7acy4AVaobGJtM871r1eukZ2M6eeW5LxG";
  //shr合约压缩后的代码
  String payload = "'use strict';const ZidOp=				{'INS':'0','DEL':'1','MOD':'2','QUERY':'3'};const    ZID_RECORD_PRE='zidrecord';const GHR_ZID_INIT='shr_zid_init';const TLOG_SET_WT='tlog_set_wt';";
  Long initBalance = ToBaseUnit.ToUGas("0.01");
  
  BIFContractCreateRequest request = new BIFContractCreateRequest();
  request.setSenderAddress(senderAddress);
  request.setPrivateKey(senderPrivateKey);
  request.setInitBalance(initBalance);
  request.setPayload(payload);
  request.setInitInput("{\"type\":\"shr_zid_init\"}");
  request.setMetadata("create shr contract");
  
  // 调用BIFContractCreate接口
  BIFContractCreateResponse response = sdk.getBIFContractService().contractCreate(request);
  if (response.getErrorCode() == 0) {
      System.out.println(JSON.toJSONString(response.getResult(), true));
  } else {
      System.out.println("error:      " + response.getErrorDesc());
  }
  ```

  合约部署完后返回对应的hash值，可以根据hash查询对应详细交易信息。

+ **LHS合约部署**

  只需要修改`setInitInput`的合约类型值即可。

  ```java
  // 初始化参数
  String senderAddress = "did:bid:efVmotQW28QDtQyupnKTFvpjKQYs5bxf";
  String senderPrivateKey = "priSPKnDue7AJ42gt7acy4AVaobGJtM871r1eukZ2M6eeW5LxG";
  //lhs合约压缩后代码
  String payload = "'use strict';const ZidOp=				{'INS':'0','DEL':'1','MOD':'2','QUERY':'3'};const    ZID_RECORD_PRE='zidrecord';const GHR_ZID_INIT='shr_zid_init';const TLOG_SET_WT='tlog_set_wt';";
  Long initBalance = ToBaseUnit.ToUGas("0.01");
  
  BIFContractCreateRequest request = new BIFContractCreateRequest();
  request.setSenderAddress(senderAddress);
  request.setPrivateKey(senderPrivateKey);
  request.setInitBalance(initBalance);
  request.setPayload(payload);
  request.setInitInput("{\"type\":\"lhs_zid_init\"}");
  request.setMetadata("create lhs contract");
  
  // 调用BIFContractCreate接口
  BIFContractCreateResponse response = sdk.getBIFContractService().contractCreate(request);
  if (response.getErrorCode() == 0) {
      System.out.println(JSON.toJSONString(response.getResult(), true));
  } else {
      System.out.println("error:      " + response.getErrorDesc());
  }
  ```

  合约部署完后返回对应的hash值，可以根据hash查询对应详细交易信息。

### 合约调用

+ **设置白名单**

  ```java
  // 初始化参数
  String senderAddress = "did:bid:efVmotQW28QDtQyupnKTFvpjKQYs5bxf";
  String contractAddress = "did:bid:ef2gAT82SGdnhj87wQWb9suPKLbnk9NP";
  String senderPrivateKey = "priSPKnDue7AJ42gt7acy4AVaobGJtM871r1eukZ2M6eeW5LxG";
  Long amount = 0L;
  
  BIFContractInvokeByGasRequest request = new BIFContractInvokeByGasRequest();
  request.setSenderAddress(senderAddress);
  request.setPrivateKey(senderPrivateKey);
  request.setContractAddress(contractAddress);
  request.setBIFAmount(amount);
  request.setMetadata("contract set whiteList invoke");
  request.setInput("{\"method\":\"setAuditWhitelist\",\"params\":{\"caller_address\": \"did:bid:efuEAGFPJMsojwPGKzjD8vZX1wbaUrVV\",\"addFlag\":true}}");
  
  // 调用 BIFContractInvoke 接口
  BIFContractInvokeByGasResponse response = sdk.getBIFContractService().contractInvoke(request);
  if (response.getErrorCode() == 0) {
      System.out.println(JSON.toJSONString(response.getResult(), true));
  } else {
      System.out.println("error:      " + response.getErrorDesc());
  }
  ```

  白名单设置和其他交易不同在于，源账户是由验证者账户触发的（必须时验证者账户否则报错），合约账户就是对应`GHR`，`SHR`以及`LHS`各自的合约地址，私钥就是验证者账户对应的，然后input合约函数以及参数都是`GHR`，`SHR`以及`LHS`对应里具体的值，然后初始化填充后调用接口发送即可将各个合约地址加入到白名单，以方便后续的管理操作。

+ **标识创建**

  ```java
  // 初始化参数
  String senderAddress = "did:bid:efVmotQW28QDtQyupnKTFvpjKQYs5bxf";
  String contractAddress = "did:bid:ef2gAT82SGdnhj87wQWb9suPKLbnk9NP";
  String senderPrivateKey = 	"priSPKnDue7AJ42gt7acy4AVaobGJtM871r1eukZ2M6eeW5LxG";
  Long amount = 0L;
  
  BIFContractInvokeByGasRequest request = new BIFContractInvokeByGasRequest();
  request.setSenderAddress(senderAddress);
  request.setPrivateKey(senderPrivateKey);
  request.setContractAddress(contractAddress);
  request.setBIFAmount(amount);
  request.setMetadata("contract create zid invoke");
  request.setInput("{\"method\":\"createZidData\",\"params\": {\n" +
          "\t\t\"zid\": \"88.1000\",\n" +
          "\t\t\"opFlag\": \"0\",\n" +
          "\t\t\"value\": [{\n" +
          "\t\t\t\"index\": \"1\",\n" +
          "\t\t\t\"type\": \"contract_address\",\n" +
          "\t\t\t\"data\": {\n" +
          "\t\t\t\t\"format\": \"string\",\n" +
          "\t\t\t\t\"value\": 		\"did:bid:efuEAGFPJMsojwPGKzjkkk89jky\"\n" +
          "\t\t\t},\n" +
          "\t\t\t\"ttl\": \"86400\",\n" +
          "\t\t\t\"ttlType\": \"0\",\n" +
          "\t\t\t\"timestamp\": \"0\",\n" +
          "\t\t\t\"references\": [],\n" +
          "\t\t\t\"adminRead\": \"1\",\n" +
          "\t\t\t\"adminWrite\": \"1\",\n" +
          "\t\t\t\"publicRead\": \"1\",\n" +
          "\t\t\t\"publicWrite\": \"0\"\n" +
          "\t\t}]\n" +
          "\t}}");
  // 调用 BIFContractInvoke 接口
  BIFContractInvokeByGasResponse response = sdk.getBIFContractService().contractInvoke(request);
  if (response.getErrorCode() == 0) {
      System.out.println(JSON.toJSONString(response.getResult(), true));
  } else {
      System.out.println("error:      " + response.getErrorDesc());
  }
  ```

  zid标识在的value数据结构字段为：
  
  | Value格式   | 参数含义                                                     | 是否必填 | 默认值 |
  | ----------- | ------------------------------------------------------------ | -------- | ------ |
  | method      | 标识创建的函数名                                             | 必填项   |        |
  | index       | 标识值索引(最好不要用默认的0，从1开始递增创建)               | 必填项   |        |
  | type        | 标识值类型(GHR和SHR创建的都为contract_address)               | 必填项   |        |
  | data        | 包含有format以及value字段如下                                | 必填项   |        |
  | format      | string类型                                                   | 必填项   |        |
  | value       | 标识值数据(GHR和SHR的为具体合约地址)                         |          |        |
  | ttl         | 标识超时时间                                                 |          | 86400s |
  | ttlType     | 标识超时类型                                                 |          | 0      |
  | timestamp   | 时间戳                                                       |          | 0      |
  | References  | 包含zid以及index字段如下                                     |          | 选填   |
  | zid         | 引用的标识名称，引用标识和index一一对应，可以是多个，可以没有引用其他标识 |          | 空     |
  | opFlag      | 标识操作标志 ，值0是创建，1是删除，2是修改，3是查询          |          | 0      |
  | index       | 引用的标识索引值(所引用handle的index不能为0)                 |          | 空     |
  | adminRead   | 标识管理员可读,1可读 0不可读                                 |          | 1      |
  | adminWrite  | 标识管理员可写，1可写 0不可写                                |          | 1      |
  | publicRead  | 标识公共可读，1可读 0不可读                                  |          | 1      |
  | publicWrite | 标识公共可写，1可写 0不可写                                  |          | 0      |

  标识创建调用接口时，每次只需修改`contract_address`的值为各自合约的账户地址，以及合约函数名,参数等数据。

  创建接口执行完之后，根据生成的hash调用`getTransactionInfo`交易记录接口查询对应的交易是否成功情况。

+ **标识修改**

  标识修改接口和标识创建章节中的接口和参数一样，只需要修改对应的`input`的parames中对应合约修改函数及参数以及标识value的各字段值即可。

+ **标识删除**

  ```java
  // 初始化参数
  String senderAddress = "did:bid:efVmotQW28QDtQyupnKTFvpjKQYs5bxf";
  String contractAddress = "did:bid:ef2gAT82SGdnhj87wQWb9suPKLbnk9NP";
  String senderPrivateKey = 	"priSPKnDue7AJ42gt7acy4AVaobGJtM871r1eukZ2M6eeW5LxG";
  Long amount = 0L;
  
  BIFContractInvokeByGasRequest request = new BIFContractInvokeByGasRequest();
  request.setSenderAddress(senderAddress);
  request.setPrivateKey(senderPrivateKey);
  request.setContractAddress(contractAddress);
  request.setBIFAmount(amount);
  request.setMetadata("contract remove zid invoke");
  request.setInput("{\"method\":\"removeZidData\",\"params\":	{\"zid\":\"88.1000\",\"type\":\"contract_address\",\"opFlag\": \"1\"}}");
  // 调用 BIFContractInvoke 接口
  BIFContractInvokeByGasResponse response = sdk.getBIFContractService().contractInvoke(request);
  if (response.getErrorCode() == 0) {
      System.out.println(JSON.toJSONString(response.getResult(), true));
  } else {
      System.out.println("error:      " + response.getErrorDesc());
  }
  ```

  标识删除接口与标识创建的核心参数基本相同，差异在input合约调用参数里，method字段为删除操作的合约函数名，params里是要删除的zid标识名，type标识类型（`GHR`, `SHR`是`contract_address`, `LHS`的是URL等类型）以及opFlag值（此处为1删除标志）。

###  合约查询

+ **标识查询**

  `Input`合约参数说明：

  	`method`：对应合约的查询接口函数名（`GHR`的查询接口是`queryZidRecord`，`SHR`合约的是`queryZidRecordShr`，`LHS`的是`queryZidRecordLhs`）。
		
  	`params`：含有type类型参数(`GHR`以及`SHR`的是`contract_address`，`LHS`可以是URL或其他自定义类型)，以及对应zid名。
  
  ```java
  // 初始化请求参数
  String contractAddress = "did:bid:ef2gAT82SGdnhj87wQWb9suPKLbnk9NP";
  BIFContractCallRequest request = new BIFContractCallRequest();
  request.setContractAddress(contractAddress);
  //标识查询合约接口操作
  request.setInput("{\"method\":\"queryZidRecord\",\"params\":{\"type\": \"contract_address\",\"zid\":\"88.1000\"}}");
  
  // 调用contractQuery接口
  BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
  if (response.getErrorCode() == 0) {
      BIFContractCallResult result = response.getResult();
      System.out.println(JSON.toJSONString(result, true));
  } else {
      System.out.println("error: " + response.getErrorDesc());
  }
  ```
  
    返回信息：
  
  ```java
  {
      "query_rets":[
          {
              "result":{
                  "type":"string",
                  "value":"{\"value\":[{\"index\":\"1\",\"type\":\"contract_address\",\"data\":{\"format\":\"string\",\"value\":\"did:bid:efuEAGFPJMsojwPGKzjkkk89888\"},\"ttl\":\"86400\",\"ttlType\":\"0\",\"timestamp\":\"0\",\"references\":[],\"adminRead\":\"1\",\"adminWrite\":\"1\",\"publicRead\":\"1\",\"publicWrite\":\"1\"}]}"
              }
          }
      ]
  }
  ```

+ **查询账户信息**

  标识合约操作的过程中可能需要查询账户详细信息，所以需要此接口。

  ```java
  // 待查询的账户地址
  String accountAddress = "did:bid:efVmotQW28QDtQyupnKTFvpjKQYs5bxf";
  BIFAccountGetInfoRequest request = new BIFAccountGetInfoRequest();
  request.setAddress(accountAddress);
  
  // 调用getAccount接口
  BIFAccountGetInfoResponse response = sdk.getBIFAccountService().getAccount(request);
  
  if (response.getErrorCode() == 0) {
      System.out.println(JSON.toJSONString(response.getResult(), true));
  } else {
      System.out.println("error: " + response.getErrorDesc());
  }
  ```

+ **查询交易信息**

  标识合约创建，修改等接口操作后，需要根据生成的hash查询交易是否成功等信息，故需要此接口查询。

  ```java
  // 初始化请求参数
  String txHash = "1653f54fbba1134f7e35acee49592a7c29384da10f2f629c9a214f6e54747705";
  BIFTransactionGetInfoRequest request = new BIFTransactionGetInfoRequest();
  request.setHash(txHash);
  
  // 调用getBIFInfo接口
  BIFTransactionGetInfoResponse response = sdk.getBIFTransactionService().getTransactionInfo(request);
  if (response.getErrorCode() == 0) {
      System.out.println(JSON.toJSONString(response.getResult(), true));
  } else {
      System.out.println("error: " + response.getErrorDesc());
  }
  ```

  返回信息：
  
  ```java
  {
  	"total_count":1,
  	"transactions":[{
  		"actual_fee":"477",
  		"close_time":1630760729249135,
  		"contract_tx_hashes": ["82411f9cd3a1fd820285a426bf43142925273b2e9522dc836ad7185f548500a0"],
  		"error_code":0,
  		"error_desc":"",
  		"hash":"b4495e6c124ea6d4c5c7094a687b8dd73bf85f7ac5f4805577c27fad56af912c",
  		"ledger_seq":22656,
  		"signatures":[{
       	"public_key":"b0656669660116b0b2ddfbba3f155962b311dc0afb671e2da069563a70fccabd9ff8c4",
              "sign_data":"7bfaa7c625619ddfd9a73c945f3231a21583c75b0d30b0c814dea43debace471edfb2485168429cadae30411b67996331e088ee9ae9636b593693f21c951b902"
          }],
          "transaction":{
  			"fee_limit":1000000,
  			"gas_price":1,
  			"metadata":"contract ",
  			"nonce":55,
  			"operations":[{
  				"pay_coin":{
  					"amount":1000,
  					"dest_address":"did:bid:efw8T4pMic9goJHe2FCNocaCb8AkDr3P",
  					"input":"{\"method\":\"removeZidData\",\"params\":{\"zid\":\"88.1000\",\"type\":\"contract_address\",\"opFlag\": \"1\"}}"
  				},
  				"type":7
  			}],
  			"source_address":"did:bid:efuEAGFPJMsojwPGKzjD8vZX1wbaUrVV"
  		},
  		"tx_size":353
  	}]
  }
  ```

