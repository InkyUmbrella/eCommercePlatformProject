# eCommercePlatformProject

前后端分离电商项目：
- 后端：Django + Django REST Framework + MySQL
- 前端：Vue 3 + Vite + Element Plus

## 目录结构

```text
.
├─ docs/
│  ├─ postman/
│  ├─ db_init.sql
│  ├─ deployment_guide.md
│  └─ support_api.md
├─ postman/
│  └─ collections/
├─ src/
│  ├─ backend/
│  └─ frontend/frontend-core/
└─ README.md
```

## 环境要求

- Python 3.11+
- MySQL 8+
- Node.js 20+
- npm 10+

## 后端启动

在仓库根目录执行：

```powershell
cd src/backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

默认地址：`http://127.0.0.1:8000`

### 后端主要 API 前缀

- `/api/users/`
- `/api/cart/`
- `/api/orders/`
- `/api/products/`
- `/api/categories/`
- `/api/home/`
- `/api/payment/`
- `/api/support/`

## 前端启动

```powershell
cd src/frontend/frontend-core
npm install
npm run dev
```

默认地址：`http://127.0.0.1:5173`

前端打包：

```powershell
npm run build
```

## 订单主链路（当前已实现）

- 确认订单：`POST /api/orders/confirm/`
- 创建订单：`POST /api/orders/`
- 支付订单：`POST /api/orders/{order_id}/pay/`
- 订单列表：`GET /api/orders/?page=1&page_size=10&status=&search=`
- 订单详情：`GET /api/orders/{order_id}/`
- 取消订单：`POST /api/orders/{order_id}/cancel/`
- 确认收货：`POST /api/orders/{order_id}/confirm-receive/`
- 发起售后：`POST /api/orders/{order_id}/refund/`
- 售后完成：`POST /api/orders/{order_id}/refund-complete/`
- 查看物流：`GET /api/orders/{order_id}/logistics/`

## 商品与首页接口

- 商品列表：`GET /api/products/`
- 商品详情：`GET /api/products/{id}/`
- 新品列表：`GET /api/products/new/`
- 分类列表：`GET /api/categories/`
- 首页轮播：`GET /api/home/banners/`

## Postman 文件

### docs/postman（JSON，可直接导入）

- `docs/postman/day3_users_auth.postman_collection.json`
- `docs/postman/day4_addresses.postman_collection.json`
- `docs/postman/day5_6_cart.postman_collection.json`
- `docs/postman/day7_8_orders.postman_collection.json`

### postman/collections（YAML）

- `postman/collections/Day3 Users Auth APIs/`
- `postman/collections/Day4 Users Address APIs/`
- `postman/collections/Day5-6 Cart APIs/`
- `postman/collections/Day7 Orders APIs/`

## 联调建议顺序

1. 注册/登录，拿到 `access_token`
2. 新增并设置默认地址
3. 创建商品（后台）并加入购物车
4. 订单确认 -> 创建 -> 支付
5. 订单列表/详情
6. 取消、收货、售后、物流接口验证

## 常见问题

- 401 未授权：检查 `Authorization: Bearer {{access_token}}`
- MySQL 连接失败：检查 `.env` 中 `DB_*` 配置
- 迁移异常：先 `python manage.py showmigrations` 再补齐缺失迁移
- 前端构建 warning（chunk 体积大）：不影响功能，可后续做按路由拆包优化
