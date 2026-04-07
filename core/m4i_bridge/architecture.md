# Architecture

## Overview

`m4i_bridge` is layered into explicit subsystems:

1. kernel lifecycle and orchestration
2. domain services
3. provider adapters
4. extension runtime (plugins/hooks/middleware)
5. DI container and observability

This structure keeps game business logic out of the bridge and keeps provider coupling isolated.

## Kernel

`core/kernel.lua` is the runtime orchestrator.

Responsibilities:

- load and merge config
- apply production flags
- validate configuration
- initialize core systems (container, metrics, hooks, middleware, plugins)
- resolve providers per domain
- start services in controlled order
- maintain domain/service state and debug snapshot
- perform explicit shutdown and cleanup

Startup order is deterministic (`logging` first, then security/callback/database, then gameplay-facing services).

## Services

Services expose bridge behavior with stable contracts. Current service modules:

- `player`
- `inventory`
- `ui`
- `notify`
- `progress`
- `target`
- `dispatch`
- `callback`
- `database`
- `logging`
- `security`

Services call adapters for provider-specific logic and should remain provider-agnostic.

## Adapters

Adapters live under `adapters/<domain>/<provider>/<side>.lua`.

Each adapter provides domain contract methods (validated by `shared/types.lua` + `core/validator.lua`).

Adapter metadata includes:

- provider identity
- implementation state
- dependencies

This allows validation and health-aware resolution without hardcoding provider APIs in services.

## Resolver

`core/resolver.lua` selects providers at runtime.

Capabilities:

- selected provider + priority fallback
- optional autodetect fallback
- dependency readiness checks
- health checks and failure tracking
- disable unhealthy providers after threshold
- soft-fail aware behavior

The resolver is runtime-switch safe when configured (`behavior.runtimeProviderSwitching = true`).

## Plugins, hooks, and middleware

### Plugins (`core/plugins.lua`)

- safe registry with unique names
- validation and metadata tracking
- lifecycle: `init`, `start`, `stop`
- owner-aware cleanup on resource stop

### Hooks (`core/hooks.lua`)

- named events
- priority ordering
- before/after patterns
- cancellation and payload mutation
- soft or fail-hard execution behavior

### Middleware (`core/middleware.lua`)

- scoped execution chains
- `next()` flow control
- context-based action shaping
- cancellation and error handling

## DI container

`core/container.lua` provides a simple explicit container:

- register factory/value
- resolve dependencies lazily
- singleton support
- circular dependency detection

The kernel registers core components into the container and exposes service resolution through exports.

## Observability

`core/metrics.lua` captures runtime telemetry:

- counters
- gauges
- timer observations
- provider/service health snapshots
- optional profiling entries and slow-call summary

`logging` service adds structured logs and trace IDs for correlation.

## Runtime lifecycle

### Startup

1. lifecycle attaches (`core/lifecycle.lua`)
2. kernel loads/validates config
3. core systems initialize
4. providers preflight
5. services start
6. plugins auto-start (if enabled)
7. provider health monitor starts

### Shutdown

1. plugins stop
2. services stop in reverse order
3. registries and runtime tables clear
4. container/metrics/hooks/middleware reset
5. kernel reference released

### Hot-reload safety foundation

On external resource stop, bridge can clean owner-bound plugins/hooks/middleware to avoid orphaned registrations.

This is a practical safety baseline, not a claim of full state migration across arbitrary external resources.
