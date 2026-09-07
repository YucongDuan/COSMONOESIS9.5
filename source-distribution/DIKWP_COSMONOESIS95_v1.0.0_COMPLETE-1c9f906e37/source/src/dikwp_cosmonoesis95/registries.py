from __future__ import annotations

from functools import lru_cache
from typing import Any

from .utils import load_bundled_json

REGISTRY_FILES = {
    "ontology": "dikwp_ontology.json",
    "traditions": "tradition_registry.json",
    "civilizations": "civilization_registry.json",
    "consciousness": "consciousness_models.json",
    "claim_rules": "claim_rules.json",
    "evidence": "evidence_registry.json",
    "principles": "cosmic_principles.json",
}


@lru_cache(maxsize=None)
def load_registry(name: str) -> dict[str, Any]:
    if name not in REGISTRY_FILES:
        raise KeyError(f"Unknown registry: {name}")
    obj = load_bundled_json(REGISTRY_FILES[name])
    if not isinstance(obj, dict):
        raise ValueError(f"Registry {name} must be a JSON object")
    return obj


def load_all_registries() -> dict[str, dict[str, Any]]:
    return {name: load_registry(name) for name in REGISTRY_FILES}


def ontology_anchor_map() -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in load_registry("ontology")["anchors"]}


def tradition_map() -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in load_registry("traditions")["traditions"]}


def source_map() -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in load_registry("evidence")["sources"]}


def consciousness_dimension_map() -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in load_registry("consciousness")["dimensions"]}


def validate_registries() -> dict[str, Any]:
    registries = load_all_registries()
    ontology = registries["ontology"]
    anchors = {item["id"] for item in ontology["anchors"]}
    if not anchors or any(anchor[0] not in "DIKWP" for anchor in anchors):
        raise ValueError("Ontology contains an invalid DIKWP anchor")

    errors: list[str] = []
    concept_count = 0
    for tradition in registries["traditions"]["traditions"]:
        if tradition.get("normalization", {}).get("out_of_space_residual") != 0.0:
            errors.append(f"{tradition['id']}: out-of-space residual must be zero")
        vector = tradition.get("profile_vector", {})
        if set(vector) - anchors:
            errors.append(f"{tradition['id']}: profile uses unknown coordinates")
        if abs(sum(vector.values()) - 1.0) > 1e-8:
            errors.append(f"{tradition['id']}: profile vector is not normalized")
        for concept in tradition.get("concepts", []):
            concept_count += 1
            cv = concept.get("vector", {})
            if set(cv) - anchors:
                errors.append(f"{tradition['id']}/{concept.get('term')}: unknown coordinate")
            if abs(sum(cv.values()) - 1.0) > 1e-8:
                errors.append(f"{tradition['id']}/{concept.get('term')}: vector is not normalized")
            if concept.get("out_of_space_residual") != 0.0:
                errors.append(f"{tradition['id']}/{concept.get('term')}: residual must be zero")

    tradition_ids = {item["id"] for item in registries["traditions"]["traditions"]}
    for civ in registries["civilizations"]["civilizations"]:
        missing = set(civ.get("member_traditions", [])) - tradition_ids
        if missing:
            errors.append(f"{civ['id']}: missing traditions {sorted(missing)}")

    dimensions = {item["id"] for item in registries["consciousness"]["dimensions"]}
    for model in registries["consciousness"]["models"]:
        unknown = (set(model.get("required", [])) | set(model.get("supportive", []))) - dimensions
        if unknown:
            errors.append(f"{model['id']}: unknown dimensions {sorted(unknown)}")
    for example in registries["consciousness"].get("illustrative_candidates", []):
        unknown = set(example.get("scores", {})) - dimensions
        if unknown:
            errors.append(f"{example['id']}: unknown dimensions {sorted(unknown)}")

    source_ids = {item["id"] for item in registries["evidence"]["sources"]}
    for rule in registries["claim_rules"]["rules"]:
        missing = set(rule.get("source_refs", [])) - source_ids
        if missing:
            errors.append(f"{rule['id']}: missing source refs {sorted(missing)}")
    for tradition in registries["traditions"]["traditions"]:
        missing = set(tradition.get("source_refs", [])) - source_ids
        if missing:
            errors.append(f"{tradition['id']}: missing source refs {sorted(missing)}")

    result = {
        "valid": not errors,
        "errors": errors,
        "counts": {
            "anchors": len(anchors),
            "traditions": len(tradition_ids),
            "concepts": concept_count,
            "civilizations": len(registries["civilizations"]["civilizations"]),
            "consciousness_dimensions": len(dimensions),
            "consciousness_models": len(registries["consciousness"]["models"]),
            "cosmic_models": len(registries["consciousness"]["cosmic_world_models"]),
            "claim_rules": len(registries["claim_rules"]["rules"]),
            "sources": len(source_ids),
            "principles": len(registries["principles"]["principles"]),
        },
        "automatic_external_action_authority": 0,
    }
    if errors:
        raise ValueError("; ".join(errors[:10]))
    return result
