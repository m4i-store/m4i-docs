# m4i_core Changelog

## Data Layer v1 — shipped

### Added

- authoritative player-state snapshot API
- revision-aware bounded snapshot micro-cache
- bounded bulk player snapshots
- native data-change event/subscription bus
- wildcard subscriptions
- bounded subscription delivery queue and fixed worker pool
- bounded per-tick delivery with cooperative yielding
- per-load `sessionGeneration` binding for queued player-scoped work
- ordinary dirty-state write-behind with per-character coalescing
- bounded min-heap persistence queue
- high-water backpressure behavior
- bounded retry/backoff and dirty-scan recovery
- wrap-safe monotonic scheduling across FiveM game-timer wrap
- Data Layer metrics and bounded latency percentile sampling
- 100 x 100 logical snapshot stress harness

### Correctness / lifecycle hardening

- critical money remains immediate, atomic, ledger-backed and idempotent rather than entering ordinary write-behind
- job/duty remains on the immediate controlled persistence path
- DB-yielding duty mutation revalidates the captured live session before sync/event emission
- stale/reused source deliveries are rejected
- same-character/same-source reconnects are separated with `sessionGeneration`
- terminal `player.unloaded` always exposes primary source as `nil` while retaining historical source/stable identity in metadata/payload
- synchronous `m4i_core:server:dataChanged` follows the same terminal unload source contract

### Trusted bridge subscription ownership

- `m4i_bridge` can delegate the real gameplay-resource owner for native subscriptions
- only the resource named exactly `m4i_bridge` may use the owner override
- per-resource subscription caps and cleanup apply to the real gameplay consumer
- gameplay-owner stop and bridge stop/crash defensively clean delegated subscription references
- direct owner unsubscribe prunes delegation bookkeeping
- non-bridge owner spoofing is rejected

These changes remain native to `m4i_core`; no Data Proxy behavior is introduced for QBCore/Qbox/ESX/Ox Core.

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
- the 100 x 100 Data Layer harness is a logical/core workload, not a claim about 100 simultaneous real FiveM clients
- broader real-client/VPS capacity testing remains required before large-scale performance claims
