# Garage Integrations — Required Changes in Other Resources

This is an **M4I Garage** integration reference: it tells you **exactly what to modify outside Garage when you enable a Garage feature**, while leaving other products' own unrelated functionality to their respective documentation.

**Source:** Garage `0.1.139-alpha`, Bridge `1.5.19-rc.1`, reviewed 7 November 2026. Third-party forks may use different APIs.

## Decide what to change

| Garage feature | Must edit another resource? | Where to change it |
| --- | --- | --- |
| Basic Open/Store | No beyond required Bridge profile | `m4i_garage/config.lua`, `m4i_bridge/config.lua`, `server.cfg` |
| Different Radial/Target/TextUI | If no matching Bridge adapter | `m4i_bridge/adapters/<domain>/<provider>/`; verify installed vendor contract |
| Sell owned vehicles from dealership | **Yes** | Your **dealership SERVER** + Garage `TrustedVehicleRegistrars` |
| Use vehicle covers | **Yes** | Actual Inventory item catalog + usable item callback (Ox needs client companion) |
| Full repair with external mechanic | Recommended | Actual mechanic SERVER+CLIENT + Garage `RepairTrustedResources` |
| External vehicle keys | If using external keys | Installed vendor's real Bridge Keys adapter |
| Insurance/GPS/Transfer payments | Provider must support personal banking | Bridge Banking adapter, not direct framework bank table writes |
| Optional Garage phone | Phone must support companion app | Bridge Phone provider + actual inventory `phone` item |
| Custom addon models | If not already classified | Bridge manual vehicles adapter or authoritative vehicle catalog |
| Existing QB/ESX player cars | **Migration plan required** | Trustworthy offline DB/source migration, not a one-way compatibility switch |
| Housing/custom phone that uses old Garage exports | If old calls exist | A verified **separate companion shim**, not fake Garage SQL rows |
| Custom pictures | Only when wanted | Optional M4I Upload global image ID and real Garage consumer support |

## 1. Choose providers, not a second framework

In `m4i_bridge/config.lua`, edit values **inside the existing table**:

```lua
-- Example for an actual Qbox server with the listed vendor resources:
Framework = 'qbox',
Inventory = 'ox_inventory',
UI = 'ox_lib',
Radial = 'qbx_radialmenu',
Target = 'ox_target',
Keys = 'qbx_vehiclekeys',
Banking = 'framework'
```

These lines are partial table **entries**, not a complete config file. A similar vendor resource name is not evidence its API matches a Bridge adapter. For unsupported third-party forks create a real adapter (proper client/server API and add/remove cleanup) using the [Bridge Provider Guide](../../core/m4i_bridge/complete-provider-setup.md). Garage should not reimplement the entire framework API itself.

If radial breaks, set Garage `Config.InteractionMode='keys'` for an E/H baseline test. NPC target interactions still need a real supported Target.

## 2. Dealership — register after verified server purchase

Edit `m4i_garage/config.lua` (trusted **resource names**, not player job names):

```lua
Config.TrustedVehicleRegistrars = {
    ['my_dealership'] = true
}
```

Then in the **real dealership SERVER**, after authenticating the player, completing payment and verifying the actual plate/model/class/category:

```lua
-- This is an integration snippet, NOT a whole dealership transaction.
local charId, err =
    exports['m4i_garage']:GetGarageCharacterId(buyerSource)
if not charId then
    print('Garage identity unavailable:', err)
    return
end

-- Example: Sultan, GTA class 6 (Sports); already verified plate.
local ok, vehicleIdOrReason =
    exports['m4i_garage']:RegisterOwnedVehicle(
        charId, 'ABC123', 'sultan', 'land',
        {}, 'public_legion', 'automobile', 6
    )
if not ok then
    print('Garage registration refused:', vehicleIdOrReason)
    -- Implement your own safe sale reversal / retry path.
    return
end
```

The Garage numeric ID from `GetGarageCharacterId` is **not** raw QBCore citizenid, ESX identifier or FiveM `source`. Only named trusted **server resources** may register purchases. The class/model, unique plate (1–8 chars), allowed Garage vehicle groups and spawn type must match. Never expose this as a freely invokable client registration event or direct SQL INSERT.

