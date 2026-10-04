# Conformance scaffold

The core scenario inventory follows C1 through C10 of the proposed Web4 provider
contract. Every scenario is not run. The GitHub and Gitea manifests currently declare
no supported operations. There is no provider runner or fabricated passing result.

`bypass-matrix.json` enumerates mutation effects against native routes. Unmeasured
cells are intentional. Do not infer that an API hook covers HTTP Git, SSH Git, UI,
internal jobs or workflows merely because the operation names match.

The minimum inventory is defined by `ROUTES` and `MUTATIONS` in
`tools/check_bootstrap.py`; the JSON instantiates that inventory. Changes to either
inventory must update both. Its 23 mutations and seven routes include changes to
branch protection, hooks, deploy keys and repository lifecycle controls. The
`operator_host` route covers administrative CLI actions and direct repository-storage
or database mutations. Evidence must distinguish these paths; one observed path does
not establish coverage of the others. This is a coverage inventory, not deployment
configuration.

Each operation also has a `pre_action_seam` assessment, separate from route coverage.
It records whether a hook or extension can act before the mutation. Evidence must
name the applicable route and scope; a seam's existence does not establish that all
native routes are governed.

`fixtures/result-template.json` is a format example, not a run. Future evidence must
bind requests and observed outcomes to exact revisions and preserve ambiguous effects.
The bootstrap checker checks structure and requires evidence for claims that advance
beyond `unmeasured`, `not_run` or `not_implemented`. Every evidence item must contain
non-empty strings for `provider`, `provider_version`, `adapter_revision`, `run_id`
and `reference` (the observation artifact). Provider-manifest evidence must match
that manifest's provider. Manifest evidence applies to its declared support and
guarantees; reviewers must verify that the referenced observations support each claim.
Scenario, route and seam evidence is stored with the corresponding assessment.

These are binding checks only: the checker does not fetch artifacts, authenticate
observations or decide whether evidence proves a claim. Its `provider_conformance`
output therefore always says `not_evaluated`, including when bound results are
present. The result template must remain empty and labelled `template_not_evidence`.
