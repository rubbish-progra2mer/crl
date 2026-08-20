# Source Priority

| source_name | priority_level | why_selected | what_it_is_good_for | what_it_cannot_cover |
|---|---:|---|---|---|
| CRL 冻结共享知识库（purpose-aware retrieval） | P0 | 具有冻结 Paper/Card/Evidence/Passage 与原文定位链 | 已摄入论文的失败模式、算子、测量与正文证据 | 不能保证覆盖 2026 最近工作；排序不证明空白 |
| Run-local Prior Audit | P0 | 可保存实时检索、候选、组件重叠与引文扩展 | 最近工作碰撞、最近邻与前后向引文 | 元数据命中仍需正文核对 |
| arXiv / OpenReview / ACL Anthology / 正式会议论文页 | P0 | 论文一级来源，可核对版本、日期和全文 | 最近工作、原始方法与实验细节 | 不提供统一引文图；预印本质量不等同正式发表 |
| Semantic Scholar / Crossref 元数据 | P1 | 适合语义召回、DOI 和引文扩展 | 第一层 100+ 元数据与引用邻域 | 不以其摘要直接支撑方法判断 |
| Papers with Code / 基准官方仓库 | P1 | 补实现、数据和评价定义 | 基准真实性、代码可用性和复现路径 | 排名与任务标签不构成科学证据 |
| 普通网页搜索 | P2 | 发现遗漏的正式入口或作者页 | 补链接和术语同义词 | 二手总结不进入核心证据 |
