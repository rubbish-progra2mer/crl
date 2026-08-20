#!/usr/bin/env python3
"""从原始观察生成报告、签发授权记录，并以失败关闭方式接入。"""

from __future__ import annotations

import hashlib
import hmac
from dataclasses import replace
from typing import Mapping, MutableSet

from compiler import (
    auxiliary_claim_ref,
    count_claim_ref,
    relation_claim_ref,
    validate_plan,
    validate_witness,
)
from typed_model import (
    AdmissionBundle,
    AdmissionDecision,
    AdmissionRequest,
    AttestationRecord,
    ClaimRef,
    EffectContract,
    EvidenceBundle,
    ExecutionReport,
    IntegrityError,
    ProbeObservation,
    ProjectionPolicy,
    SchemaError,
    canonical_bytes,
    canonical_hash,
    without_report_hash,
    without_signature,
)


def _report_status(report: ExecutionReport, claims: tuple[ClaimRef, ...]) -> str:
    if (
        report.complete
        and not report.failed_claims
        and not report.nonidentifiable_claims
        and report.passed_claims == claims
    ):
        return "pass"
    return "fail"


def _canonical_observations(
    observations: tuple[ProbeObservation, ...],
) -> tuple[ProbeObservation, ...]:
    if tuple(sorted(observations, key=lambda item: item.probe_id)) != observations:
        raise SchemaError("原始观察必须按 probe_id 排序")
    probe_ids = tuple(item.probe_id for item in observations)
    if any(not probe_id for probe_id in probe_ids):
        raise SchemaError("原始观察的 probe_id 不能为空")
    if len(set(probe_ids)) != len(probe_ids):
        raise SchemaError("同一 probe_id 只能有一份原始观察")
    for observation in observations:
        for event in observation.events:
            if not all(
                isinstance(value, str)
                for value in (event.kind, event.target_token, event.payload_token)
            ):
                raise SchemaError("观察事件字段必须都是字符串")
            if not event.kind:
                raise SchemaError("观察事件类型不能为空")
    return observations


def evaluate_observations(
    contract: EffectContract,
    projection: ProjectionPolicy,
    plan,
    observations: tuple[ProbeObservation, ...],
) -> ExecutionReport:
    """只从经重编译验证的计划和原始观察派生完整报告。"""

    validate_plan(plan, contract, projection)
    observations = _canonical_observations(observations)
    by_probe = {item.probe_id: item for item in observations}
    expected_probe_ids = tuple(item.probe_id for item in plan.probes)
    observed_probe_ids = tuple(sorted(by_probe))
    complete = observed_probe_ids == expected_probe_ids
    diagnostics: list[str] = []
    if not complete:
        missing = sorted(set(expected_probe_ids) - set(observed_probe_ids))
        extra = sorted(set(observed_probe_ids) - set(expected_probe_ids))
        diagnostics.append(f"探针集合不完整：缺少={missing}，多余={extra}")

    passed: set[ClaimRef] = set()
    failed: set[ClaimRef] = set()
    count_claim = count_claim_ref(contract)
    auxiliary_claim = auxiliary_claim_ref(contract)

    count_ok = complete
    auxiliary_ok = complete
    primary_by_probe = {}
    for probe_id in expected_probe_ids:
        observation = by_probe.get(probe_id)
        if observation is None:
            count_ok = False
            auxiliary_ok = False
            continue
        primary = tuple(
            event for event in observation.events if event.kind == contract.primary_kind
        )
        primary_by_probe[probe_id] = primary
        if not (
            contract.count_policy.minimum
            <= len(primary)
            <= contract.count_policy.maximum
        ):
            count_ok = False
            diagnostics.append(f"探针 {probe_id} 的主事件数量越界：{len(primary)}")
        unexpected = sorted(
            {
                event.kind
                for event in observation.events
                if event.kind != contract.primary_kind
                and event.kind not in contract.allowed_auxiliary_kinds
            }
        )
        if unexpected:
            auxiliary_ok = False
            diagnostics.append(f"探针 {probe_id} 含未授权辅助事件：{unexpected}")

    (passed if count_ok else failed).add(count_claim)
    (passed if auxiliary_ok else failed).add(auxiliary_claim)

    for monitor in plan.monitors:
        monitor_ok = complete
        signature: list[str] = []
        for ref in monitor.refs:
            primary = primary_by_probe.get(ref.probe_id, ())
            if len(primary) != 1:
                monitor_ok = False
                break
            event = primary[0]
            token = event.target_token if ref.channel == "target" else event.payload_token
            if not token:
                monitor_ok = False
                diagnostics.append(
                    f"探针 {ref.probe_id} 的 {ref.channel} 观察令牌为空"
                )
                break
            signature.append(token)
        if monitor_ok:
            case_table = {case.observation_signature: case.result for case in monitor.cases}
            key = tuple(signature)
            if key not in case_table:
                monitor_ok = False
                diagnostics.append(f"监控器收到域外观察签名：{key}")
            else:
                monitor_ok = case_table[key]
        (passed if monitor_ok else failed).add(monitor.claim)

    nonidentifiable = tuple(sorted(item.claim for item in plan.nonidentifiable))
    report = ExecutionReport(
        complete=complete,
        passed_claims=tuple(sorted(passed)),
        failed_claims=tuple(sorted(failed)),
        nonidentifiable_claims=nonidentifiable,
        observation_hash=canonical_hash(observations),
        observed_probe_ids=observed_probe_ids,
        diagnostics=tuple(diagnostics),
        report_hash="",
    )
    partition = set(report.passed_claims) | set(report.failed_claims) | set(
        report.nonidentifiable_claims
    )
    if partition != set(plan.contract_claims):
        raise IntegrityError("执行报告没有对合同主张完整分类")
    if (
        set(report.passed_claims) & set(report.failed_claims)
        or set(report.passed_claims) & set(report.nonidentifiable_claims)
        or set(report.failed_claims) & set(report.nonidentifiable_claims)
    ):
        raise IntegrityError("执行报告的主张分类相互重叠")
    return replace(
        report, report_hash=canonical_hash(without_report_hash(report))
    )


