# Non-Goals

- `non_goal_id`: NG-v001-01
- `explicitly_not_solving`: 不试图一次解决所有工具故障、所有长程规划错误或所有智能体安全问题；不研究显式崩溃、网络中断等已有错误码即可检测的故障；不把模型微调作为必要条件。
- `explicitly_not_claiming`: 不预先声称新颖性、通用可靠性或真实世界部署收益；不把知识库排序当作研究空白；不把更多工具调用带来的收益当作方法贡献；不把 Reviewer 分数当作论文接受概率。
- `optional_user_non_goals`: NONE
- `excluded_followup_actions`: 当前阶段不写 Seed、不启动固定 Reviewer、不形成 Delivery；在 implementation 尚未值得稳定测量前不运行三审。
