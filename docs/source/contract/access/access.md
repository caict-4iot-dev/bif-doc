# access

| 简介   | 权限控制工具库 |
| ---- | ------- |
| 是否支持 | yes     |
| 字段名  |         |

提供了限制谁可以访问合约的功能或何时可以访问的方法。

详细描述文档：

[Access Control - OpenZeppelin Docs  https://docs.openzeppelin.com/contracts/5.x/api/access](https://docs.openzeppelin.com/contracts/5.x/api/access "Access Control - OpenZeppelin Docs  https://docs.openzeppelin.com/contracts/5.x/api/access")

| 目录 & 文件            | 功能                     | 详细信息             |
| ------------------ | ---------------------- | ---------------- |
| extensions         | 基于AccessControl拓展实现的功能 | 枚举角色成员/管理admin角色 |
| manager            |                        |                  |
| IAccessControl.sol | AccessControl接口        |                  |
| AccessControl.sol  | AccessControl接口实现逻辑    |                  |
| Ownable.sol        | 基本访问控制机制               |                  |
| Ownable2Step.sol   | 两步转移合约控制所有者            |                  |

> 📌extensions

- IAccessControlEnumerable.sol

  \[描述] IAccessControl的扩展，允许枚举每个角色的成员
  ```c
  //根据角色和索引值返回对应的地址
  function getRoleMember(bytes32 role, uint256 index) external view returns (address);
  //获取指定角色授予的数量
  function getRoleMemberCount(bytes32 role) external view returns (uint256)
  ```
- AccessControlEnumerable.sol

  \[描述] 允许枚举每个角色的成员

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {AccessControlEnumerable} from "../../../openzeppelin-contracts/contracts/access/extensions/AccessControlEnumerable.sol";
  import {IAccessControlEnumerable} from "../../../openzeppelin-contracts/contracts/access/extensions/IAccessControlEnumerable.sol";

  contract MyAccessControlEnumerable is AccessControlEnumerable {
      function supportsInterface() public returns(bool) {
          return AccessControlEnumerable.supportsInterface(type(IAccessControlEnumerable).interfaceId);
      }

      //为某个账户设置某个角色
      function GrantRole(bytes32 role, address account) public returns(bool){
          return _grantRole(role, account);
      }

      //为某个账户撤销某个角色
      function RevokeRole(bytes32 role, address account) public returns(bool){
          return _revokeRole(role, account);
      }

      function GetRoleMember(bytes32 role, uint256 index) public returns(address){
          return getRoleMember(role, index);
      }

      function GetRoleMemberCount(bytes32 role) public returns(uint256){
          return getRoleMemberCount(role);
      }

  }
  ```
- IAccessControlDefaultAdminRules.sol

  \[描述] IAccessControl的扩展，管理Admin相关功能
  ```c
  ERRORS:
  //转移默认管理延迟的延迟是强制的，操作必须等到schedule
  19ca5ebb: AccessControlEnforcedDefaultAdminDelay(uint48)
  //至少违反了下列一项规定:
  //DEFAULT_ADMIN_ROLE只能由它自己管理。
  //DEFAULT_ADMIN_ROLE一次只能由一个帐户持有。
  //任何DEFAULT_ADMIN_ROLE转移必须分两个延迟步骤
  3fc3c27a: AccessControlEnforcedDefaultAdminRules()
  c22c8022: AccessControlInvalidDefaultAdmin(address) //新的默认管理员不是有效的默认管理员

  FUNCTIONS:
  //返回DEFAULT_ADMIN_ROLE持有者地址
  function defaultAdmin() external view returns (address)
  //返回由newAdmin和accept schedule，schedule过后newAdmin将能够通过调用acceptDefaultAdminTransfer来接受defaultAdmin角色，完成角色转移
  function pendingDefaultAdmin() external view returns (address newAdmin, uint48 acceptSchedule)
  //返回调度defaultAdmin转移接受所需的延迟
  //accept schedule = currentTime + defaultAdminDelay
  function defaultAdminDelay() external view returns (uint48)
  //返回newDelay和schedule。在schedule过后，newDelay将立即对以beginDefaultAdminTransfer开始的每个新的defaultAdmin转移生效
  function pendingDefaultAdminDelay() external view returns (uint48 newDelay, uint48 effectSchedule)
  //currentTime + defaultAdminDelay = schedule，当设置pendingDefaultAdmin后，开始defaultAdmin的转移
  function beginDefaultAdminTransfer(address newAdmin) external
  //取消先前由beginDefaultAdminTransfer开始的defaultAdmin转移
  function cancelDefaultAdminTransfer() external
  //完成先前由beginDefaultAdminTransfer开始的defaultAdmin转移
  //调用函数后:
  //DEFAULT_ADMIN_ROLE应该被授予调用者。
  //DEFAULT_ADMIN_ROLE应该从上一个持有者中撤销。
  //pendingDefaultAdmin应该重置为零值
  function acceptDefaultAdminTransfer() external
  //通过设置一个pendingDefaultAdminDelay(在当前时间戳加上defaultAdminDelay之后生效)来启动一个defaultAdminDelay更新
  function changeDefaultAdminDelay(uint48 newDelay) external
  //取消预定的defaultAdminDelay更改
  function rollbackDefaultAdminDelay() external
  //增加defaultAdminDelay(使用changeDefaultAdminDelay调度)生效的最大时间，以秒为单位。默认为5天
  function defaultAdminDelayIncreaseWait() external view returns (uint48)

  ```
- AccessControlDefaultAdminRules.sol

  \[描述] 使用DefaultAdmin 进行角色管理的相关逻辑

  \[是否支持] 支持

  \[修改点] 星火链返回timestamp长度为16位，星火链返回地址长度位10
  ```git
  @@ -218,7 +218,7 @@ abstract contract AccessControlDefaultAdminRules is IAccessControlDefaultAdminRu
        * Internal function without access restriction.
        */
       function _beginDefaultAdminTransfer(address newAdmin) internal virtual {
  -        uint48 newSchedule = SafeCast.toUint48(block.timestamp) + defaultAdminDelay();
  +        uint48 newSchedule = SafeCast.toUint48(block.timestamp / 1000000) + defaultAdminDelay();
           _setPendingDefaultAdmin(newAdmin, newSchedule);
           emit DefaultAdminTransferScheduled(newAdmin, newSchedule);
       }
  @@ -284,7 +284,7 @@ abstract contract AccessControlDefaultAdminRules is IAccessControlDefaultAdminRu
        * Internal function without access restriction.
        */
       function _changeDefaultAdminDelay(uint48 newDelay) internal virtual {
  -        uint48 newSchedule = SafeCast.toUint48(block.timestamp) + _delayChangeWait(newDelay);
  +        uint48 newSchedule = SafeCast.toUint48(block.timestamp / 1000000) + _delayChangeWait(newDelay);
           _setPendingDelay(newDelay, newSchedule);
           emit DefaultAdminDelayChangeScheduled(newDelay, newSchedule);
       }
  @@ -391,6 +391,6 @@ abstract contract AccessControlDefaultAdminRules is IAccessControlDefaultAdminRu
        * @dev Defines if an `schedule` is considered passed. For consistency purposes.
        */
       function _hasSchedulePassed(uint48 schedule) private view returns (bool) {
  -        return schedule < block.timestamp;
  +        return schedule < (block.timestamp / 1000000);
  ```
  ```git
  pragma solidity ^0.8.20;

  import {AccessControlDefaultAdminRules} from "../../../openzeppelin-contracts/contracts/access/extensions/AccessControlDefaultAdminRules.sol";
  import {IAccessControlDefaultAdminRules} from "../../../openzeppelin-contracts/contracts/access/extensions/IAccessControlDefaultAdminRules.sol";

  contract MyAccessControlDefaultAdminRules is AccessControlDefaultAdminRules {
      constructor(uint48 initialDelay, address initialDefaultAdmin) AccessControlDefaultAdminRules(initialDelay, initialDefaultAdmin) {

      }
      
      function supportsInterface() public returns(bool) {
          return AccessControlDefaultAdminRules.supportsInterface(type(IAccessControlDefaultAdminRules).interfaceId);
      }

      //owner 与 defaultAdmin相同 owner是为了实现IERC5313标准
      function Owner() public returns(address) {
          return owner();
      }

      function DefaultAdmin() public returns(address) {
          return defaultAdmin();
      }

      function GrantRole(bytes32 role, address account) public {
          grantRole(role, account);
      }

      function RevokeRole(bytes32 role, address account) public {
          revokeRole(role, account);
      }

      function RenounceRole(bytes32 role, address account) public {
          renounceRole(role, account);
      }

      function PendingDefaultAdmin() public returns(address,uint48) {
          return pendingDefaultAdmin();
      }
      
      function DefaultAdminDelay() public returns(uint48) {
          return defaultAdminDelay();
      }

      function PendingDefaultAdminDelay() public returns(uint48, uint48) {
          return pendingDefaultAdminDelay();
      }

      function DefaultAdminDelayIncreaseWait() public returns(uint48) {
          return defaultAdminDelayIncreaseWait();
      }

      function BeginDefaultAdminTransfer(address newAdmin) public {
          beginDefaultAdminTransfer(newAdmin);
      }

      function CancelDefaultAdminTransfer() public {
          cancelDefaultAdminTransfer();
      }

      function AcceptDefaultAdminTransfer() public {
          acceptDefaultAdminTransfer();
      }

      function ChangeDefaultAdminDelay(uint48 newDelay) public {
          changeDefaultAdminDelay(newDelay);
      }

      function RollbackDefaultAdminDelay() public {
          rollbackDefaultAdminDelay();
      }
  }
  ```
  > 📌manager
- IAuthority.sol

  \[描述] 许可标准接口
  ```c
  FUNCTIONS:
  //如果调用者可以在目标上调用由函数选择器标识的函数，则返回true。
  function canCall(address caller, address target, bytes4 selector) external view returns (bool allowed)

  ```
- Authority.sol

  \[描述] 许可标准接口

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {AuthorityUtils} from "../../../openzeppelin-contracts/contracts/access/manager/AuthorityUtils.sol";

  contract MyAuthority {
      function canCall(
          address caller,
          address target,
          bytes4 selector
      ) public virtual returns (bool, uint32) {  
          // 调用目标合约的函数  
          (bool success, bytes memory result) = target.call(abi.encodeWithSelector(selector));
          (bool ret, uint32 delay) = abi.decode(result, (bool, uint32));
          return (ret, delay);
      }
  }

  contract MyAuthorityUtils {
      function test() external returns(bool, uint32) {
          return (false,10);
      }

      function canCallWithDelay() public returns(bool, uint32) {
          address authority = address(new MyAuthority());
          return AuthorityUtils.canCallWithDelay(authority, address(this), address(this), this.test.selector);
      }
  }
  ```
- IAccessManaged.sol

  \[描述] 许可标准接口
  ```c
  ERRORS:
  c2f31e5e: AccessManagedInvalidAuthority(address)
  af77169d: AccessManagedRequiredDelay(address,uint32)
  068ca9d8: AccessManagedUnauthorized(address)

  FUNCTIONS:
  //返回当前管理者地址
  function authority() external view returns (address);
  //设置新管理员，调用者必须为当前的管理员
  function setAuthority(address) external;
  //在延迟调用情况下返回被调用函数的selector
  function isConsumingScheduledOp() external view returns (bytes4);

  ```
- AccessManaged.sol

  \[描述] 许可标准接口

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {AccessManaged} from "../../../openzeppelin-contracts/contracts/access/manager/AccessManaged.sol";

  contract MyAuthority {
      function canCall(
          address caller,
          address target,
          bytes4 selector
      ) public virtual returns (bool, uint32) {  
          // 调用目标合约的函数  
          (bool success, bytes memory result) = target.call(abi.encodeWithSelector(selector));
          (bool ret, uint32 delay) = abi.decode(result, (bool, uint32));
          return (ret, delay);
      }
  }

  contract MyAccessManaged is AccessManaged {
      constructor(address initialAuthority) AccessManaged(initialAuthority) {
      }

      function Authority() public returns(address) {
          return authority();
      }

      function SetAuthority(address newAuthority) public {
          MyAuthority add = new MyAuthority();
          setAuthority(address(add));
      }

      function IsConsumingScheduledOp() public returns (bytes4){
          return isConsumingScheduledOp();
      }
  }
  ```
- IAccessManage.sol

  \[描述] 许可标准接口
  ```c
  ERRORS:
  813e9459: AccessManagerAlreadyScheduled(bytes32)
  5f159e63: AccessManagerBadConfirmation()
  78a5d6e4: AccessManagerExpired(bytes32)
  0813ada2: AccessManagerInvalidInitialAdmin(address)
  5a068bc8: AccessManagerLockedAccount(address)
  1871a90c: AccessManagerLockedRole(uint64)
  18cb6b7a: AccessManagerNotReady(bytes32)
  60a299b0: AccessManagerNotScheduled(bytes32)
  f07e038f: AccessManagerUnauthorizedAccount(address,uint64)
  81c6f24b: AccessManagerUnauthorizedCall(address,address,bytes4)
  3fe2751c: AccessManagerUnauthorizedCancel(address,address,address,bytes4)
  320ff748: AccessManagerUnauthorizedConsume(address)

  FUNCTIONS:
  //检查一个地址(调用者)是否被授权直接调用给定合约上的给定函数(没有限制)。此外，它返回通过调度和执行工作流间接执行调用所需的延迟。
  function canCall(
          address caller,
          address target,
          bytes4 selector
      ) external view returns (bool allowed, uint32 delay)
  //计划提案的过期延迟。默认为1周。
  function expiration() external view returns (uint32)
  //更新delay的最小间隔，默认为5天
  function minSetback() external view returns (uint32);
  //判断给定的合约地址是否禁止访问
  function isTargetClosed(address target) external view returns (bool);
  //获取调用某个函数需要的角色权限
  function getTargetFunctionRole(address target, bytes4 selector) external view returns (uint64);
  //获取访问某个目标合约的管理员延迟时间
  function getTargetAdminDelay(address target) external view returns (uint32);
  //获取作为给定角色的管理员的角色的id
  function getRoleAdmin(uint64 roleId) external view returns (uint64)
  //获取作为给定角色的监护人的角色
  function getRoleGuardian(uint64 roleId) external view returns (uint64)
  //获取授予当前角色的延迟时间
  function getRoleGrantDelay(uint64 roleId) external view returns (uint32)
  //获取给定角色的给定帐户的访问详细信息
  function getAccess(uint64 roleId, address account) external view returns (uint48, uint32, uint32, uint48);
  //检查给定帐户当前是否具有与给定角色对应的权限级别
  function hasRole(uint64 roleId, address account) external view returns (bool, uint32)
  //为角色添加标签，以提高用户对角色的可发现性
  function labelRole(uint64 roleId, string calldata label) external
  //这为帐户提供了调用限制于此角色的任何函数的授权
  function grantRole(uint64 roleId, address account, uint32 executionDelay) external
  //从某个中移除给定账号信息，立即生效
  function revokeRole(uint64 roleId, address account) external
  //调用者自己移除某个权限，立即生效
  function renounceRole(uint64 roleId, address callerConfirmation) external
  //设置给定角色的admin
  function setRoleAdmin(uint64 roleId, uint64 admin) external
  //更改给定角色的监护人
  function setRoleGuardian(uint64 roleId, uint64 guardian) external
  //更新授权某个角色的延迟时间
  function setGrantDelay(uint64 roleId, uint32 newDelay) external
  //设置调用由“目标”合约中的“选择器”标识的函数所需的角色
  function setTargetFunctionRole(address target, bytes4[] calldata selectors, uint64 roleId) external
  //设置更改给定目标合约配置的延迟时间
  function setTargetAdminDelay(address target, uint32 newDelay) external
  //设置给定合约禁止访问标志
  function setTargetClosed(address target, bool closed) external
  //返回计划操作准备执行的时间点
  function getSchedule(bytes32 id) external view returns (uint48)
  //返回具有给定id的最近调度操作的nonce
  function getNonce(bytes32 id) external view returns (uint32)
  //调度延迟的操作以供将来执行，并返回操作标识符
  function schedule(address target, bytes calldata data, uint48 when) external returns (bytes32, uint32)
  //执行一个延迟受限的函数，前提是事先对其进行了适当的调度，或者执行延迟为0。
  function execute(address target, bytes calldata data) external payable returns (uint32)
  //取消预定的(延迟的)操作
  function cancel(address caller, address target, bytes calldata data) external returns (uint32)
  //使用针对调用方的计划操作
  function consumeScheduledOp(address caller, bytes calldata data) external
  //用于延迟操作的哈希函数
  function hashOperation(address caller, address target, bytes calldata data) external view returns (bytes32)
  //更改由此管理器实例管理的目标的权限
  function updateAuthority(address target, address newAuthority) external;

  ```
- AccessManager.sol

  \[描述] 许可标准接口

  \[是否支持] 支持

  \[修改点]
  ```git
  --- a/contracts/access/manager/AccessManager.sol
  +++ b/contracts/access/manager/AccessManager.sol
  @@ -635,7 +635,7 @@ contract AccessManager is Context, Multicall, IAccessManager {
               selector == this.setTargetFunctionRole.selector
           ) {
               // First argument is a target.
  -            address target = abi.decode(data[0x04:0x24], (address));
  +            address target = abi.decode(data[0x04:0x28], (address));
               uint32 delay = getTargetAdminDelay(target);
               return (true, ADMIN_ROLE, delay);
           }
  @@ -643,7 +643,7 @@ contract AccessManager is Context, Multicall, IAccessManager {
           // Restricted to that role's admin with no delay beside any execution delay the caller may have.
           if (selector == this.grantRole.selector || selector == this.revokeRole.selector) {
               // First argument is a roleId.
  -            uint64 roleId = abi.decode(data[0x04:0x24], (uint64));
  +            uint64 roleId = abi.decode(data[0x04:0x28], (uint64));
               return (true, getRoleAdmin(roleId), 0);
           }
  ```
  &#x20;

  ![](<image/AccessManager 关系_RXes3czm30.jpg>)
  ```c
  pragma solidity ^0.8.20;

  contract TestContract {
      //test function
      function testA() public {

      }

      function testB(bool ret) public returns(bool) {
          return ret;
      }
  }

  import {AccessManager} from "../../../openzeppelin-contracts/contracts/access/manager/AccessManager.sol";

  contract MyAccessManager {
      AccessManager manager;

      constructor() {
          manager = new AccessManager(address(this));
      }

      function expiration() public returns (uint32) {
          return manager.expiration();
      }

      function minSetback() public returns (uint32) {
          return manager.minSetback();
      }

      function isTargetClosed(address target) public returns (bool) {
          return manager.isTargetClosed(target);
      }

      function getTargetFunctionRole(address target, bytes4 selector) public returns (uint64) {
          return manager.getTargetFunctionRole(target, selector);
      }

      function getTargetAdminDelay(address target) public returns (uint32) {
          return manager.getTargetAdminDelay(target);
      }

      function getRoleAdmin(uint64 roleId) public returns (uint64) {
          return manager.getRoleAdmin(roleId);
      }

      function getRoleGuardian(uint64 roleId) public returns (uint64) {
          return manager.getRoleGuardian(roleId);
      }

      function getRoleGrantDelay(uint64 roleId) public returns (uint32) {
          return manager.getRoleGrantDelay(roleId);
      }

      function getAccess(
          uint64 roleId,
          address account
      ) public returns (uint48, uint32, uint32, uint48) {
          return manager.getAccess(roleId, account);
      }

      function hasRole(
          uint64 roleId,
          address account
      ) public returns (bool, uint32) {
          return manager.hasRole(roleId, account);
      }

      function labelRole(uint64 roleId, string calldata label) public {
          manager.labelRole(roleId, label);
      }

      function grantRole(uint64 roleId, address account, uint32 executionDelay) public {
          manager.grantRole(roleId, account, executionDelay);
      }

      function revokeRole(uint64 roleId, address account) public {
          manager.revokeRole(roleId, account);
      }

      //由放弃角色的账户自己调用该接口
      function renounceRole(uint64 roleId, address callerConfirmation) public {
          manager.renounceRole(roleId, callerConfirmation);
      }

      function setRoleAdmin(uint64 roleId, uint64 admin) public {
          manager.setRoleAdmin(roleId, admin);
      }

      function setRoleGuardian(uint64 roleId, uint64 guardian) public {
          manager.setRoleGuardian(roleId, guardian);
      }

      function setGrantDelay(uint64 roleId, uint32 newDelay) public {
          manager.setGrantDelay(roleId, newDelay);
      }

      //调用该接口前，先部署TestContract合约
      function setTargetFunctionRole(
          address target,
          bytes4[] memory selectors,
          uint64 roleId
      ) public {
          manager.setTargetFunctionRole(target, selectors, roleId);
      }

      function setTargetAdminDelay(address target, uint32 newDelay) public {
          manager.setTargetAdminDelay(target, newDelay);
      }

      function setTargetClosed(address target, bool closed) public {
          manager.setTargetClosed(target, closed);
      }

      function getSchedule(bytes32 id) public returns (uint48) {
          return manager.getSchedule(id);
      }

      function getNonce(bytes32 id) public returns (uint32) {
          return manager.getNonce(id);
      }

      function schedule(
          address target,
          bytes calldata data,
          uint48 when
      ) public virtual returns (bytes32, uint32) {
          return manager.schedule(target, data, when);
      }

      function execute(address target, bytes calldata data) public payable returns (uint32) {
          return manager.execute(target, data);
      }

      function cancel(address caller, address target, bytes memory data) public returns (uint32) {
          return manager.cancel(caller, target, data);
      }

      function hashOperation(address caller, address target, bytes calldata data) public returns (bytes32) {
          return manager.hashOperation(caller, target, data);
      }

      function updateAuthority(address target, address newAuthority) public {
          manager.updateAuthority(target, newAuthority);
      }
  }
  ```
- IAccessControl.sol

  \[描述] AccessControl接口文件；描述实现的接口
  ```c
  ERRORS:
  6697b232: AccessControlBadConfirmation()  //调用者不匹配
  e2517d3f: AccessControlUnauthorizedAccount(address,bytes32) //账户缺失操作权限

  FUNCTIONS:
  //某个账户是否有被赋予role操作权限
  function hasRole(bytes32 role, address account) external view returns (bool);
  //返回控制角色的管理源角色
  function getRoleAdmin(bytes32 role) external view returns (bytes32);
  //授予某个账户角色
  function grantRole(bytes32 role, address account) external;
  //撤销某个账户角色
  function revokeRole(bytes32 role, address account) external;
  //合约所有者放弃某个角色
  function renounceRole(bytes32 role, address callerConfirmation)

  ```
- AccessControl.sol

  \[描述] AccessControl接口的实现，支持ERC165标准

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {AccessControl} from "../../openzeppelin-contracts/contracts/access/AccessControl.sol";
  import {IAccessControl} from "../../openzeppelin-contracts/contracts/access/IAccessControl.sol";

  contract MyAccessControl is AccessControl {

      constructor() {
          AccessControl._grantRole(0x0, msg.sender);
      }

      //检测当前合约是否实现了ERC165标准
      function supportsInterface() public returns(bool) {
          return AccessControl.supportsInterface(type(IAccessControl).interfaceId);
      }

      //为某个role角色设置adminRole
      function SetRoleAdmin(bytes32 role, bytes32 adminRole) public {
          AccessControl._setRoleAdmin(role, adminRole);
      }

      function GetRoleAdmin(bytes32 role) public returns(bytes32) {
          return AccessControl.getRoleAdmin(role);
      }

      //为某个账户设置某个角色
      function GrantRole(bytes32 role, address account) public{
          return AccessControl.grantRole(role, account);
      }

      //判断某个账户是否有某个角色
      function HasRole(bytes32 role, address account) public returns(bool) {
          return AccessControl.hasRole(role, account);
      }

      //为某个账户撤销某个角色
      function RevokeRole(bytes32 role, address account) public {
          AccessControl._revokeRole(role, account);
      }

      //合约所有者主动放弃某个角色
      function RenounceRole(bytes32 role, address callerConfirmation) public {
          AccessControl.renounceRole(role, callerConfirmation);
      }
  }

  ```
- Ownable.sol

  \[描述] 它提供了一个基本的访问控制机制，其中有一个帐户(所有者)可以被授予对特定功能的独占访问权

  \[是否支持] 支持
  ```c
  ERRORS：
  118cdaa7: OwnableUnauthorizedAccount(address); //调用者未被授予操作权限
  1e4fbdf7: OwnableInvalidOwner(address) //非法所有者账户

  pragma solidity ^0.8.20;

  import {Ownable} from "../../openzeppelin-contracts/contracts/access/Ownable.sol";

  contract MyOwnable is Ownable {
      constructor() Ownable(msg.sender) {

      }

      function GetOwner() public returns(address) {
          return owner();
      }

      function RenounceOwnerShip() public {
          renounceOwnership();
      }

      function TransferOwnership(address newOwner) public {
          transferOwnership(newOwner);
      }
  }

  ```
- Ownable2Step.sol

  \[描述] 两步转移合约owner，transferOwnership写入pendingowner；后续通过acceptOwnership真正转移owner

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {Ownable2Step} from "../../openzeppelin-contracts/contracts/access/Ownable2Step.sol";
  import {Ownable} from "../../openzeppelin-contracts/contracts/access/Ownable.sol";

  contract MyOwnable2Step is Ownable2Step {
      constructor() Ownable(msg.sender) {}

      function PendingOwner() public returns(address) {
          return pendingOwner();
      }

      function TransferOwnership(address newOwner) public{
          return transferOwnership(newOwner);
      }

      function AcceptOwnership() public {
          acceptOwnership();
      }
  }

  ```
