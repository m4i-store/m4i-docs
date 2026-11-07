# M4I Garage — Complete Installation, External Script Edits & Go-Live Guide

**Current source:** Garage `0.1.139-alpha`, Bridge `1.5.19-rc.1`, Upload `0.2.1-alpha`. Reviewed against the M4I / QBCore / ESX / Qbox test resources on **7 November 2026**. This is the **master customer checklist**, replacing historical versioned test reports as installation guidance.

**Scope:** This guide identifies every installation-time configuration and supported external script change found in these shipped resources. A third-party fork may use different functions or paths: follow its own documentation and implement/test a matching Bridge adapter; no finite guide guarantees every unknown vendor API.

## 0. Read before changing anything

- **Mandatory for Garage:** FXServer with OneSync, `oxmysql`, a working **single** framework supported by M4I Bridge, `m4i_bridge`, `m4i_garage`, and Garage's SQL tables.
- **Conditional:** radial menu OR Garage `keys` mode; a supported Target for NPC-based impound/police actions; verified vehicle classification source; a working framework inventory and personal payment provider for item/fee features.
- **Optional:** `m4i_upload` for shared image IDs; LB/QS custom phone integration; `vehicle_cover`; external vehicle keys, dispatch, mechanic, dealership or a custom radial/target adapter.
- **Customer responsibilities:** configure their pre-existing scripts, define missing inventory items, authorize their exact external server resource names, and remove conflicting garage controllers **only when replacement coverage is confirmed**.
- **Never copy:** `m4i_test_compat`, test-only events/SQL fixtures, admin test-money code, or txAdmin test presets into a production customer server.
- **Back up first:** each framework's database (including `player_vehicles` or `owned_vehicles`), `server.cfg`, resource config, inventory item registry, Garage `data/`, and Upload `data/`. Test on a copied/staging database, not the production DB.

## 1. Extract only the inner FiveM resources

```text
resources/
  [m4i]/
    m4i_bridge/fxmanifest.lua
    m4i_garage/fxmanifest.lua
    m4i_upload/fxmanifest.lua       # optional
    m4i_cover_ox_adapter/          # only for ox_inventory vehicle_cover Use
```

Inside downloaded ZIPs, **do not** preserve wrapper folders named `m4i_garage [open-source]` or `m4i_bridge [escrow]` around the actual resource. The directory name is an API identifier. Bridge requires its own `adapters/`, `config/`, `shared/`, `services/` folders; Garage requires its `web/`, `client/`, `server/`, `shared/`, `sql/`, `stream/`. Do not unpack only `fxmanifest.lua`.

For `m4i_upload` upgrades preserve `data/index.json`, `data/assets/`, `data/backups/` and `data/audit.json`. Its image IDs are global and should not be recreated or copied into individual category folders.

**Important license note:** a file named `[escrow].zip` and `escrow_ignore` do not produce encrypted Cfx Asset Escrow. The actual protected version must be published through the appropriate Cfx process. Images, custom model assets and third-party dependencies must be distributed only with compatible licenses.

## 2. Which exact files must the customer edit?

| File / subsystem | Required when | What to do |
| --- | --- | --- |
| `server.cfg` | Always | Add ordered `ensure` entries for installed dependencies, Bridge and Garage; remove stale conflicting `setr` values; choose admin ACEs |
| `m4i_bridge/config.lua` | Always | Choose real `Framework` and registered adapter IDs for Inventory/UI/Notify/Progress/Radial/Target/Phone/Keys/Banking/etc. |
| `m4i_garage/config.lua` | Always | Set `InteractionMode` (`radial` or `keys`), police jobs, vehicle cover cooldown, fees, optional integrations and trusted resource allowlists |
| `m4i_garage/sql/install.sql` | Always | Review and import into the **right** framework DB after full backup |
| Framework inventory item file/SQL | Only if using `vehicle_cover` | Add the exact item and correct no-auto-consume Use callback; inventory-specific guide below |
| Inventory `phone` item definition | Only if using Garage phone UI/valet features | Make sure player can actually carry an item with **exact name `phone`**; Garage checks this server-side |
| `m4i_cover_ox_adapter` | Only for **Ox Inventory** cover Use | Install a tiny client resource; this is **not** automatically supplied by Bridge's Ox server provider |
| Dealership vehicle purchase script | Only when it must create Garage vehicles | Add an **authenticated server** call to `RegisterOwnedVehicle` after successful purchase; allowlist its exact resource name |
| Mechanic/repair script | Only for trusted full repair integration | Use a server-side Garage permit / verified repair flow; add exact resource name to `Config.RepairTrustedResources` |
| External radial/target/UI/notify/phone/keys/dispatch resource | Only if its bundled adapter does not match the installed fork | Implement and register a dedicated Bridge adapter, test add/remove/callbacks and error paths |
| `m4i_bridge/adapters/vehicles/manual/server.lua` | If custom/addon model classification is missing | Define verified model, GTA class and category, or provide an equivalent authoritative catalog |
| Old garage/phone/vehicles scripts | Only if they conflict with new Garage ownership | Audit exports/SQL/events/dependencies before disabling old gameplay; keep safe compatibility shims where needed |

