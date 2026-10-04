# Repository Plane

Provider-independent repository infrastructure for Web4 societies. GitHub is a
provider; Git is a storage/versioning substrate. Neither defines governance.

**Bootstrap only:** no provider adapter, gate, service, or deployment is implemented.
The design-document import is waiting for [Web4 #890](https://github.com/dp-web4/web4/pull/890)
to merge. Capability manifests describe planned scope and explicitly report no
implemented operations. Passing the bootstrap checks is not provider conformance.

## Boundaries

Repository Plane will normalize repositories, revisions, refs, change proposals,
reviews, artifacts and observed provider outcomes. Web4 remains canonical for
identity, role occupancy, authority, law, witness and ratification semantics.

- Provider permission supplies capacity, not Web4 authority.
- A permit, dispatch and verified effect are separate facts.
- A timeout after dispatch remains ambiguous until reconciled.
- Repository synchronization and merge never ratify law.
- Webhooks observe changes; they are not pre-action gates.

Start with [architecture](docs/ARCHITECTURE.md), [assurance](docs/ASSURANCE.md), and
the [source/import record](docs/SOURCES.json). The PRD, provider contract and Gitea
spike pages currently point to the exact proposed Web4 documents, not adopted copies.

## First work

1. After Web4 #890 merges, import the implementation documents with source revision
   and content hashes; keep cross-ecosystem authority definitions canonical in Web4.
2. Implement the smallest GitHub workflow: inspect revision/ref, propose, review,
   check expected state, merge, and observe the resulting revision.
3. Exercise the same semantic corpus against stock Gitea; measure every mutation
   path before choosing configuration, hooks, a broker, or a server extension.
4. Run disconnected acceptance only after dependencies are staged locally.

The [Gitea tracking fork](https://github.com/dp-web4/gitea) is an evaluation asset,
not a maintained Web4 distribution. Its default branch stays upstream-clean;
experiments belong on separate branches tied to failing conformance tests.

## Bootstrap checks

Python 3.10+ standard library only, for repository maintenance tooling:

```sh
python3 tools/check_bootstrap.py
python3 -m unittest discover -s tools/tests -v
```

These commands validate manifests, scenario inventory and required evidence bindings.
They perform no network requests or repository mutations. The application language
and library/service split remain undecided; Python here is not that decision.

Work items remain in Web4: [adapter #886](https://github.com/dp-web4/web4/issues/886),
[Gitea spike #887](https://github.com/dp-web4/web4/issues/887),
[governed mutations #888](https://github.com/dp-web4/web4/issues/888), and
[seed lifecycle #889](https://github.com/dp-web4/web4/issues/889).

## License

Repository Plane original material is licensed under **AGPL-3.0-or-later**; see
[LICENSE](LICENSE). Copyright 2026 dp-web4 contributors. Gitea is a separate
upstream project under its own MIT license; no Gitea code is incorporated here.
No adapter-library relicensing or additional patent grant is implied by this bootstrap.
