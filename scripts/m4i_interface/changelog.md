# Changelog

## 1.1.94

### Added

- Dedicated typed renderer support documented and aligned for:
  - `system`
  - `event`
  - `dm`
  - `moderation`
  - `job`
  - `video`
- Dedicated testing documentation page (`testing.md`) for in-game test commands.

### Changed

- Full docs audit for `m4i_interface` pages:
  - introduction
  - installation
  - configuration
  - integration
  - exports
  - troubleshooting
- Export/event docs expanded to include typed aliases and compatibility entry points.
- Configuration docs updated for modular notify domains and `module + preset` flow.

### Fixed

- Documentation alignment with current implementation for:
  - isolated typed pipelines
  - optional `module + preset` resolution
  - video validation and safety constraints
  - debug command gating and admin restriction behavior

## 1.1.93

### Added

- Modular notification domain config files:
  - `config_notify_core.lua`
  - `config_notify_staff.lua`
  - `config_notify_jobs.lua`
  - `config_notify_events.lua`
  - `config_notify_video.lua`
- `Config.NotifyModules` domain/preset structure (`Defaults` + `Presets`).

### Changed

- `Notify(payload)` supports optional `module + preset` merge:
  - domain defaults -> preset -> payload
- Direct notify and typed pipelines remain backward compatible.

## 1.1.92

### Added

- Built-in in-game test commands (`/m4i_test_*`) inside `m4i_interface`.
- `Config.Debug.TestCommands` gate:
  - enable/disable
  - admin restriction
  - optional group filtering
  - video test command toggle
  - chat suggestion toggle
- Server-side test command authorization callback with bridge/ACE checks.

## 1.1.91

### Added

- Bridge-first runtime ownership model (`m4i_bridge` boundary).
- Unified typed notify foundation for `system/event/dm/moderation/job/video`.
- Typed wrappers/events for compatibility and clean integration surface.
- QBCore notify/progress compatibility routing under config flags.
- Theme lock and money indicator controls integrated into interface runtime.
