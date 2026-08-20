import hashlib
import json
import re
import shutil
from pathlib import Path

from huggingface_hub import HfApi, hf_hub_download


ROOT = Path(__file__).resolve().parent
PARTITION = json.loads(
    (ROOT / "toolfailbench_partition.json").read_text(encoding="utf-8")
)
REVISION = PARTITION["dataset_revision"]
DATASET_ID = PARTITION["dataset_id"]
DESTINATION = ROOT / "toolfailbench_confirmation"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


info = HfApi().dataset_info(DATASET_ID, revision=REVISION, files_metadata=True)
available = {item.rfilename for item in info.siblings}
selected: list[str] = []
for trace_file in PARTITION["confirmation_trace_files"]:
    slug = re.sub(r"_\d{8}_\d{6}\.json$", "", trace_file)
    judges = sorted(
        name
        for name in available
        if name.startswith(f"judge/{slug}_judge_") and name.endswith(".json")
    )
    if len(judges) != 2:
        raise RuntimeError(f"expected two judge files for {slug}, found {len(judges)}")
    selected.append(trace_file)
    selected.extend(judges)

selected = sorted(set(selected))
if len(selected) != 36:
    raise RuntimeError(f"expected 36 Confirmation files, found {len(selected)}")
if any(name.startswith("judge_ensemble/") for name in selected):
    raise RuntimeError("Confirmation selection must not contain ensemble files")

DESTINATION.mkdir(exist_ok=True)
manifest = []
for index, name in enumerate(selected, start=1):
    cached = Path(
        hf_hub_download(
            repo_id=DATASET_ID,
            filename=name,
            repo_type="dataset",
            revision=REVISION,
        )
    )
    target = DESTINATION / Path(name)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.is_file() or target.stat().st_size != cached.stat().st_size:
        shutil.copyfile(cached, target)
    manifest.append(
        {
            "path": name,
            "bytes": target.stat().st_size,
            "sha256": sha256(target),
        }
    )
    print(f"{index}/{len(selected)} {name}", flush=True)

(ROOT / "toolfailbench_confirmation_manifest.json").write_text(
    json.dumps(
        {
            "schema_version": 1,
            "dataset_id": DATASET_ID,
            "revision": REVISION,
            "files": manifest,
        },
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
    newline="\n",
)
