from __future__ import annotations

import re
from typing import Any, Iterable

from .registries import load_registry, source_map
from .utils import normalize_text, stable_id

_SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3, "critical": 4}


def split_claims(text: str) -> list[str]:
    cleaned = normalize_text(text)
    if not cleaned:
        return []
    parts = re.split(r"(?<=[。！？!?；;])\s*|\n+", cleaned)
    return [p.strip() for p in parts if len(p.strip()) >= 6]


def classify_claim_type(text: str) -> str:
    value = text.lower()
    if any(token in value for token in ("应该", "必须", "值得", "正义", "伦理", "ought", "should", "must")):
        return "N"
    if any(token in value for token in ("可能", "假说", "或许", "could", "might", "hypothesis")):
        return "P"
    if any(token in value for token in ("模型", "形式", "定义", "framework", "model", "formal")):
        return "F"
    if any(token in value for token in ("历史", "传统", "古代", "history", "tradition")):
        return "H"
    return "E"


def _normalize_input(claims: Iterable[str | dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for index, item in enumerate(claims, start=1):
        if isinstance(item, str):
            text = normalize_text(item)
            record = {"claim_id": f"claim-{index:03d}", "text": text}
        else:
            record = dict(item)
            text = normalize_text(record.get("text") or record.get("claim") or record.get("content"))
            record["text"] = text
            record.setdefault("claim_id", stable_id("claim", {"index": index, "text": text}, 14))
        if text:
            record.setdefault("claim_type", classify_claim_type(text))
            out.append(record)
    return out


def audit_claims(claims: Iterable[str | dict[str, Any]]) -> dict[str, Any]:
    records = _normalize_input(claims)
    rules = load_registry("claim_rules")["rules"]
    sources = source_map()
    audited: list[dict[str, Any]] = []
    severity_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    category_counts: dict[str, int] = {}
    matched_rule_ids: set[str] = set()

    for record in records:
        text = record["text"]
        findings = []
        for rule in rules:
            patterns = rule.get("patterns", [])
            matched = [pattern for pattern in patterns if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)]
            if not matched:
                continue
            matched_rule_ids.add(rule["id"])
            severity = rule["severity"]
            severity_counts[severity] += 1
            category_counts[rule["category"]] = category_counts.get(rule["category"], 0) + 1
            findings.append({
                "rule_id": rule["id"],
                "category": rule["category"],
                "severity": severity,
                "matched_patterns": matched,
                "diagnosis_cn": rule["diagnosis_cn"],
                "correction_cn": rule["correction_cn"],
                "needed_evidence_cn": rule["needed_evidence_cn"],
                "sources": [sources[source_id] for source_id in rule.get("source_refs", []) if source_id in sources],
            })
        findings.sort(key=lambda x: (-_SEVERITY_RANK[x["severity"]], x["rule_id"]))
        highest = findings[0]["severity"] if findings else "none"
        medical = any(f["category"] in {"dangerous_medical_misinformation", "medical_treatment_overclaim", "mind_matter_medical_spiritual_claim"} for f in findings)
        audited.append({
            **record,
            "audit_status": "registered_risk_detected" if findings else "no_registered_rule_match_not_verified",
            "highest_severity": highest,
            "findings": findings,
            "safe_reformulation_cn": findings[0]["correction_cn"] if findings else "本系统未匹配到已登记的风险规则；这不等于该主张已经得到验证。",
            "medical_safety_notice_cn": "涉及肿块、癌症或身体异常时，应获得正规医疗评估；认知、正念或宗教实践不能替代诊断与治疗。" if medical else None,
            "automatic_external_action_authority": 0,
        })

    critical_claims = sum(1 for item in audited if item["highest_severity"] == "critical")
    return {
        "system": "DIKWP-COSMONOESIS95 claim audit",
        "claim_count": len(audited),
        "claims_with_registered_risks": sum(1 for item in audited if item["findings"]),
        "critical_claim_count": critical_claims,
        "finding_count": sum(len(item["findings"]) for item in audited),
        "severity_counts": severity_counts,
        "category_counts": dict(sorted(category_counts.items())),
        "matched_rule_count": len(matched_rule_ids),
        "unmatched_rule_count": len(rules) - len(matched_rule_ids),
        "claim_type_legend": {
            "E": "empirical/factual claim",
            "H": "historical/interpretive reconstruction",
            "F": "formal or constructed model",
            "P": "proposal/hypothesis requiring reality settlement",
            "N": "normative/metaphysical orientation",
        },
        "audited_claims": audited,
        "medical_boundary_cn": "系统不进行诊断。任何新出现、持续或变化的肿块，以及疑似癌症症状，都需要由合格医疗专业人员评估。",
        "automatic_external_action_authority": 0,
    }
