# 4. Openzeppelin合约模板

Openzeppelin是一套用Solidity语言编写, 基于EVM架构的**智能合约模板库**。星火链针对开源的Openzeppelin合约模板库做了一定的修改，主要有以下差异：

| 目录                                                | 简介                                   | 是否支持 |
| --------------------------------------------------- | -------------------------------------- | -------- |
| [utils](utils/utils.md "utils")                     | 工具类库                               | 部分支持 |
| [access](access/access.md "access")                 | 权限控制工具库                         | 完全支持 |
| [finance](finance/finance.md "finance")             | 财务类库                               | 不支持   |
| [metatx](metatx/metatx.md "metatx")                 | meta tx交易库，ERC2771标准             | 不支持   |
| [proxy](proxy/proxy.md "proxy")                     | 代理和可升级智能合约库                 | 完全支持 |
| [interface](interface/interface.md "interface")     | 标准合约接口文件                       | 完全支持 |
| [token](token/token.md "token")                     | 各类token的标准实现，如ERC721、ERC1155 | 完全支持 |
| [governance](governance/governance.md "governance") | 链上治理                               | 不支持   |
| [vendor](vendor/vendor.md "vendor")                 | time lock 接口                         | 完全支持 |

## 4.1 获取方式

1. 源码获取

   github地址：

   https://github.com/caict-4iot-dev/openzeppelin-contracts

2. npm包获取

   npm包地址：

   https://www.npmjs.com/package/@openzeppelin-bif/contracts

## 4.2 使用方式

1. 在remix插件中使用

   直接在合约文件中引用：

   ![image-20240515152331414](..\_static\images\image-20240515152331414.png)

2. 从github下载源码到本地，合约里填相对路径
3. 使用星火链的hardhat工具（暂未对外）

## 4.3 合约示例

### 4.3.1 合约权限控制

- 概述

  这个合约主要实现了一个基于角色的权限控制系统。用于对区块链账户实施基于角色的准入控制和交易限制的权限管理合约系统。它允许管理员和特权账户对其他账户施加合约层面的操作限制。

- 功能

  > 按照管理员、VIP和普通账户进行功能分类，当前合约的权限控制相关功能可以整理如下：
  > **管理员功能：**
  >
  > 设置 VIP 账号集合：
  >
  > 管理员可以添加或移除 VIP 账号，从而控制哪些账号拥有特殊的权限。
  >
  > 启用/禁用锁定功能：
  >
  > 管理员有权决定整个系统是否允许对账户进行锁定操作，以此来控制账户锁定功能的开关。
  >
  > 转移管理权限：
  >
  > 管理员可以将自己的管理权限转移给其他账号，实现管理权的变更和交接。
  >
  > 查询功能：
  >
  > 管理员可以查询当前的 VIP 账号列表、锁定账号列表，以及确认某个地址是否为 VIP 或被锁定。

  > **VIP 功能：**
  >
  > 对其他账号进行加锁/解锁操作：
  >
  > VIP 账号被赋予了对其他账号进行锁定的权限，这意味着 VIP 可以限制某些账号的访问或操作。
  >
  > VIP 同样可以对之前锁定的账号进行解锁操作，恢复其正常功能。
  >
  > 查询功能：
  >
  > VIP 可以查询锁定账号列表，以及确认某个地址是否被锁定。

  > **普通账户功能：**
  >
  > 账户锁定与解锁：
  >
  > 普通账户在被 VIP 锁定后，将无法进行某些操作或访问某些资源，直到被 VIP 解锁。
  >
  > 查询功能：
  >
  > 普通账户可以查询自己是否被锁定。

  > 通过这样的分类，可以更清晰地了解每个角色在权限控制体系中的职责和权限，从而确保系统的安全和有序运行。

  #### 函数说明

  > **管理员功能**：
  > 1\. 初始化合约并设置管理员账户
  > &#x20;   constructor() 函数：在合约部署时，调用此函数将合约的部署者设置为初始管理员。
  > 2\. 启用/禁用锁定功能
  > &#x20;   enableLock(bool \_lockEnabled) 函数：管理员可以调用此函数来启用或禁用锁定功能。当锁定功能关闭时，应释放所有锁定的账户。
  > 3\. 设置VIP账号
  > &#x20;   setVIPAddresses(address\[] memory \_vipAddresses) 函数：管理员可以通过此函数来设置或更新VIP账号集合，可以添加或移除VIP账号。
  > 4\. 转移管理员账户
  > &#x20;   transferAdmin(address \_newAdmin) 函数：管理员可以将自己的管理权限转移给另一个账户，实现管理权的变更。
  > **VIP 功能**：
  > 1\. 锁定某个账号
  > &#x20;   lockAddress(address \_address) 函数：VIP账号可以调用此函数来锁定指定的账户，限制其访问或操作。
  > 2\. 解锁某个账号
  > &#x20;   unlockAddress(address \_address) 函数：VIP账号可以调用此函数来解锁之前锁定的账户，恢复其正常功能。
  > **公共功能（管理员、VIP、普通账户均可查询）**：
  > 1\. 获取锁定账户地址列表
  > &#x20;   getLockedAddresses() 函数：返回当前所有被锁定的账户地址列表。
  > 2\. 检测账户是否锁定
  > &#x20;   isAddressLocked(address \_address) 函数：检查指定的账户地址是否被锁定，并返回结果。
  > 3\. 检测合约锁是否开启
  > &#x20;   isLockEnabled() 函数：返回当前合约的锁定功能是否开启的状态。
  > **辅助功能**：
  > &#x20; isLocked 映射：用于存储每个账户是否被锁定的状态。
  > &#x20; lockEnabled 变量：表示当前合约的锁定功能是否开启。
  > &#x20; lockedAddresses 数组：存储当前所有被锁定的账户地址。

