# 鎺ュ彛瀹氫箟鏂囨。锛堢粓绋匡級

鏈€鍚庢洿鏂帮細2026-03-14

## 1. 鏂囨。瀹氫綅

- 涓?API 鏂囨。锛歚docs/support_api.md`
- 璁㈠崟鐘舵€佽ˉ鍏呮枃妗ｏ細`src/backend/docs/order_status.md`

> 鏈枃妗ｆ寜褰撳墠鍚庣浠ｇ爜瀹為檯瀹炵幇鏁寸悊锛屼究浜庡厛鑱旇皟銆佸啀缁嗗寲銆?

### 1.1 鎺ュ彛鐘舵€佹爣璁拌鏄?

- `宸插疄鐜癭锛氬悗绔矾鐢卞凡鍙皟鐢紝鍙洿鎺ヨ仈璋冦€?
- `瑙勫垝鎺ュ彛`锛氱敤浜庡墠鍚庣瀵归綈鐨勫绾﹀畾涔夛紝褰撳墠鍚庣灏氭湭涓婄嚎銆?

褰撳墠鏂囨。涓殑鐢ㄦ埛璁よ瘉銆佸湴鍧€銆佽喘鐗╄溅銆佷笅鍗曠‘璁ゃ€佸垱寤鸿鍗曘€佹敮浠樸€佸鏈嶇暀瑷€涓?`宸插疄鐜癭锛?
璁㈠崟鍙戣揣銆佺‘璁ゆ敹璐с€佸晢鍝佷笌鍒嗙被鍏紑鎺ュ彛涓?`瑙勫垝鎺ュ彛`銆?

## 2. 閫氱敤绾﹀畾

### 2.1 鍩虹璺緞

- 璐墿杞︼細`/api/cart/`
- 璁㈠崟锛歚/api/orders/`
- 鏀粯锛堝綋鍓嶄唬鐮佺敓鏁堣矾寰勶級锛歚/api/paymentorders/<order_id>/pay/`
  - 璇存槑锛氬綋鍓嶄富璺敱涓?`path("api/payment", include("payment.urls"))`锛屽瓙璺敱涓?`orders/<order_id>/pay/`锛屾渶缁堜細琚?Django 鎸夊瓧绗︿覆鎷兼帴涓?`paymentorders`锛堟棤涓棿 `/`锛夈€?
  - 寤鸿锛氬悗缁皢涓昏矾鐢辫皟鏁翠负 `path("api/payment/", include("payment.urls"))`锛岃皟鏁村悗璺緞鍙鎬ф洿楂橈細`/api/payment/orders/<order_id>/pay/`銆?
- 瀹㈡湇锛歚/api/support/`
- 鐢ㄦ埛锛歚/api/users/`
- 鍟嗗搧锛歚/api/products/`锛堣鍒掍腑锛屾湭涓婄嚎锛?
- 鍒嗙被锛歚/api/categories/`锛堣鍒掍腑锛屾湭涓婄嚎锛?

### 2.2 閫氱敤鍝嶅簲缁撴瀯

```json
{
	"code": 0,
	"message": "success",
	"data": {}
}
```

- 鎴愬姛锛歚code=0`
- 澶辫触锛歚code=1`

### 2.3 閴存潈绾﹀畾

- 璁よ瘉鏂瑰紡锛歚JWT Bearer Token`
- 璇锋眰澶达細`Authorization: Bearer <access_token>`
- 榛樿鏉冮檺锛氬悗绔叏灞€ `IsAuthenticated`
- 鐧藉悕鍗曟帴鍙ｏ細鐢ㄦ埛娉ㄥ唽銆佺櫥褰曘€佸埛鏂?token锛坄AllowAny`锛?

### 2.4 鐘舵€佺爜绾﹀畾

#### HTTP 鐘舵€佺爜

- `200 OK`锛氳姹傛垚鍔燂紙涓氬姟鎴愬姛/涓氬姟澶辫触閮藉彲鑳借繑鍥烇紝闇€缁撳悎 `code` 鍒ゆ柇锛?
- `400 Bad Request`锛氬弬鏁版牎楠屽け璐?
- `401 Unauthorized`锛氭湭鐧诲綍銆乼oken 鏃犳晥/杩囨湡銆佺敤鎴峰悕瀵嗙爜閿欒
- `403 Forbidden`锛氬凡璁よ瘉浣嗘棤鏉冮檺锛堝綋鍓嶉儴鍒嗘帴鍙ｆ殏鏈崟鐙畾涔夛級
- `500 Internal Server Error`锛氭湇鍔＄寮傚父

#### 涓氬姟鐘舵€佺爜锛堝搷搴斾綋 `code`锛?

- `0`锛氫笟鍔℃垚鍔?
- `1`锛氫笟鍔″け璐?

### 2.5 閿欒鐮佽鑼冿紙琛ュ厖锛?

> 璇存槑锛氬綋鍓嶅悗绔ぇ閮ㄥ垎鎺ュ彛浠嶄娇鐢?`code=0/1`銆備互涓嬩负鍚庣画缁熶竴瑙勮寖锛岃仈璋冮樁娈靛彲鍏堟寜鈥滃吋瀹规ā寮忊€濊В鏋愩€?

#### 鍏煎妯″紡锛堝綋鍓嶅彲鐢級

- 鎴愬姛锛歚HTTP 200` 涓?`code=0`
- 澶辫触锛歚HTTP 4xx/5xx` 涓?`code=1`
- 鍓嶇鍏煎寤鸿锛氬厛鍒ゆ柇 HTTP 鐘舵€侊紝鍐嶅垽鏂?`code`锛屾渶鍚庤鍙?`message`銆?

#### 鐩爣妯″紡锛堝缓璁€愭钀藉湴锛?

| 鍖洪棿 | 妯″潡 | 璇存槑 |
|---|---|---|
| 0 | 閫氱敤 | 鎴愬姛 |
| 1000-1099 | Auth | 鐧诲綍銆乼oken銆佺敤鎴疯璇?|
| 2000-2199 | Product | 鍟嗗搧鐩稿叧 |
| 2200-2299 | Category | 鍒嗙被鐩稿叧 |
| 3000-3199 | Cart | 璐墿杞︾浉鍏?|
| 4000-4199 | Order | 璁㈠崟鐩稿叧 |
| 5000-5199 | Support | 瀹㈡湇鐣欒█鐩稿叧 |
| 9000-9099 | System | 绯荤粺绾у紓甯?|

寤鸿甯哥敤閿欒鐮侊細

| code | HTTP | message 绀轰緥 | 璇存槑 |
|---|---|---|---|
| 1001 | 401 | unauthorized | 鏈櫥褰曟垨 token 缂哄け |
| 1002 | 401 | token invalid | token 鏃犳晥鎴栬繃鏈?|
| 1003 | 401 | invalid credentials | 鐢ㄦ埛鍚嶆垨瀵嗙爜閿欒 |
| 2001 | 404 | product not found | 鍟嗗搧涓嶅瓨鍦?|
| 2002 | 400 | product is inactive | 鍟嗗搧宸蹭笅鏋?|
| 2201 | 404 | category not found | 鍒嗙被涓嶅瓨鍦?|
| 3001 | 400 | quantity must be greater than 0 | 璐拱鏁伴噺闈炴硶 |
| 3002 | 400 | insufficient stock | 搴撳瓨涓嶈冻 |
| 3003 | 400 | no selected cart items | 鏃犲嬀閫夊晢鍝?|
| 4001 | 400 | address_id is required | 鏀惰揣鍦板潃缂哄け |
| 4002 | 400 | order status invalid | 璁㈠崟鐘舵€佷笉鍏佽褰撳墠鎿嶄綔 |
| 5001 | 400 | content 蹇呭～ | 瀹㈡湇鐣欒█鍐呭涓虹┖ |
| 9000 | 500 | internal server error | 鏈嶅姟绔紓甯?|

## 3. 璐墿杞?API

### 3.1 鑾峰彇璐墿杞?

- 鏂规硶锛歚GET`
- 璺緞锛歚/api/cart/`
- 閴存潈锛?*鏄?*锛堥渶 Bearer Token锛?

璇锋眰浣擄細鏃?

鍝嶅簲浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呰繑 | 璇存槑 |
|---|---|---|---|
| code | int | 鏄?| 涓氬姟鐮侊紝`0` 鎴愬姛锛宍1` 澶辫触 |
| message | string | 鏄?| 鍝嶅簲娑堟伅 |
| data | object | 鏄?| 涓氬姟鏁版嵁 |
| data.items | array<object> | 鏄?| 璐墿杞﹂」鍒楄〃 |
| data.items[].id | int | 鏄?| 璐墿杞﹂」 ID |
| data.items[].product_id | int | 鏄?| 鍟嗗搧 ID |
| data.items[].title | string | 鏄?| 鍟嗗搧鏍囬 |
| data.items[].price | string(decimal) | 鏄?| 鍟嗗搧鍗曚环 |
| data.items[].quantity | int | 鏄?| 鏁伴噺 |
| data.items[].selected | bool | 鏄?| 鏄惁鍕鹃€?|
| data.items[].subtotal | string(decimal) | 鏄?| 褰撳墠椤瑰皬璁★紙`price * quantity`锛?|
| data.items[].stock | int | 鏄?| 鍟嗗搧搴撳瓨蹇収 |
| data.items[].is_active | bool | 鏄?| 鍟嗗搧鏄惁涓婃灦 |
| data.total_amount | string(decimal) | 鏄?| 鍕鹃€夊晢鍝佹€婚噾棰?|
| data.selected_count | int | 鏄?| 宸插嬀閫夊晢鍝侀」鏁?|
| data.item_count | int | 鏄?| 璐墿杞︽€婚」鏁?|

