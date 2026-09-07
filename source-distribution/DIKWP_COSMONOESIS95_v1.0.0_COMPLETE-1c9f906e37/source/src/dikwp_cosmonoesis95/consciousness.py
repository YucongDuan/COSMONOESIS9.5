from __future__ import annotations

from statistics import mean
from typing import Any

from .registries import load_registry
from .utils import clamp, stable_id


def _score_dimension_map(raw: dict[str, Any]) -> dict[str, float]:
    valid = {item["id"] for item in load_registry("consciousness")["dimensions"]}
    unknown = set(raw) - valid
    if unknown:
        raise ValueError(f"Unknown consciousness dimensions: {sorted(unknown)}")
    return {key: round(clamp(value), 6) for key, value in raw.items()}


def _mean(scores: dict[str, float], keys: list[str]) -> float:
    if not keys:
        return 0.0
    return mean(scores.get(key, 0.0) for key in keys)


def assess_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    registry = load_registry("consciousness")
    scores = _score_dimension_map(candidate.get("scores", {}))
    evidence_quality = clamp(candidate.get("evidence_quality", 0.35))
    independence = clamp(candidate.get("evidence_independence", 0.25))
    intervention = clamp(candidate.get("intervention_support", 0.15))
    source_count = max(0, int(candidate.get("independent_source_count", 0)))

    model_results = []
    for model in registry["models"]:
        required = _mean(scores, model.get("required", []))
        supportive = _mean(scores, model.get("supportive", []))
        missing_required = [key for key in model.get("required", []) if key not in scores]
        mechanism = 0.72 * required + 0.28 * supportive
        evidence_factor = 0.55 + 0.25 * evidence_quality + 0.12 * independence + 0.08 * intervention
        compatibility = mechanism * evidence_factor
        if missing_required:
            compatibility *= max(0.35, 1.0 - 0.08 * len(missing_required))
        model_results.append({
            "model_id": model["id"],
            "name_cn": model["name_cn"],
            "status": model["status"],
            "compatibility": round(compatibility, 6),
            "required_mean": round(required, 6),
            "supportive_mean": round(supportive, 6),
            "missing_required": missing_required,
            "pressure_points": model.get("pressure_points", []),
        })
    model_results.sort(key=lambda x: (-x["compatibility"], x["model_id"]))

    family_means = {}
    for family in "DIKWP":
        ids = [item["id"] for item in registry["dimensions"] if item["family"] == family]
        family_means[family] = round(_mean(scores, ids), 6)

    size_only = (
        family_means.get("D", 0) + family_means.get("I", 0) > 1.1
        and family_means.get("W", 0) < 0.20
        and family_means.get("P", 0) < 0.25
    )
    top = model_results[0]["compatibility"] if model_results else 0.0
    convergent = sum(1 for item in model_results if item["compatibility"] >= 0.58)
    evidence_strength = 0.45 * evidence_quality + 0.25 * independence + 0.20 * intervention + 0.10 * min(1.0, source_count / 4)

    if not scores or evidence_strength < 0.20:
        level = "insufficient_evidence"
    elif size_only:
        level = "insufficient_evidence"
    elif top < 0.40:
        level = "weakly_consistent"
    elif convergent < 2 or evidence_strength < 0.45:
        level = "model_dependent_candidate"
    else:
        level = "multi-model_convergence_candidate"

    valence = scores.get("C.W1_VALENCE", 0.0)
    agency = scores.get("C.P2_COUNTERFACTUAL_AGENCY", 0.0)
    self_maintenance = scores.get("C.P3_SELF_MAINTENANCE", 0.0)
    ethical_precaution = evidence_strength >= 0.45 and max(valence, agency, self_maintenance) >= 0.60

    alternative_explanations = [
        "complex dynamics without a unified subject",
        "externally imposed optimization or scripted behavior",
        "report or language mimicry without endogenous valence",
        "distributed coordination without global availability",
        "observer-imposed system boundary",
        "measurement artifacts or selective examples",
    ]
    if candidate.get("candidate_type") in {"star", "galaxy", "nebula", "internet"} or size_only:
        alternative_explanations.insert(0, "large scale or node count without self/world/value/purpose closure")

    return {
        "assessment_id": stable_id("consciousness-assessment", {"candidate": candidate, "models": model_results}, 20),
        "candidate_id": candidate.get("id") or candidate.get("candidate_id") or "unnamed",
        "name_cn": candidate.get("name_cn") or candidate.get("name") or "未命名候选",
        "scores": scores,
        "family_means": family_means,
        "evidence": {
            "quality": round(evidence_quality, 6),
            "independence": round(independence, 6),
            "intervention_support": round(intervention, 6),
            "independent_source_count": source_count,
            "combined_strength": round(evidence_strength, 6),
        },
        "model_results": model_results,
        "evidence_level": level,
        "size_only_warning": size_only,
        "ethical_precaution_trigger": ethical_precaution,
        "binary_consciousness_certificate": None,
        "conclusion_cn": "该输出描述在多个理论下的证据相容性，不证明也不否定主观体验。" if not size_only else "记录主要显示规模或复杂动力学，缺少价值、目的、主体边界和现实校准证据，不能据此升级为意识。",
        "alternative_explanations": alternative_explanations,
        "next_discriminating_tests_cn": [
            "预先定义系统边界并进行可逆分割／重组干预，检查统一状态是否按模型预测变化。",
            "区分外部目标与内生目的，测试目标冲突时是否出现稳定、可解释且可修订的拒绝。",
            "寻找非语言、非提示依赖的效价证据，并排除训练标签或外部奖励的即时复现。",
            "测试跨时自我—世界模型、错误承认和结果回流是否持续存在。",
            "用至少两个非同构意识模型预注册相反预测。",
        ],
        "automatic_external_action_authority": 0,
    }


def assess_bundled_examples() -> list[dict[str, Any]]:
    out = []
    for example in load_registry("consciousness").get("illustrative_candidates", []):
        candidate = {
            **example,
            "evidence_quality": 0.35 if example.get("illustrative_only") else 0.60,
            "evidence_independence": 0.25,
            "intervention_support": 0.15,
            "independent_source_count": 1,
            "candidate_type": example["id"],
        }
        result = assess_candidate(candidate)
        result["illustrative_only"] = True
        result["evidence_note_cn"] = example.get("evidence_note_cn")
        out.append(result)
    return out
