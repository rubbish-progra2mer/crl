import os

import datasets
import gradio as gr
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from content import (
    CITATION_BUTTON_LABEL,
    CITATION_BUTTON_TEXT,
    CONTACT_TEXT,
    INTRODUCTION_TEXT,
    LEADERBOARD_PATH,
    LEGACY_RESULTS_DATASET,
    LEGACY_SCENARIO_LIST,
    RESULTS_DATASET,
    SCENARIO_LIST,
    TITLE,
)
from utils import api, TOKEN


# ── Helpers ──────────────────────────────────────────────────────────────


def get_display_name(capability: str) -> str:
    """Convert internal capability names to user-friendly display names."""
    if "noise" in capability:
        return "Noise"
    elif "agent2agent" in capability or "a2a" in capability:
        return "A2A"
    else:
        return capability.capitalize()


def _build_row(row, scenario_list: list[str]) -> dict:
    """Transform a raw result row into a clean leaderboard row."""
    result = {}
    result["Model"] = row["metadata.model"]
    result["Provider"] = row["metadata.model_provider"]
    result["pass@1"] = round(row["statistics.global.macro_success_rate"], 1)

    for capability in scenario_list:
        display_name = get_display_name(capability)
        score = row.get(f"statistics.per_capability.{capability}.success_rate")
        if score is not None:
            result[display_name] = round(score, 1)
        else:
            result[display_name] = "—"

    result["Submitter"] = row.get("metadata.organisation", "—")
    result["Date"] = row["metadata.timestamp"][:10]
    return result


def _load_results_df(dataset_id: str, scenario_list: list[str]) -> pd.DataFrame:
    """Load results from a HF dataset and return a sorted DataFrame."""
    try:
        eval_results = datasets.load_dataset(
            dataset_id,
            token=TOKEN,
            verification_mode=datasets.VerificationMode.NO_CHECKS,
            download_mode="force_redownload",
        )
    except (datasets.data_files.EmptyDatasetError, ConnectionError):
        eval_results = datasets.DatasetDict()

    split = "train"
    if not eval_results or split not in eval_results or len(eval_results[split]) == 0:
        return pd.DataFrame([])

    results = eval_results[split]
    local_df = results.flatten()

    metadata_columns = [
        "metadata.model",
        "metadata.model_provider",
        "metadata.organisation",
        "metadata.timestamp",
    ]
    global_stats_columns = [
        "statistics.global.macro_success_rate",
        "statistics.global.total_runs",
        "statistics.global.total_scenarios",
    ]
    capability_columns = []
    for cap in scenario_list:
        for suffix in ("success_rate", "success_rate_sem"):
            col = f"statistics.per_capability.{cap}.{suffix}"
            if col in local_df.column_names:
                capability_columns.append(col)

    columns = metadata_columns + global_stats_columns + capability_columns
    columns = [c for c in columns if c in local_df.column_names]

    local_df = local_df.select_columns(columns)
    mapped_df = local_df.map(lambda row: _build_row(row, scenario_list), batched=False)
    mapped_df = mapped_df.remove_columns(columns)

    df = pd.DataFrame(mapped_df)
    df = df.sort_values(by=["pass@1"], ascending=False)

    # Enforce column order
    ordered_cols = ["Model", "Provider", "Harness", "pass@1"]
    for cap in scenario_list:
        name = get_display_name(cap)
        if name in df.columns:
            ordered_cols.append(name)
    ordered_cols += ["Submitter", "Date"]
    ordered_cols = [c for c in ordered_cols if c in df.columns]
    df = df[ordered_cols]

    df = df.reset_index(drop=True)
    df.index = df.index + 1
    df.index.name = "#"
    return df


# ── Load data ────────────────────────────────────────────────────────────

