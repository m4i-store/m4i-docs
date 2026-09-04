# Exports

## Integration rule

M4I gameplay resources should use `m4i_bridge` exports instead of direct framework/provider calls.

For core/framework state, prefer Universal Core Contract v4 when the capability exists. For shared catalog definitions, use the read-only definition registry surface below.

## System / API

Server and client expose platform/runtime helpers such as:

```lua
exports.m4i_bridge:IsReady()
exports.m4i_bridge:GetApiVersion()
exports.m4i_bridge:GetApiInfo()
exports.m4i_bridge:GetProvider(domain)
exports.m4i_bridge:GetMetricsSnapshot()
exports.m4i_bridge:GetDebugState()
```

## Canonical definition registry — server read-only

When `m4i_registry` is installed/ready, server-side M4I gameplay resources can resolve canonical definitions through Bridge without depending directly on Registry implementation details.

```lua
exports.m4i_bridge:GetDefinitionRegistryState()
exports.m4i_bridge:GetDefinition(domain, key, includeDisabled)
exports.m4i_bridge:ResolveDefinition(domain, keyOrAlias, includeDisabled)
exports.m4i_bridge:ResolveDefinitionKey(domain, keyOrAlias)
exports.m4i_bridge:ListDefinitions(domain, options)
```

Convenience exports:

```lua
exports.m4i_bridge:GetItemDefinition(key, includeDisabled)
exports.m4i_bridge:GetJobDefinition(key, includeDisabled)
exports.m4i_bridge:GetGangDefinition(key, includeDisabled)
exports.m4i_bridge:GetGroupDefinition(key, includeDisabled)
exports.m4i_bridge:GetVehicleDefinition(key, includeDisabled)
exports.m4i_bridge:GetWeaponDefinition(key, includeDisabled)
exports.m4i_bridge:GetLocationDefinition(key, includeDisabled)
```

Current canonical Registry domains are:

```text
item
job
gang
group
vehicle
weapon
location
```

Example:

```lua
local job, err = exports.m4i_bridge:GetJobDefinition("police")
if not job then
    -- unavailable registry / missing definition / disabled definition
    return
end

print(job.payload.label)
```

Registry state example:

```lua
local state = exports.m4i_bridge:GetDefinitionRegistryState()
if state.ready then
    print(state.version, state.generation)
end
```

Live definition changes are forwarded as server event:

```text
m4i_bridge:server:definitionChanged
```

and registry-ready as:

```text
m4i_bridge:server:definitionRegistryReady
```

Bridge only forwards trusted Registry-origin lifecycle hints and reuses the read-only Registry export surface. Gameplay Bridge exposes **no** `PutEntry`, delete, rollback, alias mutation or Smart Import write path.

For native M4I, `m4i_core` itself consumes job/gang/group definitions directly from `m4i_registry`; gameplay scripts should still prefer Bridge.

## Universal Core Contract v4 — server

Current additive contract version:

```lua
exports.m4i_bridge:GetFrameworkContractVersion()
exports.m4i_bridge:GetFrameworkCapabilities()
```

### Canonical identity

```lua
exports.m4i_bridge:GetCharacterId(sourceId)
```

### Money

```lua
exports.m4i_bridge:GetMoney(sourceId, account)
exports.m4i_bridge:AddMoney(sourceId, account, amount, reason, operationId)
exports.m4i_bridge:RemoveMoney(sourceId, account, amount, reason, operationId)
exports.m4i_bridge:SetMoney(sourceId, account, amount, reason, operationId)
```

`operationId` is optional at the call site but must only be used when the provider capability supports durable idempotency. Bridge does not silently discard an operation ID.

### Jobs / duty

```lua
exports.m4i_bridge:GetJob(sourceId)
exports.m4i_bridge:SetJob(sourceId, jobName, grade)
exports.m4i_bridge:SetDuty(sourceId, onDuty)
```

In native provider `m4i`, `SetJob` validates the canonical job/grade against `m4i_registry`; Core persists only membership/runtime state.

### Metadata / groups

```lua
exports.m4i_bridge:GetMetadata(sourceId, key)
exports.m4i_bridge:SetMetadata(sourceId, key, value)
exports.m4i_bridge:GetGroups(sourceId)
```

See [Universal Core Contract v4](universal-core-contract-v4.md) for provider-dependent semantics.

## Native M4I Data Layer — server

