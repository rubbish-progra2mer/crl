# v058 研究图谱

## 命令解释链与指令表面

- [QuoteBench](https://arxiv.org/abs/2608.13547) 已用 56 个任务和额外解析器精确分解模型生成、传输边界损伤与模型补偿；原始与部署路径配对正是该问题的核心评价。
- [Harness-IF](https://arxiv.org/abs/2608.11727) 已跨五类指令表面评价操作规则，并用 Against-Prior Accuracy 区分真实遵循与行为巧合。
- 剩余的参数向量、抽象语法树或单点转义修复是成熟编译/接口工程，也回撞 `v003`、`v033`。

## 技能与长期上下文

- [Agent Skills Can Be Harmful](https://arxiv.org/abs/2608.11888) 已用差分运行归因 307 个技能诱导失败，并指出相关技能也会遗漏任务元素或造成过度验证。
- [SkillSentry](https://arxiv.org/abs/2608.09253) 已以技能领域专用语言、历史轨迹和运行时监控提高技能执行稳定性。
- [The Sleeping Agent](https://arxiv.org/abs/2608.11775) 已将摘要压缩的时间信息丢失定位到具体提示机制，并用一句保留规则恢复。
- [Why Does CLAUDE.md Keep Growing?](https://arxiv.org/abs/2608.11095) 已定义灾难性记忆并用理由注释抑制规则无界增长。
- 这些工作分别覆盖技能归因、运行时保证、选择性保留和规则生命周期；继续组合会回撞 `v042`、`v045`。

## 长期主动性

- [VibeLifeBench](https://arxiv.org/abs/2608.10875) 提供多周、静默变化和隐含约束任务。
- [Long-term Task-oriented Agent](https://arxiv.org/abs/2601.09382) 已实现意图条件监测与事件触发跟进；[ProActor](https://aclanthology.org/2026.acl-long.832/) 已以机会时间窗和时机奖励训练主动调度；[Do Proactive Agents Really Need an LLM](https://arxiv.org/abs/2605.30152) 又以时序图模型完成低成本事件触发。
- 因此“何时检查/唤醒/行动”已有直接数据、策略与系统覆盖。

## 自治科研流程

- [Beyond Final Scores](https://arxiv.org/abs/2608.13417) 已在 36 个长程研发任务上分解问题框定、执行和反馈控制。
- [Recovering Wasted Compute in Autoresearch Agents](https://arxiv.org/abs/2608.10424) 已直接处理重复调试、缺少超参数调优、树搜索不探索和分析不驱动决策。
- [Long-Horizon Autonomous Architecture Research](https://arxiv.org/abs/2608.01995) 已把提交/丢弃规则识别为贪心爬山，并提出分叉和多样化搜索。
- 继续做全局调试顾问、搜索分叉或过程评分会回撞 `v020`、`v055` 及这些直接工作。

## 保留到下一版本的问题

- [TRACES](https://arxiv.org/abs/2608.11415) 报告：面对源自撤稿、欺诈或伪科学论文的科学上貌似合理的研究设计请求，模型往往继续深度参与；匹配结构对照指向话题关键词而非稳健的前提判断。
- 这一失败发生在实验设计之前，不等同于工具可靠性或运行后验证。`v059` 将检查“先验证科学前提、再允许条件性设计”是否已有直接方法覆盖，以及强提示能否吸收。
