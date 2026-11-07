# M4I Bridge — Installation & Framework Selector

> **CURRENT INSTALLATION — READ FIRST:** [Full installation and every third-party script edit](complete-provider-setup.md). This page is a companion guide; the full guide includes SQL, items, third-party script edits, provider compatibility and go-live steps. Also review [Source-audited limitations](../../shared/fivem-install-known-limitations.md).


**Applies to:** `m4i_bridge 1.5.19-rc.1`, `m4i_garage 0.1.139-alpha`, `m4i_upload 0.2.1-alpha` (source reviewed 7 November 2026).

This guide lets a server owner **choose their existing framework and installed scripts**. You do **not** have to replace your inventory, target, radial, notifications, phone, or banking system to install M4I. Each optional integration works only if a matching Bridge adapter exists and the resource passes readiness tests.

## 1. Choose your framework — exactly one

| Your base | Set `Framework` | Actual framework resource | Standard inventory | Standard target | Radial choice |
| --- | --- | --- | --- | --- | --- |
| Native M4I | `m4i` | `m4i_core` | `m4i_inventory` | `m4i_target` | `m4i_radialmenu` |
| QBCore | `qbcore` | `qb-core` | `qb-inventory` | `qb-target` | `qb-radialmenu` |
| Qbox / QBX | `qbox` | `qbx_core` | `ox_inventory` | `ox_target` | `qbx_radialmenu` |
| ESX Legacy | `esx` | `es_extended` | `esx_inventory` **or** supported `ox_inventory` | `ox_target` | `m4i_radialmenu`, compatible adapter, or keys mode |
| Ox Core | `ox_core` | `ox_core` | `ox_inventory` | `ox_target` | compatible radial or keys mode |

These are **example combinations**, not mandatory installations of every item shown. Ox Core and vendor forks require additional in-game validation. Do not choose QBCore just because Qbox provides a QB compatibility API: select `qbox` when `qbx_core` is your real framework.

## 2. Install the folders

Extract the **inner resource** folders directly:

```text
resources/
└── [m4i]/
    ├── m4i_bridge/fxmanifest.lua
    ├── m4i_upload/fxmanifest.lua       (optional, for global images)
    └── m4i_garage/fxmanifest.lua       (optional, for garage)
```

Never keep an extra wrapper such as `m4i_bridge [open-source]/m4i_bridge/` inside `resources/[m4i]`. Do not rename the inner folders. `m4i_bridge` requires `oxmysql`; `m4i_garage` explicitly depends on `m4i_bridge` and `oxmysql`. `m4i_upload` has no mandatory framework dependency; Bridge is recommended for consumer integrations.

## 3. Select in **one customer-editable config file**

Edit `resources/[m4i]/m4i_bridge/config.lua`, **not** the internal `config/providers.lua`. Change existing values in the full file; do not replace the file with this fragment:

```lua
M4IBridgeConfig = {
    Framework = 'qbox',        -- m4i / qbcore / qbox / esx / ox_core
    Inventory = 'framework',   -- or a registered adapter ID
    UI = 'framework',          -- or ox_lib / qb_textui / esx_textui / native / ...
    Notify = 'framework',
    Progress = 'framework',
    Radial = 'framework',      -- or qb_radialmenu / qbx_radialmenu / m4i_radialmenu / ...
    Target = 'framework',      -- or qb_target / ox_target / m4i_target / custom
    Phone = 'auto',            -- auto / lb_phone / qs_smartphone / disabled
    Vehicles = 'auto',
    Keys = 'framework',
    Dispatch = 'framework',
    Banking = 'framework',
    Appearance = 'framework',
    Database = 'framework'
}
```

`'framework'` uses the installed profile's configured provider; `'auto'` is **not** universal support for any plugin. An explicit missing provider fails closed instead of silently choosing an unrelated inventory or framework. Legacy `setr m4i_bridge_profile qbox` works, but overrides the Lua framework choice: **do not set conflicting values**. Use only one clear source of truth per deployment.

Default special cases: QBCore uses Bridge `qb_textui`, Qbox uses `ox_lib`, and ESX uses `esx_textui`. Selecting `UI='ox_lib'` requires starting `ox_lib` and validating its available exports. `qb_textui` uses QBCore `DrawText/HideText`; it is not `qb-menu`.

## 4. Startup templates

Use just **one** of the following profiles and keep your framework's normal dependencies. Do not add `ensure` lines for resources you do not own.

**M4I**

```cfg
ensure oxmysql
ensure m4i_registry
ensure m4i_core
# ensure the inventory / UI / target / radial you selected
ensure m4i_bridge
ensure m4i_upload
ensure m4i_garage
```

**QBCore**

```cfg
ensure oxmysql
ensure qb-core
ensure qb-inventory
ensure qb-target
ensure qb-radialmenu
# ensure progressbar if chosen as your progress provider
# ensure m4i_registry if you need its vehicle classification catalog
ensure m4i_bridge
ensure m4i_upload
ensure m4i_garage
```

**Qbox / QBX**

```cfg
ensure oxmysql
ensure ox_lib
ensure qbx_core
ensure ox_inventory
ensure ox_target
ensure qbx_radialmenu
# ensure m4i_registry if your vehicle classification integration uses it
ensure m4i_bridge
ensure m4i_upload
ensure m4i_garage
```

**ESX Legacy**

```cfg
ensure oxmysql
ensure es_extended
# ensure esx_inventory OR ox_inventory, according to Bridge Inventory
# ensure ox_lib if your selected providers need it
ensure ox_target
# ensure m4i_radialmenu only when selected; otherwise use Garage keys mode
ensure m4i_bridge
ensure m4i_upload
ensure m4i_garage
```

**Ox Core (provider available; validate your version)**

```cfg
ensure oxmysql
ensure ox_lib
ensure ox_core
ensure ox_inventory
ensure ox_target
ensure m4i_bridge
ensure m4i_upload
ensure m4i_garage
```

**No radial installed?** Set `Config.InteractionMode = 'keys'` in `m4i_garage/config.lua`: **E** opens, **H** stores inside a valid zone close to a bay. The garage's target-based impound/seizure NPC actions **still require a compatible target adapter**.

## 5. Database & ownership safety

For Garage, **back up your database first**, then import the complete `m4i_garage/sql/install.sql` into **this base's** database once, after reviewing the statements. Never apply test data or SQL to the wrong base. The external framework's native vehicle table and Garage's own tables may both exist: installing the script does **not** silently adopt existing `player_vehicles` / `owned_vehicles` into M4I Garage. Check `Config.NativeVehicleCompatibility` and production readiness before enabling native-table projection. Current release uses event-driven updates (`SyncIntervalMs=0`), not 15-second full-table polling. Prevent two garage controllers from managing the same vehicle simultaneously.

To register newly purchased vehicles use a **trusted server-side dealership** listed in `Config.TrustedVehicleRegistrars`, plus Garage `GetGarageCharacterId(playerSource)` and its server-owned registration flow. Never pass the raw ESX identifier or alphanumeric QB citizen ID as a numeric Garage character ID.

## 6. What happens next

- [Provider chooser for small and large third-party scripts](third-party-providers.md)
- [Garage installation, items, phone and vehicles](../../scripts/m4i_garage/framework-installation.md)
- [Upload installation and image registry](../../scripts/m4i_upload/installation.md)
- [Acceptance checklist](../../shared/fivem-qa-checklist.md)

**Release note:** ZIP packages labelled `[escrow]` do not themselves prove Cfx.re Asset Escrow encryption. Verify uploaded encrypted artifacts in Cfx before advertising a protected build. Source-level tests are not a substitute for an in-game smoke test.