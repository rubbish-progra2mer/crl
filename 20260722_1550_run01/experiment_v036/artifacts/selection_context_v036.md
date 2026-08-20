# v036 Selection Context

v036 is an execution-only successor to v035. The one frozen v035 Development
payload exited `1` before evaluating any prompt because
`AutoModelForCausalLM.from_pretrained` received `device_map={"": "cuda"}` in
an environment without `accelerate`.

Frozen evidence:

- v035 execution:
  `8805f2a91a214c5dc2156909895ca11a5ede6447e63e7e036a23b05b3510e315`;
- v035 stderr:
  `ef0a9b170afc5ed93ef227fb6ae36fd3c048f7be3b063183cf547a9961ccbd4c`;
- v035 Result:
  `ceb05197a873f1ddb1d06dff50d56c6f263cd6577caae74372dc322312c17dfc`.

No metric or model preference was produced, ToolSandbox remains absent and
unread, and no scientific choice can be informed by v035 output.

v036 retains the exact SDEJ problem, research map, nearest-prior boundary,
Candidate computation, exposed Development data, frozen model, prompts,
controls, bootstrap, gates and Claim ceiling. The only authorized difference
is model placement:

```text
v035: from_pretrained(..., torch_dtype=float16, device_map={"": "cuda"})
v036: from_pretrained(..., dtype=float16).to("cuda")
```

The shared environment is not mutated and `accelerate` is not installed.

