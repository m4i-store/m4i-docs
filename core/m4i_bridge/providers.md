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

Current bridge configuration selects:

```lua
framework = "qbox"
```

Autodetect is disabled by default.

The framework priority list includes M4I as a fallback candidate. Therefore, if `m4i_core` is running and the selected framework becomes unavailable, provider health/fallback configuration can matter.

For a production server that is not ready to cut over to M4I, do not assume that merely keeping `framework = "qbox"` is the entire migration plan. Control whether `m4i_core` is running and review the priority/fallback policy before deployment.

## M4I provider readiness

The native `m4i` provider is not healthy merely because the resource is started.

The adapter requires the normalized provider surface to be functional, including `GetPlayerData`, and requires `IsReady()` to report ready.

A partial `GetPlayer`-only implementation is not accepted as a healthy M4I framework provider.

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

They are **not** universal framework features.

For:

- `qbox`
- `qbcore`
- `esx`
- `ox_core`

these flags remain false/unsupported unless a future contract explicitly defines otherwise.

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

In practice:

1. selected provider is attempted first
2. if unavailable/invalid/unhealthy, configured priority providers may be attempted
3. if enabled, autodetect order may be attempted
4. optionally other registered providers may be considered
5. if all fail, the domain can soft-disable or startup can fail according to configuration

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