鐘舵€佺爜锛歚200/401`

鍝嶅簲绀轰緥锛?

```json
{
	"code": 0,
	"message": "success",
	"data": {
		"items": [
			{
				"id": 1,
				"product_id": 101,
				"title": "绀轰緥鍟嗗搧",
				"price": "99.00",
				"quantity": 1,
				"selected": true,
				"subtotal": "99.00",
				"stock": 100,
				"is_active": true
			}
		],
		"total_amount": "99.00",
		"selected_count": 1,
		"item_count": 1
	}
}
```

### 3.2 鍔犲叆璐墿杞?

- 鏂规硶锛歚POST`
- 璺緞锛歚/api/cart/items/`
- 閴存潈锛?*鏄?*锛堥渶 Bearer Token锛?

璇锋眰浣擄細

```json
{
	"product_id": 101,
	"quantity": 1
}
```

鏍￠獙锛?

- `product_id` 蹇呭～
- `quantity > 0`

璇锋眰浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呭～ | 璇存槑 |
|---|---|---|---|
| product_id | int | 鏄?| 鍟嗗搧 ID |
| quantity | int | 鍚?| 璐拱鏁伴噺锛岄粯璁?`1`锛屼笖蹇呴』 `> 0` |

鍝嶅簲浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呰繑 | 璇存槑 |
|---|---|---|---|
| code | int | 鏄?| 涓氬姟鐮?|
| message | string | 鏄?| 鎴愬姛鏃朵负 `item added` |
| data | object/null | 鏄?| 涓氬姟鏁版嵁 |
| data.item | object | 鍚?| 鏂板鎴栫疮鍔犲悗鐨勮喘鐗╄溅椤?|
| data.item.id | int | 鍚?| 璐墿杞﹂」 ID |
| data.item.product_id | int | 鍚?| 鍟嗗搧 ID |
| data.item.title | string | 鍚?| 鍟嗗搧鏍囬 |
| data.item.price | string(decimal) | 鍚?| 鍟嗗搧鍗曚环 |
| data.item.quantity | int | 鍚?| 褰撳墠鏁伴噺锛堝凡鍚疮鍔狅級 |
| data.item.selected | bool | 鍚?| 鏄惁鍕鹃€?|
| data.item.subtotal | string(decimal) | 鍚?| 褰撳墠椤瑰皬璁?|
| data.item.stock | int | 鍚?| 鍟嗗搧搴撳瓨 |
| data.item.is_active | bool | 鍚?| 鍟嗗搧鏄惁涓婃灦 |

鐘舵€佺爜锛歚200/400/401`

