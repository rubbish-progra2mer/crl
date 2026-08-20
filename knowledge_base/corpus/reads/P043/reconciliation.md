# P043 Reconciliation

- Disposition：`ACCEPTED_AS_EVALUATION_CARRIER`
- Read 1 SHA-256：`1ab50ea2ea113b88076f220e7fc3eeb9eba55fa024ee3592f1bfa3c734fa750b`
- Accepted read-2 attempt：`read_2_attempts/r2-20260719-p043-a1/`
- Invocation SHA-256：`5fc4f5920fe0c5c671021ba096f24957f3b6f780f2e3733cf66e82fa745064da`
- Report SHA-256：`8e8cd1b998658e2ddfc8d09a00482b874e42f7c5f6aba50ef570d3cbba9e04c3`

## Source reconciliation

- `AGREE`：RACE 是相对 Gemini Deep Research 参考报告的任务自适应 pairwise 评分；FACT 是 statement–URL 抽取、网页抓取与支撑判定，两者必须分开解释。
- `AGREE`：参考与 judge 同属 Gemini 2.5 Pro，系统级相关只基于四个均值点，人评只覆盖中文子集；RACE 不是绝对正确性。
- `AGREE`：评测前引用格式清理会改变待评对象，专有系统预算未知。

## Admission boundary

优先以 FACT 作为可核验引用算子、以 RACE 作为有明确 reference-relative 边界的测量方法准入；不把总排名当无偏系统能力或机制因果证据。

