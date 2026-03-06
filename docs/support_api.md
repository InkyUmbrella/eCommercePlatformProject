# 支撑 API 草案

最后更新：2026-03-06

## 1. 文档定位

- 主 API 文档：`docs/support_api.md`
- 订单状态补充文档：`src/backend/docs/order_status.md`

> 本文档按当前后端代码实际实现整理，便于先联调、再细化。

## 2. 通用约定

### 2.1 基础路径

- 购物车：`/api/cart/`
- 订单：`/api/orders/`
- 支付：`/api/paymentorders/<order_id>/pay/`（按当前路由配置实际拼接结果）
- 客服：`/api/support/`
- 用户：`/api/users/`
- 商品：`/api/products/`（草案，待实现）
- 分类：`/api/categories/`（草案，待实现）

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

### 2.5 错误码规范（补充）

> 说明：当前后端大部分接口仍使用 `code=0/1`。以下为后续统一规范，联调阶段可先按“兼容模式”解析。

#### 兼容模式（当前可用）

- 成功：`HTTP 200` 且 `code=0`
- 失败：`HTTP 4xx/5xx` 且 `code=1`
- 前端兼容建议：先判断 HTTP 状态，再判断 `code`，最后读取 `message`。

#### 目标模式（建议逐步落地）

| 区间 | 模块 | 说明 |
|---|---|---|
| 0 | 通用 | 成功 |
| 1000-1099 | Auth | 登录、token、用户认证 |
| 2000-2199 | Product | 商品相关 |
| 2200-2299 | Category | 分类相关 |
| 3000-3199 | Cart | 购物车相关 |
| 4000-4199 | Order | 订单相关 |
| 5000-5199 | Support | 客服留言相关 |
| 9000-9099 | System | 系统级异常 |

建议常用错误码：

| code | HTTP | message 示例 | 说明 |
|---|---|---|---|
| 1001 | 401 | unauthorized | 未登录或 token 缺失 |
| 1002 | 401 | token invalid | token 无效或过期 |
| 1003 | 401 | invalid credentials | 用户名或密码错误 |
| 2001 | 404 | product not found | 商品不存在 |
| 2002 | 400 | product is inactive | 商品已下架 |
| 2201 | 404 | category not found | 分类不存在 |
| 3001 | 400 | quantity must be greater than 0 | 购买数量非法 |
| 3002 | 400 | insufficient stock | 库存不足 |
| 3003 | 400 | no selected cart items | 无勾选商品 |
| 4001 | 400 | address_id is required | 收货地址缺失 |
| 4002 | 400 | order status invalid | 订单状态不允许当前操作 |
| 5001 | 400 | content 必填 | 客服留言内容为空 |
| 9000 | 500 | internal server error | 服务端异常 |

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
| data.items[].subtotal | string(decimal) | 是 | 当前项小计（`price * quantity`） |
| data.items[].stock | int | 是 | 商品库存快照 |
| data.items[].is_active | bool | 是 | 商品是否上架 |
| data.total_amount | string(decimal) | 是 | 勾选商品总金额 |
| data.selected_count | int | 是 | 已勾选商品项数 |
| data.item_count | int | 是 | 购物车总项数 |

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
| message | string | 是 | 成功时为 `item added` |
| data | object/null | 是 | 业务数据 |
| data.item | object | 否 | 新增或累加后的购物车项 |
| data.item.id | int | 否 | 购物车项 ID |
| data.item.product_id | int | 否 | 商品 ID |
| data.item.title | string | 否 | 商品标题 |
| data.item.price | string(decimal) | 否 | 商品单价 |
| data.item.quantity | int | 否 | 当前数量（已含累加） |
| data.item.selected | bool | 否 | 是否勾选 |
| data.item.subtotal | string(decimal) | 否 | 当前项小计 |
| data.item.stock | int | 否 | 商品库存 |
| data.item.is_active | bool | 否 | 商品是否上架 |

