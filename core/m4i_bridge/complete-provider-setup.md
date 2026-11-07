# M4I Bridge — Complete Installation and Editing Third-Party Scripts

**Shipped revision:** `m4i_bridge 1.5.19-rc.1` · **Garage:** `0.1.139-alpha` · 7 November 2026. Start here if your FiveM server has non-M4I inventory, radial, target, phone, keys, banking, dispatch, progress, text UI, or custom scripts.

## 1. Mandatory versus optional

The Bridge is a **runtime integration layer**, not a replacement framework, inventory, database or UI. Install a **healthy** one of `m4i_core`, `qb-core`, `qbx_core`, `es_extended`, or `ox_core` **before** Bridge. Bridge's `fxmanifest.lua` loads `@oxmysql/lib/MySQL.lua` server-side: install and start `oxmysql` before it. Vendor providers (e.g. `qb-target`, `ox_target`, `qb-radialmenu`) are **not bundled** by Bridge. They must be present, licensed and started if selected.

**Configure `m4i_bridge/config.lua`**. Never replace an entire adapter registry file with a documentation fragment; copy only a value inside the existing `M4IBridgeConfig` table.

```lua
M4IBridgeConfig = {
    Framework = 'qbcore',   -- or 'm4i', 'qbox', 'esx', 'ox_core'
    Inventory = 'framework',
    UI = 'framework',
    Notify = 'framework',
    Progress = 'framework',
    Radial = 'framework',
    Target = 'framework',
    Phone = 'auto',
    Vehicles = 'auto',
    Keys = 'framework',
    Dispatch = 'framework',
    Banking = 'framework',
    Appearance = 'framework',
    Database = 'framework'
}
```

**One framework.** A legacy `setr m4i_bridge_profile` in `server.cfg` overrides the Lua framework selection. A legacy `setr m4i_bridge_phone` or a `setr m4i_bridge_<domain>` override may also change a domain: audit old `setr` lines and remove conflicts. Unknown or unavailable explicit adapters should fail closed. Do not use `auto` to imply any unregistered vendor is supported.

## 2. Complete shipped provider/actual vendor matrix

| Domain in `config.lua` | Actual adapter IDs | External resource or required edit |
| --- | --- | --- |
| `Framework` | `m4i`, `qbcore`, `qbox`, `esx`, `ox_core` | `m4i_core`, `qb-core`, `qbx_core`, `es_extended`, `ox_core` |
| `Inventory` | `m4i_inventory`, `qb_inventory`, `ox_inventory`, `esx_inventory` | Only actual installed inventory; define missing vendor item names separately |
| `UI` | `m4i_hud`, `qb_textui`, `esx_textui`, `ox_lib`, `qb_menu`, `native`, `custom` | `qb_textui` maps QB DrawText/HideText; `qb_menu` is not text UI |
| `Notify` | `framework`, `m4i_hud`, `ox_lib`, `native`, `custom` | Real QBCore, Qbox or ESX notify API; test payload type and user feedback |
| `Progress` | `ox_lib`, `progressbar`, `esx_progressbar`, `native`, `custom` | Match the installed progress provider's cancellation and duration methods |
| `Radial` | `m4i_radialmenu`, `qb_radialmenu`, `qbx_radialmenu`, `qs_radialmenu`, `custom` | `qb-radialmenu`, `qbx_radialmenu` etc; correct AddOption/RemoveOption signatures; no shipped `ox_lib` radial adapter |
| `Target` | `m4i_target`, `ox_target`, `qb_target`, `custom` | Real entity/zone/model add+remove callbacks; `qb-target` and `ox_target` have different cleanup identifiers |
| `Phone` | `auto`, `lb_phone`, `qs_smartphone`, `disabled` | `lb-phone` or `qs-smartphone` custom-app APIs; QB Phone/NPWD require separate compatibility path |
| `Keys` | `qb_vehiclekeys`, `qbx_vehiclekeys`, `disabled`, custom registered adapter | `qb-vehiclekeys` keys by plate, `qbx_vehiclekeys` keys by server vehicle entity; no generic compatibility guarantee |
| `Banking` | `framework`, `qb_banking`, `renewed_banking`, `auto` and custom adapter | Use **personal** framework money; do not query QB society/business banking for player fees |
| `Dispatch` | `none`, `ps_dispatch`, `cd_dispatch`, `qs_dispatch` | Vendor events/exports must match actual installed release |
| `Vehicles` | `auto`, `manual` and custom registered adapter | Native registry or `adapters/vehicles/manual/server.lua` entries, GTA class and category |
| `Appearance` | `auto` and vendor adapter | Check the vendor's current client API and appearance contract before selecting |
| `Database` | `framework` => `oxmysql` | Database schema/backups and permissions remain the customer's responsibility |

