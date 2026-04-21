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

## Server.cfg ACE Permissions

Minimum recommended ACE entries for admin operations:

```cfg
# Example principal (replace with your real principal mapping)
add_principal group.admin group.user

# m4i admin fallback used by diagnostics/test authorization fallback
add_ace group.admin m4i.admin allow

# Theme lock command permission
add_ace group.admin command.m4i_theme_lock allow

# Video broadcast command permissions
add_ace group.admin command.m4i_video_broadcast allow
add_ace group.admin command.m4i_video_broadcast_stop allow
```

Notes:

- If you renamed commands in config, ACE must match the final command names:
  - `Config.ThemeLock.Command`
  - `Config.VideoBroadcastCommand.Command`
  - `Config.VideoBroadcastCommand.StopCommand`
- `m4i_interface:diag` and `m4i_interface:locale` use admin authorization logic:
  - bridge `IsAdmin`, or
  - ACE `m4i.admin` (fallback), or
  - ACE `command` (broad fallback; not recommended as primary grant).
- Most client-only utility commands (HUD/minimap/music/seatbelt/etc.) do not require ACE by default.

## Optional ACE for Test Command Group Gates

When `Config.Debug.TestCommands.Enabled = true` and `AllowedGroups` is used, runtime can also validate:

- `group.<name>`
- `m4i.group.<name>`

Example:

```cfg
add_ace group.admin group.admin allow
add_ace group.admin m4i.group.admin allow
```
