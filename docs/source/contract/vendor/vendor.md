# vendor

| 简介   | time lock 接口 |
| ---- | ------------ |
| 是否支持 | yes          |
| 字段名  |              |

- vendor/compound/ICompoundTimelock.sol

  \[描述] ICompoundTimelock接口描述，**该接口不存在实现及调用**
  ```c
  event NewAdmin(address indexed newAdmin);
      event NewPendingAdmin(address indexed newPendingAdmin);
      event NewDelay(uint256 indexed newDelay);
      event CancelTransaction(
          bytes32 indexed txHash,
          address indexed target,
          uint256 value,
          string signature,
          bytes data,
          uint256 eta
      );
      event ExecuteTransaction(
          bytes32 indexed txHash,
          address indexed target,
          uint256 value,
          string signature,
          bytes data,
          uint256 eta
      );
      event QueueTransaction(
          bytes32 indexed txHash,
          address indexed target,
          uint256 value,
          string signature,
          bytes data,
          uint256 eta
      );

      receive() external payable;

      // solhint-disable-next-line func-name-mixedcase
      function GRACE_PERIOD() external view returns (uint256);

      // solhint-disable-next-line func-name-mixedcase
      function MINIMUM_DELAY() external view returns (uint256);

      // solhint-disable-next-line func-name-mixedcase
      function MAXIMUM_DELAY() external view returns (uint256);

      function admin() external view returns (address);

      function pendingAdmin() external view returns (address);

      function delay() external view returns (uint256);

      function queuedTransactions(bytes32) external view returns (bool);

      function setDelay(uint256) external;

      function acceptAdmin() external;

      function setPendingAdmin(address) external;

      function queueTransaction(
          address target,
          uint256 value,
          string memory signature,
          bytes memory data,
          uint256 eta
      ) external returns (bytes32);

      function cancelTransaction(
          address target,
          uint256 value,
          string memory signature,
          bytes memory data,
          uint256 eta
      ) external;

      function executeTransaction(
          address target,
          uint256 value,
          string memory signature,
          bytes memory data,
          uint256 eta
      ) external payable returns (bytes memory);

  ```
