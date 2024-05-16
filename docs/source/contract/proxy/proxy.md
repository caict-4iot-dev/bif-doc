# proxy

| 简介   | 代理和可升级智能合约库 |
| ---- | ----------- |
| 是否支持 | yes         |
| 字段名  |             |

实现了不同的代理模式。信标代理、透明代理、UUPS代理。相关参考

[https://cloud.tencent.com/developer/article/2152968?areaSource=102001.3\&traceId=6-Em9T1yT0IVx1R8SdkQP](https://cloud.tencent.com/developer/article/2152968?areaSource=102001.3\&traceId=6-Em9T1yT0IVx1R8SdkQP "https://cloud.tencent.com/developer/article/2152968?areaSource=102001.3\&traceId=6-Em9T1yT0IVx1R8SdkQP")

详细描述文档：

[ Proxies - OpenZeppelin Docs  https://docs.openzeppelin.com/contracts/5.x/api/proxy](https://docs.openzeppelin.com/contracts/5.x/api/proxy " Proxies - OpenZeppelin Docs  https://docs.openzeppelin.com/contracts/5.x/api/proxy")

| 目录 & 文件     | 功能                                                 | 详细信息    |
| ----------- | -------------------------------------------------- | ------- |
| beacon      | 合约实现了一个代理，该代理从UpgradeableBeacon获取每个调用的实现地址         | 信标代理人   |
| ERC1967     | 该合约实现了一个可升级的代理                                     |         |
| Transparent | 这个合约实现了一个可以通过关联的ProxyAdmin实例升级的代理。                 | 透明代理人   |
| utils       | 基本合约，用于帮助编写可升级的契约，或将部署在代理后面的任何类型的契约。               | UUPS代理人 |
| Clones.sol  | EIP 1167是部署最小代理合约(也称为“克隆”)的标准。                     |         |
| Proxy.sol   | 这个合约提供了一个回调函数，该函数使用EVM指令delegatecall将所有调用委托给另一个契约。 |         |

> 📌beacon

- IBeacon.sol

  \[描述] beacon接口
  ```c
  FUNCTIONS:
  //返回能被delegatecall调用的合约地址
  function implementation() external view returns (address)

  ```
- BeaconProxy.sol

  \[描述] 此合约实现了一个代理，该代理从{UpgradeableBeacon}获取每个调用的实现地址。

  \[是否支持] 支持
  ```git
  pragma solidity ^0.8.20;

  import {BeaconProxy} from "../../../openzeppelin-contracts/contracts/proxy/beacon/BeaconProxy.sol";
  import {IBeacon} from "../../../openzeppelin-contracts/contracts/proxy/beacon/IBeacon.sol";

  contract TestContract {
      function test() public returns(uint256) {
          return 100;
      }
  }

  contract Beacon is IBeacon{
      address public add;
      constructor() {
          add = address(new TestContract());
      }
      function implementation() external view returns (address) {
          return add;
      }
  }

  contract MyBeaconProxy is BeaconProxy {

      constructor(address implementation_, bytes memory data) BeaconProxy(implementation_, data) {

      }

      function Implementation() public returns(address) {
          return _implementation();
      }

      function GetBeacon() public returns(address) {
          return _getBeacon();
      }
      
  }
  ```
- UpgradeableBeacon.sol

  \[描述] 这个合约与一个或多个{BeaconProxy}实例一起使用，以确定它们的实现合约，即它们将委托所有的函数调用。

  \[是否支持] 支持

  \[错误描述]
  ```git
  ERRORS:
  847ac564: BeaconInvalidImplementation(address)

  EVENTS:
  bc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b: Upgraded(address)

  ```
  ```纯文本
  pragma solidity ^0.8.20;

  import {UpgradeableBeacon} from "../../../openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol";

  contract TestContractA {
  }

  contract TestContractB {
  }

  contract MyUpgradeableBeacon is UpgradeableBeacon {
      //构造函数构建使用TestContractA合约地址；upgradeTo使用TestContractB合约地址
      //TestContractA.address
      constructor(address implementation_, address initialOwner) UpgradeableBeacon(implementation_, initialOwner) {

      }

      //implementation

      //TestContractB.address
      //upgradeTo
      
  }

  ```

> 📌ERC1967

- ERC1967Utils.sol

  \[描述] 这个抽象合约提供了合约delegateCall相关接口

  \[是否支持] 支持

  \[错误描述]
  ```git
  ERRORS:
  62e77ba2: ERC1967InvalidAdmin(address)
  64ced0ec: ERC1967InvalidBeacon(address)
  4c9c8ce3: ERC1967InvalidImplementation(address)
  b398979f: ERC1967NonPayable()

  EVENTS:
  7e644d79422f17c01e4894b5f4f588d331ebfa28653d42ae832dc59e38c9798f: AdminChanged(address,address)
  1cf3b03a6cf19fa2baba4df148e9dcabedea7f8a5c07840e207e5c089be95d3e: BeaconUpgraded(address)
  bc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b: Upgraded(address)

  ```
  ```纯文本
  pragma solidity ^0.8.20;

  import {ERC1967Utils} from "../../../openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol";
  import {IBeacon} from "../../../openzeppelin-contracts/contracts/proxy/beacon/IBeacon.sol";

  contract TestContractA {
      uint256 val;
      function test() public {
          val = 1;
      }
  }

  contract TestContractB {
      uint256 val;
      function test() public {
          val = 100;
      }
  }

  contract TestContractC {    
      uint256 val;
      function test() public {
          val = 1000;
      }
  }

  contract TestContractBeacon is IBeacon{
      address add;
      constructor(address ad) {
          add = ad;
      }
      function implementation() external view returns (address) {
          return add;
      }
  }

  contract MyERC1967Utils {
      TestContractA public addA;
      TestContractB public addB;
      TestContractC public addC;
      TestContractBeacon public addBeacon;
      constructor() {
          addA = new TestContractA();
          addB = new TestContractB();
          addC = new TestContractC();
          addBeacon = new TestContractBeacon(address(addC));
      }
      
      function getImplementation() public returns(address) {
          return ERC1967Utils.getImplementation();
      }

      function upgradeToAndCallA() public {
          bytes memory data = abi.encodeWithSelector(TestContractA.test.selector);
          ERC1967Utils.upgradeToAndCall(address(addA), data);
      }

      function upgradeToAndCallB() public {
          bytes memory data = abi.encodeWithSelector(TestContractB.test.selector);
          ERC1967Utils.upgradeToAndCall(address(addB), data);
      }

      function changeAdmin() public {
          address admin = did:bid:efJYtoZeKfqw81nC9mXevpGMxPcehsWC;
          ERC1967Utils.changeAdmin(admin);
      }

      function getAdmin() public returns(address) {
          return ERC1967Utils.getAdmin();
      }

      function upgradeBeaconToAndCall() public {
          bytes memory data = abi.encodeWithSelector(TestContractC.test.selector);
          ERC1967Utils.upgradeBeaconToAndCall(address(addBeacon), data);
      }

      function getBeacon() public returns(address) {
          return ERC1967Utils.getBeacon();
      }
  }

  ```
- ERC1967Proxy.sol

  \[描述] 这个合约实现了一个可升级的代理

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {ERC1967Proxy} from "../../../openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Proxy.sol";

  contract TestContractA {
      uint256 val;
      function test() public {
          val = 1;
      }
  }

  contract MyERC1967Proxy {
      TestContractA public addA;
      ERC1967Proxy public proxy;
      constructor() {
          addA = new TestContractA();
      }
      //调用buildProxy后，即可根据返回地址调用TestContractA合约
      function buildProxy() public returns(address) {
          bytes memory data = abi.encodeWithSelector(TestContractA.test.selector);

          ERC1967Proxy proxy = new ERC1967Proxy(address(addA), data);
          return address(proxy);
      }
  }
  ```

> 📌Transparent

- ProxyAdmin.sol

  \[描述] 这是一个辅助契约，被指定为一个transparentupgradeableproxy的管理员。

  \[是否支持] 支持
- TransparentUpgradeableProxy.sol

  \[描述] 该合约实现了一个可通过关联的ProxyAdmin实例升级的代理。

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {TransparentUpgradeableProxy} from "../../../openzeppelin-contracts/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";

  contract TestContract {
      function testA(bool ret) public returns(bool) {
          return ret;
      }

      function testB() public returns(uint256) {
          return 122;
      }
  }

  contract MyTransparentUpgradeableProxy is TransparentUpgradeableProxy{
      //构建合约执行testB接口；构建完成后，调用testA接口
      constructor(address _logic, address initialOwner, bytes memory _data) TransparentUpgradeableProxy(_logic, initialOwner, _data) {

      }

      function proxyAdmin() public returns(address) {
          return _proxyAdmin();
      }
      
  }
  ```

> 📌utils

- Initializable.sol

  \[描述] 这是一个基本合约，用于帮助编写可升级的契约，或将部署在代理后面的任何类型的合约。

  \[是否支持] 支持

  \[错误描述]
  ```git
  Errors:
  f92ee8a9: InvalidInitialization()
  d7e6bcf8: NotInitializing()

  Events:
  c7f505b2f371ae2175ee4913f4499e1f2633a7b5936321eed1cdaeb6115181d2: Initialized(uint64)

  ```
  ```纯文本
  pragma solidity ^0.8.20;

  import {Initializable} from "../../../openzeppelin-contracts/contracts/proxy/utils/Initializable.sol";

  contract MyInitializable is Initializable{
      bool public initFlag;
      uint64 public version;
      //第一次调用成功，第二次调用revert:f92ee8a9
      function init() public initializer() {
          initFlag = true;
          version = 0;
      }

      //只有在init/update中能调用，直接调用updateVersion revert:d7e6bcf8
      function updateVersion(uint64 ver) public onlyInitializing() {
          version = ver;
      }

      function update(uint64 ver) public reinitializer(ver) {
          updateVersion(ver);
      }

      function GetVersion() public returns(uint64) {
          return _getInitializedVersion();
      }

      function isInitializing() public returns(bool) {
          return _isInitializing();
      }

      //调用该方法后，update无法再次调用
      function disableInitializers() public {
          _disableInitializers();
      }
  }

  ```
- UUPSUpgradeable.sol

  \[描述] 为UUPS代理设计的可升级机制。

  \[是否支持] 支持

  \[错误描述]
  ```git
  ERRORS:
  9996b315: AddressEmptyCode(address)
  4c9c8ce3: ERC1967InvalidImplementation(address)
  b398979f: ERC1967NonPayable()
  1425ea42: FailedInnerCall()
  e07c8dba: UUPSUnauthorizedCallContext()
  aa1d49a4: UUPSUnsupportedProxiableUUID(bytes32)

  Events:
  bc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b: Upgraded(address)

  ```
  ```git
  pragma solidity ^0.8.20;

  import {UUPSUpgradeable} from "../../../openzeppelin-contracts/contracts/proxy/utils/UUPSUpgradeable.sol";
  import {ERC1967Utils} from "../../../openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol";
  import {Proxy} from "../../../openzeppelin-contracts/contracts/proxy/Proxy.sol";

  contract MyUUPSUpgradeableA is UUPSUpgradeable {

      function _authorizeUpgrade(address newImplementation) internal override {
          //关于合约升级权限的一些控制，比如升级调用者为指定合约地址
      }

      function testA() public returns(bool) {
          return true;
      }
  }

  contract MyUUPSUpgradeableB is UUPSUpgradeable {

      function _authorizeUpgrade(address newImplementation) internal override {
          //关于合约升级权限的一些控制，比如升级调用者为指定合约地址
      }

      function testB() public returns(bool) {
          return false;
      }
  }

  //部署时MyUUPSUpgradeableA为逻辑合约；后续升级过程中，通过调用MyProxy.upgradeToAndCall会根据fallback逻辑，调用到MyUUPSUpgradeableA.upgradeToAndCall将逻辑合约更新为MyUUPSUpgradeableB
  contract MyProxy is Proxy {
      address public add;
      constructor() {
          add = address(new MyUUPSUpgradeableA());
          bytes memory data = abi.encodeWithSelector(MyUUPSUpgradeableA.testA.selector);
          ERC1967Utils.upgradeToAndCall(add, data);
      }
      
      function _implementation() internal view override returns (address) {
          return add;
      }

      //upgradeToAndCall
  }
  ```
- Clones.sol

  \[描述] 这个合约提供了一个回调函数，该函数使用EVM指令delegatecall将所有调用委托给另一个契约

  \[是否支持] 支持

  \[修改点]
  ```git
  --- a/contracts/proxy/Clones.sol
  +++ b/contracts/proxy/Clones.sol
  @@ -28,12 +28,11 @@ library Clones {
       function clone(address implementation) internal returns (address instance) {
           /// @solidity memory-safe-assembly
           assembly {
  -            // Cleans the upper 96 bits of the `implementation` word, then packs the first 3 bytes
  -            // of the `implementation` address with the bytecode before the address.
  -            mstore(0x00, or(shr(0xe8, shl(0x60, implementation)), 0x3d602d80600a3d3981f3363d3d373d3d3d363d73000000))
  -            // Packs the remaining 17 bytes of `implementation` with the bytecode after the address.
  -            mstore(0x20, or(shl(0x78, implementation), 0x5af43d82803e903d91602b57fd5bf3))
  -            instance := create(0, 0x09, 0x37)
  +            let ptr := mload(0x40)
  +            mstore(ptr, 0x3d602d80600a3d3981f3363d3d373d3d3d363d77000000000000000000000000)
  +            mstore(add(ptr, 0x14), shl(0x40, implementation))
  +            mstore(add(ptr, 0x2c), 0x5af43d82803e903d91602f57fd5bf30000000000000000000000000000000000)
  +            instance := create(0, ptr, 0x3b)
           }
           if (instance == address(0)) {
               revert ERC1167FailedCreateClone();
  @@ -50,12 +49,11 @@ library Clones {
       function cloneDeterministic(address implementation, bytes32 salt) internal returns (address instance) {
           /// @solidity memory-safe-assembly
           assembly {
  -            // Cleans the upper 96 bits of the `implementation` word, then packs the first 3 bytes
  -            // of the `implementation` address with the bytecode before the address.
  -            mstore(0x00, or(shr(0xe8, shl(0x60, implementation)), 0x3d602d80600a3d3981f3363d3d373d3d3d363d73000000))
  -            // Packs the remaining 17 bytes of `implementation` with the bytecode after the address.
  -            mstore(0x20, or(shl(0x78, implementation), 0x5af43d82803e903d91602b57fd5bf3))
  -            instance := create2(0, 0x09, 0x37, salt)
  +            let ptr := mload(0x40)
  +            mstore(ptr, 0x3d603180600a3d3981f3363d3d373d3d3d363d77000000000000000000000000)
  +            mstore(add(ptr, 0x14), shl(0x40, implementation))
  +            mstore(add(ptr, 0x2c), 0x5af43d82803e903d91602f57fd5bf30000000000000000000000000000000000)
  +            instance := create2(0, ptr, 0x3b, salt)
           }
           if (instance == address(0)) {
               revert ERC1167FailedCreateClone();
  @@ -73,13 +71,13 @@ library Clones {
           /// @solidity memory-safe-assembly
           assembly {
               let ptr := mload(0x40)
  -            mstore(add(ptr, 0x38), deployer)
  -            mstore(add(ptr, 0x24), 0x5af43d82803e903d91602b57fd5bf3ff)
  -            mstore(add(ptr, 0x14), implementation)
  -            mstore(ptr, 0x3d602d80600a3d3981f3363d3d373d3d3d363d73)
  -            mstore(add(ptr, 0x58), salt)
  -            mstore(add(ptr, 0x78), keccak256(add(ptr, 0x0c), 0x37))
  -            predicted := keccak256(add(ptr, 0x43), 0x55)
  +            mstore(ptr, 0x3d603180600a3d3981f3363d3d373d3d3d363d77000000000000000000000000) 
  +            mstore(add(ptr, 0x14), shl(0x40, implementation))
  +            mstore(add(ptr, 0x2c), 0x5af43d82803e903d91602f57fd5bf3ff00000000000000000000000000000000) 
  +            mstore(add(ptr, 0x3c), shl(0x40, deployer)) 
  +            mstore(add(ptr, 0x54), salt)
  +            mstore(add(ptr, 0x74), keccak256(ptr, 0x3b)) 
  +            predicted := or(and(keccak256(add(ptr, 0x3b), 0x59), 0x00000000000000000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF), 0x0000000000000000656600000000000000000000000000000000000000000000)
           }
       }
  ```
  \[错误信息描述]
  ```git
  ERRORS:
  c2f868f4: ERC1167FailedCreateClone()
  ```
  ```纯文本
  pragma solidity ^0.8.20;

  import {Clones} from "../../openzeppelin-contracts/contracts/proxy/Clones.sol";

  contract TestContract {
      function testA(bool ret) public returns(bool) {
          return ret;
      }
  }

  contract MyClones {
      address public add;
      constructor() {
          add = address(new TestContract());
      }
      
      function clone() public returns(address) {
          return Clones.clone(address(add));
      }

      function cloneDeterministic() public returns(address) {
          bytes32 salt = 0x9700def5a0ee4e2cb712ce27fddcf0ba5e437006933f4de0c23e75afa497bcd9;
          return Clones.cloneDeterministic(address(add), salt);
      }

      //该接口生成地址与cloneDeterministic接口生成地址相同
      function predictDeterministicAddress() public returns(address) {
          bytes32 salt = 0x9700def5a0ee4e2cb712ce27fddcf0ba5e437006933f4de0c23e75afa497bcd9;
          return Clones.predictDeterministicAddress(address(add), salt);
      }

  }

  ```
- Proxy.sol

  \[描述] EIP 1167是部署最小代理合约(也称为“克隆”)的标准。

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {Proxy} from "../../openzeppelin-contracts/contracts/proxy/Proxy.sol";

  contract TestContract {
      function testA(bool ret) public returns(bool) {
          return ret;
      }
  }

  contract MyProxy is Proxy{
      //直接基于MyProxy合约地址调用合约TestContract.testA(ret);，该合约会调用fallback函数找到testA并进行delegateCall调用
      address public add;
      constructor() {
          add = address(new TestContract());
      }
      
      function _implementation() internal view override returns (address) {
          return add;
      }
  }

  ```
