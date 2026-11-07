# M4I Garage — Install on M4I, QBCore, Qbox/QBX, ESX or Ox Core

**Current release:** `m4i_garage 0.1.139-alpha`, `m4i_bridge 1.5.19-rc.1` (7 Nov 2026). Use this guide instead of older 0.1.12x deployment notes.

**You choose your own installed resources.** The Garage does not force its own radial, inventory, phone, notification, or progress bar. Those are selected in **Bridge `config.lua`**. The Garage still owns vehicle custody, 3D zone checks, storage, damage, cover, impound/seize, and server-side authorization.

## Step-by-step installer

1. **Back up:** your full database, `server.cfg`, framework-owned vehicle data, existing Garage resource and `m4i_upload/data` if you use it. Test on staging first.
2. Ensure your existing framework works normally and `oxmysql` is installed.
3. Install the inner resource folders `m4i_bridge`, `m4i_garage` and optionally `m4i_upload` under `resources/[m4i]/`. Do not rename these folders or install nested ZIP wrapper directories.
4. Open `m4i_bridge/config.lua`; set **`Framework`**, then **`Inventory`, `UI`, `Notify`, `Progress`, `Radial`, `Target`, `Phone`, `Keys`** to installed, supported adapters or to profile defaults.
5. For regular garage interaction choose `Config.InteractionMode='radial'` **if a compatible radial is active**, or `'keys'` (E to Open, H to Store) in `m4i_garage/config.lua`. In keys mode, Garage target NPC actions still require a real compatible Target provider.
6. Review the SQL file `m4i_garage/sql/install.sql` and import it into **this framework's database after a backup**. This defines Garage-owned tables; it does not automatically transfer legacy owned vehicles.
7. Start framework → installed inventory/UI/radial/target dependencies → `m4i_bridge` → optional `m4i_upload` → `m4i_garage`. Load `m4i_registry` before native `m4i_core`; on external bases add it only if your chosen vehicle classification source requires it.
8. Set up Garage Creator zones and safe spawn points; imported reference test zones are not your production Garage map.
9. Integrate vehicle purchasing/registration, keys, insurance banking, vehicle cover, optional phone, and existing garage compatibility separately (see [Integration Recipes](integration-recipes.md)).
10. Join with at least two players and follow the [acceptance checklist](../../shared/fivem-qa-checklist.md).

## Copy the profile matching YOUR base

| Real framework | `Framework=` in Bridge | Typical inventory | Typical radial | Typical target | Garage interaction |
| --- | --- | --- | --- | --- | --- |
| Native M4I | `'m4i'` | `m4i_inventory` | `m4i_radialmenu` | `m4i_target` | `radial` |
| QBCore | `'qbcore'` | `qb_inventory` | `qb_radialmenu` | `qb_target` | `radial` or `keys` |
| Qbox / QBX | `'qbox'` | `ox_inventory` | `qbx_radialmenu` | `ox_target` | `radial` or `keys` |
| ESX Legacy | `'esx'` | `esx_inventory` or `ox_inventory` | `m4i_radialmenu` or another implemented adapter | `ox_target` | `keys` or compatible `radial` |
| Ox Core | `'ox_core'` | `ox_inventory` | installed compatible adapter | `ox_target` | `keys` or compatible `radial` |

These are recommended *examples*, not commands to install every listed third-party plugin. Real-world compatibility with modified versions and forks must be checked. **QBX's Bridge framework identifier is `qbox`, not `qbx`.**

### Example QBCore `server.cfg`

```cfg
ensure oxmysql
ensure qb-core
ensure qb-inventory
ensure qb-target
ensure qb-radialmenu
ensure m4i_bridge
ensure m4i_upload
ensure m4i_garage
```

If you do not have `qb-radialmenu`, remove that line and set Garage `Config.InteractionMode='keys'`. Do **not** add a placeholder `ensure`. Configure Bridge `Framework='qbcore'`; its default UI is `qb_textui`. A different installed Inventory or Target needs the appropriate **Bridge adapter**.

### Example Qbox / QBX