_GAIA2_CLI_DATA = [
    {
        "model": "Claude Opus 4.6 (high)",
        "provider": "Anthropic",
        "pass1": 57.0,
        "search": 88.1,
        "execution": 82.9,
        "adaptability": 61.9,
        "ambiguity": 48.3,
        "time": 3.8,
        "date": "2026-04-13",
    },
    {
        "model": "GPT-5.5 (xhigh)",
        "provider": "OpenAI",
        "pass1": 56.4,
        "search": 96.2,
        "execution": 79.4,
        "adaptability": 55.0,
        "ambiguity": 46.9,
        "time": 4.4,
        "date": "2026-05-15",
    },
    {
        "model": "GPT-5.4 (high)",
        "provider": "OpenAI",
        "pass1": 55.6,
        "search": 94.8,
        "execution": 78.8,
        "adaptability": 54.8,
        "ambiguity": 47.3,
        "time": 2.5,
        "date": "2026-04-13",
    },
    {
        "model": "Gemini 3.1 Pro (high)",
        "provider": "Google",
        "pass1": 52.0,
        "search": 92.8,
        "execution": 78.6,
        "adaptability": 45.9,
        "ambiguity": 40.6,
        "time": 2.1,
        "date": "2026-04-14",
    },
    {
        "model": "Claude Sonnet 4.6 (high)",
        "provider": "Anthropic",
        "pass1": 51.9,
        "search": 82.5,
        "execution": 75.8,
        "adaptability": 55.7,
        "ambiguity": 40.4,
        "time": 5.0,
        "date": "2026-04-13",
    },
    {
        "model": "GLM 5.1 (enabled)",
        "provider": "OpenRouter*",
        "pass1": 50.5,
        "search": 83.8,
        "execution": 71.2,
        "adaptability": 56.9,
        "ambiguity": 39.4,
        "time": 1.2,
        "date": "2026-04-13",
    },
    {
        "model": "Kimi-K2.5 (enabled)",
        "provider": "OpenRouter*",
        "pass1": 34.0,
        "search": 62.2,
        "execution": 47.0,
        "adaptability": 43.4,
        "ambiguity": 16.6,
        "time": 0.8,
        "date": "2026-04-14",
    },
]

_SPLIT_COLS = ["search", "execution", "adaptability", "ambiguity", "time"]

