# m4i_core Introduction

## What is `m4i_core`

`m4i_core` is the native standalone primary FiveM core for the M4I platform and implements framework provider `m4i` for `m4i_bridge`.

It provides M4I with its own server-authoritative player/runtime architecture while keeping M4I gameplay scripts portable through `m4i_bridge`.

`m4i_core` does **not** depend on QBCore, Qbox, ESX, or Ox Core.

Current native runtime dependencies are:

- `oxmysql` — database driver
- `m4i_registry` — native canonical definition service

`m4i_registry` is M4I infrastructure, not another framework core.

Current standalone-primary line: `0.3.0-alpha.1`.

## Runtime identity

The core exposes:

```lua
exports.m4i_core:GetRuntimeInfo()
```

The returned runtime identity includes architecture/readiness data such as:

```text
mode = primary
externalFrameworkRequired = false
databaseDriver = oxmysql
definitionRegistry = m4i_registry
definitionRegistryRequired = true
```

These fields do not switch providers or migrate production data.

## Resource boundary

M4I-owned gameplay scripts should normally call `m4i_bridge`, not framework-specific APIs directly.

Native path:

```text
M4I Script
    |
    v
m4i_bridge
    |
    v
provider m4i
    |
    v
m4i_core
```

Canonical definition path:

```text
m4i_registry
   |      \
   |       +--> m4i_bridge read-only definition exports
   v
m4i_core job/gang/group runtime validation
```

The bridge default framework provider is `m4i`, and its default framework priority is M4I-only. QBCore/Qbox/ESX/Ox Core adapters remain available for explicit compatibility mode but are not dependencies of native M4I.

## What `m4i_core` owns

Current responsibilities include:

- canonical user and character identity
- provider identity links
- server-authoritative player objects and session lifecycle
- named money accounts
- integer-cent financial accounting
- atomic balance + ledger transactions
- durable money retry/idempotency semantics when a stable operation ID is supplied
- player job/gang/group **membership runtime**
- membership grade/active/duty state
- metadata and status state
- controlled persistence
- owner-targeted client player snapshots
- M4I Data Layer snapshots/subscriptions/write-behind/backpressure/metrics
- runtime diagnostics and readiness

## What `m4i_core` no longer owns

Core 0.3 no longer owns the canonical job/gang/group definition catalog.

Definition data now belongs to `m4i_registry`:

```text
registry: police = job, grades 0..5
core:     character 42 = police grade 3, onDuty true
```

The historical `m4i_groups` table can still exist on upgraded databases as migration/rollback evidence, but active 0.3 group runtime does not use it as a definition source.

## Live definition changes

When a trusted registry job/gang/group definition changes, Core re-reads authoritative registry data and refreshes affected online players from a bounded player snapshot.

This allows definition changes to propagate without restarting Core/server while preserving source/session safety around yielding work.

## Data philosophy

After a player is loaded, ordinary getters read authoritative in-memory player state instead of executing a SQL query per logical request.

Critical money mutations are persisted immediately and transactionally. Ordinary metadata/status state is dirty-tracked and persisted through the controlled Data Layer policy and disconnect/restart lifecycle.

## Current release state

The registry-backed Core 0.3 code contract is merged in `m4i_core/main`. The canonical group-definition Registry 0.2, Admin 0.2 UI and Bridge read-only definition surface are also merged in their respective repositories.

Repository CI verifies the native Core remains free of QBCore/Qbox/ESX/Ox Core dependencies and validates the registry-backed group/membership migration contract.

The remaining release gate before an existing production server should remove its old framework is **fresh isolated real FiveM runtime validation plus production compatibility/data migration planning**. A native Core being standalone does not make framework-specific third-party resources automatically portable.

## Read next

- [m4i_registry](../m4i_registry.md)
- [Architecture](architecture.md)
- [M4I Data Layer](data-layer.md)
- [Installation](installation.md)
- [Configuration](configuration.md)
- [Bridge Contract](bridge-contract.md)
- [Production Rollout](production-rollout.md)
