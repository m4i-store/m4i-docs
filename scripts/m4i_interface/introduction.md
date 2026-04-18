# m4i_interface Introduction

`m4i_interface` is the UI/presentation resource for M4I gameplay experience in **bridge-first mode**.

It is responsible for:

- HUD and vehicle HUD rendering
- Progress bar rendering
- Typed notification rendering and overlay pipelines
- Text UI compatibility routing
- Interface-focused commands and exports

## Typed Notification Renderers

Current implemented typed renderers:

- `system`
- `event`
- `dm`
- `moderation`
- `job`
- `video`

Each type is routed through the unified notify foundation, but rendered through its own pipeline/UI behavior.

## Relationship to m4i_bridge

`m4i_interface` consumes runtime data via `m4i_bridge` exports and does not own framework adapters directly.

Bridge boundary config lives in:

- `shared/config.lua` -> `Config.Bridge.Resource`
- `shared/config.lua` -> `Config.Bridge.Exports`

## Ownership Boundaries

`m4i_interface` owns:

- NUI state + rendering
- notification normalization/routing on client
- queue/timer/cleanup behavior for UI overlays
- integration exports/events for interface presentation

`m4i_interface` does **not** own:

- framework persistence/business logic
- identity data ownership policy
- gameplay/job/economy orchestration
- moderation backend policy

## Runtime Diagnostics

Useful runtime commands:

- `/m4i_interface:diag`
- `/m4i_interface:locale <server_id>`

Use these first when verifying bridge health and locale context before deeper script debugging.

## Read Next

- [Installation](installation.md)
- [Configuration](configuration.md)
- [Integration](integration.md)