_APP_CSS = """
.lb-wrap {
    --lb-bg: var(--background-fill-primary);
    --lb-surface: var(--background-fill-secondary, var(--background-fill-primary));
    --lb-surface-strong: var(--block-background-fill, var(--background-fill-primary));
    --lb-text: var(--body-text-color);
    --lb-header-text: color-mix(in srgb, var(--body-text-color) 78%, var(--background-fill-primary));
    --lb-secondary-text: color-mix(in srgb, var(--body-text-color) 54%, var(--background-fill-primary));
    --lb-muted-text: color-mix(in srgb, var(--body-text-color) 40%, var(--background-fill-primary));
    --lb-border: transparent;
    --lb-zebra: color-mix(in srgb, var(--body-text-color) 4%, var(--background-fill-primary));
    --lb-hover: color-mix(in srgb, var(--body-text-color) 8%, var(--background-fill-primary));
    --lb-rank-bg: color-mix(in srgb, var(--body-text-color) 8%, var(--background-fill-primary));
    --lb-pass-accent: var(--link-text-color, var(--body-text-color));
    --lb-pass-bg: color-mix(in srgb, var(--link-text-color, var(--body-text-color)) 14%, var(--background-fill-primary));
    --lb-pass-border: transparent;
    --lb-pass-text: color-mix(in srgb, var(--link-text-color, var(--body-text-color)) 70%, var(--body-text-color));
    --lb-bar-track: color-mix(in srgb, var(--body-text-color) 11%, var(--background-fill-primary));
    --lb-bar-fill-start: color-mix(in srgb, var(--link-text-color, var(--body-text-color)) 44%, var(--background-fill-primary));
    --lb-bar-fill-end: color-mix(in srgb, var(--link-text-color, var(--body-text-color)) 78%, var(--background-fill-secondary, var(--background-fill-primary)));
    --lb-bar-fill-strong-start: color-mix(in srgb, var(--link-text-color, var(--body-text-color)) 58%, var(--background-fill-primary));
    --lb-bar-fill-strong-end: color-mix(in srgb, var(--link-text-color, var(--body-text-color)) 92%, var(--background-fill-secondary, var(--background-fill-primary)));
    max-width: 100%;
    margin: 0 auto;
    padding: 0 24px;
}

.lb-heading {
    margin: 28px 0 6px;
    color: var(--lb-text);
    font-size: 1.4em;
    font-weight: 700;
}

.lb-subtitle,
.lb-caption {
    color: var(--lb-secondary-text);
}

.lb-subtitle {
    margin: 0 0 18px;
    font-size: 0.86em;
}

.lb-caption {
    margin: 12px 0 0;
    font-size: 0.77em;
    text-align: right;
}

.lb-scroll {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    border: none;
    border-radius: 18px;
    background: linear-gradient(
        180deg,
        color-mix(in srgb, var(--lb-surface) 60%, var(--lb-surface-strong)) 0%,
        var(--lb-surface-strong) 100%
    );
    box-shadow: 0 4px 16px rgba(0,0,0,0.04);
}

.lb {
    width: max-content;
    min-width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    background: var(--lb-surface-strong);
    font-size: 14px;
    border-radius: 18px;
    overflow: hidden;
}

.lb thead th {
    position: sticky;
    top: 0;
    z-index: 20;
    padding: 14px 18px;
    border-bottom: 1px solid var(--lb-border);
    background: var(--lb-surface-strong);
    color: var(--lb-header-text);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    white-space: nowrap;
}

.lb thead th.is-num {
    text-align: right;
}

.lb thead th.c-model {
    min-width: 200px;
}

.lb tbody tr {
    --lb-row-bg: var(--lb-bg);
}

.lb tbody tr:nth-child(even) {
    --lb-row-bg: var(--lb-zebra);
}

.lb tbody tr:hover {
    --lb-row-bg: var(--lb-hover);
}

.lb tbody th,
.lb tbody td {
    padding: 15px 18px;
    border-bottom: 1px solid var(--lb-border);
    background: var(--lb-row-bg);
    white-space: nowrap;
    vertical-align: middle;
}

.lb tbody tr:last-child th,
.lb tbody tr:last-child td {
    border-bottom: none;
}

.lb .c-model {
    min-width: 200px;
    text-align: left;
}

.lb .model-cell {
    display: flex;
    align-items: center;
    gap: 12px;
}

.lb .rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 2rem;
    height: 2rem;
    padding: 0 0.55rem;
    border-radius: 999px;
    background: var(--lb-rank-bg);
    color: var(--lb-secondary-text);
    font-size: 0.8rem;
    font-weight: 700;
    line-height: 1;
    flex: 0 0 auto;
}

.lb .model-name {
    color: var(--lb-text);
    font-size: 14px;
    font-weight: 650;
    letter-spacing: -0.01em;
}

.lb .c-provider,
.lb .c-harness,
.lb .c-time,
.lb .c-date {
    color: var(--lb-secondary-text);
}

.lb .is-num {
    text-align: right;
    font-variant-numeric: tabular-nums;
}

.lb .c-pass1 {
    background: color-mix(in srgb, var(--lb-pass-bg) 78%, var(--lb-row-bg));
    color: var(--lb-pass-text);
    font-size: 15px;
    font-weight: 780;
    box-shadow: none;
}

.lb thead th.c-pass1 {
    background: color-mix(in srgb, var(--lb-pass-bg) 70%, var(--lb-surface-strong));
}

.lb .c-split {
    width: 130px;
    min-width: 130px;
    color: var(--lb-secondary-text);
}

.lb .metric-stack {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 7px;
}

.lb .split-val {
    color: inherit;
    font-weight: 560;
}

.lb .c-split.is-best .split-val {
    color: var(--lb-text);
    font-weight: 670;
}

.lb .bar-track {
    width: 100%;
    height: 5px;
    border-radius: 999px;
    background: var(--lb-bar-track);
    overflow: hidden;
}

.lb .bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--lb-bar-fill-start) 0%, var(--lb-bar-fill-end) 100%);
    opacity: 0.95;
}

.lb .c-split.is-best .bar-fill {
    background: linear-gradient(90deg, var(--lb-bar-fill-strong-start) 0%, var(--lb-bar-fill-strong-end) 100%);
}

.lb thead tr:first-child th:first-child {
    border-top-left-radius: 18px;
}

.lb thead tr:first-child th:last-child {
    border-top-right-radius: 18px;
}

.lb tbody tr:last-child th.c-model {
    border-bottom-left-radius: 18px;
}

.lb tbody tr:last-child td:last-child {
    border-bottom-right-radius: 18px;
}

.dataframe table th,
.dataframe table td {
    min-width: 70px !important;
    max-width: 150px !important;
    text-align: center !important;
}

.dataframe table th:first-child,
.dataframe table td:first-child {
    min-width: 180px !important;
    max-width: 250px !important;
    text-align: left !important;
}

/* Kill any Gradio/theme-injected table borders */
.lb th, .lb td, .lb tr, .lb thead, .lb tbody {
    border-left: none !important;
    border-right: none !important;
}

@media (max-width: 900px) {
    .lb-wrap {
        padding: 0 8px;
    }

    .lb thead th,
    .lb tbody th,
    .lb tbody td {
        padding: 12px 14px;
    }

    .lb thead th.c-model,
    .lb .c-model {
        min-width: 240px;
    }
}
"""


