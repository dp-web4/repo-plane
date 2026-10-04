# Architecture boundaries

This repository will own provider adapters, normalized operations, provider evidence,
conformance tooling and local deployment experiments. It is not a new Web4 fact plane.

The intended operation path is normalization, identity/role/target/expected-state
binding, Web4/Hestia decision, provider dispatch, observation, and separate outcome
evidence. A native token never substitutes for the decision. Provider adapters carry
Web4 bindings but must not grow a parallel policy engine.

The library, daemon and broker options remain experiments. Before choosing, compare
credential custody, bypass coverage, expected-state enforcement, crash recovery,
consumer integration cost and offline operation on the same scenarios.

The first implementation is the GitHub reference workflow. Gitea starts as stock
software with local storage, local authentication and Actions disabled. Evaluate
configuration, supported hooks, a broker and narrow upstream extensions in that order.
A maintained fork requires a reproducing test that rules those options out.

No runtime package or source tree has been selected yet. The only executable material
is the standard-library bootstrap validator and its tests.
