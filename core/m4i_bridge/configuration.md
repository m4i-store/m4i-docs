# Configuration

## Configuration files

`m4i_bridge` loads and merges these files at startup:

- `config/default.lua`: core runtime defaults and safety behavior
- `config/providers.lua`: provider selection and provider fallback order
- `config/features.lua`: feature/domain/service toggles and debug switches

Merge behavior is deep-merge (later files override matching keys).

## `config/default.lua` overview

### `production`

Production override flags:

- `strictMode`
- `debugMode`
- `performanceMode`
- `safeMode`

These flags adjust other sections at runtime (for example, strict mode forces fail-hard behavior for hooks/middleware).

### `core`

- `core.debug`: baseline debug switch used by internal services.

### `plugins`

- `enabled`: enable or disable plugin subsystem
- `allowRuntimeRegistration`: allow plugin registration after kernel start
- `autoStartOnKernelStart`: automatically start registered plugins when kernel starts
- `enforceSourceNameMatch`: enforce plugin name to match invoking resource

### `hooks`

- `enabled`: global hook system toggle
- `debugLogging`: emit hook debug logs
- `failHard`: fail execution flow when hook handler errors

### `middleware`

- `enabled`: global middleware toggle
- `debugLogging`: emit middleware debug logs
- `failHard`: fail chain when middleware handler errors

### `observability`

- `enabled`: observability master switch
- `metricsEnabled`: metrics collection switch
- `sampleRate`: timer sampling ratio (0 < value <= 1)
- `debugLogging`: observability debug output

### `hotReload`

- `cleanupOnResourceStop`: cleanup plugin/hook/middleware registrations when a resource stops

### `logging`

- `level`: `debug`, `info`, `warn`, `error`, `fatal`
- `includeContext`: include context payloads in logs
- `json`: emit structured JSON logs
- `webhook`: optional Discord webhook forwarding

### `security`

Core security controls:

- source validation behavior
- callback cooldown and payload limits
- suspicious scoring thresholds and decay
- anomaly detection thresholds
- optional auto-block and ban-hook trigger

### `callbacks`

Callback runtime controls:

- timeout and max pending limits
- optional token requirement (`requireToken`)
- server/client rate-limit windows

### `performance`

- cache toggles and TTLs
- memoization interval
- profiling mode and thresholds
- metrics toggle

### `behavior`

Resolver/runtime behavior:

- `failOnMissingProvider`
- `useAutodetectFallback`
- `runtimeProviderSwitching`
- `softFailDomains`
- `softFailServices`
- `includeRegisteredProvidersInFallback`

## Provider selection (`config/providers.lua`)

### `providers.selected`

Primary provider per domain. This is the main control path.

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

### `providers.priority`

Ordered fallback list used if selected provider is unavailable/unhealthy.

### `providers.autodetect`

Optional fallback layer. Disabled by default and should not replace explicit `selected` values.

### `providers.health`

Provider health monitor controls:

- periodic checks
- max failure threshold
- optional disable-on-failure

## Feature toggles (`config/features.lua`)

### `features.domains`

Enable/disable entire domains (`framework`, `inventory`, `ui`, etc.).

### `features.services`

Enable/disable specific services (`callback`, `security`, etc.).

### `debug`

- `startupVerbose`
- `providerResolution`

## Fallback behavior explained

Resolver logic in practice:

1. Try selected provider.
2. If invalid/unavailable/unhealthy, try `providers.priority` order.
3. If enabled, try autodetect order.
4. If configured, include registered providers as last fallback.
5. If none work:
- with soft-fail, disable domain/service and continue startup
- without soft-fail, fail startup with explicit error

## Production modes

### `strictMode = true`

- hook fail-hard enabled
- middleware fail-hard enabled
- plugin source-name enforcement enabled
- stricter callback input checks

### `debugMode = true`

- verbose startup and resolver logging
- easier diagnostics during setup

### `performanceMode = true`

- observability enabled
- profiling enabled

### `safeMode = true`

- callback token requirement enabled
- invalid source rejection hardened
- hot-reload cleanup safety enforced

## Example profiles

### Local development

```lua
production = {
    strictMode = false,
    debugMode = true,
    performanceMode = true,
    safeMode = false
}
```

### Staging

```lua
production = {
    strictMode = true,
    debugMode = true,
    performanceMode = true,
    safeMode = true
}
```

### Production

```lua
production = {
    strictMode = true,
    debugMode = false,
    performanceMode = false,
    safeMode = true
}
```
