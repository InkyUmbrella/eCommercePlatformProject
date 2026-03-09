# Order Status && Transitions

## 1. Status codes
- `pending_payment`:待支付
- `pending_shipment`:待发货
- `pending_receipt`:待收货
- `completed`:已完成
- `cancelled`:已取消
- `refund_processing`:售后中

## 2. Allowed transitions
| From \ To | `pending_payment` | `pending_shipment` | `pending_receipt` | `completed` | `cancelled` | `refund_processing` |
|----------|------------------:|-------------------:|------------------:|------------:|------------:|--------------------:|
| `pending_payment` |                 - |                  ✅ |                 - |           - |           ✅ |                   - |
| `pending_shipment` |                 - |                  - |                 ✅ |           - |           ✅ |                   - |
| `pending_receipt` |                 - |                  - |                 - |            ✅ |           - |                   ✅ |
| `completed`|                 - |                  - |                 - |           - |           - |                   ✅ |
| `cancelled`|                 - |                  - |                 - |           - |           - |                   - |
| `refund_processing`|                 - |                  - |                 - |           ✅ |           ✅ |                   - |

## 3.Trigger Events
| 状态变化 | 触发方    | 触发动作            |
|---|--------|-----------------|
| `pending_payment` -> `pending_shipment` | 用户/系统  | 支付成功（模拟支付完成）    |
| `pending_payment` -> `cancelled` | 用户/系统  | 用户取消 / 支付超时自动取消 |
| `pending_shipment` -> `pending_receipt` | 管理员/商家 | 发货（后台标记发货）      |
| `pending_shipment` -> `cancelled` | 用户/管理员 | 发货前取消           |
| `pending_receipt` -> `completed` | 用户/系统  | 用户确认收货（或超时自动确认） |
| `pending_receipt` -> `refund_processing` | 用户/管理员 | 收货前进入售后         |
| `completed` -> `refund_processing` | 用户/管理员 | 收货后进入售后         |
| `refund_processing` -> `completed` | 用户/商家  | 售后后订单完成         |
| `refund_processing` -> `cancelled` | 用户/商家  | 售后后订单取消         |


## 4.Constraint
- 订单状态变更必须使用统一方法 `Order.change_status(new_status)`
- 订单状态初始值必须为`pending_payment`