- 合约代码：

  ```javascript
  // SPDX-License-Identifier: MIT
  pragma solidity ^0.8.20;
  
  import "@openzeppelin-bif/contracts/access/AccessControl.sol";
  
  contract VIPLockContract is AccessControl {
      bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
      bytes32 public constant VIP_ROLE = keccak256("VIP_ROLE");
  
      mapping(address => bool) public isLocked;
      bool public lockEnabled;
      address[] public lockedAddresses;
      //合约部署设置管理员账户
      constructor() {
          _grantRole(ADMIN_ROLE, msg.sender);
      }
      //仅管理员可操作
      modifier onlyAdmin() {
          require(hasRole(ADMIN_ROLE, msg.sender), "Only admin can call this function");
          _;
      }
      //仅VIP可操作
      modifier onlyVIP() {
          require(hasRole(VIP_ROLE, msg.sender), "Only VIP can call this function");
          _;
      }
      //管理员设置开关锁，若锁关闭，则释放全部锁定账户
      function enableLock(bool _lockEnabled) public onlyAdmin {
          lockEnabled = _lockEnabled;
          if (!_lockEnabled) {
              for (uint256 i = 0; i < lockedAddresses.length; i++) {
                  isLocked[lockedAddresses[i]] = false;
              }
              delete lockedAddresses;
          }
      }
      //管理员设置VIP账号
      function setVIPAddresses(address[] memory _vipAddresses) public onlyAdmin {
          uint256 length = _vipAddresses.length; 
          for (uint256 i=0; i < length; i++) {
              grantRole(VIP_ROLE, _vipAddresses[i]);
          }
      }
      //VIP锁定某个账号
      function lockAddress(address _address) public onlyVIP {
          require(lockEnabled, "Lock is not enabled");
          require(!isLocked[_address], "Address is already locked");
          isLocked[_address] = true;
          lockedAddresses.push(_address);
      }
      //VIP解锁某个账号
      function unlockAddress(address _address) public onlyVIP {
          require(lockEnabled, "Lock is not enabled");
          require(isLocked[_address], "Address is not locked");
          isLocked[_address] = false;
          for (uint256 i = 0; i < lockedAddresses.length; i++) {
              if (lockedAddresses[i] == _address) {
                  lockedAddresses[i] = lockedAddresses[lockedAddresses.length - 1];
                  lockedAddresses.pop();
                  break;
              }
          }
      }
      //转移管理员账户
      function transferAdmin(address _newAdmin) public onlyAdmin {
          grantRole(ADMIN_ROLE, _newAdmin);
          renounceRole(ADMIN_ROLE, msg.sender);
      }
      //获取锁定账户地址
      function getLockedAddresses() public view returns (address[] memory) {
          return lockedAddresses;
      }
      //检测账户是否锁定
      function isAddressLocked(address _address) public view returns (bool) {
          return isLocked[_address];
      }
      //检测合约锁是否开启
      function isLockEnabled() public view returns (bool) {
          return lockEnabled;
      }
  }
  ```

