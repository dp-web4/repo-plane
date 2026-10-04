# Repository Plane contributor instructions

Read README.md, docs/ASSURANCE.md, docs/ARCHITECTURE.md and docs/SOURCES.json first.
This repository is bootstrap scaffolding, not a functioning governed forge.

- Preserve concurrent work. Use branches and review for implementation changes.
- Keep authority semantics canonical in Web4; providers must not evaluate law or mint authority.
- Do not import the proposed Web4 #890 documents until its merge is verified.
- Record source revisions and evidence; never call planned or untested capabilities supported.
- Provider denial is not success. Ambiguous effects require reconciliation before retry.
- Do not choose an application language or service/library split without recording the experiment.
- Keep credentials, private coordination records and deployment details out of public artifacts.
- Do not deploy services, enable Actions on a forge, or mutate unrelated repositories as a test.
- Live conformance uses explicitly scoped disposable fixtures with an approved lifecycle.
- Gitea experiments stay on branches; default must remain upstream-clean.
- Before committing, run the bootstrap checker, its unit tests and git diff --check.
  These are structural checks, not provider, governance, or air-gap certification.
