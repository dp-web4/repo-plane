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

    def test_scaffold_is_valid_but_no_provider_test_ran(self):
        result = validate(self.bundle)
        self.assertEqual(result["provider_conformance"], "not_run")
        self.assertEqual(result["unmeasured_bypass_cells"], 96)

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
