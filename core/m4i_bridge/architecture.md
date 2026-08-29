# Architecture

## Overview

`m4i_bridge` is layered into explicit subsystems:

1. kernel lifecycle and orchestration
2. stable domain services
3. provider adapters
4. Universal Core Contract v4 framework service
5. extension runtime (plugins/hooks/middleware)
6. DI container and observability

This structure keeps gameplay business logic out of the bridge and keeps provider coupling isolated.

## Non-negotiable boundary

M4I gameplay scripts call the bridge. Provider-specific code lives in adapters.

```text
M4I Script
    |
    v
m4i_bridge
    |
    +-> m4i (m4i_core resource)
    +-> qbcore
    +-> qbox
    +-> esx
    +-> ox_core
```

The bridge does not own another framework's authoritative data/cache. It calls the provider's supported API and returns normalized results.

## Kernel

`core/kernel.lua` is the runtime orchestrator.

Responsibilities include:

- load and merge config
- validate configuration
- initialize container/metrics/hooks/middleware/plugins
- resolve providers per domain
- start services in controlled order
- maintain domain/service state and debug snapshots
- perform explicit shutdown and cleanup

## Services

Stable services include player, inventory, UI, notify, progress, target, dispatch, callback, database, logging, and security.

The additive `framework_v4` service exposes the Universal Core Contract for canonical framework operations such as identity, money, jobs, groups, duty, and metadata.

Services remain provider-agnostic and delegate provider-specific behavior to adapters.

## Adapters

Adapters live under provider/domain paths and declare metadata, dependencies, implementation state, and capabilities.

Framework adapters currently cover:

- `m4i` -> resource `m4i_core`
- `qbox`
- `qbcore`
- `esx`
- `ox_core`

The v4 adapter layer must report unsupported semantics rather than pretending all frameworks are identical.

## Resolver

`core/resolver.lua` selects providers using explicit selected-provider configuration and controlled fallback behavior.

Capabilities include:

- selected provider + priority fallback
- optional autodetect fallback
- dependency readiness checks
- health checks/failure tracking
- disable/recovery handling
- controlled runtime provider refresh

The selected provider remains the primary control. Autodetect is not a substitute for production configuration.

## M4I provider recovery

Provider `m4i` has explicit server and client recovery handling so a late `m4i_core` resource start can restore the preferred provider without requiring a bridge restart when configuration permits runtime switching.

Recovery bypasses stale fallback caches and requires the native provider to be healthy before selection.

## Data responsibility

### Provider `m4i` selected

The `m4i_core` resource owns the M4I Data Layer: authoritative in-memory state, persistence rules, financial transactions, and core data lifecycle.

### Another framework provider selected

QBCore/Qbox/ESX/Ox Core owns its own framework data architecture.

`m4i_bridge` does not maintain a competing M4I cache/write queue for that framework.

This prevents split-brain state such as a QBCore balance and an independent M4I cached balance disagreeing.

## Plugins, hooks, middleware

These extension systems are for cross-cutting integration behavior, not a place to hide provider-specific gameplay logic.

- plugins: resource-level lifecycle packages
- hooks: ordered observation/interception points
- middleware: scoped execution chains

## Observability

The bridge exposes metrics/debug state for provider health, services, timers, and optional profiling.

Performance claims should be based on these measurements and representative workload tests.

## Runtime lifecycle

### Startup

1. attach lifecycle
2. load/validate configuration
3. initialize core bridge systems
4. preflight providers
5. start services
6. auto-start plugins when enabled
7. start provider health monitoring

### Shutdown

1. stop plugins
2. stop services in reverse order
3. clear registries/runtime tables
4. reset container/metrics/hooks/middleware
5. release kernel reference

## Framework migration boundary

A configured provider change does not migrate persistent framework data automatically.

A real framework switch requires a controlled stop, database backup, identity/data migration, restart, capability validation, and rollback plan.
