# v026 研究图谱

- PolarityCheck 的 `constraint_2x2.jsonl` 含 40 对单一作者样本，交叉 20 个变异/20 个忠实标签与词面接近/遥远条件；独立决策标签字段均为空。
- 固定温度 0、种子 20260816，`qwen2.5:7b` 直接成对判断准确率 0.900：变异召回率 1.000、忠实特异度 0.800。
- `qwen3:4b` 准确率 0.850：变异召回率 0.950、忠实特异度 0.750；它漏掉“must→should”的情态降级。
- 两模型共同误报 `fail closed→fail shut`、`fail closed→deny the request`、`transaction wrapper→transaction helper`；两者也共同质疑 `Alert→Page the on-call engineer`。
- 至少三个忠实标签依赖未给出的术语共指或动作映射；`Never log the raw API key→Under no circumstances should secret material appear in diagnostic output` 还扩大了对象范围，不满足严格双向等价。
- RefNLI（NAACL Findings 2025）已把前提与假设是否指向同一上下文的“引用确定性”假设显式化，并发布引用歧义诊断集；微调自然语言推断模型和少样本语言模型均严重误判上下文不匹配。
- AbstentionBench（arXiv:2506.09038）已经系统评测欠说明、病态和不可回答输入的选择性弃答，并表明仅靠提示不能解决根本能力缺口。
- `Paraphrase Identification via Textual Inference`（*SEM 2024）已把改写等价归约到自然语言推断关系；双向蕴含是候选确定样本判断的直接祖先。

结论：真实发现是二值基准把未声明术语映射压成了确定标签，但“引用确定性检查＋弃答＋双向蕴含”只是已有方法部件组合，不构成新的智能体计算。
