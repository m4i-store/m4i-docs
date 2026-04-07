# Plugin System

## Purpose

Plugins let external resources extend `m4i_bridge` without editing bridge core files.

A plugin can register:

- hooks
- middleware
- container services/values
- lifecycle handlers (`init`, `start`, `stop`)

## Registering a plugin

Use export:

```lua
exports.m4i_bridge:RegisterPlugin(pluginDefinition)
```

Expected fields:

- `name` (string, required in practice)
- `version` (string)
- `description` (string)
- `author` (string)
- `hooks` (table)
- `middleware` (table)
- `services` (table)
- `init(context)` (function)
- `start(context)` (function)
- `stop(context)` (function)

## Lifecycle

### `init(context)`

Runs once during registration after bindings are prepared.
Use this for setup and container value registration.

### `start(context)`

Runs when plugin starts (kernel start or runtime registration with autostart).
Use this for activating runtime behavior.

### `stop(context)`

Runs on plugin stop/unregister/kernel stop.
Use this for cleanup.

## Safety and validation

Plugin registration includes:

- schema validation
- duplicate name prevention
- optional source-name enforcement
- lifecycle error containment

If plugin validation fails, registration is rejected with clear error.

## Ownership and cleanup

Plugin records include owner resource. On resource stop, bridge cleanup can remove owner-bound plugin registrations when `hotReload.cleanupOnResourceStop = true`.

## Best practices

- set plugin `name` to your resource name
- keep `init/start/stop` idempotent
- keep plugin hooks/middleware focused and explicit
- avoid heavy blocking logic in lifecycle handlers
- use bridge logging for plugin diagnostics

## Example plugin

```lua
local plugin = {
    name = GetCurrentResourceName(),
    version = "1.0.0",
    description = "Example plugin",
    author = "M4I",

    hooks = {
        ["before:callback:execute"] = {
            priority = 500,
            handler = function(payload)
                if payload.callbackName == "blocked:test" then
                    return { cancel = true, reason = "blocked_by_policy" }
                end
            end
        }
    },

    middleware = {
        ["dispatch:server:send"] = {
            priority = 300,
            handler = function(ctx, next)
                if type(ctx.payload) ~= "table" then
                    return false, "invalid_payload"
                end
                return next()
            end
        }
    },

    services = {
        audit = {
            singleton = true,
            dependencies = { "service.logging" },
            factory = function(deps)
                local logging = deps[1]
                return {
                    write = function(_, category, message, contextData)
                        logging:info(category, message, contextData)
                    end
                }
            end
        }
    },

    init = function(ctx)
        ctx:set("plugin.audit.enabled", true)
        return true
    end,

    start = function(_ctx)
        return true
    end,

    stop = function(_ctx)
        return true
    end
}

local ok, err = exports.m4i_bridge:RegisterPlugin(plugin)
if not ok then
    print(("plugin registration failed: %s"):format(tostring(err)))
end
```
