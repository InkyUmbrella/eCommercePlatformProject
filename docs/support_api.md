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

## 3. 购物车 API

### 3.1 获取购物车

- 方法：`GET`
- 路径：`/api/cart/`

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

### 3.3 更新购物车项

- 方法：`PATCH`
- 路径：`/api/cart/items/{item_id}/`

请求体（至少传一个）：

```json
{
	"quantity": 2,
	"selected": true
}
```

## 4. 订单 API

### 4.1 下单确认

- 方法：`POST`
- 路径：`/api/orders/confirm/`

请求体：

```json
{
	"address_id": 1,
	"note": "请尽快发货"
}
```

校验：

- `address_id` 必填

### 4.2 创建订单

- 方法：`POST`
- 路径：`/api/orders/`

请求体：

```json
{
	"address_id": 1
}
```

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

## 6. 用户 API

以下接口已在 `src/backend/users/urls.py` 定义

- `POST /api/users/register/`
- `POST /api/users/login/`
- `POST /api/users/refresh/`
- `GET /api/users/me/`

## 7. 落文档建议流程

1. 先以本文档为“联调草案”，保证每个接口都有：方法、路径、请求体、成功/失败示例。
2. 前后端联调后，补充字段说明（类型、是否必填、枚举值）。
3. 跟随代码变更同步更新：每改 `urls.py`/`views.py`，同时改 `docs/support_api.md`。
4. 版本化维护：按里程碑增加 `v1/v2` 变更记录。
