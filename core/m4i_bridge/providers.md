# M4I Bridge — Choose Third-Party Providers & Custom Integrations

**Bridge:** \`1.5.19-rc.1\` · **Audience:** owners of existing QBCore, QBX/Qbox, ESX, M4I, and Ox Core bases.

**Rule:** keep the installed framework and its data. Bridge translates M4I calls into the **configured adapter**. Do not randomly rename a third-party resource or paste its direct exports into Garage. Different versions/forks may expose different APIs; an adapter must match the real export signatures and return values.

## Provider selector: choose what you already use

| Function | Shipped adapter IDs (not necessarily resource names) | Notes |
| --- | --- | --- |
| Framework | \`m4i\`, \`qbcore\`, \`qbox\`, \`esx\`, \`ox_core\` | Select exactly one; no silent change of core |
| Inventory | \`m4i_inventory\`, \`ox_inventory\`, \`qb_inventory\`, \`esx_inventory\` | \`esx_inventory\` requires its matching installed resource, not just ESX Core |
| UI/TextUI | \`m4i_hud\`, \`ox_lib\`, \`qb_textui\`, \`esx_textui\`, \`qb_menu\`, \`native\`, \`custom\` | Check context/input versus TextUI support; these are not interchangeable |
| Notify | \`framework\`, \`m4i_hud\`, \`ox_lib\`, \`native\`, \`custom\` | Framework mapping is QB/ESX/Qbox aware |
| Progress | \`ox_lib\`, \`progressbar\`, \`esx_progressbar\`, \`native\`, \`custom\` | Select an installed provider |
| Radial | \`m4i_radialmenu\`, \`qb_radialmenu\`, \`qbx_radialmenu\`, \`qs_radialmenu\`, \`custom\` | No bundled \`ox_lib\` radial adapter; source-tested, fork-specific runtime QA required |
| Target | \`m4i_target\`, \`ox_target\`, \`qb_target\`, \`custom\` | Verify local-entity/zone registration and remove calls |
| Phone custom app | \`lb_phone\`, \`qs_smartphone\`; \`auto\` or \`disabled\` | \`qb-phone\` is **not** an embeddable custom app provider |
| Keys | \`qb_vehiclekeys\`, \`qbx_vehiclekeys\`, framework/custom with adapter | Vehicle keys need real server-side grant/verify |
| Banking | Framework account; shipped \`qb_banking\` / \`renewed_banking\` adapters | Use **personal** balance via framework, not society bank SQL |
| Dispatch | \`none\`, \`ps_dispatch\`, \`cd_dispatch\`, \`qs_dispatch\` | Only compatible versions of those resources |
| Database | \`oxmysql\` | Never redirect arbitrary SQL to the player's framework table |
| Vehicles | \`auto\`, \`manual\`/registered vehicle adapter | Classification needs a valid source; consider \`m4i_registry\` |

**Adapter ID ≠ actual resource folder name:** \`qb_target\` -> \`qb-target\`; \`qb_radialmenu\` -> \`qb-radialmenu\`; \`qbox\` -> \`qbx_core\`; \`lb_phone\` -> \`lb-phone\`; \`qs_smartphone\` -> \`qs-smartphone\`. The implementation in \`adapters/<domain>/<id>/\` is the authority.

## Pick an alternative without touching the framework

In \`m4i_bridge/config.lua\`, retain your \`Framework\` and choose, for example:

\`\`\`lua
Inventory = 'ox_inventory',
UI = 'ox_lib',
Notify = 'framework',
Progress = 'ox_lib',
Radial = 'qb_radialmenu',
Target = 'ox_target',
Phone = 'lb_phone',
\`\`\`

This **illustrates values inside** \`M4IBridgeConfig\`, not a complete file. Only select a provider if its adapter matches your installed resource. For an unsupported radial, use Garage keys mode until you write a matching adapter; no runtime guessing.

## Integrating a small script (notifications, UI, one NPC)

Prefer Bridge's public exports in your own resource. Example server-side notification:

\`\`\`lua
-- server.lua in YOUR resource (declare dependency 'm4i_bridge')
local ok,err = exports.m4i_bridge:NotifyPlayer(sourceId,{
    title='Vehicle', description='Action completed', type='success'
})
if ok==false then print('Bridge Notify failed: '..tostring(err)) end
\`\`\`

Calls that display UI/NUI must use the **client** Bridge API. Do not call client-only exports from a server file. For a simple command, start with a Bridge framework, notify, or progress adapter; no direct QB/ESX imports into the M4I script.

## Integrating a large script (inventory, phone, dealership, mechanic, police)

- **Inventory/item:** match your inventory's metadata/slot semantics; for \`vehicle_cover\`, **do not consume the item when Use first fires**. Garage commits its five-use receipt only after a validated action.
- **Dealership:** register a new Garage-owned vehicle from a **trusted server resource**; use \`GetGarageCharacterId\`, allowlist \`Config.TrustedVehicleRegistrars\`, validate plate/model/class and garage. Do not assume native ownership SQL rows have been imported.
- **Mechanic:** integrate repair through the Garage server authority; allowlist only exact trusted repair resources in \`Config.RepairTrustedResources\`. External full/partial repairs need test coverage for deformation, windows and tank damage.
- **Phone:** LB Phone and QS Smartphone custom-app providers are available. For QB Phone use a verified compatibility callback/backend, not a non-existent \`AddCustomApp\` export. NPWD requires its own companion adapter.
- **Keys:** Bridge/server validates plate, caller and vehicle access; do not issue keys solely on an untrusted client event.
- **Bank/insurance:** check/refund using framework personal bank accounts through Bridge; avoid writing \`players\`, \`owned_vehicles\` or \`player_vehicles\` balances directly.
- **Jobs/Police:** Bridge normalizes job data, while Garage enforces seizure and custody permissions server-side.

## A genuinely new vendor: custom adapter recipe

1. Verify the vendor resource actually has the documented client/server exports and that it starts correctly.
2. Copy a matching template under \`m4i_bridge/adapters/_templates/<domain>/\` to \`adapters/<domain>/my_vendor/client.lua\` or \`server.lua\`.
3. Set \`meta={domain='<domain>',provider='my_vendor',side='client' or 'server',implemented=true,dependencies={'real-resource-name'}}\` **only after implementing** all required methods. Use \`Bridge.registerAdapter(domain,'my_vendor',side,adapter)\`.
4. Configure \`Radial='my_vendor'\`, \`Target='my_vendor'\`, etc. in the customer \`config.lua\`, not in internal framework code. The wildcard \`adapters/**/client.lua\` and \`adapters/**/server.lua\` scripts must load your implementation.
5. Verify **both** add and remove paths, callback payloads, error reporting, resource restart, reconnect, invalid permissions and multi-player concurrency.

The shipped \`adapters/radial/custom/client.lua\` allows configuring a vendor \`resource\`, \`addExport\` and \`removeExport\` **inside that adapter**; \`adapters/target/custom/client.lua\` similarly configures add/remove entity, zone and model exports. These simple adapters are **not** generic converters for all fork APIs. If the vendor returns a different payload, implement a dedicated adapter instead. Do not return \`true\` for failed registration.

**Read next:** [Installation](setup-selector.md) · [Garage recipes](../../scripts/m4i_garage/integration-recipes.md) · [Troubleshooting](../../shared/fivem-qa-checklist.md).