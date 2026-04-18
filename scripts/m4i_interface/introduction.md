# m4i_interface Introduction

`m4i_interface` is the M4I gameplay interface/HUD resource running in bridge-only mode.

It owns client UI rendering for:

- main HUD and vehicle HUD
- progress bar flow
- typed notifications (`system`, `event`, `dm`, `moderation`, `job`, `video`)
- seatbelt and cinematic helpers
- text UI compatibility events

## Ownership Boundaries

`m4i_interface` owns:

- NUI state and HUD rendering
- notification queue/overlay rendering
- interface-facing exports and UI events

`m4i_interface` does not own:

- framework/business data persistence
- identity ownership logic
- framework adapters outside bridge boundary

## Relationship to m4i_bridge

`m4i_interface` consumes runtime data from `m4i_bridge` exports only.

Required bridge boundary is configured via:

- `shared/config.lua` -> `Config.Bridge.Resource`
- `shared/config.lua` -> `Config.Bridge.Exports`

Recommended start order:

1. `ox_lib`
2. `m4i_bridge`
3. `m4i_identity` (optional, language ownership)
4. `m4i_interface`

## Runtime Diagnostics

Server commands:

- `/m4i_interface:diag`
- `/m4i_interface:locale <server_id>`

Use these commands first when checking bridge/locale/runtime health.
