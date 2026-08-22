from pathlib import Path

from setuptools import find_packages, setup


ROOT = Path(__file__).resolve().parent


setup(
    name="search-control-preferences",
    version="0.1.0",
    description=(
        "Reference implementation for search-control preference "
        "construction and training"
    ),
    long_description=(ROOT / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires=">=3.10",

    package_dir={"": "src"},
    packages=find_packages("src"),

    py_modules=[
        "context",
        "jsonl_io",
        "preferences",
        "prompts",
        "questions",
        "schema",
        "teacher",
    ],

    # Lightweight dependencies used by the core preference-construction
    # pipeline. Training, local inference, and benchmark-specific utilities
    # are exposed through optional extras below.
    install_requires=[
        "openai>=1.30",
    ],

    extras_require={
        # DPO training dependencies.
        "train": [
            "accelerate>=0.30",
            "datasets>=4.2,<4.3",
            "torch>=2.1",
            "transformers>=4.57,<4.58",
            "trl>=0.24,<0.25",
        ],

        # Local policy inference and rerouting passage scoring.
        "infer": [
            "accelerate>=0.30",
            "torch>=2.1",
            "transformers>=4.57,<4.58",
            "vllm",
        ],

        # Benchmark and training-question preparation.
        "data": [
            "datasets>=2.19",
            "huggingface-hub>=0.23",
        ],

        # GAIA retriever service.
        "gaia": [
            "requests>=2.31",
        ],

        # Development and testing.
        "test": [
            "pytest>=8",
        ],

        # Full installation for reproducing the released pipeline.
        "all": [
            "accelerate>=0.30",
            "datasets>=4.2,<4.3",
            "huggingface-hub>=0.23",
            "pytest>=8",
            "requests>=2.31",
            "torch>=2.1",
            "transformers>=4.57,<4.58",
            "trl>=0.24,<0.25",
            "vllm",
        ],
    },

    entry_points={
        "console_scripts": [
            "search-build-preferences=cli.build_preferences:main",
            "search-train=cli.train:main",
            "search-infer=cli.infer:main",
            "search-evaluate=cli.evaluate:main",
            "search-prepare-benchmark=cli.prepare_benchmark:main",
            (
                "search-prepare-training-questions="
                "cli.prepare_training_questions:main"
            ),
            (
                "search-serve-gaia-retriever="
                "cli.serve_gaia_retriever:main"
            ),
        ],
    },
)