# Install M4I Garage on ESX Legacy

**Bridge framework ID:** `esx` · **Framework resource:** `es_extended` · **Typical original ownership table:** `owned_vehicles`.

ESX servers vary greatly. The current Garage **does not require** QBCore-specific inventories, menus, keys or phone resources. Choose the providers actually installed in **your ESX server**.

## 1. Install exact folders and resources

Back up the existing database and ESX vehicle/garage scripts. Copy the resource folders `m4i_bridge` and `m4i_garage` to `resources/[m4i]/`, then review the real ESX server startup order:

```cfg
ensure oxmysql
ensure es_extended
# Start your EXISTING ESX inventory or ox_inventory here.
# Start the actual configured ox_lib/target/radial vendor if used.
ensure m4i_bridge
ensure m4i_garage
add_ace group.admin m4i.garage.admin allow
```

The comments are placeholders, **not resource names**. Do not add a missing `esx_inventory` resource just because the Bridge profile lists that adapter. ESX releases may integrate inventory directly in `es_extended`, use `ox_inventory`, or use another system requiring a custom adapter.

## 2. Change your configuration

Edit `m4i_bridge/config.lua` in the existing `M4IBridgeConfig` table, keeping the rest:

```lua
Framework = 'esx',
Inventory = 'ox_inventory', -- ONLY if you actually use ox_inventory
UI = 'ox_lib',            -- ONLY if ox_lib is started
Target = 'ox_target',      -- ONLY if installed
Radial = 'framework',     -- no universal ESX radial API
Banking = 'framework'
```

If the server uses supported `esx_inventory` and ESX TextUI, explicitly select the registered `esx_inventory` and `esx_textui` provider IDs instead. The correct choice depends on **your installed implementation**.

For a simple universal first test use:

```lua
-- m4i_garage/config.lua
Config.InteractionMode = 'keys'
Config.InteractionOpenKey = 'E'
Config.InteractionStoreKey = 'H'
Config.DeliveryEnabled = false
```

A Target remains helpful/required for applicable NPC menus. Verify its client-side add/remove methods; Ox Target and QB Target do not share the same API.

## 3. Database and vehicle IDs

Import **only** `m4i_garage/sql/install.sql` after a full backup of the ESX database. It creates Garage-owned `m4ig_*` tables. **Do not drop or replace `owned_vehicles`**, and do not use a generic “ESX SQL” file from another Garage product.

The Garage maps ESX string identifiers to **stable numeric Garage IDs** via `m4ig_identity_map`. For an external dealership resource, get that number from trusted server code using `GetGarageCharacterId(playerSource)` and send it to `RegisterOwnedVehicle`; never pass raw identifier strings to a numeric API.

Setting `Config.NativeVehicleCompatibility.Enabled=true` does **not** import pre-existing ESX `owned_vehicles` into `m4ig_vehicles`. An approved migration/compatibility plan is required. Don't leave `esx_garage` and Garage both controlling the same owned car.

## 4. Required changes for optional features

- **Cover Item:** define `vehicle_cover` in the actual ESX item DB/table or inventory catalog, and register a usable item using the installed ESX/Inventory API. Ensure it is not auto-consumed on click: the Garage enforces its five-use receipt. [Cover instructions](../vehicle-cover-item.md).
- **Bank payments:** confirm personal ESX bank-account debit and refund through the selected provider. For Impound, transfer, insurance, GPS and valet do not query a society/job account as a player account.
- **Police role:** `Config.AuthorizedSeizureJobs` must use exact ESX `xPlayer.job.name` names and minimum grades; permissions remain server-checked.
- **Vehicle keys:** select a real supported keys adapter or implement one for the installed vendor, with actual plate/model rules.
- **Phones:** stock ESX phone scripts do not universally support Garage custom-app registration; only enable an actual supported app integration or write an appropriate companion app. Phone/valet features check the exact item `phone`.

## 5. Test and diagnose

Run `m4ig_doctor` in FXServer console and validate that ESX, inventory, TextUI, target and Garage are started. With an authorized admin, create a public Land garage and a spawn bay using `/garagecreator`. Register a test vehicle with trusted source, Store/Retrieve, reconnect, test money with bank and cash. Verify an existing ESX-owned vehicle is not assumed migrated automatically.

**Next:** [Main install](../installation.md) · [Integrating an ESX dealership](../integrations.md) · [Known limitations](../../../shared/fivem-install-known-limitations.md) · [Troubleshooting](../troubleshooting.md).