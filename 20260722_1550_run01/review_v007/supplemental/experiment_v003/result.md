# Experiment Result

```json
{
  "experiment_id": "v003",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "f0068337dd347141f41be66e70ac1d692b05afc482fbcbc050e48de7197a07d5",
  "candidate_sha256": "a9a4aa8c82e95c55007eca51402413b8b676e1467c9687bd8ffd8863e136bb03",
  "evidence_packet_sha256": "cc27bd0faddc5ccef653055695be85b14a33a4d6ddff4b87f0b745a5809677ae",
  "execution": {
    "command": "[\"D:\\\\Desktop\\\\crl\\\\crl_agent_v3\\\\.venv\\\\python.exe\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v003\\\\artifacts\\\\audit.py\", \"--config\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v003\\\\artifacts\\\\config.json\", \"acquire\", \"--phase\", \"development\", \"--queries-output\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v003\\\\work\\\\dev_acquire_001\\\\development_queries.jsonl\", \"--corpus-output\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v003\\\\work\\\\dev_acquire_001\\\\development_corpus.jsonl\", \"--manifest-output\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v003\\\\work\\\\dev_acquire_001\\\\development_acquisition_manifest.json\"]",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v003",
    "exit_code": 1,
    "stdout": "",
    "stderr": "Traceback (most recent call last):\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v003\\artifacts\\audit.py\", line 660, in <module>\n    raise SystemExit(main())\n                     ^^^^^^\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v003\\artifacts\\audit.py\", line 655, in main\n    return acquire(args)\n           ^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v003\\artifacts\\audit.py\", line 183, in acquire\n    rows = fetch_rows(\n           ^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v003\\artifacts\\audit.py\", line 123, in fetch_rows\n    for offset, value in zip(offsets, values, strict=True):\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\concurrent\\futures\\_base.py\", line 619, in result_iterator\n    yield _result_or_cancel(fs.pop())\n          ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\concurrent\\futures\\_base.py\", line 317, in _result_or_cancel\n    return fut.result(timeout)\n           ^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\concurrent\\futures\\_base.py\", line 456, in result\n    return self.__get_result()\n           ^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\concurrent\\futures\\_base.py\", line 401, in __get_result\n    raise self._exception\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\concurrent\\futures\\thread.py\", line 58, in run\n    result = self.fn(*self.args, **self.kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v003\\artifacts\\audit.py\", line 118, in <lambda>\n    lambda offset: fetch_json(\n                   ^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v003\\artifacts\\audit.py\", line 74, in fetch_json\n    with urllib.request.urlopen(request, timeout=60) as response:\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 216, in urlopen\n    return opener.open(url, data, timeout)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 525, in open\n    response = meth(req, response)\n               ^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 634, in http_response\n    response = self.parent.error(\n               ^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 563, in error\n    return self._call_chain(*args)\n           ^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 496, in _call_chain\n    result = func(*args)\n             ^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 643, in http_error_default\n    raise HTTPError(req.full_url, code, msg, hdrs, fp)\nurllib.error.HTTPError: HTTP Error 429: Too Many Requests\n",
    "environment": {
      "python_executable": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe",
      "python_version": "3.11.15",
      "result_scope": "acquisition failed before corpus completion; no retrieval metric exists"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v003/artifacts/audit.py",
      "byte_count": 25850,
      "sha256": "d97903a938096dcbee197a8af41617c1c1e2e4226438868c157ff1156c6231f4"
    },
    {
      "relative_path": "experiment_v003/artifacts/config.json",
      "byte_count": 1221,
      "sha256": "7b6e8fd6df080671be6c90769f0ffee1927737d915764018e4d412093e80e07f"
    },
    {
      "relative_path": "experiment_v003/artifacts/dev_acquire_001_execution.json",
      "byte_count": 2869,
      "sha256": "5eb75a8e1f090d0f2ec0a13bb4c2669f779d0a3be7db94f76606a14392ef13a7"
    },
    {
      "relative_path": "experiment_v003/artifacts/dev_acquire_001_stdout.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v003/artifacts/dev_acquire_001_stderr.bin",
      "byte_count": 2909,
      "sha256": "580094bfbb868d4066ad49909a65d3c2d56f1f09c2dd18060e68e7f1b1dfd761"
    },
    {
      "relative_path": "experiment_v003/artifacts/dev_acquire_001_partial_development_queries.jsonl",
      "byte_count": 2787825,
      "sha256": "b785627bffe17b69bb58ccc664f20375735e56b6870322e3dad43a771f025d31"
    },
    {
      "relative_path": "experiment_v003/artifacts/attempts_manifest.json",
      "byte_count": 1535,
      "sha256": "d01bad7832e3443beba43af1847dea5de2bda88b56a5a650cce96733c5d5f81e"
    }
  ]
}
```

## Codex Interpretation

Development was not scientifically evaluated. The first acquisition attempt persisted all Development query rows, then received HTTP 429 while paging the full tool corpus; corpus and acquisition manifest were not produced. The frozen v003 config used one HTTP worker with a one-second request interval but still received HTTP 429 after about one minute and cannot be overwritten after execution. This version is superseded for execution only; the same research claim proceeds as v004 with a fixed three-second request interval and no dependency change.