# Configuration

`m4i_interface` configuration lives in:

- `m4i_interface/shared/config.lua`

## Core Runtime

- `Config.Locale`
: Legacy fallback locale. Primary per-player locale can come from `m4i_identity`.

- `Config.Bridge`
: Bridge boundary and export-name mapping.

- `Config.Logging`
: Runtime log level (`debug`, `info`, `warn`, `error`, `none`).

## UI Entry Points

- `Config.ConfigurationMenu`
: Enables the HUD/configuration menu flow.

- `Config.ConfigureHudCommand`
: Command name used to open configure UI (default `configure_hud`).

- `Config.MenuKeybind`
: Keybind for configure command (`false` disables keybind registration).

## Notification Foundation

`Config.NotifyFoundation` controls typed notifications.

Global keys:

- `Enabled`
- `MaxVisible`
- `DefaultDuration`
- `DefaultPosition`
- `StackGap`
- `Animation.EnterMs`, `Animation.ExitMs`
- `DefaultPriority`
- `DefaultAccent`
- `DefaultIcon`
- `CategoryLabels`
- `CategoryAccents`

Typed blocks:

- `EventBanner`
- `DMAlert`
- `ModerationAlert`
- `JobAnnouncement`
- `VideoBroadcast`

Each type has its own `Enabled`, duration, queue, accent, and animation policy.

## Money Indicators (Displayers)

`Config.MoneyIndicators` controls displayers visibility behavior:

- hide-by-default flags (`HideCashByDefault`, `HideBankByDefault`, `HideJobByDefault`, `HideIdByDefault`, `HideOnlineByDefault`)
- temporary show duration (`DurationMs`)
- command names (`CashCommand`, `BankCommand`, `JobCommand`, `IdCommand`, `OnlineCommand`)
- editor behavior (`ShowAllInEditor`)

## Theme Lock

`Config.ThemeLock` can force one global color:

- `Enabled`
- `Color`
- `HideThemeSelector`
- `Command`

## External HUD Composer

`Config.ExternalHud` supports mode switching:

- `m4i`
- `ps_hud`
- `gd_hud2`
- `uz_purehud`

Config keys:

- `Enabled`
- `Mode`
- `PersistWithKvp`
- `Command`
- `NotifyOnModeChange`

## Music Controls

`Config.MenuMusic`:

- runtime enable/disable
- persisted track/volume
- command names (`TrackCommand`, `VolumeCommand`)

Track sources:

- `Config.MusicPath`
- `Config.Music`

## Framework Compatibility Flags

- `Config.QBCoreNotifyCompat`
: Routes QBCore notify to m4i_interface notify pipeline.

- `Config.QBCoreProgressCompat`
: Routes QBCore progressbar to m4i_interface progress pipeline.

## Gameplay HUD Options

Examples:

- `Config.Stress`, `Config.StressChance`, `Config.MinimumStress`
- `Config.Units` (`kmh`/`mph`)
- `Config.HideRadar`
- `Config.EnableCinematicMode`
- `Config.VoiceChat`
