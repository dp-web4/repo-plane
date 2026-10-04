"""Negative controls prevent a scaffold from looking like provider evidence.

SPDX-License-Identifier: AGPL-3.0-or-later
"""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_bootstrap import load, validate


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
        self.assertEqual(result["unmeasured_bypass_cells"], 161)

    def test_bound_matrix_claim_is_accepted_without_certifying_it(self):
        cell = self.bundle["matrix"]["operations"][0]["assessments"]["rest_api"]
        cell.update(status="intercepted", evidence=self.evidence())
        result = validate(self.bundle)
        self.assertEqual(result["unmeasured_bypass_cells"], 160)
        self.assertEqual(result["provider_conformance"], "not_evaluated")

    def test_bound_scenario_result_is_accepted(self):
        self.bundle["scenarios"]["scenarios"][0].update(
            status="passed", evidence=self.evidence())
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
                    self.bundle["scenarios"]["scenarios"][0].update(
                        status="passed", evidence=evidence)
                    with self.assertRaises(ValueError):
                        validate(self.bundle)

    def test_unbound_item_cannot_hide_behind_bound_evidence(self):
        self.bundle["scenarios"]["scenarios"][0].update(
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
                self.bundle["scenarios"]["scenarios"][0].update(
                    status="passed", evidence=evidence)
                with self.assertRaises(ValueError):
                    validate(self.bundle)

    def test_gate_control_mutations_cannot_be_omitted(self):
        for operation in ("branch_protection_change", "webhook_configuration",
                          "server_hook_configuration", "deploy_key_change",
                          "repository_transfer", "repository_rename", "repository_archive"):
            with self.subTest(operation=operation):
                bundle = copy.deepcopy(self.bundle)
                bundle["matrix"]["operations"] = [row for row in bundle["matrix"]["operations"]
                                                   if row["operation"] != operation]
                with self.assertRaises(ValueError):
                    validate(bundle)

    def test_operator_route_cannot_be_omitted(self):
        self.bundle["matrix"]["routes"].remove("operator_host")
        with self.assertRaises(ValueError):
            validate(self.bundle)

    def test_pre_action_seam_requires_evidence(self):
        seam = self.bundle["matrix"]["operations"][0]["pre_action_seam"]
        seam["status"] = "available"
        with self.assertRaises(ValueError):
            validate(self.bundle)
        seam["evidence"] = self.evidence()
        validate(self.bundle)

    def test_claimed_provider_support_is_rejected(self):
        self.bundle["github"]["supported_operations"] = ["proposal.merge"]
        with self.assertRaises(ValueError):
            validate(self.bundle)

    def test_unearned_scenario_pass_is_rejected(self):
        self.bundle["scenarios"]["scenarios"][0]["status"] = "passed"
        with self.assertRaises(ValueError):
            validate(self.bundle)

    def test_missing_native_route_is_rejected(self):
        del self.bundle["matrix"]["operations"][0]["assessments"]["git_ssh"]
        with self.assertRaises(ValueError):
            validate(self.bundle)

    def test_unearned_interception_claim_is_rejected(self):
        self.bundle["matrix"]["operations"][0]["assessments"]["rest_api"]["status"] = "intercepted"
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