The absence of an optional provider must not prevent **basic** Garage Open/Store if you configure a supported alternative and do not enable that optional feature.

## 3. Five framework configurations — install only what exists on your base

The matching Bridge framework identifiers are **`m4i`, `qbcore`, `qbox`, `esx`, `ox_core`**. The Qbox identifier is **`qbox`**, even if the server is called QBX. One framework per installation. In `m4i_bridge/config.lua` set `M4IBridgeConfig.Framework`; `'framework'` in each other field selects the shipped default for that domain, not arbitrary vendor auto-support.

| Framework | Actual core | Default Bridge Inventory | TextUI | Default Radial | Default Target |
| --- | --- | --- | --- | --- | --- |
| M4I | `m4i_core` | `m4i_inventory` | `m4i_hud` | `m4i_radialmenu` | `m4i_target` |
| QBCore | `qb-core` | `qb_inventory` (`qb-inventory`) | `qb_textui` (`qb-core` DrawText/HideText) | `qb_radialmenu` | `qb_target` |
| Qbox / QBX | `qbx_core` | `ox_inventory` | `ox_lib` | `qbx_radialmenu` | `ox_target` |
| ESX Legacy | `es_extended` | `esx_inventory` (change to `ox_inventory` if used) | `esx_textui` | `m4i_radialmenu` or switch Garage to keys | `ox_target` |
| Ox Core | `ox_core` | `ox_inventory` | `native` | `m4i_radialmenu` or keys | `ox_target` |

The rows describe shipped **profiles**, not a promise that the listed third-party resources exist on every customer server. A missing selected provider must be resolved, not papered over with a fake `ensure` line. Ox Core adapter has source-level support but still needs live acceptance.

### Native M4I — example server.cfg

```cfg
ensure oxmysql
ensure m4i_registry
ensure m4i_core
ensure m4i_inventory
ensure m4i_hud
ensure m4i_target
ensure m4i_radialmenu
ensure m4i_bridge
ensure m4i_upload
ensure m4i_garage
```

Keep only your **real** installed optional providers. If using native inventory, confirm its `shared/items.lua` includes `vehicle_cover` when covers are enabled. Never duplicate native M4I player money or identifiers in external SQL.

### QBCore — example server.cfg

```cfg
ensure oxmysql
ensure qb-core
ensure qb-inventory
ensure qb-target
ensure qb-radialmenu
ensure progressbar
# ensure m4i_registry  # if using its vehicle classification
ensure m4i_bridge
ensure m4i_upload
ensure m4i_garage
```

Set Bridge `Framework='qbcore'`. Verify `qb-core/shared/items.lua` defines `vehicle_cover` **if covers enabled** and `phone` **if using Garage Phone**. Garage/Bridge registers the QBCore `vehicle_cover` use handler at runtime; do not create a duplicate `QBCore.Functions.CreateUseableItem`. QBCore uses native player money; **`qb-banking` business accounts are not character bank balances**. `qb-phone` depends on its own garage callbacks and native ownership tables; see Sections 6 and 8 below.

### Qbox/QBX — example server.cfg

```cfg
ensure oxmysql
ensure ox_lib
ensure qbx_core
ensure ox_inventory
ensure ox_target
ensure qbx_radialmenu
# ensure m4i_registry  # only with its compatible vehicle catalog
ensure m4i_bridge
ensure m4i_upload
ensure m4i_garage
# ensure m4i_cover_ox_adapter # ONLY if enabling vehicle_cover
```

Set Bridge `Framework='qbox'`. Qbox's `qbx_vehiclekeys`, `qbx_vehicles`, `qbx_garages`, NPWD integration and phone/repair forks are **separate dependencies**. The presence of `player_vehicles` does not make every `qbx_garages` export available. Check native garage API consumers **before** disabling the old garage gameplay resource. For covers, add `ox_inventory/data/items.lua` item definition, with `consume=0`, **and** install the Ox Use client adapter.

### ESX Legacy — example server.cfg

