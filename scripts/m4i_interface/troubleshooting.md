# Troubleshooting

## 1) Notify Does Not Appear

Check:

- `Config.NotifyFoundation.Enabled = true`
- typed block is enabled for the payload type:
  - `EventBanner.Enabled`
  - `DMAlert.Enabled`
  - `ModerationAlert.Enabled`
  - `JobAnnouncement.Enabled`
  - `VideoBroadcast.Enabled`
- payload contains required fields (`message` minimum; `sourceUrl` for `video`)

If a typed block is disabled, `m4i_interface` falls back to basic notification path instead of crashing.

## 2) Wrong Renderer/Type Used

Common causes:

- `type` missing (defaults to `system`)
- using generic notify when you intended a typed wrapper
- preset sets one type and payload overrides it

Fix:

- pass explicit `type`
- or use dedicated wrappers:
  - `ShowEventBanner`
  - `ShowDMAlert`
  - `ShowModerationAlert`
  - `ShowJobAnnouncement`
  - `ShowVideoBroadcast`

## 3) Module/Preset Not Applying

Check:

- `Config.NotifyModules.<Module>` exists
- `Presets.<Preset>` exists under that module
- module/preset names match (case-insensitive match is supported, spelling must still be correct)

Behavior:

- invalid module/preset is ignored safely
- payload still runs through normal notify flow

## 4) Video Rejected

Video pipeline accepts only validated direct media URLs.

Typical rejection reasons:

- `missing_source`
- `invalid_protocol` / `protocol_not_allowed`
- `domain_not_allowed`
- `invalid_extension` / `extension_not_allowed`
- `iframe_not_allowed`
- `embed_not_allowed`
- `rate_limited`

Check:

- URL is direct `https://.../*.mp4` or `https://.../*.webm`
- `Config.NotifyFoundation.VideoBroadcast.Enabled = true`
- protocol/domain/extension policy in config matches your URL
- rate limit is not currently exceeded

## 5) Debug/Test Commands Not Available

Check:

- `Config.Debug.TestCommands.Enabled = true`
- `RequireAdmin` and ACE/bridge admin policy allow the player
- optional `AllowedGroups` permits player group
- chat suggestions require `ShowChatSuggestion = true` and `chat` resource running

Video test command additionally needs:

- `EnableVideoTestCommand = true`
- `NotifyFoundation.VideoBroadcast.Enabled = true`

## 6) Legacy Notify vs Module/Preset Confusion

Both are valid:

- Legacy/direct calls: provide full payload directly
- Module/preset calls: template values from config domains + payload override

Rule of thumb:

- If your script already has full values, call direct `Notify`.
- If you need consistent reusable style/policy, use `module + preset`.

## 7) HUD/Display Issues

### `/configure_hud` does not open

- `Config.ConfigurationMenu = true`
- `Config.ConfigureHudCommand` is correct
- if keybind expected, `Config.MenuKeybind` must not be `false`

### Money indicators (`/cash`, `/bank`, `/job`, `/id`, `/online`) do not show

- `Config.MoneyIndicators.Enabled = true`
- command names are correctly set
- hide-by-default flags and `DurationMs` are not blocking expected behavior

### Theme still changeable by player

- `Config.ThemeLock.Enabled = true`
- `Config.ThemeLock.HideThemeSelector = true`
- reload resource after config change

## 8) Bridge/Locale Diagnostics

If HUD data looks wrong:

- ensure `m4i_bridge` starts before `m4i_interface`
- run `/m4i_interface:diag`
- verify bridge export names in `Config.Bridge.Exports`

If locale looks wrong:

- run `/m4i_interface:locale <server_id>`
- ensure `m4i_identity` is running (if used)

## 9) Minimap Command Not Working

Check:

- `Config.MinimapPositionCommand` matches the command you run (default: `/m4i_map`)
- `Config.HideRadar = false` if you want radar visible on foot
- `Config.MinimapOffsetLimits` not too restrictive for your intended move

Validate with:

- `/m4i_map show`
- `/m4i_map move right 0.01`
- `/m4i_map reset`

If movement does not appear:

- ensure resource restarted after config/script changes
- verify no external HUD script is overriding minimap component positions

## 10) Video Broadcast Stop/Radius Issues

If stop command does not work:

- use `/m4i_video_broadcast stop` or `/m4i_video_broadcast_stop`
- ensure player has ACE:
  - `command.m4i_video_broadcast`
  - `command.m4i_video_broadcast_stop` (when using dedicated stop command)

If near/radius broadcast does not work:

- command must be used by an in-game player (not server console)
- test syntax:
  - `/m4i_video_broadcast near 30 <url>`
  - `/m4i_video_broadcast 30 <url>`
- radius value must be within configured max (`Config.VideoBroadcastCommand.MaxRadius`)
