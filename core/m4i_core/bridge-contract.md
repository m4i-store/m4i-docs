# m4i_core Bridge Contract

## Contract direction

The FiveM resource `m4i_core` implements framework provider `m4i` and exposes the native provider surface consumed by `m4i_bridge`.

M4I gameplay scripts should consume the **bridge** contract, not call the provider/core surface directly.

```text
M4I gameplay script -> m4i_bridge -> provider m4i -> m4i_core resource
```

## Universal Core Contract

Current additive bridge contract version:

```text
4.0.0-alpha.1
```

Provider key and resource name are intentionally different:

```text
provider key: m4i
resource:     m4i_core
```

## Required server provider surface

The native framework adapter expects core functionality including:

```lua
IsReady()
GetPlayer(sourceId)
GetPlayerData(sourceId)
GetPlayers()
GetOnlinePlayerCount()
GetIdentifier(sourceId)
HasPermission(sourceId, permission)
IsAdmin(sourceId)
GetStatus(sourceId, statusName)
SetStatus(sourceId, statusName, value)

GetCharacterId(sourceId)
GetMoney(sourceId, account)
AddMoney(sourceId, account, amount, reason, operationId?)
RemoveMoney(sourceId, account, amount, reason, operationId?)
SetMoney(sourceId, account, amount, reason, operationId?)
GetJob(sourceId)
SetJob(sourceId, jobName, grade)
SetDuty(sourceId, onDuty)
GetMetadata(sourceId, key)
SetMetadata(sourceId, key, value)
GetGroups(sourceId)
```

`GetPlayerData` is part of the required normalized surface. A resource exposing only `GetPlayer` must not be treated as a healthy native M4I provider.

`IsReady()` must return `true` before the bridge advertises provider `m4i` as ready.

## Native Data Layer contract

When provider `m4i` is active and the current `m4i_core` Data Layer is available, the bridge can expose the native-only data capabilities:

```lua
GetPlayerSnapshot(sourceId, fields)
GetPlayersSnapshot(fields, limit)
GetDataLayerState()
SubscribeData(topic, handler, ownerOverride?)
UnsubscribeData(token, ownerOverride?)
```

The public gameplay-facing form remains the `m4i_bridge` exports. `ownerOverride` is an internal trusted delegation mechanism between `m4i_bridge` and `m4i_core`; gameplay resources must not use it to impersonate another resource.

### Trusted subscription owner delegation

A gameplay resource subscribing through `m4i_bridge` must remain the effective owner inside Core so that per-resource limits and lifecycle cleanup are accurate.

Core therefore accepts a delegated owner only when `GetInvokingResource()` is exactly:

```text
m4i_bridge
```

Rules:

- direct Core callers retain their own invoking-resource ownership
- non-bridge owner spoofing is rejected
- delegated subscribe requires a valid running/starting gameplay resource
- delegated unsubscribe remains possible during owner shutdown
- gameplay-owner stop removes its delegated subscriptions
- `m4i_bridge` stop/crash removes all outstanding delegated subscription references
- owner-driven direct unsubscribe also clears delegation bookkeeping

This bookkeeping is bounded and is not a general cross-resource impersonation API.

## Native Data Layer capability reporting

`m4i_bridge:GetFrameworkCapabilities()` may report these native-only capability flags:

```text
nativeDataLayer
playerSnapshot
bulkPlayerSnapshot
dataLayerState
dataSubscriptions
```

They are true only when the selected framework provider is `m4i` and the required `m4i_core` exports are healthy.

For QBCore, Qbox, ESX and Ox Core these capabilities are explicitly unsupported/false. The bridge does not emulate them with a Data Proxy.

## Additional native core exports

`m4i_core` also exposes operational helpers such as:

```lua
GetVersion()
GetStress(sourceId)
SavePlayer(sourceId, force)
SaveAll(force)
LinkProviderIdentity(sourceId, providerName, externalId)
GetMetricsSnapshot()
```

These are core/provider APIs. Gameplay resources should use bridge abstractions whenever a bridge contract exists.

## Client compatibility surface

The current client core exposes:

```lua
GetPlayerData()
IsLoggedIn()
GetCharacterId()
GetStatus(statusName?)
```

The owning client receives its state through targeted events. Sensitive full player data is not intended to be globally replicated to other clients.

## Money operation IDs

Provider `m4i`, implemented by `m4i_core`, supports durable idempotent money operation IDs.

A stable operation ID may be supplied to:

```lua
AddMoney(..., operationId)
RemoveMoney(..., operationId)
SetMoney(..., operationId)
```

Replaying the same committed operation must not apply the mutation twice.

Reusing an operation ID for a conflicting operation must fail rather than silently applying a different mutation.

## Capability reporting rule

M4I scripts needing provider-dependent semantics should inspect:

```lua
local info = exports.m4i_bridge:GetFrameworkCapabilities()
```

Do not infer a capability from provider name alone. Check the reported capability contract and handle explicit unsupported results.

## Data ownership

When provider `m4i` is selected, core-owned player data belongs to `m4i_core` and its native Data Layer.

M4I gameplay scripts must not update native `m4i_*` core tables directly. Use bridge exports so authoritative RAM state, persistence rules, events, idempotency and security remain consistent.

When another framework provider is selected, that framework owns its own data/cache/persistence. There is no M4I Data Proxy above it.
