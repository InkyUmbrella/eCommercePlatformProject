# 电商系统项目

## 🚀 快速开始

### 1️ 环境要求
| 组件       | 版本要求      | 安装指南                     |
|------------|--------------|----------------------------|
| Python     | 3.9+         | [下载安装](https://www.python.org/downloads/) |
| MySQL      | 8.0+         | [下载安装](https://dev.mysql.com/downloads/installer/) |
| Node.js    | 16.0+        | [下载安装](https://nodejs.org/) |

### 2️ 安装步骤

#### 后端 (Django)
cd backend
pip install -r requirements.txt  (下载时记得换国内源，不然会很慢)
python manage.py migrate
python manage.py createsuperuser   (按提示创建管理员账号)

#### 前端 (Vue3)
cd ../frontend
npm install
npm run serve  (启动前端)
### 3 项目结构
````bash
ecommerce-system/  
├──src/   
    ├── backend/       (Django后端)  
    ├── frontend/      (Vue3前端)  
├── docs/          (项目文档（含API说明）)  
└── README.md      (项目介绍)