状态码：`200/400/401`

失败场景（示例）：

- `product_id is required`
- `quantity must be an integer`
- `quantity must be greater than 0`
- `product is inactive`
- `insufficient stock`

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
| message | string | 是 | 成功时为 `item updated` |
| data | object/null | 是 | 业务数据 |
| data.item | object | 否 | 更新后的购物车项（结构同 3.2） |

状态码：`200/400/401`

失败场景（示例）：

- `provide quantity or selected`
- `quantity must be an integer`
- `quantity must be greater than 0`
- `insufficient stock`

### 3.4 删除购物车项

- 方法：`DELETE`
- 路径：`/api/cart/items/{item_id}/`
- 鉴权：**是**（需 Bearer Token）

请求体：无

响应体字段：

| 字段 | 类型 | 必返 | 说明 |
|---|---|---|---|
| code | int | 是 | 业务码 |
| message | string | 是 | 成功时为 `item deleted` |
| data | null | 是 | 固定为 `null` |

状态码：`200/401`

### 3.5 购物车全选/全不选

- 方法：`PATCH`
- 路径：`/api/cart/select-all/`
- 鉴权：**是**（需 Bearer Token）

请求体：

```json
{
	"selected": true
}
```

请求体字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| selected | bool/string/int | 是 | 支持 `true/false`、`1/0`、`yes/no` 等可转布尔值 |

响应体字段：

| 字段 | 类型 | 必返 | 说明 |
|---|---|---|---|
| code | int | 是 | 业务码 |
| message | string | 是 | 成功时为 `select all updated` |
| data | object | 是 | 最新购物车快照（结构同 3.1） |

状态码：`200/400/401`

失败场景（示例）：

- `selected is required`

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

## 6. 客服留言最小闭环说明

### 6.1 闭环目标

在当前版本中，客服能力聚焦“留言-回复-可见”最小闭环：

1. 用户在前端提交留言（可匿名、可留联系方式）。
2. 客服或运营在 Django Admin 填写 `reply_content` 进行回复。
3. 用户在留言列表中看到回复状态与回复内容。

### 6.2 角色与边界

- 访客/登录用户：可提交留言、可查看最新留言列表。
- 客服/运营（Admin）：在后台维护回复内容。
- 当前不包含：工单分配、会话状态机、催单、文件上传、通知推送。

### 6.3 最小闭环流程

1. 前端 `POST /api/support/messages/` 提交 `content`（`nickname/contact` 可选）。
2. 后端落库 `SupportMessage`，返回留言详情。
3. 后台编辑同一条留言的 `reply_content`，保存后自动标记 `is_replied=true` 并写入 `replied_at`。
4. 前端 `GET /api/support/messages/` 拉取最近 50 条，渲染回复块。

### 6.4 数据对象（SupportMessage）

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int | 留言 ID |
| user | FK(User)/null | 登录用户提交时自动关联 |
| nickname | string(50) | 昵称，未传时自动回退为用户名或“匿名用户” |
| contact | string(100) | 联系方式（邮箱/手机号等） |
| content | text | 留言正文 |
| is_replied | bool | 是否已回复（由 `reply_content` 自动驱动） |
| reply_content | text | 回复内容 |
| created_at | datetime | 创建时间 |
| replied_at | datetime/null | 回复时间 |

### 6.5 运行约束（当前实现）

- 留言内容 `content` 必填。
- 列表只返回最近 50 条（按创建时间倒序）。
- 接口权限为 `AllowAny`，匿名可读可写。

## 7. 客服留言 API

以下接口已在 `src/backend/common/urls.py` 定义

- `GET /api/support/messages/`
- `POST /api/support/messages/`

### 7.1 获取留言列表

- 方法：`GET`
- 路径：`/api/support/messages/`
- 鉴权：**否**（`AllowAny`）

请求体：无

响应体字段：