澶辫触鍦烘櫙锛堢ず渚嬶級锛?

- `product_id is required`
- `quantity must be an integer`
- `quantity must be greater than 0`
- `product is inactive`
- `insufficient stock`

### 3.3 鏇存柊璐墿杞﹂」

- 鏂规硶锛歚PATCH`
- 璺緞锛歚/api/cart/items/{item_id}/`
- 閴存潈锛?*鏄?*锛堥渶 Bearer Token锛?

璇锋眰浣擄紙鑷冲皯浼犱竴涓級锛?

```json
{
	"quantity": 2,
	"selected": true
}
```

璇锋眰浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呭～ | 璇存槑 |
|---|---|---|---|
| quantity | int | 鍚?| 鏇存柊鏁伴噺锛涘浼犲叆搴斾繚璇?`> 0` |
| selected | bool | 鍚?| 鏄惁鍕鹃€?|

鍝嶅簲浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呰繑 | 璇存槑 |
|---|---|---|---|
| code | int | 鏄?| 涓氬姟鐮?|
| message | string | 鏄?| 鎴愬姛鏃朵负 `item updated` |
| data | object/null | 鏄?| 涓氬姟鏁版嵁 |
| data.item | object | 鍚?| 鏇存柊鍚庣殑璐墿杞﹂」锛堢粨鏋勫悓 3.2锛?|

鐘舵€佺爜锛歚200/400/401`

澶辫触鍦烘櫙锛堢ず渚嬶級锛?

- `provide quantity or selected`
- `quantity must be an integer`
- `quantity must be greater than 0`
- `insufficient stock`

### 3.4 鍒犻櫎璐墿杞﹂」

- 鏂规硶锛歚DELETE`
- 璺緞锛歚/api/cart/items/{item_id}/`
- 閴存潈锛?*鏄?*锛堥渶 Bearer Token锛?

璇锋眰浣擄細鏃?

鍝嶅簲浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呰繑 | 璇存槑 |
|---|---|---|---|
| code | int | 鏄?| 涓氬姟鐮?|
| message | string | 鏄?| 鎴愬姛鏃朵负 `item deleted` |
| data | null | 鏄?| 鍥哄畾涓?`null` |

鐘舵€佺爜锛歚200/401`

### 3.5 璐墿杞﹀叏閫?鍏ㄤ笉閫?

- 鏂规硶锛歚PATCH`
- 璺緞锛歚/api/cart/select-all/`
- 閴存潈锛?*鏄?*锛堥渶 Bearer Token锛?

璇锋眰浣擄細

```json
{
	"selected": true
}
```

璇锋眰浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呭～ | 璇存槑 |
|---|---|---|---|
| selected | bool/string/int | 鏄?| 鏀寔 `true/false`銆乣1/0`銆乣yes/no` 绛夊彲杞竷灏斿€?|

鍝嶅簲浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呰繑 | 璇存槑 |
|---|---|---|---|
| code | int | 鏄?| 涓氬姟鐮?|
| message | string | 鏄?| 鎴愬姛鏃朵负 `select all updated` |
| data | object | 鏄?| 鏈€鏂拌喘鐗╄溅蹇収锛堢粨鏋勫悓 3.1锛?|

鐘舵€佺爜锛歚200/400/401`

澶辫触鍦烘櫙锛堢ず渚嬶級锛?

- `selected is required`

## 4. 璁㈠崟 API

### 4.0 璁㈠崟鐘舵€佹祦杞紙缁熶竴绾﹀畾锛?

褰撳墠妯″瀷鐘舵€佸€硷紙`orders.models.Order.STATUS_CHOICES`锛夛細

- `pending_payment`锛氬緟鏀粯
- `pending_shipment`锛氬緟鍙戣揣
- `pending_receipt`锛氬緟鏀惰揣
- `completed`锛氬凡瀹屾垚
- `cancelled`锛氬凡鍙栨秷

鎺ㄨ崘涓绘祦绋嬶細`pending_payment -> pending_shipment -> pending_receipt -> completed`

### 4.1 涓嬪崟纭锛堝凡瀹炵幇锛?

- 鏂规硶锛歚POST`
- 璺緞锛歚/api/orders/confirm/`
- 閴存潈锛?*鏄?*锛堥渶 Bearer Token锛?

璇锋眰浣擄細鏃?

璇存槑锛?

- 璇诲彇鈥滃綋鍓嶇敤鎴峰凡鍕鹃€夆€濈殑璐墿杞﹂」骞舵眹鎬婚噾棰濄€?
- 杩斿洖榛樿鍦板潃銆佸湴鍧€鍒楄〃銆佸嬀閫夊晢鍝佹槑缁嗐€侀噾棰濇眹鎬汇€?
- 鑻ュ嬀閫夊晢鍝佷负绌烘垨搴撳瓨/涓婃灦鐘舵€佸紓甯革紝杩斿洖澶辫触銆?

鍝嶅簲浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呰繑 | 璇存槑 |
|---|---|---|---|
| code | int | 鏄?| 涓氬姟鐮?|
| message | string | 鏄?| 鍝嶅簲娑堟伅 |
| data | object/null | 鏄?| 涓氬姟鏁版嵁 |
| data.default_address | object/null | 鍚?| 榛樿鍦板潃锛堝彲鑳戒负绌猴級 |
| data.addresses | array<object> | 鍚?| 鍦板潃鍒楄〃锛堟寜榛樿+鍊掑簭锛?|
| data.items | array<object> | 鍚?| 鍕鹃€夎喘鐗╄溅椤瑰垪琛?|
| data.items[].cart_item_id | int | 鍚?| 璐墿杞﹂」 ID |
| data.items[].product_id | int | 鍚?| 鍟嗗搧 ID |
| data.items[].title | string | 鍚?| 鍟嗗搧鏍囬 |
| data.items[].price | string(decimal) | 鍚?| 鍟嗗搧鍗曚环 |
| data.items[].quantity | int | 鍚?| 鏁伴噺 |
| data.items[].stock | int | 鍚?| 褰撳墠搴撳瓨 |
| data.items[].subtotal | string(decimal) | 鍚?| 褰撳墠椤瑰皬璁?|
| data.items_amount | string(decimal) | 鍚?| 鍟嗗搧鎬婚噾棰?|
| data.shipping_fee | string(decimal) | 鍚?| 杩愯垂锛堝綋鍓嶅浐瀹?`0.00`锛?|
| data.pay_amount | string(decimal) | 鍚?| 搴斾粯閲戦 |

鐘舵€佺爜锛歚200/400/401`

