# Script Development Guide

## Purpose

This guide defines the required development standard for M4I-owned gameplay scripts.

The goal is one script codebase that can run against supported framework providers through `m4i_bridge`, while keeping M4I-native data behavior centralized in `m4i_core` when that provider is selected.

## Non-negotiable rules

- NEVER call QBCore/Qbox/ESX/Ox Core APIs directly from M4I gameplay business logic.
- NEVER call `m4i_core` directly from M4I gameplay business logic when a bridge contract exists.
- NEVER call inventory/UI/target providers directly when bridge abstraction exists.
- ALWAYS use `m4i_bridge` as the compatibility boundary.
- NEVER mutate core/framework-owned player data with direct SQL.
- A missing capability is a platform-contract problem; extend the bridge/adapter instead of bypassing it.

## Framework-neutral example

Preferred:

```lua
local characterId = exports.m4i_bridge:GetCharacterId(source)
local cash, err = exports.m4i_bridge:GetMoney(source, "cash")
local job = exports.m4i_bridge:GetJob(source)
```

Forbidden:

```lua
local QBCore = exports['qb-core']:GetCoreObject()
local player = exports.qbx_core:GetPlayer(source)
local cash = exports.m4i_core:GetMoney(source, "cash")
```

## Recommended resource structure

```text
my_script/
  fxmanifest.lua
  shared/
    config.lua
  server/
    main.lua
    services/
      data_service.lua
      webhook_service.lua
  client/
    main.lua
    ui.lua
  sql/
```

The script should depend on `m4i_bridge` and start after it.

## Startup

1. verify bridge readiness before provider-facing boot work
2. register callbacks/hooks/middleware during resource start when required
3. keep initialization idempotent
4. log startup with meaningful context

## Runtime integration

- use bridge exports for framework/inventory/UI/target/dispatch behavior
- validate all external/client input before side effects
- use structured callback responses
- handle unsupported provider capabilities explicitly
- do not infer framework identity from a returned data shape

## Universal Core Contract v4

For portable framework state, use v4 contracts where appropriate:

```lua
GetFrameworkCapabilities
GetCharacterId
GetMoney / AddMoney / RemoveMoney / SetMoney
GetJob / SetJob / SetDuty
GetMetadata / SetMetadata
GetGroups
```

Before depending on provider-specific semantics such as duty or idempotent money, inspect capability reporting.

## Money rules

Money is security- and persistence-sensitive.

- validate the server-side reason/context
- use a stable operation ID for retryable financial actions when the provider advertises durable idempotency
- never update a framework balance table directly
- never trust a client-supplied resulting balance
- treat `false/nil, reason` as a real failure

Example:

```lua
local caps = exports.m4i_bridge:GetFrameworkCapabilities()
local operationId = ("my_script:reward:%s"):format(rewardId)

if caps.ready and caps.capabilities and caps.capabilities.idempotentMoney then
    local ok, err = exports.m4i_bridge:AddMoney(source, "bank", 500, "mission_reward", operationId)
    if not ok then
        return false, err
    end
else
    -- Decide an approved non-retryable behavior for this provider.
end
```

## Data access rules

### Core/framework-owned state

Read/mutate through bridge contracts.

Do not issue SQL against provider/core player, money, job, group, identity, or metadata tables.

### Script-owned persistence

A script may own dedicated tables for its own business domain.

Use the bridge database service/exports and keep SQL inside a clear data/repository service rather than scattering it across gameplay files.

### Do not poll unchanged state

Avoid short loops that repeatedly request money/job/status merely to detect changes.

Prefer:

- initial read
- platform/domain change event
- explicit refresh when the feature actually needs it

If many scripts need the same missing event or snapshot API, extend the shared platform instead of creating duplicate polling implementations.

See [M4I Data Access Policy](../../shared/data-access-policy.md).

## Bulk reads

Do not create thousands of repeated fine-grained calls when a bounded snapshot/bulk contract can express the requirement better.

If a needed snapshot API is not yet part of the bridge/core, propose it as a platform feature. Do not bypass the architecture with direct provider access.

## Callbacks

- namespace callback names (`my_script:action`)
- validate source and payload server-side
- return structured `success/reason/data`
- handle timeout/error branches
- keep handlers bounded and deterministic
- use bridge callback channels for sensitive request/response flows

## Logging

Use structured bridge logging:

```lua
local traceId = exports.m4i_bridge:NewTraceId()
exports.m4i_bridge:Log("info", "my_script", "flow started", {
    source = source,
    traceId = traceId
})
```

Use trace IDs for multi-step actions where correlation matters.

## Security

- authority lives on the server
- validate item/money/job/permission requirements on the server
- use cooldown/rate-limit controls for spam-sensitive actions
- do not expose raw DB mutation through client events
- do not trust client-supplied identity, amount, price, permission, or ownership state

## Provider behavior

When provider = `m4i`, framework calls reach `m4i_core` and benefit from native M4I data behavior.

When provider = QBCore/Qbox/ESX/Ox Core, the bridge calls that provider's APIs and that provider owns its data architecture. M4I does not add a second player-data source of truth.

## Third-party resources

A framework-native third-party resource is not automatically an M4I-native script.

It may need:

- a reverse compatibility shim
- source patch
- migration adapter
- replacement

Hard-coded provider SQL/private internals require special review.

## Release checklist

Before releasing an M4I script:

1. no direct framework/core/provider calls in gameplay business logic
2. no direct SQL to core/framework-owned state
3. external inputs validated
4. financial operations use approved server-authoritative flow
5. callbacks handle timeout/error
6. polling avoided where event-driven behavior is possible
7. bridge capabilities handled explicitly
8. script-owned SQL isolated in a data service
9. logs/trace IDs exist for critical flows
10. tested against every provider claimed as supported
11. resource restart and provider-unavailable behavior tested
12. documentation updated in `m4i-docs`