```cfg
ensure oxmysql
ensure es_extended
# ensure esx_inventory OR ox_inventory (choose your actually installed inventory)
# ensure ox_lib if required by your installed providers
ensure ox_target
# ensure m4i_radialmenu if you actually use a compatible radial
ensure m4i_bridge
ensure m4i_upload
ensure m4i_garage
```

Set Bridge `Framework='esx'` and set `Inventory='ox_inventory'` **only if you actually use Ox** (otherwise retain `esx_inventory`). If no compatible radial, `m4i_garage/config.lua` **`Config.InteractionMode='keys'`**. When ESX default inventory is selected, define `vehicle_cover` in the correct **`items` SQL schema/vendor item registry**; its use callback is registered through Bridge. Default ESX item storage has no Ox/QB slot metadata, so the cover life ledger is per-owner and transfer/drop of partly used covers requires special care. Other ESX inventory forks may require a separate adapter.

### Ox Core

Start `oxmysql`, `ox_lib`, actual `ox_core`, `ox_inventory`, supported `ox_target`, Bridge and Garage. Set `Framework='ox_core'`, configure the actual UI/keys/radial/notify/phone providers, use `keys` interaction if no radial. Do not assume Ox Core players, banks, identity or native garage tables are interchangeable with QB/ESX. Test in-game because this profile is not included in the four currently running test bases.

## 4. Mandatory Garage settings after selecting Bridge

In `m4i_garage/config.lua`:

```lua
Config.InteractionMode = 'radial'      -- change to 'keys' if no supported radial
Config.InteractionOpenKey = 'E'
Config.InteractionStoreKey = 'H'
Config.SpawnClearance = 3.0
Config.CoverActionCooldownSeconds = 15
Config.VehicleCoverItem = 'vehicle_cover'
Config.CreatorAce = 'm4i.garage.admin'
Config.AuthorizedSeizureJobs = { police = 0, sheriff = 0, fib = 0 }
Config.TrustedVehicleRegistrars = {} -- add ONLY real trusted dealership resource names
```

These are **selected excerpts of an existing file**, not replacement contents. Preserve every other setting and its default. Radial items show only in valid 3D zones near configured spawn bays. `keys` mode provides **E Open / H Store** without radial; police/impound NPCs still require a compatible Target. Check your server's actual keys, radial icons, menu add/remove exports and target entity remove semantics.

Give trusted admins the ACE using your server's existing principal structure:

```cfg
add_ace group.admin m4i.garage.admin allow
add_ace group.admin m4i.upload allow  # only if installing Upload
```

Your existing `add_principal` must already map real trusted staff into `group.admin`; **never grant staff ACEs to every player**. In-game Garage Creator command is `/garagecreator`; server console diagnostic is `m4ig_doctor`; Bridge has `m4i:debug`. Commands, roles and UI read permissions are **not** a replacement for server-side ownership authorization.

## 5. Inventory items — mandatory only when their features are used

**`vehicle_cover`**: the exact item is required for the cover system, but **not for ordinary Garage Open/Store**. Customer must add an item definition to their real inventory; QB/ESX use callback registered by Garage/Bridge after the item exists; Ox requires an independent client Use adapter. Set `consume=0`: the successful Cover action, not the click, consumes **one of five uses**. Review the working, copyable item and companion-resource snippets in **[Vehicle Cover Installation](vehicle-cover-item.md)**. Do not package the test helper `m4i_test_compat` as a production dependency.

**`phone`**: Garage's phone list and AI delivery handler call Bridge `HasItem(source,'phone',1)`. Even after LB Phone or QS Smartphone registers a custom app, a player missing **an inventory item literally named `phone`** can receive `PHONE_REQUIRED`. This is a real source-code restriction. Check your inventory item definitions, trading rules and item granting. If a custom phone vendor uses a different name (e.g. `smartphone`), the shipped Garage does **not** expose a simple `Config.PhoneItem` toggle: a tested adapter/code change is required; do not pretend a `Phone` Bridge selector renames the item.

**Images**: QB inventory may need local `vehicle_cover.png` under its actual images folder, unless its UI has been explicitly wired to `m4i_upload` through Bridge. A global Upload ID does **not** cause every unrelated inventory UI to render an image automatically.

## 6. Existing owned cars, SQL, dealerships, and old garage scripts

