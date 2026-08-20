from pathlib import Path
import sys

sys.path.insert(0, r"D:\Desktop\crl\crl_agent_v3")

from crl_v3.workspace import ResearchWorkspace


workspace = ResearchWorkspace(
    Path(r"D:\Desktop\crl\20260802_1719_run06"),
    version="v007",
    product_root=Path(r"D:\Desktop\crl"),
)
body = Path(
    r"D:\Desktop\crl\20260802_1719_run06\workbench_v007\decision_body.md"
).read_text(encoding="utf-8")
document = workspace.write_review_decision(body)
print(document.sha256)
