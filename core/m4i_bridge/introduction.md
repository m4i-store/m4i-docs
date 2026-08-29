# Introduction

## What is `m4i_bridge`

`m4i_bridge` is the universal integration and compatibility boundary for M4I FiveM resources.

It standardizes how M4I scripts interact with:

- framework/player data
- money, jobs, groups, duty, metadata, and canonical character identity
- inventory operations
- UI and notifications
- progress flows
- target interactions
- dispatch integrations
- callbacks
- approved database access for script-owned persistence
- logging and security helpers
- runtime extensibility (plugins, hooks, middleware)

Instead of each M4I script binding directly to QBCore, Qbox, ESX, Ox Core, or `m4i_core`, scripts use one stable bridge API.

## What the bridge is not

`m4i_bridge` is **not** a replacement database/cache for every framework.

When QBCore/Qbox/ESX/Ox Core is selected, that provider remains responsible for its own player cache, persistence, schema, and data behavior.

There is no M4I Data Proxy layered over another framework.

When `m4i_core` is selected, the native M4I Data Layer lives inside `m4i_core`, behind the same bridge boundary.

## Why it exists

FiveM stacks are often mixed. Direct integration in every script creates:

- duplicated framework compatibility code
- fragile migration paths
- inconsistent security/logging behavior
- framework lock-in
- harder maintenance as the server evolves

`m4i_bridge` centralizes adapters, validation, capability reporting, callbacks, security, and provider resolution behind one contract.

## Framework portability

The additive Universal Core Contract v4 allows M4I-owned scripts to use normalized framework operations such as:

- canonical `characterId`
- money reads/mutations
- job and duty
- metadata
- groups
- capability reporting

Supported framework provider targets include:

- `m4i` (`m4i_core` resource)
- `qbox`
- `qbcore`
- `esx`
- `ox_core`

Provider semantics are not assumed to be identical. Unsupported behavior must fail explicitly rather than be silently faked.

## Design philosophy

- explicit over implicit
- modular over monolithic
- safe defaults over permissive defaults
- compatibility without hidden data ownership
- capability reporting instead of false equivalence
- observability as a first-class requirement

## M4I script rule

M4I-owned gameplay scripts depend on `m4i_bridge`.

If a needed framework capability is missing, extend the bridge contract/adapter instead of importing a concrete framework inside gameplay business logic.

## Read next

- [Architecture](architecture.md)
- [Providers](providers.md)
- [Universal Core Contract v4](universal-core-contract-v4.md)
- [Exports](exports.md)
- [Script Development Guide](script-development-guide.md)
- [M4I Data Access Policy](../../shared/data-access-policy.md)
