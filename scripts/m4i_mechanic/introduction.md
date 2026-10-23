# m4i_mechanic

**Source inventory:** confirmed in the live Roleplay VPS filesystem on 2026-10-21. This page is a source-derived inventory, not a claim of runtime test coverage.

**Manifest description:** M4I Mechanic — paid service fulfillment and persistent engine state

**Manifest version:** 0.1.4-alpha

**M4I dependencies explicitly declared:** No explicit M4I dependency detected in the manifest (does not prove zero runtime dependencies)

**GitHub source:** [m4i-store/m4i_mechanic](https://github.com/m4i-store/m4i_mechanic)

## Source authority

The VPS copy at resources/[m4i]/m4i_mechanic was treated as the most current candidate. Compare the working tree against the GitHub branch and resolve modifications before merging; do not overwrite VPS files with an older checkout.

## Integration and configuration

This script should use m4i_bridge for cross-resource and framework interactions. A configuration section becomes editable in m4i_confige only after the script provides an explicit validated settings schema. Configuration Lua files, secrets and runtime credentials are not directly editable through the UI. Confirm settings and exports by inspecting this script's current source.

## Documentation status

Only manifest metadata and repository availability are verified on this page. Commands, configuration keys, exports, migrations and gameplay behavior must be documented from actual source before being labeled supported.

## 2026-10-23 Confige Live Settings

Source at https://github.com/m4i-store/m4i_mechanic main commit 402fb5c is based on the latest Roleplay VPS Mechanic implementation with no live database files. A shared client/server live adapter accepts four bounded, schema-verified settings from M4I Confige: target and invoice-pair distance, vehicle network-control timeout and vehicle-state polling frequency. The original server-side invoice, character, job and finance checks remain intact. Source version 0.1.5-alpha; real in-game Save & Apply acceptance remains pending.
