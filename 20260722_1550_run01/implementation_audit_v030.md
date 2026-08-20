# Main Codex Implementation Audit v030

Disposition: `APPROVED_FOR_DEVELOPMENT_ARTIFACT_FREEZE`.

I read the complete v030 Candidate, Problem, Research Map, Selection Context, nearest-prior commitment, scoring program, independent auditor, config builder, conditional Confirmation acquisition script, config and tests before any v030 feature score or ranking was executed.

## Computation and boundary

- The scoring path opens only each record's SHA-bound base query and optional base answer. Head/post-fix data are not represented by a scoring key.
- Merged patches supply changed entry IDs as exposed Development labels. Repaired values do not enter question, schema, reference, channel or score construction.
- The six channels and their `4,4,4,4,2,4` weights are literal in the frozen code. Controls, per-PR pools and SHA tie breaking share the same labels and source bytes.
- Development and conditional Confirmation use the same scoring and independent-audit code. The builder contains both fixed PR lists and both gate presets before Confirmation acquisition; a later Confirmation config may only bind the fixed, newly acquired records.
- The fixed Confirmation IDs are `1084, 1085, 1086, 1087, 1175, 1177`. Their file listings, patches and data bytes remain absent. The acquisition script cannot run before a positive written Main-Codex Development Promotion Audit.

## Independent audit

The auditor does not import `program.py`. It independently:

- verifies every metadata, patch-list, base-query and base-answer SHA;
- recovers changed IDs from removed patch rows;
- reparses reference calls and recursively recomputes all six feature channels;
- recomputes all seven scores, SHA tie ranks, MRR, MAP, Recall@10 and top-10 PR coverage;
- reruns the fixed 20,000 PR-cluster bootstrap;
- replays phase gates and checks the primary summary contract.

Support requires zero channel, score, rank and metric error plus `AUDIT_OK`.

## Actual pre-freeze checks

- Shared Python `3.11.15` compiled five source files in memory with exit `0`.
- `python -B -m pytest ...\test_program.py -q -p no:cacheprovider` exited `0`: `5 passed in 0.05s`.
- The Development builder exited `0` and produced phase `development`, 8 records, 9 changed IDs and the exact fixed gate object.
- A separate binding check opened and rehashed all 31 config-bound source files: missing `0`, SHA mismatches `0`, non-base scoring fields `0`.
- The generated source manifest records 16 GitHub API responses, 30 downloaded data files, 31 scoring-bound files and 4 local prior PDFs. Independent rehashing checked 50 unique local source/PDF facts with mismatches `0`.
- The acquisition transcript contains two real HTTP 404 responses for inferred PR-962 possible-answer paths. No absent answer file is represented as downloaded or bound.
- Encoding roundtrip checks passed for all edited scripts as UTF-8 without BOM and LF. Generated `__pycache__` and `.pytest_cache` directories were removed after exact-path validation; `CACHE_LEFT=0`.

## Frozen-byte candidates

- Candidate: `0c32820a453be37564888f69d4e829af12dfd9b73845ae76c64c4be0a503a2fc`
- Problem: `83766bea1548e72787dc9072072cf639fc59ef877c57a8ca66eafbc37bf4592d`
- Research Map: `afc2129d3882d7d7e27f5409dcaedd393902a89c727e8e1a3e94114a021f69d0`
- Selection Context: `e413fe37551dd0b3f195887491698734b0d061ee7056cec19d8e42d4c6c3f3ff`
- Nearest Prior: `d178befec244dcd8f5a8db8778143569ed404e6b6a925e983e884dcd379ba680`
- Program: `e400d51e39ea886f82ec6bcc187b7923d4004a0a487204f98f036f2ff8b9c290`
- Independent auditor: `695bbbeaab08fc9176832222608904c046fa11b6edf5db4ed65d47dc3de43f8d`
- Config builder: `22a7e2bbb20f2ce91bd671bc93c1ece93a6c534ee8bab7d7ea6bf93488643baa`
- Conditional acquisition: `7e3e699c9fdfe2b8a9b956f70b52e4871ffbd6d7b55299f8f78467abcc1bf25a`
- Tests: `366b4ca9fd9f2ff95878bb645b9527407084dcfdfc339a753c8addefd112d6b6`
- Development config: `d09872217c94d11cea04c56282656e2a298ba885e724e6f85ad42ce99923e2a1`
- Source manifest: `45e30446bbe312c2acc1770f9ce0517c1d3aea1089f1d4162f2bfd3cf37850ed`

This audit authorizes immutable artifact copying and one publish-once v030 Development Plan. It does not authorize Development execution by itself, Confirmation, Review, Decision, Delivery or `READY_FOR_RESEARCH_USAGE`.
