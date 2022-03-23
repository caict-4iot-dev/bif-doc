# OpenZeppelin

## access

* `AccessControl.sol`

    基于权限role的access control系统.

    adminRole[user1, user2] => RoleA[user2, user3] => RoleB[usern...]

* `AccessControlEnumerable.sol`

    支持某一个Role下的user的枚举

* `Ownable.sol`

    Owner Allowed Access Control

## finance

* `PaymentSplitter.sol`

    一个自动按比例划分发放ETH, 或者ERC20代币的合约. 使用方式为初始化合约时, 约定参与分成用户和分成比例.

    之后可以往该合约转入ETH或者ERC20代币, 合约内部会按照事先定义的比例划分到各个分成用户名下.

* `VestingWallet.sol`

    一个按时间等比例释放ETH/ERC20代币的合约. 指定一个收款人, 可以根据时间线性提取资金

## governance

### compatibility

* `GovernorCompatibilityBravo.sol`

### extensions

### utils

#### Votes.sol

* `Governor.sol`

* `TimelockController.sol`

## metatx

metatx指的是现在比较流行的一种代发交易模式, 用户账户不必有足够的油费, 而且交易签名后发送给relayer, relayer代替用户发出该交易.

* `ERC2771Context.sol`

    支持meta transaction版本的ERC2771Context, 主要支持了两个函数:

    * _msgSender()

        如果交易来自replayer, sender从calldata中选取, 否则走默认的msgSender
    
    * _msgData()

        replayer的话, 从calldata中截取, 否则走默认的

    继承该context的合约, 再收到trusted relayer发来的交易时, msgSender和msgData会从calldata中截取.

    这个Context是给正常的业务合约用的, 也就是接受replayer转发的交易的合约.

* `MinimalForwarder.sol`

    relayer的一个简单实现, 核心有verify和execute两个函数, 为了避免交易重放, 还有一个nonce字段.

    这个实现还是有不少问题, 比如nonce是每个合约分开计数, 那么同一个签名数据还是可能在不同的relayer之间重放的.

## mocks

## proxy

### beacon

* `BeaconProxy.sol`

### ERC1967

* `ERC1967Proxy.sol`

    基于Proxy协议实现的代理

* `ERC1967Upgrade.sol`

    主要处理合约升级,
### transparent

* `ProxyAdmin.sol`

* `TransparentUpgradeableProxy.sol`

    

### utils

* `Clones.sol`

    Clone是一个工厂合约, 可以调用其中函数复制指定合约.

* `Proxy.sol`

    到proxy的所有调用, 都会转发给implementation, 调用delegatecall, 在自身的存储空间上调用implementation的代码


## security

## token

### common

* `ERC2981.sol`

支持版税的ERC721, 每一个Token可以单独设置RoyaltyInfo { receiver, royaltyFraction }, receiver是版权方, royaltyFraction是1/10000为单位的版税比例.


### ERC20

#### extensions

* `draft-ERC20Permit.sol`

    base On ERC20, ERC712, 但是多了一个permit函数, 允许用用户签名来做approve, 这样可以连approve和使用在一个交易内完成.
1. presets

1. utils

* `ERC20.sol`

ERC20的标准实现

### ERC721

* `extensions/draft-ERC721Votes.sol`

* `extensions/ERC721Burnable.sol`

* `extensions/ERC721Enumerable.sol`

* `extensions/ERC721Pausable.sol`

* `extensions/ERC721Royalty.sol`

* `extensions/ERC721URIStorage.sol`

* `presets/ERC721PresetMinterPauserAutold.sol`

* `utils/ERC721Holder.sol`

* `ERC721.sol`

    ERC721的标准实现, 值得注意的几个函数:

    * tokenURI(uint256 tokenId)

        返回baseURI+TokenId

    * mint, transfer都需要检查to地址,如果为合约, 需要支持安全回调

## utils

### cryptography

* `draft-EIP712.sol`

* `ECDSA.sol`

### escrow

### introspection

* `ERC165.sol`

    ERC165就多了一个函数, 用来表示合约是否支持某一个interface.

    这里使用了一个机制 type(interface).interfaceId, interfaceId为该interface下所有function的signature(不考虑返回值)的hash结果.

    function supportsInterface(bytes4 interfaceId) 

* `ERC165Storage.sol`

    做了一个map来存储支持的interface, 其它函数可以继承该函数, 然后调用 _registerInterface来声明对某个interface的支持

* `ERC1820Impelementer.sol`


### math

#### Math.sol

#### SafeCast.sol

#### SafeMath.sol

#### SignedMath.sol

#### SignedSafeMath.sol

### structs

#### BitMaps.sol

#### DoubleEndedQueue.sol

#### EnumerableMap.sol

#### EnumerableSet.sol

### Address.sol

`library Address`

1. isContract
1. sendValue // use call instead of transfer
1. function

### Array.sol

### Base64.sol

提供了base64编码的函数

### Checkpoints.sol

一个library, 可以存储和读取指定的history value 

### Context.sol

提供了msgSender和msdData的函数式访问方法

### Counters.sol

### Create2.sol

create2 library, 提供函数提前计算地址

### Multicall.sol

1. function multicall(bytes[] calldata data) external virtual retuns (bytes[] memory results) {

}

### StorageSlot.sol


基于汇编slot语法, 提供一个对于固定存储位置的访问功能.


### Strings.sol

1. toString(uint256 value) returns (string memory)

1. toHexString(uint256 value)

### Timers.sol

struct Timestamp {
    uint64 _deadline;
}

1. getDeadline(Timestamp memory timer) returns uint64

