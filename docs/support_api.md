# 支撑 API 草案

最后更新：2026-03-03

## 1. 文档定位

- 主 API 文档：`docs/support_api.md`
- 订单状态补充文档：`src/backend/docs/order_status.md`

> 本文档按当前后端代码实际实现整理，便于先联调、再细化。

## 2. 通用约定

### 2.1 基础路径

- 购物车：`/api/cart/`
- 订单：`/api/orders/`
- 支付：`/api/paymentorders/<order_id>/pay/`（按当前路由配置实际拼接结果）

### 2.2 通用响应结构

```json
{
	"code": 0,
	"message": "success",
	"data": {}
}
```

- 成功：`code=0`
- 失败：`code=1`

### 2.3 鉴权约定

- 认证方式：`JWT Bearer Token`
- 请求头：`Authorization: Bearer <access_token>`
- 默认权限：后端全局 `IsAuthenticated`
- 白名单接口：用户注册、登录、刷新 token（`AllowAny`）

### 2.4 状态码约定

#### HTTP 状态码

- `200 OK`：请求成功（业务成功/业务失败都可能返回，需结合 `code` 判断）
- `400 Bad Request`：参数校验失败
- `401 Unauthorized`：未登录、token 无效/过期、用户名密码错误
- `403 Forbidden`：已认证但无权限（当前草案接口暂未单独定义）
- `500 Internal Server Error`：服务端异常

#### 业务状态码（响应体 `code`）

- `0`：业务成功
- `1`：业务失败

## 3. 购物车 API

### 3.1 获取购物车

- 方法：`GET`
- 路径：`/api/cart/`
- 鉴权：**是**（需 Bearer Token）

请求体：无

响应体字段：

| 字段 | 类型 | 必返 | 说明 |
|---|---|---|---|
| code | int | 是 | 业务码，`0` 成功，`1` 失败 |
| message | string | 是 | 响应消息 |
| data | object | 是 | 业务数据 |
| data.items | array<object> | 是 | 购物车项列表 |
| data.items[].id | int | 是 | 购物车项 ID |
| data.items[].product_id | int | 是 | 商品 ID |
| data.items[].title | string | 是 | 商品标题 |
| data.items[].price | string(decimal) | 是 | 商品单价 |
| data.items[].quantity | int | 是 | 数量 |
| data.items[].selected | bool | 是 | 是否勾选 |
| data.total_amount | string(decimal) | 是 | 勾选商品总金额 |

状态码：`200/401`

响应示例：

```json
{
	"code": 0,
	"message": "success",
	"data": {
		"items": [
			{
				"id": 1,
				"product_id": 101,
				"title": "示例商品",
				"price": "99.00",
				"quantity": 1,
				"selected": true
			}
		],
		"total_amount": "99.00"
	}
}
```

### 3.2 加入购物车

- 方法：`POST`
- 路径：`/api/cart/items/`
- 鉴权：**是**（需 Bearer Token）

请求体：

```json
{
	"product_id": 101,
	"quantity": 1
}
```

校验：

- `product_id` 必填
- `quantity > 0`

请求体字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| product_id | int | 是 | 商品 ID |
| quantity | int | 否 | 购买数量，默认 `1`，且必须 `> 0` |

响应体字段：

| 字段 | 类型 | 必返 | 说明 |
|---|---|---|---|
| code | int | 是 | 业务码 |
| message | string | 是 | 成功时通常为“加入购物车成功” |
| data | object/null | 是 | 业务数据 |
| data.item_id | int | 否 | 新增购物车项 ID（成功时返回） |

状态码：`200/400/401`

### 3.3 更新购物车项

- 方法：`PATCH`
- 路径：`/api/cart/items/{item_id}/`
- 鉴权：**是**（需 Bearer Token）

请求体（至少传一个）：

```json
{
	"quantity": 2,
	"selected": true
}
```

请求体字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| quantity | int | 否 | 更新数量；如传入应保证 `> 0` |
| selected | bool | 否 | 是否勾选 |

响应体字段：

| 字段 | 类型 | 必返 | 说明 |
|---|---|---|---|
| code | int | 是 | 业务码 |
| message | string | 是 | 成功时通常为“更新成功” |
| data | object/null | 是 | 业务数据 |
| data.item_id | int | 否 | 购物车项 ID（成功时返回） |

状态码：`200/400/401`

## 4. 订单 API

### 4.1 下单确认

- 方法：`POST`
- 路径：`/api/orders/confirm/`
- 鉴权：**是**（需 Bearer Token）

请求体：

```json
{
	"address_id": 1,
	"note": "请尽快发货"
}
```

校验：

- `address_id` 必填

请求体字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| address_id | int | 是 | 收货地址 ID |
| note | string | 否 | 订单备注，默认空字符串 |

响应体字段：

| 字段 | 类型 | 必返 | 说明 |
|---|---|---|---|
| code | int | 是 | 业务码 |
| message | string | 是 | 响应消息 |
| data | object/null | 是 | 业务数据 |
| data.address_id | int | 否 | 收货地址 ID |
| data.note | string | 否 | 订单备注 |
| data.items_amount | string(decimal) | 否 | 商品总金额 |
| data.shipping_fee | string(decimal) | 否 | 运费 |
| data.pay_amount | string(decimal) | 否 | 应付金额 |

