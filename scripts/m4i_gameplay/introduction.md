# m4i_gameplay

**Source inventory:** confirmed in the live Roleplay VPS filesystem on 2026-10-21. This page is a source-derived inventory, not a claim of runtime test coverage.

**Manifest description:** Independent GTA gameplay rules for M4I

**Manifest version:** 1.1.0

**M4I dependencies explicitly declared:** No explicit M4I dependency detected in the manifest (does not prove zero runtime dependencies)

**GitHub source:** [m4i-store/m4i_gameplay](https://github.com/m4i-store/m4i_gameplay) (private source snapshot created 2026-10-21)

## Source authority

The VPS copy at resources/[m4i]/m4i_gameplay was treated as the most current candidate. Compare the working tree against the GitHub branch and resolve modifications before merging; do not overwrite VPS files with an older checkout.

## Integration and configuration

This script should use m4i_bridge for cross-resource and framework interactions. A configuration section becomes editable in m4i_confige only after the script provides an explicit validated settings schema. Configuration Lua files, secrets and runtime credentials are not directly editable through the UI. Confirm settings and exports by inspecting this script's current source.

## Documentation status

Only manifest metadata and repository availability are verified on this page. Commands, configuration keys, exports, migrations and gameplay behavior must be documented from actual source before being labeled supported.

## 2026-10-24 Gameplay live controls in Confige

m4i_gameplay main a832900 version 1.2.0-alpha supports nine server-authoritative, bounded gameplay policy settings exposed through Confige main 0b0390e. Confige persists, audits and revises settings before applying. The client now refreshes weapon-wheel native control arrays, vehicle rewards, NPC scan interval and batch size, pickup ownership and future NPC drops without a resource restart. Worker execution idles when disabled. Already-marked NPC flags cannot be restored because their original state is unknown. Initial controlled install and service startup were verified, but real GTA client/owner Save & Apply and performance acceptance are still pending.
