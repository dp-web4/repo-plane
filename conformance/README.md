# Conformance scaffold

The core scenario inventory follows C1 through C10 of the proposed Web4 provider
contract. Every scenario is not run. The GitHub and Gitea manifests currently declare
no supported operations. There is no provider runner or fabricated passing result.

`bypass-matrix.json` enumerates mutation effects against native routes. Unmeasured
cells are intentional. Do not infer that an API hook covers HTTP Git, SSH Git, UI,
internal jobs or workflows merely because the operation names match.

`fixtures/result-template.json` is a format example, not a run. Future evidence must
bind requests and observed outcomes to exact revisions and preserve ambiguous effects.
The bootstrap checker only checks that the scaffold remains structurally consistent
and makes no measured claims.
