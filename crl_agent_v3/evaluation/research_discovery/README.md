# 时间截断的 CRL 研究发现评测

本目录提供一个离线、只读导入的最小评测框架，用于比较研究系统在探索、多样性、可证伪性、实现转化和匹配强基线后的实证存活事实。它不调用在线模型，不访问或写入生产知识库，不运行科研任务，也不产生总分、排名、冠军或自动科研裁决。

## 数据边界

`TaskManifest` 明确记录任务、智能体子领域、研究问题、时间可见性、留出论文、资源预算、强基线、盲化规则、人工标注说明和每个系统的配置哈希。系统输入包只包含可见论文标识，不包含留出论文标识或留出标注。

时间可见性支持精确日期、年份或显式 `visible_paper_ids`。如果只有年份，框架只自动纳入严格早于截断年份的论文；与截断年份相同且没有精确日期的论文保持“时序不确定”，除非清单显式把它列为可见。框架不会自行推断同年论文的先后。

五种离线导入格式为：

- `bare_llm`：`responses` 中的候选；
- `passage_rag`：`retrieval` 与 `hypotheses`；
- `card_only`：`cards` 与 `ideas`；
- `current_crl`：P2 `HypothesisPortfolio` 及可选 `candidate_facts`；
- `crl_scientific_search`：组合、`scientific_search` 可见输入记录及 `candidate_facts`。

所有格式最终转换成 `SystemOutput` schema 1。导入器只读取现成 JSON，不默认调用模型、网络、实验运行器或知识库查询。

## 指标语义

自动指标只计算明示记录：可见先行碰撞、结构完全重复、描述符覆盖、变化计算完整度、反证条件和杀手实验完整度、最近先行审计覆盖、实现转化、实现前早杀、匹配清单强基线后的存活，以及各资源维度的每个存活假设成本。可见先行碰撞率只以 `performed=true` 的已审计候选为分母；未审计候选是未知，不作为“无碰撞”。结构重复率只比较七个结构描述符均已观察的候选对。缺失成本保持 `null`，不会当作零。

留出机制再发现来自盲化专家的布尔标注；简单文本相似度单独披露，不能替代机制判断。新颖性、意义和技术正确性的主结论只接受 `blinded_expert` 标注。`llm_auxiliary` 的大语言模型裁判标注必须写明 `auxiliary_only`，不会进入主指标。

启用自助法置信区间时，每个指标同时披露其抽样单位。候选、候选对、被杀候选、强基线比较、专家标注和候选—留出论文对不会混作同一种样本。

## 命令行

```powershell
python tools/evaluate_research_discovery.py `
  --manifest evaluation/research_discovery/fixtures/synthetic/task_manifest.json `
  --system-output bare_llm evaluation/research_discovery/fixtures/synthetic/bare_llm.json `
  --system-output current_crl evaluation/research_discovery/fixtures/synthetic/current_crl.json `
  --annotation evaluation/research_discovery/fixtures/synthetic/expert_annotations.json `
  --bootstrap-replicates 200 --seed 7
```

同时给出 `--report-json` 与 `--report-markdown` 可不可覆盖地保存确定性报告；否则报告写到标准输出。

## 合成夹具声明

`fixtures/synthetic/` 的论文、系统、候选、成本、比较结果和专家标注全部是人工构造的虚构数据，只验证代码路径和隔离规则，**不代表真实科研能力**，也不是任何 CRL 系统优于其他系统的证据。

## 科研搜索奖励校准

`calibration.py` 与 `calibration_runner.py` 提供独立于正式 Run 的三组搜索策略校准：现行
启发式、朴素标量和硬约束下的非支配搜索。科学比较使用共同任务—种子的配对二元效应与
贝叶斯自助法；机械失败不进入科学负结果。该仪器只回答搜索策略是否比现行做法更容易找到
高保真实证候选，不能自动淘汰科研候选、认证新颖性或形成 Delivery。

阶段命令为：

```powershell
python tools/run_scientific_search_calibration.py preflight --tau2-root <隔离的tau2-v1.0.1路径>
python tools/run_tau2_calibration_block.py --tau2-root <隔离路径> --phase preflight --fidelity smoke --block-id <块> --attempt-id <尝试> --scaffold <声明式scaffold.json>
python tools/run_scientific_search_calibration.py preflight-results --selection <显式尝试选择.json>
python tools/run_scientific_search_calibration.py pilot
python tools/run_scientific_search_calibration.py confirm
python tools/run_scientific_search_calibration.py temporal --packet <时间洁净材料包.json>
python tools/run_scientific_search_calibration.py report
```

默认产物位于产品根的 `research_workspace/reward_calibration_v001/`，不进入任何 Run，
也不写共享知识库。预检汇总不会猜测“最新”尝试；调用者必须显式绑定 smoke、两次基线
和 ground-truth 的块与尝试标识。ground-truth 只调度 τ² 官方声明支持的任务子集。
