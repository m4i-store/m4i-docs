# m4i_garage — Changelog

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