澶辫触鍦烘櫙锛堢ず渚嬶級锛?

- `no selected cart items`
- `product is inactive`
- `insufficient stock`

### 4.2 鍒涘缓璁㈠崟锛堝凡瀹炵幇锛?

- 鏂规硶锛歚POST`
- 璺緞锛歚/api/orders/`
- 閴存潈锛?*鏄?*锛堥渶 Bearer Token锛?

璇锋眰浣擄細

```json
{
	"address_id": 1
}
```

璇锋眰浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呭～ | 璇存槑 |
|---|---|---|---|
| address_id | int | 鏄?| 褰撳墠鐢ㄦ埛鏀惰揣鍦板潃 ID |

鍝嶅簲浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呰繑 | 璇存槑 |
|---|---|---|---|
| code | int | 鏄?| 涓氬姟鐮?|
| message | string | 鏄?| 鎴愬姛鏃朵负 `order created` |
| data | object/null | 鏄?| 涓氬姟鏁版嵁 |
| data.order_id | int | 鍚?| 璁㈠崟 ID |
| data.order_no | string | 鍚?| 璁㈠崟鍙凤紙鏍煎紡 `ORD{order_id:08d}`锛?|
| data.status | string | 鍚?| 鍒濆鐘舵€侊紝鍥哄畾涓?`pending_payment` |
| data.items_amount | string(decimal) | 鍚?| 鍟嗗搧鎬婚噾棰?|
| data.shipping_fee | string(decimal) | 鍚?| 杩愯垂锛堝綋鍓嶅浐瀹?`0.00`锛?|
| data.pay_amount | string(decimal) | 鍚?| 搴斾粯閲戦 |

鐘舵€佺爜锛歚200/400/401/404`

鍝嶅簲绀轰緥锛?

```json
{
	"code": 0,
	"message": "order created",
	"data": {
		"order_id": 10001,
		"order_no": "ORD00010001",
		"status": "pending_payment",
		"items_amount": "199.00",
		"shipping_fee": "0.00",
		"pay_amount": "199.00"
	}
}
```

澶辫触鍦烘櫙锛堢ず渚嬶級锛?

- `address_id is required`
- `no selected cart items`
- `product is inactive`
- `insufficient stock`

### 4.3 璁㈠崟鍙戣揣

- 鏂规硶锛歚POST`
- 璺緞锛歚/api/orders/{order_id}/ship/`
- 閴存潈锛?*鏄?*锛堝缓璁粎绠＄悊鍛?杩愯惀鍙皟鐢級

璇锋眰浣擄紙寤鸿锛夛細

```json
{
	"express_company": "SF",
	"express_no": "SF1234567890",
	"shipping_remark": "Leave at service desk"
}
```

鍓嶇疆鐘舵€侊細

- 浠呭厑璁?`pending_shipment -> pending_receipt`

鍝嶅簲绀轰緥锛堝缓璁級锛?

```json
{
	"code": 0,
	"message": "order shipped",
	"data": {
		"order_id": 10001,
		"status_before": "pending_shipment",
		"status_after": "pending_receipt",
		"express_company": "SF",
		"express_no": "SF1234567890",
		"shipping_remark": "Leave at service desk"
	}
}
```

### 4.4 纭鏀惰揣锛堣鍒掓帴鍙ｏ紝鏈笂绾匡級

> 褰撳墠鍚庣浠ｇ爜灏氭湭鏆撮湶纭鏀惰揣璺敱锛涗互涓嬩负鑱旇皟寤鸿濂戠害銆?

- 鏂规硶锛歚POST`
- 璺緞锛歚/api/orders/{order_id}/receive/`
- 閴存潈锛?*鏄?*锛堝缓璁粎涓嬪崟鐢ㄦ埛鏈汉鍙皟鐢級

璇锋眰浣擄細鏃?

鍓嶇疆鐘舵€侊細

- 浠呭厑璁?`pending_receipt -> completed`

鍝嶅簲绀轰緥锛堝缓璁級锛?

```json
{
	"code": 0,
	"message": "order received",
	"data": {
		"order_id": 10001,
		"status_before": "pending_receipt",
		"status_after": "completed"
	}
}
```

### 4.5 璁㈠崟鏌ヨ涓庡彇娑堬紙寰呰ˉ鍏呭疄鐜帮級

褰撳墠鏂囨。宸茶鐩栤€滅‘璁や笅鍗曘€佸垱寤鸿鍗曘€佸彂璐у绾︺€佺‘璁ゆ敹璐у绾︹€濓紝浣嗕互涓嬪父鐢ㄨ兘鍔涘湪鍚庣璺敱涓皻鏈疄鐜帮細

- 璁㈠崟鍒楄〃锛歚GET /api/orders/`
- 璁㈠崟璇︽儏锛歚GET /api/orders/{order_id}/`
- 鍙栨秷璁㈠崟锛歚POST /api/orders/{order_id}/cancel/`

