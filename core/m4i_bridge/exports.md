# Exports

## Usage patterns

### 1) Always treat bridge as the integration boundary

Use bridge exports from scripts instead of direct framework/inventory/UI calls.

### 2) Handle structured errors

Some exports return a third value with structured error data:

```lua
local ok, msg, err = exports.m4i_bridge:RegisterMiddleware(...)
if not ok then
    print(msg)
    if err then
        print(err.code, err.message)
    end
end
```

### 3) Use trace IDs for correlation

```lua
local traceId = exports.m4i_bridge:NewTraceId()
exports.m4i_bridge:Log("info", "my_script", "started", { traceId = traceId })
```

## Server exports

### System and API

```lua
exports.m4i_bridge:IsReady()
exports.m4i_bridge:GetApiVersion()
exports.m4i_bridge:GetApiInfo()
exports.m4i_bridge:GetProvider(domain)
exports.m4i_bridge:GetMetricsSnapshot()
exports.m4i_bridge:GetDebugState()
```

### Player and permissions

```lua
exports.m4i_bridge:GetPlayerData(sourceId)
exports.m4i_bridge:HasPermission(sourceId, permission)
exports.m4i_bridge:HasAcePermission(sourceId, permission)
```

### Inventory

```lua
exports.m4i_bridge:HasItem(sourceId, itemName, amount, metadata)
exports.m4i_bridge:CanCarryItem(sourceId, itemName, amount, metadata)
exports.m4i_bridge:AddItem(sourceId, itemName, amount, metadata, slot)
exports.m4i_bridge:RemoveItem(sourceId, itemName, amount, metadata, slot)
```

### Notify and progress

```lua
exports.m4i_bridge:NotifyPlayer(sourceId, payload)
exports.m4i_bridge:NotifyAll(payload)
exports.m4i_bridge:StartProgress(sourceId, payload)
```

### Dispatch

```lua
exports.m4i_bridge:SendDispatch(payload)
```

### Callback

```lua
exports.m4i_bridge:RegisterCallback(name, handler)
exports.m4i_bridge:UnregisterCallback(name)
exports.m4i_bridge:TriggerClientCallback(sourceId, name, args, timeoutMs)
exports.m4i_bridge:TriggerClientCallbackPromise(sourceId, name, args, timeoutMs, options)
exports.m4i_bridge:SyncCallbackToken(sourceId)
```

### Database

```lua
exports.m4i_bridge:DBScalar(query, params)
exports.m4i_bridge:DBSingle(query, params)
exports.m4i_bridge:DBQuery(query, params)
exports.m4i_bridge:DBInsert(query, params)
exports.m4i_bridge:DBUpdate(query, params)
exports.m4i_bridge:DBTransaction(queries, params)
```

### Logging

```lua
exports.m4i_bridge:Log(level, category, message, contextData)
exports.m4i_bridge:NewTraceId()
```

Legacy compatibility (deprecated, still available):

```lua
exports.m4i_bridge:LogDebug(category, message, contextData)
exports.m4i_bridge:LogInfo(category, message, contextData)
exports.m4i_bridge:LogWarn(category, message, contextData)
exports.m4i_bridge:LogError(category, message, contextData)
exports.m4i_bridge:LogFatal(category, message, contextData)
```

### Security

```lua
exports.m4i_bridge:CheckCooldown(bucket, actor, durationMs)
exports.m4i_bridge:GetSuspicionScore(sourceId)
exports.m4i_bridge:GetRiskScore(sourceId)
exports.m4i_bridge:IsSourceBlocked(sourceId)
```

### Plugin, hook, middleware, container

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

## Client exports

### System and API

```lua
exports.m4i_bridge:IsReady()
exports.m4i_bridge:GetApiVersion()
exports.m4i_bridge:GetApiInfo()
exports.m4i_bridge:GetProvider(domain)
exports.m4i_bridge:GetMetricsSnapshot()
exports.m4i_bridge:GetDebugState()
```

### Player

```lua
exports.m4i_bridge:GetPlayerData()
exports.m4i_bridge:IsLoggedIn()
```

### UI, notify, progress

```lua
exports.m4i_bridge:Notify(payload)
exports.m4i_bridge:Progress(payload)
exports.m4i_bridge:RegisterContext(contextDefinition)
exports.m4i_bridge:ShowContext(contextId)
exports.m4i_bridge:InputDialog(title, rows, options)
```

### Inventory and target

```lua
exports.m4i_bridge:HasItem(itemName, amount, metadata)
exports.m4i_bridge:GetItemCount(itemName, metadata)
exports.m4i_bridge:AddTargetBoxZone(options)
exports.m4i_bridge:RemoveTargetZone(zoneId)
```

### Dispatch and callback

```lua
exports.m4i_bridge:SendDispatch(payload)
exports.m4i_bridge:RegisterCallback(name, handler)
exports.m4i_bridge:UnregisterCallback(name)
exports.m4i_bridge:TriggerServerCallback(name, args, timeoutMs)
exports.m4i_bridge:TriggerServerCallbackPromise(name, args, timeoutMs, options)
```

### Plugin, hook, middleware, container

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
```

## Example: safe callback call

```lua
local ok, data, err, traceId = exports.m4i_bridge:TriggerServerCallback("m4i:test", { value = 42 }, 4000)
if not ok then
    print(("callback failed [%s]: %s"):format(tostring(traceId), tostring(err)))
    return
end

print("callback data", json.encode(data))
```

## Example: service resolution

```lua
local logging, err = exports.m4i_bridge:ResolveService("logging")
if logging then
    logging:info("my_script", "resolved logging service")
end
```
