# m4i_garage — Installation

**Source status:** TEST VPS package `v0.1.122-alpha`, November 2026. Earlier `m4i_garage` GitHub source snapshots and this GitBook page are not evidence that every historical build exposes the new API.

## Requirements

- FXServer with OneSync and Lua 5.4-compatible resource runtime
- `oxmysql`
- `m4i_bridge` (all framework and player/provider interactions)
- A radial provider configured and supported by `m4i_bridge` (e.g. `m4i_radialmenu`, `qb-radialmenu`, `qbx_radialmenu`)
- A target provider configured and supported by `m4i_bridge` (e.g. `m4i_target`, `ox_target`, `qb-target`)
- The Garage-owned SQL schema from `sql/install.sql`
- Optional integrations such as LB Phone and image lookup depend on their respective configured resources.

## Startup order

```cfg
ensure oxmysql
ensure m4i_radialmenu
ensure m4i_target
ensure m4i_bridge
ensure m4i_garage
```
The native M4I example above uses M4I's default radial and target; on a third-party framework choose installed Bridge-supported provider resource names as documented in [Five Frameworks and Bridge Providers](framework-compatibility.md).

Load core/registry providers before the bridge per the selected framework's documented startup sequence. Do not reorder the internal `client_scripts` or `server_scripts` entries arbitrarily: `server/exports.lua` and `client/exports.lua` are loaded after their underlying services.

## fxmanifest and editable files

The manifest keeps all arrays multiline (one dependency, script, asset or ignore path per line), using valid FiveM Lua syntax. Its `escrow_ignore` set is intentional:

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
These are editable configuration/documentation/extension files. Core vehicle custody, damage, permission and payment logic remains protected by the normal Asset Escrow packaging rules. Adding an ignore path **does not encrypt** or automatically upload a resource. Existing GTA stream assets follow their normal distribution/licensing rules.

## Deployment and smoke tests

On a staging server, back up the resource and its database before making configuration/schema changes. Ensure no active players are using a vehicle to avoid disrupting Spawn/Store. In FXServer Console:

```cfg
refresh
restart m4i_garage
```
Verify the resource starts, a permitted player can open a regular Garage, Store and retrieve a registered vehicle, shared/temporary access is enforced, and a second observer sees the saved damage without extra synthetic detached doors.

The source-level regression suite can run without spawning GTA clients:

```bash
lua tests/public_exports_contract_v0221.lua
lua tests/manifest_exports_escrow_v0221.lua
bash /tmp/m4ig-audit-suite.sh
```
The `audit-suite.sh` path above is part of the TEST VPS operator environment and not promised as a portable packaged release file.

See [Exports](exports.md) and [Integration](integration.md).
