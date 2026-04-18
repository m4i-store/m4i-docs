# Troubleshooting

## HUD Data Not Updating

Check:

- `m4i_bridge` is started before `m4i_interface`
- bridge providers are healthy (`/m4i_interface:diag`)
- `Config.Bridge.Resource` and `Config.Bridge.Exports` names are correct

## Notifications Not Showing

Check:

- `Config.NotifyFoundation.Enabled = true`
- per-type block is enabled (for example `EventBanner.Enabled`, `DMAlert.Enabled`, `VideoBroadcast.Enabled`)
- payload has at least a valid `message` or typed equivalent

For video:

- source must be direct `.mp4` or `.webm`
- protocol must pass configured allow policy (default https-only)

## /configure_hud Does Not Open

Check:

- `Config.ConfigurationMenu = true`
- `Config.ConfigureHudCommand` value
- if keybind is expected, ensure `Config.MenuKeybind` is not `false`

## Cash/Bank/Job/ID/Online Indicators Do Not Appear

Check `Config.MoneyIndicators`:

- `Enabled = true`
- command names (`CashCommand`, `BankCommand`, `JobCommand`, `IdCommand`, `OnlineCommand`)
- temporary display time (`DurationMs`)
- hide-by-default flags

## Theme Still Changeable by Player

Check:

- `Config.ThemeLock.Enabled = true`
- `Config.ThemeLock.HideThemeSelector = true`
- client reloaded after config change

## External HUD Mode Not Applying

Check:

- `Config.ExternalHud.Enabled = true`
- target external HUD resource is started
- command `/m4i_hud_mode status` for effective mode/resource

If target resource is down, mode safely falls back to `m4i`.

## QBCore Notify/Progress Not Routed

Check:

- `qb-core` resource is started
- `Config.QBCoreNotifyCompat = true`
- `Config.QBCoreProgressCompat = true`

Routing is installed at runtime and retried periodically.

## Locale Mismatch

Use:

- `/m4i_interface:locale <server_id>`

Check:

- `m4i_identity` is started (if used for language ownership)
- locale files exist in `locales/*.json`
