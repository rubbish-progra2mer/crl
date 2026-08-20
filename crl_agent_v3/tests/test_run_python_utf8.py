from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WRAPPER = PROJECT_ROOT / "tools" / "run_python_utf8.ps1"
def _run_wrapper(temp_dir: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    environment = os.environ.copy()
    temp_dir.mkdir(exist_ok=True)
    environment["TEMP"] = str(temp_dir)
    environment["TMP"] = str(temp_dir)
    return subprocess.run(
        ["powershell.exe", "-NoProfile", "-File", str(WRAPPER), *arguments],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=environment,
    )


@pytest.mark.windows
def test_wrapper_round_trips_utf8_file_argument_and_output(tmp_path: Path) -> None:
    script = tmp_path / "脚本😀.py"
    text_file = tmp_path / "研究内容.txt"
    argument = "参数：中文 • 😀"
    text = "中文研究内容\n• 项目符号\nemoji 😀\n"
    script.write_bytes(
        b"from pathlib import Path\n"
        b"import sys\n"
        b"sys.stdout.buffer.write(sys.argv[1].encode('utf-8') + b'\\n')\n"
        b"sys.stdout.buffer.write(Path(sys.argv[2]).read_bytes())\n"
    )
    text_file.write_bytes(text.encode("utf-8"))

    result = _run_wrapper(tmp_path / "process-temp", str(script), argument, str(text_file))

    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    assert result.stdout == argument.encode("utf-8") + b"\n" + text.encode("utf-8")
    assert not script.read_bytes().startswith(b"\xef\xbb\xbf")
    assert not text_file.read_bytes().startswith(b"\xef\xbb\xbf")


def test_wrapper_is_ascii_only_and_has_no_bom() -> None:
    wrapper_bytes = WRAPPER.read_bytes()

    assert wrapper_bytes.isascii()
    assert not wrapper_bytes.startswith(b"\xef\xbb\xbf")


@pytest.mark.windows
def test_wrapper_propagates_python_nonzero_exit_code(tmp_path: Path) -> None:
    script = tmp_path / "fails.py"
    script.write_bytes(b"raise SystemExit(37)\n")

    result = _run_wrapper(tmp_path / "process-temp", str(script))

    assert result.returncode == 37


@pytest.mark.windows
def test_wrapper_uses_shared_crl_environment(tmp_path: Path) -> None:
    script = tmp_path / "interpreter.py"
    script.write_bytes(
        b"from pathlib import Path\n"
        b"import sys\n"
        b"print(Path(sys.executable).resolve())\n"
    )

    result = _run_wrapper(tmp_path / "process-temp", str(script))

    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    actual = Path(result.stdout.decode("utf-8").strip()).resolve()
    expected = (PROJECT_ROOT.parent / "env" / "crl_agent_v3" / "python.exe").resolve()
    assert actual == expected
