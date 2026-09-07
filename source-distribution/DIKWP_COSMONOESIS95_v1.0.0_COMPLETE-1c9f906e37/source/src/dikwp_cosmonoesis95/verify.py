from __future__ import annotations

from pathlib import Path
from typing import Any

from .registries import validate_registries
from .utils import load_json, sha256_bytes, sha256_obj


def verify_output_dir(output_dir: str | Path) -> dict[str, Any]:
    root = Path(output_dir)
    errors: list[str] = []
    required = [
        "cosmonoesis_bundle.json", "FULL_SYSTEM_REPORT_CN.md", "dashboard.html",
        "claim_audit.json", "tradition_mappings.json", "civilization_mappings.json",
        "consciousness_assessments.json", "contact_protocol_demo.json", "MANIFEST.json",
    ]
    for name in required:
        if not (root / name).is_file():
            errors.append(f"Missing required file: {name}")
    if errors:
        return {"valid": False, "errors": errors, "automatic_external_action_authority": 0}

    manifest = load_json(root / "MANIFEST.json")
    checked = 0
    for record in manifest.get("files", []):
        path = root / record["path"]
        if not path.is_file():
            errors.append(f"Manifest file missing: {record['path']}")
            continue
        digest = sha256_bytes(path.read_bytes())
        if digest != record["sha256"]:
            errors.append(f"Digest mismatch: {record['path']}")
        if path.stat().st_size != record["bytes"]:
            errors.append(f"Size mismatch: {record['path']}")
        checked += 1

    bundle = load_json(root / "cosmonoesis_bundle.json")
    expected = bundle.get("bundle_digest")
    core = dict(bundle)
    core.pop("bundle_digest", None)
    core.pop("generated_at", None)
    if sha256_obj(core) != expected:
        errors.append("Bundle digest mismatch")
    policy = bundle.get("bundle_digest_policy", {})
    if policy.get("excluded_top_level_fields") != ["generated_at", "bundle_digest"]:
        errors.append("Bundle digest policy is missing or unsupported")
    contract = bundle.get("semantic_normalization_contract", {})
    if not contract.get("all_concepts_inside_dikwp"):
        errors.append("Semantic closure contract is not enabled")
    if contract.get("permanent_untranslatable_outside_zone"):
        errors.append("Permanent outside-space residual zone must be disabled")
    if float(contract.get("out_of_space_residual", 1.0)) != 0.0:
        errors.append("Out-of-space residual must equal zero")
    if bundle.get("automatic_external_action_authority") != 0:
        errors.append("Automatic external action authority must be zero")
    if "http" in (root / "dashboard.html").read_text(encoding="utf-8").split("<script", 1)[-1].split("</script>", 1)[0]:
        # Payload may contain source URLs; this check only ensures there is no external script element.
        pass
    dashboard = (root / "dashboard.html").read_text(encoding="utf-8")
    if "<script src=" in dashboard.lower():
        errors.append("Dashboard contains an external script reference")

    try:
        registry_validation = validate_registries()
    except Exception as exc:
        registry_validation = {"valid": False, "error": str(exc)}
        errors.append(f"Bundled registry validation failed: {exc}")

    return {
        "valid": not errors,
        "errors": errors,
        "checked_manifest_files": checked,
        "manifest_file_count": manifest.get("file_count"),
        "compilation_id": bundle.get("compilation_id"),
        "bundle_digest": expected,
        "registry_validation": registry_validation,
        "automatic_external_action_authority": 0,
    }
