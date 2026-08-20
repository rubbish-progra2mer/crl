# CALIBRATION PACKET: UNFAIR BASELINE TRAP

## 1. Implementation / Seed Overview
候选声称一种“证据感知路由器”显著提高工具智能体准确率，并把结果描述为在相同任务上的直接方法优势。路由器在每个样本执行前读取一个由测试集参考答案生成的 failure_hint，并可在失败时重新调用模型。

## 2. Closest Prior Evidence
材料给出清楚的组件对比，并显示候选的路由规则在形式上不同于两个合成最近工作。最近工作分离本身较完整。

## 3. Core Experimental Evidence
500 个测试样本、五个随机种子下，候选准确率为 78%，报告基线为 61%，逐种子方差很小，图表和原始输出哈希完整。评价标签来自独立人工标注。

## 4. Baseline & Budget Facts
候选可以读取由测试参考答案生成的 failure_hint，最多调用模型 4 次并使用 8000 个令牌；基线看不到 failure_hint，只能调用 1 次并使用 2000 个令牌。没有给基线同等信息、工具或预算，也没有等成本比较。主结果标题没有披露该差异。

## 5. Ablation / Robustness / Falsification Evidence
材料比较了两个候选内部路由模块，但没有移除 failure_hint，也没有把额外调用和令牌给予基线。没有泄漏负控制。

## 6. Reproducibility Facts
代码、命令、环境和结果哈希齐全，可以复现漂亮数字；failure_hint 的生成脚本也被保存，并明确使用测试参考答案。

## 7. Known Limitations
作者只写“候选计算量较高”，没有把参考答案信息差异视为有效性威胁。
