# Order Status && Transitions

## 1. Status codes
- `pending_payment`:待支付
- `pending_shipment`:待发货
- `pending_receipt`:待收货
- `completed`:已完成
- `cancelled`:已取消

## 2. Allowed transitions
| From \ To | `pending_payment` | `pending_shipment` | `pending_receipt` | `completed` | `cancelled` |
|----------|---:|---:|---:|---:|----------:|
| `pending_payment` | - | ✅ | - | - |         ✅ |
| `pending_shipment` | - | - | ✅ | - |         ✅ |
| `pending_receipt` | - | - | - | ✅ |         ✅ |
| `completed`| - | - | - | - |         - |
| `cancelled`| - | - | - | - |         - |

## 3.Trigger Events
| 状态变化 | 触发方 | 触发动作 |
|---|---|---|
| `pending_payment` -> `pending_shipment` | 用户/系统 | 支付成功（模拟支付完成） |
| `pending_payment` -> `cancelled` | 用户/系统 | 用户取消 / 支付超时自动取消 |
| `pending_shipment` -> `pending_receipt` | 管理员/商家 | 发货（后台标记发货） |
| `pending_shipment` -> `cancelled` | 用户/管理员 | 发货前取消（是否允许取决于业务，此项目允许） |
| `pending_receipt` -> `completed` | 用户/系统 | 用户确认收货（或超时自动确认） |
| `pending_receipt` -> `cancelled` | 用户/管理员 | 收货前取消（此项目允许） |

## 4.Constraint
- 订单状态变更必须使用统一方法 `Order.change_status(new_status)`
- 订单状态初始值必须为`pending_payment`