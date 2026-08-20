# Evidence Packet v030

## Candidate identity

- Candidate: `candidate_v030.md`, SHA-256 `0c32820a453be37564888f69d4e829af12dfd9b73845ae76c64c4be0a503a2fc`.
- Research problem: `problem_v030.md`, SHA-256 `83766bea1548e72787dc9072072cf639fc59ef877c57a8ca66eafbc37bf4592d`.
- Research map: `research_map_v030.md`, SHA-256 `afc2129d3882d7d7e27f5409dcaedd393902a89c727e8e1a3e94114a021f69d0`.
- Selection context: `selection_context_v030.md`, SHA-256 `e413fe37551dd0b3f195887491698734b0d061ee7056cec19d8e42d4c6c3f3ff`.
- Nearest prior: `nearest_prior_v030.md`, SHA-256 `d178befec244dcd8f5a8db8778143569ed404e6b6a925e983e884dcd379ba680`.

## Formal knowledge evidence

- Failure Card `failure-semantically-related-toolkit-expansion`, Card SHA-256 `13f9b53bfc7c5abfed685fb6ca569a38c49e8df7aee196a3cbd43ff8b55d4223`.
- Paper Card `paper-p085`, Card SHA-256 `645c3de5d4fd20c6cb63e8a9c1c94fbe3461e5806401f34288cb256b37bdd6a8`.
- P084 source SHA-256 `8276bcab484eef370bc63afca580ea19d8f6e2ccc6c2afcdaf684225d5e635c7`.
- ToolRet source SHA-256 `26ce2766e8c4b72e88dfd2cf93bfe56ff758fea6fe0ec0bea34228f555311d2a`.

## Open-primary-source evidence

- PairReranker PDF SHA-256 `2d96cb361f9ebb63bb694d09194b6a32715fc2d7a7c959731f99a3eb466e4e48`.
- Pairwise Ranking Prompting PDF SHA-256 `2449d1f79f102f1b2c79f8b2b535e13419c5e10a0cf1edee17cd4811daa35354`.
- PRP-Graph PDF SHA-256 `8a8ba7e6bca389c0403485be0ac6da7e14bd5e6d89fb17f3dcbe780106fc02bb`.
- MagicSelector PDF SHA-256 `bce125f5d225d72bba71bbe9a5ace065bb79815c7980359be0422e3e0b538527`.
- EigenData arXiv v1 PDF SHA-256 `da87908b8000a4e29f7fc38fd455c612af12555ba5164579c6ef67285dae6ba5`.
- Official BFCL/Gorilla merged PR records for the fixed Development IDs.

## Development sources

`sources_v030/bfcl_development_history/` contains raw GitHub API metadata/file-list responses and available base/head data files for PRs `865, 870, 871, 872, 876, 892, 962, 963`.

Acquisition facts:

- API source files: 16;
- downloaded base/head data files: 30;
- downloaded data bytes: 4,634,523;
- inferred PR-962 possible-answer downloads: two HTTP 404 responses, no files created;
- changed IDs recovered from patches: 9;
- all eight PR metadata records report merged state.

The final source manifest, implementation, tests, config, implementation audit and their exact hashes must be frozen as Experiment Artifacts before Plan publication.

The generated source manifest is `sources_v030/source_manifest_v030.json`, SHA-256 `45e30446bbe312c2acc1770f9ce0517c1d3aea1089f1d4162f2bfd3cf37850ed`. Its 50 local byte facts were independently rehashed with zero mismatch.

## Implementation evidence

- scoring program `e400d51e39ea886f82ec6bcc187b7923d4004a0a487204f98f036f2ff8b9c290`;
- independent auditor `695bbbeaab08fc9176832222608904c046fa11b6edf5db4ed65d47dc3de43f8d`;
- phase config builder `22a7e2bbb20f2ce91bd671bc93c1ece93a6c534ee8bab7d7ea6bf93488643baa`;
- conditional Confirmation acquisition `7e3e699c9fdfe2b8a9b956f70b52e4871ffbd6d7b55299f8f78467abcc1bf25a`;
- unit tests `366b4ca9fd9f2ff95878bb645b9527407084dcfdfc339a753c8addefd112d6b6`;
- Development config `d09872217c94d11cea04c56282656e2a298ba885e724e6f85ad42ce99923e2a1`;
- Main Codex Implementation Audit `7cf97a4dc38959c181b931f24ea3e164f3d12cc61d62179a332e4c1717803535`;
- existing path-generic capture runner `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`.

Shared Python 3.11.15 compiled all five source files with exit `0`; the only unit-test command exited `0` with `5 passed in 0.05s`. This Packet authorizes no scientific execution until these exact bytes and all 31 scoring inputs are copied and rehashed under `experiment_v030/artifacts/`, and a publish-once Plan binds this Packet's final SHA.

## Confirmation isolation

No file listing, patch, base data or head data for PRs `1084, 1085, 1086, 1087, 1175, 1177` is present in the product. They remain conditional on a positive Main-Codex Development Promotion Audit.
