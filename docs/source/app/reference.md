# 智能合约示例

本节为星火链智能合约的示例。

## ERC20合约

本节描述通过星火链网实现并部署ERC20智能合约。

ERC20可以简单理解成以太坊上的一个代币协议，所有基于以太坊开发的代币合约都遵守这个协议。有关ERC20标准可以参考[官方文档](https://theethereum.wiki/w/index.php/ERC20_Token_Standard)。

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

```
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

本节描述通过星火链网实现并部署ERC721智能合约。

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

```
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

**合约文件 - JavaScript**

```
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

```
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

**合约文件 - JavaScript**

```
'use strict';

// 管理员  
const FUNDATION = "_fundation";

// 代币名称
const NAME = "_name";

// 代币符号
const SYMBOL = "_symbol";

// metadata uri
const TOKENURI = "_tokenUri";

// 账户有 几个NFT      address => uint256
const BALANCEOF = "_balanceOf";

// NFT 属于哪个账户的    uint256 => address
var TOKENS = "_tokens";

// 授权集合    uint256 => address
const ALLOWANCES = "_allowances";

// 全部 NFT 的授权集合    address => mapping(address => bool)
const ISALLAPPROVED = "_isAllApproved";

// enumeration
// 所有nft的tokenId 数组     address[]
const ALLTOKENS = "_allTokens";

// tokenId  => 在所有nft中的 index      address => uint256
const ALLTOKENSINDEX = "_allTokensIndex";

// tokenId => owner里面的index    address => uint256
const OWNEDTOKENSINDEX = "_ownedTokensIndex";

// 账户地址  => nft的tokenId 数组     address => address[]
const OWNEDTOKENS = "_ownedTokens";

const sender_g = Chain.msg.sender;
const chainCode_g = Chain.chainCode;


function hashCode(str)
{
  var hash = 0;
  if (str.length === 0) {
     return hash;
  }
  var i;
  var char;
  for (i = 0; i < str.length; i+=1) {
    char = str.charCodeAt(i);
    hash += char;
  }
  return hash%100;
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
        Utils.log("onlyFundation can call this method!");
        return false;
    }
}

function _setTokenURI(newuri) {
    Chain.store(TOKENURI, newuri);
}

function setTokenURI(params) {

    if(isContractOwner() === false){
        Utils.log('setTokenURI' + Chain.msg.sender);
        return;
    }

    var tokenUri = params.tokenUri;
    _setTokenURI(tokenUri);
}

function init(input_str){

    var input = JSON.parse(input_str);
    var params = input.params;

    Utils.log('input_str: (' + input_str + ').');

    if(params.name=== undefined || params.symbol === undefined || params.tokenUri === undefined ||
        !params.name.length || !params.symbol.length || !params.tokenUri.length){     
        Utils.assert(false , "DNA721: init  params is invalid, please check!");
    }

    Chain.store(NAME, params.name);
    Chain.store(SYMBOL, params.symbol);
    _setTokenURI(params.tokenUri);
    Chain.store(FUNDATION, sender_g);
    return;
} 


// metadata
function name() {
    return Chain.load("_name");
}
function symbol() {
    return Chain.load("_symbol");
}

function _exists(tokenId) {
    var index=hashCode(tokenId);
    var tokens = {}; // 二维数组
    var dataToken = JSON.parse(Chain.load(TOKENS+'_'+index));
    if (dataToken) {
        tokens = dataToken;
    }

    if (tokens[tokenId] !== undefined){
        return true;
    }else{
        return false;  
    }
}

// return string
function tokenURI(params) {
    
    var tokenId = params.tokenId;
    Utils.assert(Utils.addressCheck(tokenId) , "DNA721: tokenURI for params: tokenId is invalid bid address");
    Utils.log('tokenId: ' + params.tokenId);

    Utils.assert(_exists(tokenId), "DNA721: URI query for nonexistent token");
    var tokenUri = Chain.load(TOKENURI);

    if(tokenUri.length > 0){
        
        return tokenUri + tokenId;
    }
    return "";
}

// 必须实现 ----  9个方法
function balanceOf(params) {

    var owner = params.owner; 
	
    Utils.assert(Utils.addressCheck(owner) , "DNA721: balanceOf query for params: owner is invalid bid address");
    var index=hashCode(owner);
    var balances = {};
    var data = JSON.parse(Chain.load(BALANCEOF+'_'+index));
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
    var index=hashCode(tokenId);
    var tokens = {}; 
    var dataToken = JSON.parse(Chain.load(TOKENS+'_'+index));
    if (dataToken) {
        tokens = dataToken;
    }

    var owner = "";
    if (tokens[tokenId] !== undefined){
        owner = tokens[tokenId];  
    }
    
    Utils.assert(owner.length !== 0, "DNA721: owner query for nonexistent token");
    return owner;
}

/**
* 返回NFT的 拥有者。
* @param params 
* @param params.tokenId 代币的标识符

*/
function ownerOf(params) {

    var tokenId = params.tokenId;
    Utils.assert(Utils.addressCheck(tokenId) , "DNA721: ownerOf for params: tokenId is invalid bid address");
    return _ownerOf(tokenId);
}


// for enumeration
function _addTokenToOwnerEnumeration(to, tokenId) {

    // 1 
	var index=hashCode(to);
    var ownedTokens = {}; 
    var data = JSON.parse(Chain.load(OWNEDTOKENS+'_'+index));
    if (data) {
        ownedTokens = data;
    }
    
    var ownedTokensIndex = {}; 
    var dataIndex = JSON.parse(Chain.load(OWNEDTOKENSINDEX+'_'+index));
    if (dataIndex) {
        ownedTokensIndex = dataIndex;
    }

    if (ownedTokens[to] !== undefined){
        ownedTokensIndex[tokenId] = ownedTokens[to].length;   
    }else{
        ownedTokens[to] = [];
        ownedTokensIndex[tokenId] = 0;
    }

    // 2 
    ownedTokens[to].push(tokenId);

    // 3. store ownedTokens、_ownedTokensIndex
    Chain.store(OWNEDTOKENS+'_'+index, JSON.stringify(ownedTokens));
    Chain.store(OWNEDTOKENSINDEX+'_'+index, JSON.stringify(ownedTokensIndex));
}

function _addTokenToAllTokensEnumeration(tokenId) {

    // 1 
    var allTokensNum=1 ; 
    var dataAllNum = JSON.parse(Chain.load(ALLTOKENS));
    if (dataAllNum) {
        allTokensNum = dataAllNum+1;
    }
    var allTokens = []; 
   var index=hashCode(tokenId);
   var dataAll = JSON.parse(Chain.load(ALLTOKENS+'_'+(allTokensNum-1)));
    if (dataAll) {
        allTokens = dataAll;
    }
  
    var allTokensIndex = {}; 
    var data = JSON.parse(Chain.load(ALLTOKENSINDEX+'_'+index));
    if (data) {
        allTokensIndex = data;
    }

    // 2
    allTokensIndex[tokenId] = allTokens.length;
    allTokens.push(tokenId);

    // 3. store ownedTokens、_ownedTokensIndex
    Chain.store(ALLTOKENS, JSON.stringify(allTokensNum));
	  Chain.store(ALLTOKENS+'_'+(allTokensNum-1), JSON.stringify(allTokens));
    Chain.store(ALLTOKENSINDEX+'_'+index, JSON.stringify(allTokensIndex));
}


function _removeTokenFromOwnerEnumeration(from, tokenId) {

    // 1
	var index=hashCode(from);
    var ownedTokens = {}; 
    var data = JSON.parse(Chain.load(OWNEDTOKENS+'_'+index));
    if (data) {
        ownedTokens = data;
    }else{
        Utils.assert(false, "DNA721: removeTokenFromOwnerEnumeration ownedTokens is null");
    }

    var ownedTokensIndex = {}; 
    var dataIndex = JSON.parse(Chain.load(OWNEDTOKENSINDEX+'_'+index));
    if (dataIndex) {
        ownedTokensIndex = dataIndex;
    }

    // 2
    // 为了保护数组的顺序，将最后一个元素挪到 要删除的元素 的角标处
    var lastTokenIndex = ownedTokens[from].length - 1;
    var tokenIndex = ownedTokensIndex[tokenId];

    if (tokenIndex !== lastTokenIndex) {
        var lastTokenId = ownedTokens[from][lastTokenIndex];

        ownedTokens[from][tokenIndex] = lastTokenId; // Move the last token to the slot of the to-delete token
        ownedTokensIndex[lastTokenId] = tokenIndex; // Update the moved token's index
    }

    ownedTokens[from].length = ownedTokens[from].length - 1;

    // 3. store ownedTokens、_ownedTokensIndex
    Chain.store(OWNEDTOKENS+'_'+index, JSON.stringify(ownedTokens));
    Chain.store(OWNEDTOKENSINDEX+'_'+index, JSON.stringify(ownedTokensIndex));
}

/**
* 创建NFT。
* @param _tokenId 代币的标识符
* @param owner 拥有者
*/
function mint(params) {
  
    Utils.assert(isContractOwner(), ' mint is not  contract account');
    var to = params.to;
    var tokenId = params.tokenId;
    Utils.log('mint-params: ' + params);

    Utils.assert(Utils.addressCheck(to) , "DNA721: mint to is not bid address");
    Utils.assert(Utils.addressCheck(tokenId) , "DNA721: mint tokenId is not bid address");
    Utils.assert(!_exists(tokenId), "DNA721: token already minted");

    var balances = {}; 
	var ownerIndex=hashCode(to);
    var data = JSON.parse(Chain.load(BALANCEOF+'_'+ownerIndex));
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
    var index=hashCode(tokenId);
    var tokens = {};
    var dataToken = JSON.parse(Chain.load(TOKENS+'_'+index));
    if (dataToken) {
        tokens = dataToken;
    }

    tokens[tokenId] = to;

    Chain.store(BALANCEOF+'_'+ownerIndex, JSON.stringify(balances));
    Chain.store(TOKENS+'_'+index, JSON.stringify(tokens));

    // for enumeration
    _addTokenToOwnerEnumeration(to, tokenId);
    _addTokenToAllTokensEnumeration(tokenId);
     
    Chain.tlog('Transfer', '', to, tokenId);
}

function __setApproved( tokenId, to) {

    // 读取 allowance 集合
	var index=hashCode(tokenId);
    var allowances = {}; 
    var data = JSON.parse(Chain.load(ALLOWANCES+'_'+index));
    if (data) {
        allowances = data;
    }

    allowances[tokenId] = to;
    Chain.store(ALLOWANCES+'_'+index, JSON.stringify(allowances));
}

function _approve( to, tokenId)  {

    __setApproved( tokenId, to);

    Chain.tlog('Approval', _ownerOf(tokenId), to, tokenId);
}

function _getApproved(tokenId) {

    Utils.assert(_exists(tokenId), "DNA721: approved query for nonexistent token");
    
    // 读取 allowance 集合
	var index=hashCode(tokenId);
    var allowances = {};
    var data = JSON.parse(Chain.load(ALLOWANCES+'_'+index));
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
	var index=hashCode(owner);
    var data = JSON.parse(Chain.load(ISALLAPPROVED+'_'+index));
    if (data) {
        allApproved = data;
    }
    
    if (allApproved[owner] === undefined ){
        return false;
    }

    return allApproved[owner][to];
}

function _isApprovedForAll( owner, operator) {

    Utils.assert(Utils.addressCheck(owner) , "DNA721: _isApprovedForAll params: owner is invalid bid address");
    Utils.assert(Utils.addressCheck(operator) , "DNA721: _isApprovedForAll params: operator is invalid bid address");

    return  __getIsAllApproved(owner, operator);
}

function isApprovedForAll(params) {

    var input = params; // owner, operator
    return _isApprovedForAll(input.owner, input.operator);
}

function __setAllApproved(owner, to, isAllApproved){
    
    // 读取 全部授权的集合
    var allApproved = {}; 
	var index=hashCode(owner);
    var data = JSON.parse(Chain.load(ISALLAPPROVED+'_'+index));
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

    Chain.store(ISALLAPPROVED+'_'+index, JSON.stringify(allApproved));
}

function _setApprovalForAll(owner, operator, isApproved) {

    Utils.assert(Utils.addressCheck(owner) , "DNA721: _setApprovalForAll params: owner is invalid bid address");
    Utils.assert(Utils.addressCheck(operator) , "DNA721: _setApprovalForAll params: operator is invalid bid address");
    Utils.assert(owner !== operator, "DNA721: approve to caller");
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
     tokenId,
     data_params
)  {

    Utils.log('_ownerOf(tokenId): (' + _ownerOf(tokenId) + ').');
    Utils.log('from: (' + from + ').');

    Utils.assert(Utils.addressCheck(from) , "DNA721: transfer params: from is invalid bid address");
    Utils.assert(Utils.addressCheck(to) , "DNA721: transfer params: to is invalid bid address");
    Utils.assert(Utils.addressCheck(tokenId) , "DNA721: transfer params: tokenId is invalid bid address");

    Utils.assert(_ownerOf(tokenId) === from, "DNA721: transfer from incorrect owner");

    _approve('', tokenId);

    var balances = {}; 
	var fromIndex=hashCode(from);
    var data = JSON.parse(Chain.load(BALANCEOF+'_'+fromIndex));
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
    var index=hashCode(tokenId);
    var tokens = {};
    var dataToken = JSON.parse(Chain.load(TOKENS+'_'+index));
    if (dataToken) {
        tokens = dataToken;
    }

    tokens[tokenId] = to;

    Chain.store(BALANCEOF+'_'+fromIndex, JSON.stringify(balances));
    Chain.store(TOKENS+'_'+index, JSON.stringify(tokens));

    // for enumeration
    _removeTokenFromOwnerEnumeration(from, tokenId);
    _addTokenToOwnerEnumeration(to, tokenId);

    Chain.tlog('Transfer', from, to, tokenId);
}

function _isApprovedOrOwner(spender, tokenId)  {

    Utils.log("_exists(tokenId): " + _exists(tokenId));
    Utils.assert(_exists(tokenId), "DNA721: operator query for nonexistent token");

    var owner = _ownerOf(tokenId);
    Utils.log("owner: " + owner);
    Utils.log("_getApproved(tokenId): " + _getApproved(tokenId));
    Utils.log("_isApprovedForAll(owner, spender): " + _isApprovedForAll(owner, spender));
    return (spender === owner && (_getApproved(tokenId) === spender || _isApprovedForAll(owner, spender)));
}

function approve( params )  {

    var input = params; // to,  tokenId

    Utils.assert(Utils.addressCheck(input.to), "DNA721: approve params: to is invalid bid address");
    Utils.assert(Utils.addressCheck(input.tokenId), "DNA721: approve params: tokenId is invalid bid address");

    var owner = _ownerOf(input.tokenId);
    Utils.assert(input.to !== owner, "DNA721: approval to current owner");
    Utils.log("approve-sender_g:" + sender_g + "  owner:" + owner);
    Utils.assert(
        sender_g === owner || _isApprovedForAll(owner, sender_g),
        "DNA721: approve caller is not owner nor approved for all"
    );

    _approve(input.to, input.tokenId);
}

function transferFrom(params) {

    var input = params; // from、to、tokenId
    
    Utils.assert(_isApprovedOrOwner(sender_g, input.tokenId), "DNA721: transfer caller is not owner nor approved");

    _transfer(input.from, input.to, input.tokenId, "");
}

function safeTransferFrom(params) {

    var from = params.from; // from
    var to = params.to; // to
    var tokenId = params.tokenId; // tokenId
    var data = params.data; // data

    // safe check

    // _transfer
    Utils.assert(_isApprovedOrOwner(sender_g, tokenId), "DNA721: transfer caller is not owner nor approved");
    _transfer(from, to, tokenId, data);
}


// enumeration
// return int
function totalSupply() {
    
    var allTokens; 
    var dataAll = JSON.parse(Chain.load(ALLTOKENS));
    if (dataAll) {
        allTokens = dataAll;
    }
    return allTokens;
}

// return tokenId -> address
function tokenByIndex(params) {
    var index = params.index;
    
    Utils.assert(index%1 === 0, "DNA721 tokenByIndex: your index should be int");
    Utils.assert(index >= 0, "DNA721 tokenByIndex: your index <= 0");
    Utils.assert(index < totalSupply(), "DNA721 tokenByIndex: global index out of bounds");

    var allTokens; 
    var dataAll = JSON.parse(Chain.load(ALLTOKENS+'_'+index));
    if (dataAll) {
        allTokens = dataAll;
    }
    return allTokens;
}

// return tokenId -> address
function tokenOfOwnerByIndex(params) {
    var owner = params.owner;
    var index = params.index;
	var ownerIndex=hashCode(owner);
    Utils.assert(index%1 === 0, "DNA721 tokenOfOwnerByIndex: your index should be int");
    Utils.assert(Utils.addressCheck(owner) , "DNA721: tokenOfOwnerByIndex params: owner is invalid bid address");
    Utils.assert(index >= 0, "DNA721 tokenOfOwnerByIndex: your index <= 0");
    Utils.assert(index < balanceOf(params), "DNA721 Enumerable: owner index out of bounds"); // 注意：使用 params
    var ownedTokens = {}; 
    var data = JSON.parse(Chain.load(OWNEDTOKENS+'_'+ownerIndex));
    if (data) {
        ownedTokens = data;
    }
    return ownedTokens[owner][index];
}

function main(input_str){
    var input = JSON.parse(input_str);

    if(input.method === 'mint'){
        mint(input.params);
    }
    else if(input.method === 'transferFrom'){
        transferFrom(input.params);
    }else if(input.method === 'safeTransferFrom'){
        safeTransferFrom(input.params);
    }else if(input.method === 'approve') {
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
    if(input.method === 'name'){
        object = name();
    }else if(input.method === 'symbol'){
        object = symbol();
    }else if(input.method === 'tokenURI'){
        object = tokenURI(input.params);
    }else if(input.method === 'totalSupply'){
        object = totalSupply();
    }else if(input.method === 'tokenByIndex'){
        object = tokenByIndex(input.params);
    }else if(input.method === 'tokenOfOwnerByIndex'){
        object = tokenOfOwnerByIndex(input.params);
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

## 工业互联网标识合约

本节描述通过星火链网实现并部署工业互联网标识智能合约。

工业互联网标识映射的信息资源是具有唯一性的功能，对比传统互联网的DNS功能作用，可以通过标识代表映射具体某资源，而星火链工业互联网标识合约是基于星火链网主链，将各顶级GHR、二级SHR以及企业LHS的数据维护在主链账本中，通过自主身份体系和BID，实现对其所辖数据的自管理。

### 合约说明

标识合约是由JavaScript语言开发，在链上由V8虚拟机引擎解释执行。

标识合约有GHR（顶级节点），SHR（二级节点），LHS（企业节点）三种类型，在链上部署合约后即生成对应的合约账户，用户就可以根据合约接口分别进行注册，修改，删除以及查询的操作，其中注册，修改以及删除操作需要有白名单权限才可以操作，所以必须在部署发行到链上后，先进行白名单设置在进行后续接口调用操作。

+ 合约接口说明

| 合约函数          | 说明       |
| ----------------- | ---------- |
| createZidData     | 创建标识   |
| modifyZidData     | 修改标识   |
| queryZidRecord    | 查询标识   |
| removeZidData     | 删除标识   |
| setAuditWhitelist | 设置白名单 |

+ **合约示例**

```
'use strict';


//ZID  data操作
const ZidOp = {
    'INS'                : '0',      //insert
    'DEL'                : '1',      //delete
    'MOD'                : '2',       //modify
	'QUERY'				 : '3'       //query
};

const ZID_RECORD_PRE = 'zidrecord';
const GHR_ZID_INIT = 'ghr_zid_init';
const SHR_ZID_INIT = 'shr_zid_init';
const LHS_ZID_INIT = 'lhs_zid_init';

/*
    ***********************************
                事件定义
    ***********************************
*/
//白名单设置
const TLOG_SET_WT = 'tlog_set_wt';

//创建标识事件
const TLOG_ZID_CREATE_CONTRACT_ADDRESS = 'tlog_zid_create_contract_address';

//修改标识事件
const TLOG_ZID_MODIFY_CONTRACT_ADDRESS = 'tlog_zid_modify_contract_address';

//删除标识事件
const TLOG_ZID_REMOVE_CONTRACT_ADDRESS = 'tlog_zid_remove_contract_address';


/*
    ***********************************
                权限控制
    ***********************************
*/
function isValidator(addr){
    return Chain.isValidator(addr);
}

function getWhiteKey(addr){
    return 'wk-' + addr;
}
  
function checkInAuditWhitelist(addr) {
    const res = Chain.load(getWhiteKey(addr));
    return res !== false;
}

function getKey(first, second, third = ''){
    return (third === '') ? (first + '_' + second) : (first + '_' + second + '_' + third);
}

function loadObj(key){
	let data = Chain.load(getKey(ZID_RECORD_PRE,key));
	return JSON.parse(data);
}

/* 
    函数名称：setAuditWhitelist()
    函数描述：白名单注册接口；该接口需要验证者账户调用
    调用方式：main
    参数：
        caller_address         待操作白名单账户
        addFlag         操作
    返回值：无
*/
function setAuditWhitelist(paramObj) {
    Utils.assert(paramObj.caller_address !== undefined, 'Param obj has no caller_address');
    Utils.assert(paramObj.addFlag !== undefined, 'Param obj has no addFlag');

    Utils.assert(Utils.addressCheck(paramObj.caller_address), `The caller_address(${paramObj.caller_address}) is invalid`);
    Utils.assert(typeof paramObj.addFlag === 'boolean', `The addFlag(${paramObj.addFlag}) is invalid`);

    //isValidator check
    Utils.assert(isValidator(Chain.msg.sender), `The caller_address(${Chain.msg.sender}) is not validator`);
    
    if (paramObj.addFlag === true) {
        Utils.assert(loadObj(getWhiteKey(paramObj.caller_address)) === false, `The account(${paramObj.caller_address}) is already in whitelist`);
        Chain.store(getWhiteKey(paramObj.caller_address), '');
    } else {
        Chain.del(getWhiteKey(paramObj.caller_address));
    }

    Chain.tlog(TLOG_SET_WT, Chain.msg.sender, paramObj.caller_address, `${paramObj.addFlag}`);
}

function createZidValue(key, value){
    Chain.store(getKey(ZID_RECORD_PRE, key), JSON.stringify(value));
}

function deleteZidValue(key){
    Chain.del(getKey(ZID_RECORD_PRE,key));
}

function modifyZidValue(key, value) {
    deleteZidValue(key);
    createZidValue(key, value);
} 

function queryZidRecord(paramObj){
    Utils.assert(paramObj.zid !== undefined, 'Param obj has no zid');
	
    return loadObj(paramObj.zid);
}
/* 
    函数名称：createZidData()
    函数描述：创建标识;

    调用方式：main
    参数：
        zid             标识
        value        	标识值数组
		index			标识值索引
		type			标识类型
		data			标识数据结构
		format			数据格式
		value			标识值
		ttl				ttl值
		ttlType			ttl类型
		timestamp		时间戳
		references		引用
		adminRead		管理员可读
		adminWrite		管理员可写
		publicRead		公共可读
		publicWrite		公共可写
    返回值：
        无
*/
function createZidData(paramObj) {
    //check param
    Utils.assert(paramObj.zid !== undefined, 'Param obj has no zid');
    Utils.assert(paramObj.value[0].index !== undefined, 'Param obj has no index');
    Utils.assert(paramObj.value[0].type !== undefined, 'Param obj has no type');
    Utils.assert(paramObj.value[0].data.format !== undefined, 'Param obj has no format');
	Utils.assert(paramObj.value[0].data.value !== undefined, 'Param obj has no data value');
	Utils.assert(paramObj.value[0].ttl !== undefined, 'Param obj has no ttl');
	Utils.assert(paramObj.value[0].ttlType !== undefined, 'Param obj has no ttl');
	Utils.assert(paramObj.value[0].timestamp !== undefined, 'Param obj has no timestamp');

    //检测操作权限
    Utils.assert(checkInAuditWhitelist(Chain.msg.sender), `The address(${Chain.msg.sender}) checkInAuditWhitelist error`);
	
	//判断对应zid是否已存在
	Utils.assert(loadObj(paramObj.zid) === false, 'createZidData exist of zid:' + paramObj.zid);
	
	let regiRecord = {  
	    'value': [{
		'index': paramObj.value[0].index,
		'type': paramObj.value[0].type,
		'data': {
			'format': paramObj.value[0].data.format,
			'value': paramObj.value[0].data.value
		},
		'ttl': paramObj.value[0].ttl,
		'ttlType': paramObj.value[0].ttlType,
		'timestamp': paramObj.value[0].timestamp,
		'references': paramObj.value[0].references,
		'adminRead': paramObj.value[0].adminRead,
		'adminWrite': paramObj.value[0].adminWrite,
		'publicRead': paramObj.value[0].publicRead,
		'publicWrite': paramObj.value[0].publicWrite
	}]
    };
	
    createZidValue(paramObj.zid, regiRecord);
	Chain.tlog(TLOG_ZID_CREATE_CONTRACT_ADDRESS, 'zid data record', 'create', paramObj.zid);
}

function removeZidData(paramObj) {
	//check param
	Utils.assert(paramObj.zid !== undefined, 'Param obj has no zid');
	if(paramObj.opFlag === ZidOp.DEL)
	{
		 //检测操作权限
		Utils.assert(checkInAuditWhitelist(Chain.msg.sender), `The address(${Chain.msg.sender}) checkInAuditWhitelist error`);
		
		deleteZidValue(paramObj.zid);
		Chain.tlog(TLOG_ZID_REMOVE_CONTRACT_ADDRESS, 'zid data record', 'remove', paramObj.zid);
	}
}

function modifyZidData(paramObj) {
	//check param
    Utils.assert(paramObj.zid !== undefined, 'Param obj has no zid');
	Utils.assert(paramObj.opFlag !== undefined, 'Param obj has no opFlag');
    Utils.assert(paramObj.value[0].index !== undefined, 'Param obj has no index');
    Utils.assert(paramObj.value[0].type !== undefined, 'Param obj has no type');
    Utils.assert(paramObj.value[0].data.format !== undefined, 'Param obj has no format');
	Utils.assert(paramObj.value[0].data.value !== undefined, 'Param obj has no data value');
	Utils.assert(paramObj.value[0].ttl !== undefined, 'Param obj has no ttl');
	Utils.assert(paramObj.value[0].ttlType !== undefined, 'Param obj has no ttl');
	Utils.assert(paramObj.value[0].timestamp !== undefined, 'Param obj has no timestamp');
	
    //检测操作权限
    Utils.assert(checkInAuditWhitelist(Chain.msg.sender), `The address(${Chain.msg.sender}) checkInAuditWhitelist error`);
	
	//判断对应zid是否已存在
	Utils.assert(loadObj(paramObj.zid) === false, 'modifyZidData exist of zid:' + paramObj.zid);
	if(paramObj.opFlag === ZidOp.MOD)
	{
		let modifyRecord = {  
	    'value': [{
		'index': paramObj.value[0].index,
		'type': paramObj.value[0].type,
		'data': {
			'format': paramObj.value[0].data.format,
			'value': paramObj.value[0].data.value
		},
		'ttl': paramObj.value[0].ttl,
		'ttlType': paramObj.value[0].ttlType,
		'timestamp': paramObj.value[0].timestamp,
		'references': paramObj.value[0].references,
		'adminRead': paramObj.value[0].adminRead,
		'adminWrite': paramObj.value[0].adminWrite,
		'publicRead': paramObj.value[0].publicRead,
		'publicWrite': paramObj.value[0].publicWrite
		}]
		};
	
		modifyZidValue(paramObj.zid, modifyRecord);
		Chain.tlog(TLOG_ZID_MODIFY_CONTRACT_ADDRESS, 'zid data record', 'modify', paramObj.zid);
		
	}
}
/*
    ***********************************
                调用入口
    ***********************************
*/

function init(input){
	let inputObj = JSON.parse(input);
    if (inputObj.type === GHR_ZID_INIT){
        Chain.store(GHR_ZID_INIT, 'TRUE');
    }
	else if(inputObj.type === SHR_ZID_INIT)
	{
		Chain.store(SHR_ZID_INIT, 'TRUE');
	}
    else if(inputObj.type === LHS_ZID_INIT)
	{
		Chain.store(LHS_ZID_INIT, 'TRUE');
	}
    return;
}

function main(input){
    let funcList = {
        //验证者账户设置白名单
        'setAuditWhitelist' : setAuditWhitelist,
        //标识功能接口
        'createZidData' : createZidData,
        'modifyZidData' : modifyZidData,
        'removeZidData' : removeZidData
    };
    let inputObj = JSON.parse(input);
    Utils.assert(funcList.hasOwnProperty(inputObj.method) && typeof funcList[inputObj.method] === 'function', 'Cannot find func:' + inputObj.method);
    funcList[inputObj.method](inputObj.params);
}

function query(input){
    let result = {};
    let inputObj = JSON.parse(input);
    if (inputObj.method === 'queryZidRecord'){
        result = queryZidRecord(inputObj.params);
    }
    return JSON.stringify(result);
}
```

### 5.4.3 合约部署

运行链节点服务之后就可以部署合约到链上，生成对应的合约账户，合约账户可以后续进行合约管理，部署合约是通过调用SDK接口。

+ **GHR合约部署**

```
// 初始化参数
String senderAddress = "did:bid:efuEAGFPJMsojwPGKzjD8vZX1wbaUrVV";
String senderPrivateKey = "priSPKnDue7AJ42gt7acy4AVaobGJtM871r1eukZ2M6eeW5LxG";
//ghr合约压缩后的代码
String payload = "'use strict';const ZidOp=				{'INS':'0','DEL':'1','MOD':'2','QUERY':'3'};const    ZID_RECORD_PRE='zidrecord';const GHR_ZID_INIT='ghr_zid_init';const TLOG_SET_WT='tlog_set_wt';";
Long initBalance = ToBaseUnit.ToUGas("0.01");

BIFContractCreateRequest request = new BIFContractCreateRequest();
request.setSenderAddress(senderAddress);
request.setPrivateKey(senderPrivateKey);
request.setInitBalance(initBalance);
request.setPayload(payload);
request.setInitInput("{\"type\":\"ghr_zid_init\"}");
request.setMetadata("create ghr contract");

// 调用BIFContractCreate接口
BIFContractCreateResponse response = sdk.getBIFContractService().contractCreate(request);
if (response.getErrorCode() == 0) {
    System.out.println(JSON.toJSONString(response.getResult(), true));
} else {
    System.out.println("error:      " + response.getErrorDesc());
}
```

其中`payload`参数即是对应合约源码压缩后的值，`input`参数里的类型填写对应的类型值即可。

合约部署完后返回对应的hash值，可以根据hash查询对应详细交易信息。

+ **SHR合约部署**

只需要将`setInitInput`的合约类型换成SHR的即可。

```
// 初始化参数
String senderAddress = "did:bid:efuEAGFPJMsojwPGKzjD8vZX1wbaUrVV";
String senderPrivateKey = "priSPKnDue7AJ42gt7acy4AVaobGJtM871r1eukZ2M6eeW5LxG";
//shr合约压缩后的代码
String payload = "'use strict';const ZidOp=				{'INS':'0','DEL':'1','MOD':'2','QUERY':'3'};const    ZID_RECORD_PRE='zidrecord';const GHR_ZID_INIT='shr_zid_init';const TLOG_SET_WT='tlog_set_wt';";
Long initBalance = ToBaseUnit.ToUGas("0.01");

BIFContractCreateRequest request = new BIFContractCreateRequest();
request.setSenderAddress(senderAddress);
request.setPrivateKey(senderPrivateKey);
request.setInitBalance(initBalance);
request.setPayload(payload);
request.setInitInput("{\"type\":\"shr_zid_init\"}");
request.setMetadata("create shr contract");

// 调用BIFContractCreate接口
BIFContractCreateResponse response = sdk.getBIFContractService().contractCreate(request);
if (response.getErrorCode() == 0) {
    System.out.println(JSON.toJSONString(response.getResult(), true));
} else {
    System.out.println("error:      " + response.getErrorDesc());
}
```

合约部署完后返回对应的hash值，可以根据hash查询对应详细交易信息。

+ **LHS合约部署**

​		只需要修改`setInitInput`的合约类型值即可。

```
// 初始化参数
String senderAddress = "did:bid:efVmotQW28QDtQyupnKTFvpjKQYs5bxf";
String senderPrivateKey = "priSPKnDue7AJ42gt7acy4AVaobGJtM871r1eukZ2M6eeW5LxG";
//lhs合约压缩后代码
String payload = "'use strict';const ZidOp=				{'INS':'0','DEL':'1','MOD':'2','QUERY':'3'};const    ZID_RECORD_PRE='zidrecord';const GHR_ZID_INIT='shr_zid_init';const TLOG_SET_WT='tlog_set_wt';";
Long initBalance = ToBaseUnit.ToUGas("0.01");

BIFContractCreateRequest request = new BIFContractCreateRequest();
request.setSenderAddress(senderAddress);
request.setPrivateKey(senderPrivateKey);
request.setInitBalance(initBalance);
request.setPayload(payload);
request.setInitInput("{\"type\":\"lhs_zid_init\"}");
request.setMetadata("create lhs contract");

// 调用BIFContractCreate接口
BIFContractCreateResponse response = sdk.getBIFContractService().contractCreate(request);
if (response.getErrorCode() == 0) {
    System.out.println(JSON.toJSONString(response.getResult(), true));
} else {
    System.out.println("error:      " + response.getErrorDesc());
}
```

​		合约部署完后返回对应的hash值，可以根据hash查询对应详细交易信息。

### 5.4.4 合约调用

+ **设置白名单**

```
// 初始化参数
String senderAddress = "did:bid:efVmotQW28QDtQyupnKTFvpjKQYs5bxf";
String contractAddress = "did:bid:ef2gAT82SGdnhj87wQWb9suPKLbnk9NP";
String senderPrivateKey = "priSPKnDue7AJ42gt7acy4AVaobGJtM871r1eukZ2M6eeW5LxG";
Long amount = 0L;

BIFContractInvokeByGasRequest request = new BIFContractInvokeByGasRequest();
request.setSenderAddress(senderAddress);
request.setPrivateKey(senderPrivateKey);
request.setContractAddress(contractAddress);
request.setBIFAmount(amount);
request.setMetadata("contract set whiteList invoke");
request.setInput("{\"method\":\"setAuditWhitelist\",\"params\":{\"caller_address\": \"did:bid:efuEAGFPJMsojwPGKzjD8vZX1wbaUrVV\",\"addFlag\":true}}");

// 调用 BIFContractInvoke 接口
BIFContractInvokeByGasResponse response = sdk.getBIFContractService().contractInvoke(request);
if (response.getErrorCode() == 0) {
    System.out.println(JSON.toJSONString(response.getResult(), true));
} else {
    System.out.println("error:      " + response.getErrorDesc());
}
```

​		白名单设置和其他交易不同在于，源账户是由验证者账户触发的（必须时验证者账户否则报错），合约账户就是对应GHR，SHR以及LHS各自的合约地址，私钥就是验证者账户对应的，然后input合约函数以及参数都是GHR，SHR以及LHS对应里具体的值，然后初始化填充后调用接口发送即可将各个合约地址加入到白名单，以方便后续的管理操作。

+ **标识创建**

```
// 初始化参数
String senderAddress = "did:bid:efVmotQW28QDtQyupnKTFvpjKQYs5bxf";
String contractAddress = "did:bid:ef2gAT82SGdnhj87wQWb9suPKLbnk9NP";
String senderPrivateKey = 	"priSPKnDue7AJ42gt7acy4AVaobGJtM871r1eukZ2M6eeW5LxG";
Long amount = 0L;

BIFContractInvokeByGasRequest request = new BIFContractInvokeByGasRequest();
request.setSenderAddress(senderAddress);
request.setPrivateKey(senderPrivateKey);
request.setContractAddress(contractAddress);
request.setBIFAmount(amount);
request.setMetadata("contract create zid invoke");
request.setInput("{\"method\":\"createZidData\",\"params\": {\n" +
        "\t\t\"zid\": \"88.1000\",\n" +
        "\t\t\"opFlag\": \"0\",\n" +
        "\t\t\"value\": [{\n" +
        "\t\t\t\"index\": \"1\",\n" +
        "\t\t\t\"type\": \"contract_address\",\n" +
        "\t\t\t\"data\": {\n" +
        "\t\t\t\t\"format\": \"string\",\n" +
        "\t\t\t\t\"value\": 		\"did:bid:efuEAGFPJMsojwPGKzjkkk89jky\"\n" +
        "\t\t\t},\n" +
        "\t\t\t\"ttl\": \"86400\",\n" +
        "\t\t\t\"ttlType\": \"0\",\n" +
        "\t\t\t\"timestamp\": \"0\",\n" +
        "\t\t\t\"references\": [],\n" +
        "\t\t\t\"adminRead\": \"1\",\n" +
        "\t\t\t\"adminWrite\": \"1\",\n" +
        "\t\t\t\"publicRead\": \"1\",\n" +
        "\t\t\t\"publicWrite\": \"0\"\n" +
        "\t\t}]\n" +
        "\t}}");
// 调用 BIFContractInvoke 接口
BIFContractInvokeByGasResponse response = sdk.getBIFContractService().contractInvoke(request);
if (response.getErrorCode() == 0) {
    System.out.println(JSON.toJSONString(response.getResult(), true));
} else {
    System.out.println("error:      " + response.getErrorDesc());
}
```

​		zid标识在的value数据结构字段为：

| Value格式   | 参数含义                                                     | 是否必填 | 默认值 |
| ----------- | ------------------------------------------------------------ | -------- | ------ |
| method      | 标识创建的函数名                                             | 必填项   |        |
| index       | 标识值索引(最好不要用默认的0，从1开始递增创建)               | 必填项   |        |
| type        | 标识值类型(GHR和SHR创建的都为contract_address)               | 必填项   |        |
| data        | 包含有format以及value字段如下                                | 必填项   |        |
| format      | string类型                                                   | 必填项   |        |
| value       | 标识值数据(GHR和SHR的为具体合约地址)                         |          |        |
| ttl         | 标识超时时间                                                 |          | 86400s |
| ttlType     | 标识超时类型                                                 |          | 0      |
| timestamp   | 时间戳                                                       |          | 0      |
| References  | 包含zid以及index字段如下                                     |          | 选填   |
| zid         | 引用的标识名称，引用标识和index一一对应，可以是多个，可以没有引用其他标识 |          | 空     |
| opFlag      | 标识操作标志 ，值0是创建，1是删除，2是修改，3是查询          |          | 0      |
| index       | 引用的标识索引值(所引用handle的index不能为0)                 |          | 空     |
| adminRead   | 标识管理员可读,1可读 0不可读                                 |          | 1      |
| adminWrite  | 标识管理员可写，1可写 0不可写                                |          | 1      |
| publicRead  | 标识公共可读，1可读 0不可读                                  |          | 1      |
| publicWrite | 标识公共可写，1可写 0不可写                                  |          | 0      |

​		标识创建调用接口时，每次只需修改contract_address的值为各自合约的账户地址，以及合约函数名,参数等数据。

​		创建接口执行完之后，根据生成的hash调用getTransactionInfo交易记录接口查询对应的交易是否成功情况。

+ **标识修改**

​		标识修改接口和标识创建章节中的接口和参数一样，只需要修改对应的`input`的parames中对应合约修改函数及参数以及标识value的各字段值即可。

+ **标识删除**

```
// 初始化参数
String senderAddress = "did:bid:efVmotQW28QDtQyupnKTFvpjKQYs5bxf";
String contractAddress = "did:bid:ef2gAT82SGdnhj87wQWb9suPKLbnk9NP";
String senderPrivateKey = 	"priSPKnDue7AJ42gt7acy4AVaobGJtM871r1eukZ2M6eeW5LxG";
Long amount = 0L;

BIFContractInvokeByGasRequest request = new BIFContractInvokeByGasRequest();
request.setSenderAddress(senderAddress);
request.setPrivateKey(senderPrivateKey);
request.setContractAddress(contractAddress);
request.setBIFAmount(amount);
request.setMetadata("contract remove zid invoke");
request.setInput("{\"method\":\"removeZidData\",\"params\":	{\"zid\":\"88.1000\",\"type\":\"contract_address\",\"opFlag\": \"1\"}}");
// 调用 BIFContractInvoke 接口
BIFContractInvokeByGasResponse response = sdk.getBIFContractService().contractInvoke(request);
if (response.getErrorCode() == 0) {
    System.out.println(JSON.toJSONString(response.getResult(), true));
} else {
    System.out.println("error:      " + response.getErrorDesc());
}
```

​		标识删除接口与标识创建的核心参数基本相同，差异在input合约调用参数里，method字段为删除操作的合约函数名，params里是要删除的zid标识名，type标识类型（GHR, SHR是contract_address, LHS的是URL等类型）以及opFlag值（此处为1删除标志）。

### 5.4.5 合约查询

+ **标识查询**

​		Input合约参数说明：

​		method：对应合约的查询接口函数名（GHR的查询接口是queryZidRecord，SHR合约的是queryZidRecordShr，LHS的是queryZidRecordLhs）。

​		params：含有type类型参数(GHR以及SHR的是contract_address，LHS可以是URL或其他自定义类型)，以及对应zid名。

```
// 初始化请求参数
String contractAddress = "did:bid:ef2gAT82SGdnhj87wQWb9suPKLbnk9NP";
BIFContractCallRequest request = new BIFContractCallRequest();
request.setContractAddress(contractAddress);
//标识查询合约接口操作
request.setInput("{\"method\":\"queryZidRecord\",\"params\":{\"type\": \"contract_address\",\"zid\":\"88.1000\"}}");

// 调用contractQuery接口
BIFContractCallResponse response = sdk.getBIFContractService().contractQuery(request);
if (response.getErrorCode() == 0) {
    BIFContractCallResult result = response.getResult();
    System.out.println(JSON.toJSONString(result, true));
} else {
    System.out.println("error: " + response.getErrorDesc());
}
```

​		返回信息：

```
{
    "query_rets":[
        {
            "result":{
                "type":"string",
                "value":"{\"value\":[{\"index\":\"1\",\"type\":\"contract_address\",\"data\":{\"format\":\"string\",\"value\":\"did:bid:efuEAGFPJMsojwPGKzjkkk89888\"},\"ttl\":\"86400\",\"ttlType\":\"0\",\"timestamp\":\"0\",\"references\":[],\"adminRead\":\"1\",\"adminWrite\":\"1\",\"publicRead\":\"1\",\"publicWrite\":\"1\"}]}"
            }
        }
    ]
}
```

+ **查询账户信息**

​		标识合约操作的过程中可能需要查询账户详细信息，所以需要此接口。

```
// 待查询的账户地址
String accountAddress = "did:bid:efVmotQW28QDtQyupnKTFvpjKQYs5bxf";
BIFAccountGetInfoRequest request = new BIFAccountGetInfoRequest();
request.setAddress(accountAddress);

// 调用getAccount接口
BIFAccountGetInfoResponse response = sdk.getBIFAccountService().getAccount(request);

if (response.getErrorCode() == 0) {
    System.out.println(JSON.toJSONString(response.getResult(), true));
} else {
    System.out.println("error: " + response.getErrorDesc());
}
```

+ **查询交易信息**

​		标识合约创建，修改等接口操作后，需要根据生成的hash查询交易是否成功等信息，故需要此接口查询。

```
// 初始化请求参数
String txHash = "1653f54fbba1134f7e35acee49592a7c29384da10f2f629c9a214f6e54747705";
BIFTransactionGetInfoRequest request = new BIFTransactionGetInfoRequest();
request.setHash(txHash);

// 调用getBIFInfo接口
BIFTransactionGetInfoResponse response = sdk.getBIFTransactionService().getTransactionInfo(request);
if (response.getErrorCode() == 0) {
    System.out.println(JSON.toJSONString(response.getResult(), true));
} else {
    System.out.println("error: " + response.getErrorDesc());
}
```

​		返回信息：

```
{
	"total_count":1,
	"transactions":[{
		"actual_fee":"477",
		"close_time":1630760729249135,
		"contract_tx_hashes": ["82411f9cd3a1fd820285a426bf43142925273b2e9522dc836ad7185f548500a0"],
		"error_code":0,
		"error_desc":"",
		"hash":"b4495e6c124ea6d4c5c7094a687b8dd73bf85f7ac5f4805577c27fad56af912c",
		"ledger_seq":22656,
		"signatures":[{
     	"public_key":"b0656669660116b0b2ddfbba3f155962b311dc0afb671e2da069563a70fccabd9ff8c4",
            "sign_data":"7bfaa7c625619ddfd9a73c945f3231a21583c75b0d30b0c814dea43debace471edfb2485168429cadae30411b67996331e088ee9ae9636b593693f21c951b902"
        }],
        "transaction":{
			"fee_limit":1000000,
			"gas_price":1,
			"metadata":"contract ",
			"nonce":55,
			"operations":[{
				"pay_coin":{
					"amount":1000,
					"dest_address":"did:bid:efw8T4pMic9goJHe2FCNocaCb8AkDr3P",
					"input":"{\"method\":\"removeZidData\",\"params\":{\"zid\":\"88.1000\",\"type\":\"contract_address\",\"opFlag\": \"1\"}}"
				},
				"type":7
			}],
			"source_address":"did:bid:efuEAGFPJMsojwPGKzjD8vZX1wbaUrVV"
		},
		"tx_size":353
	}]
}
```

### 