**IDs are not folder names:** `qbox` uses `qbx_core`; `qb_inventory` uses `qb-inventory`; `qb_target` uses `qb-target`; `qb_vehiclekeys` uses `qb-vehiclekeys`; `lb_phone` uses `lb-phone`.

## 3. What customers actually need to edit in OTHER scripts

### Inventory

The Bridge maps API operations but does **not automatically insert** a new item into QB, Ox, ESX or M4I catalog. For Garage Cover, define `vehicle_cover` in the selected inventory and ensure usable item emits the correct validated slot; **do not auto-consume** on Use. For Garage phone list/valet, player must possess the inventory item **`phone`**. A different phone item name requires a real Garage adaptation, not just a Bridge `Phone` setting. Full copyable snippets are in [Vehicle Cover Item Setup](../../scripts/m4i_garage/vehicle-cover-item.md).

### Radial

Make sure the vendor resource is started **before Bridge**, select its Bridge adapter ID and verify the menu appears in a valid Garage zone, with correct icon names, click and remove-on-exit behaviour. `qb-radialmenu` often expects FontAwesome icon names; `qbx_radialmenu` needs its vendor-specific item label schema. To use an unsupported radial, copy `adapters/_templates/radial/client.template.lua` to a new adapter folder and write a real translation layer, or use Garage's `Config.InteractionMode='keys'` instead. Do not add arbitrary `ox_lib` radial IDs unless you built the adapter.

### Target

Bridge's `ox_target` handles local entity add/remove differently from `qb-target`. Ensure vendor NPC target methods actually return the required handle or status; an event-only fire-and-forget script is not automatically compatible. Copy `adapters/_templates/target/client.template.lua` to a named adapter and implement add/remove entity, box, model and optional sphere/global methods the customer needs.

### Keys

QB plate-based keys and QBX entity-based keys are **different contracts**. For a custom garage to grant vendor keys, set Bridge `Keys` to a working adapter and test the actual server export and `HasKeys`. Do not assume installing a keys resource means the selected adapter is active. A new vendor requires an adapter in `adapters/keys/<vendor>/server.lua` that checks vehicle ownership/permission on the trusted server route.

### Banking and personal money

Use the framework's actual personal account for Garage transfer, GPS, impound, insurance and valet. Do not confuse **`qb-banking` shared/job accounts** with player checking or ESX society accounts. To support a custom banking fork, adapt `adapters/_templates/banking/server.template.lua` to the current get/remove/refund contract, with integer bounds and verified result; no SQL write directly to a player's bank table.

### Phones

- `lb-phone`: Bridge `Phone='lb_phone'` needs real `AddCustomApp/RemoveCustomApp`.
- `qs-smartphone`: `Phone='qs_smartphone'` needs `addCustomApp/removeCustomApp`.
- `qb-phone`: Bridge does **not** embed a Garage custom iframe into stock QB Phone; Garage's QB vehicle-list callback and native table compatibility are separate.
- `NPWD`: implement a real companion NPWD app/backend. Native Qbox phone apps may depend on `qbx_garages` exports, not just a SQL table.
- No phone: select `Phone='disabled'`. Garage's normal physical storage does not require a custom-phone app.

### Repair, dealership, police

