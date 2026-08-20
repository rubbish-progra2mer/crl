from __future__ import annotations

import csv
import io
import json
import re
from dataclasses import dataclass
from pathlib import Path

from .workspace import ResearchWorkspace, _atomic_write_text, _publish_once


_TOOL_NAME = re.compile(r"[a-z][a-z0-9_-]{1,47}")


@dataclass(frozen=True, slots=True)
class RunToolContext:
    workspace: ResearchWorkspace
    tool_name: str

    @property
    def root(self) -> Path:
        return self.workspace.workbench_path / "tools" / self.tool_name

    def output_path(self, relative: str | Path) -> Path:
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts or not path.parts:
            raise ValueError("tool output path must be safe and relative")
        target = self.workspace.assert_write_target(self.root / "outputs" / path)
        target.parent.mkdir(parents=True, exist_ok=True)
        return target

    def write_json(self, relative: str | Path, value: object) -> Path:
        path = self.output_path(relative)
        data = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
        _atomic_write_text(path, data.decode("utf-8"), within=self.workspace.workspace_path)
        return path

    def write_markdown(self, relative: str | Path, content: str) -> Path:
        path = self.output_path(relative)
        data = (content.rstrip() + "\n").encode("utf-8")
        _atomic_write_text(path, data.decode("utf-8"), within=self.workspace.workspace_path)
        return path

    def write_csv(self, relative: str | Path, rows: list[dict[str, object]]) -> Path:
        if not rows:
            raise ValueError("CSV rows must not be empty")
        fields = list(rows[0])
        if any(list(row) != fields for row in rows):
            raise ValueError("CSV rows must have identical ordered fields")
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        path = self.output_path(relative)
        _atomic_write_text(path, stream.getvalue(), within=self.workspace.workspace_path)
        return path


def create_run_tool(workspace: ResearchWorkspace, tool_name: str) -> dict[str, object]:
    workspace.assert_run_writable()
    name = _validate_tool_name(tool_name)
    root = workspace.assert_write_target(workspace.workbench_path / "tools" / name)
    if root.exists():
        raise FileExistsError(f"Run-local tool already exists: {name}")
    (root / "logs").mkdir(parents=True)
    (root / "outputs").mkdir()
    files = {
        "README.md": (
            f"# Run-local tool: {name}\n\n"
            "This helper belongs only to the current CRL Run. It is not an OS sandbox and "
            "does not create scientific authority. Keep outputs under `outputs/` and logs under `logs/`.\n"
        ),
        "main.py": (
            "from __future__ import annotations\n\n"
            "import json\n\n\n"
            "def main() -> None:\n"
            "    print(json.dumps({'status': 'ok'}, sort_keys=True))\n\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        ),
        "test_tool.py": (
            "from main import main\n\n\n"
            "def test_main_smoke(capsys):\n"
            "    main()\n"
            "    assert '\"status\": \"ok\"' in capsys.readouterr().out\n"
        ),
    }
    try:
        for relative, content in files.items():
            _publish_once(root / relative, content.encode("utf-8"), within=workspace.workspace_path)
    except BaseException:
        for path in root.rglob("*"):
            if path.is_file():
                path.unlink()
        for directory in sorted((path for path in root.rglob("*") if path.is_dir()), reverse=True):
            directory.rmdir()
        root.rmdir()
        raise
    return {
        "tool_name": name,
        "path": str(root),
        "files": sorted(files),
        "boundary": "RUN_LOCAL_HELPER_NOT_OS_SANDBOX",
    }


def _validate_tool_name(value: str) -> str:
    if not isinstance(value, str) or _TOOL_NAME.fullmatch(value) is None:
        raise ValueError("tool name must be 2-48 lowercase safe characters")
    return value
