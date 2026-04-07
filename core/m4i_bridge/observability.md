# Observability

## Overview

`m4i_bridge` observability combines:

- structured logging
- trace ID propagation
- metrics snapshot API
- optional profiling mode
- debug command snapshots

The goal is production insight with low default overhead.

## Logging

Logging service supports levels:

- `debug`
- `info`
- `warn`
- `error`
- `fatal`

Config:

```lua
logging = {
    level = "info",
    includeContext = true,
    json = true,
    webhook = {
        enabled = false,
        url = "",
        minLevel = "error",
        timeoutMs = 5000
    }
}
```

When `json = true`, console logs are structured JSON entries.

## Trace IDs

Generate with:

```lua
local traceId = exports.m4i_bridge:NewTraceId()
```

Use trace IDs across callback calls, logs, and hook/middleware context to correlate distributed flow.

## Metrics snapshot

Read at runtime:

```lua
local metrics = exports.m4i_bridge:GetMetricsSnapshot()
```

Snapshot includes:

- `counters`
- `gauges`
- `timers`
- `providerHealth`
- `serviceHealth`
- profiling state and entries (when enabled)

Examples of captured metric families:

- callback latency/execution
- service call/error counters
- hook execution/cancellation
- middleware execution/handler timings
- provider and service health gauges

## Profiling mode

Profiling is optional and controlled in `performance.profiling`:

```lua
performance = {
    profiling = {
        enabled = true,
        maxEntries = 200,
        slowThresholdMs = 25
    }
}
```

When enabled, snapshot contains:

- `profilingEnabled`
- `profilingSummary` (`total`, `slow`)
- `profiling` records with category/action/duration/context

Use it for performance investigations, not as permanent high-noise telemetry.

## Debug command

Use `/m4i:debug`:

- server: prints bridge runtime snapshot to console or chat output
- client: prints local runtime snapshot

Debug snapshot includes:

- provider assignments and disabled domains
- service state
- plugin count/state
- disabled provider list
- metrics summary and profiling summary

## Operational best practices

- keep default `logging.level = "info"` for production
- enable webhook only for actionable severities
- enable profiling temporarily for incident diagnosis
- include trace IDs in script-level logs
- collect debug snapshot before changing provider config
