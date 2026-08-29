# m4i_core Changelog

## 0.1.0-alpha.1 — Native Core Release Candidate

### Added

- canonical M4I user and character identity
- provider identity links
- server-authoritative player runtime
- integer-cent named money accounts
- atomic account + ledger transactions
- durable money operation ID idempotency
- jobs/groups/grades/duty
- metadata/status state
- controlled persistence
- owner-targeted client player snapshots
- metrics/runtime validation hooks
- native `m4i_bridge` provider surface

### Hardened

The v0.1 line includes fixes for:

- stale and recycled source IDs
- duplicate character sessions
- bounded reconnect/session handoff
- delayed reservation cleanup
- load-attempt ownership during source reuse
- job grade validation
- final disconnect position capture
- deterministic money failure handling
- optimistic money rollback/retry
- sensitive state replication
- client data-request throttling

### Post-RC hotfix

A delayed `playerUnloaded` event could otherwise fire after FiveM reused the same numeric source ID. The hotfix emits the old-session unload signal before yielding persistence paths and carries stable detached-session identity data for downstream cleanup.

The hotfix passed its regression suite, Codex review, and post-merge `main` CI.

## Current limitations

- first-character/slot-1 auto-provisioning is the current alpha lifecycle
- complete multicharacter selection is not yet part of the released contract
- reverse compatibility for arbitrary third-party framework resources is separate work
- broader multi-client capacity testing remains useful before making large-scale performance claims
