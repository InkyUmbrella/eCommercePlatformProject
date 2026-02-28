# Day1（分工1：后端核心）完成指南

> 你现在已经有 Django + Vue 框架，这份指南对应你表格里的 Day1 目标：
> 1) 建立 Django 工程骨架；2) 统一返回体与异常处理；3) 起草交易域 API 草案。

## 1. 本次已落地内容

- Django 后端新增 `common` 模块，提供：
  - 统一成功/失败返回体（`api_success` / `api_error`）。
  - 业务异常 `AppException`。
  - 全局异常中间件 `GlobalExceptionMiddleware`，自动把异常转成统一 JSON。
- 新增 `trading` 模块，提供 Day1 的交易域接口草案：
  - `GET /api/v1/transactions/draft`
- 主路由已挂载 `api/v1/` 前缀，方便后续 Day2~Day10 按模块扩展。

## 2. Day1 对照验收清单

你可以按下面 4 项打钩：

1. **工程骨架**
   - [x] 有独立 Django project
   - [x] 有独立业务 app（`trading`）
   - [x] 路由分层（`backendCore.urls` -> `trading.urls`）

2. **统一返回体**
   - [x] 成功返回结构：`{code, message, data}`
   - [x] 失败返回结构：`{code, message, data}`

3. **异常处理**
   - [x] 业务异常可控返回（HTTP 4xx）
   - [x] 未知异常统一返回（HTTP 500）

4. **交易域 API 草案**
   - [x] 覆盖购物车、订单预览、下单、支付等主链路

## 3. 本地自测命令

```bash
# 进入后端
cd src/backend

# 运行 Django 自检
python manage.py check

# 启动服务
python manage.py runserver

# 访问草案接口
curl http://127.0.0.1:8000/api/v1/transactions/draft
```

预期响应（示例）：

```json
{
  "code": 0,
  "message": "transaction api draft",
  "data": {
    "module": "transaction-core",
    "version": "v1",
    "apis": []
  }
}
```

## 4. 你今天可以对组员同步的话术（可直接复制）

“Day1 分工1已完成：后端骨架、统一返回体、全局异常处理、交易域 API 草案接口已落地。后续 Day2 起可直接在 `api/v1` 下按模块补齐用户/购物车/订单等正式接口实现。”