寤鸿鍦ㄥ悗缁凯浠ｈˉ榻愬悗锛屽啀琛ュ厖瀵瑰簲瀛楁琛ㄤ笌閿欒鐮侊紙濡?`order not found`銆乣order status invalid`锛夈€?

## 5. 鏀粯 API

### 5.1 璁㈠崟鏀粯锛堝凡瀹炵幇锛屾ā鎷燂級

- 鏂规硶锛歚POST`
- 璺緞锛歚/api/paymentorders/{order_id}/pay/`
- 閴存潈锛?*鏄?*锛堥渶 Bearer Token锛?

璇锋眰浣擄細鏃?

璺緞鍙傛暟锛?

| 瀛楁 | 绫诲瀷 | 蹇呭～ | 璇存槑 |
|---|---|---|---|
| order_id | int | 鏄?| 瑕佹敮浠樼殑璁㈠崟 ID |

鍝嶅簲浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呰繑 | 璇存槑 |
|---|---|---|---|
| code | int | 鏄?| 涓氬姟鐮?|
| message | string | 鏄?| 鎴愬姛鏃朵负 `鏀粯鎴愬姛` |
| data | object/null | 鏄?| 涓氬姟鏁版嵁 |
| data.order_id | int | 鍚?| 璁㈠崟 ID |
| data.status_before | string | 鍚?| 鏀粯鍓嶇姸鎬侊紙褰撳墠鍥哄畾 `PENDING_PAY`锛?|
| data.status_after | string | 鍚?| 鏀粯鍚庣姸鎬侊紙褰撳墠鍥哄畾 `PENDING_SHIP`锛?|

鐘舵€佺爜锛歚200/401`

鍝嶅簲绀轰緥锛?

```json
{
	"code": 0,
	"message": "鏀粯鎴愬姛",
	"data": {
		"order_id": 10001,
		"status_before": "PENDING_PAY",
		"status_after": "PENDING_SHIP"
	}
}
```

### 5.2 鏀粯鎺ュ彛娉ㄦ剰浜嬮」锛堝綋鍓嶅疄鐜帮級

- 褰撳墠涓?Day1 妯℃嫙鎺ュ彛锛?*涓嶆牎楠岃鍗曞綊灞炪€佷笉鏍￠獙璁㈠崟鐪熷疄鐘舵€併€佷笉钀藉簱鏇存柊璁㈠崟鐘舵€?*銆?
- 杩斿洖鐘舵€佸€间负澶у啓 `PENDING_*`锛屼笌璁㈠崟妯″瀷涓殑灏忓啓铔囧舰鍊硷紙濡?`pending_payment`锛夋殏涓嶄竴鑷淬€?
- 鑱旇皟闃舵寤鸿浠ュ墠绔€滄敮浠樻垚鍔熸彁绀?+ 璁㈠崟鍒锋柊鍏滃簳鈥濆鐞嗭紱鍚庣画搴旀浛鎹负鐪熷疄鏀粯鍥炶皟涓庣姸鎬佽惤搴撱€?

## 6. 瀹㈡湇鐣欒█鏈€灏忛棴鐜鏄?

### 6.1 闂幆鐩爣

鍦ㄥ綋鍓嶇増鏈腑锛屽鏈嶈兘鍔涜仛鐒︹€滅暀瑷€-鍥炲-鍙鈥濇渶灏忛棴鐜細

1. 鐢ㄦ埛鍦ㄥ墠绔彁浜ょ暀瑷€锛堝彲鍖垮悕銆佸彲鐣欒仈绯绘柟寮忥級銆?
2. 瀹㈡湇鎴栬繍钀ュ湪 Django Admin 濉啓 `reply_content` 杩涜鍥炲銆?
3. 鐢ㄦ埛鍦ㄧ暀瑷€鍒楄〃涓湅鍒板洖澶嶇姸鎬佷笌鍥炲鍐呭銆?

### 6.2 瑙掕壊涓庤竟鐣?

- 璁垮/鐧诲綍鐢ㄦ埛锛氬彲鎻愪氦鐣欒█銆佸彲鏌ョ湅鏈€鏂扮暀瑷€鍒楄〃銆?
- 瀹㈡湇/杩愯惀锛圓dmin锛夛細鍦ㄥ悗鍙扮淮鎶ゅ洖澶嶅唴瀹广€?
- 褰撳墠涓嶅寘鍚細宸ュ崟鍒嗛厤銆佷細璇濈姸鎬佹満銆佸偓鍗曘€佹枃浠朵笂浼犮€侀€氱煡鎺ㄩ€併€?

### 6.3 鏈€灏忛棴鐜祦绋?

1. 鍓嶇 `POST /api/support/messages/` 鎻愪氦 `content`锛坄nickname/contact` 鍙€夛級銆?
2. 鍚庣钀藉簱 `SupportMessage`锛岃繑鍥炵暀瑷€璇︽儏銆?
3. 瀹㈡湇閫氳繃鍥炲鎺ュ彛鎻愪氦 `reply_content`锛岃嚜鍔ㄦ爣璁?`is_replied=true` 骞跺啓鍏?`replied_at`銆?
4. 鍓嶇 `GET /api/support/messages/` 鎷夊彇鏈€杩?50 鏉★紝娓叉煋鍥炲鍧椼€?

### 6.4 鏁版嵁瀵硅薄锛圫upportMessage锛?

| 瀛楁 | 绫诲瀷 | 璇存槑 |
|---|---|---|
| id | int | 鐣欒█ ID |
| user | FK(User)/null | 鐧诲綍鐢ㄦ埛鎻愪氦鏃惰嚜鍔ㄥ叧鑱?|
| nickname | string(50) | 鏄电О锛屾湭浼犳椂鑷姩鍥為€€涓虹敤鎴峰悕鎴栤€滃尶鍚嶇敤鎴封€?|
| contact | string(100) | 鑱旂郴鏂瑰紡锛堥偖绠?鎵嬫満鍙风瓑锛?|
| content | text | 鐣欒█姝ｆ枃 |
| is_replied | bool | 鏄惁宸插洖澶嶏紙鐢?`reply_content` 鑷姩椹卞姩锛?|
| reply_content | text | 鍥炲鍐呭 |
| created_at | datetime | 鍒涘缓鏃堕棿 |
| replied_at | datetime/null | 鍥炲鏃堕棿 |

### 6.5 杩愯绾︽潫锛堝綋鍓嶅疄鐜帮級

- 鐣欒█鍐呭 `content` 蹇呭～銆?
- 鍒楄〃鍙繑鍥炴渶杩?50 鏉★紙鎸夊垱寤烘椂闂村€掑簭锛夈€?
- 鎺ュ彛鏉冮檺涓?`AllowAny`锛屽尶鍚嶅彲璇诲彲鍐欍€?

## 7. 瀹㈡湇鐣欒█ API

浠ヤ笅鎺ュ彛宸插湪 `src/backend/common/urls.py` 瀹氫箟

- `GET /api/support/messages/`
- `POST /api/support/messages/`
- `PATCH /api/support/messages/{message_id}/reply/`

### 7.1 鑾峰彇鐣欒█鍒楄〃

- 鏂规硶锛歚GET`
- 璺緞锛歚/api/support/messages/`
- 閴存潈锛?*鍚?*锛坄AllowAny`锛?

