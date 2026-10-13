# Contributing to comic-character-consistency-studio

Thanks for wanting to push the character-consistency needle. This repo is a
service-oriented Python desktop tool that turns a character bible + script
into a page-by-page comic with locked character identity across panels.

## Dev environment

```bash
python -m venv .venv
. .venv/Scripts/activate     # Windows
pip install -e ".[dev]"
pre-commit install
```

Python 3.12+ is required. We track Ruff for lint/format, mypy for types, and
pytest for tests. CI runs all three on Windows and Linux.

## Architecture

The codebase is service-oriented:

- `handlers/` — thin CLI + desktop entry points. No business logic lives here.
- `services/` — orchestration: identity locking, panel composition, pipeline runs.
- `models/` — data contracts (pydantic v2). No I/O.
- `adapters/` — platform boundaries: SDXL/Flux backends, GPU probes, filesystem.
- `utils/` — pure helpers. No service imports.

Rules:
1. Handlers never import adapters directly.
2. Services own cross-adapter orchestration.
3. Adapters never import services (inversion via protocols in `models/protocols.py`).

## Adding a new render backend

1. Implement `RenderBackend` from `models/protocols.py`.
2. Register it in `services/backend_registry.py`.
3. Add a smoke test in `tests/test_backend_registry.py`.

## Character identity contract

Every panel must carry a `CharacterFingerprint` — a 128-D identity embedding
plus a hash of the character bible revision. If two panels for the same
character disagree beyond `IDENTITY_DRIFT_TOLERANCE`, the pipeline fails the
page and emits a `ConsistencyViolation`.

Do not loosen the tolerance without a benchmark in `benchmarks/`.

## Commit style

Conventional commits. Scope = service or adapter name.
`feat(identity-lock): add pose-agnostic face anchor`

## Security

See `SECURITY.md`. Report privately, not via issues.