def _build_leaderboard_html() -> str:
    """Build the Gaia2-CLI leaderboard as pure HTML."""
    data = sorted(_GAIA2_CLI_DATA, key=lambda r: r["pass1"], reverse=True)

    best = {col: max(r[col] for r in data) for col in _SPLIT_COLS}

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}

    def split_cell(val: float, col: str, extra_class: str = "") -> str:
        best_class = " is-best" if val == best[col] else ""
        return (
            f'<td class="c-split is-num{best_class}{extra_class}">'
            f'<div class="metric-stack">'
            f'<span class="split-val">{val:.1f}%</span>'
            f'<div class="bar-track" aria-hidden="true">'
            f'<div class="bar-fill" style="width:{val:.1f}%"></div>'
            f"</div>"
            f"</div>"
            f"</td>"
        )

    rows = ""
    for rank, r in enumerate(data, 1):
        rank_badge = medals.get(rank, str(rank))
        rows += f"""<tr>
            <th class="c-model" scope="row">
                <div class="model-cell">
                    <span class="rank-badge" title="Rank {rank}">{rank_badge}</span>
                    <span class="model-name">{r["model"]}</span>
                </div>
            </th>
            <td class="c-provider">{r["provider"]}</td>
            <td class="c-harness">{r.get("harness", "OpenClaw 2026.4.1")}</td>
            <td class="c-pass1">{r["pass1"]:.1f}%</td>
            {split_cell(r["search"], "search")}
            {split_cell(r["execution"], "execution")}
            {split_cell(r["adaptability"], "adaptability")}
            {split_cell(r["ambiguity"], "ambiguity")}
            {split_cell(r["time"], "time", " c-time")}
            <td class="c-date">{r["date"]}</td>
        </tr>"""

    return f"""
    <div class="lb-wrap">
        <h2 class="lb-heading"><a href="https://github.com/facebookresearch/meta-agents-research-environments/tree/main/gaia2-cli" target="_blank" style="color:inherit;text-decoration:none;">Gaia2-CLI Leaderboard</a></h2>
        <p class="lb-subtitle">{len(data)} models &middot; higher is better &middot; <a href="https://github.com/facebookresearch/meta-agents-research-environments/tree/main/gaia2-cli" target="_blank" style="color:inherit;text-decoration:underline;">Test your own model / harness here</a></p>

        <div class="lb-scroll">
        <table class="lb" role="table">
            <thead>
                <tr>
                    <th class="c-model" scope="col">Model</th>
                    <th scope="col">Provider</th>
                    <th scope="col">Harness</th>
                    <th class="c-pass1 is-num" scope="col">pass@1</th>
                    <th class="is-num" scope="col">Search</th>
                    <th class="is-num" scope="col">Execution</th>
                    <th class="is-num" scope="col">Adaptability</th>
                    <th class="is-num" scope="col">Ambiguity</th>
                    <th class="is-num c-time" scope="col">Time</th>
                    <th class="is-num c-date" scope="col">Date</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        </div>
        <p style="color:var(--lb-muted-text, #9ca3af);font-size:0.78em;margin:12px 0 0;text-align:left;">* Accessed via OpenRouter. The harness does not round-trip reasoning context between turns for this provider, which may affect multi-step performance.</p>
    </div>
    """


eval_dataframe = None  # not used for CLI leaderboard anymore
legacy_dataframe = _load_results_df(LEGACY_RESULTS_DATASET, LEGACY_SCENARIO_LIST)


def refresh():
    return _load_results_df(RESULTS_DATASET, SCENARIO_LIST)


def refresh_legacy():
    return _load_results_df(LEGACY_RESULTS_DATASET, LEGACY_SCENARIO_LIST)


