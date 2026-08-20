# v046 假设组合

本版本未注册正式假设。

- 草案：从工作簿依赖图选择源单元格，生成反事实输入，重算并以多点输出关系验证动态正确性。
- 判定：`KILLED_BY_DIRECT_PRIOR_COLLISION`。
- 直接碰撞：SpreadsheetBench 已通过修改源单元格生成测试实例并执行重算；WorkstreamBench、BlueFin 与 SpreadsheetBench 2 已显式覆盖公式质量、动态正确性和调试。
- 未保留差分：扩大扰动数量、加入依赖图可视化或把规则称为“见证”只改变实现与报告形式。

因此没有创建实验或正式假设注册项。