璇锋眰浣擄細鏃?

鍝嶅簲浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呰繑 | 璇存槑 |
|---|---|---|---|
| code | int | 鏄?| 涓氬姟鐮?|
| message | string | 鏄?| 閫氬父涓?`success` |
| data | array<object> | 鏄?| 鐣欒█鍒楄〃锛堟渶澶?50 鏉★級 |
| data[].id | int | 鏄?| 鐣欒█ ID |
| data[].nickname | string | 鏄?| 鏄电О |
| data[].content | string | 鏄?| 鐣欒█鍐呭 |
| data[].is_replied | bool | 鏄?| 鏄惁宸插洖澶?|
| data[].reply_content | string | 鏄?| 鍥炲鍐呭锛堟湭鍥炲鏃朵负绌哄瓧绗︿覆锛?|
| data[].created_at | string(datetime) | 鏄?| 鐣欒█鏃堕棿锛圛SO 8601锛?|
| data[].replied_at | string(datetime)/null | 鏄?| 鍥炲鏃堕棿 |

鐘舵€佺爜锛歚200`

### 7.2 鎻愪氦鐣欒█

- 鏂规硶锛歚POST`
- 璺緞锛歚/api/support/messages/`
- 閴存潈锛?*鍚?*锛坄AllowAny`锛?

璇锋眰浣擄細

```json
{
	"nickname": "灏忕帇",
	"contact": "138****8888",
	"content": "璁㈠崟浠€涔堟椂鍊欏彂璐э紵"
}
```

璇锋眰浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呭～ | 璇存槑 |
|---|---|---|---|
| nickname | string | 鍚?| 鏄电О锛涗负绌烘椂鑷姩鍥為€€ |
| contact | string | 鍚?| 鑱旂郴鏂瑰紡 |
| content | string | 鏄?| 鐣欒█鍐呭 |

鍝嶅簲浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呰繑 | 璇存槑 |
|---|---|---|---|
| code | int | 鏄?| 涓氬姟鐮?|
| message | string | 鏄?| 鎴愬姛鏃朵负鈥滅暀瑷€鎻愪氦鎴愬姛鈥?|
| data | object/null | 鏄?| 涓氬姟鏁版嵁 |
| data.id | int | 鍚?| 鐣欒█ ID |
| data.nickname | string | 鍚?| 鏄电О |
| data.content | string | 鍚?| 鐣欒█鍐呭 |
| data.is_replied | bool | 鍚?| 鏄惁宸插洖澶?|
| data.reply_content | string | 鍚?| 鍥炲鍐呭 |
| data.created_at | string(datetime) | 鍚?| 鐣欒█鏃堕棿 |
| data.replied_at | string(datetime)/null | 鍚?| 鍥炲鏃堕棿 |

鐘舵€佺爜锛歚200/400`

澶辫触鍦烘櫙锛堢ず渚嬶級锛?

- `content 蹇呭～`

### 7.3 瀹㈡湇鍥炲鐣欒█

- 鏂规硶锛歚PATCH`
- 璺緞锛歚/api/support/messages/{message_id}/reply/`
- 閴存潈锛?*鏄?*锛坄IsAuthenticated`锛屼笖闇€ `is_staff=true`锛?

璇锋眰浣擄細

```json
{
	"reply_content": "鎮ㄥソ锛屼粖澶╀細鍙戣揣銆?
}
```

璇锋眰浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呭～ | 璇存槑 |
|---|---|---|---|
| reply_content | string | 鏄?| 瀹㈡湇鍥炲鍐呭 |

鍝嶅簲浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呰繑 | 璇存槑 |
|---|---|---|---|
| code | int | 鏄?| 涓氬姟鐮?|
| message | string | 鏄?| 鎴愬姛鏃朵负鈥滃洖澶嶆垚鍔熲€?|
| data | object/null | 鏄?| 鐣欒█璇︽儏锛堢粨鏋勫悓 7.2 杩斿洖 data锛?|

鐘舵€佺爜锛歚200/400/401/403`

澶辫触鍦烘櫙锛堢ず渚嬶級锛?

- `reply_content 蹇呭～`
- `forbidden`

## 8. Auth锛堢敤鎴疯璇侊級API

浠ヤ笅鎺ュ彛宸插湪 `src/backend/users/urls.py` 瀹氫箟

- `POST /api/users/register/`
- `POST /api/users/login/`
- `POST /api/users/refresh/`
- `GET /api/users/me/`

### 8.1 娉ㄥ唽

- 鏂规硶锛歚POST`
- 璺緞锛歚/api/users/register/`
- 閴存潈锛?*鍚?*锛坄AllowAny`锛?

璇锋眰浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呭～ | 璇存槑 |
|---|---|---|---|
| username | string | 鏄?| 鐢ㄦ埛鍚?|
| password | string | 鏄?| 瀵嗙爜 |

鍝嶅簲浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呰繑 | 璇存槑 |
|---|---|---|---|
| code | int | 鏄?| 涓氬姟鐮?|
| message | string | 鏄?| 鎴愬姛鏃堕€氬父涓衡€滄敞鍐屾垚鍔熲€?|
| data | object/null | 鏄?| 涓氬姟鏁版嵁 |
| data.id | int | 鍚?| 鐢ㄦ埛 ID |
| data.username | string | 鍚?| 鐢ㄦ埛鍚?|

鐘舵€佺爜锛歚200/400`

### 8.2 鐧诲綍

- 鏂规硶锛歚POST`
- 璺緞锛歚/api/users/login/`
- 閴存潈锛?*鍚?*锛坄AllowAny`锛?