| 字段 | 类型 | 必返 | 说明 |
|---|---|---|---|
| code | int | 是 | 业务码 |
| message | string | 是 | 通常为 `success` |
| data | array<object> | 是 | 留言列表（最多 50 条） |
| data[].id | int | 是 | 留言 ID |
| data[].nickname | string | 是 | 昵称 |
| data[].content | string | 是 | 留言内容 |
| data[].is_replied | bool | 是 | 是否已回复 |
| data[].reply_content | string | 是 | 回复内容（未回复时为空字符串） |
| data[].created_at | string(datetime) | 是 | 留言时间（ISO 8601） |
| data[].replied_at | string(datetime)/null | 是 | 回复时间 |

状态码：`200`

### 7.2 提交留言

- 方法：`POST`
- 路径：`/api/support/messages/`
- 鉴权：**否**（`AllowAny`）

请求体：

```json
{
	"nickname": "小王",
	"contact": "138****8888",
	"content": "订单什么时候发货？"
}
```

请求体字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| nickname | string | 否 | 昵称；为空时自动回退 |
| contact | string | 否 | 联系方式 |
| content | string | 是 | 留言内容 |

响应体字段：

| 字段 | 类型 | 必返 | 说明 |
|---|---|---|---|
| code | int | 是 | 业务码 |
| message | string | 是 | 成功时为“留言提交成功” |
| data | object/null | 是 | 业务数据 |
| data.id | int | 否 | 留言 ID |
| data.nickname | string | 否 | 昵称 |
| data.content | string | 否 | 留言内容 |
| data.is_replied | bool | 否 | 是否已回复 |
| data.reply_content | string | 否 | 回复内容 |
| data.created_at | string(datetime) | 否 | 留言时间 |
| data.replied_at | string(datetime)/null | 否 | 回复时间 |

状态码：`200/400`

失败场景（示例）：

- `content 必填`

## 8. Auth（用户认证）API

以下接口已在 `src/backend/users/urls.py` 定义

- `POST /api/users/register/`
- `POST /api/users/login/`
- `POST /api/users/refresh/`
- `GET /api/users/me/`

### 8.1 注册

- 方法：`POST`
- 路径：`/api/users/register/`
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

### 8.2 登录

- 方法：`POST`
- 路径：`/api/users/login/`
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

### 8.3 刷新 Token

- 方法：`POST`
- 路径：`/api/users/refresh/`
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

### 8.4 当前用户信息

- 方法：`GET`
- 路径：`/api/users/me/`
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

### 8.5 地址列表/新增

- 方法：`GET` / `POST`
- 路径：`/api/users/addresses/`
- 鉴权：**是**（`IsAuthenticated`）

`GET` 响应 `data` 为地址数组；`POST` 请求体字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 是 | 收货人 |
| address | string | 是 | 收货地址 |
| phone_number | string | 是 | 联系电话 |
| is_default | bool/string/int | 否 | 是否默认地址 |

状态码：`200/400/401`

### 8.6 地址更新/删除

- 方法：`PATCH` / `DELETE`
- 路径：`/api/users/addresses/{address_id}/`
- 鉴权：**是**（`IsAuthenticated`）

`PATCH` 可更新 `name/address/phone_number/is_default`；`DELETE` 删除地址。

状态码：`200/401`

### 8.7 设为默认地址

- 方法：`POST`
- 路径：`/api/users/addresses/{address_id}/set-default/`
- 鉴权：**是**（`IsAuthenticated`）

状态码：`200/401`

## 9. Product / Categories API

### 9.1 当前实现状态

- 数据模型已存在：`Category`、`Product`、`ProductImage`（`src/backend/products/models.py`）。
- 管理后台已可维护分类和商品（`src/backend/products/admin.py`）。
- 当前未挂载公开 API：`backendCore/urls.py` 中尚未 `include("products.urls")`，且 `products/views.py` 暂无接口实现。

