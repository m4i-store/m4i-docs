# Configuration

Primary config file:

- `m4i_interface/shared/config.lua`

Modular notification domain files:

- `m4i_interface/config/config_notify_core.lua`
- `m4i_interface/config/config_notify_staff.lua`
- `m4i_interface/config/config_notify_jobs.lua`
- `m4i_interface/config/config_notify_events.lua`
- `m4i_interface/config/config_notify_video.lua`

## 1) NotifyFoundation (Core Notification Runtime)

`Config.NotifyFoundation` controls normalized typed notification behavior.

Global keys:

- `Enabled`
- `MaxVisible`
- `DefaultDuration`
- `DefaultPosition`
- `StackGap`
- `Animation.EnterMs` / `Animation.ExitMs`
- `DefaultPriority`
- `DefaultAccent`
- `DefaultIcon`
- `DefaultSound`
- `CategoryLabels`
- `CategoryAccents`

Typed pipeline blocks:

- `EventBanner`
- `DMAlert`
- `ModerationAlert`
- `JobAnnouncement`
- `VideoBroadcast`

Each typed block has isolated queue/timer/render settings.

## 2) VideoBroadcast Safety Config

`Config.NotifyFoundation.VideoBroadcast` is intentionally conservative.

Important keys:

- `Enabled` (default `false`)
- `DefaultDuration`
- `MaxVisible` (expected `1`)
- `QueueLimit`
- `DefaultMode` (`windowed` or `fullscreen`)
- `AllowFullscreen`
- `DefaultMuted`
- `AllowSkip`
- `AutoCloseOnEnd`
- `AllowedExtensions` (default `mp4`, `webm`)
- `AllowedProtocols` (default `https`)
- `AllowedDomains` (`{}` means no domain restriction beyond protocol+extension)
- `RateLimit.Enabled`, `RateLimit.WindowMs`, `RateLimit.MaxEvents`

### Production-Safe Video Recommendation

Use this baseline:

```lua
Config.NotifyFoundation.VideoBroadcast = {
    Enabled = false,
    AllowFullscreen = false,
    DefaultMuted = true,
    AllowedProtocols = { 'https' },
    AllowedExtensions = { 'mp4', 'webm' },
    AllowedDomains = {},
    RateLimit = {
        Enabled = true,
        WindowMs = 5000,
        MaxEvents = 5
    }
}
```

## 3) Modular Notify Domains (`Config.NotifyModules`)

Each domain file populates:

```lua
Config.NotifyModules = Config.NotifyModules or {}
```

Domain shape:

```lua
Config.NotifyModules.<Domain> = {
    Defaults = { ... },
    Presets = {
        <PresetName> = { ... }
    }
}
```

Built-in domain names in current implementation:

- `Core`
- `Staff`
- `Jobs`
- `Events`
- `Video`

`Notify(payload)` supports optional `module` and `preset`.

Merge order:

1. domain defaults
2. preset values
3. payload values

Payload values always override defaults/preset values.

If `module` or `preset` is invalid, resolution fails safely without runtime crash.

## 4) Debug/Test Commands

`Config.Debug.TestCommands` controls built-in test commands.

Keys:

- `Enabled`
- `RequireAdmin`
- `AllowedGroups`
- `EnableVideoTestCommand`
- `ShowChatSuggestion`

Recommended:

- Enable in dev/staging only
- Keep `RequireAdmin = true`
- Disable in production

## 5) Related Interface Runtime Areas

Other high-impact config areas:

- `Config.ConfigureHudCommand`, `Config.MenuKeybind`, `Config.ConfigurationMenu`
- `Config.ThemeLock` (global color + selector visibility + runtime command)
- `Config.MoneyIndicators` (`/cash`, `/bank`, `/job`, `/id`, `/online`)
- `Config.ExternalHud` (switching among `m4i`, `ps_hud`, `gd_hud2`, `uz_purehud`)
- `Config.QBCoreNotifyCompat`, `Config.QBCoreProgressCompat`

## 6) What to Keep Out of Notify Module Files

Keep only notification-related values:

- display defaults
- presets/templates
- labels/accents/icons/durations
- renderer-facing metadata

Do not place:

- business/job economy logic
- database orchestration
- permission system ownership rules unrelated to notify display