def issue_attestation(
    bundle_without_record: EvidenceBundle,
    *,
    issuer_id: str,
    issuer_key: bytes,
    tool_id: str,
    tool_version: str,
    issued_at: int,
    expires_at: int,
    nonce: str,
) -> AttestationRecord:
    """用共享密钥原型签发完整、短时、不可重放的授权记录。"""

    if not issuer_id or not tool_id or not tool_version or not nonce:
        raise SchemaError("签发者、工具和 nonce 均不能为空")
    if len(issuer_key) < 16:
        raise SchemaError("HMAC 共享密钥至少需要 16 字节")
    if issued_at < 0 or expires_at <= issued_at:
        raise SchemaError("证明有效期非法")
    contract = bundle_without_record.contract
    projection = bundle_without_record.projection
    plan = bundle_without_record.plan
    observations = bundle_without_record.observations
    report = bundle_without_record.report
    expected_report = evaluate_observations(contract, projection, plan, observations)
    if report != expected_report:
        raise IntegrityError("待签发报告不是原始观察的规范重算结果")
    for witness in plan.nonidentifiable:
        matching = tuple(
            claim
            for claim in contract.relation_claims
            if relation_claim_ref(claim) == witness.claim
        )
        if len(matching) != 1:
            raise IntegrityError("不可识别见证不能唯一绑定合同主张")
        validate_witness(witness, matching[0], projection)
    record = AttestationRecord(
        issuer_id=issuer_id,
        tool_id=tool_id,
        tool_version=tool_version,
        issued_at=issued_at,
        expires_at=expires_at,
        nonce=nonce,
        contract_hash=canonical_hash(contract),
        projection_hash=canonical_hash(projection),
        plan_hash=plan.plan_hash,
        observation_hash=report.observation_hash,
        report_hash=report.report_hash,
        contract_claims=plan.contract_claims,
        passed_claims=report.passed_claims,
        failed_claims=report.failed_claims,
        nonidentifiable_claims=report.nonidentifiable_claims,
        status=_report_status(report, plan.contract_claims),
        signature="",
    )
    signature = hmac.new(
        issuer_key, canonical_bytes(without_signature(record)), hashlib.sha256
    ).hexdigest()
    return replace(record, signature=signature)


