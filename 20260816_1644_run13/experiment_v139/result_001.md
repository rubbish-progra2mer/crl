# v139 Recorded 结果 001

## 记录

- 记录标识：`skillshapley-removal-target-counterexample-001`
- 状态：`SUCCESS`
- 层级：`RECORDED_NON_SUPPORTING`
- 记录文件：`experiment_v139/recorded/skillshapley-removal-target-counterexample-001/record.json`
- 程序：`workbench_v139/shapley_banzhaf_removal_counterexample.py`
- 输出：`workbench_v139/shapley_banzhaf_metrics.json`
- 程序 SHA-256：`3d46cef71229d3d5bdd3d06d8231d51ade14f06c240fbce9d19a5dc4e37e99a5`
- 输出 SHA-256：`9c99b15a56bf53c8e11adcc4919459a0899b555aff74d101d4972b6cf9a4a263`
- 记录 SHA-256：`8d9f56f42685539b60878c0cc16ac3eca042b4c696eb06881679824e8854679d`

## 预注册结果

八项断言全部通过：

- 示例游戏单调且效用位于 `[0,1]`；
- 沙普利唯一首位为 `p1`；
- 班扎夫唯一首位为 `p2`；
- 论文式单步删除下降唯一首位为 `p2`；
- 示例四个步骤均精确满足 `删除下降=班扎夫/2`；
- 32,768 个参数网格游戏中存在排序反转；
- 网格删除恒等式零违例；
- 网格单调性零违例。

## 精确数值

- 沙普利：`p1=3/11`，`p2=p3=p4=8/33`；
- 班扎夫：`p1=7/33`，`p2=8/33`，`p3=p4=2/11`；
- 全联盟均值：`5/22`；
- 删除 `p1` 的下降：`7/66`；
- 删除 `p2` 的下降：`4/33`；
- `1..32` 网格反转数：`887/32768`。

## 解释

该反例证明：在单调、有限二元实例平均的技能博弈中，沙普利首位可以不是均匀联盟删除验证的最佳首位；第一删除点严格对应班扎夫排序。因此目标论文的删除曲线不是沙普利值独有的行为有效性验证，班扎夫是应纳入的最近公平基线。

该结果不证明目标论文三个真实技能上的曲线错误，不否定沙普利的公平分摊性质，也不评价 BAES 对沙普利值的近似精度。
