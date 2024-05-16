# finance

| 简介   | 财务类库 |
| ---- | ---- |
| 是否支持 | no   |
| 字段名  |      |

该目录包含金融系统原语。

详细描述文档：

[ Finance - OpenZeppelin Docs  https://docs.openzeppelin.com/contracts/5.x/api/finance](https://docs.openzeppelin.com/contracts/5.x/api/finance " Finance - OpenZeppelin Docs  https://docs.openzeppelin.com/contracts/5.x/api/finance")

| 目录 & 文件           | 功能     | 详细信息 |
| ----------------- | ------ | ---- |
| VestingWallet.sol | 金融系统原语 |      |

- VestingWallet.sol

  \[描述] 接收本地货币和ERC20代币，并根据归属时间表将这些资产释放给钱包所有者

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {VestingWallet} from "../../openzeppelin-contracts/contracts/finance/VestingWallet.sol";

  contract MyVestingWallet is VestingWallet{
      constructor(address beneficiary, uint64 startTimestamp, uint64 durationSeconds) VestingWallet(beneficiary, startTimestamp, durationSeconds) {
      }

      function Start() public view returns (uint256) {
          return start();
      }

      function Duration() public view returns (uint256) {
          return duration();
      }

      function End() public view returns (uint256) {
          return end();
      }

      function Released() public view returns (uint256) {
          return released();
      }

      function Released(address token) public view returns (uint256) {
          return released(token);
      }

      function Releasable() public view returns (uint256) {
          return releasable();
      }

      function Releasable(address token) public view returns (uint256) {
          return releasable(token);
      }

      function Release() public{
          return release();
      }

      function Release(address token) public {
          return release(token);
      }

      function VestedAmount(uint64 timestamp) public view returns (uint256) {
          return vestedAmount(timestamp);
      }
  }
  ```
