-- =========================================================
-- MySQL 初始化脚本（开发/测试环境示例）
-- 对应 src/backend/.env 中的 DB_* 变量
-- 最后更新：2026-03-11
-- =========================================================

-- 1) 创建数据库
CREATE DATABASE IF NOT EXISTS ecommerce_platform
	DEFAULT CHARACTER SET utf8mb4
	DEFAULT COLLATE utf8mb4_0900_ai_ci;

-- 2) 创建应用账户（如已存在可改为先 DROP 或手动维护）
CREATE USER IF NOT EXISTS 'ecom_user'@'%' IDENTIFIED BY 'StrongPassword_ChangeMe_2026!';

-- 3) 授权
-- 开发环境可使用 ALL PRIVILEGES；生产环境建议按最小权限原则收敛。
GRANT ALL PRIVILEGES ON ecommerce_platform.* TO 'ecom_user'@'%';
FLUSH PRIVILEGES;

-- 4) 验证（可选）
SHOW DATABASES;
SELECT User, Host FROM mysql.user WHERE User = 'ecom_user';

