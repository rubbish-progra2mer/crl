from pathlib import Path
import runpy


SOURCE = Path(__file__).resolve().parents[1] / "workbench_v007" / "contract_activation_baseline_audit.py"
runpy.run_path(str(SOURCE), run_name="__main__")
