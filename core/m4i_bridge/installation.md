# Installation

## Requirements

Minimum runtime requirements depend on the selected providers.

For native framework provider `m4i`:

- FiveM artifact with Lua 5.4 support
- `oxmysql`
- `m4i_registry`
- `m4i_core`
- configured provider resources for other enabled bridge domains

Explicit external framework compatibility examples remain:

- `qbox` -> `qbx_core`
- `qbcore` -> `qb-core`
- `esx` -> `es_extended`
- `ox_core` -> Ox Core resource stack

Other domains may use providers such as `ox_inventory`, `qb-inventory`, `ox_lib`, `qb-menu`, `ox_target`, `qb-target`, dispatch resources, and so on according to configuration.

## Resource setup

1. place `m4i_bridge` in the resources folder
2. keep the folder name exactly `m4i_bridge`
3. review `config/default.lua`, `config/providers.lua`, and `config/features.lua`
4. confirm every selected provider resource exists with the expected exact name
5. for native M4I, confirm `m4i_registry` and `m4i_core` are the current compatible release lines

## Native M4I start order

Current native Core 0.3 requires Registry before Core:

```cfg
ensure oxmysql
ensure m4i_registry
ensure m4i_core

# optional non-framework domain providers
ensure ox_inventory
ensure ox_lib
ensure ox_target

ensure m4i_bridge
ensure m4i_admin

ensure m4i_example
```

The important framework/definition order is:

```text
oxmysql -> m4i_registry -> m4i_core -> m4i_bridge
```

`m4i_core` consumes canonical job/gang/group definitions directly from `m4i_registry`. Bridge consumes Core as framework provider `m4i` and exposes Registry definitions to gameplay scripts through a read-only service.

## Explicit Qbox compatibility example

```cfg
ensure oxmysql
ensure ox_lib
ensure qbx_core
ensure ox_inventory
ensure ox_target
ensure m4i_bridge

ensure m4i_example
```

In explicit external-framework compatibility mode, `m4i_registry` is not automatically turned into a Data Proxy or player-state authority for that external framework.

## Current framework default

The repository currently selects framework provider:

```text
m4i
```

The default framework priority is M4I-only, autodetect is disabled, and registered-provider fallback is disabled for the normal native profile.

Therefore a missing native Core does not silently convert the server to QBCore/Qbox/ESX/Ox Core. External providers are used only when explicitly configured for compatibility.

## First boot checklist — native M4I

1. verify `m4i_registry` becomes ready
2. verify `m4i_core:GetRuntimeInfo()` reports primary mode and required Registry
3. verify `m4i_core:IsReady()`
4. start Bridge
5. inspect `/m4i:debug`
6. confirm framework provider `m4i`
7. inspect `GetFrameworkCapabilities()`
8. inspect `GetDefinitionRegistryState()`
9. resolve one known definition through Bridge, such as `GetJobDefinition("unemployed")`
10. test callback/notify/inventory/target paths required by the server
11. test provider/resource restart behavior in isolated staging

## Definition registry read surface

When Registry is available, Bridge exposes read-only catalog access including:

```lua
exports.m4i_bridge:GetDefinitionRegistryState()
exports.m4i_bridge:GetDefinition(domain, key)
exports.m4i_bridge:ResolveDefinition(domain, keyOrAlias)
exports.m4i_bridge:ListDefinitions(domain, options)

exports.m4i_bridge:GetItemDefinition(key)
exports.m4i_bridge:GetJobDefinition(key)
exports.m4i_bridge:GetGangDefinition(key)
exports.m4i_bridge:GetGroupDefinition(key)
exports.m4i_bridge:GetVehicleDefinition(key)
exports.m4i_bridge:GetWeaponDefinition(key)
exports.m4i_bridge:GetLocationDefinition(key)
```

Bridge does not expose Registry create/update/delete/import/rollback mutations to gameplay scripts.

## M4I Core migration warning

Installing/staging the new Bridge does not migrate an existing production framework to native M4I.

A cutover can require identity, money, jobs/groups, shared definitions, ownership, vehicles, licenses, housing, inventory references, and third-party schema migration.

Use [m4i_core Production Rollout](../m4i_core/production-rollout.md).

## Common mistakes

- starting `m4i_core` before `m4i_registry` in native mode
- starting Bridge before required providers
- selecting the wrong provider/resource name
- assuming all framework capabilities are identical
- bypassing Bridge from M4I gameplay code
- mutating framework/Core/Registry-owned DB tables directly from gameplay scripts
- running Registry/Core automatic migrations against production without a backup
- assuming an existing framework can be removed because native Core merely starts
- switching framework provider with connected players