璇锋眰浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呭～ | 璇存槑 |
|---|---|---|---|
| username | string | 鏄?| 鐢ㄦ埛鍚?|
| password | string | 鏄?| 瀵嗙爜 |

鍝嶅簲浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呰繑 | 璇存槑 |
|---|---|---|---|
| code | int | 鏄?| 涓氬姟鐮?|
| message | string | 鏄?| 鎴愬姛鏃堕€氬父涓衡€滅櫥褰曟垚鍔熲€?|
| data | object/null | 鏄?| 涓氬姟鏁版嵁 |
| data.access | string | 鍚?| JWT 璁块棶浠ょ墝 |
| data.refresh | string | 鍚?| JWT 鍒锋柊浠ょ墝 |

鐘舵€佺爜锛歚200/401`

鍝嶅簲绀轰緥锛?

```json
{
	"code": 0,
	"message": "鐧诲綍鎴愬姛",
	"data": {
		"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.access_token_demo",
		"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.refresh_token_demo"
	}
}
```

### 8.3 鍒锋柊 Token

- 鏂规硶锛歚POST`
- 璺緞锛歚/api/users/refresh/`
- 閴存潈锛?*鍚?*锛坄AllowAny`锛?

璇锋眰浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呭～ | 璇存槑 |
|---|---|---|---|
| refresh | string | 鏄?| JWT 鍒锋柊浠ょ墝 |

鍝嶅簲浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呰繑 | 璇存槑 |
|---|---|---|---|
| code | int | 鏄?| 涓氬姟鐮?|
| message | string | 鏄?| 鎴愬姛鏃堕€氬父涓衡€滃埛鏂版垚鍔熲€?|
| data | object/null | 鏄?| 涓氬姟鏁版嵁 |
| data.access | string | 鍚?| 鏂扮殑 JWT 璁块棶浠ょ墝 |

鐘舵€佺爜锛歚200/400/401`

### 8.4 褰撳墠鐢ㄦ埛淇℃伅

- 鏂规硶锛歚GET`
- 璺緞锛歚/api/users/me/`
- 閴存潈锛?*鏄?*锛坄IsAuthenticated`锛?

璇锋眰浣擄細鏃?

鍝嶅簲浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呰繑 | 璇存槑 |
|---|---|---|---|
| code | int | 鏄?| 涓氬姟鐮?|
| message | string | 鏄?| 鍝嶅簲娑堟伅 |
| data | object/null | 鏄?| 涓氬姟鏁版嵁 |
| data.id | int | 鍚?| 鐢ㄦ埛 ID |
| data.username | string | 鍚?| 鐢ㄦ埛鍚?|

鐘舵€佺爜锛歚200/401`

### 8.5 鍦板潃鍒楄〃/鏂板

- 鏂规硶锛歚GET` / `POST`
- 璺緞锛歚/api/users/addresses/`
- 閴存潈锛?*鏄?*锛坄IsAuthenticated`锛?

`GET` 鍝嶅簲 `data` 涓哄湴鍧€鏁扮粍锛沗POST` 璇锋眰浣撳瓧娈碉細

| 瀛楁 | 绫诲瀷 | 蹇呭～ | 璇存槑 |
|---|---|---|---|
| name | string | 鏄?| 鏀惰揣浜?|
| address | string | 鏄?| 鏀惰揣鍦板潃 |
| phone_number | string | 鏄?| 鑱旂郴鐢佃瘽 |
| is_default | bool/string/int | 鍚?| 鏄惁榛樿鍦板潃 |

鐘舵€佺爜锛歚200/400/401`

### 8.6 鍦板潃鏇存柊/鍒犻櫎

- 鏂规硶锛歚PATCH` / `DELETE`
- 璺緞锛歚/api/users/addresses/{address_id}/`
- 閴存潈锛?*鏄?*锛坄IsAuthenticated`锛?

`PATCH` 鍙洿鏂?`name/address/phone_number/is_default`锛沗DELETE` 鍒犻櫎鍦板潃銆?

鐘舵€佺爜锛歚200/401`

### 8.7 璁句负榛樿鍦板潃

- 鏂规硶锛歚POST`
- 璺緞锛歚/api/users/addresses/{address_id}/set-default/`
- 閴存潈锛?*鏄?*锛坄IsAuthenticated`锛?

鐘舵€佺爜锛歚200/401`

## 9. Product / Categories API

### 9.1 褰撳墠瀹炵幇鐘舵€?

- 鏁版嵁妯″瀷宸插瓨鍦細`Category`銆乣Product`銆乣ProductImage`锛坄src/backend/products/models.py`锛夈€?
- 绠＄悊鍚庡彴宸插彲缁存姢鍒嗙被鍜屽晢鍝侊紙`src/backend/products/admin.py`锛夈€?
- 褰撳墠鏈寕杞藉叕寮€ API锛歚backendCore/urls.py` 涓皻鏈?`include("products.urls")`锛屼笖 `products/views.py` 鏆傛棤鎺ュ彛瀹炵幇銆?

浠ヤ笅涓哄榻愬綋鍓嶆暟鎹粨鏋勭殑瑙勫垝鎺ュ彛瀹氫箟锛屼緵鍚庣画寮€鍙戜笌鑱旇皟浣跨敤銆?

### 9.2 鍟嗗搧鍒楄〃锛堣鍒掓帴鍙ｏ級

- 鏂规硶锛歚GET`
- 璺緞锛歚/api/products/`
- 閴存潈锛?*鍚?*锛堝缓璁?`AllowAny`锛?

鏌ヨ鍙傛暟锛堝缓璁級锛?

| 鍙傛暟 | 绫诲瀷 | 蹇呭～ | 璇存槑 |
|---|---|---|---|
| category_id | int | 鍚?| 鎸夊垎绫昏繃婊?|
| keyword | string | 鍚?| 鍟嗗搧鍚嶆ā绯婃悳绱?|
| is_active | bool | 鍚?| 鏄惁涓婃灦 |
| page | int | 鍚?| 椤电爜锛岄粯璁?`1` |
| page_size | int | 鍚?| 姣忛〉鏁伴噺锛岄粯璁?`20` |
| ordering | string | 鍚?| 鎺掑簭锛屽 `price`銆乣-created_at` |

