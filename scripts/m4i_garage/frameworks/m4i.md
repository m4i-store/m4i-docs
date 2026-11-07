# Install M4I Garage on M4I Core

**Framework ID:** `m4i` · **Core resource:** `m4i_core` · **Garage version:** `0.1.139-alpha`.

## Requirements and recommended load order

This is the native M4I profile. Start `oxmysql`, `m4i_registry` and `m4i_core` first. M4I-specific Inventory, Target, Radial and HUD have their own dependency manifests; the **current native test base** loads `m4i_bridge` before those M4I UI resources, then starts `m4i_garage` after their initialization.

```cfg
# Example segment. Keep the rest of your existing M4I server.cfg.
ensure oxmysql
ensure m4i_registry
ensure m4i_core
ensure m4i_bridge
ensure m4i_inventory
ensure m4i_target
ensure m4i_radialmenu
ensure m4i_hud
ensure m4i_garage

add_ace group.admin m4i.garage.admin allow
```

Only `ensure` resources actually installed. Do not duplicate entries already loaded through a bracketed folder. The native test instance also includes other core game systems not listed here; retain their declared ordering.

## Files you change

**`m4i_bridge/config.lua`:** `Framework='m4i'`. Provider defaults can be kept at `'framework'` when the native inventory, target and radial are installed. Check `m4i_bridge_profile` and older framework convars in server.cfg for overrides.

**`m4i_garage/config.lua`:** start with `InteractionMode='radial'` when `m4i_radialmenu` is functional, otherwise use `'keys'` (E Open/H Store). Review `CreatorAce`, `AuthorizedSeizureJobs`, `TrustedVehicleRegistrars`, `RepairTrustedResources` and optional Cover item. Keep optional AI `DeliveryEnabled=false` unless its payment schema/ledger is verified.

**SQL:** import `m4i_garage/sql/install.sql` into the same M4I database used by `oxmysql`; do not delete an existing M4I character/vehicle table. Extra runtime-created Garage tables require reviewed migration privileges.

**Vehicle registration:** new player-owned cars must enter Garage's custody through a trusted server `RegisterOwnedVehicle` call. Merely giving a car in a menu or native framework registry does not guarantee `m4ig_vehicles` ownership.

## First-use checks

1. In server console run `m4ig_doctor`; verify Bridge, framework, inventory, radial/target and Garage readiness.
2. Connect with authorized admin and run `/garagecreator`; make a Land/Public zone and a clear spawn bay.
3. Register or safely admin-adopt a test car; Store/Retrieve and log out/reconnect.
4. If enabled, test Cover's 5-use item, 15s cooldown, true full repair and shared keys separately.

**Screenshots:** [Garage Creator](../visual-setup-guide.md) · **Exact install steps:** [Installation](../installation.md) · **Exports:** [Server API](../server-exports.md).