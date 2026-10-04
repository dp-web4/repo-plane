# Disconnected acceptance plan

Status: not run. No local forge has been installed by this bootstrap.

On an isolated, explicitly owned test environment, stage pinned binaries/images,
dependencies and checksums before denying external networking. Record outbound
connection attempts throughout the test; do not disable the operator's shared network.

The acceptance sequence is cold start, local authentication, repository creation,
clone, push/fetch, proposal/review/merge, conformance execution, one Web4-gated
mutation, provider-event consumption, restart and reconciliation. If Actions later
enter scope, test with locally available components and runners.

Evidence must distinguish staged dependencies from runtime external dependencies.
Unexpected requests to public forges, registries or identity services are findings,
not silently allowed exceptions. Offline operation remains unknown until this is measured.
