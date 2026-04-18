# Testing

This page covers the built-in in-game test commands shipped inside `m4i_interface`.

These commands are intended for **dev/staging validation** and should be disabled in production.

## Purpose

Use test commands to quickly validate:

- typed notification routing
- renderer visibility
- queue/timer behavior
- progress flow
- video validation behavior

## Enable/Disable

Configure in `shared/config.lua`:

```lua
Config.Debug = Config.Debug or {}
Config.Debug.TestCommands = {
    Enabled = true,
    RequireAdmin = true,
    AllowedGroups = { 'god', 'admin' },
    EnableVideoTestCommand = true,
    ShowChatSuggestion = true
}
```

Production recommendation:

- `Enabled = false`

## Admin/Group Restriction Behavior

When `RequireAdmin = true`, command use requires admin authorization through bridge/permission checks.

`AllowedGroups` is an additional filter and is best-effort:

- if group data is available, groups are enforced
- if group data is unavailable in the current framework bridge context, group filtering is not hard-blocking

## Available Commands

- `/m4i_test_notify`
- `/m4i_test_event`
- `/m4i_test_dm`
- `/m4i_test_moderation`
- `/m4i_test_job`
- `/m4i_test_progress`
- `/m4i_test_all`
- `/m4i_test_video [url]` (only when `EnableVideoTestCommand = true`)

## Sample Usage

```txt
/m4i_test_notify
/m4i_test_event
/m4i_test_dm
/m4i_test_moderation
/m4i_test_job
/m4i_test_progress
/m4i_test_all
/m4i_test_video https://cdn.example.com/broadcast.mp4
```

## Expected Outcomes

- `m4i_test_notify`: one system notification card appears.
- `m4i_test_event`: event banner overlay appears.
- `m4i_test_dm`: DM alert renderer appears.
- `m4i_test_moderation`: moderation alert renderer appears with severity style.
- `m4i_test_job`: job announcement renderer appears.
- `m4i_test_progress`: progress bar starts and completes/cancels correctly.
- `m4i_test_all`: non-video typed tests run in short sequence.
- `m4i_test_video`: video broadcast path is tested (if video pipeline is enabled).

## Video Test Constraints

Video test command still obeys runtime video safety:

- `Config.NotifyFoundation.VideoBroadcast.Enabled = true`
- URL must be valid by policy (`AllowedProtocols`, `AllowedDomains`, `AllowedExtensions`)
- direct media only (`.mp4` / `.webm`)
- iframe/embed/Youtube-style links are rejected

If invalid, broadcast is rejected safely.
