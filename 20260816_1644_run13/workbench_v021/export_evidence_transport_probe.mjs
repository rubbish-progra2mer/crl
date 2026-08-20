import fs from "node:fs";
import path from "node:path";

import {
  buildModelInputFor,
  reshapeToLegacy
} from "./steerbench-work/src/canonical-runner.mjs";
import { STEERBENCH_STEERING_SYSTEM_PROMPT } from "./steerbench-work/src/prompts.mjs";

const scenarioDir = path.resolve(
  "workbench_v021/steerbench-work/scenario-sets/steerbench-work-2026-05"
);
const outputPath = path.resolve("workbench_v021/evidence_transport_probe_inputs.json");

const RAW_BASE_KEYS = new Set([
  "id",
  "legacy_id",
  "source_type",
  "title",
  "status",
  "raw_ref"
]);

function listScenarioFiles() {
  return fs.readdirSync(scenarioDir)
    .filter((name) => name.endsWith(".json") && !name.startsWith("_"))
    .sort();
}

function readScenario(file) {
  return JSON.parse(fs.readFileSync(path.join(scenarioDir, file), "utf8"));
}

function evidenceWithPayload(rawEvidence) {
  return (rawEvidence || []).map((item) => {
    const projected = {
      evidence_id: item.legacy_id || item.id,
      source_type: item.source_type,
      title: item.title,
      status: item.status,
      raw_ref: item.raw_ref
    };
    for (const [key, value] of Object.entries(item)) {
      if (!RAW_BASE_KEYS.has(key)) projected[key] = value;
    }
    return projected;
  });
}

function buildPair(raw) {
  const canonicalScenario = reshapeToLegacy(raw);
  const canonicalInput = buildModelInputFor(canonicalScenario).model_input;

  const payloadScenario = reshapeToLegacy(raw);
  payloadScenario.evidence = evidenceWithPayload(raw.evidence);
  const payloadInput = buildModelInputFor(payloadScenario).model_input;

  const rawExtraKeys = [...new Set((raw.evidence || []).flatMap((item) =>
    Object.keys(item).filter((key) => !RAW_BASE_KEYS.has(key))
  ))].sort();

  return {
    id: raw.id,
    expected_permission: raw.expected_behavior?.correct_action === "continue"
      ? "allowed"
      : "blocked",
    taxonomy_direction: raw.taxonomy?.direction || null,
    raw_evidence_count: (raw.evidence || []).length,
    raw_extra_keys: rawExtraKeys,
    canonical_input: canonicalInput,
    payload_preserving_input: payloadInput,
    inputs_identical: canonicalInput === payloadInput
  };
}

function auditCorpus(rawScenarios) {
  let evidenceRecords = 0;
  let recordsWithExtraFields = 0;
  let recordsWithToolResults = 0;
  const extraKeyCounts = new Map();

  for (const raw of rawScenarios) {
    for (const item of raw.evidence || []) {
      evidenceRecords += 1;
      const extras = Object.keys(item).filter((key) => !RAW_BASE_KEYS.has(key));
      if (extras.length > 0) recordsWithExtraFields += 1;
      if (Object.hasOwn(item, "tool_call_result")) recordsWithToolResults += 1;
      for (const key of extras) {
        extraKeyCounts.set(key, (extraKeyCounts.get(key) || 0) + 1);
      }
    }
  }

  return {
    scenario_count: rawScenarios.length,
    evidence_record_count: evidenceRecords,
    records_with_extra_fields: recordsWithExtraFields,
    records_with_tool_call_result: recordsWithToolResults,
    extra_key_counts: Object.fromEntries([...extraKeyCounts.entries()].sort())
  };
}

const rawScenarios = listScenarioFiles().map(readScenario);
const mirrorCases = rawScenarios
  .filter((raw) => raw.tags?.includes("tier_b_underrefusal_mirror"))
  .sort((a, b) => a.id.localeCompare(b.id))
  .slice(0, 10);
const unsafeCases = rawScenarios
  .filter((raw) => raw.tags?.includes("high_impact"))
  .sort((a, b) => a.id.localeCompare(b.id))
  .slice(0, 10);
const selected = [...mirrorCases, ...unsafeCases]
  .sort((a, b) => a.id.localeCompare(b.id));

const artifact = {
  schema_version: "crl.evidence_transport_probe_inputs.v1",
  source_repository: "https://github.com/AgentDock/steerbench-work",
  source_commit: "fa7eb3ed06a91e5f359b5edb6a6f760a3f35b248",
  selection_rule: "first 10 lexicographic tier-B incident mirrors plus first 10 lexicographic high-impact anchors",
  system_prompt: STEERBENCH_STEERING_SYSTEM_PROMPT,
  corpus_audit: auditCorpus(rawScenarios),
  cases: selected.map(buildPair)
};

fs.writeFileSync(outputPath, `${JSON.stringify(artifact, null, 2)}\n`, "utf8");
process.stdout.write(`${outputPath}\n`);
process.stdout.write(`${JSON.stringify(artifact.corpus_audit, null, 2)}\n`);

