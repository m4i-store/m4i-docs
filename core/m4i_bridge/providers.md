# Providers

## Provider system overview

A provider is a concrete integration for a bridge domain such as framework, inventory, UI, target, or database access.

`m4i_bridge` isolates provider-specific logic in adapters so M4I scripts remain provider-neutral.

Provider selection is driven by `config/providers.lua`.

## Supported provider matrix

### Framework

- `m4i` -> FiveM resource name exactly `m4i_core`
- `qbox`
- `qbcore`
- `esx`
- `ox_core`

### Inventory

- `ox_inventory`
- `qb_inventory`

### UI

- `ox_lib`
- `qb_menu`
- `custom`

### Notify

- `ox_lib`
- `framework`
- `custom`

### Progress

- `ox_lib`
- `progressbar`
- `custom`

### Target

- `ox_target`
- `qb_target`
- `custom`

### Dispatch

- `none`
- `ps_dispatch`
- `cd_dispatch`
- `qs_dispatch`

### Database

- `oxmysql`

## Current framework defaults

Native M4I is now the default framework mode:

```lua
framework = "m4i"
```

The default automatic framework priority is intentionally M4I-only:

```lua
framework = { "m4i" }
```

This means the normal M4I configuration will **not silently fall back** to QBCore, Qbox, ESX, or Ox Core if `m4i_core` becomes unavailable.

Autodetect remains disabled by default. External framework adapters remain installed for explicit compatibility mode, and an operator can intentionally select one of them through configuration or a profile-scoped provider override.

## M4I provider readiness

The native `m4i` provider is implemented by the resource named exactly `m4i_core`.

The adapter does not consider it healthy merely because the resource is started. The normalized provider surface must be available and `IsReady()` must report ready. Bridge framework-domain recovery handles late Core readiness/resource restart without changing the default provider to another core.

## Universal v4 capability semantics

Framework providers do not all expose identical concepts.

The v4 contract reports capabilities for operations such as:

- canonical character identity
- money accounts
- idempotent money mutations
- primary job
- duty
- metadata
- groups

M4I scripts must not assume that a capability exists just because a provider is selected.

Use:

```lua
local info = exports.m4i_bridge:GetFrameworkCapabilities()
```

Unsupported semantics should fail explicitly.

## Native M4I Data Layer capabilities

The following capabilities are native to provider `m4i` / resource `m4i_core`:

```text
nativeDataLayer
playerSnapshot
bulkPlayerSnapshot
dataLayerState
dataSubscriptions
```

They expose the shipped M4I Data Layer snapshot/subscription/observability contract through `m4i_bridge`.

They are **not** universal framework features. For `qbox`, `qbcore`, `esx`, and `ox_core`, these flags remain false/unsupported unless a future contract explicitly defines otherwise.

The bridge must not emulate native M4I Data Layer capabilities by caching/intercepting another framework's data.

## Data ownership rule

Provider selection does **not** mean the bridge owns provider persistence.

- `m4i`: `m4i_core` owns the M4I Data Layer.
- `qbox`: Qbox owns its framework data/cache/persistence.
- `qbcore`: QBCore owns its framework data/cache/persistence.
- `esx`: ESX owns its framework data/cache/persistence.
- `ox_core`: Ox Core owns its framework data/cache/persistence.

There is no M4I Data Proxy layered over the non-M4I frameworks.

## Native subscription ownership

When an M4I gameplay resource subscribes through `m4i_bridge` while provider `m4i` is selected:

1. bridge captures the gameplay resource with `GetInvokingResource()`
2. bridge delegates that resource name to `m4i_core`
3. Core applies per-owner limits and cleanup to the gameplay resource
4. direct owner unsubscribe and resource stop remove the delegated bookkeeping
5. bridge stop/crash triggers defensive cleanup of all delegated callback references

Only the resource named exactly `m4i_bridge` can use the Core owner-delegation override. This is a narrow native integration contract, not a generic provider feature.

## Resolution and fallback

With the default M4I configuration:

1. selected framework provider `m4i` is attempted
2. default framework priority contains only `m4i`
3. autodetect is disabled
4. registered-provider fallback is disabled
5. if M4I is temporarily unavailable, the framework domain can soft-disable and recover when `m4i_core` becomes healthy; it does not silently become another framework

If an operator explicitly selects or enables another compatibility provider, that is a deliberate deployment choice and its own data architecture remains authoritative.

## Health checks

Resolver health behavior includes:

- periodic health checks
- failure counting per provider
- disable-after-threshold behavior
- recovery/reselection paths

Provider health is visible through bridge debug/metrics snapshots.

## Adding a new provider

1. implement the adapter for the required domain/side
2. declare exact dependencies and capabilities
3. register it through the bridge registry
4. add it to provider configuration where appropriate
5. run conformance tests for every capability it advertises
6. test stop/restart/recovery behavior

Provider logic stays inside adapters. M4I gameplay scripts stay provider-neutral.
