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
    framework = "m4i",
    inventory = "ox_inventory",
    ui = "ox_lib",
    notify = "ox_lib",
    progress = "ox_lib",
    target = "ox_target",
    dispatch = "none",
    database = "oxmysql"
}
```

The default framework is now native M4I, implemented by the `m4i_core` resource.

### Framework priority

The normal/default automatic framework priority is intentionally restricted to M4I:

```lua
framework = { "m4i" }
```

This prevents an outage or late readiness of `m4i_core` from silently changing the server to QBCore, Qbox, ESX, or Ox Core.

External framework adapters remain available for **explicit compatibility mode**. An operator can intentionally select another provider through configuration or the profile-scoped `m4i_bridge:frameworkProvider` override.

### Autodetect

Autodetect is disabled by default.

Its order may still contain supported external framework adapters, but that list is inactive unless an operator deliberately enables autodetection. Native M4I remains first.

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

With the shipped defaults, framework-domain soft-fail/recovery allows `m4i_bridge` to start while `m4i_core` is finishing database/migration readiness. When the Core ready signal arrives, the bridge refreshes provider `m4i`. This recovery does not select an external core under the default framework priority.

## Provider health

`providers.health` controls:

- periodic health interval
- maximum failures
- disable-on-failure behavior

The M4I provider has explicit recovery logic for server/client alignment after a late or restarted `m4i_core` when runtime switching permits it.

## Native M4I primary mode

Required framework start order:

```text
oxmysql -> m4i_core -> m4i_bridge -> M4I scripts
```

No QBCore/Qbox/ESX/Ox Core resource is required for this framework path.

Other bridge domains can still use their selected non-core providers such as `ox_inventory`, `ox_lib`, or `ox_target`. Those are separate domain providers, not framework cores.

## Explicit compatibility mode

To intentionally run an M4I script against another supported framework, select that provider explicitly, for example:

```lua
selected = {
    framework = "qbox"
}
```

or use the isolated/profile override:

```cfg
set m4i_bridge:frameworkProvider qbox
```

In that mode, the selected external framework owns its own state and persistence. `m4i_bridge` does not place an M4I Data Proxy above it.

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

Keep provider selection explicit, debug low, security validated, and do not change framework providers with connected players. Even though M4I is now the product default, migrating an existing production server remains a controlled compatibility/data-cutover operation.