def _validate_required_claims(request: AdmissionRequest) -> None:
    if (
        request.schema_version != 1
        or not isinstance(request.tool_id, str)
        or not isinstance(request.tool_version, str)
        or not request.tool_id
        or not request.tool_version
        or not isinstance(request.contract_hash, str)
        or not isinstance(request.projection_hash, str)
        or not isinstance(request.plan_hash, str)
        or not request.contract_hash
        or not request.projection_hash
        or not request.plan_hash
    ):
        raise SchemaError("接入请求模式或工具标识非法")
    if not request.required_claims:
        raise SchemaError("接入请求必须显式声明至少一个所需主张")
    if request.required_claims != tuple(sorted(request.required_claims)):
        raise SchemaError("所需主张必须规范排序")
    if len(set(request.required_claims)) != len(request.required_claims):
        raise SchemaError("所需主张不能重复")


def verify_and_admit(
    bundle: AdmissionBundle,
    request: AdmissionRequest,
    *,
    trusted_issuers: Mapping[str, bytes],
    replay_cache: MutableSet[str],
    now: int,
) -> AdmissionDecision:
    """重算所有可派生内容；任一不一致、未知或重放均拒绝。"""

    try:
        _validate_required_claims(request)
        record = bundle.record
        scalar_text = (
            record.issuer_id,
            record.tool_id,
            record.tool_version,
            record.nonce,
            record.contract_hash,
            record.projection_hash,
            record.plan_hash,
            record.observation_hash,
            record.report_hash,
            record.status,
            record.signature_algorithm,
            record.signature,
        )
        if not all(isinstance(value, str) for value in scalar_text):
            raise SchemaError("证明文本字段类型非法")
        if (
            isinstance(record.issued_at, bool)
            or isinstance(record.expires_at, bool)
            or not isinstance(record.issued_at, int)
            or not isinstance(record.expires_at, int)
        ):
            raise SchemaError("证明时间字段类型非法")
        if record.schema_version != 1 or record.signature_algorithm != "hmac-sha256":
            raise IntegrityError("证明模式或签名算法不受支持")
        key = trusted_issuers.get(record.issuer_id)
        if key is None or len(key) < 16:
            raise IntegrityError("签发者不受信任")
        expected_signature = hmac.new(
            key, canonical_bytes(without_signature(record)), hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(record.signature, expected_signature):
            raise IntegrityError("证明签名无效")
        if record.issued_at > now or now > record.expires_at:
            raise IntegrityError("证明尚未生效或已经过期")
        if not record.nonce or record.nonce in replay_cache:
            raise IntegrityError("证明 nonce 为空或已被使用")
        if (record.tool_id, record.tool_version) != (
            request.tool_id,
            request.tool_version,
        ):
            raise IntegrityError("证明未绑定当前工具版本")
        if (
            record.contract_hash,
            record.projection_hash,
            record.plan_hash,
        ) != (
            request.contract_hash,
            request.projection_hash,
            request.plan_hash,
        ):
            raise IntegrityError("证明未绑定请求指定的合同、投影和计划")

        validate_plan(bundle.plan, bundle.contract, bundle.projection)
        expected_report = evaluate_observations(
            bundle.contract,
            bundle.projection,
            bundle.plan,
            bundle.observations,
        )
        if bundle.report != expected_report:
            raise IntegrityError("报告与原始观察的重算结果不同")
        expected_fields = {
            "contract_hash": canonical_hash(bundle.contract),
            "projection_hash": canonical_hash(bundle.projection),
            "plan_hash": bundle.plan.plan_hash,
            "observation_hash": expected_report.observation_hash,
            "report_hash": expected_report.report_hash,
            "contract_claims": bundle.plan.contract_claims,
            "passed_claims": expected_report.passed_claims,
            "failed_claims": expected_report.failed_claims,
            "nonidentifiable_claims": expected_report.nonidentifiable_claims,
            "status": _report_status(expected_report, bundle.plan.contract_claims),
        }
        for name, expected in expected_fields.items():
            if getattr(record, name) != expected:
                raise IntegrityError(f"证明字段 {name} 与规范派生值不同")
        if record.status != "pass":
            raise IntegrityError("证明没有覆盖并通过全部合同主张")
        if not set(request.required_claims).issubset(set(record.contract_claims)):
            raise IntegrityError("请求含合同之外的主张")
        if not set(request.required_claims).issubset(set(record.passed_claims)):
            raise IntegrityError("所需主张未全部通过")
        replay_cache.add(record.nonce)
        return AdmissionDecision(True, ("授权证明、计划和原始观察均已验证",))
    except (IntegrityError, SchemaError, KeyError, TypeError, ValueError) as error:
        return AdmissionDecision(False, (str(error),))
