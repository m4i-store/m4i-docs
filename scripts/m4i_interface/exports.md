# Exports

All exports below are client-side exports from `m4i_interface`.

## Core HUD

### Initialize

```lua
exports.m4i_interface:Initialize()
```

Starts UI initialization flow.

### ToggleHud

```lua
exports.m4i_interface:ToggleHud(state)
```

- `state` (`boolean`)

Shows/hides HUD.

## Notifications

### Notify

```lua
exports.m4i_interface:Notify(payload)
```

Unified typed notify entry.

Common payload keys:

- `id`
- `type` (`system`, `event`, `dm`, `moderation`, `job`, `video`)
- `title`
- `message`
- `duration`
- `icon`
- `accent`
- `priority`
- `metadata`

### AddNotify

```lua
exports.m4i_interface:AddNotify(textOrPayload, header, time, icon)
```

Legacy-friendly alias to `Notify`.

### ShowEventBanner / ShowDMAlert / ShowModerationAlert / ShowJobAnnouncement / ShowVideoBroadcast

```lua
exports.m4i_interface:ShowEventBanner(payload)
exports.m4i_interface:ShowDMAlert(payload)
exports.m4i_interface:ShowModerationAlert(payload)
exports.m4i_interface:ShowJobAnnouncement(payload)
exports.m4i_interface:ShowVideoBroadcast(payload)
```

Typed wrappers that force the matching notification type.

## Progress

### ProgressBar / progress

```lua
exports.m4i_interface:ProgressBar(data)
exports.m4i_interface:progress(data)
```

`data` supports duration, label, cancel rules, disabled controls, animation, and prop attachments.

### CancelProgress

```lua
exports.m4i_interface:CancelProgress()
```

Cancels active progress.

### ProgressActive

```lua
exports.m4i_interface:ProgressActive()
```

Returns `true` when progress is active.

## Text UI

### OpenTextUI / CloseTextUI

```lua
exports.m4i_interface:OpenTextUI(message, color, position)
exports.m4i_interface:CloseTextUI()
```

Aliases:

```lua
exports.m4i_interface:Open(message, color, position)
exports.m4i_interface:Close()
```

## Cinematic

```lua
exports.m4i_interface:StartCinematicCam()
exports.m4i_interface:StopCinematicCam()
exports.m4i_interface:IsCinematicActive()
```

## Seatbelt

```lua
exports.m4i_interface:HasHarness()
exports.m4i_interface:IsSeatbeltOn()
exports.m4i_interface:ToggleSeatbelt(state)
```

`ToggleSeatbelt` returns `(ok, currentState)`.

## External HUD Mode

```lua
exports.m4i_interface:IsExternalHudModeEnabled()
exports.m4i_interface:GetHudMode()
exports.m4i_interface:SetHudMode(mode, persist)
```

`mode` values: `m4i`, `ps_hud`, `gd_hud2`, `uz_purehud`.

## UI Configuration State

```lua
exports.m4i_interface:HasHudConfigured()
```

Returns current UI configured state after initialization.