1. Inspect and back up existing framework-native vehicle rows and schemas: QB/Qbox typically `player_vehicles`, ESX typically `owned_vehicles`. Keep primary keys, finance, mods/properties, state, job and plate columns.
2. Import the shipped **`m4i_garage/sql/install.sql`** into the correct DB. This creates Garage's `m4ig_*` tables. Do **not** clear the native tables or overwrite them with a sample test schema.
3. **Garage does not auto-import existing vehicles** simply because `player_vehicles` / `owned_vehicles` exist. Plan an explicit backup + dry-run + collision/identity/plate reconciliation before adopting old rows; do not assume `m4ig_vehicles` is magically populated.
4. `Config.NativeVehicleCompatibility.Enabled` is **off by default**. In the test environment, enabling this projects **already Garage-owned vehicles** to native read-compatible tables for QB/ESX/Qbox; it is **not** native-table-first storage and is **not** reverse migration. With `SyncIntervalMs=0` it performs startup projection and subsequent Garage actions emit event-based projection, rather than a recurring 15s full-table scan.
5. Stop duplicate garage **gameplay** for the same car only after auditing scripts that still require old `qb-garages`, `qbx_garages` or `esx_garage` exports/events. A vendor's housing, phone, police, key or mechanic script may hard-depend on its garage resource name. Compatibility shims must be implemented/tested separately; **do not rename M4I Garage to the vendor name**.
6. For **new vehicle sales**, call `exports.m4i_garage:GetGarageCharacterId(src)` from the trusted dealership server after character load. Put its exact invoking resource name in `Config.TrustedVehicleRegistrars`; after validated payment/ownership/plate/class/garage selection, call:

```lua
local id, why = exports.m4i_garage:GetGarageCharacterId(src)
if not id then return false, why end
-- Run ONLY inside a trusted dealership *server* resource after successful purchase.
local ok, garageVehicleId = exports.m4i_garage:RegisterOwnedVehicle(
    id, plate, model, category, properties, garageId, spawnType, verifiedVehicleClass
)
```

This is a **partial integration example**. Your dealership must supply valid server-authoritative values and avoid double charges/duplicate plates. `category` is one of `land`, `water`, `air`; GTA class is validated; `spawnType` must match actual vehicle type. A client-provided ID is never proof of ownership.

7. For custom addon vehicles that your server lacks in Registry, add a verified entry in `m4i_bridge/adapters/vehicles/manual/server.lua` and select `Vehicles='manual'` or a supported auto fallback. Example:

```lua
local Models = {
    my_custom_car = {
        Label = 'My Custom Car',
        Class = 6,
        Type = 'automobile',
        Category = 'land'
    }
}
```

Do **not** replace the entire shipped adapter with this excerpt; populate its existing `Models` table. Verify real GTA class and Garage bay category. `m4i_registry` is the native M4I catalog; a third-party framework can use a verified manual or custom classification provider instead.

## 7. Integrating existing third-party scripts

| System already on the customer's server | What must be checked/changed |
| --- | --- |
| `qb-radialmenu`, `qbx_radialmenu`, `m4i_radialmenu` | Select the registered Bridge Radial ID; verify vendor `AddOption` and `RemoveOption`, nested child options, FontAwesome icon names and zone entry/exit cleanup |
| `qs-radialmenu` or custom radial | Select `qs_radialmenu` only on matching vendor API; for any untested fork, implement a dedicated Bridge adapter; if impossible use Garage keys mode |
| `ox_target`, `qb-target`, `m4i_target` | Choose the matching Bridge Target ID and test register/remove for the *actual* NPC entity and zone, job requirements and reconnect |
| Unknown third-party Target | Implement both add **and remove** exports in a Bridge `adapters/target/` module; never return false success |
| TextUI, Notify and Progress | Choose actual Bridge IDs (`qb_textui`, `esx_textui`, `ox_lib`, `framework`, `progressbar`, `esx_progressbar`, etc.); menus are not interchangeable with text prompts |
| Vehicle keys | A compatible `qb_vehiclekeys` or `qbx_vehiclekeys` adapter may be selected in Bridge `Keys`; verify granting and `HasKeys` on actual plate/entity; other vendors need their own adapter |
| `qb-banking`, `renewed-banking`, ESX accounts | Test **personal** balance debit, insufficient funds and refunds through Bridge; never use society balance or manual SQL to pay an individual driver's impound |
| LB Phone | Set Bridge `Phone='lb_phone'`; real `lb-phone` resource must support `AddCustomApp` / `RemoveCustomApp`; player still needs `phone` item |
| QS Smartphone | `Phone='qs_smartphone'` expects `qs-smartphone` with `addCustomApp` / `removeCustomApp`; require `phone` item |
| QB Phone | Its existing Garage UI depends on QB callbacks and native ownership SQL; `NativeVehicleCompatibility.QbPhoneCallback` is a scoped compatibility option, **not** generic embedded-app support |
| NPWD / Qbox Phone | Needs a companion app/backend and possibly original `qbx_garages` APIs; native SQL alone is not sufficient to promise compatibility |
| Police/impound/seize | Update `Config.AuthorizedSeizureJobs` for exact job names/grades; test grade, retrieval fee, payment, cleanup and targeting; no broad job bypass |
| Mechanic, QS Repair or repair creator | Add trusted exact server script names to `Config.RepairTrustedResources` and use Garage's `AuthorizeFullRepair` / `BeginFullRepair` permit integration; do not bypass the server with client-only full repair |
| Blips or vehicle preview images | Use Bridge exports; add an NUI consumer adapter for any vendor UI not already integrated |
| AI valet / GPS | Configure Garage fees and enable deliberately; `phone` item is checked and server-side money charge/refund must be exercised |
| Custom vendor overall | Copy `m4i_bridge/adapters/_templates/<domain>/`, implement real export argument/return transformations, select the provider ID in Bridge `config.lua`, and test its restart/error paths |

