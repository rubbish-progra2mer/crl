from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import requests

OUT = Path(__file__).resolve().parents[1] / "experiment_v001" / "exp-h15-002-screen-b"
SCHEMAS = "ship(city,kg,service=standard|express); temperature(value,from_scale,to_scale); stock(product,warehouse); meeting(day,hour,minutes)"
ITEMS = [
{"id":"s1","task":"Express shipping for 2 kg to Rome.","expected":{"name":"ship","arguments":{"city":"Rome","kg":2,"service":"express"}},"failed":{"name":"ship","arguments":{"city":"Rome","kg":2,"service":"fast"}},"category":"Argument value violates the service enum."},
{"id":"s2","task":"Standard shipping for 5 kg to Oslo.","expected":{"name":"ship","arguments":{"city":"Oslo","kg":5,"service":"standard"}},"failed":{"name":"ship","arguments":{"city":"Oslo","kg":5,"service":"express"}},"category":"One argument conflicts with requested service."},
{"id":"t1","task":"Convert 32 Fahrenheit to Celsius.","expected":{"name":"temperature","arguments":{"value":32,"from_scale":"fahrenheit","to_scale":"celsius"}},"failed":{"name":"temperature","arguments":{"value":32,"from_scale":"celsius","to_scale":"fahrenheit"}},"category":"Source and target scales are reversed."},
{"id":"t2","task":"Convert 10 Celsius to Fahrenheit.","expected":{"name":"temperature","arguments":{"value":10,"from_scale":"celsius","to_scale":"fahrenheit"}},"failed":{"name":"temperature","arguments":{"value":10,"from_scale":"fahrenheit","to_scale":"celsius"}},"category":"Source and target scales are reversed."},
{"id":"i1","task":"Check product AX-7 in warehouse W2.","expected":{"name":"stock","arguments":{"product":"AX-7","warehouse":"W2"}},"failed":{"name":"stock","arguments":{"product":"AX-7","warehouse":"W3"}},"category":"Warehouse conflicts with request."},
{"id":"i2","task":"Check product B9 in warehouse NORTH.","expected":{"name":"stock","arguments":{"product":"B9","warehouse":"NORTH"}},"failed":{"name":"stock","arguments":{"product":"B8","warehouse":"NORTH"}},"category":"Product conflicts with request."},
{"id":"m1","task":"Schedule 45 minutes on 2026-09-03 at hour 14.","expected":{"name":"meeting","arguments":{"day":"2026-09-03","hour":14,"minutes":45}},"failed":{"name":"meeting","arguments":{"day":"2026-09-03","hour":14,"minutes":30}},"category":"Duration conflicts with request."},
{"id":"m2","task":"Schedule 30 minutes on 2026-10-11 at hour 9.","expected":{"name":"meeting","arguments":{"day":"2026-10-11","hour":9,"minutes":30}},"failed":{"name":"meeting","arguments":{"day":"2026-10-12","hour":9,"minutes":30}},"category":"Date conflicts with request."}
]

def attempt(item: dict[str, Any], informative: bool) -> dict[str, Any]:
    error=item["category"] if informative else "Execution failed. Try again."
    prompt=f"Available functions: {SCHEMAS}\nTask: {item['task']}\nFailed call: {json.dumps(item['failed'])}\nError: {error}\nReturn the corrected call as JSON with keys name and arguments."
    result=requests.post("http://127.0.0.1:11434/api/chat",timeout=180,json={"model":"qwen3:4b","messages":[{"role":"system","content":"Return only one JSON object."},{"role":"user","content":prompt}],"format":"json","stream":False,"think":False,"options":{"temperature":0,"seed":15002,"num_predict":1024}})
    result.raise_for_status()
    content=(result.json().get("message") or {}).get("content") or "{}"
    try: parsed=json.loads(content)
    except json.JSONDecodeError: parsed={}
    return {"case_id":item["id"],"condition":"category" if informative else "opaque","success":parsed==item["expected"],"parsed":parsed,"expected":item["expected"]}

def main() -> None:
    OUT.mkdir(parents=True,exist_ok=True)
    rows=[attempt(item,info) for item in ITEMS for info in (False,True)]
    opaque=sum(r["success"] for r in rows if r["condition"]=="opaque")
    category=sum(r["success"] for r in rows if r["condition"]=="category")
    metrics={"evidence_fidelity":"SCREENING","independent_implementation_count":2,"task_count":8,"opaque_successes":opaque,"category_successes":category,"category_gain":category-opaque,"parse_failure_count":sum(not r["parsed"] for r in rows)}
    (OUT/"observations.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    (OUT/"metrics.json").write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps(metrics,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
