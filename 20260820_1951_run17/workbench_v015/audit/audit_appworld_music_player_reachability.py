from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any


TARGET_URLS = {
    "/spotify/music_player/current_song",
    "/spotify/music_player/song_queue",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(lines: list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(lines)).encode("utf-8")).hexdigest()


def player_coverage(connection: sqlite3.Connection) -> dict[str, int]:
    return {
        "user_count": connection.execute("SELECT COUNT(*) FROM users").fetchone()[0],
        "music_player_count": connection.execute(
            "SELECT COUNT(*) FROM music_players"
        ).fetchone()[0],
        "users_without_music_player": connection.execute(
            """
            SELECT COUNT(*)
            FROM users AS u
            WHERE NOT EXISTS (
                SELECT 1 FROM music_players AS m WHERE m.user_id = u.id
            )
            """
        ).fetchone()[0],
        "users_with_multiple_music_players": connection.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT user_id FROM music_players GROUP BY user_id HAVING COUNT(*) > 1
            )
            """
        ).fetchone()[0],
        "music_players_without_user": connection.execute(
            """
            SELECT COUNT(*)
            FROM music_players AS m
            WHERE NOT EXISTS (SELECT 1 FROM users AS u WHERE u.id = m.user_id)
            """
        ).fetchone()[0],
    }


def task_ids_with_target_calls(data_root: Path) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for split_file in sorted((data_root / "datasets").glob("*.txt")):
        split = split_file.stem
        matched: set[str] = set()
        for task_id in split_file.read_text(encoding="utf-8").splitlines():
            task_id = task_id.strip()
            if not task_id:
                continue
            api_path = data_root / "tasks" / task_id / "ground_truth" / "api_calls.json"
            if not api_path.is_file():
                continue
            calls = json.loads(api_path.read_text(encoding="utf-8"))
            if any(
                str(call.get("method", "")).lower() == "get"
                and call.get("url") in TARGET_URLS
                for call in calls
            ):
                matched.add(task_id)
        result[split] = matched
    return result


def rebuild_task_database(
    base_database: Path, patch_file: Path
) -> sqlite3.Connection:
    source = sqlite3.connect(f"file:{base_database}?mode=ro", uri=True)
    target = sqlite3.connect(":memory:")
    try:
        source.backup(target)
    finally:
        source.close()
    for line in patch_file.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        statement, parameters, _ = json.loads(line)
        target.execute(statement, parameters)
    target.commit()
    return target


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    base_database = args.data_root / "base_dbs" / "spotify.db"
    split_to_task_ids = task_ids_with_target_calls(args.data_root)
    task_ids = set().union(*split_to_task_ids.values())

    base_connection = sqlite3.connect(
        f"file:{base_database}?mode=ro", uri=True
    )
    try:
        base_coverage = player_coverage(base_connection)
    finally:
        base_connection.close()

    coverage_rows: list[dict[str, Any]] = []
    input_manifest: list[str] = []
    failures: list[dict[str, str]] = []
    for task_id in sorted(task_ids):
        patch_file = args.data_root / "tasks" / task_id / "dbs" / "spotify.jsonl"
        api_file = (
            args.data_root
            / "tasks"
            / task_id
            / "ground_truth"
            / "api_calls.json"
        )
        try:
            connection = rebuild_task_database(base_database, patch_file)
            try:
                coverage_rows.append(player_coverage(connection))
            finally:
                connection.close()
            input_manifest.append(
                f"{task_id}:{sha256_file(patch_file)}:{sha256_file(api_file)}"
            )
        except (OSError, UnicodeError, json.JSONDecodeError, sqlite3.Error) as exc:
            failures.append(
                {
                    "task_ref_sha256": hashlib.sha256(
                        task_id.encode("utf-8")
                    ).hexdigest(),
                    "error": str(exc),
                }
            )

    result = {
        "schema_version": 1,
        "scope": (
            "Reachability of the conditional MusicPlayer creation branch for the locally "
            "available AppWorld train/dev tasks whose frozen ground-truth traces call "
            "show_current_song or show_song_queue. Task databases are reconstructed in memory."
        ),
        "inputs": {
            "data_version": (args.data_root / "version.txt")
            .read_text(encoding="utf-8")
            .strip(),
            "base_spotify_db_sha256": sha256_file(base_database),
            "matched_task_input_manifest_sha256": sha256_text(input_manifest),
        },
        "target_urls": sorted(TARGET_URLS),
        "matched_task_count": len(task_ids),
        "matched_task_count_by_split": {
            split: len(ids) for split, ids in sorted(split_to_task_ids.items())
        },
        "base_database_coverage": base_coverage,
        "reconstructed_task_coverage": {
            "successful_task_count": len(coverage_rows),
            "failed_task_count": len(failures),
            "tasks_with_any_user_without_music_player": sum(
                row["users_without_music_player"] > 0 for row in coverage_rows
            ),
            "tasks_with_any_duplicate_music_player": sum(
                row["users_with_multiple_music_players"] > 0
                for row in coverage_rows
            ),
            "tasks_with_orphan_music_player": sum(
                row["music_players_without_user"] > 0 for row in coverage_rows
            ),
            "minimum_user_count": min(
                (row["user_count"] for row in coverage_rows), default=None
            ),
            "maximum_user_count": max(
                (row["user_count"] for row in coverage_rows), default=None
            ),
            "minimum_music_player_count": min(
                (row["music_player_count"] for row in coverage_rows), default=None
            ),
            "maximum_music_player_count": max(
                (row["music_player_count"] for row in coverage_rows), default=None
            ),
        },
        "failures": failures,
        "interpretation_boundary": (
            "Zero users without a MusicPlayer makes the create-and-save branch unreachable for "
            "authenticated users in these reconstructed initial task states. It does not prove "
            "the branch is unreachable for arbitrary or future AppWorld databases."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
