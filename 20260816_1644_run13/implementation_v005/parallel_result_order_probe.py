from __future__ import annotations

import runpy
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "workbench_v005" / "parallel_result_order_probe.py"


if __name__ == "__main__":
    runpy.run_path(str(SOURCE), run_name="__main__")
