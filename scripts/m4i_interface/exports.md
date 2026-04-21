# Exports

All exports below are **client exports** from `m4i_interface`.

Use bracket syntax:

```lua
exports['m4i_interface']:Notify(payload)
```

## Notification Exports

### `Notify(payload)`

Unified typed entrypoint.

Supported `type` values:

- `system`
- `event`
- `dm`
- `moderation`
- `job`
- `video`

### `AddNotify(textOrPayload, header, time, icon)`

Legacy-friendly alias path that routes to the normalized notify flow.

### Typed wrapper exports

- `ShowEventBanner(payload)`
- `ShowDMAlert(payload)`
- `ShowModerationAlert(payload)`
- `ShowJobAnnouncement(payload)`
- `ShowVideoBroadcast(payload)`

These enforce their matching typed route.

## Progress Exports

- `ProgressBar(data)`
- `progress(data)` (alias)
- `CancelProgress()`
- `ProgressActive()`

`data` supports duration/label/cancel rules/control disable/animation/props.

## HUD and UI Exports

- `Initialize()`
- `ToggleHud(state)`
- `HasHudConfigured()`

## Text UI Exports

- `OpenTextUI(message, color, position)`
- `CloseTextUI()`
- `Open(message, color, position)` (alias)
- `Close()` (alias)

## Cinematic Exports

- `StartCinematicCam()`
- `StopCinematicCam()`
- `IsCinematicActive()`

## Seatbelt Exports

- `HasHarness()`
- `IsSeatbeltOn()`
- `ToggleSeatbelt(state)`

`ToggleSeatbelt` returns `(ok, currentState)`.

## External HUD Mode Exports

- `IsExternalHudModeEnabled()`
- `GetHudMode()`
- `SetHudMode(mode, persist)`

Supported modes:

- `m4i`
- `ps_hud`
- `gd_hud2`
- `uz_purehud`

## Event Names (for TriggerEvent/TriggerClientEvent)

Primary:

- `m4i_interface:notify`

Typed notify aliases:

- `m4i_interface:notify:system`
- `m4i_interface:notify:event`
- `m4i_interface:notify:dm`
- `m4i_interface:notify:moderation`
- `m4i_interface:notify:job`
- `m4i_interface:notify:video`

Typed direct aliases:

- `m4i_interface:eventBanner`
- `m4i_interface:event:banner`
- `m4i_interface:dm`
- `m4i_interface:dm:alert`
- `m4i_interface:moderation`
- `m4i_interface:moderation:alert`
- `m4i_interface:job`
- `m4i_interface:job:announcement`
- `m4i_interface:video`
- `m4i_interface:video:broadcast`
- `m4i_interface:video:broadcast:clear`
- `m4i_interface:video:clear`

Video command menu/request events:

- `m4i_interface:video:broadcast:openMenu`
- `m4i_interface:video:broadcast:request`

Legacy compatibility:

- `interface:notification`
- `m4i_interface:notification`
