"""让原始 ToolSandbox 测试只加载本版本锁定的最小上游源码。"""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "vendor"))
