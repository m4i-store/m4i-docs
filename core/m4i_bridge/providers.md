# Providers

## Provider system overview

A provider is a concrete integration for a bridge domain (framework, inventory, UI, and so on).

`m4i_bridge` separates provider-specific logic into adapters so scripts stay provider-neutral.

Provider selection is driven by `config/providers.lua`.

## Supported provider matrix

### Framework

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

## How resolution and fallback work

When resolving a domain:

1. selected provider is attempted first
2. if unavailable/invalid/unhealthy, priority providers are attempted in order
3. if enabled, autodetect order is attempted
4. optionally, other registered providers are considered
5. if all fail:
- domain may soft-disable (if configured)
- or startup fails with clear reason

## Health checks

Resolver health behavior includes:

- periodic health checks (`providers.health.checkIntervalMs`)
- failure counting per provider
- disable provider after `maxFailures` when `disableOnFailure = true`

Health state is visible via debug snapshot and metrics snapshot.

## Dependency checks

Each adapter may declare dependencies (for example `ox_lib`, `qb-core`, `es_extended`).

Resolver validates resource state before using the adapter.

## Conceptual guide: adding a new provider

1. create adapter files under `adapters/<domain>/<provider>/` for required sides
2. implement all contract methods for that domain/side
3. include adapter `meta` with `implemented = true` and dependencies
4. register adapter via `Bridge.registerAdapter(domain, provider, side, adapter)`
5. add provider into `config/providers.lua` (selected/priority/autodetect as needed)
6. test startup resolution and runtime calls with `/m4i:debug`

Keep provider logic inside adapters only. Service and script layers should remain provider-agnostic.