def restart_space():
    api.restart_space(repo_id=LEADERBOARD_PATH, token=TOKEN)


# ── App ──────────────────────────────────────────────────────────────────

demo = gr.Blocks(
    css=_APP_CSS,
    theme=gr.themes.Soft(
        font=[gr.themes.GoogleFont("Inter"), "Arial", "sans-serif"],
        primary_hue="blue",
    ),
)

with demo:
    gr.HTML(TITLE)

    with gr.Accordion("About", open=False):
        gr.Markdown(INTRODUCTION_TEXT)

    # ── Gaia2-CLI Leaderboard ────────────────────────────────────────
    gr.HTML(_build_leaderboard_html())

    # ── Vanilla Gaia2 Leaderboard ────────────────────────────────────
    gr.HTML(
        """
        <hr style="margin: 40px 0 20px 0; border: none; border-top: 1px solid #ddd;">
        <h2 style="margin: 0 0 10px 0; font-weight: 700; font-size: 1.4em;">
            Vanilla Gaia2 Leaderboard
        </h2>
        <p style="color: #666; margin: 0 0 15px 0;">
            Original benchmark with noise and agent-to-agent splits
        </p>
        """
    )

    legacy_table = gr.Dataframe(
        value=legacy_dataframe,
        interactive=False,
        wrap=False,
    )

    refresh_legacy_button = gr.Button("Refresh", variant="secondary", size="sm")
    refresh_legacy_button.click(refresh_legacy, inputs=[], outputs=[legacy_table])

    # ── Submit section ───────────────────────────────────────────────
    gr.HTML(
        """
        <hr style="margin: 40px 0 20px 0; border: none; border-top: 1px solid #ddd;">
        <h2 style="margin: 0 0 10px 0; font-weight: 700; font-size: 1.4em;">
            Run the Benchmark
        </h2>
        """
    )

    with gr.Accordion("How to run and submit", open=True):
        gr.Markdown(CONTACT_TEXT)

    # ── Links ────────────────────────────────────────────────────────
    gr.HTML(
        """
        <div style="text-align: center; margin: 30px 0; display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;">
            <a href="https://github.com/facebookresearch/meta-agents-research-environments" target="_blank"
            style="display: inline-flex; align-items: center; gap: 8px;
                    background: #24292e; color: white; font-weight: 600; padding: 10px 20px;
                    border-radius: 8px; text-decoration: none; font-size: 14px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="white" viewBox="0 0 24 24">
                    <path d="M12 .5C5.7.5.5 5.7.5 12c0 5.1 3.3 9.4 7.9 10.9.6.1.8-.2.8-.6v-2.1c-3.2.7-3.9-1.4-3.9-1.4-.5-1.2-1.2-1.6-1.2-1.6-1-.7.1-.7.1-.7 1.1.1 1.7 1.1 1.7 1.1 1 .1.8 1.4 2.9 1.9.3-.8.6-1.3.6-1.3-2.6-.3-5.3-1.3-5.3-5.8 0-1.3.5-2.4 1.1-3.3 0-.3-.5-1.6.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.6 1.6.1 2.9.1 3.2.7.9 1.1 2 1.1 3.3 0 4.5-2.7 5.5-5.3 5.8.4.3.7 1 .7 2v3c0 .3.2.7.8.6A11.5 11.5 0 0 0 23.5 12C23.5 5.7 18.3.5 12 .5Z"/>
                </svg>
                GitHub
            </a>
            <a href="https://arxiv.org/abs/2602.11964" target="_blank"
            style="display: inline-flex; align-items: center; gap: 8px;
                    background: #0081FB; color: white; font-weight: 600; padding: 10px 20px;
                    border-radius: 8px; text-decoration: none; font-size: 14px;">
                Paper
            </a>
        </div>
        """
    )

    # ── Citation ─────────────────────────────────────────────────────
    with gr.Accordion("Citation", open=False):
        gr.Textbox(
            value=CITATION_BUTTON_TEXT,
            label=CITATION_BUTTON_LABEL,
            elem_id="citation-button",
            show_copy_button=True,
        )


scheduler = BackgroundScheduler()
scheduler.add_job(restart_space, "interval", seconds=3600)
scheduler.start()
demo.launch(debug=True, server_name="0.0.0.0", server_port=7860)
