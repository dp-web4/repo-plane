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

Do not claim a successful operation from an HTTP acceptance response alone. Lost
responses after dispatch remain ambiguous. Expected-state changes require a new
governed request, not an automatic retry against a newer revision.
