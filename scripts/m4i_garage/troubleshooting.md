# m4i_garage — Troubleshooting

This page covers the public Client/Server API delivered in TEST VPS source `v0.1.121-alpha`.

| Symptom | Likely cause | Safe check |
| --- | --- | --- |
| Export `No such export` | Wrong resource version or `m4i_garage` not started | Check `ensure m4i_garage`, `fxmanifest.lua` and script load order |
| `GetCurrentGarage()` returns `nil` | Client has not received synced garages or is outside a normal configured polygon | Confirm a valid Garage Creator zone, not Impound/Seized/Cover-only |
| `OpenGarage() -> false, NOT_AT_GARAGE` | Caller is physically outside the configured 3D Garage zone | Walk into the correct zone; do not bypass server location checks |
| `OpenGarage() -> true, REQUESTED` but no UI | Initial client request succeeded, later server validation rejected it | Inspect client F8 and server logs for `vehicles` action result |
| `OpenGarage('wrong-id')` | Invalid explicitly named garage | API now refuses unknown IDs instead of falling back to another nearby garage |
| `GetVehicleCondition(handle) -> NOT_HYDRATED` | The vehicle's OneSync restoration has not finished | Wait for signed `m4iGarageHydrated=true`; do not treat blank natives as full repair |
| `GetVehicleEntity(id) -> NOT_IN_WORLD` | Car is stored, outside world, or no longer a signed live network entity | Read `GetVehicleCondition(id).physicalStatus` server-side |
| `GetVehicleByPlate() -> INVALID_PLATE` | Invalid characters/length; plate may be unregistered | Normalize player input and supply 1–8 valid characters |
| `HasVehicleAccess() -> NO_ACCESS` | Player is not the canonical owner or shared/temporary key holder | Use Bridge-backed identity and Garage's canonical key access |
| `RegisterOwnedVehicle() -> UNTRUSTED_RESOURCE` | Resource not on registrar allowlist | Verify actual invoking resource, review rights, then configure allowlist |
| Full repair appears to restore old dents later | Unverified repair, stale client mesh or missing trusted permit | Follow `BeginFullRepair` trusted flow; do not clear SQL damage manually |
| Extra detached doors on observer | Local GTA synthetic deformation replay or custom model debris | Check the updated observer guard and test two real clients; door guard does not necessarily protect custom bumper/fender fragments |

## Important distinction: IDs

`vehicleId` is the persistent numeric Garage database ID. `vehicleHandle` is a local Client GTA entity handle. `netId` is a network ID. Passing one in place of another can query the wrong vehicle or fail to find it.

## Safe debug sequence

1. Check that `m4i_bridge`, `oxmysql` and `m4i_garage` are started, in order.
2. Use the existing read-only exports to inspect current Garage ID, vehicle status and vehicle condition.
3. Review F8/client and FXServer logs without dumping framework secrets, entire `props` JSON or raw player identity into public logs.
4. Run `tests/public_exports_contract_v0221.lua` and `tests/manifest_exports_escrow_v0221.lua` on a staging copy.
5. For visual fidelity, check the **same car** with two actual GTA clients. StateBag simulations do not validate 3D rendering or loose debris.

No troubleshooting procedure here authorizes changing another player's vehicle ownership, money or police custody through SQL.
