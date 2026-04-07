# Hook System

## Purpose

Hooks let services and plugins intercept or observe bridge actions through named events.

Common event patterns:

- `before:*` for pre-execution control
- `after:*` for post-execution observation

## Registering hooks

```lua
local hookId, err = exports.m4i_bridge:RegisterHook(eventName, handler, {
    priority = 100,
    once = false
})
```

`priority` is higher-first execution order.

## Before vs after hooks

### Before hooks

Use to:

- validate payloads
- cancel flow
- mutate payload before main action

### After hooks

Use to:

- audit outcomes
- emit telemetry
- enrich result context

After hooks are observation-oriented and typically non-cancelable in caller flow.

## Cancellation behavior

A cancelable hook can stop flow by returning:

- `false, "reason"`
- `{ cancel = true, reason = "reason" }`

If cancelled, hook emission returns a cancelled result and caller may abort action.

## Mutation behavior

Hook handlers may modify payload by returning:

- table with `payload = <newPayload>`
- table with `data = <newPayload>`
- table with `patch = <partialTable>` (deep merge)
- any non-nil direct value as replacement payload

## Priority order

Hooks are sorted:

1. higher `priority` first
2. if same priority, stable ID ordering

Use high priorities only for cross-cutting guards.

## Error handling mode

Controlled by config:

- `hooks.failHard = false`: hook errors are isolated and flow continues
- `hooks.failHard = true`: hook handler errors fail the active flow

## Deprecated legacy names

Legacy names are still accepted for compatibility but should be replaced:

- `beforePlayerLoad` -> `before:player:get`
- `afterPlayerLoad` -> `after:player:get`
- `beforeItemAdd` -> `before:inventory:addItem`
- `afterItemAdd` -> `after:inventory:addItem`
- `beforeCallbackExecute` -> `before:callback:execute`
- `afterCallbackExecute` -> `after:callback:execute`
- `afterDispatch` -> `after:dispatch:send`

## Example

```lua
local hookId = exports.m4i_bridge:RegisterHook("before:inventory:addItem", function(payload)
    if payload.amount and payload.amount > 100 then
        return { cancel = true, reason = "amount_too_large" }
    end

    payload.metadata = payload.metadata or {}
    payload.metadata.audit = "bridge_hook"
    return { payload = payload }
end, {
    priority = 400
})
```
