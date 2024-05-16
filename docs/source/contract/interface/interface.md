# interface

| 简介   | 标准合约接口文件 |
| ---- | -------- |
| 是否支持 | yes      |
| 字段名  |          |

[ Interfaces - OpenZeppelin Docs  https://docs.openzeppelin.com/contracts/5.x/api/interfaces](https://docs.openzeppelin.com/contracts/5.x/api/interfaces " Interfaces - OpenZeppelin Docs  https://docs.openzeppelin.com/contracts/5.x/api/interfaces")

- draft-IERC1822.sol

  \[描述] 通用可升级代理标准(Universal Upgradeable Proxy Standard, UUPS)记录了一种通过简化代理实现可升级性的方法，该代理的升级完全由当前实现控制。
  ```c
  FUNCTIONS:
  //返回可代理合约假定用于存储实现地址的存储槽。
  function proxiableUUID() external view returns (bytes32)

  ```
- draft-IERC6093.sol

  \[描述] ERC20/721/1155错误码

  \[ERC20错误码]
  ```c
  fb8f41b2: ERC20InsufficientAllowance(address,uint256,uint256)
  e450d38c: ERC20InsufficientBalance(address,uint256,uint256)
  e602df05: ERC20InvalidApprover(address)
  ec442f05: ERC20InvalidReceiver(address)
  96c6fd1e: ERC20InvalidSender(address)
  94280d62: ERC20InvalidSpender(address)

  ```
  \[ERC721错误码]
  ```c
  64283d7b: ERC721IncorrectOwner(address,uint256,address)
  177e802f: ERC721InsufficientApproval(address,uint256)
  a9fbf51f: ERC721InvalidApprover(address)
  5b08ba18: ERC721InvalidOperator(address)
  89c62b64: ERC721InvalidOwner(address)
  64a0ae92: ERC721InvalidReceiver(address)
  73c6ac6e: ERC721InvalidSender(address)
  7e273289: ERC721NonexistentToken(uint256)

  ```
  \[ERC1155错误码]
  ```c
  03dee4c5: ERC1155InsufficientBalance(address,uint256,uint256,uint256)
  3e31884e: ERC1155InvalidApprover(address)
  5b059991: ERC1155InvalidArrayLength(uint256,uint256)
  ced3e100: ERC1155InvalidOperator(address)
  57f447ce: ERC1155InvalidReceiver(address)
  01a83514: ERC1155InvalidSender(address)
  e237d922: ERC1155MissingApprovalForAll(address,address)

  ```
- IERC3156FlashBorrower.sol

  \[描述] ERC3156 FlashBorrower 闪电贷接口
  ```c
  FUNCTIONS:
  //闪贷请求
  function onFlashLoan(
          address initiator,
          address token,
          uint256 amount,
          uint256 fee,
          bytes calldata data
      ) external returns (bytes32)

  ```
- IERC3156FlashLender.sol

  \[描述] ERC3156 FlashLender闪电贷接口
  ```c
  FUNCTIONS:
  //可供借贷的token数量
  function maxFlashLoan(address token) external view returns (uint256);
  //对某项贷款收取的费用
  function flashFee(address token, uint256 amount) external view returns (uint256);
  //初始化闪贷信息
  function flashLoan(
          IERC3156FlashBorrower receiver,
          address token,
          uint256 amount,
          bytes calldata data
      ) external returns (bool);

  ```
- IERC4626.sol

  \[描述] ERC4626“令牌化保险库标准”的接口
  ```c
  EVENTS:
  8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925: Approval(address,address,uint256)
  dcbc1c05240f31ff3ad067ef1ee35ce4997762752e3a095284754544f4c709d7: Deposit(address,address,uint256,uint256)
  ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef: Transfer(address,address,uint256)
  fbde797d201c681b91056529119e0b02407c7bb96a4a2c75c01fc9667232c8db: Withdraw(address,address,address,uint256,uint256)

  FUNCTIONS:
  //返回用于金库进行会计、存款和取款的基础token的地址
  function asset() external view returns (address assetTokenAddress);
  //返回金库“管理”的基础资产总额
  function totalAssets() external view returns (uint256 totalManagedAssets)
  //在所有条件都满足的理想情况下，返回金库将交换的资产数量的份额数量。
  function convertToShares(uint256 assets) external view returns (uint256 shares)
  //在所有条件都满足的理想情况下，返回金库将用提供的股份交换的资产金额。
  function convertToAssets(uint256 shares) external view returns (uint256 assets)
  //通过存款通知，返回可为接收者存入金库的基础资产的最大金额
  function maxDeposit(address receiver) external view returns (uint256 maxAssets)
  //允许链上或链下用户在当前链上条件下模拟其存款在当前区块的影响。
  function previewDeposit(uint256 assets) external view returns (uint256 shares)
  //Mints通过存入准确数量的标的代币来向接收者分享金库股份。
  function deposit(uint256 assets, address receiver) external returns (uint256 shares)
  //通过mint调用，返回可以为接收者铸造的金库份额的最大金额。
  function maxMint(address receiver) external view returns (uint256 maxShares)
  //允许链上或链下用户在当前链上条件下模拟其造币厂在当前区块的影响
  function previewMint(uint256 shares) external view returns (uint256 assets)
  //Mints通过存入一定量的基础代币，准确地将金库股份分享给接收者
  function mint(uint256 shares, address receiver) external returns (uint256 assets)
  //通过提现调用，返回可从金库所有者余额中提取的基础资产的最大金额
  function maxWithdraw(address owner) external view returns (uint256 maxAssets)
  //允许链上或链下用户在给定当前链上条件的情况下，模拟他们在当前区块的退出效果
  function previewWithdraw(uint256 assets) external view returns (uint256 shares)
  //从所有者那里烧毁股票，并将基础代币的确切资产发送给接收者。
  function withdraw(uint256 assets, address receiver, address owner) external returns (uint256 shares)
  //通过赎回通知，返回可从金库所有者余额中赎回的金库股份的最大数量。
  function maxRedeem(address owner) external view returns (uint256 maxShares)
  //允许链上或链下用户在给定当前链上条件的情况下，模拟其在当前区块的赎回效果。
  function previewRedeem(uint256 shares) external view returns (uint256 assets)
  //从所有者处准确地燃烧股份，并将基础代币资产发送给接收者
  function redeem(uint256 shares, address receiver, address owner) external returns (uint256 assets)

  ```
- IERC2309.sol

  \[描述] ERC721 "连续转移拓展"接口
  ```c
  EVENTS:
  //当从`fromTokenId`到`toTokenId`的token从`fromAddress`传输到`toAddress`时触发。
  event ConsecutiveTransfer(
          uint256 indexed fromTokenId,
          uint256 toTokenId,
          address indexed fromAddress,
          address indexed toAddress
      );

  ```
- IERC4906.sol

  \[描述] EIP-721元数据更新扩展
  ```c
  EVENTS：
  6bd5c950a8d8df17f772f5af37cb3655737899cbf903264b9795592da439661c: BatchMetadataUpdate(uint256,uint256)
  f8e1a15aba9398e019f0b49df1a4fde98ee17ae345cb5f6b5e2c27f5033e8ce7: MetadataUpdate(uint256)

  ```
