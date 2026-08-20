# W06 Card source audit B disposition

- Audit ID: `w06-audit-b`
- Report SHA-256: `d187f055456872208bb8037a578f1d77a614011a2024b2251f77afd778084098`
- Decision: `ACCEPT_WITH_SINGLE_ROUND_NARROWING`
- Atomic totals: 138 PASS / 11 NARROW / 2 REJECT（内部交叉引用类 N/A 项不计入）

## Disposition

主 Codex 按审计意见完成一轮收窄（不循环审计）。两处 REJECT 与全部 NARROW 逐条采纳：

**内容级修正（REJECT + 内容 NARROW）：**
1. `paper-p095` / `failure-llm-freshness-judgment-prior-override-and-drift`：SubEM 口径方向反了（REJECT）——按 §4.5 改为 "子串匹配利好冗长输出（作者自注略抬长上下文 oracle 基线），对短实体/弃答输出反而更严"。
2. `paper-p095`：三步管线第三步为直接返回 max-serial 候选的抽取实体（§3.1，无 LLM 生成步）；"union-accuracy 下界" 改为 "软天花板（88.5%；剩余 11.5% 为检索失败下界）"。
3. `failure-llm-freshness…` / `operator-extract-then-deterministic-max-assembly`：LongMemEval-KU 实有时间戳全序标记（§5.7 管线跑的就是 max(timestamp)）——平局定性从 "无显式标记载体" 改为 "问题型超出 current-value 域（max 为错算子）"，跨载体优势仍不证。
4. `paper-p094`：覆写消融子句移出 AUTHOR_FACT 绑定行，改 CODEX_SYNTHESIS 并落 App. K.2/Table 19 定位（内容本身核验为真）。
5. `failure-selective-forgetting…`：TTL <4% 零样本地板系 TTL 任务控制（App. H.2），不作 FactCon 先验排除论据——替换为 MQUAKE 反事实编辑对构造论证（§3.1）。

**绑定级修正（binding-only NARROW，内容全部核验为真）：**
6. `operator-extract-then-deterministic-max-assembly`：verbatim/不挑最优与 ≈50 行细节补 §3.1 定位注。
7. `paper-p096`：信号/聚合/门控细节补 §3/Alg.1–3、§4.2 定位注。
8. `paper-p097`：L1/L2 参数细节补 §3.2–3.4/App.E 定位注。
9. `failure-solver-feasibility-near-zero-information-proxy`：扰动边界补 §5.4/Limitations 定位注。
10. `operator-behavioral-perturbation-existence-test`：前提句错绑 `ev-p097-feasibility-gap` → 改绑 `ev-p097-behavioral-perturbation`（部分锚）+ §3.2/App.E.2/§3.4 定位注。

审计正面结论：全部头条数字精确核验（80.0→14.0、+10.8pp、75%→61%、91.5%/23–34%、91.1% vs 0.5%、ReLoop 逐字引语、扰动因子与阈值）；P096 卡的对抗性缺陷主张（不可能分母算术、A.2/A.3 transcript 错配、best-of-K 无配平对照、R1 双套数字）被审计员独立重推导确认；机械层 9/9 evidence 逐字节一致、4/4 PDF SHA 匹配；invocation 点名的四组过度声明风险全部已被卡正确处理。

修订后卡片重过 `manage_cards.py validate`；三份审计全部处置后统一重建 FTS 索引（见 v010 冻结快照）。一轮修订后不触发循环审计。
