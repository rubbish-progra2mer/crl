# v137 问题

[When Your Agent Opens the Chat App: Agent-Controlled Search over Raw Chat Logs Rivals Structured Memory](https://arxiv.org/abs/2608.12888) 的 ReFind 在轮级 BM25 命中后只展开该命中附近的固定窗口（默认 ±2 轮），但跨轮去重以整个会话为单位：一个会话只要返回过，后续所有查询都会排除该会话的全部候选轮。

v137 检查一个粒度不一致问题：局部窗口被观察后，把父会话整体标成已观察，是否会让同一长会话中相距较远的第二条证据永久不可达。该问题与一般“重复结果浪费预算”不同，因为抑制单位严格大于实际观察单位。

本版只进行无模型、无网络调用的良性合成检索实验。它不涉及 v029 的安全边界、真实聊天数据、隐私数据或安全过滤绕过。
