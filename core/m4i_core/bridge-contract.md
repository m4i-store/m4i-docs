# m4i_core Bridge Contract

## Contract direction

The FiveM resource `m4i_core` implements framework provider `m4i` and exposes the provider surface that `m4i_bridge` consumes.

M4I gameplay scripts should consume the **bridge** contract, not this provider surface directly.

```text
M4I gameplay script -> m4i_bridge -> provider m4i -> m4i_core resource
```

## Universal Core Contract

Current additive bridge contract version:

```text
4.0.0-alpha.1
```

The native provider key and resource name are different:

```text
provider key: m4i
resource:     m4i_core
```

## Required server provider surface

The current native adapter expects core functionality including:

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

`GetPlayerData` is part of the required normalized surface. A resource that exposes only `GetPlayer` must not be treated as a healthy native M4I provider.

`IsReady()` must return `true` before the bridge advertises provider `m4i` as ready.

## Additional native core exports

`m4i_core` also exposes native operational helpers such as:

```lua
GetVersion()
GetStress(sourceId)
SavePlayer(sourceId, force)
SaveAll(force)
LinkProviderIdentity(sourceId, providerName, externalId)
GetMetricsSnapshot()
```

These are core/provider APIs. M4I gameplay resources should use bridge abstractions when a bridge contract exists.

## Client compatibility surface

The current client core exposes:

```lua
GetPlayerData()
IsLoggedIn()
GetCharacterId()
GetStatus(statusName?)
```

The owning client receives its snapshot through targeted events. Sensitive full player data is not intended to be globally replicated to other clients.

## Money operation IDs

Provider `m4i`, implemented by `m4i_core`, supports durable idempotent money operation IDs.

A stable operation ID may be supplied to:

```lua
AddMoney(..., operationId)
RemoveMoney(..., operationId)
SetMoney(..., operationId)
```

Replaying the same committed operation must not apply the money mutation a second time.

Reusing an operation ID for a conflicting operation must fail rather than silently applying a different mutation.

## Capability reporting

M4I scripts that need provider-dependent semantics can inspect:

```lua
local info = exports.m4i_bridge:GetFrameworkCapabilities()
```

Do not infer a capability merely from the selected provider name. Use the reported capability contract when behavior is provider-dependent.

## Data ownership

When bridge provider `m4i` is selected, core-owned player data belongs to the implementing `m4i_core` resource.

M4I gameplay scripts must not update native `m4i_*` core tables directly. Use bridge exports so the in-memory state, persistence rules, events, idempotency, and security remain consistent.