### 4.3.2 合约数据管理

- 概述
`DatabaseManagement`合约是一个简洁的Solidity智能合约，旨在管理一个基于区块链的数据库。此合约允许存在一个管理员（admin）和多个操作员（operators），只有管理员有权限添加或删除操作员，而操作员负责管理存储在合约中的数据。该数据分为两类：一类是字符串的集合，另一类是键值对映射，键和值都是字符串类型。

- 功能
> **管理员相关**
> 管理员设定：合约部署时，部署者自动成为管理员。
> 获取管理员地址：任何人都可以查询当前的管理员地址。
>
> **操作员相关**
>
> 添加操作员：管理员可以添加新的操作员。
>
> 删除操作员：管理员可以删除现有的操作员。
>
> 查询操作员：提供一个函数来检查一个地址是否为操作员。
>
> 获取当前操作员列表：允许查询当前所有操作员的地址。
>
> **数据管理**
>
> 添加字符串：操作员可以向字符串集合添加新的字符串。
>
> 删除字符串：操作员可以从集合中删除指定的字符串。
>
> 更新字符串：允许先删除旧字符串，再添加新字符串的方式进行更新。
>
> 查询字符串：检查指定的字符串是否存在于集合中。
>
> **映射数据库操作**
>
> 更新映射：操作员可以更新映射数据库中的元素。
>
> 查询映射值：通过键查询映射数据库中的值。
>
> 删除映射元素：操作员可以删除映射数据库中的指定元素。
>
> 添加映射元素：操作员可以向映射数据库添加新的元素，前提是键不存在或与之关联的值为空。
>
> **访问控制**
>
> onlyAdmin：修饰符用于限制只有管理员可以执行某些操作。
> onlyOperator：修饰符确保只有操作员可以执行特定的数据库操作。

>函数说明
>
> **Admin Functions**
>`getAdmin()`: 返回当前管理员的地址。
>`addOperator(address _operator)`: 管理员调用此函数以添加新的操作员。
>`removeOperator(address _operator)`: 管理员调用此函数以删除指定的操作员。
> **Operator Functions**
>`getCurrentOperators()`: 返回当前所有操作员的地址数组。
>`addString(string calldata stringValue)`: 操作员可以添加新的字符串到集合中。
> `updateString(string calldata oldStringValue, string calldata newStringValue)`: 允许操作员通过删除旧字符串再添加新字符串来更新集合。
>`removeString(string calldata stringValue)`: 从集合中删除指定的字符串。
>`containsString(string calldata stringValue)`: 查询指定字符串是否存在于集合中。
>`updateMapping(string calldata key, string calldata value)`: 更新映射数据库。
>`getMapping(string calldata key)`: 通过键查询映射数据库中的值。
>`removeMapping(string calldata key)`: 删除映射数据库中的指定元素。
>`addToMappingDatabase(string calldata key, string calldata value)`: 在映射数据库中添加新元素，若键已存在则阻止操作。
- 安全性

  合约使用`onlyAdmin`和`onlyOperator`修饰符确保操作的授权和安全性。对于每一个敏感操作，包括添加或删除操作员、更新数据库，都进行了适当地权限检查。

- 注意事项

  删除字符串或操作员时，为了保持数据连贯性并减少`gas`消耗，采用了将目标元素与数组最后一个元素交换然后`pop()`的逻辑。

  在向映射数据库添加数据时，进行键冲突检查以避免意外覆盖现有数据。

