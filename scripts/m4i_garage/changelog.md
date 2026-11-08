# m4i_garage — Changelog


## 0.1.140-alpha — 2026-11-08 (staged source, default OFF)

- Added **`Config.NativeVehicleCompatibility.DeleteOnNativeRowMissing = false`** customer setting for QBCore, Qbox and ESX native vehicle table deletion.
- When both `Enabled=true` and `DeleteOnNativeRowMissing=true`, verifies **previously linked** native rows missing for at least 180 seconds, checks once a minute (independent of native projection interval), and archives/removes eligible **normally stored** Garage cars. Max five deletions per minute.
- Protected vehicles (`out`, `covered`, `impounded`, `seized`, `delivering`, legal hold, world entities, valet charges) cannot be automatically removed.
- Added `m4ig_native_delete_archive` recovery snapshots, `native_delete_sync` audit, and transactional cleanup of access/temporary keys and existing auxiliary rows.
- Updated installer, framework, configuration, SQL ownership and troubleshooting docs. **No public arbitrary vehicle Delete export** and **no production multiplayer deletion QA**; opt in only after staging.
- Verified isolated MariaDB SQL transactions and Lua 3-minute grace/cancellation cases; default remains off on all distributed profiles.


> **HISTORICAL CHANGELOG:** For the currently documented `0.1.140-alpha` source and supported customer workflows, start at [Garage Overview](introduction.md), [Installation](installation.md) and [Client/Server APIs](exports.md). Individual older milestone entries do not certify current live compatibility.


## 0.1.123-alpha — 2026-11-03 (staged TEST VPS source)

- Added external Framework **bank money adapters** in Bridge for Qbox, QBCore, ESX and Ox Core, with invalid/insufficient-funds/refund source-contract tests.
- Added explicit `setr m4i_bridge_profile ...` installer profiles (default native M4I unchanged); profile provider priorities cannot fall back to another Framework.
- Added native TextUI, notification and progress Bridge providers for bases without `m4i_hud`.
- Added Garage console-only `m4ig_doctor` to inspect provider readiness without touching player data.
- Installation docs updated; full real-provider and existing-vehicle migration QA remain mandatory.

## 0.1.122-alpha — 2026-11-03 (staged TEST VPS source)

- Bridge-driven target and radial provider selection, no hard dependencies on `m4i_target` or `m4i_radialmenu` in Garage manifest.
- Framework-qualified persistent Garage identity mapping table for Qbox, QBCore, ESX, Ox Core; native M4I identity unchanged.
- Added read-only server `GetGarageCharacterId` export for trusted server-side integration.
- Added Bridge ox_target/qb-target local NPC entity adapters and QB/QBX radial adapters (source-level tested; real runtime acceptance pending).
- Existing five-use Cover still requires an inventory adapter with atomic receipt semantics; support for third-party inventory not certified.
- Separate [Five Frameworks and Bridge Providers](framework-compatibility.md) documentation and installation guide.

## 0.1.121-alpha — 2026-11-03 (staged TEST VPS source)

- Introduced editable `client/exports.lua` and `server/exports.lua` public API facades.
- Added seven new read-only or UI-request Client exports: `GetGarages`, `GetGarage`, `GetCurrentGarage`, `IsPlayerInGarage`, `IsGarageUIOpen`, `OpenGarage` and `GetVehicleCondition`.
- Added seven new Server exports: `GetGarage`, `CanPlayerAccessGarage`, `HasVehicleAccess`, `GetVehicleByPlate`, `GetVehicleCondition`, `IsVehicleStored` and `GetVehicleEntity`.
- Preserved existing `RegisterOwnedVehicle`, `GetVehicleStatus`, `GetGarages` (server), `PlayerHasVehicleKey`, `AuthorizeFullRepair`, `BeginFullRepair` and client `NotifyVehicleRepaired` for compatibility.
- Added parameter validation, deep-copied public Garage snapshots, SQL column whitelisting, resource-only server gate, and local polygon verification for UI.
- Fixed invalid named Garage IDs silently falling back to the currently active zone.
- Reformatted all `fxmanifest.lua` lists so each item is on its own line; preserved source and asset load order.
- Added selective Asset Escrow ignore entries for configuration, JSON data, documentation, SQL installation files and editable API integrations, without exposing core custody/repair code.
- Added production-source contract and manifest tests. Existing resource regression suite passed on the TEST VPS.
- Documentation published in `m4i-store/m4i-docs`.

**Runtime validation:** still requires testing inside an actual running FiveM client after the source is restarted/loaded. Automated tests are not a guarantee of 200-client GPU, bandwidth or cosmetic parity.

## 0.1.120-alpha — observer debris and damage synchronization

- Added a guarded deformation replay to prevent observer-only detached doors during synthetic native impacts.
- Added repeated StateBag update deduplication and cleanup on timeout or resource stop.
- Source-level simulated 200-observer stress tests passed; real 200-player production performance is **not** claimed.

For older Garage development notes, see the resource-local `docs/` directory on the TEST VPS. Historical GitHub snapshots can have different APIs and versions.
