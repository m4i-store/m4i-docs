# m4i_garage — Configuration

**Applies to:** staged TEST VPS source `v0.1.122-alpha`. Configuration availability may differ in older snapshots or future releases.

## Editable files and Asset Escrow

`config.lua` is the script's local configuration. The following integration/config files are listed in the manifest's `escrow_ignore`:

```lua
escrow_ignore {
    'config.lua',
    'data/*.json',
    'docs/*.md',
    'docs/*.txt',
    'sql/*.sql',
    'README.md',
    'client/exports.lua',
    'server/exports.lua',
}
```
Game-critical custody, key validation, anti-duplication, automatic condition saving, deformation reconstruction and police Seize algorithms are **not** globally escrow-ignored. Do not add `server/*.lua` or `client/*.lua` wholesale to `escrow_ignore` when distributing this resource unless you deliberately intend to expose all of that source.

The framework, target, radial and inventory providers are selected in `m4i_bridge/config/providers.lua` (its existing `providers.selected` table), **not** through `m4i_garage/config.lua`. See [Five Frameworks and Bridge Providers](framework-compatibility.md).

## Main settings relevant to integrations

| Key | Current test value / behavior | Important warning |
| --- | --- | --- |
| `Config.TrustedVehicleRegistrars` | `{}` by default | Exact names of authorized **server resources** that may call `RegisterOwnedVehicle`. No arbitrary client writes |
| `Config.RepairTrustedResources` | Controlled resource allowlist | Only trusted repair/server scripts may request `BeginFullRepair` permits |
| `Config.CreatorAce` | `m4i.garage.admin` | Required creator administration ACE |
| `Config.StoreDistance` | `3.0` meters | Storage requires real nearby signed vehicle, validated on server |
| `Config.StorePassengerExitTimeoutMs` | `8000` milliseconds | Normal passenger leave animation; never delete occupied vehicle |
| `Config.StorePassengerMaxSpeed` | `1.25` m/s | Automatic passenger exit only when near-stationary |
| `Config.SpawnClearance` | `3.0` meters fallback | Online Garage Creator options may override |
| `Config.ConditionAutoSaveTickMs` | `30000` milliseconds | Saved SQL condition can lag live physics |
| `Config.DebugVehicleDamagePersistence` | `true` on TEST | Verbose diagnostics; disable for production unless investigating damage |
| `Config.VehicleDeformation` | Engine deformation options | Signed Garage vehicles only |
| `Config.MaxVehiclePropertiesBytes` | `16000` bytes | Limits registered vehicle property payload |

All player identity, job, group and inventory integration continues through `m4i_bridge`. Do not configure Qbox/ESX/Core direct calls in custom Garage exports.

## Integration allowlists

```lua
-- Example ONLY: enable after the resource has been reviewed and tested.
Config.TrustedVehicleRegistrars = {
    ['m4i_store'] = true
}

-- Trusted repair allowlists must match GetInvokingResource() exactly.
-- Review Config.RepairTrustedResources in the installed version.
```
Do not add any generic net event or insecure resource that can be invoked from clients to these allowlists.

## Global settings

Garage Creator and live configuration support server-validated settings for Garage Spawn, Cover and delivery behavior. Changing a public `GetGarage()` snapshot does **not** save these settings. Use the actual authorized admin/Creator flow.

For API use, see [Exports](exports.md). For resource dependencies, see [Installation](installation.md).