These are **native-only** capabilities, available only when selected framework provider is `m4i` and `m4i_core` exposes the healthy Data Layer contract.

```lua
exports.m4i_bridge:GetPlayerSnapshot(sourceId, fields)
exports.m4i_bridge:GetPlayersSnapshot(fields, limit)
exports.m4i_bridge:GetDataLayerState()
exports.m4i_bridge:SubscribeData(topic, handler)
exports.m4i_bridge:UnsubscribeData(token)
```

Check capabilities first:

```lua
local info = exports.m4i_bridge:GetFrameworkCapabilities()
local caps = info and info.capabilities or {}

if caps.nativeDataLayer and caps.playerSnapshot then
    local snapshot = exports.m4i_bridge:GetPlayerSnapshot(sourceId, {
        "accounts",
        "job",
        "status"
    })
end
```

Native Data Layer flags include:

```text
nativeDataLayer
playerSnapshot
bulkPlayerSnapshot
dataLayerState
dataSubscriptions
```

For `qbox`, `qbcore`, `esx` and `ox_core`, these capabilities are false/unsupported. Bridge does **not** emulate them with a Data Proxy/cache/write queue above another framework.

### Snapshot example

```lua
local snapshot, err = exports.m4i_bridge:GetPlayerSnapshot(sourceId, {
    "identity",
    "account:cash",
    "job",
    "metadata:phone",
    "status:hunger"
})
```

### Subscription example

```lua
local token, err = exports.m4i_bridge:SubscribeData("status.changed", function(sourceId, payload, meta)
    -- ordinary player-scoped source is session-safe
end)
```

Release the token when no longer needed:

```lua
exports.m4i_bridge:UnsubscribeData(token)
```

Ownership is tied to the invoking gameplay resource. Bridge delegates the real owner to Core so per-resource caps and stop cleanup remain correct.

For terminal `player.unloaded`, primary `sourceId` is intentionally `nil`; historical source/stable identity remain in metadata/payload.

## Player compatibility exports — server

```lua
exports.m4i_bridge:GetPlayerData(sourceId)
exports.m4i_bridge:GetIdentifier(sourceId)
exports.m4i_bridge:GetJobName(sourceId)
exports.m4i_bridge:GetJobLabel(sourceId)
exports.m4i_bridge:GetPlayers()
exports.m4i_bridge:GetOnlinePlayerCount()
exports.m4i_bridge:GetStatus(sourceId, statusName)
exports.m4i_bridge:GetStress(sourceId)
exports.m4i_bridge:UpdateStress(sourceId, value)
exports.m4i_bridge:IsAdmin(sourceId)
exports.m4i_bridge:HasPermission(sourceId, permission)
exports.m4i_bridge:HasAcePermission(sourceId, permission)
```

## Inventory — server

```lua
exports.m4i_bridge:HasItem(sourceId, itemName, amount, metadata)
exports.m4i_bridge:CanCarryItem(sourceId, itemName, amount, metadata)
exports.m4i_bridge:AddItem(sourceId, itemName, amount, metadata, slot)
exports.m4i_bridge:RemoveItem(sourceId, itemName, amount, metadata, slot)
```

Inventory runtime/quantity remains owned by the selected inventory provider. Canonical item definitions can be read from Registry, but current Bridge inventory adapters do not imply every provider can hot-materialize newly created items/images without provider-specific support.

## Notify / progress / dispatch — server

```lua
exports.m4i_bridge:NotifyPlayer(sourceId, payload)
exports.m4i_bridge:NotifyAll(payload)
exports.m4i_bridge:StartProgress(sourceId, payload)
exports.m4i_bridge:SendDispatch(payload)
```

## Callbacks — server

```lua
exports.m4i_bridge:RegisterCallback(name, handler)
exports.m4i_bridge:UnregisterCallback(name)
exports.m4i_bridge:TriggerClientCallback(sourceId, name, args, timeoutMs)
exports.m4i_bridge:TriggerClientCallbackPromise(sourceId, name, args, timeoutMs, options)
exports.m4i_bridge:TriggerClientCallbackAsync(sourceId, name, args, timeoutMs, completion, options)
exports.m4i_bridge:SyncCallbackToken(sourceId)
```

## Database — server

