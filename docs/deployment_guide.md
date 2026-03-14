# 电商平台后端部署说明（终稿）

最后更新：2026-03-14

> 目标：完成后端基础部署，覆盖 **MySQL 建库、数据库导入、环境变量、数据库迁移、创建超级管理员**。
> 
> 适用范围：当前仓库 Django 后端（`src/backend`），不包含 Nginx / Gunicorn / HTTPS 等生产网关配置。

## 1. 前置条件

请先准备以下环境：

- Python 3.11+（建议 3.11 或 3.12）
- MySQL 8.0+
- pip 可用

项目后端目录：`src/backend`

---

## 2. MySQL 建库与授权

### 2.1 登录 MySQL

```bash
mysql -u root -p
```

### 2.2 执行建库与授权（示例）

> 以下示例与 Django 配置一致，使用 `utf8mb4`。

```sql
CREATE DATABASE ecommerce_platform
	DEFAULT CHARACTER SET utf8mb4
	DEFAULT COLLATE utf8mb4_0900_ai_ci;

CREATE USER 'ecom_user'@'%' IDENTIFIED BY 'StrongPassword_ChangeMe_2026!';
GRANT ALL PRIVILEGES ON ecommerce_platform.* TO 'ecom_user'@'%';
FLUSH PRIVILEGES;
```

### 2.3 可选：使用脚本初始化

仓库已提供脚本模板：`docs/db_init.sql`

```bash
mysql -u root -p < docs/db_init.sql
```

### 2.4 数据库导入（推荐）

> 用于快速导入初始化结构/测试数据。请先确认目标数据库已创建，且 `DB_NAME` 与导入目标一致。

#### 方式 A：导入仓库初始化脚本（推荐）

从仓库根目录执行：

```bash
mysql -u ecom_user -p ecommerce_platform < docs/db_init.sql
```

如果你已经在 `src/backend` 目录，可改用：

```bash
mysql -u ecom_user -p ecommerce_platform < ..\..\docs\db_init.sql
```

#### 方式 B：导入已有 SQL 备份文件（可选）

```bash
mysql -u ecom_user -p ecommerce_platform < your_backup.sql
```

#### 导入后校验

登录 MySQL 并检查目标库：

```sql
USE ecommerce_platform;
SHOW TABLES;
```

若需继续使用 Django 迁移体系，导入后仍建议执行一次迁移（见第 5 节）。

---

## 3. 配置环境变量（.env）

后端会从 `src/backend/.env` 读取配置（已在 settings 中启用 `python-dotenv`）。

### 3.1 复制模板

#### Windows PowerShell

```powershell
cd src/backend
Copy-Item .env.example .env
```

#### Linux / macOS

```bash
cd src/backend
cp .env.example .env
```

### 3.2 编辑 `.env`（示例）

```dotenv
DEBUG=False
SECRET_KEY=replace_with_a_long_random_secret_key
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=ecommerce_platform
DB_USER=ecom_user
DB_PASSWORD=StrongPassword_ChangeMe_2026!
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 3.3 注意事项

- `SECRET_KEY` 必填；为空时 Django 将拒绝启动。
- `ALLOWED_HOSTS` 使用英文逗号分隔。
- 生产环境请设置 `DEBUG=False`。
- `.env` 已在 `.gitignore` 中忽略，不要提交真实密钥。

---

## 4. 安装依赖

> 请在 `src/backend` 目录执行。

### 4.1 创建并激活虚拟环境（可选但推荐）

#### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4.2 安装依赖包

```bash
pip install -r requirements.txt
```

---

## 5. 执行数据库迁移

> 确保当前目录为 `src/backend`。

```bash
python manage.py migrate
```

如迁移成功，数据库会生成 Django 核心表与业务应用表。

---

## 6. 创建超级管理员

```bash
python manage.py createsuperuser
```

按提示输入用户名、邮箱和密码即可。

---

## 7. 启动与验证

### 7.1 启动服务

```bash
python manage.py runserver
```

### 7.2 验证项

1. 访问 `http://127.0.0.1:8000/admin/`
2. 使用上一步创建的超级管理员登录
3. 确认后台可正常进入（说明迁移与权限配置成功）

---

## 8. 常见问题排查

### 8.1 `SECRET_KEY is required in .env`

- 检查 `src/backend/.env` 是否存在
- 检查 `SECRET_KEY` 是否为空

### 8.2 无法连接 MySQL / 迁移报错

- 检查 `DB_NAME / DB_USER / DB_PASSWORD / DB_HOST / DB_PORT`
- 检查 MySQL 服务是否启动
- 检查 MySQL 账户是否有目标数据库权限

### 8.3 `Access denied for user`

- 重新执行授权语句并 `FLUSH PRIVILEGES`
- 确认 `.env` 与 MySQL 用户密码一致

---

## 9. 最小部署命令清单

```bash
cd src/backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

