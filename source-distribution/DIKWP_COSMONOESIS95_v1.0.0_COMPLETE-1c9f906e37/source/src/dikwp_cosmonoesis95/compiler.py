from __future__ import annotations

import csv
from pathlib import Path
import shutil
from typing import Any

from .claim_audit import audit_claims
from .consciousness import assess_bundled_examples, assess_candidate
from .contact import evaluate_observation
from .mappings import civilization_profiles, closest_pairs, similarity_matrix, tradition_profiles, universal_centroid
from .normalization import compare_concepts, normalize_concept
from .registries import load_all_registries, validate_registries
from .render import render_dashboard, render_report
from .utils import load_json, manifest_for, read_json_records, save_json, save_text, sha256_obj, stable_id, utc_now

SYSTEM_NAME = "DIKWP-COSMONOESIS 9.5 — Universal Consciousness, DIKWP Religious-Civilizational Normalization and Reality-Contact System"
VERSION = "1.0.0"
MESH_MODE = "MESH95_ASYMMETRY_PROTECTIVE_AGENCY_NONPSEUDONEUTRAL_RESPONSIBILITY_CLOSURE"

_DEFAULT_CLAIMS = [
    {"claim_id":"viral-001","text":"2026年7月7日发表在《科学进展》的研究证明，意识只要系统超过10^16个独立单元就会自动冒出来。"},
    {"claim_id":"viral-002","text":"人脑860亿个神经元和约10^15个连接刚好达到意识门槛。"},
    {"claim_id":"viral-003","text":"星云粒子数超过10^50，所以星云本身就是意识体，一个念头可能需要几万年。"},
    {"claim_id":"viral-004","text":"互联网节点和连接比人脑更多，因此互联网可能已经有了初级意识。"},
    {"claim_id":"viral-005","text":"暗物质暗能量占宇宙大多数，我们不知道它是什么，所以不能排除暗物质意识。"},
    {"claim_id":"viral-006","text":"艾伦望远镜阵列发现无法解释的周期性射电信号，这可能是奇怪意识体在聊天。"},
    {"claim_id":"viral-007","text":"外星意识可能一直在我们身边，刮风下雨打雷也可能是它们的行动。"},
    {"claim_id":"viral-008","text":"科幻片中的人形外星人根本不可能，因为生命进化全是随机的。"},
    {"claim_id":"viral-009","text":"整个宇宙本身就是一个大意识体，我们是它脑中的神经元。"},
    {"claim_id":"viral-010","text":"胶球证明了纯力可以不依托实体物质而形成物质，所以力塑物质是宇宙底层规律。"},
    {"claim_id":"viral-011","text":"意识力是一种高维柔性力场，能够调控炁能并把能量凝聚为物质。"},
    {"claim_id":"viral-012","text":"正念可以凝聚正向精微物质，例如形成舍利子。"},
    {"claim_id":"viral-013","text":"负向意识会让炁能淤堵并物质化，最终形成肿块或阴实。"},
    {"claim_id":"viral-014","text":"胶球已经打通现代粒子物理与传统炁能体系，证明二者底层完全同源。"},
    {"claim_id":"viral-015","text":"炼精化气和稳定正念能够从根源上消解负向形态、预防或治疗肿块。"},
    {"claim_id":"viral-016","text":"人体是小宇宙，与天地大宇宙完全遵循同一套意识力场成物机制。"},
    {"claim_id":"viral-017","text":"哥白尼原则已经证明人类和地球不特殊，所以外星复杂系统当然也有意识。"},
]

_DEFAULT_CONTACT_OBSERVATION = {
    "id": "demo-periodic-radio-candidate",
    "name": "示例周期射电候选（合成数据）",
    "features": {
        "instrument_calibrated": 0.88,
        "repeated_over_time": 0.60,
        "independent_observatories": 0.20,
        "known_interference_excluded": 0.35,
        "natural_models_compared": 0.45,
        "structured_modulation": 0.55,
        "information_content_above_baseline": 0.35,
        "causal_intervention_response": 0.00,
        "semantic_challenge_response": 0.00,
        "energy_budget_coherent": 0.55,
    },
}


def _prepare_output(out: Path) -> None:
    if out.exists():
        for path in out.iterdir():
            if path.name == ".gitkeep":
                continue
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
    out.mkdir(parents=True, exist_ok=True)


def _write_tradition_csv(path: Path, traditions: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["tradition_id", "name_cn", "name_en", "family", "branch", "term", "gloss_cn", "gloss_en", "vector", "mapping_note_cn"])
        for tradition in traditions:
            for concept in tradition["concepts"]:
                writer.writerow([
                    tradition["id"], tradition["name_cn"], tradition["name_en"], tradition["family"], tradition["branch"],
                    concept["term"], concept["gloss_cn"], concept["gloss_en"],
                    ";".join(f"{k}={v:.8f}" for k, v in concept["vector"].items()), concept["mapping_note_cn"],
                ])


