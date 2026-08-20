from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiment_v001" / "exp-h15-002-screen-a"

TOOLS = [
    {"type":"function","function":{"name":"ship","description":"Quote parcel shipping.","parameters":{"type":"object","properties":{"city":{"type":"string"},"kg":{"type":"number"},"service":{"type":"string","enum":["standard","express"]}},"required":["city","kg","service"]}}},
    {"type":"function","function":{"name":"temperature","description":"Convert temperature scales.","parameters":{"type":"object","properties":{"value":{"type":"number"},"from_scale":{"type":"string","enum":["celsius","fahrenheit"]},"to_scale":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["value","from_scale","to_scale"]}}},
    {"type":"function","function":{"name":"stock","description":"Look up product inventory.","parameters":{"type":"object","properties":{"product":{"type":"string"},"warehouse":{"type":"string"}},"required":["product","warehouse"]}}},
    {"type":"function","function":{"name":"meeting","description":"Schedule a meeting.","parameters":{"type":"object","properties":{"day":{"type":"string"},"hour":{"type":"integer"},"minutes":{"type":"integer"}},"required":["day","hour","minutes"]}}}
]

CASES = [
    ("s1","Express shipping for 2 kg to Rome.","ship",{"city":"Rome","kg":2,"service":"express"},{"city":"Rome","kg":2,"service":"fast"},"Argument value violates the service enum."),
    ("s2","Standard shipping for 5 kg to Oslo.","ship",{"city":"Oslo","kg":5,"service":"standard"},{"city":"Oslo","kg":5,"service":"express"},"One argument value conflicts with the requested service."),
    ("t1","Convert 32 Fahrenheit to Celsius.","temperature",{"value":32,"from_scale":"fahrenheit","to_scale":"celsius"},{"value":32,"from_scale":"celsius","to_scale":"fahrenheit"},"Source and target scale arguments are reversed."),
    ("t2","Convert 10 Celsius to Fahrenheit.","temperature",{"value":10,"from_scale":"celsius","to_scale":"fahrenheit"},{"value":10,"from_scale":"fahrenheit","to_scale":"celsius"},"Source and target scale arguments are reversed."),
    ("i1","Check product AX-7 in warehouse W2.","stock",{"product":"AX-7","warehouse":"W2"},{"product":"AX-7","warehouse":"W3"},"The warehouse argument conflicts with the request."),
    ("i2","Check product B9 in warehouse NORTH.","stock",{"product":"B9","warehouse":"NORTH"},{"product":"B8","warehouse":"NORTH"},"The product argument conflicts with the request."),
    ("m1","Schedule 45 minutes on 2026-09-03 at hour 14.","meeting",{"day":"2026-09-03","hour":14,"minutes":45},{"day":"2026-09-03","hour":14,"minutes":30},"The duration argument conflicts with the request."),
    ("m2","Schedule 30 minutes on 2026-10-11 at hour 9.","meeting",{"day":"2026-10-11","hour":9,"minutes":30},{"day":"2026-10-12","hour":9,"minutes":30},"The date argument conflicts with the request.")
]

def run(case: tuple[Any, ...], category: bool) -> dict[str, Any]:
    cid, task, name, expected, failed, category_message = case
    feedback = category_message if category else "Execution failed. Try again."
    prompt = f"User task: {task}\nPrevious failed call: {json.dumps({'name': name, 'arguments': failed})}\nTool error: {feedback}\nIssue exactly one corrected tool call."
    payload = {"model":"qwen3:4b","messages":[{"role":"system","content":"Correct the failed call using one supplied tool. Do not answer in prose."},{"role":"user","content":prompt}],"tools":TOOLS,"stream":False,"think":False,"options":{"temperature":0,"seed":15001,"num_predict":1024}}
    req = urllib.request.Request("http://127.0.0.1:11434/api/chat",data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=180) as response:
        body=json.loads(response.read().decode())
    calls=(body.get("message") or {}).get("tool_calls") or []
    emitted=(calls[0].get("function") if len(calls)==1 else {}) or {}
    arguments=emitted.get("arguments") or {}
    if isinstance(arguments,str): arguments=json.loads(arguments)
    success=len(calls)==1 and emitted.get("name")==name and arguments==expected
    return {"case_id":cid,"condition":"category" if category else "opaque","success":success,"call_count":len(calls),"emitted":{"name":emitted.get("name"),"arguments":arguments},"expected":{"name":name,"arguments":expected}}

def main() -> None:
    OUT.mkdir(parents=True,exist_ok=True)
    rows=[run(case,condition) for case in CASES for condition in (False,True)]
    pairs={cid:{r["condition"]:r for r in rows if r["case_id"]==cid} for cid,*_ in CASES}
    metrics={"evidence_fidelity":"SCREENING","task_count":8,"opaque_successes":sum(r["success"] for r in rows if r["condition"]=="opaque"),"category_successes":sum(r["success"] for r in rows if r["condition"]=="category"),"category_gain":sum(p["category"]["success"] for p in pairs.values())-sum(p["opaque"]["success"] for p in pairs.values()),"paired_difference_ids":[cid for cid,p in pairs.items() if p["category"]["success"]!=p["opaque"]["success"]]}
    (OUT/"observations.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    (OUT/"metrics.json").write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps(metrics,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