状态码：`200/400/401`

### 4.2 创建订单

- 方法：`POST`
- 路径：`/api/orders/`
- 鉴权：**是**（需 Bearer Token）

请求体：

```json
{
	"address_id": 1
}
```

请求体字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| address_id | int | 是 | 收货地址 ID |

响应体字段：

| 字段 | 类型 | 必返 | 说明 |
|---|---|---|---|
| code | int | 是 | 业务码 |
| message | string | 是 | 成功时通常为“下单成功” |
| data | object/null | 是 | 业务数据 |
| data.order_id | int | 否 | 订单 ID |
| data.order_no | string | 否 | 订单号 |
| data.status | string | 否 | 订单状态，示例 `PENDING_PAY` |

状态码：`200/400/401`

响应示例：

```json
{
	"code": 0,
	"message": "下单成功",
	"data": {
		"order_id": 10001,
		"order_no": "ORD202603010001",
		"status": "PENDING_PAY"
	}
}
```

## 5. 支付 API

### 5.1 订单支付

- 方法：`POST`
- 路径：`/api/paymentorders/{order_id}/pay/`
- 鉴权：**是**（需 Bearer Token）

请求体：无

路径参数：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| order_id | int | 是 | 要支付的订单 ID |

响应体字段：

| 字段 | 类型 | 必返 | 说明 |
|---|---|---|---|
| code | int | 是 | 业务码 |
| message | string | 是 | 成功时通常为“支付成功” |
| data | object/null | 是 | 业务数据 |
| data.order_id | int | 否 | 订单 ID |
| data.status_before | string | 否 | 支付前状态 |
| data.status_after | string | 否 | 支付后状态 |

状态码：`200/401`

响应示例：

```json
{
	"code": 0,
	"message": "支付成功",
	"data": {
		"order_id": 10001,
		"status_before": "PENDING_PAY",
		"status_after": "PENDING_SHIP"
	}
}
```

## 6. 用户 API（已实现，待主路由挂载）

以下接口已在 `src/backend/user/urls.py` 定义，但当前 `backendCore/urls.py` 尚未 include：

- `POST /api/user/register/`
- `POST /api/user/login/`
- `POST /api/user/refresh/`
- `GET /api/user/me/`

### 6.1 注册

- 方法：`POST`
- 路径：`/api/user/register/`
- 鉴权：**否**（`AllowAny`）

请求体字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

响应体字段：

| 字段 | 类型 | 必返 | 说明 |
|---|---|---|---|
| code | int | 是 | 业务码 |
| message | string | 是 | 成功时通常为“注册成功” |
| data | object/null | 是 | 业务数据 |
| data.id | int | 否 | 用户 ID |
| data.username | string | 否 | 用户名 |

状态码：`200/400`

### 6.2 登录

- 方法：`POST`
- 路径：`/api/user/login/`
- 鉴权：**否**（`AllowAny`）

请求体字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

响应体字段：

| 字段 | 类型 | 必返 | 说明 |
|---|---|---|---|
| code | int | 是 | 业务码 |
| message | string | 是 | 成功时通常为“登录成功” |
| data | object/null | 是 | 业务数据 |
| data.access | string | 否 | JWT 访问令牌 |
| data.refresh | string | 否 | JWT 刷新令牌 |

状态码：`200/401`

### 6.3 刷新 Token

- 方法：`POST`
- 路径：`/api/user/refresh/`
- 鉴权：**否**（`AllowAny`）

请求体字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| refresh | string | 是 | JWT 刷新令牌 |

响应体字段：

| 字段 | 类型 | 必返 | 说明 |
|---|---|---|---|
| code | int | 是 | 业务码 |
| message | string | 是 | 成功时通常为“刷新成功” |
| data | object/null | 是 | 业务数据 |
| data.access | string | 否 | 新的 JWT 访问令牌 |

状态码：`200/400/401`

### 6.4 当前用户信息

- 方法：`GET`
- 路径：`/api/user/me/`
- 鉴权：**是**（`IsAuthenticated`）

请求体：无

响应体字段：

| 字段 | 类型 | 必返 | 说明 |
|---|---|---|---|
| code | int | 是 | 业务码 |
| message | string | 是 | 响应消息 |
| data | object/null | 是 | 业务数据 |
| data.id | int | 否 | 用户 ID |
| data.username | string | 否 | 用户名 |

状态码：`200/401`

建议补充主路由后再开放给前端联调。

## 7. 落文档建议流程

1. 先以本文档为“联调草案”，保证每个接口都有：方法、路径、请求体、成功/失败示例。
2. 前后端联调后，补充字段说明（类型、是否必填、枚举值）。
3. 跟随代码变更同步更新：每改 `urls.py`/`views.py`，同时改 `docs/support_api.md`。
4. 版本化维护：按里程碑增加 `v1/v2` 变更记录。
