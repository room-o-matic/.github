Fixes room-o-matic/docs#<!-- N --> <!-- or "Part of room-o-matic/docs#N" for companion PRs -->

**What and why**

**Tests**
- [ ] New tests fail without this change
- [ ] `uv run pytest -q`, `ruff check`, and `ruff format --check` pass
- [ ] `client/scripts/e2e.py` passes (any change that crosses a service boundary)
- [ ] Shared copies (`verify.py`, `ops.py`) are synced, if touched
- [ ] Schema change: `SCHEMA_VERSION` bumped and the migration tested
- [ ] No real credentials or personal data in code, tests or this PR
