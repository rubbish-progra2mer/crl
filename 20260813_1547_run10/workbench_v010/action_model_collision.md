# v010 反事实语义足迹的动作模型碰撞

## 裁决

- `h-v010-001`: `prior_collision`
- 杀伤范围：淘汰“用隔离状态/响应差分学习工具前置条件、读写效果和隐式资源参数，再将所得模板交给并发协议”的当前方法核；不构成 Run-level 终局。

## 计算映射

| v010 对象 | 动作模型学习对象 |
|---|---|
| 工具模式/调用类型 | lifted action schema |
| 调用参数和响应句柄 | 显式或隐式 action arguments |
| 写前/写后状态 | state-action-state trace |
| 读依赖/适用条件 | preconditions |
| W/CREATE/DELETE | add/delete effects |
| 未见工具实例化 | lifted operator grounding |
| UNKNOWN/部分观测 | partial or local observability |

该映射不是表面类比，而是相同的输入—计算—输出。Mourão 等已经从噪声/不完整观测学习 STRIPS transition classifiers 与显式规则；Aineto 等从初末状态/轨迹学习 action model；Jansen、Gösgens 与 Geffner 的 STRIPS+ 进一步允许动作只暴露选择所需参数、其余对象由前置条件查询隐式绑定，并在部分/局部状态可见下给出等价域学习条件。

RESTler、Morest 与其谱系又把这一问题落实到黑盒 REST API：从 OpenAPI、请求/响应和执行反馈恢复生产者—消费者依赖、CRUD 关系、属性等价与动态属性图。因而“对工具 API 做配对执行以归纳资源流”也不是空白。

## 与并发智能体最近工作的组合碰撞

即便动作模型学习能产生更准确的足迹，下游用途已由 CoAgent/MTPO、Atomix、Cordon 和 Verified Concurrency 占据。候选的整体等价于：

`已有动作模型/API依赖学习 + 已有智能体事务/可串行化协议`。

没有剩余的新核心计算足以支持继续实现。AppWorld 离线足迹数据集可能有评测价值，但当前 Goal 要求方法研究种子；不能把基准构造冒充方法贡献。

## 反复活规则

除非新候选不再学习前置条件/效果/资源依赖，或能指出动作模型学习和 REST API 依赖图无法表示的并发相关对象并给出独立计算，否则不得以“语义足迹、反事实差分、资源模板、工具效果编译”换名复活。
