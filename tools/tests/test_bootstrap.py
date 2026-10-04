"""Negative controls prevent a scaffold from looking like provider evidence.

SPDX-License-Identifier: AGPL-3.0-or-later
"""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_bootstrap import PROVIDERS, ROUTE_STATUSES, SEAM_STATUSES, SCENARIO_STATUSES, load, validate


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.bundle = copy.deepcopy(load())

    def evidence(self, provider="gitea"):
        # Synthetic bindings exercise the validator; they are not run evidence.
        return [{"provider": provider, "provider_version": "test-version",
                 "adapter_revision": "test-revision", "run_id": "unit-test-only",
                 "reference": "fixture://synthetic-observation"}]

    def test_scaffold_is_valid_but_conformance_is_not_evaluated(self):
        result = validate(self.bundle)
        self.assertEqual(result["provider_conformance"], "not_evaluated")
        self.assertEqual(result["unmeasured_bypass_cells"], 414)
        self.assertEqual(result["unmeasured_bypass_cells_by_provider"],
                         {"github": 207, "gitea": 207})

    def test_bound_matrix_claim_is_accepted_without_certifying_it(self):
        cell = self.bundle["gitea_matrix"]["operations"][0]["assessments"]["rest_api"]
        cell.update(status="blocked", evidence=self.evidence())
        result = validate(self.bundle)
        self.assertEqual(result["unmeasured_bypass_cells"], 413)
        self.assertEqual(result["provider_conformance"], "not_evaluated")

    def test_bound_scenario_result_is_accepted(self):
        self.bundle["scenarios"]["scenarios"][0]["assessments"]["gitea"].update(
            status="passed", evidence=self.evidence())
        validate(self.bundle)

    def test_provider_results_are_independent(self):
        for provider, status in (("github", "blocked"), ("gitea", "bypassable")):
            self.bundle[f"{provider}_matrix"]["operations"][0]["assessments"]["git_ssh"].update(
                status=status, evidence=self.evidence(provider))
            result = validate(self.bundle)
            self.assertEqual(result["unmeasured_bypass_cells_by_provider"][provider], 206)
            if provider == "github":
                self.assertEqual(result["unmeasured_bypass_cells_by_provider"]["gitea"], 207)
        self.assertEqual(result["unmeasured_bypass_cells"], 412)
        case = self.bundle["scenarios"]["scenarios"][0]["assessments"]
        case["github"].update(status="passed", evidence=self.evidence("github"))
        self.assertEqual(case["gitea"]["status"], "not_run")
        case["gitea"].update(status="failed", evidence=self.evidence("gitea"))
        validate(self.bundle)

    def test_wrong_provider_is_rejected_for_every_assessment(self):
        for provider in PROVIDERS:
            row = self.bundle[f"{provider}_matrix"]["operations"][0]
            scenario = self.bundle["scenarios"]["scenarios"][0]["assessments"][provider]
            for assessment, status in ((row["assessments"]["git_ssh"], "blocked"),
                                       (row["pre_action_seam"], "present"),
                                       (scenario, "passed")):
                with self.subTest(provider=provider, status=status):
                    previous = copy.deepcopy(assessment)
                    wrong = "github" if provider == "gitea" else "gitea"
                    evidence = self.evidence(wrong)
                    evidence[0].update(route="git_ssh", scope="synthetic push fixture")
                    assessment.update(status=status, evidence=evidence)
                    with self.assertRaisesRegex(ValueError, "evidence provider mismatch"):
                        validate(self.bundle)
                    assessment.update(previous)

    def test_provider_identity_and_inventory_cannot_be_changed(self):
        for provider in PROVIDERS:
            with self.subTest(provider=provider):
                bundle = copy.deepcopy(self.bundle)
                bundle[f"{provider}_matrix"]["provider"] = "other"
                with self.assertRaises(ValueError):
                    validate(bundle)
                bundle = copy.deepcopy(self.bundle)
                del bundle["scenarios"]["scenarios"][0]["assessments"][provider]
                with self.assertRaises(ValueError):
                    validate(bundle)
                bundle = copy.deepcopy(self.bundle)
                bundle[provider]["direct_path_bypasses"]["matrix"] = "../other/bypass-matrix.json"
                with self.assertRaises(ValueError):
                    validate(bundle)

    def test_closed_assessment_vocabularies(self):
        row = self.bundle["gitea_matrix"]["operations"][0]
        scenario = self.bundle["scenarios"]["scenarios"][0]["assessments"]["gitea"]
        for assessment, allowed in ((row["assessments"]["rest_api"], ROUTE_STATUSES),
                                    (row["pre_action_seam"], SEAM_STATUSES),
                                    (scenario, SCENARIO_STATUSES)):
            previous = copy.deepcopy(assessment)
            evidence = self.evidence()
            evidence[0].update(route="rest_api", scope="synthetic repository fixture")
            for status in sorted(allowed):
                assessment.update(status=status, evidence=evidence)
                validate(self.bundle)
            for status in ("unmeasred", "available", "intercepted", "", None, 42):
                with self.subTest(status=status, allowed=allowed):
                    assessment.update(status=status, evidence=evidence)
                    with self.assertRaises(ValueError):
                        validate(self.bundle)
            assessment.update(previous)

    def test_operator_paths_are_separate_required_cells(self):
        for provider in PROVIDERS:
            for route in ("operator_cli", "operator_storage", "operator_db"):
                with self.subTest(provider=provider, route=route):
                    bundle = copy.deepcopy(self.bundle)
                    matrix = bundle[f"{provider}_matrix"]
                    row = next(r for r in matrix["operations"]
                               if r["operation"] == "branch_protection_change")
                    row["assessments"][route].update(status="blocked", evidence=self.evidence(provider))
                    result = validate(bundle)
                    self.assertEqual(result["unmeasured_bypass_cells_by_provider"][provider], 206)
                    del row["assessments"][route]
                    with self.assertRaises(ValueError):
                        validate(bundle)
                    row["assessments"][route] = {"status": "unmeasured", "evidence": []}
                    matrix["routes"].remove(route)
                    with self.assertRaises(ValueError):
                        validate(bundle)

    def test_seam_evidence_requires_known_route_and_nonempty_scope(self):
        seam = self.bundle["gitea_matrix"]["operations"][0]["pre_action_seam"]
        for field, invalids in (("route", (None, "", "operator_host", "unknown", 42)),
                                ("scope", (None, "", "   ", 42))):
            for invalid in invalids:
                with self.subTest(field=field, invalid=invalid):
                    evidence = self.evidence()
                    evidence[0].update(route="rest_api", scope="synthetic push fixture")
                    evidence[0][field] = invalid
                    seam.update(status="present", evidence=evidence)
                    with self.assertRaises(ValueError):
                        validate(self.bundle)
            del evidence[0][field]
            with self.assertRaises(ValueError):
                validate(self.bundle)

    def test_bound_provider_support_is_accepted(self):
        self.bundle["github"].update(implementation_status="implemented",
                                      supported_operations=["proposal.merge"],
                                      offline_support="unsupported",
                                      evidence=self.evidence("github"))
        validate(self.bundle)

    def test_each_evidence_binding_is_required(self):
        for field in self.evidence()[0]:
            for invalid in (None, "", "   ", 42):
                with self.subTest(field=field, invalid=invalid):
                    evidence = self.evidence()
                    evidence[0][field] = invalid
                    self.bundle["scenarios"]["scenarios"][0]["assessments"]["gitea"].update(
                        status="passed", evidence=evidence)
                    with self.assertRaises(ValueError):
                        validate(self.bundle)

    def test_unbound_item_cannot_hide_behind_bound_evidence(self):
        self.bundle["scenarios"]["scenarios"][0]["assessments"]["gitea"].update(
            status="passed", evidence=self.evidence() + [{}])
        with self.assertRaises(ValueError):
            validate(self.bundle)

    def test_wrong_provider_evidence_is_rejected(self):
        self.bundle["github"].update(offline_support="verified", evidence=self.evidence())
        with self.assertRaises(ValueError):
            validate(self.bundle)

    def test_evidence_shapes_are_checked(self):
        for evidence in ("claim", {"provider": "gitea"}, ["claim"]):
            with self.subTest(evidence=evidence):
                self.bundle["scenarios"]["scenarios"][0]["assessments"]["gitea"].update(
                    status="passed", evidence=evidence)
                with self.assertRaises(ValueError):
                    validate(self.bundle)

    def test_gate_control_mutations_cannot_be_omitted(self):
        for operation in ("branch_protection_change", "webhook_configuration",
                          "server_hook_configuration", "deploy_key_change",
                          "repository_transfer", "repository_rename", "repository_archive"):
            with self.subTest(operation=operation):
                bundle = copy.deepcopy(self.bundle)
                bundle["gitea_matrix"]["operations"] = [row for row in bundle["gitea_matrix"]["operations"]
                                                   if row["operation"] != operation]
                with self.assertRaises(ValueError):
                    validate(bundle)

    def test_operator_route_cannot_be_omitted(self):
        self.bundle["gitea_matrix"]["routes"].remove("operator_cli")
        with self.assertRaises(ValueError):
            validate(self.bundle)

    def test_pre_action_seam_requires_evidence(self):
        seam = self.bundle["gitea_matrix"]["operations"][0]["pre_action_seam"]
        seam["status"] = "present"
        with self.assertRaises(ValueError):
            validate(self.bundle)
        seam["evidence"] = self.evidence()
        seam["evidence"][0].update(route="rest_api", scope="synthetic repository push hook")
        validate(self.bundle)

    def test_claimed_provider_support_is_rejected(self):
        self.bundle["github"]["supported_operations"] = ["proposal.merge"]
        with self.assertRaises(ValueError):
            validate(self.bundle)

    def test_unearned_scenario_pass_is_rejected(self):
        self.bundle["scenarios"]["scenarios"][0]["assessments"]["gitea"]["status"] = "passed"
        with self.assertRaises(ValueError):
            validate(self.bundle)

    def test_missing_native_route_is_rejected(self):
        del self.bundle["gitea_matrix"]["operations"][0]["assessments"]["git_ssh"]
        with self.assertRaises(ValueError):
            validate(self.bundle)

    def test_unearned_interception_claim_is_rejected(self):
        self.bundle["gitea_matrix"]["operations"][0]["assessments"]["rest_api"]["status"] = "blocked"
        with self.assertRaises(ValueError):
            validate(self.bundle)

    def test_duplicate_scenario_is_rejected(self):
        self.bundle["scenarios"]["scenarios"][1]["id"] = "C1"
        with self.assertRaises(ValueError):
            validate(self.bundle)

    def test_unadopted_import_is_rejected(self):
        self.bundle["sources"]["import_status"] = "imported"
        with self.assertRaises(ValueError):
            validate(self.bundle)

    def test_unknown_provider_guarantee_must_stay_unknown(self):
        self.bundle["gitea"]["offline_support"] = "verified"
        with self.assertRaises(ValueError):
            validate(self.bundle)

    def test_template_is_not_a_run(self):
        self.bundle["template"]["run_id"] = "invented-run"
        with self.assertRaises(ValueError):
            validate(self.bundle)

    def test_unplanned_operation_is_rejected(self):
        self.bundle["github"]["planned_operations"].remove("proposal.merge")
        with self.assertRaises(ValueError):
            validate(self.bundle)


if __name__ == "__main__":
    unittest.main()
