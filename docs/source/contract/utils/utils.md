# utils

| 简介   | 工具类库      |
| ---- | --------- |
| 是否支持 | yes(部分支持) |
| 字段名  |           |

OpenZeppelin Contracts提供了大量有用的实用工具，可以直接在项目中使用。

详细描述文档：

[Utilities - OpenZeppelin Docs  https://docs.openzeppelin.com/contracts/5.x/api/utils](https://docs.openzeppelin.com/contracts/5.x/api/utils "Utilities - OpenZeppelin Docs  https://docs.openzeppelin.com/contracts/5.x/api/utils")

| 目录 & 文件            | 功能                                             | 详细信息                                                     |
| ------------------ | ---------------------------------------------- | -------------------------------------------------------- |
| cryptography       | 数字签名和验证库函数                                     | EIP712 struct序列化签名,&#xA;ECDSA 椭圆曲线签名/验证, 默克尔树验证&#xA;合约签名 |
| introspection      | ERC165实现                                       | 展示合约接口                                                   |
| math               | 数学计算库                                          | 安全运算、类型转换                                                |
| structs            | 一些数据结构的实现                                      | BitMap、Queue、可枚举map/set等                                 |
| types              | 操作与时间相关的对象的帮助程序                                |                                                          |
| Address.sol        | 地址相关操作                                         |                                                          |
| Arrays.sol         | 数组相关操作                                         |                                                          |
| Base64.sol         | Base64相关操作                                     |                                                          |
| Context.sol        | 上下问相关操作                                        |                                                          |
| Create2.sol        | create2 指令相关操作                                 |                                                          |
| Muticall.sol       | 批量处理操作                                         |                                                          |
| Nonces.sol         | 追踪指定地址的nonce                                   |                                                          |
| Pausable.sol       | 可由授权账户触发合约停止                                   |                                                          |
| ReetrancyGuard.sol | 防止对函数的可重入调用                                    |                                                          |
| ShortStrings.sol   | 提供了将短内存字符串转换为' ShortString '类型的函数，该类型可以用作不可变变量 |                                                          |
| StorageSlot.sol    | 用于将基本类型读写到特定存储槽的库。                             |                                                          |
| Strings.sol        | 字符串相关操作                                        |                                                          |

> 📌cryptography

- ECDSA.sol【不支持】 (星火底层链不支持ECDSA，该合约作用为根据hash和签名恢复签名者地址，星火链未支持ecrecover预编译合约 )
- EIP712.sol【不支持】（EIP712相关内容，该分隔符用作编码方案的一部分，并在编码的最后一步获得消息摘要，然后通过ECDSA (\_hashTypedDataV4)对消息摘要进行签名，同ECDSA.sol）
- MerkleProof.sol

  \[描述] 处理默克尔树证明的验证；

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {MerkleProof} from "../../../openzeppelin-contracts/contracts/utils/cryptography/MerkleProof.sol";

  contract MyMerkProof {

      /*
          [
              0x0000000000000000000000000000000000000000000000000000000000000001,(left)
              0x0000000000000000000000000000000000000000000000000000000000000002 (right)
          ]
          0xe90b7bceb6e7df5418fb78d8ee546e97c83a08bbccc01a0644d599ccd2a7c2e0(root)
      */

      function verify() public returns(bool) {
          bytes32[] memory _proof = new bytes32[](1);
          _proof[0] = 0x0000000000000000000000000000000000000000000000000000000000000001;

          bytes32 root = 0xe90b7bceb6e7df5418fb78d8ee546e97c83a08bbccc01a0644d599ccd2a7c2e0;
          bytes32 leaf = 0x0000000000000000000000000000000000000000000000000000000000000002;

          return MerkleProof.verify(_proof, root, leaf);
      }
  }
  ```
- MessageHashUtils.sol【不支持】（用于生成供ECDSA恢复或签名使用的摘要的签名消息散列实用程序，同ECDSA.sol）
- SignatureChecker.sol【不支持】（可以代替ECDSA使用的签名验证帮助器，同ECDSA.sol）

> 📌introspection

ERC165标准的实现，即检测合约是否实现接口规范；

- IERC165.sol

  \[描述] 定义ERC165标准必须实现的接口（supportsInterface(bytes4)）
- ERC165.sol

  \[描述] ERC165标准的实现合约；
- ERC165Checker.sol

  \[描述] 根据ERC165规则检查某个合约是否实现了某些接口；

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {ERC165} from "../../../openzeppelin-contracts/contracts/utils/introspection/ERC165.sol";
  import {ERC165Checker} from "../../../openzeppelin-contracts/contracts/utils/introspection/ERC165Checker.sol";
  import {IERC165} from "../../../openzeppelin-contracts/contracts/utils/introspection/IERC165.sol";

  interface AA {
      function aa(bool) external view returns (bool);
      function bb(address) external view returns (bool);
  }

  interface BB {
      function cc(bytes32) external view returns (address);
      function dd(address) external view returns (uint256);
  }

  contract MyERC165 is ERC165, AA {

      function aa(bool) external view returns (bool) {
          return true;
      }

      function bb(address) external view returns (bool) {
          return true;
      }

      //检测当前合约是否实现了ERC165标准
      function supportsERC165() public returns(bool) {
          return ERC165Checker.supportsERC165(address(this));
      }

      function getSupportedInterfaces() public returns(bool[] memory) {
          bytes4[] memory interfaceIdsSupported = new bytes4[](3);
          interfaceIdsSupported[0] = type(AA).interfaceId;
          interfaceIdsSupported[1] = type(BB).interfaceId;
          interfaceIdsSupported[2] = type(IERC165).interfaceId;

          return ERC165Checker.getSupportedInterfaces(address(this), interfaceIdsSupported);
      }

      function supportsAllInterfaces() public returns(bool) {
          bytes4[] memory interfaceIdsSupported = new bytes4[](3);
          interfaceIdsSupported[0] = type(AA).interfaceId;
          interfaceIdsSupported[1] = type(BB).interfaceId;
          interfaceIdsSupported[2] = type(IERC165).interfaceId;

          return ERC165Checker.supportsAllInterfaces(address(this), interfaceIdsSupported);
      }
  }
  ```

> 📌math

- Math.sol

  \[描述] solidity标准数学函数

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {Math} from "../../../openzeppelin-contracts/contracts/utils/math/Math.sol";

  pragma solidity ^0.8.20;

  contract MyMath {
      function tryAdd(uint256 a, uint256 b) public returns(bool, uint256){
          return Math.tryAdd(a, b);
      }

      function trySub(uint256 a, uint256 b) public returns(bool, uint256){
          return Math.trySub(a, b);
      }

      function tryMul(uint256 a, uint256 b) public returns(bool, uint256){
          return Math.tryMul(a, b);
      }

      function tryDiv(uint256 a, uint256 b) public returns(bool, uint256){
          return Math.tryDiv(a, b);
      }

      function tryMod(uint256 a, uint256 b) public returns(bool, uint256){
          return Math.tryMod(a, b);
      }

      function max(uint256 a, uint256 b) public returns(uint256){
          return Math.max(a, b);
      }

      function min(uint256 a, uint256 b) public returns(uint256){
          return Math.min(a, b);
      }

      function average(uint256 a, uint256 b) public returns(uint256){
          return Math.average(a, b);
      }

      function ceilDiv(uint256 a, uint256 b) public returns(uint256){
          return Math.ceilDiv(a, b);
      }
      // a * b / denominator
      function mulDiv(uint256 a, uint256 b, uint256 denominator) public returns(uint256){
          return Math.mulDiv(a, b, denominator);
      }

      function mulDiv(uint256 a, uint256 b, uint256 denominator, uint8 r) public returns(uint256){
          return Math.mulDiv(a, b, denominator, Math.Rounding(r));
      }

      function sqrt(uint256 a) public returns(uint256){
          return Math.sqrt(a);
      }

      function sqrt(uint256 a, uint8 r) public returns(uint256){
          return Math.sqrt(a);
      }

      function log2(uint256 a) public returns(uint256){
          return Math.log2(a);
      }

      function log2(uint256 a, uint8 r) public returns(uint256){
          return Math.log2(a);
      }

      function log10(uint256 a) public returns(uint256){
          return Math.log10(a);
      }

      function log10(uint256 a, uint8 r) public returns(uint256){
          return Math.log10(a);
      }

      function log256(uint256 a) public returns(uint256){
          return Math.log256(a);
      }

      function log256(uint256 a, uint8 r) public returns(uint256){
          return Math.log256(a);
      }

      function unsignedRoundsUp(uint8 r) public returns(bool){
          return Math.unsignedRoundsUp(Math.Rounding(r));
      }
  }

  ```

> 📌structs

- BitMaps.sol

  \[描述] solidity bit map实现

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {BitMaps} from "../../../openzeppelin-contracts/contracts/utils/structs/BitMaps.sol";

  contract MyBitMaps {
      BitMaps.BitMap bmap;
      
      function setTo(uint256 index, bool value) public {
          BitMaps.setTo(bmap, index, value);
      }

      function get(uint256 index) public returns(bool) {
          return BitMaps.get(bmap, index);
      }
  }
  ```
- CheckPoints.sol

  \[描述] 检查在不同时间点上发生变化的值，然后通过块号查找过去的值

  \[修改点] 增加地址相关checkpoint结构
  ```git
  --- a/contracts/utils/structs/Checkpoints.sol
  +++ b/contracts/utils/structs/Checkpoints.sol
  @@ -600,4 +600,198 @@ library Checkpoints {
               result.slot := add(keccak256(0, 0x20), pos)
           }
       }
  +
  +    struct Trace192 {
  +        Checkpoint192[] _checkpoints;
  +    }
  +
  +    struct Checkpoint192 {
  +        uint64 _key;
  +        uint192 _value;
  +    }
  +
  +    /**
  +     * @dev Pushes a (`key`, `value`) pair into a Trace192 so that it is stored as the checkpoint.
  +     *
  +     * Returns previous value and new value.
  +     *
  +     * IMPORTANT: Never accept `key` as a user input, since an arbitrary `type(uint64).max` key set will disable the
  +     * library.
  +     */
  +    function push(Trace192 storage self, uint64 key, uint192 value) internal returns (uint192, uint192) {
  +        return _insert(self._checkpoints, key, value);
  +    }
  +
  +    /**
  +     * @dev Returns the value in the first (oldest) checkpoint with key greater or equal than the search key, or zero if
  +     * there is none.
  +     */
  +    function lowerLookup(Trace192 storage self, uint64 key) internal view returns (uint192) {
  +        uint256 len = self._checkpoints.length;
  +        uint256 pos = _lowerBinaryLookup(self._checkpoints, key, 0, len);
  +        return pos == len ? 0 : _unsafeAccess(self._checkpoints, pos)._value;
  +    }
  +
  +    /**
  +     * @dev Returns the value in the last (most recent) checkpoint with key lower or equal than the search key, or zero
  +     * if there is none.
  +     */
  +    function upperLookup(Trace192 storage self, uint64 key) internal view returns (uint192) {
  +        uint256 len = self._checkpoints.length;
  +        uint256 pos = _upperBinaryLookup(self._checkpoints, key, 0, len);
  +        return pos == 0 ? 0 : _unsafeAccess(self._checkpoints, pos - 1)._value;
  +    }
  +
  +    /**
  +     * @dev Returns the value in the last (most recent) checkpoint with key lower or equal than the search key, or zero
  +     * if there is none.
  +     *
  +     * NOTE: This is a variant of {upperLookup} that is optimised to find "recent" checkpoint (checkpoints with high
  +     * keys).
  +     */
  +    function upperLookupRecent(Trace192 storage self, uint64 key) internal view returns (uint192) {
  +        uint256 len = self._checkpoints.length;
  +
  +        uint256 low = 0;
  +        uint256 high = len;
  +
  +        if (len > 5) {
  +            uint256 mid = len - Math.sqrt(len);
  +            if (key < _unsafeAccess(self._checkpoints, mid)._key) {
  +                high = mid;
  +            } else {
  +                low = mid + 1;
  +            }
  +        }
  +
  +        uint256 pos = _upperBinaryLookup(self._checkpoints, key, low, high);
  +
  +        return pos == 0 ? 0 : _unsafeAccess(self._checkpoints, pos - 1)._value;
  +    }
  +
  +    /**
  +     * @dev Returns the value in the most recent checkpoint, or zero if there are no checkpoints.
  +     */
  +    function latest(Trace192 storage self) internal view returns (uint192) {
  +        uint256 pos = self._checkpoints.length;
  +        return pos == 0 ? 0 : _unsafeAccess(self._checkpoints, pos - 1)._value;
  +    }
  +
  +    /**
  +     * @dev Returns whether there is a checkpoint in the structure (i.e. it is not empty), and if so the key and value
  +     * in the most recent checkpoint.
  +     */
  +    function latestCheckpoint(Trace192 storage self) internal view returns (bool exists, uint64 _key, uint192 _value) {
  +        uint256 pos = self._checkpoints.length;
  +        if (pos == 0) {
  +            return (false, 0, 0);
  +        } else {
  +            Checkpoint192 memory ckpt = _unsafeAccess(self._checkpoints, pos - 1);
  +            return (true, ckpt._key, ckpt._value);
  +        }
  +    }
  +
  +    /**
  +     * @dev Returns the number of checkpoint.
  +     */
  +    function length(Trace192 storage self) internal view returns (uint256) {
  +        return self._checkpoints.length;
  +    }
  +
  +    /**
  +     * @dev Returns checkpoint at given position.
  +     */
  +    function at(Trace192 storage self, uint32 pos) internal view returns (Checkpoint192 memory) {
  +        return self._checkpoints[pos];
  +    }
  +
  +    /**
  +     * @dev Pushes a (`key`, `value`) pair into an ordered list of checkpoints, either by inserting a new checkpoint,
  +     * or by updating the last one.
  +     */
  +    function _insert(Checkpoint192[] storage self, uint64 key, uint192 value) private returns (uint192, uint192) {
  +        uint256 pos = self.length;
  +
  +        if (pos > 0) {
  +            // Copying to memory is important here.
  +            Checkpoint192 memory last = _unsafeAccess(self, pos - 1);
  +
  +            // Checkpoint keys must be non-decreasing.
  +            if (last._key > key) {
  +                revert CheckpointUnorderedInsertion();
  +            }
  +
  +            // Update or push new checkpoint
  +            if (last._key == key) {
  +                _unsafeAccess(self, pos - 1)._value = value;
  +            } else {
  +                self.push(Checkpoint192({_key: key, _value: value}));
  +            }
  +            return (last._value, value);
  +        } else {
  +            self.push(Checkpoint192({_key: key, _value: value}));
  +            return (0, value);
  +        }
  +    }
  +
  +    /**
  +     * @dev Return the index of the last (most recent) checkpoint with key lower or equal than the search key, or `high`
  +     * if there is none. `low` and `high` define a section where to do the search, with inclusive `low` and exclusive
  +     * `high`.
  +     *
  +     * WARNING: `high` should not be greater than the array's length.
  +     */
  +    function _upperBinaryLookup(
  +        Checkpoint192[] storage self,
  +        uint64 key,
  +        uint256 low,
  +        uint256 high
  +    ) private view returns (uint256) {
  +        while (low < high) {
  +            uint256 mid = Math.average(low, high);
  +            if (_unsafeAccess(self, mid)._key > key) {
  +                high = mid;
  +            } else {
  +                low = mid + 1;
  +            }
  +        }
  +        return high;
  +    }
  +
  +    /**
  +     * @dev Return the index of the first (oldest) checkpoint with key is greater or equal than the search key, or
  +     * `high` if there is none. `low` and `high` define a section where to do the search, with inclusive `low` and
  +     * exclusive `high`.
  +     *
  +     * WARNING: `high` should not be greater than the array's length.
  +     */
  +    function _lowerBinaryLookup(
  +        Checkpoint192[] storage self,
  +        uint64 key,
  +        uint256 low,
  +        uint256 high
  +    ) private view returns (uint256) {
  +        while (low < high) {
  +            uint256 mid = Math.average(low, high);
  +            if (_unsafeAccess(self, mid)._key < key) {
  +                low = mid + 1;
  +            } else {
  +                high = mid;
  +            }
  +        }
  +        return high;
  +    }
  +
  +    /**
  +     * @dev Access an element of the array without performing bounds check. The position is assumed to be within bounds.
  +     */
  +    function _unsafeAccess(
  +        Checkpoint192[] storage self,
  +        uint256 pos
  +    ) private pure returns (Checkpoint192 storage result) {
  +        assembly {
  +            mstore(0, self.slot)
  +            result.slot := add(keccak256(0, 0x20), pos)
  +        }
  +    }
   }
  ```
  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {Checkpoints} from "../../../openzeppelin-contracts/contracts/utils/structs/Checkpoints.sol";

  contract MyCheckpoints {

      Checkpoints.Trace224 trace;

      function push(uint32 key, uint224 value) public returns(uint224, uint224) {
          return Checkpoints.push(trace, key, value);
      }

      function lowerLookup(uint32 key) public returns(uint224) {
          return Checkpoints.lowerLookup(trace, key);
      }

      function upperLookup(uint32 key) public returns(uint224) {
          return Checkpoints.upperLookup(trace, key);
      }

      function upperLookupRecent(uint32 key) public returns(uint224) {
          return Checkpoints.upperLookupRecent(trace, key);
      }

      function latest(uint32 key) public returns(uint224) {
          return Checkpoints.latest(trace);
      }

      function latestCheckpoint() public returns(bool, uint32, uint224) {
          return Checkpoints.latestCheckpoint(trace);
      }

      function length() public returns(uint256) {
          return Checkpoints.length(trace);
      }
      
      function at(uint32 pos) public returns(uint32, uint224) {
          return (Checkpoints.at(trace, pos)._key, Checkpoints.at(trace, pos)._value);
      }
  }

  ```
- DoubleEndedQueue.sol

  \[描述] solidity中双端队列的实现

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {DoubleEndedQueue} from "../../../openzeppelin-contracts/contracts/utils/structs/DoubleEndedQueue.sol";

  contract MyDoubleEndedQueue {
      DoubleEndedQueue.Bytes32Deque deque;

      function pushBack(bytes32 value) public {
          DoubleEndedQueue.pushBack(deque, value);
      }

      function back() public returns(bytes32) {
          return DoubleEndedQueue.back(deque);
      }

      function popBack() public returns(bytes32) {
          return DoubleEndedQueue.popBack(deque);
      }

      function pushFront(bytes32 value) public {
          DoubleEndedQueue.pushFront(deque, value);
      }

      function front() public returns(bytes32) {
          return DoubleEndedQueue.front(deque);
      }

      function at(uint256 index) public returns(bytes32) {
          return DoubleEndedQueue.at(deque, index);
      }

      function popFront() public returns(bytes32) {
          return DoubleEndedQueue.popFront(deque);
      }

      function length() public returns(uint256) {
          return DoubleEndedQueue.length(deque);
      }

      function clear() public {
          return DoubleEndedQueue.clear(deque);
      }

      function empty() public returns(bool){
          return DoubleEndedQueue.empty(deque);
      }
      
  }

  ```
- EnumerableMap.sol

  \[描述] solidity中map的实现

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {EnumerableMap} from "../../../openzeppelin-contracts/contracts/utils/structs/EnumerableMap.sol";

  contract MyEnumerableMap {
      EnumerableMap.UintToAddressMap map;

      function set(uint256 key, address value) public returns(bool) {
          return EnumerableMap.set(map, key, value);
      }

      function remove(uint256 key) public returns(bool) {
          return EnumerableMap.remove(map, key);
      }

      function contains(uint256 key) public returns(bool) {
          return EnumerableMap.contains(map, key);
      }

      function length() public returns(uint256) {
          return EnumerableMap.length(map);
      }

      function at(uint256 index) public returns(uint256, address) {
          return EnumerableMap.at(map, index);
      }

      function tryGet(uint256 key) public returns(bool, address) {
          return EnumerableMap.tryGet(map, key);
      }

      function get(uint256 key) public returns(address) {
          return EnumerableMap.get(map, key);
      }

      function keys() public returns(uint256[] memory) {
          return EnumerableMap.keys(map);
      }
      
  }

  ```
- EnumerableSet.sol

  \[描述] solidity中map的实现

  \[是否支持] 支持
  ```纯文本

  pragma solidity ^0.8.20;

  import {EnumerableSet} from "../../../openzeppelin-contracts/contracts/utils/structs/EnumerableSet.sol";

  contract MyEnumerableSet {
      EnumerableSet.Bytes32Set set;

      function add(bytes32 value) public returns(bool) {
          return EnumerableSet.add(set, value);
      }

      function remove(bytes32 value) public returns(bool) {
          return EnumerableSet.remove(set, value);
      }

      function contains(bytes32 value) public returns(bool) {
          return EnumerableSet.contains(set, value);
      }

      function length() public returns(uint256) {
          return EnumerableSet.length(set);
      }

      function at(uint256 index) public returns(bytes32) {
          return EnumerableSet.at(set, index);
      }

      function values() public returns(bytes32[] memory) {
          return EnumerableSet.values(set);
      }
      
  }
  ```

> 📌types

- Time.sol

  \[描述] 提供用于操作与时间相关的对象的帮助程序

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {Time} from "../../../openzeppelin-contracts/contracts/utils/types/Time.sol";

  pragma solidity ^0.8.20;

  contract MyTime {
      function timestamp() public returns(uint48){
          return Time.timestamp();
      }

      function blockNumber() public returns(uint48) {
          return Time.blockNumber();
      }

      function toDelay() public returns(uint32, uint32, uint48) {
          Time.Delay de =  Time.toDelay(10);
          return Time.getFull(de);
      }

      function get() public returns(uint32) {
          Time.Delay de =  Time.toDelay(10);
          return Time.get(de);
      }

      function withUpdate() public returns(Time.Delay, uint48) {
          Time.Delay de =  Time.toDelay(10);
          uint32 newValue = 20;
          uint32 minSetback = 15;
          return Time.withUpdate(de, newValue, minSetback);
      }
  }
  ```
  \[修改点]  星火链返回timestamp长度为16位，星火链返回地址长度位10
  ```git
       function timestamp() internal view returns (uint48) {
  -        return SafeCast.toUint48(block.timestamp);
  +        return SafeCast.toUint48(block.timestamp / 1000000);
       }
  ```
- SafeCast.sol

  \[描述] 在solid的uintXX/intXX类型转换操作符上的包装器增加了溢出检查

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {SafeCast} from "../../../openzeppelin-contracts/contracts/utils/math/SafeCast.sol";


  contract MySafeCast {
      function toUint248(uint256 value) public returns(uint248) {
          return SafeCast.toUint248(value);
      }

      function toInt248(int256 value) public returns(int248) {
          return SafeCast.toInt248(value);
      }
  }
  ```
- SignedMath.sol

  \[描述] 在solid的intXX相关函数工具

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {SignedMath} from "../../../openzeppelin-contracts/contracts/utils/math/SignedMath.sol";


  contract MySignedMath {
      function max(int256 a, int256 b) public returns (int256) {
          return SignedMath.max(a, b);
      }

      function min(int256 a, int256 b) public returns (int256) {
          return SignedMath.min(a, b);
      }

      function average(int256 a, int256 b) public returns (int256) {
          return SignedMath.average(a, b);
      }

      function abs(int256 n) public returns (uint256) {
          return SignedMath.abs(n);
      }
  }
  ```

> 📌security

- ReentrancyGuard.sol

  \[描述] 防止对函数的可重入调用

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {ReentrancyGuard} from "../../openzeppelin-contracts/contracts/utils/ReentrancyGuard.sol";

  contract MyReentrancyGuard is ReentrancyGuard{
      function normalCall() public nonReentrant{

      }

      function abnormalCall() public nonReentrant{
          normalCall();
      }
  }
  ```
- Pausable.sol

  \[描述] 允许子合约实现可由授权帐户触发的紧急停止机制

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {Pausable} from "../../openzeppelin-contracts/contracts/utils/Pausable.sol";


  contract MyPausable is Pausable{

      function pause() public{
          _pause();
      }

      function unpause() public{
          _unpause();
      }

      function whennotpaused() public whenNotPaused returns(uint256){
          return 1;
      }

      function whenpaused() public whenPaused returns(uint256) {
          return 2;
      }
  }
  ```
- Nonces.sol

  \[描述] 跟踪给定地址的nonce值，nonce值只会递增；

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {Nonces} from "../../openzeppelin-contracts/contracts/utils/Nonces.sol";

  contract MyNonces is Nonces {
      function getNonce(address add) public returns(uint256){
          return nonces(add);
      }

      function useNonce(address add) public returns(uint256){
          return _useNonce(add);
      }

      function useCheckedNonce(address add, uint256 nonce) public {
          _useCheckedNonce(add, nonce);
      }
  }
  ```

> 📌libraries

- Address.sol

  \[描述] 地址类型相关功能的集合

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {Address} from "../../openzeppelin-contracts/contracts/utils/Address.sol";

  pragma solidity ^0.8.20;

  contract MyAddress {
      function test() public payable returns(string memory) {
          return "hello world"; 
      }

      function sendValue() public {
          Address.sendValue(payable(address(this)), 1);
      }

      function functionCall() public {
          bytes memory data = abi.encodeWithSelector(this.test.selector);
          Address.functionCall(payable(address(this)), data);
      }

      function functionCallWithValue() public {
          bytes memory data = abi.encodeWithSelector(this.test.selector);
          Address.functionCallWithValue(payable(address(this)), data, 1);
      }

      function functionStaticCall() public returns(bytes memory) {
          bytes memory data = abi.encodeWithSelector(this.test.selector);
          return Address.functionStaticCall(payable(address(this)), data);
      }

      function functionDelegateCall() public returns(bytes memory) {
          bytes memory data = abi.encodeWithSelector(this.test.selector);
          return Address.functionDelegateCall(payable(address(this)), data);
      }
  }
  ```
- Array.sol

  \[描述] 与数组类型相关的函数集合

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {Arrays} from "../../openzeppelin-contracts/contracts/utils/Arrays.sol";

  pragma solidity ^0.8.20;

  contract MyArrays {
      uint256[] uint256_array = [1,2,3,4,5];
      bytes32[] bytes32_array;
      address[] address_array = [did:bid:ef22ceNHdxTGMKfthBEjMaqHPj2TXT3VN, did:bid:ef22ceNHdxTGMKfthBEjMaqHPj2TXT3VN];

      constructor() {
          bytes32_array.push("0x1");
          bytes32_array.push("0x2");
          bytes32_array.push("0x3");
          bytes32_array.push("0x4");
      }

      //遍历地址数组到指定pos
      function unsafeMemoryAccess(address[] memory array, uint256 pos) public returns(address) {
          return Arrays.unsafeMemoryAccess(array, pos);
      }
      //遍历uint256数组到指定pos
      function unsafeMemoryAccess(uint256[] memory array, uint256 pos) public returns(uint256) {
          return Arrays.unsafeMemoryAccess(array, pos);
      }
      //遍历uint256数组到指定pos，返回元素
      function unsafeAccessuint256(uint256 pos) public returns(uint256) {
          return Arrays.unsafeAccess(uint256_array, pos).value;
      }
      //遍历bytes32数组到指定pos，返回元素
      function unsafeAccessbytes32(uint256 pos) public returns(bytes32) {
          return Arrays.unsafeAccess(bytes32_array, pos).value;
      }
      //遍历address数组到指定pos，返回元素
      function unsafeAccessaddress(uint256 pos) public returns(address) {
          return Arrays.unsafeAccess(address_array, pos).value;
      }

      function findUpperBound() public returns(uint256) {
          return Arrays.findUpperBound(uint256_array, 2);
      }
  }
  ```
- Base64.sol

  \[描述] 提供一组对Base64字符串进行操作的函数。

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {Base64} from "../../openzeppelin-contracts/contracts/utils/Base64.sol";

  pragma solidity ^0.8.20;

  contract MyBase64 {
      function encodetest() public returns(string memory) {
          bytes memory str = bytes("0x40c0d99bb87fb8fe451506144e7baf97ff1f7d4bb6ec");
          return Base64.encode(str);
      }
  }
  ```
- Context.sol

  \[描述] 提供有关当前执行上下文的信息，包括事务的发送方及其数据

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;  
    
  import {Context} from "../../openzeppelin-contracts/contracts/utils/Context.sol";

  pragma solidity ^0.8.20;

  contract MyContext is Context {

      function getMsgSender() public returns(address) {
          return _msgSender();
      }

      function getMsgData() public returns(bytes memory) {
          return _msgData();
      }

  }
  ```
- Create2.sol

  \[描述] 使CREATE2 EVM操作码的使用更容易和更安全。CREATE2可以用来提前计算智能合约将被部署的地址

  \[是否支持] 支持

  \[修改点]&#x20;
  ```git
  -            mstore(add(ptr, 0x40), bytecodeHash)
  -            mstore(add(ptr, 0x20), salt)
  -            mstore(ptr, deployer) // Right-aligned with 12 preceding garbage bytes
  -            let start := add(ptr, 0x0b) // The hashed data starts at the final garbage byte which we will set to 0xff
  +            //right160(sha3(bytes{0xff} +_sender.asBytes() + toBigEndian(_salt) + sha3(_init)));
  +
  +            let start := add(ptr, 0x07) // The hashed data starts at the final garbage byte which we will set to 0xff
  +            mstore(ptr, deployer) // Right-aligned with 12 preceding garbage bytes //24
               mstore8(start, 0xff)
  -            addr := keccak256(start, 85)
  +            mstore(add(ptr, 0x20), salt)            //32
  +            mstore(add(ptr, 0x40), bytecodeHash) //32
  +            addr := or(and(keccak256(start, 89), 0x00000000000000000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF), 0x0000000000000000656600000000000000000000000000000000000000000000)
  ```
  ```纯文本
  pragma solidity ^0.8.20;  
    
  import {Create2} from "../../openzeppelin-contracts/contracts/utils/Create2.sol";

  pragma solidity ^0.8.20;

  contract Test{
      function test() public returns(string memory) {
          return "hello world";
      }
  }
  contract MyCreate2 {  
      function deploytest() public returns(address){
          uint256 amount = 0;
          bytes32 salt = keccak256("123");
          bytes memory stringBytes = type(Test).creationCode;

          return Create2.deploy(amount, salt, stringBytes);
      }

      function computeAddresstest() public returns(address) {
          bytes32 salt = keccak256("123");
          bytes memory stringBytes = type(Test).creationCode;
          bytes32 bytecodeHash = keccak256(stringBytes); 
          return Create2.computeAddress(salt, bytecodeHash);
      }
  }
  ```
- Multicall.sol

  \[描述] 将多个调用批处理在单个外部调用中

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;  
    
  import {Multicall} from "../../openzeppelin-contracts/contracts/utils/Multicall.sol";  
    
  contract MyMuticall is Multicall {  
      uint256 public myNumber;  
    
      function setMyNumber(uint256 _number) external {  
          myNumber = _number;  
      }  
    
      function getMyNumber() external view returns (uint256) {  
          return myNumber;  
      }  
    
      function multicalltest() public returns(uint256, uint256){
          bytes[] memory bytesArray = new bytes[](3);
          bytesArray[0] = abi.encodeWithSelector(this.setMyNumber.selector, 100);
          bytesArray[1] = abi.encodeWithSelector(this.getMyNumber.selector);
          bytesArray[2] = abi.encodeWithSelector(this.getMyNumber.selector);
          bytes[] memory results = this.multicall(bytesArray);

          uint256 valueA = abi.decode(results[1], (uint256));  
          uint256 valueB = abi.decode(results[2], (uint256));

          return (valueA, valueB);
      }  
  }
  ```
- ShortStrings.sol

  \[描述] 将短内存字符串转换为可以用作不可变变量的ShortString类型的函数(string和bytes32数据之间的相互转换，如果超过32字节，则将数据写入存储)

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {ShortString} from "../../openzeppelin-contracts/contracts/utils/ShortStrings.sol";
  import {ShortStrings} from "../../openzeppelin-contracts/contracts/utils/ShortStrings.sol";


  contract MyShortStrings{
      string strstr;
      function toShortString(string memory str) public returns(ShortString) {
          return ShortStrings.toShortString(str);
      }

      function toString(ShortString str) public returns(string memory) {
          return ShortStrings.toString(str);
      }

      function byteLength(ShortString str) public returns(uint256) {
          return ShortStrings.byteLength(str);
      }

      function toShortStringWithFallback(string memory str) public returns(ShortString) {
          return ShortStrings.toShortStringWithFallback(str, strstr);
      }

      function toStringWithFallback(ShortString str) public returns(string memory) {
          return ShortStrings.toStringWithFallback(str, strstr);
      }

      function byteLengthWithFallback(ShortString str) public returns(uint256) {
          return ShortStrings.byteLengthWithFallback(str, strstr);
      }
  }


  ```
- StorageSlot.sol

  \[描述] 用于将基本类型读写到特定存储槽的库

  \[是否支持] 支持
  ```纯文本
  pragma solidity ^0.8.20;

  import {StorageSlot} from "../../openzeppelin-contracts/contracts/utils/StorageSlot.sol";

  contract MyStorageSlot{
      bytes32 internal constant _IMPLEMENTATION_SLOT = 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;
   
      //address
      function setAddressSlot(address newImplementation) public {
          StorageSlot.getAddressSlot(_IMPLEMENTATION_SLOT).value = newImplementation;
      }

      function getAddressSlot() public view returns (address) {
          return StorageSlot.getAddressSlot(_IMPLEMENTATION_SLOT).value;
      }
    
      //bool
      function setBooleanSlot(bool newImplementation) public {
          StorageSlot.getBooleanSlot(_IMPLEMENTATION_SLOT).value = newImplementation;
      }

      function getBooleanSlot() public view returns (bool) {
          return StorageSlot.getBooleanSlot(_IMPLEMENTATION_SLOT).value;
      }

      //bytes32
      function setBytes32Slot(bytes32 newImplementation) public {
          StorageSlot.getBytes32Slot(_IMPLEMENTATION_SLOT).value = newImplementation;
      }

      function getBytes32Slot() public view returns (bytes32) {
          return StorageSlot.getBytes32Slot(_IMPLEMENTATION_SLOT).value;
      }

      //uint256
      function setUint256Slot(uint256 newImplementation) public {
          StorageSlot.getUint256Slot(_IMPLEMENTATION_SLOT).value = newImplementation;
      }

      function getUint256Slot() public view returns (uint256) {
          return StorageSlot.getUint256Slot(_IMPLEMENTATION_SLOT).value;
      }

      //string
      function setStringSlot(string memory newImplementation) public {
          StorageSlot.getStringSlot(_IMPLEMENTATION_SLOT).value = newImplementation;
      }

      function getStringSlot() public view returns (string memory) {
          return StorageSlot.getStringSlot(_IMPLEMENTATION_SLOT).value;
      }

      //bytes
      function setBytesSlot(bytes memory newImplementation) public {
          StorageSlot.getBytesSlot(_IMPLEMENTATION_SLOT).value = newImplementation;
      }

      function getBytesSlot() public view returns (bytes memory) {
          return StorageSlot.getBytesSlot(_IMPLEMENTATION_SLOT).value;
      }
  }

  ```
- Strings.sol

  \[描述] uint256/int256→string  及 字符串比较相关函数

  \[是否支持] 支持

  \[修改点]&#x20;
  ```git
  + uint8 private constant ADDRESS_LENGTH = 24;
  - uint8 private constant ADDRESS_LENGTH = 20;
  function toHexString(address addr) internal pure returns (string memory) {
  +        return toHexString(uint256(uint192(addr)), ADDRESS_LENGTH);
  -        return toHexString(uint256(uint160(addr)), ADDRESS_LENGTH);
  }
  ```
  ```纯文本
  pragma solidity ^0.8.20;

  import {Strings} from "../../openzeppelin-contracts/contracts/utils/Strings.sol";

  contract MyStrings{
      /*
          call Strings.toString(uint256) ->string
      */
    function toString(uint256 value) public returns(string memory){
      return Strings.toString(value);
    }

      function toStringSigned(int256 value) public returns(string memory){
          return Strings.toStringSigned(value);
      }

      function toHexString(uint256 value) public returns(string memory){
          return Strings.toHexString(value);
      }

      function toHexString(uint256 value, uint256 length) public returns(string memory){
          return Strings.toHexString(value, length);
      }

      function toHexString(address add) public returns(string memory) {
          return Strings.toHexString(add);
      }

      function equal(string memory a, string memory b) public returns(bool) {
          return Strings.equal(a, b);
      }
  }

  ```

pragma solidity ^0.8.20;

import {Pausable} from "../../openzeppelin-contracts/contracts/utils/Pausable.sol";

contract MyPausable is Pausable{

function pause() public{

\_pause();

}

function unpause() public{

\_unpause();

}

function whennotpaused() public whenNotPaused returns(uint256){

return 1;

}

function whenpaused() public whenPaused returns(uint256) {

return 2;

}

}
