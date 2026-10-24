# m4i_appearance

**Source inventory:** confirmed in the live Roleplay VPS filesystem on 2026-10-21. This page is a source-derived inventory, not a claim of runtime test coverage.

**Manifest description:** Native M4I character appearance, clothing, grooming, wardrobes, uniforms and ped access.

**Manifest version:** 4.1.0-alpha.1

**M4I dependencies explicitly declared:** m4i_bridge

**GitHub source:** [m4i-store/m4i_appearance](https://github.com/m4i-store/m4i_appearance)

## Source authority

The VPS copy at resources/[m4i]/m4i_appearance was treated as the most current candidate. Compare the working tree against the GitHub branch and resolve modifications before merging; do not overwrite VPS files with an older checkout.

## Integration and configuration

This script should use m4i_bridge for cross-resource and framework interactions. A configuration section becomes editable in m4i_confige only after the script provides an explicit validated settings schema. Configuration Lua files, secrets and runtime credentials are not directly editable through the UI. Confirm settings and exports by inspecting this script's current source.

## Documentation status

Only manifest metadata and repository availability are verified on this page. Commands, configuration keys, exports, migrations and gameplay behavior must be documented from actual source before being labeled supported.

## 2026-10-24 Confige V0.14 Appearance camera prototype, NOT ENABLED

Source on feature branch https://github.com/m4i-store/m4i_appearance/tree/feat/confige-camera-v014 (d20b62e). Client adapter supports bounded camera field of view, transition duration, smoothing and zoom. M4I_TEST intentionally disables m4i_appearance while rcore_clothing controls player appearances; the code is installed but does not run in this server. Never enable without separate migration/compatibility validation. Character data, ped rights and prices are unchanged.
