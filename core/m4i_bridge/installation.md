# Installation

## Requirements

Minimum runtime requirements:

- FiveM artifact with Lua 5.4 support
- required provider resources for every enabled domain
- `oxmysql` when the bridge database domain is enabled

Framework provider examples:

- `m4i` -> resource `m4i_core`
- `qbox` -> `qbx_core`
- `qbcore` -> `qb-core`
- `esx` -> `es_extended`
- `ox_core` -> Ox Core resource stack

Other domains may require `ox_inventory`, `qb-inventory`, `ox_lib`, `qb-menu`, `ox_target`, `qb-target`, dispatch resources, and so on according to configuration.

## Resource setup

1. place `m4i_bridge` in the resources folder
2. keep the folder name exactly `m4i_bridge`
3. review `config/default.lua`, `config/providers.lua`, and `config/features.lua`
4. confirm every selected provider resource exists with the expected exact name

## Start order

The selected providers must be available before bridge-dependent M4I gameplay resources.

### Qbox example

```cfg
ensure oxmysql
ensure ox_lib
ensure qbx_core
ensure ox_inventory
ensure ox_target
ensure m4i_bridge

ensure m4i_example
```

### Native M4I Core example

```cfg
ensure oxmysql
ensure m4i_core
ensure m4i_bridge

ensure m4i_example
```

`m4i_core` must start before `m4i_bridge` when it is the selected framework provider.

## Current production default

The repository currently selects `qbox` as the framework by default and disables autodetect.

Do not assume this alone prevents every possible M4I fallback: review the configured framework priority list and whether `m4i_core` is running before a production staging/cutover.

## First boot checklist

1. verify selected providers match installed resources
2. start server and check startup validation
3. inspect `/m4i:debug`
4. confirm framework provider and domain/service states
5. inspect `GetFrameworkCapabilities()` for v4 framework semantics
6. test one callback
7. test notify/progress/inventory/target paths required by the server
8. verify provider stop/restart behavior in staging

## M4I Core migration warning

Installing `m4i_bridge` does not migrate an existing framework to `m4i_core`.

A native-core cutover can require identity, money, jobs, ownership, vehicles, licenses, housing, inventory references, and third-party schema migration.

Use the [m4i_core Production Rollout](../m4i_core/production-rollout.md) procedure.

## Common mistakes

- starting bridge before required providers
- selecting the wrong resource/provider name
- assuming all framework capabilities are identical
- bypassing bridge from M4I gameplay code
- mutating framework/core-owned DB tables directly
- running `m4i_core` automatic migrations against production without a backup
- switching a framework with connected players