These are **Garage-specific** integrations, not general Bridge provider flags. Add a trusted dealership resource to `Config.TrustedVehicleRegistrars` and invoke `RegisterOwnedVehicle` server-side after purchase using `GetGarageCharacterId`. Add trusted server mechanic resources to `Config.RepairTrustedResources`; use `AuthorizeFullRepair` / `BeginFullRepair` and test full/partial damage persistence. Configure exact police job names in `Config.AuthorizedSeizureJobs`; target options must still enforce server role validation. See [Complete Garage Installation](../../scripts/m4i_garage/complete-installation.md).

### Dispatch, Appearance, TextUI, Notify and Progress

For each optional vendor, examine the shipped adapter `adapters/<domain>/<provider>/client.lua` or `server.lua`. Verify resource name, exported function names, payload and cancellation/cleanup. If vendor is not exactly supported, create a new adapter rather than changing `m4i_garage` gameplay modules.

### Vehicle models / addon dealerships

Use `m4i_registry` when the matching M4I vehicle catalog is available, or populate `m4i_bridge/adapters/vehicles/manual/server.lua` with **verified** model names/GTA classes and matching `Type`/`Category`. `Vehicles='auto'` can fall back to the manual list, but no unknown vehicle will classify correctly merely because an addon model streams.

## 4. How to implement a vendor adapter

1. Look at the real third-party resource's API docs/source and record its **exact resource name, client/server side, export arguments, return values, and remove behaviour**.
2. Choose one Bridge domain, e.g. `target`, `radial`, `keys`, `inventory`, `notify`, `banking`, `phone`, `dispatch`.
3. Copy the matching file from `m4i_bridge/adapters/_templates/<domain>/` into `m4i_bridge/adapters/<domain>/your_vendor/client.lua` or `server.lua`; update `meta.provider`, `meta.dependencies` and `implemented=true` **only when functionality is genuinely implemented**.
4. Call `Bridge.registerAdapter('<domain>','your_vendor','client' or 'server',adapter)` and implement the domain's methods with meaningful failures. The Bridge manifest's `adapters/**/client.lua` and `adapters/**/server.lua` patterns load these folders automatically.
5. Select the exact registered ID in `m4i_bridge/config.lua` (for example `Target='your_vendor'`). Start its upstream resource before Bridge.
6. Test vendor start-stop, client reconnect, two-player action, add/remove, unavailable resource, duplicate ID, permission refusal, and no ghost radial/target options. **A working startup alone is not proof.**

The shipped generic `custom` radial and target adapters also have an **editable local `resource` + export names** in `adapters/radial/custom/client.lua` and `adapters/target/custom/client.lua`. They do not translate arbitrary vendor payloads; copy a dedicated adapter when the argument shape differs. Do not put imaginary `resource` or `addExport` fields into the customer's main `config.lua`.

## 5. Correct boot and diagnostics

```text
oxmysql
→ one chosen framework
→ installed inventory + ox_lib/UI + radial + target + other selected vendors
→ m4i_bridge
→ m4i_upload (optional)
→ m4i_garage
→ customer's separately written companion adapters (if needed)
```

Real `server.cfg` examples for all five profiles are in [Complete Garage Installation](../../scripts/m4i_garage/complete-installation.md). Avoid starting a resource twice through both a whole folder `ensure [qb]` and an individual `ensure qb-core`.

**Diagnostics:** `m4i:debug`; server console `m4ig_doctor`; verify Bridge framework and per-domain readiness. Test player login, inventory, money, commands, NPC target, phone, keys, cover action, database and restart. Admin ACEs must use real server principals. The test-only `m4i_test_compat` is **not** a distribution dependency.

**Important:** the Garage's initial SQL installer is **not all possible runtime schemas**. Some Garage features initialize additional `m4ig_*` tables when enabled/started, and ESX cover usage may initialize `m4i_bridge_esx_cover_uses`. Give a migration user required schema privileges in a controlled maintenance window, or pre-apply exact versioned schema with a database administrator; production player DB credentials should not be given broad permanent DDL rights without a deliberate operational policy.

**Read next:** [Garage complete install](../../scripts/m4i_garage/complete-installation.md), [Vehicle Cover item](../../scripts/m4i_garage/vehicle-cover-item.md), [M4I Upload integrations](../../scripts/m4i_upload/integration.md), [Go-live QA](../../shared/fivem-qa-checklist.md).