- 代码

  ```javascript
  pragma solidity ^0.8.0;
  
  import "@openzeppelin-bif/contracts/access/Ownable.sol";
  import "@openzeppelin-bif/contracts/utils/Strings.sol";
  
  contract DatabaseManagement is Ownable {
  
      /**
       引入了operatorAddresses数组来追踪所有当前的操作员地址。当一个操作员被添加时，他们的地址被推入
       operatorAddresses数组；当一个操作员被删除时，他们的地址被从数组中移除（通过将其与数组最后一个
       元素交换然后调用pop()方法来实现，以保持数组的连续性和减少gas消耗）。
       getCurrentOperators函数允许外部调用者获取当前所有操作员的地址数组。
      */
      mapping(address => bool) private operators;
      address[] private operatorAddresses; 
      
      // 使用动态数组存储字符串集合
      string[] private stringDatabase;
  
      // 辅助映射，用于快速检查字符串是否在集合中
      mapping(string => bool) private stringExists;
  
      mapping(string => string) private mappingDatabase;
  
      modifier onlyOperator() {
          require(operators[msg.sender], "Only operator can perform this action");
          _;
      }
  
      constructor() Ownable(msg.sender) {  
      }
  
      function getAdmin() public view returns (address) {
          return owner();
      }
  
      function hasOperator(address operator) public view returns (bool) {
          return operators[operator];
      }
  
      function addOperator(address _operator) external onlyOwner {
          if (!operators[_operator]) {
              operators[_operator] = true;
              operatorAddresses.push(_operator); // 同时更新操作员数组
          }
      }
  
      function removeOperator(address _operator) external onlyOwner {
          if (operators[_operator]) {
              operators[_operator] = false;
              for (uint i = 0; i < operatorAddresses.length; i++) {
                  if (operatorAddresses[i] == _operator) {
                      operatorAddresses[i] = operatorAddresses[operatorAddresses.length - 1];
                      operatorAddresses.pop(); // 同时更新操作员数组
                      break;
                  }
              }
          }
      }
  
      // 新增函数，返回当前所有操作员的地址数组
      function getCurrentOperators() external view returns (address[] memory) {
          return operatorAddresses;
      }
  
      // 操作员增加新的字符串到集合中
      function addString(string calldata stringValue) public onlyOperator {
          require(!stringExists[stringValue], "String already exists in database");
          stringDatabase.push(stringValue);
          stringExists[stringValue] = true;
      }
  
      // 先删除旧的字符串，然后添加一个新的字符串
      function updateString(string calldata oldStringValue, string calldata newStringValue) public onlyOperator {
          require(stringExists[oldStringValue], "String does not exist in database");
          removeString(oldStringValue);
          addString(newStringValue);
      }
  
      // 操作员删除集合中的字符串
      function removeString(string calldata stringValue) public onlyOperator {
          require(stringExists[stringValue], "String does not exist in database");
          // 将存在标记设置为false
          stringExists[stringValue] = false;
          
          // 移除操作需要找到字符串的索引，然后用数组最后一个元素替换它，并移除最后一个元素
          for(uint i = 0; i < stringDatabase.length; i++) {
              //if(keccak256(bytes(stringDatabase[i])) == keccak256(bytes(stringValue))) {
              if(Strings.equal(stringDatabase[i], stringValue)) {
                  stringDatabase[i] = stringDatabase[stringDatabase.length - 1];
                  break;
              }
          }
          stringDatabase.pop();
      }
      
      // 查询字符串是否存在于集合中
      function containsString(string calldata stringValue) public view returns (bool) {
          return stringExists[stringValue];
      }
  
      // 操作员更新映射数据库
      function updateMapping(string calldata key, string calldata value) external onlyOperator {
          mappingDatabase[key] = value;
      }
  
      // 查询映射数据库
      function getMapping(string calldata key) public view returns (string memory) {
          require(bytes(mappingDatabase[key]).length != 0, "Key does not exist");
          return mappingDatabase[key];
      }
  
      // 删除映射数据库中的一个元素
      function removeMapping(string calldata key) external onlyOperator {
          require(bytes(mappingDatabase[key]).length != 0, "Key does not exist");
          delete mappingDatabase[key];
      }
  
      // 修改后的addToMappingDatabase函数，检查键是否冲突
      function addToMappingDatabase(string calldata key, string calldata value) external onlyOperator {
          // 检查键是否已经存在，并且相关联的值不为空
          require(bytes(mappingDatabase[key]).length == 0, "Key already exists with a non-empty value");
          mappingDatabase[key] = value;
      }
  }
  ```

  
