# Exports

## Integration rule

M4I gameplay resources should use `m4i_bridge` exports instead of direct framework/provider calls.

For core/framework state, prefer the Universal Core Contract v4 exports when the capability exists.

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

`operationId` is optional at the call site but must only be used when the provider capability supports durable idempotency. The bridge does not silently discard an operation ID.

### Jobs / duty

```lua
exports.m4i_bridge:GetJob(sourceId)
exports.m4i_bridge:SetJob(sourceId, jobName, grade)
exports.m4i_bridge:SetDuty(sourceId, onDuty)
```

### Metadata / groups

```lua
exports.m4i_bridge:GetMetadata(sourceId, key)
exports.m4i_bridge:SetMetadata(sourceId, key, value)
exports.m4i_bridge:GetGroups(sourceId)
```

See [Universal Core Contract v4](universal-core-contract-v4.md) for provider-dependent semantics.

## Native M4I Data Layer — server

These exports are **native-only capabilities**. They are available only when the selected framework provider is `m4i` and the implementing `m4i_core` resource exposes the healthy Data Layer contract.

```lua
exports.m4i_bridge:GetPlayerSnapshot(sourceId, fields)
exports.m4i_bridge:GetPlayersSnapshot(fields, limit)
exports.m4i_bridge:GetDataLayerState()
exports.m4i_bridge:SubscribeData(topic, handler)
exports.m4i_bridge:UnsubscribeData(token)
```

Check capability flags first:

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

For `qbox`, `qbcore`, `esx` and `ox_core`, these capabilities are false/unsupported. `m4i_bridge` does **not** emulate them with a cache/Data Proxy/write queue above another framework.

### Snapshot example

```lua
local snapshot, err = exports.m4i_bridge:GetPlayerSnapshot(sourceId, {
    "identity",
    "account:cash",
    "job",
    "metadata:phone",
    "status:hunger"
})

if not snapshot then
    -- Handle unsupported provider / unavailable player / validation error.
end
```

### Subscription example

```lua
local token, err = exports.m4i_bridge:SubscribeData("status.changed", function(sourceId, payload, meta)
    -- sourceId is session-safe for ordinary player-scoped events.
    -- Use meta.characterId/sessionGeneration when lifecycle identity matters.
end)
```

Keep the token and release it when no longer needed:

```lua
exports.m4i_bridge:UnsubscribeData(token)
```

Ownership is tied to the invoking gameplay resource. The bridge delegates that real owner to `m4i_core` so Core per-resource caps and resource-stop cleanup remain correct.

For terminal `player.unloaded`, the primary `sourceId` is intentionally `nil`; historical source and stable identity remain in `meta`/payload so cleanup code cannot target a replacement session.

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

These compatibility helpers remain available alongside v4.

## Inventory — server

```lua
exports.m4i_bridge:HasItem(sourceId, itemName, amount, metadata)
exports.m4i_bridge:CanCarryItem(sourceId, itemName, amount, metadata)
exports.m4i_bridge:AddItem(sourceId, itemName, amount, metadata, slot)
exports.m4i_bridge:RemoveItem(sourceId, itemName, amount, metadata, slot)
```

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

**Do not use them to mutate core/framework-owned player, money, job, group, or identity tables.** Use the framework/core bridge contracts instead so provider memory and persistence cannot diverge.

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

The selected framework client adapter is responsible for normalized client state. M4I scripts should not infer the active framework from returned data.

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

The extension systems are available on the client as well:

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
