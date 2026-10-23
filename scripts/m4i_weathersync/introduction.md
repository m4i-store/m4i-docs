# m4i_weathersync

**Source inventory:** confirmed in the live Roleplay VPS filesystem on 2026-10-21. This page is a source-derived inventory, not a claim of runtime test coverage.

**Manifest description:** Authoritative, synced FiveM time and weather with day/night durations and random weather blacklist

**Manifest version:** 1.1.3

**M4I dependencies explicitly declared:** No explicit M4I dependency detected in the manifest (does not prove zero runtime dependencies)

**GitHub source:** [m4i-store/m4i_weathersync](https://github.com/m4i-store/m4i_weathersync)

## Source authority

The VPS copy at resources/[m4i]/m4i_weathersync was treated as the most current candidate. Compare the working tree against the GitHub branch and resolve modifications before merging; do not overwrite VPS files with an older checkout.

## Integration and configuration

This script should use m4i_bridge for cross-resource and framework interactions. A configuration section becomes editable in m4i_confige only after the script provides an explicit validated settings schema. Configuration Lua files, secrets and runtime credentials are not directly editable through the UI. Confirm settings and exports by inspecting this script's current source.

## Documentation status

Only manifest metadata and repository availability are verified on this page. Commands, configuration keys, exports, migrations and gameplay behavior must be documented from actual source before being labeled supported.

## 2026-10-23 Canonical Confige Weather Settings

WeatherSync source at https://github.com/m4i-store/m4i_weathersync main commit 7cd42ca (1.1.4-alpha) exposes authenticated server-only Confige getters and setters for dynamic weather, change interval and transition duration. Native WeatherSync state.json remains authoritative and verified upon write. Its original admin UI increments the same revision when these fields change, preventing stale saves from Confige. FiveM runtime startup restored existing state without overwriting it. Confige V0.11 also supports launching the original Weather & Time UI for broader controls including in-game time, day/night lengths, and blacklist. Live in-game Save & Apply still needs owner acceptance testing.
