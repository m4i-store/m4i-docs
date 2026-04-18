# Integration

## Core Rule

Integrate with `m4i_interface` through its events/exports.

Do not:

- bypass the interface pipeline with direct NUI messages from other resources
- duplicate notification rendering in parallel UIs without clear ownership
- bypass `m4i_bridge` for framework data ownership

## Notification Entry Points

Primary event:

```lua
TriggerEvent('m4i_interface:notify', {
    type = 'system',
    title = 'Server',
    message = 'Welcome',
    duration = 5000
})
```

Typed event aliases:

- `m4i_interface:notify:system`
- `m4i_interface:notify:event`
- `m4i_interface:notify:dm`
- `m4i_interface:notify:moderation`
- `m4i_interface:notify:job`
- `m4i_interface:notify:video`

Dedicated typed events:

- `m4i_interface:eventBanner`
- `m4i_interface:dm`
- `m4i_interface:moderation`
- `m4i_interface:job`
- `m4i_interface:video`

## Bridge and Legacy Compatibility

The resource keeps compatibility paths for existing flows:

- legacy notify events (`interface:notification`, `m4i_interface:notification`)
- `okokTextUI:Open` / `okokTextUI:Close` are routed to m4i text UI
- QBCore notify/progress wrappers can be patched to m4i_interface when enabled in config

## Text UI Integration

Use:

```lua
TriggerEvent('m4i_interface:textui:open', '[E] Interact', 'lightgreen', 'right')
TriggerEvent('m4i_interface:textui:close')
```

## Runtime Diagnostic Integration

Operational commands:

- `/m4i_interface:diag`
- `/m4i_interface:locale <server_id>`

Use these before debugging gameplay scripts that depend on HUD/runtime values.
