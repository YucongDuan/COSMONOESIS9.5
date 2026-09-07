from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from dikwp_cosmonoesis95.claim_audit import audit_claims
from dikwp_cosmonoesis95.compiler import _DEFAULT_CLAIMS, compile_system
from dikwp_cosmonoesis95.consciousness import assess_bundled_examples, assess_candidate
from dikwp_cosmonoesis95.contact import evaluate_observation
from dikwp_cosmonoesis95.mappings import civilization_profiles, tradition_profiles, universal_centroid
from dikwp_cosmonoesis95.normalization import compare_concepts, compare_vectors, normalize_concept
from dikwp_cosmonoesis95.registries import load_registry, validate_registries
from dikwp_cosmonoesis95.utils import sha256_obj
from dikwp_cosmonoesis95.verify import verify_output_dir


class RegistryTests(unittest.TestCase):
    def test_registry_validation(self):
        report = validate_registries()
        self.assertTrue(report["valid"])
        self.assertEqual(report["counts"]["traditions"], 36)
        self.assertEqual(report["counts"]["concepts"], 144)
        self.assertEqual(report["counts"]["civilizations"], 13)

    def test_anchor_families_are_dikwp(self):
        anchors = load_registry("ontology")["anchors"]
        self.assertEqual({a["family"] for a in anchors}, set("DIKWP"))
        self.assertEqual(len(anchors), 32)

    def test_all_tradition_vectors_normalized(self):
        for tradition in tradition_profiles():
            self.assertAlmostEqual(sum(tradition["profile_vector"].values()), 1.0, places=8)
            self.assertEqual(tradition["normalization"]["out_of_space_residual"], 0.0)

    def test_all_concepts_inside_space(self):
        for tradition in tradition_profiles():
            for concept in tradition["concepts"]:
                self.assertAlmostEqual(sum(concept["vector"].values()), 1.0, places=8)
                self.assertEqual(concept["out_of_space_residual"], 0.0)
                self.assertEqual(concept["normalization_status"], "complete_in_dikwp_space")

    def test_civilization_profiles(self):
        items = civilization_profiles()
        self.assertEqual(len(items), 13)
        self.assertTrue(all(x["out_of_space_residual"] == 0.0 for x in items))
        self.assertTrue(all(abs(sum(x["profile_vector"].values()) - 1.0) < 1e-8 for x in items))

    def test_universal_centroid(self):
        result = universal_centroid()
        self.assertAlmostEqual(sum(result["vector"].values()), 1.0, places=8)
        self.assertEqual(result["out_of_space_residual"], 0.0)

    def test_principle_count(self):
        self.assertEqual(len(load_registry("principles")["principles"]), 20)

    def test_consciousness_model_counts(self):
        reg = load_registry("consciousness")
        self.assertEqual(len(reg["dimensions"]), 17)
        self.assertEqual(len(reg["models"]), 15)
        self.assertEqual(len(reg["cosmic_world_models"]), 7)


class NormalizationTests(unittest.TestCase):
    def test_exact_native_term(self):
        result = normalize_concept("śūnyatā", context="Madhyamaka")
        self.assertEqual(result["normalization_status"], "complete_in_dikwp_space")
        self.assertEqual(result["out_of_space_residual"], 0.0)
        self.assertGreater(len(result["candidate_source_mappings"]), 0)

    def test_unknown_term_is_provisional_in_space(self):
        result = normalize_concept("量子灵性奇点之风")
        self.assertAlmostEqual(sum(result["vector"].values()), 1.0, places=8)
        self.assertEqual(result["out_of_space_residual"], 0.0)
        self.assertIn(result["method"], {"provisional_in_space_extension", "keyword_in_space_projection", "registry_exact_or_contextual_alignment"})

    def test_ambiguous_qi_keeps_contextual_candidates(self):
        result = normalize_concept("气", context="道教修炼与身体经验")
        self.assertGreaterEqual(len(result["candidate_source_mappings"]), 1)
        self.assertFalse(result["historical_identity_claim"])

    def test_compare_is_not_equivalence(self):
        result = compare_concepts("Brahman", "God", context_a="Advaita", context_b="Christianity")
        self.assertFalse(result["comparison"]["equivalence_claim"])
        self.assertTrue(result["comparison"]["difference_is_inside_dikwp_space"])

    def test_compare_symmetry(self):
        a = normalize_concept("道")["vector"]
        b = normalize_concept("Asha")["vector"]
        ab = compare_vectors(a, b)
        ba = compare_vectors(b, a)
        self.assertAlmostEqual(ab["cosine_similarity"], ba["cosine_similarity"], places=8)
        self.assertAlmostEqual(ab["l1_distance"], ba["l1_distance"], places=8)

    def test_same_vector_similarity(self):
        a = normalize_concept("ubuntu")["vector"]
        self.assertAlmostEqual(compare_vectors(a, a)["cosine_similarity"], 1.0, places=8)


class ClaimAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = audit_claims(_DEFAULT_CLAIMS)

    def test_all_registered_rules_exercised(self):
        self.assertEqual(self.audit["matched_rule_count"], 20)
        self.assertEqual(self.audit["unmatched_rule_count"], 0)

    def test_all_default_claims_flagged(self):
        self.assertEqual(self.audit["claim_count"], self.audit["claims_with_registered_risks"])

    def test_threshold_flagged(self):
        item = next(x for x in self.audit["audited_claims"] if x["claim_id"] == "viral-001")
        ids = {f["rule_id"] for f in item["findings"]}
        self.assertIn("R02_FABRICATED_THRESHOLD", ids)
        self.assertIn("R01_SOURCE_MISATTRIBUTION", ids)

    def test_glueball_scope_flagged_critical(self):
        item = next(x for x in self.audit["audited_claims"] if x["claim_id"] == "viral-010")
        self.assertEqual(item["highest_severity"], "critical")
        self.assertIn("R11_GLUEBALL_SCOPE_INFLATION", {f["rule_id"] for f in item["findings"]})

    def test_negative_thought_tumor_flagged_critical(self):
        item = next(x for x in self.audit["audited_claims"] if x["claim_id"] == "viral-013")
        self.assertEqual(item["highest_severity"], "critical")
        self.assertIsNotNone(item["medical_safety_notice_cn"])

    def test_no_match_is_not_verification(self):
        result = audit_claims(["这是一条非常具体但尚未被规则库覆盖的新主张。"])
        self.assertEqual(result["audited_claims"][0]["audit_status"], "no_registered_rule_match_not_verified")


class ConsciousnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.examples = {x["candidate_id"]: x for x in assess_bundled_examples()}

    def test_no_binary_certificate(self):
        self.assertTrue(all(x["binary_consciousness_certificate"] is None for x in self.examples.values()))

    def test_internet_size_warning(self):
        self.assertTrue(self.examples["internet"]["size_only_warning"])
        self.assertEqual(self.examples["internet"]["evidence_level"], "insufficient_evidence")

    def test_star_has_no_value_purpose_evidence(self):
        item = self.examples["star"]
        self.assertLess(item["family_means"]["W"], 0.05)
        self.assertLess(item["family_means"]["P"], 0.10)

    def test_future_agent_still_not_certificate(self):
        item = self.examples["future_embodied_agent"]
        self.assertIsNone(item["binary_consciousness_certificate"])
        self.assertGreater(len(item["model_results"]), 5)

    def test_unknown_dimension_rejected(self):
        with self.assertRaises(ValueError):
            assess_candidate({"id":"bad", "scores":{"C.UNKNOWN":1.0}})

    def test_scores_clamped(self):
        result = assess_candidate({"id":"clamp", "scores":{"C.D1_EVENT_REGISTRATION":5,"C.W1_VALENCE":-2}})
        self.assertEqual(result["scores"]["C.D1_EVENT_REGISTRATION"], 1.0)
        self.assertEqual(result["scores"]["C.W1_VALENCE"], 0.0)


class ContactTests(unittest.TestCase):
    def test_low_evidence_stays_early(self):
        result = evaluate_observation({"features": {}})
        self.assertEqual(result["current_stage"], "D0_acquisition_incomplete")
        self.assertFalse(result["transmission_authorized"])

    def test_interference_stage(self):
        result = evaluate_observation({"features": {"instrument_calibrated":1,"repeated_over_time":1,"independent_observatories":1,"known_interference_excluded":0.2}})
        self.assertEqual(result["current_stage"], "I1_interference_exclusion")

    def test_high_signal_only_candidate(self):
        result = evaluate_observation({"features": {k:1 for k in [
            "instrument_calibrated","repeated_over_time","independent_observatories","known_interference_excluded",
            "natural_models_compared","structured_modulation","information_content_above_baseline",
            "causal_intervention_response","semantic_challenge_response","energy_budget_coherent"]}})
        self.assertEqual(result["current_stage"], "P5_semantic_handshake_candidate")
        self.assertFalse(result["transmission_authorized"])
        self.assertEqual(result["automatic_external_action_authority"], 0)


class CompilationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temp.name) / "compiled"
        cls.bundle = compile_system(cls.output)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_compilation_contract(self):
        contract = self.bundle["semantic_normalization_contract"]
        self.assertTrue(contract["all_concepts_inside_dikwp"])
        self.assertFalse(contract["permanent_untranslatable_outside_zone"])
        self.assertEqual(contract["out_of_space_residual"], 0.0)

    def test_output_verify(self):
        result = verify_output_dir(self.output)
        self.assertTrue(result["valid"], result["errors"])

    def test_manifest(self):
        manifest = json.loads((self.output / "MANIFEST.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(manifest["file_count"], 20)

    def test_dashboard_offline(self):
        text = (self.output / "dashboard.html").read_text(encoding="utf-8").lower()
        self.assertNotIn("<script src=", text)
        self.assertIn("automatic external action authority 0", text)

    def test_report_is_substantive(self):
        report = (self.output / "FULL_SYSTEM_REPORT_CN.md").read_text(encoding="utf-8")
        self.assertGreater(len(report), 50000)
        self.assertIn("在 DIKWP 语义空间归一", report)

    def test_bundle_digest_present(self):
        self.assertEqual(len(self.bundle["bundle_digest"]), 64)
        self.assertEqual(self.bundle["automatic_external_action_authority"], 0)

    def test_bundle_digest_is_time_independent(self):
        core = dict(self.bundle)
        expected = core.pop("bundle_digest")
        core.pop("generated_at", None)
        self.assertEqual(sha256_obj(core), expected)
        self.assertEqual(
            self.bundle["bundle_digest_policy"]["excluded_top_level_fields"],
            ["generated_at", "bundle_digest"],
        )


if __name__ == "__main__":
    unittest.main()
