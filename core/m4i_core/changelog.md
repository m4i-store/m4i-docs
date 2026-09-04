# m4i_core Changelog

## 0.3.0-alpha.1 — Registry-backed group runtime

### Changed

- `m4i_registry` is now a required native M4I dependency alongside `oxmysql`
- `m4i_core` no longer owns the canonical job/gang/group definition catalog
- active Core group runtime resolves job/gang/group definitions from `m4i_registry`
- `m4i_group_memberships` now carries `group_domain`
- fresh membership identity is `(character_id, group_domain, group_name)`
- `SetJob` validates canonical Registry job definitions and grades
- Core startup waits for required Registry readiness before Core migration/player load

### Migration

- schema migration v3 upgrades legacy membership rows to domain-aware membership state
- upgraded databases may read historical `m4i_groups` only to translate membership domains
- active Core 0.3 runtime does not create/query/update `m4i_groups` as a definition source
- the old table is intentionally not dropped automatically and remains rollback/migration evidence until isolated/production verification is complete

### Live definition refresh

- trusted Registry job/gang/group changes trigger a bounded refresh of affected online players
- Core re-reads authoritative Registry definitions rather than trusting event payload as canonical state
- Registry change events are accepted only from resource `m4i_registry`
- refresh uses a finite player snapshot with cooperative yielding; no unbounded frame loop was introduced
- source/session ownership guards remain enforced around yielding paths

### Architecture

- native start order is now `oxmysql -> m4i_registry -> m4i_core -> m4i_bridge`
- `GetRuntimeInfo()` reports the required definition registry
- Core still has no QBCore/Qbox/ESX/Ox Core dependency
- gameplay resources continue to depend on `m4i_bridge`, not direct Core internals

### Validation

- complete Core repository CI: PASS
- post-merge `main` CI: PASS
- manual migration/runtime diff review: completed
- fresh isolated real FiveM runtime validation is still required because previous isolated runtime evidence predates Registry 0.2/Core 0.3

## 0.2.0-alpha.1 — Standalone Primary Core

### Changed

- `m4i_core` was formally declared as the standalone primary framework runtime for native M4I mode
- its only dependency at that release stage was `oxmysql`; 0.3 later added native `m4i_registry`
- QBCore/Qbox/ESX/Ox Core remained non-required compatibility ecosystems, not Core dependencies
- runtime identity reports `mode = primary` and `externalFrameworkRequired = false`

### Added

- `GetRuntimeInfo()` for runtime identity/readiness diagnostics
- replicated `m4i_core:mode` and `m4i_core:externalFrameworkRequired` diagnostics
- CI static guards against accidental external-core coupling

### Validation

- feature/PR/post-merge CI passed
- manual diff/security review completed

This release did not itself perform a production framework/data migration. Existing production third-party resources still require compatibility audit before an old framework is removed.

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

- critical money remains immediate, atomic and ledger-backed rather than entering ordinary write-behind; durable retry idempotency applies when callers supply a stable `operationId`
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
