# CALIBRATION PACKET: WEAK

## 1. Implementation / Seed Overview
我们在一个语言模型智能体回答后追加“请反思并给出更好答案”，然后从原答案和反思答案中选择模型自称更好的一个。我们声称该方法普遍提高智能体可靠性。changed computation、适用边界和可证伪机制未进一步定义。

## 2. Closest Prior Evidence
作者知道“反思”和“自我改进”方向可能存在相关工作，但没有给出最近工作、检索范围、组件比较或实质差异。

## 3. Core Experimental Evidence
在人工挑选的 20 个任务上，新实现答对 16 个，原实现答对 13 个。正确性由产生答案的同一个模型自行判断。只运行一次，没有原始逐样本输出、随机种子或独立标签。

## 4. Baseline & Budget Facts
新实现最多调用模型 3 次、使用约 3000 个令牌；基线调用 1 次、使用约 1000 个令牌。没有同预算基线，也没有披露选择器是否看到参考答案。

## 5. Ablation / Robustness / Falsification Evidence
NOT PROVIDED

## 6. Reproducibility Facts
没有代码、提交身份、完整提示、环境、命令或输出哈希。只有一段结果总结。

## 7. Known Limitations
任务是人工挑选的；评价器与方法同源；预算不公平；没有最近工作审计或复现材料。
