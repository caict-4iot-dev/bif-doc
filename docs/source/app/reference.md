# 星火链智能合约参考

​本节为星火链智能合约的示例。

## ERC20合约
<h2 id="min-content" style="display:none;"> </h2>
​
本节描述通过星火链网实现并部署ERC20智能合约。

​ERC20可以简单理解成以太坊上的一个代币协议，所有基于以太坊开发的代币合约都遵守这个协议。有关ERC20标准可以参考[官方文档](https://theethereum.wiki/w/index.php/ERC20_Token_Standard)。

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

```solidity
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

## ERC721合约

​本节描述通过星火链网实现并部署ERC721智能合约。

相比于ERC20，ERC721是非同质化代币，也就意味着每个Token都是不一样的，都有自己的唯一性和独特价值，当然这也就意味着它们是不可分割的。有关ERC721标准可以参考[官方文档](https://eips.ethereum.org/EIPS/eip-721)。

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

```solidity
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
    function TokenERC721(string memory name_, string memory symbol_) public {
        _name = name_;
        _symbol = symbol_;
	    fundation = msg.sender; 
    }
    
    constructor() {
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

### JavaScript合约

**合约文件 - JavaScript **

```js
'use strict';

// 管理员  
const _fundation = "_fundation";

// 代币名称
const _name = "_name";

// 代币符号
const _symbol = "_symbol";


// 账户有 几个NFT      address => uint256
const BALANCEOF = "_balanceOf";

// NFT 属于哪个账户的    uint256 => address
var TOKENS = "_tokens";

// 授权集合    uint256 => address
const ALLOWANCES = "_allowances";

// 全部 NFT 的授权集合    address => mapping(address => bool)
const ISALLAPPROVED = "_isAllApproved";

const sender_g = Chain.msg.sender;
const chainCode_g = Chain.chainCode;

/*
	是否为合约所有者
*/
function isContractOwner(){
    var owner = Chain.load(_fundation);
    if(Chain.msg.sender === owner){
        return true;
    }
    else{
        return false;
    }
}

function init(input_str){

    var input = JSON.parse(input_str);
    var params = input.params;

    Utils.log('input_str: (' + input_str + ').');

    Chain.store("_name", params.name);
    Chain.store("_symbol", params.symbol);
    Chain.store("_fundation", sender_g);
        
    return;
} 


// 可选
function nameOfNFT() {
    return Chain.load("_name");
}
function symbol() {
    return Chain.load("_symbol");
}

function _exists(tokenId) {

    var tokens = {}; // 二维数组
    var dataToken = JSON.parse(Chain.load(TOKENS));
    if (dataToken) {
        tokens = dataToken;
    }

    if (tokens[tokenId] !== undefined){
        return true;
    }else{
        return false;  
    }
}

// 必须实现 ----  9个方法
function balanceOf(params) {

    var owner = params.owner; 

    Utils.assert(owner.length !== 0 , "ERC721: balance query for the zero address");

    var balances = {};
    var data = JSON.parse(Chain.load(BALANCEOF));
    if (data) {
        balances = data;
    }

    if (balances[owner] !== undefined){
        return balances[owner];  
    }else{
        return 0;    
    }
}

// 代币的地址
function _ownerOf(tokenId) {

    var tokens = {}; 
    var dataToken = JSON.parse(Chain.load(TOKENS));
    if (dataToken) {
        tokens = dataToken;
    }

    var owner = "";
    if (tokens[tokenId] !== undefined){
        owner = tokens[tokenId];  
    }
    
    Utils.assert(owner.length !== 0, "ERC721: owner query for nonexistent token");
    return owner;
}

/**
* 返回NFT的 拥有者。
* @param params 
* @param params.tokenId 代币的标识符

*/
function ownerOf(params) {

    var tokenId = params.tokenId;
    return _ownerOf(tokenId);
}

/**
* 创建NFT。
* @param _tokenId 代币的标识符
* @param owner 拥有者
*/
function mint(params) {

    if(isContractOwner() === false){
        Utils.log('mint' + Chain.msg.sender);
        return;
    }

    var to = params.to;
    var tokenId = params.tokenId;
    Utils.log('mint-params: ' + params);

    Utils.assert(to.length !== 0 , "ERC721: mint to the zero address");
    Utils.assert(!_exists(tokenId), "ERC721: token already minted");

    var balances = {}; 
    var data = JSON.parse(Chain.load(BALANCEOF));
    if (data) {
        balances = data;
    }

    if (balances[to] !== undefined){
        var temp = balances[to];
        balances[to] = temp + 1;  
    }else{
        balances[to] = 1;  
    }
      
    // 读取 tokens 集合
    var tokens = {};
    var dataToken = JSON.parse(Chain.load(TOKENS));
    if (dataToken) {
        tokens = dataToken;
    }

    tokens[tokenId] = to;

    Chain.store(BALANCEOF, JSON.stringify(balances));
    Chain.store(TOKENS, JSON.stringify(tokens));
     
    Chain.tlog('Transfer', '', to, tokenId);
}

function __setApproved( tokenId, to) {

    // 读取 allowance 集合
    var allowances = {}; 
    var data = JSON.parse(Chain.load(ALLOWANCES));
    if (data) {
        allowances = data;
    }

    allowances[tokenId] = to;
    Chain.store(ALLOWANCES, JSON.stringify(allowances));
}

function _approve( to, tokenId)  {

    __setApproved( tokenId, to);

    Chain.tlog('Approval', _ownerOf(tokenId), to, tokenId);
}

function _getApproved(tokenId) {

    Utils.assert(_exists(tokenId), "ERC721: approved query for nonexistent token");
    
    // 读取 allowance 集合
    var allowances = {};
    var data = JSON.parse(Chain.load(ALLOWANCES));
    if (data) {
        allowances = data;
    }

    if (allowances[tokenId] !== undefined){
        
        return allowances[tokenId]; 
    }else{
        return "";  
    }
}

function getApproved(params) {
    var input = params; // tokenId

    return _getApproved(input.tokenId);
}

function __getIsAllApproved(owner, to){

    // 读取 全部授权的集合
    var allApproved = {}; 
    var data = JSON.parse(Chain.load(ISALLAPPROVED));
    if (data) {
        allApproved = data;
    }
    
    if (allApproved[owner] === undefined ){
        return false;
    }

    return allApproved[owner][to];
}

function _isApprovedForAll( owner, operator) {

    Utils.assert(owner.length !== 0, "_owner can not be empty!");
    Utils.assert(operator.length !== 0, "_operator can not be empty!");

    return  __getIsAllApproved(owner, operator);
}

function isApprovedForAll(params) {

    var input = params; // owner, operator

    return _isApprovedForAll(input.owner, input.operator);
}


function __setAllApproved(owner, to, isAllApproved){
    
    // 读取 全部授权的集合
    var allApproved = {}; 
    var data = JSON.parse(Chain.load(ISALLAPPROVED));
    if (data) {
        allApproved = data;
    }

    var inner_allApproved = {};
    
    if (allApproved[owner] === undefined ){
        allApproved[owner] = inner_allApproved; 
    }
    
    Utils.log("allApproved:" + allApproved);
    
    allApproved[owner][to] = isAllApproved;

    Utils.log("allApproved after:" + allApproved);

    Chain.store(ISALLAPPROVED, JSON.stringify(allApproved));
}

function _setApprovalForAll(owner, operator, isApproved) {
    Utils.assert(owner !== operator, "ERC721: approve to caller");
    // 设置 全部授权
    __setAllApproved(owner, operator, isApproved);
    Chain.tlog('ApprovalForAll', owner, operator, isApproved);
}

// 设置 全部授权
function setApprovalForAll( params )  {

    return _setApprovalForAll(sender_g, params.operator, params.isApproved);
}

function _transfer(
     from,
     to,
     tokenId
)  {

    Utils.log('_ownerOf(tokenId): (' + _ownerOf(tokenId) + ').');
    Utils.log('from: (' + from + ').');

    Utils.assert(_ownerOf(tokenId) === from, "ERC721: transfer from incorrect owner");
    Utils.assert(to.length !== 0, "ERC721: transfer to the zero address");

    _approve('', tokenId);

    var balances = {}; 
    var data = JSON.parse(Chain.load(BALANCEOF));
    if (data) {
        balances = data;
    }

    if (balances[from] !== undefined){
        var temp = balances[from];
        balances[from] = temp - 1;  
    }

    if (balances[to] !== undefined){
        var tempTo = balances[to];
        balances[to] = tempTo + 1; 
    }else{
        balances[to] = 1; 
    }
    
    // 读取 tokens 集合
    var tokens = {};
    var dataToken = JSON.parse(Chain.load(TOKENS));
    if (dataToken) {
        tokens = dataToken;
    }

    tokens[tokenId] = to;

    Chain.store(BALANCEOF, JSON.stringify(balances));
    Chain.store(TOKENS, JSON.stringify(tokens));

    Chain.tlog('Transfer', from, to, tokenId);
}

function _isApprovedOrOwner(spender, tokenId)  {

    Utils.log("_exists(tokenId): " + _exists(tokenId));
    Utils.assert(_exists(tokenId), "ERC721: operator query for nonexistent token");

    var owner = _ownerOf(tokenId);
    Utils.log("owner: " + owner);
    Utils.log("_getApproved(tokenId): " + _getApproved(tokenId));
    Utils.log("_isApprovedForAll(owner, spender): " + _isApprovedForAll(owner, spender));
    return (spender === owner || _getApproved(tokenId) === spender || _isApprovedForAll(owner, spender));
}

function approve( params )  {

    var input = params; // to,  tokenId

    var owner = _ownerOf(input.tokenId);
    Utils.assert(input.to !== owner, "ERC721: approval to current owner");
    Utils.log("approve-sender_g:" + sender_g + "  owner:" + owner);
    Utils.assert(
        sender_g === owner || _isApprovedForAll(owner, sender_g),
        "ERC721: approve caller is not owner nor approved for all"
    );

    _approve(input.to, input.tokenId);
}

function transferFrom(params) {

    var input = params; // from、to、tokenId

    Utils.assert(_isApprovedOrOwner(sender_g, input.tokenId), "ERC721: transfer caller is not owner nor approved");

    _transfer(input.from, input.to, input.tokenId);
}

function main(input_str){
    var input = JSON.parse(input_str);

    if(input.method === 'mint'){
        mint(input.params);
    }
    else if(input.method === 'transferFrom'){
        transferFrom(input.params);
    }
    else if(input.method === 'approve') {
        approve(input.params);
    }else if(input.method === 'setApprovalForAll') {
        setApprovalForAll(input.params);
    }
 
    else{
        throw '<Main interface passes an invalid operation type>';
    }
}

function query(input_str){
    var input  = JSON.parse(input_str);
    var object ={};
    if(input.method === 'nameOfNFT'){
        object = nameOfNFT();
    }else if(input.method === 'symbol'){
        object = symbol();
    }else if(input.method === 'balanceOf'){
        object = balanceOf(input.params);
    }else if(input.method === 'ownerOf'){
        object = ownerOf(input.params);
    }else if(input.method === 'isApprovedForAll'){
        object = isApprovedForAll(input.params);
    }else if(input.method === 'getApproved'){
        object = getApproved(input.params);
    }
    else{
       	throw '<unidentified operation type>';
    }
    return JSON.stringify(object);
}
```

##  ERC1155合约

本节描述通过星火链网实现并部署ERC1155智能合约。

ERC1155在一定程度上融合了ERC-20和ERC-721的功能。其主要用途包括了发行同质化代币和非同质化代币。同质化代币是指：能像ERC-20一样发布各样的代币类型；与此同时，ERC-1155标准更是能够发行NFT，且能基于一个合约同时发行多个NFT，有关ERC1155标准可以参考[官方文档](https://eips.ethereum.org/EIPS/eip-1155)。


### 合约说明

- **合约接口**

  注意：在实现转账功能时，如果接收方的地址没有拥有者，或者是一个合约地址，那么NFT被转出去之后，就意味着该NFT以后将没有流通的功能了。因此转账的时候，要慎重。若是合约地址，可以采取安全转账的方式，根据ERC165的方式判断该合约是否实现了onERC1155Received接口，若是没有实现，则智能合约的执行将被中止，若实现了，说明该合约遵守了ERC1155合约的标准，确保以后NFT可以进行流通，则转账继续。目前，在星火链网上实现的非同质化代币智能合约模板仅提供基础的功能，并没有提供安全转账的功能。

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

```solidity
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

### JavaScript合约

**合约文件 - JavaScript **

```js
'use strict';

// 管理员  
const FUNDATION = "_fundation";
// uri
const URI = "_uri";

// 账户有 几个NFT      ( uint256(代币类型), map(address, uint256))
const BALANCES = "_balances";

// 全部 NFT 的授权集合    (address, map(address, bool))
const OPERATORAPPROVALS = "_operatorApprovals";

const sender_g = Chain.msg.sender;
const chainCode_g = Chain.chainCode;

function _setURI(newuri) {
    Chain.store(URI, JSON.stringify(newuri));
}

/*
	是否为合约所有者
*/
function isContractOwner(){
    var owner = Chain.load(FUNDATION);
    if(Chain.msg.sender === owner){
        return true;
    }
    else{
        return false;
    }
}

function init(input_str) {

    var input = JSON.parse(input_str);
    var params = input.params; // uri

    Utils.log('input_str: (' + input_str + ').');

    _setURI(params.uri);
    Chain.store(FUNDATION, sender_g);

    return;
}

function uri(id) {
    return JSON.parse(Chain.load(URI));
}

function _getBalanceOf(id, account) {

    //读取 数组集合
    var balances = {}; 
    var data = JSON.parse(Chain.load(BALANCES));
    if (data) {
        balances = data;
    }

    var inner_balances = {};

    if (balances[id] === undefined ){
        balances[id] = inner_balances; 
    }

    if (balances[id][account] === undefined ){
        return 0; 
    }

    return balances[id][account];
}

function _setBalanceOfForKey(id, account, value) {
   
    // 读取 全部授权的集合
    var balances = {}; 
    var data = JSON.parse(Chain.load(BALANCES));
    if (data) {
        balances = data;
    }

    var inner_balances = {};
    
    if (balances[id] === undefined ){
        balances[id] = inner_balances; 
    }
        
    balances[id][account] = value;

    Utils.log("balances:" + balances);

    Chain.store(BALANCES, JSON.stringify(balances));
}

function balanceOf(params) {

    var account = params.account;
    var id = params.id;

    Utils.assert(account.length !== 0, "ERC1155: balance query for the zero address");

    return _getBalanceOf(id, account);
}

function balanceOfBatch(params) { 

    var accounts = params.accounts;
    var ids = params.ids;

    Utils.assert(accounts.length === ids.length, "ERC1155: accounts and ids length mismatch");

    var batchBalances = [];
    var i = 0;
    for (i = 0; i < accounts.length; i += 1) {
        batchBalances[i] = _getBalanceOf(ids[i], accounts[i]);
    }
   
    return JSON.stringify(batchBalances);
}

function __setAllApproved(owner, to, isAllApproved){
    
    // 读取 全部授权的集合
    var allApproved = {}; 
    var data = JSON.parse(Chain.load(OPERATORAPPROVALS));
    if (data) {
        allApproved = data;
    }

    var inner_allApproved = {};
    
    if (allApproved[owner] === undefined ){
        allApproved[owner] = inner_allApproved; 
    }
        
    allApproved[owner][to] = isAllApproved;

    Utils.log("allApproved:" + allApproved);

    Chain.store(OPERATORAPPROVALS, JSON.stringify(allApproved));
}

function _setApprovalForAll(owner, operator ,isApproved)  {

    Utils.assert(owner !== operator, "ERC1155: setting approval status for self");

    __setAllApproved(owner, operator, isApproved);
    Chain.tlog('ApprovalForAll', owner, operator, isApproved);
}

function setApprovalForAll( params ) {

    var operator = params.operator;
    var isApproved = params.isApproved; // bool 类型

    _setApprovalForAll(sender_g, operator, isApproved);
}

function __getIsAllApproved(owner, to){

    // 读取 全部授权的集合
    var allApproved = {}; 
    var data = JSON.parse(Chain.load(OPERATORAPPROVALS));
    if (data) {
        allApproved = data;
    }

    var inner_allApproved = {};

    if (allApproved[owner] === undefined ){
        allApproved[owner] = inner_allApproved; 
    }

    if (allApproved[owner][to] === undefined ){
        return false; 
    }

    return allApproved[owner][to];
}

function _isApprovedForAll( owner, operator) {

    Utils.assert(owner.length !== 0, "_owner can not be empty!");
    Utils.assert(operator.length !== 0, "_operator can not be empty!");

    return  __getIsAllApproved(owner, operator);
}

function isApprovedForAll( params ) {

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

function safeTransferFrom( params ) {

    var from = params.from;
    var to = params.to; 
    var id = params.id; // int
    var amount = params.amount; // int
    var data = params.data; 

    Utils.assert(from === sender_g || _isApprovedForAll(from, sender_g), "ERC1155: caller is not owner nor approved");

    _safeTransferFrom(from, to, id, amount, data);
}

function _safeBatchTransferFrom( from, to, ids, amounts, data )  {

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

        fromBalance = _getBalanceOf(id, from);
        Utils.assert(fromBalance >= amount, "ERC1155:  insufficient balance for transfer");

        _setBalanceOfForKey(id, from, fromBalance - amount);
        toBalance = _getBalanceOf(id, to);
        _setBalanceOfForKey(id, to, toBalance + amount);
    }

    Chain.tlog('TransferBatch', operator, from, to, JSON.stringify(ids), JSON.stringify(amounts));
}

function safeBatchTransferFrom( params ) {

    var from = params.from;
    var to = params.to; 
    var ids = params.ids; 
    var amounts = params.amounts;
    var data = params.data; 

    Utils.assert(from === sender_g || _isApprovedForAll(from, sender_g), "ERC1155: caller is not owner nor approved");

    _safeBatchTransferFrom(from, to, ids, amounts, data);
}

function mint( params ) {

    if(isContractOwner() === false){
        Utils.log('mint' + Chain.msg.sender);
        return;
    }

    var to = params.to;
    var id = params.id; //int 
    var amount = params.amount; //int 
    var data = params.data;

    Utils.assert(to.length > 0 , "ERC1155: mint to the zero address");

    var operator = sender_g;

    var toBalance = _getBalanceOf(id, to);
    _setBalanceOfForKey(id, to , toBalance + amount);

    Chain.tlog('TransferSingle', operator, "", to, id, amount);
}

function mintBatch( params ) {

    if(isContractOwner() === false){
        Utils.log('mint' + Chain.msg.sender);
        return;
    }

    var to = params.to;
    var ids = params.ids; 
    var amounts = params.amounts; 
    var data = params.data;

    Utils.assert(to.length > 0 , "ERC1155: mint to the zero address");
    Utils.assert(ids.length === amounts.length, "ERC1155: ids and amounts length mismatch");

    Utils.log('mintBatch-ids: (' + ids + ').');
    Utils.log('mintBatch-amounts: (' + amounts + ').');

    var operator = sender_g;

    var i = 0;
    var toBalance;
    for ( i = 0; i < ids.length; i += 1) {
         toBalance = _getBalanceOf(ids[i], to);
         _setBalanceOfForKey(ids[i], to , toBalance + amounts[i]);
    }

    Chain.tlog('TransferBatch', operator, "", to, JSON.stringify(ids), JSON.stringify(amounts));
}

function main(input_str){
    var input = JSON.parse(input_str);

    if(input.method === 'mint'){
        mint(input.params);
    }
    else if(input.method === 'mintBatch'){
        mintBatch(input.params);
    }
    else if(input.method === 'safeTransferFrom'){
        safeTransferFrom(input.params);
    }
    else if(input.method === 'safeBatchTransferFrom') {
        safeBatchTransferFrom(input.params);
    }else if(input.method === 'setApprovalForAll') {
        setApprovalForAll(input.params);
    }
 
    else{
        throw '<Main interface passes an invalid operation type>';
    }
}

function query(input_str){
    var input  = JSON.parse(input_str);
    var object ={};
    if(input.method === 'uri'){
        object = uri(input.params);
    }else if(input.method === 'balanceOf'){
        object = balanceOf(input.params);
    }else if(input.method === 'balanceOfBatch'){
        object = balanceOfBatch(input.params);
    }else if(input.method === 'isApprovedForAll'){
        object = isApprovedForAll(input.params);
    }
    else{
       	throw '<unidentified operation type>';
    }
    return JSON.stringify(object);
}
```