See [Server Export Contract](server-exports.md#6-trusted-dealership-registration--registerownedvehicle) for all arguments and return codes.

## 3. Existing cars and legacy Garage controllers

Garage does **not** import existing `player_vehicles` or `owned_vehicles` rows just because its SQL installer ran. `Config.NativeVehicleCompatibility.Enabled=true` projects **already Garage-owned vehicles into native read-compatible tables**; it is not an old-car importer or a complete implementation of the old `qbx_garages` API.

Before replacing another Garage, audit owner identity, vehicle model/plate/status, house and job garages, phone callbacks, impound/seized state, key scripts and vehicle spawner ownership. A separate validated migration/shim is required for any missing old API. Do **not** let two Garage scripts store/spawn the same car. Full safe migration guide: [Updating](updating.md).

## 4. Inventory: optional cover item

No `vehicle_cover` is required for ordinary Open/Store. When enabling Cover:

- `m4i_inventory`: current native item catalog may already define `vehicle_cover`; don't duplicate it.
- `qb-inventory`: add a unique usable `vehicle_cover` in actual `qb-core/shared/items.lua`; **no auto-consume**.
- `ox_inventory`: add the item to `ox_inventory/data/items.lua` with `consume=0`, `stack=false`, and a real client Use event companion (Bridge's Ox server inventory adapter does not create it automatically).
- ESX stock inventory: add `vehicle_cover` to the actual item SQL/vendor file and let the selected ESX usable callback run.

The intended accounting is **five successful uses per physical item**, but your real vendor must preserve the required item slot/receipt semantics. Do not use test-only `m4i_test_compat` in a customer package. **Copy-paste definitions and Ox companion:** [Vehicle Cover Item Guide](vehicle-cover-item.md).

## 5. External mechanic: trusted SERVER + real CLIENT repair

Garage needs verified **physical repair** and, for a signed full repair, authoritative permission.

Edit `m4i_garage/config.lua`:

```lua
Config.RepairTrustedResources = {
    ['my_mechanic'] = true
}
```

In the **mechanic SERVER** after valid invoice/service authorization:

```lua
local allowed, reason =
    exports['m4i_garage']:BeginFullRepair(customerSource, vehicleNetId)
if not allowed then
    print('Garage repair permission denied:', reason)
    return
end
```

After actually fixing the correct car on its controlling **CLIENT**:

```lua
exports['m4i_garage']:NotifyVehicleRepaired(vehicleHandle, 'full')
```

For partial repair use `'partial'`. A client notification alone does not erase Garage SQL damage. The other mechanic's **prices, invoice UI and staff permissions** remain in that mechanic's documentation. [Damage and Repair Guide](damage-persistence.md).

## 6. Radial, Target, TextUI, Notify, Progress and Keys

Garage requires these **behaviors**, rather than a particular unrelated store product:

| Provider | Garage needs |
| --- | --- |
| Radial | Register Open/Store only inside valid zone; correct vendor icon/handler; unregister cleanly on exit |
| Target | Register valid NPC/entity/zone action and remove it cleanly |
| TextUI | Show E/H prompt without leaving stuck overlays |
| Notify | Actual success/error feedback on client |
| Progress | Reliable completion/cancel callback and animation cleanup |
| Banking | Personal player account balance/remove/refund with real server result |
| Keys | Correct vendor API: QB plate-based versus Qbox entity-based resource contracts |
| Vehicle registry | Actual spawn model, verified GTA class, land/water/air category |

Use [Bridge adapters](../../core/m4i_bridge/complete-provider-setup.md) to implement missing vendor API methods; do not edit Garage SQL directly or invent an adapter ID because a vendor folder has a similar name. If Qbox radial doesn't show Garage, prove Garage works in `keys` mode first, then fix the radial adapter itself.

## 7. Phone companion (optional)

- Supported provider IDs include `lb_phone` and `qs_smartphone` when the real custom-app API matches. A stock QB Phone/NPWD does **not** automatically expose LB/QS custom-app registration.
- Garage's phone/valet paths also check that the player carries an inventory item **literally named `phone`**. Installing a phone resource alone is insufficient.
- QB Phone's limited Garage-list callback or one-way native SQL compatibility may help certain reads, but do not claim it replaces all QB Phone or Qbox NPWD garage exports.
- Keep **paid AI Valet** disabled on unverified external frameworks because its payment schema/ledger recovery needs work. [Known Limitations](../../shared/fivem-install-known-limitations.md).

## 8. Custom images (optional)

Garage can use shared image IDs from M4I Upload through Bridge. Assign an image ID in the Garage-supported artwork workflow, and verify fallback icon, cache and UI. A third-party QB inventory or phone does **not** automatically receive uploaded images: its own NUI may need a consumer adapter or local PNG asset.

[Separate M4I Upload manual](../m4i_upload/complete-installation.md) documents the image library itself.

## 9. Housing, police and old API consumers

For a housing/phone/custom police script calling your old garage:

1. List actual old callback/export names and **client/server** side.
2. Look for equivalent [Client Exports](client-exports.md) or [Server Exports](server-exports.md).
3. If missing, implement a **separate server-validated compatibility shim** using trusted Garage APIs.
4. Test stored/out/seized/impounded state, shared keys, login/reconnect and planned restart.
5. Do not give the shim unrestricted access to Garage-owned SQL or money.

## 10. Integration acceptance

- [ ] One framework, one Garage custody controller.
- [ ] Every installed vendor has a matching actual Bridge adapter; no fictional `ensure` entries.
- [ ] Dealer calls only from allowlisted server after successful payment; numeric Garage character ID used.
- [ ] Cover item exists in the actual inventory and behaves correctly for five successful uses.
- [ ] Full repair persists after Store/Retrieve; partial repair leaves other damage.
- [ ] Personal banking charges exactly once; no society-account confusion.
- [ ] Optional phone has real custom-app support and the exact `phone` item.
- [ ] Legacy cars and house/phone APIs are not silently lost.
- [ ] Client and server exports are never interchanged.

**Next:** [Installation](installation.md) · [Developer Client API](client-exports.md) · [Developer Server API](server-exports.md) · [Verification](verification.md).