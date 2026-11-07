# M4I Garage — Practical Integrations (small scripts to full systems)

> **CURRENT INSTALLATION — READ FIRST:** [Complete Garage installation — all required external edits](complete-installation.md). This page is a companion guide; the full guide includes SQL, items, third-party script edits, provider compatibility and go-live steps. Also review [Source-audited limitations](../../shared/fivem-install-known-limitations.md).


> **Ready-to-copy item definitions:** [Vehicle Cover for QBCore, Ox/QBX, ESX and M4I](vehicle-cover-item.md). The generic inventory table below does not by itself create the item or wire the Ox client Use event.


**Version:** Garage `0.1.139-alpha`, Bridge `1.5.19-rc.1`. Every integration chooses the customer's **installed, adapter-supported** resources. Neither M4I Garage nor Bridge should rewrite a vendor framework or database table just to make an unsupported export appear to exist.

## 1. A small script: show Garage UI from another resource

```lua
-- CLIENT-side only; validates zone and location on the normal Garage path.
local ok, reason = exports.m4i_garage:OpenGarage()
if not ok then print(('OpenGarage refused: %s'):format(tostring(reason))) end
```

The client also provides `GetGarages()`, `GetGarage(id)`, `GetCurrentGarage()`, `IsPlayerInGarage(id)`, `IsGarageUIOpen()`, `GetVehicleCondition(vehicleEntity)`. Calling `OpenGarage` **does not bypass server** authorization, ownership, access, 3D zone or spawn safety.

## 2. An admin/dealership: register a purchased vehicle

```lua
-- SERVER-side in a trusted dealership resource, after the framework
-- player is loaded. Source/plate/model/category/props/class MUST be validated.
local characterId, err = exports.m4i_garage:GetGarageCharacterId(playerSource)
if not characterId then
    print('No mapped Garage identity: '..tostring(err))
    return
end

-- The target API must match the current Registry export:
-- RegisterOwnedVehicle(characterId, plate, model, category,
--                      properties, garageId, spawnType, verifiedVehicleClass)
-- Call ONLY after checking the customer truly purchased/owns the car.
```

Set `Config.TrustedVehicleRegistrars = { my_dealership = true }` **only for a trusted server resource**. Avoid duplicates by stable plate and a real transaction ID; use server-side permission, owner and vehicle class checks. This does not import all QB/Qbox/ESX vehicles by itself.

## 3. Mechanic: preserve full and partial repair results

The Garage is the condition/custody authority. A mechanic script should call the authorized Garage repair route or permitted Bridge integration; do not just set health in an untrusted client event and assume SQL snapshots updated. Add only trusted exact resource names under `Config.RepairTrustedResources`. Test engine/body/fuel, deformation, glass, petrol-tank damage, and vehicle condition after **Store → Take → server restart**. Read the vehicle state using the public API:

```lua
-- CLIENT: live physical condition of a hydrated Garage-signed entity
local live, why = exports.m4i_garage:GetVehicleCondition(vehicleHandle)

-- SERVER: persisted Garage snapshot, which can lag the live entity
local stored, why = exports.m4i_garage:GetVehicleCondition(garageVehicleId)
```

The client receives a GTA entity handle; the server receives a persistent numeric Garage vehicle ID. A network ID or plate is **not** interchangeable with either.

## 4. Different inventories and the five-use vehicle cover

| Customer inventory | Bridge adapter | Integration detail |
| --- | --- | --- |
| `m4i_inventory` | `m4i_inventory` | Native transactional item path |
| `qb-inventory` | `qb_inventory` | Real slot via `GetItemBySlot`; metadata is usually `info` |
| `ox_inventory` | `ox_inventory` | Real slot via `GetSlot`; metadata has `metadata` |
| `esx_inventory` | `esx_inventory` | ESX usable item callback; no native numbered slot (Bridge uses sentinel) |

