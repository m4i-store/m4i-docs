# Universal M4I Architecture

## Purpose

M4I is designed as a platform, not as a single FiveM framework.

The platform has two separate responsibilities:

- `m4i_bridge` provides a stable compatibility boundary for M4I scripts.
- `m4i_core` is the native M4I framework/runtime and implements framework provider `m4i`.

These responsibilities must not be mixed.

## Platform model

```text
                    M4I SCRIPTS
                         |
                         v
                    m4i_bridge
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
 m4i (m4i_core)       QBCore         Qbox / ESX / Ox
        |                |                |
        v                v                v
 M4I DATA LAYER     Their own data    Their own data
        |            architecture      architecture
        v
     oxmysql
        |
        v
   MariaDB / MySQL
```

### Rule 1 — scripts depend on the bridge

M4I-owned gameplay resources must not depend directly on a framework.

They call `m4i_bridge` and the bridge translates the operation to the configured provider.

This allows one M4I script to run with provider `m4i` (`m4i_core` resource), QBCore, Qbox, ESX, or Ox Core when the required capability exists.

### Rule 2 — the selected framework owns its data

When framework provider `m4i` is selected, `m4i_core` owns the full player-state and persistence architecture.

When QBCore, Qbox, ESX, or Ox Core is selected, that framework remains responsible for its own cache, persistence, schema, and performance behavior.

**There is no M4I Data Proxy over other frameworks.**

`m4i_bridge` translates APIs. It does not create a second source of truth for another framework's player data.

### Rule 3 — M4I Data Layer is native-core only

The M4I Data Layer belongs to `m4i_core`, the resource implementing provider `m4i`.

Its design goals are:

- server-authoritative player state
- hot-path reads from memory after player load
- dirty tracking for ordinary mutable state
- immediate transactional persistence for critical financial operations
- event-driven state changes instead of polling
- controlled persistence instead of unnecessary writes
- metrics and slow-path observability

Future data-engine work may add request coalescing, snapshots, write queues, batching, backpressure, and additional subscription APIs. Planned features must not be documented as implemented until they ship.

## Third-party scripts

There are two categories.

### M4I-native scripts

These use `m4i_bridge` directly and are portable across supported providers.

### Framework-native third-party scripts

A script that directly imports QBCore, Qbox, ESX, or Ox Core is not automatically portable.

Long-term compatibility can be provided by reverse-compatibility resources such as QB/Qbox/ESX/Ox shims that translate public framework APIs into M4I contracts.

Compatibility shims cannot safely guarantee support for scripts that:

- hard-code framework database schemas
- import private framework internals
- rely on undocumented side effects
- execute provider-specific SQL directly

Those resources require a patch, adapter, or migration.

## Framework switching

Changing the framework provider is a controlled deployment operation, not a live gameplay feature.

A switch may require:

1. clean server stop
2. database backup
3. canonical identity mapping
4. money/job/group/ownership migration
5. provider configuration change
6. capability validation
7. restart and smoke tests
8. rollback if validation fails

Do not remove the existing framework from production until every required resource has either:

- been migrated to `m4i_bridge`, or
- passed an approved compatibility path.

## Current production policy

The current `m4i_bridge` default framework selection remains `qbox`, with autodetect disabled.

Provider `m4i` is supported through the `m4i_core` resource, but production cutover must be explicit. Staging the resource is not the same as selecting provider `m4i` as the active framework.
