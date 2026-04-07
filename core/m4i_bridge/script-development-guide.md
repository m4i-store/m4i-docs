# Script Development Guide

## Purpose

This guide defines the required development standard for all scripts built on `m4i_bridge`.

## Non-negotiable rules

- NEVER call framework APIs directly from script business logic.
- NEVER call inventory provider APIs directly.
- ALWAYS consume bridge exports for integrations.
- ALWAYS treat bridge as your compatibility/security boundary.

If a needed capability is missing, extend bridge contracts first instead of bypassing bridge.

## Recommended script structure

```text
my_script/
  fxmanifest.lua
  shared/
    config.lua
  server/
    main.lua
    callbacks.lua
  client/
    main.lua
    ui.lua
```

`my_script` should depend on `m4i_bridge` and start after it.

## Integration lifecycle

### Startup

1. ensure bridge is started before script boot logic
2. register callbacks/hooks/middleware during resource start
3. log startup with trace context for diagnostics

### Runtime

- use exports for all provider-facing actions
- pass structured tables through callbacks
- enforce script-level permissions and validation before side effects

### Shutdown

- unregister callbacks/hooks/middleware if your script created persistent bindings
- keep cleanup idempotent

## Logging rules

- use `exports.m4i_bridge:Log(...)` for structured logs
- include meaningful `category` values per script area
- include trace IDs on multi-step flows

Example:

```lua
local traceId = exports.m4i_bridge:NewTraceId()
exports.m4i_bridge:Log("info", "my_script", "starting flow", {
    traceId = traceId,
    action = "open_menu"
})
```

## Security rules

- validate all external input before callback or DB actions
- use bridge callback channel instead of ad-hoc sensitive net events
- use `CheckCooldown` where user-triggered actions can be spammed
- review suspicion-related logs for abuse patterns

## Callback rules

- register callback names with clear namespace (`my_script:action`)
- return structured response payloads (`success`, `reason`, `data`)
- handle timeout and error branches on caller side
- keep callback handlers fast and deterministic

Server callback example:

```lua
exports.m4i_bridge:RegisterCallback("my_script:get_status", function(source)
    if not exports.m4i_bridge:HasPermission(source, "my_script.use") then
        return {
            success = false,
            reason = "no_permission"
        }
    end

    return {
        success = true,
        data = {
            online = true
        }
    }
end)
```

Client callback call example:

```lua
local ok, response, err, traceId = exports.m4i_bridge:TriggerServerCallback(
    "my_script:get_status",
    {},
    5000
)

if not ok then
    print(("status callback failed [%s]: %s"):format(tostring(traceId), tostring(err)))
    return
end

if response and response.success then
    print("status online", response.data and response.data.online)
end
```

## Database and state access

- use bridge DB exports only (`DBQuery`, `DBSingle`, etc.)
- keep SQL and schema logic inside your script, but connection access through bridge
- never expose raw DB operations through unsecured client events

## Plugin/hook/middleware integration flow

Use these systems only for cross-cutting concerns:

- plugin: resource-level integration package
- hook: event interception/observation
- middleware: scoped pipeline logic

Do not put business gameplay logic into generic middleware/hooks when direct script code is clearer.

## Do / Don't

### Do

- use bridge exports for framework/inventory/ui/dispatch access
- validate payloads before actions
- log with category and trace IDs
- handle structured errors
- keep callback handlers small and predictable

### Don't

- call `QBCore`, `ESX`, `ox_inventory`, `ox_lib` directly in script business layer
- bypass bridge security for convenience
- rely on fallback behavior as primary configuration strategy
- ignore timeout/error branches in callback calls

## Example server flow (end-to-end)

```lua
RegisterCommand("my_status", function(source)
    local traceId = exports.m4i_bridge:NewTraceId()

    local allowed = exports.m4i_bridge:HasPermission(source, "my_script.use")
    if not allowed then
        exports.m4i_bridge:NotifyPlayer(source, {
            type = "error",
            title = "Access denied",
            description = "Missing permission"
        })

        exports.m4i_bridge:Log("warn", "my_script", "permission denied", {
            source = source,
            traceId = traceId
        })
        return
    end

    local hasItem = exports.m4i_bridge:HasItem(source, "phone", 1)
    if not hasItem then
        exports.m4i_bridge:NotifyPlayer(source, {
            type = "error",
            description = "You need a phone"
        })
        return
    end

    exports.m4i_bridge:NotifyPlayer(source, {
        type = "success",
        description = "Command executed"
    })

    exports.m4i_bridge:Log("info", "my_script", "command completed", {
        source = source,
        traceId = traceId
    })
end, false)
```

## Team checklist before releasing a script

1. no direct provider/framework calls in gameplay code
2. all external inputs validated
3. callback timeouts handled
4. bridge logging used in critical paths
5. security-sensitive actions protected with permission + cooldown/rate-limit controls
6. tested with `/m4i:debug` and provider configuration used by target server
