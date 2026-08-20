<!-- crl-v3-evidence-ids
["ev-p069-description-induced-preference","ev-p069-identical-tool-order-bias","ev-p073-internal-confidence-misalignment","ev-p073-execution-supervised-probe","ev-p081-independent-path-majority-aggregation","ev-p081-fixed-answer-space-boundary"]
-->
# 研究地图

## 已观察失败与边界

P069 证明工具描述和排列能显著改变工具偏好，功能相同工具也表现出位置偏差。[[evidence:ev-p069-description-induced-preference]] [[evidence:ev-p069-identical-tool-order-bias]] 但 provider 使用份额变化不自动等于任务正确性下降，因此 v003 只研究有唯一正确工具的选择任务。

内部置信度也不能直接当作真实执行成功概率；ProbeCal 需要执行标签训练隐藏表示探针。[[evidence:ev-p073-internal-confidence-misalignment]] [[evidence:ev-p073-execution-supervised-probe]]

## 干预阶段

真实工具调用前：便宜模型分别读取正序和逆序的同一工具菜单；若规范工具身份不同则升级强模型，否则执行共同选择。

## 使用论题、价值桥与机制需求

需要证明无标签顺序分歧能富集便宜模型错误，进而在任务成功—费用曲线上优于始终便宜与始终昂贵。只证明存在顺序偏差或提高一致率不够。

## 操作符与竞争内核

- K1：便宜模型单次正序选择。
- K2：便宜模型正序、逆序各一次；一致时采用，分歧时强模型规范顺序裁决。
- K3：始终强模型。
- K4：同候选预算的独立路径/多数聚合；固定预算 self-consistency 是额外调用解释的必要比较器。[[evidence:ev-p081-independent-path-majority-aggregation]] [[evidence:ev-p081-fixed-answer-space-boundary]]
- 有监督上界：ProbeCal，但它需要标签和隐藏表示，信息条件不同。

## 决定性工作台

`workbench_v003/` 预声明 24 个任务、16 个中性描述工具，覆盖网页/内部知识、数据库读写、日历读写、邮件读写、文件读写、计算/代码、工单读写和客户关系管理读写。每个工作单元调用 `deepseek-v4-flash` 正序与逆序各一次，并调用 `deepseek-v4-pro` 规范顺序一次；金标准是预先固定的工具身份。

完成标记如实记录 21 个 completed、3 个 failed；失败单元不进入分母。完成单元结果：

- Flash 正序 20/21；
- Flash 逆序 20/21；
- Pro 20/21；
- 正逆序分歧 0/21；
- 唯一 Flash 错误发生在一致子集，Pro 也未修正；
- 级联从不触发，结果仍为 20/21。

这同时触发三条预先杀伤条件：分歧不富集错误、升级不发生、强模型没有提供错误修正。不能通过加入 P069 已证明具有诱导作用的夸张描述、泄漏正确位置或事后挑任务来制造信号。

## 自然语言处置

K2 kill。P069 的群体层顺序偏好是重要测量警告，但在本工作台的语义明确、有唯一正确工具条件下，没有转化为 per-query selective escalation 信号。K1 与 K3 在一个错误上共同失败，提示该任务的困难不是位置不稳定。

## 家族可行性

系统实现容易，费用也低；科学家族在当前载体不可行，因为关键路由变量退化为常数。扩大同类简单任务只会更精确地估计接近零的分歧率，不值得 Promotion。

## Candidate 晋级与种子准备度

没有形成 Candidate。v003 没有正式实现、Promotion、Confirmation 或 Review Packet，不能送审或交付。

## 唯一窄缺口

黑盒、无标签的工具选择风险路由仍缺一个能在单查询层面富集真实执行错误的稳定信号；顺序分歧不是当前载体中的该信号。
