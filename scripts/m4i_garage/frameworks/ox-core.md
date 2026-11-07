# Install M4I Garage on Ox Core

**Bridge ID:** `ox_core` · **Framework resource:** `ox_core`. **Important release status:** an Ox Core framework adapter is present in the shipped M4I Bridge code; however, the four active test bases checked on 7 November 2026 are **M4I, QBCore, ESX and Qbox**. Ox Core did **not** receive a full independent live-player acceptance pass. Treat this installation as **integration testing**, not certified plug-and-play production support.

## 1. Requirements

Use a genuinely working Ox Core server: it must have its own configured identity, item storage, bank accounts, player permissions and vehicle model source, plus `oxmysql`.

Copy only the inner `m4i_bridge` and `m4i_garage` folders into your resources category. Keep `ox_lib` / `ox_inventory` / `ox_target` if they actually exist and your installed Ox Core release supports their declared dependencies.

```cfg
# EXAMPLE. Adjust to your installed Ox Core release and manifests.
ensure oxmysql
ensure ox_lib
ensure ox_core
# ensure ox_inventory
# ensure ox_target
ensure m4i_bridge
ensure m4i_garage

add_ace group.admin m4i.garage.admin allow
```

Do not start `qbx_core`, `qb-core`, `es_extended` or other second framework to make Garage start.

## 2. Framework settings

Edit values **inside `M4IBridgeConfig`** in `m4i_bridge/config.lua`:

```lua
Framework = 'ox_core',
Inventory = 'ox_inventory', -- if actually installed and matched
UI = 'ox_lib',             -- if installed
Target = 'ox_target',      -- if installed
Radial = 'framework',      -- only a registered, verified radial adapter
Keys = 'framework',        -- must test actual vendor API
Banking = 'framework'
```

For the first minimum test use **`Config.InteractionMode='keys'`** in `m4i_garage/config.lua`; it does not need an unverified radial. NPC functions can still need Target. Keep `Config.DeliveryEnabled=false` until external framework banking/ledger and valet schema/restart refunds are verified.

**Do not copy unqualified vendor names into the Bridge config.** If a resource's API differs, register a real adapter in Bridge and test its identity, money, inventory, TextUI, keys and callbacks; that adapter is outside Garage's own Lua core.

## 3. SQL and character mapping

Back up the Ox Core database, import `m4i_garage/sql/install.sql` without deleting existing players/vehicle records, and verify Garage can create its extra runtime support tables or has pre-applied migrations.

Garage uses `m4ig_identity_map` to create provider-qualified **numeric** character identifiers for non-M4I frameworks. For a dealership test: use server-side `GetGarageCharacterId(playerSource)` **after an Ox character has fully loaded**, not a source ID or arbitrary native identifier; then register using the trusted server export.

Native framework vehicle table projection does not migrate legacy Ox vehicle data or reproduce arbitrary vendor housing garage exports. Leave `NativeVehicleCompatibility.Enabled=false` until measured, reviewed, documented support exists.

## 4. Acceptance gates specific to Ox Core

- [ ] Correct server script loads and selects exactly `ox_core`, with a usable numeric Garage ID after login/relogin.
- [ ] Framework jobs and grades are read correctly for police and garage access.
- [ ] Inventory `HasItem`/Use/Count/Refund handles Cover item safely and respects five-use count.
- [ ] Banking can charge and refund a **personal account** once, not a group account.
- [ ] Zone Open/Store works in keys mode and at least one GUI/NPC target workflow works.
- [ ] New dealership-registered vehicle Store/Retrieve persists fuel, engine/body/deformation.
- [ ] Keys and shared vehicle access survive reconnection.
- [ ] Two players and FXServer restart produce no ghost cars or duplicate rows.
- [ ] Any unavailable provider/phone callback is documented as unsupported with this Ox Core build.

Until these pass, do not claim full Ox Core compatibility.

**Next:** [Start-to-finish installation](../installation.md) · [Garage-specific integrations](../integrations.md) · [Server exports](../server-exports.md) · [Known limitations](../../../shared/fivem-install-known-limitations.md).