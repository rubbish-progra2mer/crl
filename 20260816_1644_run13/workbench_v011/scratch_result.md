# v011 公开分叉标签密度审计

## 数据与可复现性

- 来源：`ashritha0907/replay-gap-trajectories` 的 `rollouts_index.jsonl.gz`。
- 本地 SHA-256：`A19E70F53CDDAEB925055DDEFB69CE92FABE0C102CA7882E6D998AE1FB4BC7E7`。
- 行数：896；其中基础轨迹 179 行、分叉轨迹 717 行。
- 配对键：`(run, instance_id, fork_step)`；要求同时存在 `small` 与 `large` 分支。
- 分析脚本：`workbench_v011/analyze_public_forks.py`。
- 机器结果：`workbench_v011/public_fork_label_audit.json`。

## 结果

- 完整同状态小/大模型对：358。
- 大模型单独成功：5。
- 小模型单独成功：0。
- 两者均成功：0。
- 两者均失败：353。
- 成功处理差异率：5/358 = 1.3966%。
- 95% 威尔逊区间：0.5980%–3.2273%。
- 同模型控制相对基础轨迹的成功翻转：0。
- 随机 20% 测试集的有效成功差异期望值：1.0。

## 解释边界

该审计只否决“用这份终局二元结果直接训练并可信评测路由器”的可执行性，不否决更高成功率环境、稠密过程奖励或新的主动分叉采样方法。
