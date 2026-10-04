# Conformance scaffold

The core scenario inventory follows C1 through C10 of the proposed Web4 provider
contract. Every scenario is not run. The GitHub and Gitea manifests currently declare
no supported operations. There is no provider runner or fabricated passing result.

`providers/<provider>/bypass-matrix.json` enumerates mutation effects against native
routes separately for GitHub and Gitea. Each matrix names its provider. Unmeasured
cells are intentional. Do not infer that an API hook covers HTTP Git, SSH Git, UI,
internal jobs or workflows merely because the operation names match.

The minimum inventory is defined by `ROUTES` and `MUTATIONS` in
`tools/check_bootstrap.py`; the JSON instantiates that inventory. Changes to either
inventory must update both provider matrices. Its 23 mutations and nine routes include changes to
branch protection, hooks, deploy keys and repository lifecycle controls. The
`operator_cli`, `operator_storage` and `operator_db` routes distinguish administrative
CLI actions, direct repository-storage mutations and direct database mutations.
Each provider has 207 cells (414 total); one observed path or provider does not establish
coverage of the others. This is a coverage inventory, not deployment
configuration.

Each operation also has a `pre_action_seam` assessment, separate from route coverage.
It records whether a hook or extension can act before the mutation. Evidence must
name the applicable `route` (one of the nine route identifiers) and a non-empty
`scope` describing the conditions under which the observation applies. These fields
are required on every seam evidence item. A seam's existence does not establish that
all native routes are governed.

Route status is one of `unmeasured`, `blocked`, `bypassable`, `partial` or
`not_applicable`. `blocked` means the observed mutation was prevented in the tested
conditions; it does not establish that Web4 authority caused that prevention.
Seam status is `unmeasured`, `present` or `absent`. C1–C10 share scenario definitions,
with separate `assessments` for `github` and `gitea`; each status is `not_run`,
`passed`, `failed`, `partial` or `unsupported`. Unknown status strings are rejected
in these assessments, including when evidence is present. No status aggregates
other routes or providers. Capability-manifest descriptions retain their existing
free-text vocabulary and evidence requirements.

`fixtures/result-template.json` is a format example, not a run. Future evidence must
bind requests and observed outcomes to exact revisions and preserve ambiguous effects.
The bootstrap checker checks structure and requires evidence for claims that advance
beyond `unmeasured`, `not_run` or `not_implemented`. Every evidence item must contain
non-empty strings for `provider`, `provider_version`, `adapter_revision`, `run_id`
and `reference` (the observation artifact). Every evidence item's provider must match
its manifest, matrix or scenario assessment. Manifest evidence applies to its declared support and
guarantees; reviewers must verify that the referenced observations support each claim.
Scenario, route and seam evidence is stored with the corresponding assessment.
The checker reports unmeasured route-cell counts per provider and in total.

These are binding checks only: the checker does not fetch artifacts, authenticate
observations or decide whether evidence proves a claim. Its `provider_conformance`
output therefore always says `not_evaluated`, including when bound results are
present. The result template must remain empty and labelled `template_not_evidence`.
