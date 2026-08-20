"""Point the auditor at dashboard exhaust.

Writes a synthetic JSONL log in the messy field names real dashboards
use (pool_size, top_k, found), then audits it with zero configuration.
A tool-selection service runs K=40 over a 600-tool registry with about
6 relevant tools per query. The dashboard graphs 'found' and looks
healthy. The audit prices that number against a blind draw.
"""

import json
import random

from bor import audit, from_jsonl, random_success_at_least_one

random.seed(7)

LOG = "dashboard_exhaust.jsonl"
N_TOOLS, R_TYPICAL, K_SHOWN, N_QUERIES = 600, 6, 40, 800

with open(LOG, "w") as f:
    for i in range(N_QUERIES):
        R = max(1, round(random.gauss(R_TYPICAL, 2)))
        p_hit = min(1.0, 2.5 * random_success_at_least_one(N=N_TOOLS, R=R, K=K_SHOWN))
        row = {
            "query_id": f"req-{i:05d}",
            "pool_size": N_TOOLS,
            "top_k": K_SHOWN,
            "num_relevant": R,
            "found": random.random() < p_hit,
            "latency_ms": round(random.gauss(120, 30), 1),
        }
        f.write(json.dumps(row) + "\n")

records = from_jsonl(LOG)
print(audit(records).summary())

print(f"\nlog written to {LOG} (current directory)")
print(f"next: bor audit {LOG}")
