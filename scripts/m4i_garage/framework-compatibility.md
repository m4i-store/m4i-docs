# m4i_garage — Five Frameworks and Bridge Providers

**Source version:** `m4i_garage v0.1.122-alpha` on the M4I TEST VPS, 3 November 2026. The bridge provider adapters were source-level tested, **not** validated in live Qbox/QBCore/ESX/Ox Core player sessions. This is an integration configuration guide, not an unconditional compatibility certification.

## Design contract

```text
m4i_garage  ──framework, identity, jobs, money, items──> m4i_bridge
            ──Radial registration and removals────────> m4i_bridge
            ──Target entity registration and removals─> m4i_bridge
            ──Database (garage-owned tables)──────────> oxmysql
m4i_bridge  ──selected, explicit provider adapter─────> one framework / target / radial / inventory
```

The Garage manifest depends on **`m4i_bridge` and `oxmysql` only**. The selected Radial/Target script is installed and started separately; no forced `m4i_radialmenu` or `m4i_target` dependency. Bridge makes the actual provider choice, rather than Garage guessing a script from what happens to be running.

The Bridge **does not auto-select external frameworks** by default. Edit the installed `m4i_bridge/config/providers.lua` `providers.selected` table before starting the Bridge and Garage. The M4I default is intentionally unchanged.

## Recommended provider combinations

| Framework provider key | Framework resource | Bridge target key | Bridge radial key | Inventory example | Qualification |
| --- | --- | --- | --- | --- | --- |
| `m4i` | `m4i_core` | `m4i_target` | `m4i_radialmenu` | `m4i_inventory` | Native default; source tests passed |
| `qbox` | `qbx_core` | `ox_target` | `qbx_radialmenu` or `qb_radialmenu` | `ox_inventory` | Provider adapters present; real-game acceptance pending |
| `qbcore` | `qb-core` | `qb_target` | `qb_radialmenu` | `qb_inventory` or `ox_inventory` | Provider adapters present; real-game acceptance pending |
| `esx` | `es_extended` | `ox_target` | `m4i_radialmenu` or an installed compatible QB radial | `ox_inventory` | No generic ESX radial adapter shipped |
| `ox_core` | `ox_core` | `ox_target` | `m4i_radialmenu` or an installed compatible QB radial | `ox_inventory` | No ox_lib radial adapter shipped |

**Important:** `qbx_radialmenu` and `qb_radialmenu` adapters use the corresponding provider's `AddOption` / `RemoveOption` contract and translate Garage's nested children. Verify the installed provider version exposes these exports. Do not assume any resource with “radial” in its name is automatically supported. `ox_lib` radial is **not** an integrated Bridge radial provider in this version.

For target, the Bridge has working source-level adapters for `m4i_target`, `ox_target` (local entities via `addLocalEntity`/`removeLocalEntity`), and `qb_target` (resource `qb-target`, option label cleanup). A generic `custom` target needs a dedicated Bridge entity adapter before the Garage NPC target can be claimed operational.

## Setup examples

Edit **Bridge**, not the Garage, to select the installed providers:

```lua
-- /resources/[m4i]/m4i_bridge/config/providers.lua
providers = {
    selected = {
        framework = 'qbox',         -- m4i | qbox | qbcore | esx | ox_core
        inventory = 'ox_inventory', -- needs matching Bridge adapter
        target = 'ox_target',       -- m4i_target | ox_target | qb_target
        radial = 'qbx_radialmenu',  -- m4i_radialmenu | qb_radialmenu | qbx_radialmenu
        database = 'oxmysql',
        -- other configured domains retain appropriate existing settings
    },
}
```

This is an **illustrative excerpt**, not a replacement for the full `config/providers.lua` module. Change only the existing `providers.selected` values. Keep auto-detect disabled unless you deliberately configure and validate it.

Startup order (the actual framework/provider resources must be installed):

```cfg
ensure oxmysql
ensure <selected_framework>
ensure m4i_registry
ensure <selected_inventory>
ensure <selected_radial>
ensure <selected_target>
ensure m4i_bridge
ensure m4i_garage
```

