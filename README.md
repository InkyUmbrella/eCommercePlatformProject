# 电商平台项目（Ecommerce Platform）

一个前后端分离的电商平台示例项目：

- 后端：Django + Django REST Framework + MySQL
- 前端：Vue 3 + Vite + Element Plus
- 文档：部署说明、接口文档、Postman 集合

## 1. 目录结构

```text
ecommerce_platform_project/
├─ docs/                         # 项目文档（部署、API、Postman）
├─ src/
│  ├─ backend/                   # Django 后端
│  └─ frontend/
|— __init__.py
|─ README.md
L— .gitignore
```

## 2. 环境要求

| 组件 | 版本建议 |
|---|---|
| Python | 3.11+ |
| MySQL | 8.0+ |
| Node.js | 20.19+（或 22.12+） |
| npm | 10+ |

## 3. 后端启动（Django）

在仓库根目录执行：

```powershell
cd src/backend
```

### 3.1 配置环境变量

```powershell
Copy-Item .env.example .env
```

然后按实际数据库信息修改 `.env`，至少包含以下字段：

```dotenv
DEBUG=True
SECRET_KEY=replace_me_with_secure_key
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=replace_with_db_name
DB_USER=replace_with_db_user
DB_PASSWORD=replace_with_db_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 3.2 初始化数据库（可选脚本）

仓库已提供 MySQL 初始化脚本：`docs/db_init.sql`

```bash
mysql -u root -p < docs/db_init.sql
```

### 3.3 安装依赖并迁移

```powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

默认访问：

- 管理后台：`http://127.0.0.1:8000/admin/`
- API 前缀：`/api/users/`、`/api/cart/`、`/api/orders/`、`/api/payment`、`/api/support/`

## 4. 前端启动（Vue 3 + Vite）

在仓库根目录执行：

```powershell
cd src/frontend/frontend-core
npm install
npm run dev
```

默认访问：

- 前端开发地址：`http://127.0.0.1:5173/`（或终端输出地址）

## 5. 常用命令

### 后端

```powershell
cd src/backend
python manage.py test
```

### 前端

```powershell
cd src/frontend/frontend-core
npm run build
npm run preview
```

## 6. 文档导航

- 部署说明：`docs/deployment_guide.md`
- 支撑 API（联调文档）：`docs/support_api.md`
- 订单状态说明：`src/backend/docs/order_status.md`
- Postman 集合：
    - `docs/postman/day3_users_auth.postman_collection.json`
    - `docs/postman/day4_addresses.postman_collection.json`

## 7. 技术栈

后端主要依赖：

- Django 6
- djangorestframework
- djangorestframework-simplejwt
- django-cors-headers
- drf-yasg
- mysqlclient / PyMySQL

前端主要依赖：

- Vue 3
- Vite
- Vue Router
- Element Plus
- Axios

## 8. 常见问题

- 启动时报 `SECRET_KEY is required`：检查 `src/backend/.env` 是否存在且 `SECRET_KEY` 非空。
- MySQL 连接失败：核对 `DB_*` 配置与数据库权限。
- 前端命令无效：该项目使用 Vite，请使用 `npm run dev`，不是 `npm run serve`。
