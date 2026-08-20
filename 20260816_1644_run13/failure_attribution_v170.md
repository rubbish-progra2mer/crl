# v170 失败归因

## 类型

`MECHANISM_REDESIGN_GATE_COLLIDES_WITH_BEHAVIOR_SIGNATURE_QUALITY_DIVERSITY_AND_STRUCTURE_PARAMETER_DECOMPOSITION_PRIORS`

## 直接原因

- 按多输入执行结果形成程序行为签名并维护多样性，FunSearch 已直接实现；
- 大语言模型程序变异与 MAP-Elites 在二维机器人形态搜索上的组合，ELM 已直接实现；
- 把代码结构搜索和参数优化拆开，R* 已直接实现；
- 局部微扰、灵敏度和可达性判定只是成熟的门控组件，尚未产生超出上述三条先行的独立方法核。

## 非原因

- 不是 PACE-Bench 没有真实瓶颈；参数披露不抬高上限是明确负结果；
- 不是词元杰卡德足以度量机制差异；静态代码检查恰好表明它过于粗糙；
- 不是仓库不安全或实验环境不可用；本版在先行碰撞后主动停止，无需运行；
- 不是 v029 安全控制、Run 终局或用户终止。

## 决定

不注册实验或 Seed。保留机制差异测量警告，v171 转向结构不同的 frontier，Run 保持 `ACTIVE`。