鍝嶅簲浣撳瓧娈碉紙寤鸿锛夛細

| 瀛楁 | 绫诲瀷 | 璇存槑 |
|---|---|---|
| data.list | array<object> | 鍟嗗搧鍒楄〃 |
| data.list[].id | int | 鍟嗗搧 ID |
| data.list[].name | string | 鍟嗗搧鍚嶇О |
| data.list[].price | string(decimal) | 浠锋牸 |
| data.list[].stock | int | 搴撳瓨 |
| data.list[].is_active | bool | 鏄惁涓婃灦 |
| data.list[].category_id | int | 鍒嗙被 ID |
| data.list[].category_name | string | 鍒嗙被鍚嶇О |
| data.list[].cover_image | string/null | 灏侀潰鍥?URL |
| data.pagination.page | int | 褰撳墠椤?|
| data.pagination.page_size | int | 姣忛〉鏁伴噺 |
| data.pagination.total | int | 鎬绘暟 |

鐘舵€佺爜锛堝缓璁級锛歚200/400`

鍝嶅簲绀轰緥锛堣鍒掓帴鍙ｏ級锛?

```json
{
	"code": 0,
	"message": "success",
	"data": {
		"list": [
			{
				"id": 101,
				"name": "YSL 鏂圭鍙ｇ孩",
				"price": "199.00",
				"stock": 88,
				"is_active": true,
				"category_id": 10,
				"category_name": "鍙ｇ孩",
				"cover_image": "/media/products/ysl-101.jpg"
			}
		],
		"pagination": {
			"page": 1,
			"page_size": 20,
			"total": 1
		}
	}
}
```

### 9.3 鍟嗗搧璇︽儏锛堣鍒掓帴鍙ｏ級

- 鏂规硶锛歚GET`
- 璺緞锛歚/api/products/{product_id}/`
- 閴存潈锛?*鍚?*锛堝缓璁?`AllowAny`锛?

鍝嶅簲浣撳瓧娈碉紙寤鸿锛夛細

| 瀛楁 | 绫诲瀷 | 璇存槑 |
|---|---|---|
| data.id | int | 鍟嗗搧 ID |
| data.name | string | 鍟嗗搧鍚嶇О |
| data.price | string(decimal) | 浠锋牸 |
| data.stock | int | 搴撳瓨 |
| data.is_active | bool | 鏄惁涓婃灦 |
| data.description | string | 鍟嗗搧鎻忚堪 |
| data.category | object | 鍒嗙被淇℃伅 |
| data.category.id | int | 鍒嗙被 ID |
| data.category.name | string | 鍒嗙被鍚嶇О |
| data.cover_image | string/null | 灏侀潰鍥?URL |
| data.images | array<object> | 璇︽儏鍥惧垪琛?|
| data.images[].image | string | 鍥剧墖 URL |
| data.images[].sort_order | int | 鎺掑簭 |

鐘舵€佺爜锛堝缓璁級锛歚200/404`

### 9.4 鍒嗙被鍒楄〃锛堣鍒掓帴鍙ｏ級

- 鏂规硶锛歚GET`
- 璺緞锛歚/api/categories/`
- 閴存潈锛?*鍚?*锛堝缓璁?`AllowAny`锛?

鍝嶅簲浣撳瓧娈碉紙寤鸿锛夛細

| 瀛楁 | 绫诲瀷 | 璇存槑 |
|---|---|---|
| data | array<object> | 鍒嗙被鍒楄〃 |
| data[].id | int | 鍒嗙被 ID |
| data[].name | string | 鍒嗙被鍚?|
| data[].parent_id | int/null | 鐖跺垎绫?ID |
| data[].sort_order | int | 鎺掑簭 |

鐘舵€佺爜锛堝缓璁級锛歚200`

### 9.5 鍒嗙被鏍戯紙瑙勫垝鎺ュ彛锛?

- 鏂规硶锛歚GET`
- 璺緞锛歚/api/categories/tree/`
- 閴存潈锛?*鍚?*锛堝缓璁?`AllowAny`锛?

鍝嶅簲浣撳瓧娈碉紙寤鸿锛夛細

| 瀛楁 | 绫诲瀷 | 璇存槑 |
|---|---|---|
| data | array<object> | 涓€绾у垎绫绘暟缁?|
| data[].id | int | 鍒嗙被 ID |
| data[].name | string | 鍒嗙被鍚?|
| data[].children | array<object> | 瀛愬垎绫?|

鐘舵€佺爜锛堝缓璁級锛歚200`

### 9.6 鍒嗙被涓嬪晢鍝侊紙瑙勫垝鎺ュ彛锛?

- 鏂规硶锛歚GET`
- 璺緞锛歚/api/categories/{category_id}/products/`
- 閴存潈锛?*鍚?*锛堝缓璁?`AllowAny`锛?

璇存槑锛氳繑鍥炴煇鍒嗙被锛堝彲閫夊惈瀛愬垎绫伙級涓嬪晢鍝佸垪琛紱杩斿洖缁撴瀯鍙鐢ㄢ€?.2 鍟嗗搧鍒楄〃鈥濄€?

鐘舵€佺爜锛堝缓璁級锛歚200/404`



## 10. 鏂囨。缁存姢娴佺▼

1. 浠ユ湰鏂囨。涓哄敮涓€鑱旇皟鍩虹嚎锛屼繚璇佹瘡涓帴鍙ｉ兘鏈夛細鏂规硶銆佽矾寰勩€佽姹備綋銆佹垚鍔?澶辫触绀轰緥銆?
2. 鍓嶅悗绔仈璋冨悗锛岃ˉ鍏呭瓧娈佃鏄庯紙绫诲瀷銆佹槸鍚﹀繀濉€佹灇涓惧€硷級銆?
3. 璺熼殢浠ｇ爜鍙樻洿鍚屾鏇存柊锛氭瘡鏀?`urls.py`/`views.py`锛屽悓鏃舵敼 `docs/support_api.md`銆?
4. 鐗堟湰鍖栫淮鎶わ細鎸夐噷绋嬬澧炲姞 `v1/v2` 鍙樻洿璁板綍銆?
