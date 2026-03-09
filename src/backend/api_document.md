\# 商品相关接口文档



\## 基础信息

\- 基础URL: `http://127.0.0.1:8000/api`

\- 响应格式: JSON



---



\## 1. 分类接口



\### 获取所有分类

\- \*\*URL\*\*: `/categories/`

\- \*\*方法\*\*: GET

\- \*\*响应示例\*\*:

```json

\[

&nbsp; {

&nbsp;   "id": 1,

&nbsp;   "name": "电子产品",

&nbsp;   "parent": null,

&nbsp;   "children": \[

&nbsp;     {

&nbsp;       "id": 2,

&nbsp;       "name": "手机",

&nbsp;       "parent": 1,

&nbsp;       "children": \[]

&nbsp;     }

&nbsp;   ]

&nbsp; }

]