Define `vehicle_cover` in the selected inventory according to that vendor's **actual schema**, and ensure it is recognized as usable. **Do not consume an item immediately on Use**; Garage reserves and commits a life only after it has validated ownership/proximity/collision/cooldown. Test fresh item, remaining lives, final-use depletion, rapid repeat use, disconnect/restart and rollback of failed placement. Some stacked metadata combinations are not atomic: test individual item slots.

## 5. Phone app: optional, not automatic

| Phone | What to do |
| --- | --- |
| `lb-phone` | Bridge `Phone='lb_phone'`; client adapter uses `AddCustomApp` / `RemoveCustomApp` |
| `qs-smartphone` | Bridge `Phone='qs_smartphone'`; client adapter uses `addCustomApp` / `removeCustomApp` |
| Either installed | `Phone='auto'` only chooses a supported healthy adapter |
| QB Phone | No built-in custom-app export; test native Garage callback compatibility, do not fake custom UI |
| NPWD | Needs a separate companion/registration resource; not auto-installed |
| No phone | Leave `Phone='disabled'`; Garage works without a custom app |

Third-party phone versions can differ. Validate permissions and session cleanup in the actual phone UI.

## 6. Radial, target, TextUI and progress

- **Radial installed:** Bridge `Radial='qb_radialmenu'`, `'qbx_radialmenu'`, `'m4i_radialmenu'`, or `'qs_radialmenu'` **only if that exact adapter's API matches**. Garage `InteractionMode='radial'` registers items only when allowed in a valid zone.
- **No radial:** Garage `InteractionMode='keys'`, E = Open and H = Store. This does not remove target needs from police/impound NPC interactions.
- **Target:** `ox_target`, `qb_target` or `m4i_target`. `custom` must implement matching add/remove entity and zone exports.
- **TextUI:** Select Bridge `UI='qb_textui'` for QB DrawText/HideText, `'ox_lib'` for working ox_lib text UI, or `'esx_textui'` for compatible ESX. `qb-menu` is not a drop-in TextUI.
- **Progress:** Select a started Bridge adapter. Do not assume NUI names/events are identical across versions.

For arbitrary custom vendors, create an adapter under `m4i_bridge/adapters/<domain>/<your_id>/` and select that ID. See [Bridge Provider Guide](../../core/m4i_bridge/third-party-providers.md).

## 7. Police, impound, keys, finance, vehicle images

- Police job access/seize/retrieve stays server-authoritative; integrate job grades from Bridge and validate each target and F1 action.
- Insurance/impound payments must run through the Bridge's selected **personal bank/cash** route and tested refund semantics. Society bank account APIs are not player balances.
- Custom key scripts require a Bridge Keys adapter and verified permission/plate grants; never trust a client-generated plate.
- Shared vehicle thumbnails use the global `m4i_upload` library via Bridge. A key/ID resolves across scripts; local fallback images can remain if no matching key is present.
- For addon vehicles, verify GTAV vehicle class/category, spawn clearance and garage allowed type in the Creator. Use a verified classification provider (M4I Registry if configured).

## 8. Public server API quick reference

`GetGarage(id)`, `CanPlayerAccessGarage(source,id)`, `HasVehicleAccess(source,vehicleId,includeTemporary)`, `GetVehicleByPlate(plate)`, `GetVehicleCondition(vehicleId)`, `IsVehicleStored(vehicleId)`, `GetVehicleEntity(vehicleId)`, `GetGarageCharacterId(source)`, plus the guarded registration and operational exports from `server/registry.lua` and related modules. **Read** the API signatures in the delivered files before calling them; several exports reject non-resource invocations and invalid IDs.

## 9. QA before release

Test one player, two players, a job-restricted user, reconnect, character switch, payment and refunds, real item metadata, radial/target add+remove, Garage outside/inside zone, spawn with blocked bay, cover cooldown, full/partial repair, missing phone, missing optional provider, and resource restart. Check Cfx server console **and** player F8 console. See [shared checklist](../../shared/fivem-qa-checklist.md).

These integrations are shipped adapters, not a universal guarantee for every commercial fork.