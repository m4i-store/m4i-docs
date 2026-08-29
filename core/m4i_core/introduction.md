# m4i_core Introduction

## What is `m4i_core`

`m4i_core` is the native, framework-neutral FiveM core for the M4I platform and implements framework provider `m4i` for `m4i_bridge`.

It is designed to provide M4I with its own server-authoritative runtime while keeping M4I gameplay scripts portable through `m4i_bridge`.

`m4i_core` does **not** depend on QBCore, Qbox, ESX, or Ox Core.

## Resource boundary

M4I-owned gameplay scripts must not call `m4i_core` directly.

The required path is:

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

This prevents M4I scripts from being locked to one framework and allows the same script to run against another supported framework provider.

## What `m4i_core` owns

Current v0.1 responsibilities include:

- canonical user and character identity
- provider identity links
- server-authoritative player objects
- named money accounts
- integer-cent financial accounting
- atomic balance + ledger transactions
- idempotent money operation IDs
- jobs, groups, grades, and duty state
- metadata and status state
- controlled persistence
- owner-targeted client player snapshots
- metrics and runtime diagnostics

## Data philosophy

After a player is loaded, ordinary getters read the in-memory player state instead of executing a SQL query per request.

Critical money mutations are persisted immediately and transactionally. Ordinary metadata/status state is dirty-tracked and persisted on the controlled save cycle and disconnect.

This is the foundation of the M4I Data Layer.

## Current release state

Current resource version: `0.1.0-alpha.1`.

The release candidate passed isolated runtime testing, real-client lifecycle testing, persistence/restart checks, concurrency/idempotency tests, a controlled soak, multiple Codex review cycles, and post-merge CI.

Production framework migration is still a separate controlled deployment operation. A successful code release does not mean an existing QBCore/Qbox/ESX server should remove its framework immediately.

## Read next

- [Architecture](architecture.md)
- [M4I Data Layer](data-layer.md)
- [Installation](installation.md)
- [Configuration](configuration.md)
- [Bridge Contract](bridge-contract.md)
- [Production Rollout](production-rollout.md)
