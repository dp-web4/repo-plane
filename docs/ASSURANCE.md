# Assurance status

No provider behavior, pre-mutation enforcement, crash safety, or offline capability
has been demonstrated by this bootstrap. Empty supported-operation lists mean no
adapter exists, not that the underlying provider lacks those operations.

Capability declarations separate planned operations from implemented support and
measured guarantees. The bypass matrix is entirely unmeasured. A route may only be
marked intercepted, disabled or inapplicable after concrete configuration and evidence
establish that claim; a post-action notification is not pre-action enforcement.

The conformance scenarios are design inputs pending Web4 #890 adoption. A future run
must identify provider/version, adapter revision, fixture scope, operation IDs,
expected/prior/resulting state and evidence references. Unsupported and unrun cases
must not be counted as passing. Passing a mock does not establish native-path coverage.

Administrative and internal mutation paths remain in the threat model. A broker is
insufficient if equivalent mutations can bypass it through another enabled route.
Native identity is not role occupancy; provider history is not the Web4 witness chain.

Gate-control mutations and administrative routes are explicit matrix entries.
`pre_action_seam` records hook/extension availability separately from interception
coverage. Inapplicability requires evidence about equivalent effects, not just a
missing API operation: a direct push of a merge commit to a target ref can produce
the ref change a proposal merge would produce. Do not prefill such cells as `n/a`.

The structural checker accepts bound evidence without verifying its truth or
sufficiency. Passing it establishes neither a measured guarantee nor conformance;
provider observations and review remain necessary.

Do not claim a successful operation from an HTTP acceptance response alone. Lost
responses after dispatch remain ambiguous. Expected-state changes require a new
governed request, not an automatic retry against a newer revision.