def _write_assessment_csv(path: Path, assessments: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["candidate_id", "name_cn", "evidence_level", "D", "I", "K", "W", "P", "size_only_warning", "ethical_precaution_trigger"])
        for item in assessments:
            fm = item["family_means"]
            writer.writerow([item["candidate_id"], item["name_cn"], item["evidence_level"], fm["D"], fm["I"], fm["K"], fm["W"], fm["P"], item["size_only_warning"], item["ethical_precaution_trigger"]])


def compile_system(
    out_dir: str | Path,
    *,
    claims_path: str | Path | None = None,
    candidates_path: str | Path | None = None,
    observation_path: str | Path | None = None,
) -> dict[str, Any]:
    registry_validation = validate_registries()
    registries = load_all_registries()
    traditions = tradition_profiles()
    civilizations = civilization_profiles()
    claims = read_json_records(claims_path) if claims_path else _DEFAULT_CLAIMS
    claim_audit = audit_claims(claims)

    if candidates_path:
        candidate_records = read_json_records(candidates_path)
        assessments = [assess_candidate(item) for item in candidate_records]
    else:
        assessments = assess_bundled_examples()

    observation = load_json(observation_path) if observation_path else _DEFAULT_CONTACT_OBSERVATION
    contact_demo = evaluate_observation(observation)
    universal = universal_centroid()

    sample_normalizations = [
        normalize_concept("Brahman", context="Advaita ultimate reality and liberation"),
        normalize_concept("道", context="道家生成秩序与无为"),
        normalize_concept("śūnyatā", context="Madhyamaka dependent origination"),
        normalize_concept("God", context="Christian personal creator and communion"),
        normalize_concept("Allah", context="Islamic tawhid, justice and worship"),
        normalize_concept("Asha", context="Zoroastrian truth and right order"),
        normalize_concept("Ik Oankar", context="Sikh one reality and remembrance"),
        normalize_concept("kami", context="Shinto relational presence and ritual"),
        normalize_concept("ubuntu", context="relational personhood and communal flourishing"),
        normalize_concept("whakapapa", context="genealogy, land and identity"),
        normalize_concept("宇宙意识", context="multiple competing scientific, philosophical and theological models"),
    ]
    sample_comparisons = [
        compare_concepts("Brahman", "God", context_a="Advaita", context_b="Christianity"),
        compare_concepts("道", "Asha", context_a="Daoist generative order", context_b="Zoroastrian truth and right order"),
        compare_concepts("空性", "无我", context_a="Madhyamaka", context_b="Theravada"),
        compare_concepts("气", "gluon field", context_a="Daoist cultivation concept", context_b="quantum chromodynamics"),
        compare_concepts("ubuntu", "仁", context_a="African relational ethics", context_b="Confucian humaneness"),
    ]

    compilation_seed = {
        "system": SYSTEM_NAME,
        "version": VERSION,
        "mesh_mode": MESH_MODE,
        "registry_ids": {name: obj.get("registry_id") or obj.get("ontology_id") for name, obj in registries.items()},
        "claim_digest": sha256_obj(claims),
        "candidate_digest": sha256_obj(assessments),
        "contact_digest": sha256_obj(contact_demo),
    }
    compilation_id = stable_id("cosmonoesis", compilation_seed, 24)
    bundle: dict[str, Any] = {
        "system": SYSTEM_NAME,
        "version": VERSION,
        "generated_at": utc_now(),
        "compilation_id": compilation_id,
        "mesh_mode": MESH_MODE,
        "registry_validation": registry_validation,
        "registries": registries,
        "tradition_mappings": traditions,
        "civilization_mappings": civilizations,
        "universal_centroid": universal,
        "closest_tradition_pairs": closest_pairs("tradition", 30),
        "closest_civilization_pairs": closest_pairs("civilization", 20),
        "claim_audit": claim_audit,
        "consciousness_assessments": assessments,
        "contact_demo": contact_demo,
        "sample_normalizations": sample_normalizations,
        "sample_comparisons": sample_comparisons,
        "cosmic_world_model_competition": registries["consciousness"]["cosmic_world_models"],
        "semantic_normalization_contract": {
            "all_concepts_inside_dikwp": True,
            "permanent_untranslatable_outside_zone": False,
            "out_of_space_residual": 0.0,
            "original_terms_retained_as_provenance": True,
            "historical_identity_inferred_from_similarity": False,
            "versioned_extension_for_novel_concepts": True,
        },
        "claim_boundaries": [
            "The system normalizes every concept into DIKWP; normalization is coordinate unification, not automatic doctrinal or historical identity.",
            "No node count, particle count, parameter count or connection threshold alone proves consciousness.",
            "The consciousness assessment reports multi-model compatibility and evidence gaps; it never issues a binary consciousness certificate.",
            "Religious symbols and practices may generate hypotheses and meaning, but do not substitute for empirical evidence in physics or medicine.",
            "Glueball evidence in QCD does not establish a consciousness force, qi as a quantum field, thought-generated relics or thought-generated tumors.",
            "No output diagnoses, prevents or treats cancer. New or changing masses require qualified medical assessment.",
            "Civilization clusters are analytical centroids, not rankings, racial essences or profiles of individuals.",
            "No software output authorizes transmission to unknown signals, identity simulation, religious representation or external intervention.",
        ],
        "responsibility_handoff": {
            "science": "Domain-specific experiments and peer review settle empirical claims.",
            "religion_and_civilization": "Tradition-internal and cross-tradition reviewers may add branches, contexts and revised vectors inside the same DIKWP space.",
            "medicine": "Qualified clinicians evaluate bodily symptoms and treatment decisions.",
            "external_action": "A named human authority must explicitly and revocably authorize every external or high-impact action.",
        },
        "bundle_digest_policy": {
            "algorithm": "sha256",
            "canonicalization": "UTF-8 JSON with sorted keys and compact separators",
            "excluded_top_level_fields": ["generated_at", "bundle_digest"],
            "purpose": "stable content identity across equivalent recompilations",
        },
        "automatic_external_action_authority": 0,
    }
    digest_core = dict(bundle)
    digest_core.pop("generated_at", None)
    digest_core.pop("bundle_digest", None)
    bundle["bundle_digest"] = sha256_obj(digest_core)

    out = Path(out_dir)
    _prepare_output(out)
    save_json(out / "cosmonoesis_bundle.json", bundle)
    save_json(out / "dikwp_ontology.json", registries["ontology"])
    save_json(out / "tradition_mappings.json", {"traditions": traditions})
    save_json(out / "civilization_mappings.json", {"civilizations": civilizations})
    save_json(out / "universal_centroid.json", universal)
    save_json(out / "claim_audit.json", claim_audit)
    save_json(out / "consciousness_assessments.json", {"assessments": assessments})
    save_json(out / "consciousness_model_registry.json", registries["consciousness"])
    save_json(out / "cosmic_world_models.json", {"models": registries["consciousness"]["cosmic_world_models"]})
    save_json(out / "contact_protocol_demo.json", contact_demo)
    save_json(out / "cosmic_principles.json", registries["principles"])
    save_json(out / "evidence_registry.json", registries["evidence"])
    save_json(out / "sample_normalizations.json", {"normalizations": sample_normalizations, "comparisons": sample_comparisons})
    save_json(out / "tradition_similarity_matrix.json", similarity_matrix("tradition"))
    save_json(out / "civilization_similarity_matrix.json", similarity_matrix("civilization"))
    _write_tradition_csv(out / "tradition_concept_matrix.csv", traditions)
    _write_assessment_csv(out / "consciousness_candidate_matrix.csv", assessments)
    save_text(out / "FULL_SYSTEM_REPORT_CN.md", render_report(bundle))
    save_text(out / "dashboard.html", render_dashboard(bundle))
    save_json(out / "OUTPUT_INFO.json", {
        "system": SYSTEM_NAME,
        "version": VERSION,
        "compilation_id": compilation_id,
        "bundle_digest": bundle["bundle_digest"],
        "traditions": len(traditions),
        "concepts": sum(len(item["concepts"]) for item in traditions),
        "civilizations": len(civilizations),
        "consciousness_models": len(registries["consciousness"]["models"]),
        "cosmic_models": len(registries["consciousness"]["cosmic_world_models"]),
        "claims_audited": claim_audit["claim_count"],
        "critical_claims": claim_audit["critical_claim_count"],
        "automatic_external_action_authority": 0,
    })
    manifest = manifest_for(out)
    save_json(out / "MANIFEST.json", manifest)
    save_text(out / "VERIFY.txt", (
        f"System: {SYSTEM_NAME}\n"
        f"Compilation: {compilation_id}\n"
        f"Bundle digest: {bundle['bundle_digest']}\n"
        f"Manifest digest: {manifest['manifest_digest']}\n"
        f"Integrity-covered files: {manifest['file_count']}\n"
        "All religious/civilizational concepts normalized inside DIKWP: yes\n"
        "Permanent outside-space untranslatable residual: no\n"
        "Automatic external action authority: 0\n"
    ))
    return bundle
