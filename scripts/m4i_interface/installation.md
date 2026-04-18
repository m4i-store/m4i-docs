# Installation

## Requirements

- FiveM server with Lua 5.4 enabled
- `ox_lib`
- `m4i_bridge`
- `m4i_interface`
- Optional: `m4i_identity` (per-player language context)

`m4i_interface/fxmanifest.lua` depends on `ox_lib` and `m4i_bridge`.

## Recommended Start Order

1. `ox_lib`
2. `oxmysql` (if used in your stack)
3. `m4i_bridge`
4. `m4i_identity` (optional)
5. `m4i_interface`

## First Boot Checklist

1. Start server and confirm `m4i_bridge` has no blocking provider failures.
2. Start `m4i_interface`.
3. Run `/m4i_interface:diag` in server console.
4. Validate locale sync with `/m4i_interface:locale <server_id>` (optional but recommended).
5. In-game, open HUD config with `/<Config.ConfigureHudCommand>` (default `/configure_hud`).
6. Trigger a system notify test:

```lua
TriggerEvent('m4i_interface:notify', {
    type = 'system',
    title = 'Boot Check',
    message = 'm4i_interface loaded successfully.',
    duration = 4000
})
```

## Staging vs Production

Recommended baseline:

- Staging/Dev:
  - `Config.Debug.TestCommands.Enabled = true`
  - `Config.Debug.TestCommands.RequireAdmin = true`
  - `Config.NotifyFoundation.VideoBroadcast.Enabled = true` only for controlled testing
- Production:
  - `Config.Debug.TestCommands.Enabled = false`
  - Keep `Config.Debug.Interface = false` unless actively diagnosing
  - Keep video conservative (`VideoBroadcast.Enabled` only when fully validated)

## Optional QBCore Compatibility Routing

If you want QBCore wrappers routed through `m4i_interface`:

- `Config.QBCoreNotifyCompat = true`
- `Config.QBCoreProgressCompat = true`

If set to `false`, QBCore native behavior remains in place.