```lua
exports.m4i_bridge:DBScalar(query, params)
exports.m4i_bridge:DBSingle(query, params)
exports.m4i_bridge:DBQuery(query, params)
exports.m4i_bridge:DBInsert(query, params)
exports.m4i_bridge:DBUpdate(query, params)
exports.m4i_bridge:DBTransaction(queries, params)
```

These exports are for approved script-owned persistence.

**Do not use them to mutate Core/framework/Registry-owned player, money, membership, identity, or canonical-definition tables.** Use the appropriate Bridge/Core/Registry contract.

See [M4I Data Access Policy](../../shared/data-access-policy.md).

## Logging — server

```lua
exports.m4i_bridge:Log(level, category, message, contextData)
exports.m4i_bridge:NewTraceId()
```

Deprecated compatibility helpers remain available for older scripts:

```lua
exports.m4i_bridge:LogDebug(...)
exports.m4i_bridge:LogInfo(...)
exports.m4i_bridge:LogWarn(...)
exports.m4i_bridge:LogError(...)
exports.m4i_bridge:LogFatal(...)
```

## Security — server

```lua
exports.m4i_bridge:CheckCooldown(bucket, actor, durationMs)
exports.m4i_bridge:GetSuspicionScore(sourceId)
exports.m4i_bridge:GetRiskScore(sourceId)
exports.m4i_bridge:IsSourceBlocked(sourceId)
```

## Plugin / hook / middleware / container — server

```lua
exports.m4i_bridge:RegisterPlugin(pluginDefinition)
exports.m4i_bridge:UnregisterPlugin(pluginName)
exports.m4i_bridge:ListPlugins()
exports.m4i_bridge:GetPluginState(pluginName)

exports.m4i_bridge:RegisterHook(eventName, handler, options)
exports.m4i_bridge:UnregisterHook(eventName, hookId)
exports.m4i_bridge:GetHookState(eventName)

exports.m4i_bridge:RegisterMiddleware(scope, name, handler, options)
exports.m4i_bridge:UnregisterMiddleware(scope, name)
exports.m4i_bridge:GetMiddlewareState(scope)

exports.m4i_bridge:ResolveService(name, options)
```

## Client player exports

```lua
exports.m4i_bridge:GetPlayerData()
exports.m4i_bridge:IsLoggedIn()
```

## Client UI / inventory / target / dispatch

```lua
exports.m4i_bridge:Notify(payload)
exports.m4i_bridge:Progress(payload)
exports.m4i_bridge:RegisterContext(contextDefinition)
exports.m4i_bridge:ShowContext(contextId)
exports.m4i_bridge:InputDialog(title, rows, options)

exports.m4i_bridge:HasItem(itemName, amount, metadata)
exports.m4i_bridge:GetItemCount(itemName, metadata)
exports.m4i_bridge:AddTargetBoxZone(options)
exports.m4i_bridge:RemoveTargetZone(zoneId)
exports.m4i_bridge:SendDispatch(payload)
```

## Client callbacks

```lua
exports.m4i_bridge:RegisterCallback(name, handler)
exports.m4i_bridge:UnregisterCallback(name)
exports.m4i_bridge:TriggerServerCallback(name, args, timeoutMs)
exports.m4i_bridge:TriggerServerCallbackPromise(name, args, timeoutMs, options)
exports.m4i_bridge:TriggerServerCallbackAsync(name, args, timeoutMs, completion, options)
```

## Client extensions / observability

```lua
exports.m4i_bridge:RegisterPlugin(pluginDefinition)
exports.m4i_bridge:UnregisterPlugin(pluginName)
exports.m4i_bridge:ListPlugins()
exports.m4i_bridge:GetPluginState(pluginName)

exports.m4i_bridge:RegisterHook(eventName, handler, options)
exports.m4i_bridge:UnregisterHook(eventName, hookId)
exports.m4i_bridge:GetHookState(eventName)

exports.m4i_bridge:RegisterMiddleware(scope, name, handler, options)
exports.m4i_bridge:UnregisterMiddleware(scope, name)
exports.m4i_bridge:GetMiddlewareState(scope)

exports.m4i_bridge:ResolveService(name, options)
exports.m4i_bridge:NewTraceId()
exports.m4i_bridge:GetMetricsSnapshot()
exports.m4i_bridge:GetDebugState()
```

## Error handling

Always handle explicit `nil/false, reason` results for provider-dependent operations.

Do not assume an unsupported provider capability will be emulated.
