# 3.BID文档

`BID`文档就是用于描述身份详细信息的文档，一个`BID`标识符关联到一个`BID`文档。`BID`标识符具体解析为`BID`文档，`BID`文档内包括`BID`标识符和公钥详细信息(持有者、加密算法、密钥状态等)，以及`BID`持有者的其他非隐私属性描述等。

## 3.1 规范

BID的协议元数据为BID文档。BID文档遵循DID Document规范，并在之基础上做了一定的扩展。BID文档字段说明如下：

* @context：必填字段。一组解释JSON-LD文档的规则,遵循DID规范，用于实现不同DID Document的互操作，必须包含 https://www.w3.org/ns/did/v1。

* version：必填字段。文档的版本号，用于文档的版本升级。

* id：必填字段。文档的BID。

* publicKey：选填字段。一组公钥，包含id，type，controller,publicKeyHex四个字段，凭证类的BID文档不包含该字段。

  * id:公钥的ID。
  * type：字符串，代表公钥的加密算法类型，具体支持的类型见附录公钥类型章节。
  * controller：一个BID,表明此公钥的归属。
  * publicKeyHex：公钥的十六进制编码。

* authentication：必填字段。一组公钥的BID，表名此BID的归属，拥有此公钥对应私钥的一方可以控制和管理此BID文档。

* alsoKnownAs。选填字段。一组和本BID关联的其他ID, 包括type和id两个字段。

  * type:关联标识的类型,取值详见附录关联标识类型。
  * id:关联的标识。

* extension：BID扩展字段。包含如下字段：

  * recovery：选填字段。一组公钥id, 在authentication 私钥泄漏或者丢失的情况下用来恢复对文档的控制权。
  * ttl: 必填字段。Time-To-Live，即如果解析使用缓存的话缓存生效的时间，单位秒。
  * delegateSign: 选填字段。第三方对publicKey的签名，可信解析使用。包括：signer和signatureValue。

    * signer ：签名者，这里是一个公钥的id。
    * signatureValue: 使用相应私钥对publicKey字段的签名。
  * type: 必填字段。BID文档的属性类型，取值见附录属性类型。

* attributes: 必填字段。一组属性，属性为如下结构：

  | 字段名  | 描述                                        |
  | ------- | ------------------------------------------- |
  | key     | 属性的关键字                                |
  | desc    | 选填。属性描述                              |
  | encrypt | 选填。是否加密，0非加密，1加密              |
  | format  | 选填。image、text、video、mixture等数据类型 |
  | value   | 选填。属性自定义value                       |

* acsns:选填字段。一组子链AC号，只有BID文档类型不是凭证类型且文档是主链上的BID文档才可能有该字段，存放当前BID拥有的所有AC号。

* verifiableCredentials:选填字段。凭证列表，包含id和type两个字段。

  * id:可验证声明的BID。
  * type：凭证类型。详见附录凭证类型。

* service：选填字段。一组服务地址，包括id，type，serviceEndpoint三个必填字段。

  * id: 服务地址的ID。

  * type：字符串，代表服务的类型。取值见附录服务类型。

  * serviceEndpoint：一个URI地址。

    当type为子链解析服务时， service为以下结构：

    | 字段名          | 描述                                                       |
    | --------------- | ---------------------------------------------------------- |
    | id              | 服务地址的ID                                               |
    | type            | DIDSubResolver                                             |
    | version         | 服务支持的BID解析协议版本                                  |
    | protocol        | 解析协议支持的传输协议类型, 具体取值见附录解析服务协议类型 |
    | serverType      | 服务地址类型，0为域名形式，1为IP地址形式                   |
    | serviceEndpoint | 解析地址的IP或域名                                         |
    | port            | serverType为1时有该字段，解析服务的端口号                  |

* created：必填字段。创建时间。

* updated：必填字段。上次的更新时间。

* proof：选填字段。文档所有者对文档内容的签名，包括：creator和signatureValue。

  * creator：proof的创建者，这里是一个公钥的id。
  * signatureValue：使用相应私钥对除proof字段的整个BID文档签名。

## 3.2 元数据示例

```json
{
	"@context": ["https://www.w3.org/ns/did/v1"],
	"version": "1.0.0",
	"id": "did:bid:efnVUgqQFfYeu97ABf6sGm3WFtVXHZB2",
	"publicKey": [{
		"id": "did:bid:efnVUgqQFfYeu97ABf6sGm3WFtVXHZB2#key-1",
		"type": "Ed25519",
		"controller": "did:bid:efnVUgqQFfYeu97ABf6sGm3WFtVXHZB2",
		"publicKeyHex": "b9906e1b50e81501369cc777979f8bcf27bd1917d794fa6d5e320b1ccc4f48bb"
	}, {
		"id": "did:bid:efnVUgqQFfYeu97ABf6sGm3WFtVXHZB2#key-2",
		"type": "Ed25519",
		"controller": "did:bid:efnVUgqQFfYeu97ABf6sGm3WFtVXHZB2",
		"publicKeyHex": "31c7fc771eba5b511b7231e9b291835dd4ebde51cc0e757a84464e7582aba652"
	}],
	"authentication": ["did:bid:efnVUgqQFfYeu97ABf6sGm3WFtVXHZB2#key-1"],
	"extension": {
		"recovery": ["did:bid:efnVUgqQFfYeu97ABf6sGm3WFtVXHZB2#key-2"],
		"ttl": 86400,
		"delegateSign ": {
			"signer": "did:bid:efJgt44mNDewKK1VEN454R17cjso3mSG#key-1",
			"signatureValue": "eyJhbGciOiJSUzI1NiIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19"
		},
		"type": 206
	},
	"service": [{
		"id": "did:bid:ef24NBA7au48UTZrUNRHj2p3bnRzF3YCH#subResolve",
		"type": "DIDSubResolve",
		"version": "1.0.0",
		"serverType": 1,
		"protocol": 3,
		"serviceEndpoint": "192.168.1.23",
		"port": 8080
	}],
	"created": "2021-05-10T06:23:38Z",
	"updated": "2021-05-10T06:23:38Z",
	"proof": {
		"creator": "did:bid:efJgt44mNDewKK1VEN454R17cjso3mSG#key-1",
		"signatureValue": "9E07CD62FE6CE0A843497EBD045C0AE9FD6E1845414D0ED251622C66D9CC927CC21DB9C09DFF628DC042FCBB7D8B2B4901E7DA9774C20065202B76D4B1C15900"
	}
}
```
