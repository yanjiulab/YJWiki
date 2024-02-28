# Linux 网络管理

## Sysrepo

Module change subscriptions
用于订阅配置改变
·sr_module_change_subscribe· 函数

事件：

- SR_EV_CHANGE
- SR_EV_DONE
- SR_EV_ABORT

Operational subscriptions

客户端获取时提供数据
·sr_oper_get_items_subscribe· 函数

RPC subscription

·sr_rpc_subscribe_tree· 函数
sr_rpc_subscribe

The RPC callback receives RPC inputs, and should then call the RPC and fill the output libyang tree. An example is available in the generic-sd-bus-plugin. The variant without the tree postfix shouldn’t be used, as it only exists for legacy reasons.

sr_rpc_subscribe_tree

notifications subscription

sr_noti_send
sr_notif_subscribe

sr_unsubscribe
