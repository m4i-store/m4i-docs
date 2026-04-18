# Installation

## Requirements

- FiveM server (Lua 5.4)
- `ox_lib`
- `m4i_bridge`
- `m4i_interface` files installed
- `m4i_identity` optional (for per-player language)

## Dependencies

`m4i_interface/fxmanifest.lua` requires:

- `ox_lib`
- `m4i_bridge`

`m4i_bridge` must be started before `m4i_interface`.

## Recommended Start Order

1. `ox_lib`
2. `oxmysql` (if your stack uses it)
3. `m4i_bridge`
4. `m4i_identity` (optional)
5. `m4i_interface`

## First Setup Checklist

1. Confirm `m4i_bridge` is started with no critical provider errors.
2. Configure `m4i_interface/shared/config.lua` for your server policy.
3. Start `m4i_interface`.
4. Run `/m4i_interface:diag` and verify bridge mode is healthy.
5. Test UI open command (`/configure_hud` by default).
6. Test one notification via:
   - `TriggerEvent('m4i_interface:notify', { title = 'Test', message = 'OK' })`

## Optional Compatibility

If you use QBCore wrappers:

- keep `Config.QBCoreNotifyCompat = true` to route `QBCore.Functions.Notify`
- keep `Config.QBCoreProgressCompat = true` to route `QBCore.Functions.Progressbar`

If disabled, QBCore uses its native handlers.