The placeholders are intentional—replace them with resource names from the table, not literal `ensure <...>` statements. For native M4I load `m4i_registry`, then `m4i_core`, and keep any framework-required shared dependencies in their own supported order. The Garage uses the Bridge's `GetVehicleClassification`, currently backed by `m4i_registry` even on external framework providers, so ship a compatible vehicle catalogue or extend that Bridge provider before release.

## Framework-neutral character ownership

Garage's SQL tables were originally `BIGINT`-based while Qbox/QBCore/ESX commonly use string citizen/character IDs.

This release adds the **Garage-owned** table `m4ig_identity_map` (created on first external-framework startup, included in `sql/install.sql`). It maps `(framework, external_character_id)` to one stable numeric `BIGINT`, separated by framework. **Native M4I character IDs remain unchanged.** It never writes to any Qbox/QBCore/ESX/Ox Core player table.

Server-owned player state `m4igCharacterId` supplies the same mapped identity to local Garage UI/key visibility; it is a trusted replicated server value. Never accept a client-provided numeric ID as registration authority.

### Approved dealership example (server-side only)

```lua
local id, err = exports['m4i_garage']:GetGarageCharacterId(playerSource)
if not id then
    print('Garage identity unavailable:', err)
    return
end

-- Only invoke from a resource explicitly included in
-- Config.TrustedVehicleRegistrars.
local ok, vehicleIdOrReason = exports['m4i_garage']:RegisterOwnedVehicle(
    id, plate, model, category, props, garageId, spawnType, verifiedClass
)
```

Make this call only after the framework has finished loading the selected character; the Garage validates the trust allowlist. An existing external framework-owned vehicle is **not** automatically imported by installing `m4i_garage`.

## Critical differences and limitations

- **Vehicle cover with five physical uses:** Bridge's `ChargeVehicleCover`, `RefundVehicleCover`, and `FinalizeVehicleCover` currently use `m4i_inventory` transaction receipts. Basic `HasItem` / `AddItem` functionality may work through other Bridge inventory adapters, but five-use Cover cannot be claimed compatible with `qb_inventory` / `ox_inventory` without an equivalent atomic receipt adapter. The existing code deliberately fails closed.
- **Car identity migration:** Existing M4I ownership rows use native numeric IDs, whereas external frameworks use mapped Garage IDs. Changing the selected framework without planning ownership migration does **not** transfer or merge vehicles automatically.
- **Radial and Target:** Garage registers/removes items through Bridge, with dynamically queried provider readiness and restart recovery, but each custom Radial/Target resource needs an adapter implementing the same add/remove/visibility semantics. No universal compatibility with literally any resource is claimed.
- **Phone and image assets:** `lb-phone` integration and catalogue `m4i_upload` availability depend on installed resources. Some optional features may not be present on a third-party framework server.
- **Permissions and payments:** Bridge normalizes job/grade and bank operations for each provider. Source-level adapter tests do not verify the real user balances, provider-specific item metadata, payment refunds or live police/impound permissions on other frameworks.
- **Database:** `oxmysql` is required. Garage only writes its own `m4ig_*` tables; the framework owns its player and account tables.

## Verification sequence

1. Start your chosen Framework and Bridge; confirm `exports.m4i_bridge:GetProvider('framework')` equals the intended selected key.
2. Run `exports.m4i_garage:GetGarageCharacterId(source)` on the server from a trusted resource after a player logs in. The returned value must stay identical across reconnects to the same character and change after character switching.
3. Confirm Garage UI appears only inside the right 3D polygon and disappears outside, with the installed radial provider. Verify NPC Target on Impound and Seized with the installed target provider.
4. Test car registration by a trusted dealership, Spawn/Store, locked keys, shared/temporary key access, job-gated Seize, bank fees/refunds, and full/partial native repair.
5. Test Bridge inventory features separately; only enable five-use Cover when the selected inventory passes the receipt test.
6. Test actual two-client OneSync vehicle damage and full-repair persistence; automated tests do not guarantee exact custom-model debris at 200 real clients.

**Status:** bridge/garage Lua source contract tests passed on M4I TEST VPS. No live Qbox, QBCore, ESX or Ox Core session has yet been validated, so those integrations are not production-certified.
