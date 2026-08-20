# 目标问题卡

- problem_id: `CRL-PREMISE-AUDIT-001`
- research_direction: 评估“以当前前沿大语言模型作为长期自主主研究者，结合只读论文知识库和本地小规模反证实验，发现值得人类继续投入的研究实现种子”是否具有现实意义。
- target_problem: 在不把“大模型智力等同研究生”当作先验事实的前提下，判断 CRL 的系统级价值主张是否得到现有实证证据支持，以及成立所需的边界条件是什么。
- problem_statement: 需要分别检验四条链路：科研任务能力、长期自主代理可靠性、知识库与工具支撑的增益、小规模代理实验对后续研究价值的预测有效性。只有整条链路在可操作边界内成立，CRL 才可能稳定优于一次性大模型构思或普通人机协作。
- task_setting: 输入为当前前沿模型、论文知识库、本地计算资源和长期执行环境；输出不是可直接投稿论文，而是带有先行工作定位、可证伪主张、最小实现、本地证据、失败边界和后续资源需求的候选研究种子；主要约束为无法承担大规模训练，但允许长期检索、推理、编码和小实验。
- assumed_user_goal: 判断是否值得继续完善 CRL，并为后续诊断 Run 13 提供外部证据基线，而不是为既有设计辩护。
- explicit_boundary: 聚焦计算机科学中的文本与工具型大语言模型智能体科研；评价发现、去风险和候选排序能力，不要求系统独立完成整篇论文；只接受论文、基准、官方技术报告和可核验系统材料作为主要依据。
- excluded_subfields: 湿实验科学的全自动实验室、需要机器人硬件的实验、纯粹哲学意义上的通用智能、仅讨论写作润色或文献摘要的工具、与候选研究发现无关的自动代码生成。
- first_pass_search_keywords: autonomous AI scientist, AI research agent benchmark, research idea generation evaluation, long-horizon agent reliability, scientific discovery agent, PaperBench, MLE-bench, AI Scientist, research ideation benchmark, scaling proxy experiment predictive validity, small-scale experiment ranking.
- historical_failure_constraints: 已知 Run 13 出现长时间无响应且候选质量未见提升，但本阶段不读取其内部材料，也不把单次运行失败外推为 CRL 总体无效。
- consulted_route_registry_ids: `NONE`
- rerun_avoidance_strategy: 先建立外部能力上限、已知失败模式和代理评估有效性证据；之后若分析 Run 13，只检查其失败是否落入这些机制，不重新进行无边界文献泛搜。
- ambiguity_needing_user_confirmation: `needs-user-confirmation`——“研究生媲美”暂按“能在有边界、有工具、有检查点的任务上达到合格研究生水平”解释，而非全面、持续、无监督等价；“有意义”暂按“有合理概率提高候选发现与排序的期望价值，且可通过对照和前瞻验证检验”解释。若用户要求更强定义，最终结论会相应收紧。

- disposition: `keep`
