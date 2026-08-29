# Configuration

## Configuration files

`m4i_bridge` loads and merges:

- `config/default.lua`: runtime/safety behavior
- `config/providers.lua`: provider selection, priority, autodetect, health
- `config/features.lua`: domain/service toggles and debug options

Later config layers override matching keys through deep merge.

## Current framework selection

Current default selected providers include:

```lua
selected = {
    framework = "qbox",
    inventory = "ox_inventory",
    ui = "ox_lib",
    notify = "ox_lib",
    progress = "ox_lib",
    target = "ox_target",
    dispatch = "none",
    database = "oxmysql"
}
```

The default framework therefore remains Qbox.

### Framework priority

Current framework priority begins with M4I as a fallback candidate:

```lua
framework = { "m4i", "qbox", "qbcore", "esx", "ox_core" }
```

This does **not** override a healthy selected Qbox provider. It matters when resolver fallback/recovery is needed.

For a production server that is not ready for M4I cutover, review both the selected provider and fallback policy before running `m4i_core` in production.

### Autodetect

Autodetect is disabled by default.

Explicit selected-provider configuration remains the production control path.

## `config/default.lua`

### `production`

Flags:

- `strictMode`
- `debugMode`
- `performanceMode`
- `safeMode`

Use these as deployment profiles, not as substitutes for testing.

### `plugins`

Controls plugin subsystem enablement, runtime registration, auto-start, and source-name enforcement.

### `hooks` / `middleware`

Controls extension system enablement, debug logging, and fail-hard behavior.

### `observability`

Controls metrics/timer collection and sampling.

### `logging`

Controls level, structured context, JSON output, and optional webhook forwarding.

### `security`

Controls source validation, callback payload/rate limits, suspicion scoring, anomaly thresholds, optional blocking, and ban-hook behavior.

### `callbacks`

Controls timeout, pending-request limits, optional token requirements, request ID limits, and server/client rate limits.

### `performance`

Contains bridge-level cache/memoization/profiling/metrics settings.

These bridge caches are integration/runtime optimizations. They do not turn the bridge into a second authoritative data store for another framework.

### `behavior`

Important resolver behavior includes:

- `failOnMissingProvider`
- `useAutodetectFallback`
- `runtimeProviderSwitching`
- `softFailDomains`
- `softFailServices`
- `includeRegisteredProvidersInFallback`

## Provider health

`providers.health` controls:

- periodic health interval
- maximum failures
- disable-on-failure behavior

The M4I provider also has explicit recovery logic for server/client alignment after a late or restarted `m4i_core` when runtime switching permits it.

## Selecting M4I Core

For a test/staging profile:

```lua
selected = {
    framework = "m4i",
    -- other domains stay explicit
}
```

Required start order:

```text
oxmysql -> m4i_core -> m4i_bridge -> M4I scripts
```

Do not make this production change until persistent data and third-party resources have a validated migration/compatibility path.

## Data responsibility

Changing `framework` changes which provider handles framework operations.

It does not make `m4i_bridge` responsible for provider persistence.

- provider `m4i`: native data behavior belongs to `m4i_core`
- provider QBCore/Qbox/ESX/Ox: data behavior belongs to that provider

## Example profiles

### Development

Use debug/profiling as needed and explicit provider selections.

### Staging

Use the exact production provider plan, stricter safety flags, and isolated persistent data.

### Production

Keep provider selection explicit, debug low, security validated, and do not change framework providers with connected players.
