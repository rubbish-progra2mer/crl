# v166 失败归因

## 类型

`CONTEXTUAL_MESSAGE_TRAJECTORY_VALUE_CLOSED_BY_COALITION_UTILITY_SIGNED_RELATION_AND_ROUTING_CERTIFICATE_PRIORS`

## 直接原因

- DHD 已把轨迹价值定义为指定消息池和整合器下的上下文量，并分别测量单消息与池内留一效应；
- 动态联盟形成已用任务条件化集合效用、Shapley 值和次模／非单调集合优化处理交互贡献；
- SIGMA 已显式建模消息间可信、冲突和中性关系；
- RouteGuard 已给出多顾问路由收益的有限样本部署证书；
- 因而跨池变号只能作为现有集合选择方法的诊断，不产生新的不可替代计算。

## 非原因

- 不是缺少公开数据：目标论文附属材料足以做离线重放统计；
- 不是观察到变号或不变号：逐条结果尚未下载或查看；
- 不是模型调用成本、硬件不足或实验不可执行；
- 不是 v029 安全边界、科研反证、Run 终局或用户终止。

## 决定

不注册实验或 Seed。将消息池与整合器上下文列为轨迹价值标签的必需元数据；v167 转向结构不同的 frontier，Run 保持 `ACTIVE`。
