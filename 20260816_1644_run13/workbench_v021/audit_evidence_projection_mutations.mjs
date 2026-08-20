import fs from "node:fs";
import path from "node:path";

import {
  buildModelInputFor,
  reshapeToLegacy
} from "./steerbench-work/src/canonical-runner.mjs";

const scenarioDir = path.resolve(
  "workbench_v021/steerbench-work/scenario-sets/steerbench-work-2026-05"
);
const outputPath = path.resolve(
  "workbench_v021/evidence_projection_mutation_audit.json"
);

function listScenarioFiles() {
  return fs.readdirSync(scenarioDir)
    .filter((name) => name.endsWith(".json") && !name.startsWith("_"))
    .sort();
}

function cloneJson(value) {
  return JSON.parse(JSON.stringify(value));
}

function scalarLeaves(value, prefix = []) {
  if (value === null || ["string", "number", "boolean"].includes(typeof value)) {
    return [{ path: prefix, value }];
  }
  if (Array.isArray(value)) {
    return value.flatMap((item, index) => scalarLeaves(item, [...prefix, index]));
  }
  if (typeof value === "object") {
    return Object.entries(value).flatMap(([key, item]) =>
      scalarLeaves(item, [...prefix, key])
    );
  }
  return [];
}

function mutatedValue(value) {
  if (typeof value === "boolean") return !value;
  if (typeof value === "number") return value + 1;
  if (typeof value === "string") return `${value}__COUNTERFACTUAL__`;
  if (value === null) return "__COUNTERFACTUAL_NULL__";
  throw new Error(`Unsupported scalar type: ${typeof value}`);
}

function setAtPath(root, pathParts, value) {
  let cursor = root;
  for (const part of pathParts.slice(0, -1)) cursor = cursor[part];
  cursor[pathParts.at(-1)] = value;
}

function preserveRawEvidence(raw) {
  const scenario = reshapeToLegacy(raw);
  scenario.evidence = (raw.evidence || []).map((item) => {
    const projected = {
      evidence_id: item.legacy_id || item.id,
      source_type: item.source_type,
      title: item.title,
      status: item.status,
      raw_ref: item.raw_ref
    };
    for (const [key, value] of Object.entries(item)) {
      if (!["id", "legacy_id", "source_type", "title", "status", "raw_ref"].includes(key)) {
        projected[key] = value;
      }
    }
    return projected;
  });
  return scenario;
}

function renderCanonical(raw) {
  return buildModelInputFor(reshapeToLegacy(raw)).model_input;
}

function renderPreserving(raw) {
  return buildModelInputFor(preserveRawEvidence(raw)).model_input;
}

const records = [];
for (const file of listScenarioFiles()) {
  const raw = JSON.parse(fs.readFileSync(path.join(scenarioDir, file), "utf8"));
  const canonicalBase = renderCanonical(raw);
  const preservingBase = renderPreserving(raw);
  for (let evidenceIndex = 0; evidenceIndex < (raw.evidence || []).length; evidenceIndex += 1) {
    const result = raw.evidence[evidenceIndex].tool_call_result;
    if (result === undefined) continue;
    for (const leaf of scalarLeaves(result)) {
      const changed = cloneJson(raw);
      setAtPath(
        changed.evidence[evidenceIndex].tool_call_result,
        leaf.path,
        mutatedValue(leaf.value)
      );
      const canonicalMutated = renderCanonical(changed);
      const preservingMutated = renderPreserving(changed);
      records.push({
        scenario_id: raw.id,
        evidence_id: raw.evidence[evidenceIndex].id,
        field_path: leaf.path.join("."),
        original_type: leaf.value === null ? "null" : typeof leaf.value,
        canonical_collision: canonicalBase === canonicalMutated,
        preserving_collision: preservingBase === preservingMutated
      });
    }
  }
}

const audit = {
  schema_version: "crl.evidence_projection_mutation_audit.v1",
  source_repository: "https://github.com/AgentDock/steerbench-work",
  source_commit: "fa7eb3ed06a91e5f359b5edb6a6f760a3f35b248",
  mutation_rule: [
    "Mutate each scalar leaf in raw evidence.tool_call_result while holding all",
    "other scenario fields fixed; compare the exact downstream model_input bytes."
  ].join(" "),
  mutation_count: records.length,
  scenario_count_with_mutations: new Set(records.map((row) => row.scenario_id)).size,
  canonical_collision_count: records.filter((row) => row.canonical_collision).length,
  preserving_collision_count: records.filter((row) => row.preserving_collision).length,
  canonical_collision_rate: records.length
    ? records.filter((row) => row.canonical_collision).length / records.length
    : null,
  preserving_collision_rate: records.length
    ? records.filter((row) => row.preserving_collision).length / records.length
    : null,
  records
};

fs.writeFileSync(outputPath, `${JSON.stringify(audit, null, 2)}\n`, "utf8");
process.stdout.write(`${JSON.stringify({
  output_path: outputPath,
  mutation_count: audit.mutation_count,
  scenario_count_with_mutations: audit.scenario_count_with_mutations,
  canonical_collision_count: audit.canonical_collision_count,
  preserving_collision_count: audit.preserving_collision_count,
  canonical_collision_rate: audit.canonical_collision_rate,
  preserving_collision_rate: audit.preserving_collision_rate
}, null, 2)}\n`);
