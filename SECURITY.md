# Security policy

## Reporting a vulnerability

**Please don't open a public issue for a security problem.**

Report it privately with GitHub's vulnerability reporting: open the affected repository's **Security** tab and choose **Report a vulnerability**. If you aren't sure which repository is affected, report it against [room-o-matic/docs](https://github.com/room-o-matic/docs).

Please include:

- the affected service and commit
- the configuration you used, such as the backend, room admission and tenants
- the steps to reproduce, and what an attacker gains

We aim to acknowledge reports within a week. We'll keep you updated until a fix lands, and credit you in the fix unless you'd rather not be named.

## Supported versions

The project is pre-1.0, and only `main` of each repository is supported. Fixes are not backported.

## Scope

**In scope:** anything that lets a caller act as another identity, read or write a room it has no rights to, escape an agentd profile or the sandbox backend, keep access after it has been revoked, or exhaust a service despite its documented budgets.

**Documented limits, not vulnerabilities:**

- **The agentd `process` backend provides no isolation.** It is for trusted callers only; untrusted callers must run on `backend: sandbox`.
- **Issued access tokens outlive their revocation.** A revoked API key's tokens stay valid until they expire, at most 15 minutes.
- **Quickstart defaults are trusting.** `open` rooms, the `internal` tenant and `trusted` callers are meant for a single operator. See the [security posture](https://github.com/room-o-matic/docs#security-posture).
- **Exposing `/metrics` or serving without TLS** is a deployment choice. Put a reverse proxy with TLS in front, and keep `/metrics` internal.
