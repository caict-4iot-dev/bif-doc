# token

| 简介   | 各类token的标准实现，如ERC721、ERC1155 |
| ---- | ---------------------------- |
| 是否支持 | yes                          |
| 字段名  | ERC20删掉                      |

以太坊ERC20/721/1155标准的实现。

详细描述文档：

| 目录 & 文件 | 功能         | 文档链接                                                                                                                                                                                           |
| ------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| common  | 数字签名和验证库函数 | [https://docs.openzeppelin.com/contracts/5.x/api/token/common](https://docs.openzeppelin.com/contracts/5.x/api/token/common "https://docs.openzeppelin.com/contracts/5.x/api/token/common")    |
| ERC20   | 未适配        |                                                                                                                                                                                                |
| ERC721  | ERC721实现   | [https://docs.openzeppelin.com/contracts/5.x/api/token/erc721](https://docs.openzeppelin.com/contracts/5.x/api/token/erc721 "https://docs.openzeppelin.com/contracts/5.x/api/token/erc721")    |
| ERC1155 | ERC1155实现  | [https://docs.openzeppelin.com/contracts/5.x/api/token/erc1155](https://docs.openzeppelin.com/contracts/5.x/api/token/erc1155 "https://docs.openzeppelin.com/contracts/5.x/api/token/erc1155") |

> 📌common

- ERC2981.sol

  \[描述] 实施NFT特许权使用费标准，一种检索特许权使用费支付信息的标准化方式。

  \[是否支持] 支持

  \[错误描述]
  ```c
  ERRORS:
  6f483d09: ERC2981InvalidDefaultRoyalty(uint256,uint256)
  b6d9900a: ERC2981InvalidDefaultRoyaltyReceiver(address)
  dfd1fc1b: ERC2981InvalidTokenRoyalty(uint256,uint256,uint256)
  969f0852: ERC2981InvalidTokenRoyaltyReceiver(uint256,address)
  ```
  ```git
  pragma solidity ^0.8.20;

  import {ERC2981} from "../../../openzeppelin-contracts/contracts/token/common/ERC2981.sol";
  import {IERC2981} from "../../../openzeppelin-contracts/contracts/interfaces/IERC2981.sol";

  contract MyERC2981 is ERC2981{

      function SupportsInterface() public returns (bool) {
          return supportsInterface(type(IERC2981).interfaceId);
      }

      function FeeDenominator() public returns (uint96) {
          return _feeDenominator();
      }

      //设置默认值
      function SetDefaultRoyalty(address receiver, uint96 feeNumerator) public {
          _setDefaultRoyalty(receiver, feeNumerator);
      }
      //删除默认值
      function DeleteDefaultRoyalty() public {
          _deleteDefaultRoyalty();
      }

      function SetTokenRoyalty(uint256 tokenId, address receiver, uint96 feeNumerator) public {
          _setTokenRoyalty(tokenId, receiver, feeNumerator);
      }

      function ResetTokenRoyalty(uint256 tokenId) public {
          _resetTokenRoyalty(tokenId);
      }

  }
  ```

> 📌ERC721

- extensions/ERC721Burnable.sol

  \[描述] 拓展ERC721标准，被授权人可销毁指定token

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {ERC721Burnable} from "../../../../openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Burnable.sol";
  import {ERC721} from "../../../../openzeppelin-contracts/contracts/token/ERC721/ERC721.sol";

  contract MyERC721Burnable is ERC721Burnable {

      constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_) {

      }

      //ownerOf
      //approve
      //getApproved
      
      function mint(address to, uint256 tokenId) public {
          _mint(to, tokenId);
      }
      //burn
  }

  ```
- extensions/ERC721Consecutive.sol

  \[描述] 拓展ERC721标准，批量铸造

  \[是否支持] 支持

  \[修改点] 修改地址长度
  ```git
  --- a/contracts/token/ERC721/extensions/ERC721Consecutive.sol
  +++ b/contracts/token/ERC721/extensions/ERC721Consecutive.sol
  @@ -29,9 +29,9 @@ import {Checkpoints} from "../../../utils/structs/Checkpoints.sol";
    */
   abstract contract ERC721Consecutive is IERC2309, ERC721 {
       using BitMaps for BitMaps.BitMap;
  -    using Checkpoints for Checkpoints.Trace160;
  +    using Checkpoints for Checkpoints.Trace192;

  -    Checkpoints.Trace160 private _sequentialOwnership;
  +    Checkpoints.Trace192 private _sequentialOwnership;
       BitMaps.BitMap private _sequentialBurn;

       /**
  @@ -64,7 +64,7 @@ abstract contract ERC721Consecutive is IERC2309, ERC721 {
        * NOTE: Overriding the default value of 5000 will not cause on-chain issues, but may result in the asset not being
        * correctly supported by off-chain indexing services (including marketplaces).
        */
  -    function _maxBatchSize() internal view virtual returns (uint96) {
  +    function _maxBatchSize() internal view virtual returns (uint64) {
           return 5000;
       }

  @@ -76,13 +76,13 @@ abstract contract ERC721Consecutive is IERC2309, ERC721 {
           address owner = super._ownerOf(tokenId);

           // If token is owned by the core, or beyond consecutive range, return base value
  -        if (owner != address(0) || tokenId > type(uint96).max || tokenId < _firstConsecutiveId()) {
  +        if (owner != address(0) || tokenId > type(uint64).max || tokenId < _firstConsecutiveId()) {
               return owner;
           }

           // Otherwise, check the token was not burned, and fetch ownership from the anchors
  -        // Note: no need for safe cast, we know that tokenId <= type(uint96).max
  -        return _sequentialBurn.get(tokenId) ? address(0) : address(_sequentialOwnership.lowerLookup(uint96(tokenId)));
  +        // Note: no need for safe cast, we know that tokenId <= type(uint64).max
  +        return _sequentialBurn.get(tokenId) ? address(0) : address(_sequentialOwnership.lowerLookup(uint64(tokenId)));
       }

       /**
  @@ -101,8 +101,8 @@ abstract contract ERC721Consecutive is IERC2309, ERC721 {
        *
        * Emits a {IERC2309-ConsecutiveTransfer} event.
        */
  -    function _mintConsecutive(address to, uint96 batchSize) internal virtual returns (uint96) {
  -        uint96 next = _nextConsecutiveId();
  +    function _mintConsecutive(address to, uint64 batchSize) internal virtual returns (uint64) {
  +        uint64 next = _nextConsecutiveId();

           // minting a batch of size 0 is a no-op
           if (batchSize > 0) {
  @@ -119,8 +119,8 @@ abstract contract ERC721Consecutive is IERC2309, ERC721 {
               }

               // push an ownership checkpoint & emit event
  -            uint96 last = next + batchSize - 1;
  -            _sequentialOwnership.push(last, uint160(to));
  +            uint64 last = next + batchSize - 1;
  +            _sequentialOwnership.push(last, uint192(to));

               // The invariant required by this function is preserved because the new sequentialOwnership checkpoint
               // is attributing ownership of `batchSize` new tokens to account `to`.
  @@ -161,7 +161,7 @@ abstract contract ERC721Consecutive is IERC2309, ERC721 {
       /**
        * @dev Used to offset the first token id in {_nextConsecutiveId}
        */
  -    function _firstConsecutiveId() internal view virtual returns (uint96) {
  +    function _firstConsecutiveId() internal view virtual returns (uint64) {
           return 0;
       }

  @@ -169,8 +169,8 @@ abstract contract ERC721Consecutive is IERC2309, ERC721 {
        * @dev Returns the next tokenId to mint using {_mintConsecutive}. It will return {_firstConsecutiveId}
        * if no consecutive tokenId has been minted before.
        */
  -    function _nextConsecutiveId() private view returns (uint96) {
  -        (bool exists, uint96 latestId, ) = _sequentialOwnership.latestCheckpoint();
  +    function _nextConsecutiveId() private view returns (uint64) {
  +        (bool exists, uint64 latestId, ) = _sequentialOwnership.latestCheckpoint();
           return exists ? latestId + 1 : _firstConsecutiveId();
       }
   }
  ```
  \[错误描述]
  ```c
  ERRORS:
  8f58e570: ERC721ExceededMaxBatchMint(uint256,uint256)
  1d089165: ERC721ForbiddenBatchBurn()
  539f9062: ERC721ForbiddenBatchMint()
  ad895052: ERC721ForbiddenMint()


  ```
  ```git
  pragma solidity ^0.8.20;

  import {ERC721Consecutive} from "../../../../openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Consecutive.sol";
  import {ERC721} from "../../../../openzeppelin-contracts/contracts/token/ERC721/ERC721.sol";

  contract MyERC721Consecutive is ERC721Consecutive {

      constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_) {
          _mintConsecutive(msg.sender, 100);
      }

      function MaxBatchSize() public view virtual returns (uint64) {
          return _maxBatchSize();
      }

      //ownerof
  }
  ```
- extensions/ERC721Enumerable.sol

  \[描述] 拓展ERC721标准，该扩展增加了合约中所有tokenid的可枚举性以及每个帐户拥有的所有tokenid

  \[错误描述]
  ```git
  ERRORS:
  59171fc1: ERC721EnumerableForbiddenBatchMint()
  a57d13dc: ERC721OutOfBoundsIndex(address,uint256)

  ```
  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {ERC721Enumerable} from "../../../../openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
  import {ERC721} from "../../../../openzeppelin-contracts/contracts/token/ERC721/ERC721.sol";

  contract MyERC721Enumerable is ERC721Enumerable {

      constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_) {

      }

      //tokenOfOwnerByIndex
      //totalSupply
      //tokenByIndex
      //balanceOf
      //ownerOf

      function mint(address to, uint256 tokenId) public {
          _mint(to, tokenId);
      }
  }

  ```
- extensions/ERC721Pausable.sol

  \[描述] 拓展ERC721标准，可暂停代币转移，铸造和燃烧

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {ERC721Pausable} from "../../../../openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Pausable.sol";
  import {ERC721} from "../../../../openzeppelin-contracts/contracts/token/ERC721/ERC721.sol";

  contract MyERC721Pausable is ERC721Pausable {

      constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_) {

      }


      function mint(address to, uint256 tokenId) public {
          _mint(to, tokenId);
      }

      function Pause() public {
          _pause();
      }

      function Unpause() public {
          _unpause();
      }
  }

  ```
- extensions/ERC721Royalty.sol

  \[描述] 拓展ERC721标准，支持ERC2981标准

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {ERC721Royalty} from "../../../../openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Royalty.sol";
  import {ERC721} from "../../../../openzeppelin-contracts/contracts/token/ERC721/ERC721.sol";
  import {IERC2981} from "../../../../openzeppelin-contracts/contracts/interfaces/IERC2981.sol";

  contract MyERC721Royalty is ERC721Royalty {

      constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_) {

      }


      function SupportsInterface() public returns (bool) {
          return supportsInterface(type(IERC2981).interfaceId);
      }

      //其余接口同ERCERC2981相关接口
  }

  ```
- extensions/ERC721URIStorage.sol

  \[描述] 拓展ERC721标准，基于存储的token URI管理的ERC721 token。

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {ERC721URIStorage} from "../../../../openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
  import {ERC721} from "../../../../openzeppelin-contracts/contracts/token/ERC721/ERC721.sol";

  contract MyERC721URIStorage is ERC721URIStorage {

      constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_) {

      }

      //tokenURI

      function SetTokenURI(uint256 tokenId, string memory _tokenURI) public {
          _setTokenURI(tokenId, _tokenURI);
      }

      function mint(address to, uint256 tokenId) public {
          _mint(to, tokenId);
      }
  }

  ```
- extensions/ERC721Votes.sol

  \[描述] ERC721的扩展，以支持类似compound的投票和委托

  \[是否支持] 不支持，内部使用goverance模块vote逻辑。
- extensions/ERC721Wrapper.sol

  \[描述] 拓展ERC721标准，支持token包装

  \[错误描述]
  ```git
  ERRORS:
  c7d837c6: ERC721UnsupportedToken(address)
  ```
  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {ERC721Wrapper} from "../../../../openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Wrapper.sol";
  import {ERC721} from "../../../../openzeppelin-contracts/contracts/token/ERC721/ERC721.sol";
  import {IERC721} from "../../../../openzeppelin-contracts/contracts/token/ERC721/IERC721.sol";
  import {IERC721Receiver} from "../../../../openzeppelin-contracts/contracts/token/ERC721/IERC721Receiver.sol";

  contract MyERC721 is ERC721 {
      constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_) {

      }
      function mint(address to, uint256 tokenId) public {
          _mint(to, tokenId);
      }
      //setApprovalForAll depositFor 调用者msgsender为合约，切记
  }

  contract MyERC721Wrapper is ERC721Wrapper {

      constructor(address token, string memory name_, string memory symbol_) ERC721Wrapper(IERC721(token)) ERC721(name_, symbol_) {

      }

      //underlying

      //depositFor

      //withdrawTo

      function Recover(address account, uint256 tokenId) public returns (uint256) {
          return _recover(account, tokenId);
      }
  }
  ```
- extensions/IERC721Enumerable.sol

  \[描述] ERC721标准接口文件可选枚举拓展

  \[是否支持] 支持

  \[文件描述]
  ```c
  //返回合约中存储的所有token的数量
  function totalSupply() external view returns (uint256);
  //在token列表的给定“索引”处，返回一个由“owner”拥有的token ID。与{balanceOf}一起使用枚举所有“所有者”的令牌。
  function tokenOfOwnerByIndex(address owner, uint256 index) external view returns (uint256);
  //返回合约中存储的所有token的给定“索引”处的token ID。
  function tokenByIndex(uint256 index) external view returns (uint256);

  ```
- extensions/IERC721Metadata.sol

  \[描述] ERC721标准接口文件可选元数据

  \[是否支持] 支持

  \[文件描述]
  ```c
  //返回token 名称
  function name() external view returns (string memory)
  //返回token 符号
  function symbol() external view returns (string memory)
  //返回`tokenId` token的统一资源标识符(URI)。
  function tokenURI(uint256 tokenId) external view returns (string memory)

  ```
- utils/ERC721Holder.sol

  \[描述] IERC721Receiver标准接口实现合约

  \[是否支持] 支持
  ```git
  pragma solidity ^0.8.20;

  import {ERC721Holder} from "../../../../openzeppelin-contracts/contracts/token/ERC721/utils/ERC721Holder.sol";

  contract MyERC721Holder is ERC721Holder {
      //onERC721Received

      function OnERC721Received() public returns(bool) {
          return onERC721Received(address, address, uint256, bytes memory) == 0x150b7a02;
      }
  }
  ```
- IERC721.sol

  \[描述] ERC721标准接口文件

  \[是否支持] 支持

  \[文件描述]
  ```git
  //tokenid发生转移时触发
  event Transfer(address indexed from, address indexed to, uint256 indexed tokenId)
  //owner授权approved管理tokenid时触发
  event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId)
  //owner批准或禁止operator操作所有资产时触发
  event ApprovalForAll(address indexed owner, address indexed operator, bool approved)
  //返回owner中包含token数量
  function balanceOf(address owner) external view returns (uint256 balance)
  //返回指定tokenid的owner
  function ownerOf(uint256 tokenId) external view returns (address owner)
  //安全转移tokenid
  function safeTransferFrom(address from, address to, uint256 tokenId, bytes calldata data) external
  //
  function safeTransferFrom(address from, address to, uint256 tokenId) external
  //
  function transferFrom(address from, address to, uint256 tokenId) external
  //授权转移指定tokenid的权限
  function approve(address to, uint256 tokenId) external
  //调用者授权或移除指定operator操作的权限
  function setApprovalForAll(address operator, bool approved) external
  //获取被授权操作某个tokenid的账户地址
  function getApproved(uint256 tokenId) external view returns (address operator)
  //如果允许“操作员”管理“所有者”的所有资产，则返回。
  function isApprovedForAll(address owner, address operator) external view returns (bool)

  ```
- IERC721Receiver.sol

  \[描述] IERC721Receiver标准接口文件

  \[是否支持] 支持

  \[文件描述]
  ```git
  //当一个{IERC721} ' tokenId '令牌被' operator '从' from '通过{IERC721- safetransferfrom}转移到这个合约时，这个函数被调用。
  function onERC721Received(
          address operator,
          address from,
          uint256 tokenId,
          bytes calldata data
      ) external returns (bytes4)
  ```
- ERC721.sol

  \[描述] ERC721标准实现文件

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {ERC721} from "../../../openzeppelin-contracts/contracts/token/ERC721/ERC721.sol";

  contract MyERC721 is ERC721 {

      constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_) {

      }

      //balanceOf
      //ownerOf
      //name
      //symbol
      //approve
      //getApproved
      //setApprovalForAll
      //isApprovedForAll
      //transferFrom
      //safeTransferFrom
      
      function mint(address to, uint256 tokenId) public {
          _mint(to, tokenId);
      }
      
      function SafeMint(address to, uint256 tokenId) public {
          _safeMint(to, tokenId);
      }

      function Burn(uint256 tokenId) public {
          _burn(tokenId);
      }
  }

  ```

> 📌ERC1155

- utils/ERC1155Holder.sol

  \[描述] IERC1155Receiver 实现实例

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {ERC1155Holder} from "../../../../openzeppelin-contracts/contracts/token/ERC1155/utils/ERC1155Holder.sol";

  contract MyERC1155Holder is ERC1155Holder {
      //onERC721Received

      function OnERC1155Received() public returns(bool) {
          address a;
          address b;
          uint256 c;
          uint256 d;
          bytes memory e;
          return onERC1155Received(a, b, c, d, e) == 0xf23a6e61;
      }

      function OnERC1155BatchReceived() public returns(bool) {
          address a;
          address b;
          uint256[] memory c;
          uint256[] memory d;
          bytes memory e;
          return onERC1155BatchReceived(a, b, c, d, e) == 0xbc197c81;
      }
  }
  ```
- extensions/ERC1155Burnable.sol

  \[描述] ERC1155 允许token持有者销毁他们拥有的token和已被批准使用的token

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {ERC1155Burnable} from "../../../../openzeppelin-contracts/contracts/token/ERC1155/extensions/ERC1155Burnable.sol";
  import {ERC1155} from "../../../../openzeppelin-contracts/contracts/token/ERC1155/ERC1155.sol";

  contract MyERC1155Burnable is ERC1155Burnable {

      constructor(string memory uri_) ERC1155(uri_) {

      }

      //balanceOf
      
      function mint(address to, uint256 id, uint256 value, bytes memory data) public {
          _mint(to, id, value, data);
      }

      function mintBatch(address to, uint256[] memory ids, uint256[] memory values, bytes memory data) public {
          _mintBatch(to, ids, values, data);
      }

      //burn
      //burnBatch
  }
  ```
- extensions/ERC1155Pausable.sol

  \[描述] ERC1155 拓展，可暂停token转移、铸币及销毁

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {ERC1155Pausable} from "../../../../openzeppelin-contracts/contracts/token/ERC1155/extensions/ERC1155Pausable.sol";
  import {ERC1155} from "../../../../openzeppelin-contracts/contracts/token/ERC1155/ERC1155.sol";

  contract MyERC1155Pausable is ERC1155Pausable {

      constructor(string memory uri_) ERC1155(uri_) {

      }
      
      function mint(address to, uint256 id, uint256 value, bytes memory data) public {
          _mint(to, id, value, data);
      }

      function Pause() public {
          _pause();
      }

      function Unpause() public {
          _unpause();
      }

  }
  ```
- extensions/ERC1155Supply.sol

  \[描述] ERC1155 拓展，增加了对每个id的总供应量的跟踪

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {ERC1155Supply} from "../../../../openzeppelin-contracts/contracts/token/ERC1155/extensions/ERC1155Supply.sol";
  import {ERC1155} from "../../../../openzeppelin-contracts/contracts/token/ERC1155/ERC1155.sol";

  contract MyERC1155Supply is ERC1155Supply {

      constructor(string memory uri_) ERC1155(uri_) {

      }
      
      //totalSupply
      //totalSupply id
      //exists
      function mint(address to, uint256 id, uint256 value, bytes memory data) public {
          _mint(to, id, value, data);
      }

  }
  ```
- extensions/ERC1155URIStorage.sol

  \[描述] ERC1155 拓展，增加了对token uri管理

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {ERC1155URIStorage} from "../../../../openzeppelin-contracts/contracts/token/ERC1155/extensions/ERC1155URIStorage.sol";
  import {ERC1155} from "../../../../openzeppelin-contracts/contracts/token/ERC1155/ERC1155.sol";

  contract MyERC1155URIStorage is ERC1155URIStorage {

      constructor(string memory uri_) ERC1155(uri_) {

      }
      
      //uri -id 
      //
      function mint(address to, uint256 id, uint256 value, bytes memory data) public {
          _mint(to, id, value, data);
      }

      function SetBaseURI(string memory baseURI) public {
          _setBaseURI(baseURI);
      }

      function SetURI(uint256 tokenId, string memory tokenURI) public {
          _setURI(tokenId, tokenURI);
      }
  }
  ```
- extensions/IERC1155MetadataURI.sol

  \[描述] ERC1155标准接口文件可选元数据

  \[是否支持] 支持

  \[文件描述]
  ```c
  //返回类型为id的token uri
  function uri(uint256 id) external view returns (string memory)
  ```
- IERC1155.sol

  \[描述] ERC1155标准接口文件

  \[是否支持] 支持

  \[文件描述]
  ```git
  EVENTS：
  17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c31: ApprovalForAll(address,address,bool)
  4a39dc06d4c0dbc64b70af90fd698a233a518aa5d07e595d983b8c0526c8f7fb: TransferBatch(address,address,address,uint256[],uint256[])
  c3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62: TransferSingle(address,address,address,uint256,uint256)
  6bb7ff708619ba0610cba295a58592e0451dee2622938c8755667688daf3529b: URI(string,uint256)

  FUNCTIONS： 
  //返回' account '拥有的token类型' id '的值。
  function balanceOf(address account, uint256 id) external view returns (uint256)
  //balanceOf的批处理版本
  function balanceOfBatch(
          address[] calldata accounts,
          uint256[] calldata ids
      ) external view returns (uint256[] memory)
  //授予或撤销转移调用者token的许可，
  function setApprovalForAll(address operator, bool approved) external
  //如果' operator '被批准转移' ' account ' '的token，则返回true
  function isApprovedForAll(address account, address operator) external view returns (bool)
  //在from和to之间传输转移value个token，id为指定的token类型id
  function safeTransferFrom(address from, address to, uint256 id, uint256 value, bytes calldata data) external
  //safeTransferFrom的批处理版本
  function safeBatchTransferFrom(
          address from,
          address to,
          uint256[] calldata ids,
          uint256[] calldata values,
          bytes calldata data
      ) external

  ```
- IERC1155Receiver.sol

  \[描述] IERC1155Receiver标准接口文件

  \[是否支持] 支持

  \[文件描述]
  ```git
  //处理单个ERC1155 token类型的接收。此函数在余额更新后的safeTransferFrom结束时调用。
  function onERC1155Received(
          address operator,
          address from,
          uint256 id,
          uint256 value,
          bytes calldata data
      ) external returns (bytes4)
  //处理多个ERC1155 token类型的接收。在更新余额之后，在safeBatchTransferFrom结束时调用该函数。
  function onERC1155BatchReceived(
          address operator,
          address from,
          uint256[] calldata ids,
          uint256[] calldata values,
          bytes calldata data
      ) external returns (bytes4)

  ```
- ERC1155.sol

  \[描述] ERC1155标准实现文件

  \[是否支持] 支持
  ```c
  pragma solidity ^0.8.20;

  import {ERC1155} from "../../../openzeppelin-contracts/contracts/token/ERC1155/ERC1155.sol";

  contract MyERC1155 is ERC1155 {

      constructor(string memory uri_) ERC1155(uri_) {

      }

      //uri
      //balanceOf
      //balanceOfBatch
      //setApprovalForAll
      //isApprovedForAll
      //safeTransferFrom
      //safeBatchTransferFrom

      function SetURI(string memory newuri) public {
          _setURI(newuri);
      }

      function mint(address to, uint256 id, uint256 value, bytes memory data) public {
          _mint(to, id, value, data);
      }

      function mintBatch(address to, uint256[] memory ids, uint256[] memory values, bytes memory data) public {
          _mintBatch(to, ids, values, data);
      }

      function Burn(address from, uint256 id, uint256 value) public {
          _burn(from, id, value);
      }

      function BurnBatch(address from, uint256[] memory ids, uint256[] memory values) public {
          _burnBatch(from, ids, values);
      }
  }

  ```
