"""Validate bootstrap metadata only; never execute provider operations.

SPDX-License-Identifier: AGPL-3.0-or-later
"""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROVIDERS = ("github", "gitea")
ROUTES = {"web_ui", "rest_api", "git_http", "git_ssh", "internal_background", "workflow",
          "operator_cli", "operator_storage", "operator_db"}
ROUTE_STATUSES = {"unmeasured", "blocked", "bypassable", "partial", "not_applicable"}
SEAM_STATUSES = {"unmeasured", "present", "absent"}
SCENARIO_STATUSES = {"not_run", "passed", "failed", "partial", "unsupported"}
MUTATIONS = {
    "push", "force_push", "branch_create", "branch_delete", "tag_create", "tag_delete",
    "proposal_merge", "repository_create", "repository_delete", "visibility_change",
    "acl_team_change", "release_publish", "package_publish", "workflow_config",
    "workflow_execution", "mirror_configuration",
    "branch_protection_change", "webhook_configuration", "server_hook_configuration",
    "deploy_key_change", "repository_transfer", "repository_rename", "repository_archive",
}


def load(root=ROOT):
    paths = {
        "sources": "docs/SOURCES.json",
        "scenarios": "conformance/scenarios/core.json",
        "github_matrix": "providers/github/bypass-matrix.json",
        "gitea_matrix": "providers/gitea/bypass-matrix.json",
        "template": "conformance/fixtures/result-template.json",
        "github": "providers/github/capabilities.json",
        "gitea": "providers/gitea/capabilities.json",
    }
    return {key: json.loads((root / path).read_text()) for key, path in paths.items()}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_claim(status, evidence, *, unknown="unmeasured", provider, statuses=None, seam=False):
    """Check evidence bindings, not whether an observation proves a claim."""
    require(isinstance(status, str) and bool(status.strip()), "claim status must be non-empty")
    if statuses is not None:
        require(status in statuses, "unknown claim status")
    require(isinstance(evidence, list), "evidence must be a list")
    if status != unknown:
        require(bool(evidence), "measured claims need bound evidence")
    for item in evidence:
        require(isinstance(item, dict), "evidence must be an object")
        for field in ("provider", "provider_version", "adapter_revision", "run_id", "reference"):
            require(isinstance(item.get(field), str) and bool(item[field].strip()),
                    f"evidence must bind {field}")
        require(item["provider"] == provider, "evidence provider mismatch")
        if seam:
            require(isinstance(item.get("route"), str) and item["route"] in ROUTES,
                    "seam evidence must name a native route")
            require(isinstance(item.get("scope"), str) and bool(item["scope"].strip()),
                    "seam evidence must name its scope")


def validate(bundle):
    for name, item in bundle.items():
        require(item["schema_version"] == 1, f"{name}: unknown schema version")
    sources = bundle["sources"]
    require(sources["import_status"] == "pending_merge" and sources["imported_revision"] is None,
            "bootstrap must not claim an adopted contract")
    require(sources["tracking_fork"]["source_changes"] is False,
            "bootstrap must not claim modified Gitea")
    scenarios = bundle["scenarios"]["scenarios"]
    require(bundle["scenarios"]["design_status"] == "provisional_pending_merge",
            "scenario design must stay provisional")
    ids = [case["id"] for case in scenarios]
    require(len(ids) == 10 and set(ids) == {f"C{i}" for i in range(1, 11)},
            "scenario inventory must contain C1 through C10 exactly once")
    for case in scenarios:
        require(set(case["assessments"]) == set(PROVIDERS),
                "every scenario needs every provider assessed")
        for provider, assessment in case["assessments"].items():
            check_claim(assessment["status"], assessment["evidence"], unknown="not_run",
                        provider=provider, statuses=SCENARIO_STATUSES)
        require(bool(case["expectation"]) and bool(case["required_operations"]),
                "scenario must state an expectation and required operations")
    unmeasured = {}
    for name in PROVIDERS:
        manifest = bundle[name]
        require(manifest["provider"] == name, "provider identity mismatch")
        require(manifest["direct_path_bypasses"]["matrix"] == "bypass-matrix.json",
                "manifest must reference its own provider matrix")
        check_claim(manifest["implementation_status"], manifest["evidence"],
                    unknown="not_implemented", provider=name)
        if manifest["supported_operations"]:
            require(manifest["implementation_status"] != "not_implemented",
                    "supported operations require an implementation")
            check_claim("supported", manifest["evidence"], provider=name)
        for field in ("expected_state_guarantees", "idempotency_guarantees", "event_mechanism",
                      "pre_mutation_interception", "offline_support"):
            check_claim(manifest[field], manifest["evidence"], provider=name)
        for field in ("direct_path_bypasses", "external_dependencies"):
            check_claim(manifest[field]["status"], manifest["evidence"], provider=name)
        planned = manifest["planned_operations"]
        require(len(planned) == len(set(planned)), "duplicate planned operation")
        require(set(manifest["supported_operations"]) <= set(planned),
                "supported operation not planned")
        for case in scenarios:
            require(set(case["required_operations"]) <= set(planned), "scenario operation not planned")
        matrix = bundle[f"{name}_matrix"]
        require(matrix["provider"] == name, "matrix provider identity mismatch")
        require(len(matrix["routes"]) == len(ROUTES) and set(matrix["routes"]) == ROUTES,
                "native route inventory is incomplete")
        operations = matrix["operations"]
        require(len(operations) == len(MUTATIONS) and
                {row["operation"] for row in operations} == MUTATIONS,
                "mutation inventory is incomplete")
        for row in operations:
            require(set(row["assessments"]) == ROUTES, "every mutation needs every route assessed")
            seam = row["pre_action_seam"]
            check_claim(seam["status"], seam["evidence"], provider=name,
                        statuses=SEAM_STATUSES, seam=True)
            for cell in row["assessments"].values():
                check_claim(cell["status"], cell["evidence"], provider=name, statuses=ROUTE_STATUSES)
        unmeasured[name] = sum(cell["status"] == "unmeasured" for row in operations
                               for cell in row["assessments"].values())
    template = bundle["template"]
    require(template["kind"] == "template_not_evidence" and template["status"] == "not_run" and
            template["evidence"] == [] and template["operations"] == [], "template is not run evidence")
    for field in ("provider", "adapter_revision", "provider_version", "run_id"):
        require(template[field] is None, "template must not impersonate an actual run")
    return {"bootstrap_structure_valid": True, "provider_conformance": "not_evaluated",
            "scenarios": len(scenarios), "unmeasured_bypass_cells": sum(unmeasured.values()),
            "unmeasured_bypass_cells_by_provider": unmeasured}


if __name__ == "__main__":
    try:
        print(json.dumps(validate(load()), sort_keys=True))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"bootstrap_structure_valid": False, "error": str(error)}))
        raise SystemExit(1)
