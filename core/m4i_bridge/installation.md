# Installation

## Requirements

Minimum runtime requirements:

- FiveM server artifact with Lua 5.4 support
- OneSync enabled (recommended for modern server stacks)
- `oxmysql` resource installed and started (database provider)
- At least one provider available per enabled domain (framework, inventory, UI, target, notify, progress, dispatch)

Provider resources depend on your configuration. Example:

- `qbx_core` for `framework = "qbox"`
- `qb-core` for `framework = "qbcore"`
- `es_extended` for `framework = "esx"`
- `ox_core` for `framework = "ox_core"`
- `ox_inventory` or `qb-inventory`
- `ox_lib` and/or `qb-menu`
- `ox_target` and/or `qb-target`

## Resource setup

1. Place `m4i_bridge` in your resources folder.
2. Keep the folder name exactly `m4i_bridge`.
3. Ensure config files are edited before first production boot:
- `config/default.lua`
- `config/providers.lua`
- `config/features.lua`

## Start order

`m4i_bridge` should start after its required provider resources and before any scripts that depend on bridge exports.

Example `server.cfg` segment:

```cfg
ensure oxmysql
ensure ox_lib
ensure qbx_core
ensure ox_inventory
ensure ox_target

ensure m4i_bridge

ensure m4i_jobs
ensure m4i_garage
ensure m4i_housing
```

## First boot checklist

1. Confirm selected providers in `config/providers.lua` match installed resources.
2. Start server and check console for startup validation errors.
3. Run `/m4i:debug` (server console or in-game with permission) to inspect:
- provider resolution
- domain status
- service status
- plugin/hook/middleware state
- metrics state
4. Confirm no domain is unexpectedly soft-disabled.
5. Trigger one callback and one notify/progress flow from a test script.

## Common mistakes

- Starting `m4i_bridge` before provider resources.
- Selecting a provider that is not installed or named differently.
- Assuming autodetect is primary control (it is fallback only when enabled).
- Using direct framework APIs in scripts instead of bridge exports.
- Enabling strict/safe flags in production without validating dependent scripts first.
