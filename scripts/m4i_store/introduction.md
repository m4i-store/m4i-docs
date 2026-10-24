# m4i_store

**Source inventory:** confirmed in the live Roleplay VPS filesystem on 2026-10-21. This page is a source-derived inventory, not a claim of runtime test coverage.

**Manifest description:** M4I Store — Finance/Inventory checkout

**Manifest version:** 0.2.0-alpha.3

**M4I dependencies explicitly declared:** No explicit M4I dependency detected in the manifest (does not prove zero runtime dependencies)

**GitHub source:** [m4i-store/m4i_store](https://github.com/m4i-store/m4i_store) (private source snapshot created 2026-10-21)

## Source authority

The VPS copy at resources/[m4i]/m4i_store was treated as the most current candidate. Compare the working tree against the GitHub branch and resolve modifications before merging; do not overwrite VPS files with an older checkout.

## Integration and configuration

This script should use m4i_bridge for cross-resource and framework interactions. A configuration section becomes editable in m4i_confige only after the script provides an explicit validated settings schema. Configuration Lua files, secrets and runtime credentials are not directly editable through the UI. Confirm settings and exports by inspecting this script's current source.

## Documentation status

Only manifest metadata and repository availability are verified on this page. Commands, configuration keys, exports, migrations and gameplay behavior must be documented from actual source before being labeled supported.

## 2026-10-24 Confige V0.14 active Store settings

Store main c0e6f56 (0.2.0-alpha.4) exposes live InteractionDistance and DrawDistance settings. The shared adapter synchronizes client prompts with the server's actual store-interaction proximity policy. No product prices, catalog, basket, payments or inventory mechanics were modified. Runtime service active on M4I_TEST; direct in-game acceptance pending.