The shipped code **does not** automatically edit `qb-phone`, `qbx_garages`, `esx_garage`, third-party keys or mechanic scripts. Customers must implement and test the missing vendor compatibility layer when their exact resource requires it. See [Bridge Adapter Guide](../../core/m4i_bridge/third-party-providers.md) and [Integration Recipes](integration-recipes.md).

## 8. Garage Creator, assets, and gameplay setup

- Run **`/garagecreator`** with the proper admin permission. Add 3D PolyZones, enough safe spawn bays, valid map coordinates/Z, category/class restrictions, NPC placement, and garage access rules. Review public, shared, VIP, police seized and impound types separately.
- Public garages are not automatically populated with the server's full world of vehicles. Only registered/allowed vehicles in their intended Garage custody flow should be exposed.
- The shipped `data/garage_presets.json` contains **reference presets**, not necessarily active garages appropriate for every custom map.
- GTA cover props depend on installed stream YTYP and available YDR/YTD model data. The resource may safely fall back to native cover props; do not claim a custom 3D object exists unless all its streamed assets are licensed, included and loaded. Check F8 for missing archetypes.
- Cover allowed/denied zones, ownership permissions, transparency/collision, removal cooldown and restart recovery must be verified on the customer's mapping.
- Test OneSync with at least two clients (stream in/out), blocked spawn (3m), Store/Take, persistence and full/partial repair. Live damage snapshots are **not** the same as database snapshots until updated.

## 9. Start, verify, and repair failures

1. **Before boot:** select one framework; verify exact resource names, `oxmysql`, SQL schema and correct `server.cfg` order. Any legacy `setr m4i_bridge_profile` overrides `Framework` from `config.lua`; remove contradictory convars.
2. **Boot/restart:** start framework and installed vendor providers first, then Bridge, optional Upload, then Garage. Restart a live production server only during maintenance when players' vehicles can be safely saved.
3. **Console check:** `m4ig_doctor` from **server console**, `m4i:debug` for Bridge, and logs confirming `Started resource m4i_bridge`, `Started resource m4i_garage`. Upload logs its image catalog ready state.
4. **Player check:** character loaded, mapped identity, Garage Open/Store/Take, outside-zone rejection, admin creator, radial/keys, NPC target, personal bank fee, insufficient balance, cover item Use, phone item, and vehicle persistence after restart.
5. **Compatibility check:** with a different framework's phone, mechanic, dealership, keys and radial vendor, test the **actual** exports and native SQL rows, not only whether both resources say “started”.
6. **Review F8 and FXServer:** verify no provider unready errors, missing item definition, SQL conflict, oxmysql error, malformed NUI image, or stale radial cleanup.
7. **Rollback:** preserve pre-change SQL and configs, restore matching Bridge/Garage versions together, then rebuild/restart only during a maintenance window. Keep Upload's original `data/` intact.

## 10. Final go-live signoff

Use [Customer QA Checklist](../../shared/fivem-qa-checklist.md) together with this guide. The release is not production-verified merely because the resources boot. Verify on the customer's specific versions and at least two real game clients. No unsupported script may be advertised as plug-and-play without its matching tested adapter.

**Other required pages:** [Vehicle Cover item + Ox event](vehicle-cover-item.md), [Bridge Setup](../../core/m4i_bridge/setup-selector.md), [Bridge Provider Matrix](../../core/m4i_bridge/third-party-providers.md), [Upload Complete Setup](../m4i_upload/installation.md).