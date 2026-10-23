# m4i_radialmenu

**Source inventory:** confirmed in the live Roleplay VPS filesystem on 2026-10-21. This page is a source-derived inventory, not a claim of runtime test coverage.

**Manifest description:** Native dynamic radial menu provider for the M4I ecosystem

**Manifest version:** 0.2.0-alpha.1

**M4I dependencies explicitly declared:** No explicit M4I dependency detected in the manifest (does not prove zero runtime dependencies)

**GitHub source:** [m4i-store/m4i_radialmenu](https://github.com/m4i-store/m4i_radialmenu)

## Source authority

The VPS copy at resources/[m4i]/m4i_radialmenu was treated as the most current candidate. Compare the working tree against the GitHub branch and resolve modifications before merging; do not overwrite VPS files with an older checkout.

## Integration and configuration

This script should use m4i_bridge for cross-resource and framework interactions. A configuration section becomes editable in m4i_confige only after the script provides an explicit validated settings schema. Configuration Lua files, secrets and runtime credentials are not directly editable through the UI. Confirm settings and exports by inspecting this script's current source.

## Documentation status

Only manifest metadata and repository availability are verified on this page. Commands, configuration keys, exports, migrations and gameplay behavior must be documented from actual source before being labeled supported.

## 2026-10-23 Confige 0.12.1 live adapter

Main commit 2b9c2a6 (Radial 0.2.1-alpha) supports server-authoritative changes to maximum root items, submenu items and nested menu depth. New values are validated and applied in place for the next menu render; player keybindings are not changed. Real in-game Save & Apply acceptance remains pending.
