# Integration

## Integration Rule

Use `m4i_interface` exports/events for UI notifications and overlays.

Avoid:

- direct NUI message injection from external scripts
- parallel duplicate notification UIs for the same message source
- bypassing bridge ownership for framework-facing data

## Choose the Right Entry Path

Use **direct payloads** when your script already has full runtime values.
Use **module + preset** when you want reusable policy templates from `Config.NotifyModules`.

Both paths are valid and can coexist.

## Direct Notify (Unified Entry)

Client-side:

```lua
TriggerEvent('m4i_interface:notify', {
    type = 'system',
    title = 'Server',
    message = 'Welcome to MKS RolePlay',
    duration = 5000
})
```

Server-to-client:

```lua
TriggerClientEvent('m4i_interface:notify', targetSource, {
    type = 'system',
    title = 'Dispatch',
    message = 'Unit assigned.',
    duration = 4500
})
```

## Typed Integration (Dedicated Wrappers)

Use dedicated typed wrappers when intent is explicit:

- `ShowEventBanner`
- `ShowDMAlert`
- `ShowModerationAlert`
- `ShowJobAnnouncement`
- `ShowVideoBroadcast`

Or trigger typed events:

- `m4i_interface:eventBanner` / `m4i_interface:event:banner`
- `m4i_interface:dm` / `m4i_interface:dm:alert`
- `m4i_interface:moderation` / `m4i_interface:moderation:alert`
- `m4i_interface:job` / `m4i_interface:job:announcement`
- `m4i_interface:video` / `m4i_interface:video:broadcast`

Typed notify aliases are also available:

- `m4i_interface:notify:system`
- `m4i_interface:notify:event`
- `m4i_interface:notify:dm`
- `m4i_interface:notify:moderation`
- `m4i_interface:notify:job`
- `m4i_interface:notify:video`

Video runtime control aliases:

- `m4i_interface:video:broadcast:clear`
- `m4i_interface:video:clear`

Video command-menu bridge events:

- client -> server: `m4i_interface:video:broadcast:request`
- server -> client: `m4i_interface:video:broadcast:openMenu`

## Module + Preset Resolution

`Notify(payload)` supports:

- `module`
- `preset`

Merge order:

1. `Config.NotifyModules.<module>.Defaults`
2. `Config.NotifyModules.<module>.Presets.<preset>`
3. incoming payload

Payload overrides preset/default values.

Invalid module/preset is handled safely (no crash).

## Module + Preset Examples

### Core/System

```lua
TriggerEvent('m4i_interface:notify', {
    module = 'Core',
    preset = 'System',
    message = 'Restart completed successfully.'
})
```

### Staff Warning

```lua
TriggerEvent('m4i_interface:notify', {
    module = 'Staff',
    preset = 'Warning',
    message = 'Roleplay violation detected.'
})
```

### Staff DM

```lua
TriggerEvent('m4i_interface:notify', {
    module = 'Staff',
    preset = 'DM',
    senderLabel = 'Senior Admin',
    message = 'Please open a support ticket.'
})
```

### Jobs Dispatch

```lua
TriggerEvent('m4i_interface:notify', {
    module = 'Jobs',
    preset = 'Dispatch',
    jobName = 'Police Department',
    locationLabel = 'Mission Row',
    message = 'Units report to dispatch room.'
})
```

### Event Announcement

```lua
TriggerEvent('m4i_interface:notify', {
    module = 'Events',
    preset = 'Announcement',
    title = 'City Event',
    description = 'Meet at Legion Square in 10 minutes.'
})
```

### Video Broadcast

```lua
TriggerEvent('m4i_interface:notify', {
    module = 'Video',
    preset = 'Broadcast',
    title = 'Public Broadcast',
    sourceUrl = 'https://cdn.example.com/broadcast.mp4'
})
```

Video payload still must pass protocol/domain/extension validation.

## Legacy and Compatibility Paths

Still supported:

- `interface:notification`
- `m4i_interface:notification`
- `okokTextUI:Open` / `okokTextUI:Close`

Optional compatibility routing:

- `QBCore.Functions.Notify` -> `m4i_interface` (`Config.QBCoreNotifyCompat = true`)
- `QBCore.Functions.Progressbar` -> `m4i_interface` (`Config.QBCoreProgressCompat = true`)

## Runtime Commands

Video command:

- `/m4i_video_broadcast` (opens menu in-game when no args)
- `/m4i_video_broadcast <url> [duration_ms] [windowed|fullscreen] [title ...]`
- `/m4i_video_broadcast near <radius_m> <url> [duration_ms] [windowed|fullscreen] [title ...]`
- `/m4i_video_broadcast <radius_m> <url> [duration_ms] [windowed|fullscreen] [title ...]`
- `/m4i_video_broadcast stop`
- `/m4i_video_broadcast_stop`

Minimap command:

- `/m4i_map show`
- `/m4i_map move left|right|up|down [amount]`
- `/m4i_map set <x> <y>`
- `/m4i_map reset`

## Full Command Inventory (Current Runtime)

This list reflects commands currently registered in `m4i_interface`.

Always available (or config-driven):

- `/<Config.ConfigureHudCommand>` (default `/configure_hud`, when `Config.ConfigurationMenu = true`)
- `/m4i_interface_status`
- `/openui`
- `/closeui`
- `/<Config.MinimapPositionCommand>` (default `/m4i_map`)
- `/<Config.ExternalHud.Command>` (default `/m4i_hud_mode`)
- `/toggleseatbelt`
- `/interface:cancelProgress`
- `/<Config.MoneyIndicators.CashCommand>` (default `/cash`)
- `/<Config.MoneyIndicators.BankCommand>` (default `/bank`)
- `/<Config.MoneyIndicators.JobCommand>` (default `/job`)
- `/<Config.MoneyIndicators.IdCommand>` (default `/id`)
- `/<Config.MoneyIndicators.OnlineCommand>` (default `/online`)
- `/omline` (legacy alias kept in runtime)
- `/<Config.MenuMusic.TrackCommand>` (default `/m4i_music`)
- `/<Config.MenuMusic.VolumeCommand>` (default `/m4i_music_volume`)
- `/<Config.NotifyFoundation.VideoBroadcast.AudioControl.Command>` (default `/m4i_video_sound`)
- `/<Config.NotifyFoundation.VideoBroadcast.AudioControl.VolumeCommand>` (default `/m4i_video_volume`)
- `/m4i_video_audio_reset`
- `/m4i_video_beep`
- `/<Config.ThemeLock.Command>` (default `/m4i_theme_lock`)
- `/<Config.VideoBroadcastCommand.Command>` (default `/m4i_video_broadcast`)
- `/<Config.VideoBroadcastCommand.StopCommand>` (default `/m4i_video_broadcast_stop`)
- `/m4i_interface:diag`
- `/m4i_interface:locale <server_id>`

Debug-only commands:

- `/m4i_refresh_locale` (only when interface debug mode is enabled)
- `/reset_hud_config` (only when interface debug mode is enabled)
- `/close_configure_hud` (only when interface debug mode is enabled)
- `/cinematic` (only when interface debug mode is enabled)
- `/stopcinematic` (only when interface debug mode is enabled)

Test commands (`Config.Debug.TestCommands.Enabled = true`):

- `/m4i_test_notify`
- `/m4i_test_event`
- `/m4i_test_dm`
- `/m4i_test_moderation`
- `/m4i_test_job`
- `/m4i_test_progress`
- `/m4i_test_all`
- `/m4i_test_video [url]` (only when `EnableVideoTestCommand = true`)
