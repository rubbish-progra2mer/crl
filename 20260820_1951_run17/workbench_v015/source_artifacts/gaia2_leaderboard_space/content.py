OWNER = "meta-agents-research-environments"
CONTACT_DATASET = f"{OWNER}/leaderboard_contact_info_internal"
RESULTS_DATASET = f"{OWNER}/leaderboard_results"
LEGACY_RESULTS_DATASET = RESULTS_DATASET  # old results live in the same dataset for now
LEADERBOARD_PATH = f"{OWNER}/leaderboard"

TITLE = """
<div style="text-align: center; padding: 20px 0; background: linear-gradient(135deg, #1877f2 0%, #42a5f5 100%); border-radius: 15px; margin-bottom: 30px;">
    <h1 style="color: white; font-size: 2em; margin: 0; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
        Gaia2 Leaderboard 🏆
    </h1>
</div>
"""

# Gaia2-CLI splits (current benchmark)
SCENARIO_LIST = [
    "search",
    "execution",
    "adaptability",
    "ambiguity",
    "time",
]

# Legacy splits (old benchmark, includes noise and A2A)
LEGACY_SCENARIO_LIST = [
    "execution",
    "search",
    "ambiguity",
    "adaptability",
    "time",
    "mini_noise",
    "mini_agent2agent",
]

MAX_PARALLELISM = 10

INTRODUCTION_TEXT = """
[**Gaia2**](https://huggingface.co/datasets/meta-agents-research-environments/gaia2-cli) is a benchmark designed to measure general agent capabilities. Beyond traditional search and execution tasks, Gaia2 runs asynchronously, requiring agents to handle ambiguities, adapt to dynamic environments, and operate under temporal constraints.

Gaia2 evaluates agents across the following dimensions: **Execution** (instruction following, multi-step tool-use), **Search** (information retrieval), **Ambiguity** (handling unclear or incomplete instructions), **Adaptability** (responding to dynamic environment changes), and **Time** (managing temporal constraints and scheduling).

⚠️ All scores on this page are reported by the submitting team.
"""

CONTACT_TEXT = """
1. Clone the [gaia2-cli](https://github.com/facebookresearch/meta-agents-research-environments) repository and follow the setup instructions
2. Run the benchmark on all 5 splits (execution, search, ambiguity, adaptability, time)
3. Contact us to validate and update your scores on the leaderboard

**Contact:** Open an issue on the [GitHub repository](https://github.com/facebookresearch/meta-agents-research-environments/issues) and we will review and add your scores.
"""

CITATION_BUTTON_LABEL = "Copy the following snippet to cite these results"
CITATION_BUTTON_TEXT = r"""@misc{froger2026gaia2benchmarkingllmagents,
      title={Gaia2: Benchmarking LLM Agents on Dynamic and Asynchronous Environments},
      author={Romain Froger and Pierre Andrews and Matteo Bettini and Amar Budhiraja and Ricardo Silveira Cabral and Virginie Do and Emilien Garreau and Jean-Baptiste Gaya and Hugo Laurençon and Maxime Lecanu and Kunal Malkan and Dheeraj Mekala and Pierre Ménard and Gerard Moreno-Torres Bertran and Ulyana Piterbarg and Mikhail Plekhanov and Mathieu Rita and Andrey Rusakov and Vladislav Vorotilov and Mengjue Wang and Ian Yu and Amine Benhalloum and Grégoire Mialon and Thomas Scialom},
      year={2026},
      eprint={2602.11964},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2602.11964},
}"""
