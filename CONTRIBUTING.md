# Contributing to room-o-matic

Thanks for helping. room-o-matic is five repositories that ship together:

| Repo | Contains |
|---|---|
| [docs](https://github.com/room-o-matic/docs) | Design, protocols, operations, **and the issue tracker for everything** |
| [lobby](https://github.com/room-o-matic/lobby) | `lobbyd` |
| [rooms](https://github.com/room-o-matic/rooms) | `roomsd` |
| [agents](https://github.com/room-o-matic/agents) | `agentd` |
| [client](https://github.com/room-o-matic/client) | `roomomatic` library and `rom` CLI |

## How work flows

1. **Open or pick an issue in [room-o-matic/docs](https://github.com/room-o-matic/docs/issues)**, even if the fix is in a code repo.
2. Make the change on a branch in each affected repo. Name branches like `fix/docs-N-short-name` or `feat/docs-N-short-name`.
3. **Add a test that fails without your change.** We check this by running the new tests against the old code.
4. Open one PR per repo. The PR that completes the issue says `Fixes room-o-matic/docs#N`, and companion PRs say `Part of room-o-matic/docs#N`.
5. PRs are squash-merged once CI passes.

## Local setup

Clone the code repos side by side. The cross-service test expects `../lobby`, `../rooms` and `../agents` next to `client`. You need Python 3.12 and [uv](https://docs.astral.sh/uv/). The agentd sandbox tests also need bubblewrap.

```bash
uv sync
uv run pytest -q                          # what CI runs, plus:
uv run ruff check . && uv run ruff format --check .
cd client && uv run python scripts/e2e.py # real lobbyd + roomsd + agentd; run it for any cross-service change
```

## Conventions

- **Stack:** Python 3.12, FastAPI and raw `sqlite3`, with no ORM. Use ruff with a line length of 100.
- **Read the architecture notes first.** [CLAUDE.md](https://github.com/room-o-matic/docs/blob/main/CLAUDE.md) records the invariants every change must keep. For example:
  - identity comes only from the token;
  - roomsd never calls agentd;
  - agentd routes are `async` on one shared connection;
  - access removals are journaled for restore.
- **Shared files are copies.** `verify.py` (canonical in `lobby`) and `ops.py` are kept identical across lobby, rooms and agents. Change one, then copy it to the others in the same set of PRs.
- **Schema changes need migrations:** bump `SCHEMA_VERSION`, add a migration, and test the upgrade. See the [operations guide](https://github.com/room-o-matic/docs/blob/main/design/operations.md).
- **API changes reach the client:** update the `roomomatic` client, its `FakeWorld` test fakes, and `scripts/e2e.py`.
- **No real credentials anywhere,** including tests, fixtures, logs, issues and PRs. Use obviously fake values such as `sk-ant-xyz-123456` or `rmsd_secret`.
- **Paid live tests are opt-in.** `agents/scripts/live_smoke.py` makes real, budget-capped model calls and runs only with `ROM_LIVE_SMOKE=1`; CI never runs it.

## Security issues

Report them privately; see [SECURITY.md](SECURITY.md).
