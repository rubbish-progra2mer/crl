# v063 研究图谱

## 已否决的脚手架迁移

- [Life-Harness](https://arxiv.org/abs/2605.22166) 已从单一 Qwen 骨干演化脚手架并迁移到另外 17 个模型。
- [EVOTOOL](https://aclanthology.org/2026.acl-long.2016/) 已直接评价工具使用策略的跨模型和跨数据集迁移。
- [HarnessForge](https://arxiv.org/abs/2606.01779) 与 [Co-Harness](https://arxiv.org/abs/2607.22688) 已联合优化脚手架与模型策略。

因此不沿跨骨干极小极大脚手架继续。

## 工具恢复最近工作

- [Bench2Robust](https://arxiv.org/abs/2608.11977) 显式构造重试、切换和不可解场景，并用 Bayesian Tool Memory 提供回退图、约束、单工具—错误 Beta 恢复率与源—目标切换率。
- 其注入核明确写明每个工具调用独立采样噪声；替代路径是功能等价类，没有共同故障域或从已失败工具向未调用同域工具传播后验。
- [Graph-Based Self-Healing Tool Routing](https://arxiv.org/abs/2603.01548) 在工具失败后把该工具边权置为无穷并重算最短路，但公开方法仍以工具边为故障单元。
- [Failing Tools](https://openreview.net/pdf/2be5795add6ec19f401efc71c99e69f5dea50e1c.pdf) 与 [Verified Tool Calls](https://arxiv.org/abs/2608.02645) 分别覆盖运行时恢复和非原子调用验证，未解决共享后端冗余失真。
- [STAR](https://arxiv.org/abs/2605.10057) 已把类型化执行状态外化为条件转移路由，因此“按故障类型切换”本身不是新内核。
- 系统领域已有[相关故障风险最小化路由](https://ieeexplore.ieee.org/document/8713864)与[依赖/故障域分析](https://www.usenix.org/publications/loginonline/hunting-risky-dependencies)；共享故障域传播不能只凭迁入智能体场景主张新颖性。

## 候选内核

把工具图提升为工具—故障域二部依赖图：观测错误先定位到本地适配器或共享服务，再对相关未调用工具更新可用性，最后按条件成功概率与执行成本重路由。相对源—目标成对统计，它可在同域多工具间共享证据并对新工具按依赖元数据零样本传播。

该内核借用经典共同原因故障建模；若模型仅凭原始元数据或一句原则即可稳定做对，独立编译层没有方法价值。

去推荐语消融又给出另一侧边界：若只有把最终最佳回退直接写入卡片才成功，则收益是答案转抄；若把选择也固化为确定性路由，方法差分被经典依赖图与成本路由吸收。v063 实际命中后一边界。