```cfg
ensure oxmysql
ensure ox_lib
ensure qbx_core
ensure ox_inventory
ensure ox_target
ensure qbx_radialmenu
ensure m4i_bridge
ensure m4i_upload
ensure m4i_garage
```

Set `Framework='qbox'` in Bridge. QBX/Qbox's callable exports and `ox_lib` TextUI are supported by the shipped adapter, but a custom radial fork may need a new adapter.

### Example ESX Legacy

```cfg
ensure oxmysql
ensure es_extended
# ensure your chosen, installed ESX or Ox inventory
# ensure your target (e.g. ox_target) and its dependencies
ensure m4i_bridge
ensure m4i_upload
ensure m4i_garage
```

Set `Framework='esx'`. Choose `Inventory='esx_inventory'` **only when `esx_inventory` is installed and ready**; otherwise use the supported `ox_inventory` adapter if that is what your server runs. ESX does not supply a universal target, radial or phone. If there is no supported radial, use Garage **keys** interaction. Ensure the intended TextUI provider is actually available. Default Garage `keys` mode is suitable when you do not have a radial.

### Example native M4I

```cfg
ensure oxmysql
ensure m4i_registry
ensure m4i_core
# start configured native inventory / UI / target / radial
ensure m4i_bridge
ensure m4i_upload
ensure m4i_garage
```

Keep `Framework='m4i'`. Do not replace native character IDs with QB or ESX identifiers.

### Ox Core

Select `Framework='ox_core'`, set the actual installed inventory, target and optional radial/keys. The adapter is included, but this is **not** a claim of full live test coverage; accept it only after the same SQL, payment, player identity and multi-client tests.

## Native-owned vehicles, keys and ownership

M4I Garage currently maintains its own `m4ig_*` tables. Framework-native `player_vehicles` (QB/Qbox) and `owned_vehicles` (ESX) are not magically the same table or auto-imported. Its `Config.NativeVehicleCompatibility` is a controlled, opt-in framework compatibility/projection facility, **not** a direct-native-table storage guarantee. Current recommended event-driven setting is `SyncIntervalMs=0` (not full-table 15s polling); validate the initial data and compatibility **before** enabling projection. Do not run `qb-garages`, `qbx_garages`, `esx_garage` and M4I Garage as competing owners for the same vehicles.

For a newly purchased car, the trusted server script must call `exports.m4i_garage:GetGarageCharacterId(playerSource)` after authentication; authorize the caller in `Config.TrustedVehicleRegistrars` and register the vehicle using the documented `RegisterOwnedVehicle` export with validated model, plate, category, props, garage and GTA class. Do not pass the player's OneSync source ID as a persistent owner ID.

## Cover, impound and damage

- Create the `vehicle_cover` item in the **actual** inventory and wire its usable item callback. Never auto-remove on initial Use; Garage manages the five-use charge/commit/refund path. ESX default inventory and Ox/QB slot metadata behave differently—see [recipes](integration-recipes.md).
- `Config.CoverActionCooldownSeconds=15` restricts repeated Cover / Uncover on the **same** vehicle (0 disables; maximum 3600). Server owns the timer; it persists over restarts.
- Police seize, impound retrieval, insurance and transfer payments must pass through Bridge's real **personal account** provider, not raw SQL assumptions.
- Deformation, body, engine, fuel, doors and glass need two-client verification after full/partial repair. Do not use test-only admin money in a customer deployment.

## Quick diagnostics

In console: `refresh` then `ensure m4i_bridge` (or `restart m4i_bridge` during controlled testing), followed by `ensure m4i_garage`. Check `m4i_bridge` framework and provider availability before blaming Garage. A missing Radial option can mean the selected vendor is offline, its required add/remove API differs, Garage is outside the PolyZone, or the nearest bay is too far. Use [Troubleshooting QA](../../shared/fivem-qa-checklist.md) and [Provider Selector](../../core/m4i_bridge/third-party-providers.md).

**Release note:** `[escrow]` filenames and an `escrow_ignore` manifest do not imply Cfx.re encryption. Check your real escrow build before sale.