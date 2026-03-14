# 最终交付规范与步骤

最后更新：2026-03-14

## 1. 交付目标

形成一套可验收、可复现、可归档的项目交付包，确保接收方可以按文档独立完成：

1. 环境搭建
2. 服务启动
3. 接口联调
4. 前端业务演示
5. 结果验收

## 2. 交付物清单（必须）

1. 源码仓库（本项目）
2. 部署文档：`docs/deployment_guide.md`
3. API 支撑文档：`docs/support_api.md`
4. 录屏脚本：`docs/screen_recording_script_outline.md`
5. 录屏成片：`docs/` 下新增或外链说明（建议 mp4）
6. Postman 集合：
   - `docs/postman/day3_users_auth.postman_collection.json`
   - `docs/postman/day4_addresses.postman_collection.json`
   - `docs/postman/day5_6_cart.postman_collection.json`
   - `docs/postman/day7_8_orders.postman_collection.json`
7. 初始化 SQL：`docs/db_init.sql`

## 3. 交付规范（DoD）

### 3.1 运行规范

1. 后端可启动且无阻塞错误
2. 前端可启动且可访问首页
3. 数据库迁移可执行通过

### 3.2 功能规范

至少覆盖以下闭环：

1. 用户注册/登录
2. 地址增改与默认地址
3. 商品浏览与加购
4. 购物车结算与创建订单
5. 订单查询与状态流转（取消/收货/退款至少演示其一）
6. 客服留言提交（管理员回复可选）

### 3.3 文档规范

1. 文档路径清晰、标题统一
2. 每份文档包含最后更新时间
3. 命令可直接复制执行
4. 与代码当前实现一致（路径、参数、接口返回）

### 3.4 可追溯规范

1. 录屏与文档版本一致
2. 录屏中展示的核心路径必须与路由一致
3. 提供最小复现顺序（见第 4 节）

## 4. 最终交付步骤（执行顺序）

### Step 1：环境检查

1. 检查 Python、Node、MySQL 版本
2. 确认 `.env` 已配置
3. 确认数据库账号有目标库权限

### Step 2：后端准备

1. 进入 `src/backend`
2. 安装依赖：`pip install -r requirements.txt`
3. 执行迁移：`python manage.py migrate`
4. 启动服务：`python manage.py runserver`

### Step 3：前端准备

1. 进入 `src/frontend/frontend-core`
2. 安装依赖：`npm install`
3. 启动服务：`npm run dev`

### Step 4：联调验证

1. 按 `docs/support_api.md` 验证关键接口
2. 按 Postman 集合跑通 day3-day8 关键请求
3. 记录失败项与修复结果（如有）

### Step 5：业务链路验收

1. 按 `docs/screen_recording_script_outline.md` 完整走一遍
2. 录制并导出演示视频
3. 检查视频中页面路径、点击动作、结果提示是否完整

### Step 6：交付包整理

1. 核对第 2 节交付物是否齐全
2. 补充变更说明（本次新增/修复点）
3. 统一命名并打包（zip 或仓库 tag）

### Step 7：交付确认

1. 向接收方发送交付包与文档入口
2. 现场或远程做一次 10 分钟演示
3. 收集验收意见并记录结论

## 5. 建议命名与版本策略

1. 交付包命名：`ecommerce_platform_delivery_YYYYMMDD_vX.Y.Z.zip`
2. 录屏命名：`ecommerce_demo_YYYYMMDD_vX.Y.Z.mp4`
3. 文档更新时间统一写在文件头部
4. 仓库建议打 tag：`delivery/vX.Y.Z`

## 6. 交付前自检清单

1. 前后端可在新环境按文档启动
2. 录屏路径与脚本一致
3. 关键截图或视频片段清晰可读
4. 文档无明显过期路径或命令
5. 提供已知问题列表（如存在）与规避方法
