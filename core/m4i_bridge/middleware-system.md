# Middleware System

## Purpose

Middleware provides scoped execution pipelines for selected actions.

Typical scopes:

- `callback:server:execute`
- `callback:client:execute`
- `dispatch:server:send`
- `dispatch:client:send`

## Registering middleware

```lua
local ok, err = exports.m4i_bridge:RegisterMiddleware(
    "callback:server:execute",
    "my_resource:rate_guard",
    function(ctx, next)
        return next()
    end,
    {
        priority = 200
    }
)
```

## Middleware flow

Execution model:

1. middleware chain selected by `scope`
2. middleware runs in priority order
3. each middleware decides whether to call `next()`
4. final handler runs when chain reaches end

## `next()` rules

- `next()` can be called once per middleware
- calling `next()` multiple times is an error
- not calling `next()` short-circuits the chain

## Return behavior

Middleware handler return values:

- `return next()` to continue
- `return false, "reason"` to cancel/fail chain
- `return value` to short-circuit with result
- set `ctx.cancelled = true` to signal cancellation state

## Context usage

`ctx` is shared across the chain and can carry:

- action payload
- source/callback metadata
- traceId
- intermediate result
- cancellation flags

Keep context keys explicit and domain-relevant.

## Error handling mode

Controlled by config:

- `middleware.failHard = true`: middleware errors fail the execution flow
- `middleware.failHard = false`: middleware errors are soft-failed and chain continues

## Example: validation middleware

```lua
exports.m4i_bridge:RegisterMiddleware(
    "dispatch:server:send",
    "my_resource:dispatch_validate",
    function(ctx, next)
        if type(ctx.payload) ~= "table" then
            return false, "invalid_dispatch_payload"
        end

        if not ctx.payload.title then
            return false, "dispatch_title_required"
        end

        return next()
    end,
    {
        priority = 300
    }
)
```

## Example: timing middleware

```lua
exports.m4i_bridge:RegisterMiddleware(
    "callback:server:execute",
    "my_resource:timing",
    function(ctx, next)
        local started = GetGameTimer()
        local ok, result = next()
        local elapsed = GetGameTimer() - started

        exports.m4i_bridge:Log("debug", "middleware", "callback timing", {
            callback = ctx.callbackName,
            durationMs = elapsed,
            ok = ok
        })

        if not ok then
            return false, result
        end

        return result
    end,
    {
        priority = 100
    }
)
```
