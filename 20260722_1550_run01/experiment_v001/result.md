# Experiment Result

```json
{
  "experiment_id": "v001",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "11be2bb8810e30c3d445816c44648da2288eb62e4fc9f9c5cbf9e6e0d5d99221",
  "candidate_sha256": "8c2dea3772d06086f86378cdf131e96e467c00590b0a1aea8b8e278ce075f3a7",
  "evidence_packet_sha256": "c7f31b683b955e1d6e383d0336fb0f51f1fdbb3edc18b60050d69ea2d696c6a3",
  "execution": {
    "command": "[\"D:\\\\Desktop\\\\crl\\\\crl_agent_v3\\\\.venv\\\\python.exe\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v001\\\\artifacts\\\\audit.py\", \"--config\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v001\\\\artifacts\\\\config.json\", \"acquire\", \"--phase\", \"development\", \"--queries-output\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v001\\\\work\\\\dev_acquire_001\\\\development_queries.jsonl\", \"--corpus-output\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v001\\\\work\\\\dev_acquire_001\\\\development_corpus.jsonl\", \"--manifest-output\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v001\\\\work\\\\dev_acquire_001\\\\development_acquisition_manifest.json\"]",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v001",
    "exit_code": 1,
    "stdout": "",
    "stderr": "Traceback (most recent call last):\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v001\\artifacts\\audit.py\", line 636, in <module>\n    raise SystemExit(main())\n                     ^^^^^^\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v001\\artifacts\\audit.py\", line 631, in main\n    return acquire(args)\n           ^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v001\\artifacts\\audit.py\", line 165, in acquire\n    rows = fetch_rows(tool_id, str(tool_config), str(tool_spec[\"split\"]), workers)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v001\\artifacts\\audit.py\", line 112, in fetch_rows\n    for offset, value in zip(offsets, values, strict=True):\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\concurrent\\futures\\_base.py\", line 619, in result_iterator\n    yield _result_or_cancel(fs.pop())\n          ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\concurrent\\futures\\_base.py\", line 317, in _result_or_cancel\n    return fut.result(timeout)\n           ^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\concurrent\\futures\\_base.py\", line 456, in result\n    return self.__get_result()\n           ^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\concurrent\\futures\\_base.py\", line 401, in __get_result\n    raise self._exception\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\concurrent\\futures\\thread.py\", line 58, in run\n    result = self.fn(*self.args, **self.kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v001\\artifacts\\audit.py\", line 109, in <lambda>\n    lambda offset: fetch_json(rows_url(dataset_id, config, split, offset)),\n                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v001\\artifacts\\audit.py\", line 71, in fetch_json\n    with urllib.request.urlopen(request, timeout=60) as response:\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 216, in urlopen\n    return opener.open(url, data, timeout)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 525, in open\n    response = meth(req, response)\n               ^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 634, in http_response\n    response = self.parent.error(\n               ^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 563, in error\n    return self._call_chain(*args)\n           ^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 496, in _call_chain\n    result = func(*args)\n             ^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 643, in http_error_default\n    raise HTTPError(req.full_url, code, msg, hdrs, fp)\nurllib.error.HTTPError: HTTP Error 429: Too Many Requests\n",
    "environment": {
      "python_executable": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe",
      "python_version": "3.11.15",
      "result_scope": "acquisition failed before corpus completion; no retrieval metric exists"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v001/artifacts/audit.py",
      "byte_count": 25397,
      "sha256": "db96542622185ebc0adaad38a7fc1734bb20bd64f385037b40f25d7ef0a4f524"
    },
    {
      "relative_path": "experiment_v001/artifacts/config.json",
      "byte_count": 1193,
      "sha256": "8b307524c48defc3be60fae914ae5d1d4a69321015707cde75b90239f82cf07f"
    },
    {
      "relative_path": "experiment_v001/artifacts/dev_acquire_001_execution.json",
      "byte_count": 2870,
      "sha256": "9cc9b5e3842423edc59ef693737561268dab96cfbae60a17a877069adfdc9997"
    },
    {
      "relative_path": "experiment_v001/artifacts/dev_acquire_001_stdout.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v001/artifacts/dev_acquire_001_stderr.bin",
      "byte_count": 3118,
      "sha256": "1ca4f85426d94ffff3642e534b5427dddee1d452addb8cef16983ed65ff77f20"
    },
    {
      "relative_path": "experiment_v001/artifacts/dev_acquire_001_partial_development_queries.jsonl",
      "byte_count": 2787825,
      "sha256": "b785627bffe17b69bb58ccc664f20375735e56b6870322e3dad43a771f025d31"
    },
    {
      "relative_path": "experiment_v001/artifacts/attempts_manifest.json",
      "byte_count": 1535,
      "sha256": "4490f6b1f00a59aceb324f303aadee71164b3048e782ce3f0c81944e394d0d6e"
    }
  ]
}
```

## Codex Interpretation

Development was not scientifically evaluated. The first acquisition attempt persisted all Development query rows, then received HTTP 429 while paging the full tool corpus; corpus and acquisition manifest were not produced. The frozen v001 config used 16 HTTP workers and cannot be overwritten after execution. This version is superseded for execution only; the same research claim proceeds as v002 with a single-worker acquisition config.