以下为对齐当前数据结构的接口草案，供后续开发与联调使用。

### 9.2 商品列表（草案）

- 方法：`GET`
- 路径：`/api/products/`
- 鉴权：**否**（建议 `AllowAny`）

查询参数（建议）：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| category_id | int | 否 | 按分类过滤 |
| keyword | string | 否 | 商品名模糊搜索 |
| is_active | bool | 否 | 是否上架 |
| page | int | 否 | 页码，默认 `1` |
| page_size | int | 否 | 每页数量，默认 `20` |
| ordering | string | 否 | 排序，如 `price`、`-created_at` |

响应体字段（建议）：

| 字段 | 类型 | 说明 |
|---|---|---|
| data.list | array<object> | 商品列表 |
| data.list[].id | int | 商品 ID |
| data.list[].name | string | 商品名称 |
| data.list[].price | string(decimal) | 价格 |
| data.list[].stock | int | 库存 |
| data.list[].is_active | bool | 是否上架 |
| data.list[].category_id | int | 分类 ID |
| data.list[].category_name | string | 分类名称 |
| data.list[].cover_image | string/null | 封面图 URL |
| data.pagination.page | int | 当前页 |
| data.pagination.page_size | int | 每页数量 |
| data.pagination.total | int | 总数 |

状态码（建议）：`200/400`

### 9.3 商品详情（草案）

- 方法：`GET`
- 路径：`/api/products/{product_id}/`
- 鉴权：**否**（建议 `AllowAny`）

响应体字段（建议）：

| 字段 | 类型 | 说明 |
|---|---|---|
| data.id | int | 商品 ID |
| data.name | string | 商品名称 |
| data.price | string(decimal) | 价格 |
| data.stock | int | 库存 |
| data.is_active | bool | 是否上架 |
| data.description | string | 商品描述 |
| data.category | object | 分类信息 |
| data.category.id | int | 分类 ID |
| data.category.name | string | 分类名称 |
| data.cover_image | string/null | 封面图 URL |
| data.images | array<object> | 详情图列表 |
| data.images[].image | string | 图片 URL |
| data.images[].sort_order | int | 排序 |

状态码（建议）：`200/404`

### 9.4 分类列表（草案）

- 方法：`GET`
- 路径：`/api/categories/`
- 鉴权：**否**（建议 `AllowAny`）

响应体字段（建议）：

| 字段 | 类型 | 说明 |
|---|---|---|
| data | array<object> | 分类列表 |
| data[].id | int | 分类 ID |
| data[].name | string | 分类名 |
| data[].parent_id | int/null | 父分类 ID |
| data[].sort_order | int | 排序 |

状态码（建议）：`200`

### 9.5 分类树（草案）

- 方法：`GET`
- 路径：`/api/categories/tree/`
- 鉴权：**否**（建议 `AllowAny`）

响应体字段（建议）：

| 字段 | 类型 | 说明 |
|---|---|---|
| data | array<object> | 一级分类数组 |
| data[].id | int | 分类 ID |
| data[].name | string | 分类名 |
| data[].children | array<object> | 子分类 |

状态码（建议）：`200`

### 9.6 分类下商品（草案）

- 方法：`GET`
- 路径：`/api/categories/{category_id}/products/`
- 鉴权：**否**（建议 `AllowAny`）

说明：返回某分类（可选含子分类）下商品列表；返回结构可复用“9.2 商品列表”。

状态码（建议）：`200/404`



## 10. 落文档建议流程

1. 先以本文档为“联调草案”，保证每个接口都有：方法、路径、请求体、成功/失败示例。
2. 前后端联调后，补充字段说明（类型、是否必填、枚举值）。
3. 跟随代码变更同步更新：每改 `urls.py`/`views.py`，同时改 `docs/support_api.md`。
4. 版本化维护：按里程碑增加 `v1/v2` 变更记录。
