# Experiment Result

```json
{
  "experiment_id": "v002",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "474161b7a7787429c454e77df06ccb8652580e5fecfcb89ea18591e406a19672",
  "candidate_sha256": "2a2c37fe390bf70f952922a8b4f5d8925178ac5b1037fac4b7c36cc42f9af6d0",
  "evidence_packet_sha256": "3e029d124d71f76736770742f7bb8bbdaaf72fdbbebfe8937db5693a9ce19145",
  "execution": {
    "command": "[\"D:\\\\Desktop\\\\crl\\\\crl_agent_v3\\\\.venv\\\\python.exe\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v002\\\\artifacts\\\\audit.py\", \"--config\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v002\\\\artifacts\\\\config.json\", \"acquire\", \"--phase\", \"development\", \"--queries-output\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v002\\\\work\\\\dev_acquire_001\\\\development_queries.jsonl\", \"--corpus-output\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v002\\\\work\\\\dev_acquire_001\\\\development_corpus.jsonl\", \"--manifest-output\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v002\\\\work\\\\dev_acquire_001\\\\development_acquisition_manifest.json\"]",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v002",
    "exit_code": 1,
    "stdout": "",
    "stderr": "Traceback (most recent call last):\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v002\\artifacts\\audit.py\", line 636, in <module>\n    raise SystemExit(main())\n                     ^^^^^^\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v002\\artifacts\\audit.py\", line 631, in main\n    return acquire(args)\n           ^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v002\\artifacts\\audit.py\", line 165, in acquire\n    rows = fetch_rows(tool_id, str(tool_config), str(tool_spec[\"split\"]), workers)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v002\\artifacts\\audit.py\", line 112, in fetch_rows\n    for offset, value in zip(offsets, values, strict=True):\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\concurrent\\futures\\_base.py\", line 619, in result_iterator\n    yield _result_or_cancel(fs.pop())\n          ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\concurrent\\futures\\_base.py\", line 317, in _result_or_cancel\n    return fut.result(timeout)\n           ^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\concurrent\\futures\\_base.py\", line 456, in result\n    return self.__get_result()\n           ^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\concurrent\\futures\\_base.py\", line 401, in __get_result\n    raise self._exception\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\concurrent\\futures\\thread.py\", line 58, in run\n    result = self.fn(*self.args, **self.kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v002\\artifacts\\audit.py\", line 109, in <lambda>\n    lambda offset: fetch_json(rows_url(dataset_id, config, split, offset)),\n                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v002\\artifacts\\audit.py\", line 71, in fetch_json\n    with urllib.request.urlopen(request, timeout=60) as response:\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 216, in urlopen\n    return opener.open(url, data, timeout)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 525, in open\n    response = meth(req, response)\n               ^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 634, in http_response\n    response = self.parent.error(\n               ^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 563, in error\n    return self._call_chain(*args)\n           ^^^^^^^^^^^^^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 496, in _call_chain\n    result = func(*args)\n             ^^^^^^^^^^^\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\urllib\\request.py\", line 643, in http_error_default\n    raise HTTPError(req.full_url, code, msg, hdrs, fp)\nurllib.error.HTTPError: HTTP Error 429: Too Many Requests\n",
    "environment": {
      "python_executable": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe",
      "python_version": "3.11.15",
      "result_scope": "acquisition failed before corpus completion; no retrieval metric exists"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v002/artifacts/audit.py",
      "byte_count": 25397,
      "sha256": "db96542622185ebc0adaad38a7fc1734bb20bd64f385037b40f25d7ef0a4f524"
    },
    {
      "relative_path": "experiment_v002/artifacts/config.json",
      "byte_count": 1192,
      "sha256": "2377b265cd8a60628fd6293b16da29ff17ab0295c8910232e7a5541f488f925a"
    },
    {
      "relative_path": "experiment_v002/artifacts/dev_acquire_001_execution.json",
      "byte_count": 2869,
      "sha256": "59deef9233f8d5cbdecc03d5b72a2dd4451647f027c758332938563116a14865"
    },
    {
      "relative_path": "experiment_v002/artifacts/dev_acquire_001_stdout.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v002/artifacts/dev_acquire_001_stderr.bin",
      "byte_count": 3118,
      "sha256": "e1a4bdcbb26437238031d3b34d2e387ddbb40ca7ba554509f6ae26413ef35b34"
    },
    {
      "relative_path": "experiment_v002/artifacts/dev_acquire_001_partial_development_queries.jsonl",
      "byte_count": 2787825,
      "sha256": "b785627bffe17b69bb58ccc664f20375735e56b6870322e3dad43a771f025d31"
    },
    {
      "relative_path": "experiment_v002/artifacts/attempts_manifest.json",
      "byte_count": 1535,
      "sha256": "3972b0fff2ed4cc05de078faebb0efac2fcbd81da602c46d6ee3faa2c24da80c"
    }
  ]
}
```

## Codex Interpretation

Development was not scientifically evaluated. The first acquisition attempt persisted all Development query rows, then received HTTP 429 while paging the full tool corpus; corpus and acquisition manifest were not produced. The frozen v002 config used one HTTP worker but still exhausted the rows endpoint request quota and cannot be overwritten after execution. This version is superseded for execution only; the same research claim proceeds as v003 with fixed one-second request pacing and no dependency change.