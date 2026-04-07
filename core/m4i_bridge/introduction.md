# Introduction

## What is `m4i_bridge`

`m4i_bridge` is the internal integration platform for M4I FiveM resources.

It standardizes how scripts interact with:

- framework data
- inventory operations
- UI and notifications
- progress flows
- target interactions
- dispatch integrations
- callbacks
- database access
- logging and security helpers
- runtime extensibility (plugins, hooks, middleware)

Instead of each script binding directly to framework-specific APIs, scripts use one stable bridge API.

## Why it exists

FiveM stacks are often mixed (QBCore/Qbox/ESX/ox_core, ox_inventory/qb-inventory, ox_lib/qb-menu, and so on). Direct integration in every script creates:

- duplicated compatibility logic
- fragile migration paths
- inconsistent security and logging quality
- harder maintenance as servers evolve

`m4i_bridge` solves this by centralizing adapters, validation, and runtime behavior behind one contract.

## Design philosophy

`m4i_bridge` is designed around these principles:

- explicit over implicit
- modular over monolithic
- safe defaults over permissive defaults
- compatibility without hidden magic
- observability as a first-class requirement

Key guarantees:

- stable public API surface
- adapter-based provider abstraction
- strict input validation and structured errors
- centralized security and callback controls
- low-overhead observability with optional profiling

## What problems it solves

### For server owners

- switch providers with config instead of rewriting scripts
- consistent startup checks and provider health handling
- production flags for strict/safe/performance behavior

### For developers

- one predictable API for all scripts
- typed, documented exports
- plugin/hook/middleware extension model
- unified logging/trace/error model

### For the M4I team

- long-term maintainable architecture
- easier rollout of security and platform updates
- reduced drift across internal scripts

## Who should read what

- Server setup: [installation.md](installation.md) and [configuration.md](configuration.md)
- Platform internals: [architecture.md](architecture.md) and [providers.md](providers.md)
- Script integration: [script-development-guide.md](script-development-guide.md)
- Extension systems: [plugin-system.md](plugin-system.md), [hook-system.md](hook-system.md), [middleware-system.md](middleware-system.md)
- Operations: [security.md](security.md), [observability.md](observability.md), [troubleshooting.md](troubleshooting.md)
