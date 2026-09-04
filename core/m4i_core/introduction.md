# m4i_core Introduction

## What is `m4i_core`

`m4i_core` is the native standalone primary FiveM core for the M4I platform and implements framework provider `m4i` for `m4i_bridge`.

It provides M4I with its own server-authoritative runtime while keeping M4I gameplay scripts portable through `m4i_bridge`.

`m4i_core` does **not** depend on QBCore, Qbox, ESX, or Ox Core. Its declared runtime dependency is `oxmysql`, which is the database driver rather than another framework core.

Current standalone-primary line: `0.2.0-alpha.1`.

## Runtime identity

The core exposes:

```lua
exports.m4i_core:GetRuntimeInfo()
```

The returned runtime identity includes:

```text
mode = primary
externalFrameworkRequired = false
databaseDriver = oxmysql
```

Replicated diagnostics also publish the primary mode so runtime health/debug tooling can verify the intended architecture.

## Resource boundary

M4I-owned gameplay scripts should normally call `m4i_bridge`, not framework-specific APIs directly.

The native path is:

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
m4i_core resource
```

The bridge default framework provider is now `m4i`, and its default framework priority is M4I-only. QBCore/Qbox/ESX/Ox Core adapters remain available for explicit compatibility mode but are not required by the native M4I stack.

## What `m4i_core` owns

Current responsibilities include:

- canonical user and character identity
- provider identity links
- server-authoritative player objects and session lifecycle
- named money accounts
- integer-cent financial accounting
- atomic balance + ledger transactions
- durable idempotent money behavior when a stable operation ID is supplied
- jobs, groups, grades, and duty state
- metadata and status state
- controlled persistence
- owner-targeted client player snapshots
- M4I Data Layer snapshots/subscriptions/write-behind/backpressure/metrics
- runtime diagnostics and readiness

## Data philosophy

After a player is loaded, ordinary getters read authoritative in-memory player state instead of executing a SQL query per logical request.

Critical money mutations are persisted immediately and transactionally. Ordinary metadata/status state is dirty-tracked and persisted through the controlled Data Layer policy and disconnect/restart lifecycle.

## Current release state

The standalone-primary code contract is merged in `m4i_core/main`, and the corresponding bridge primary-default change is merged in `m4i_bridge/main`.

Repository CI validates that the core manifest declares only `oxmysql` as a runtime dependency and that native runtime Lua is not coupled to QBCore/Qbox/ESX/Ox Core symbols.

The remaining release gate before an existing production server should remove its old framework is **isolated FiveM runtime validation plus production compatibility/data migration planning**. A native Core being standalone does not mean third-party framework-specific resources can be deleted without audit.

## Read next

- [Architecture](architecture.md)
- [M4I Data Layer](data-layer.md)
- [Installation](installation.md)
- [Configuration](configuration.md)
- [Bridge Contract](bridge-contract.md)
- [Production Rollout](production-rollout.md)
