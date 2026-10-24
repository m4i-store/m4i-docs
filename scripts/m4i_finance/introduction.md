# m4i_finance

**Source inventory:** confirmed in the live Roleplay VPS filesystem on 2026-10-21. This page is a source-derived inventory, not a claim of runtime test coverage.

**Manifest description:** M4I Finance — guarded financial foundation and in-game creator

**Manifest version:** 0.2.0-alpha.15

**M4I dependencies explicitly declared:** No explicit M4I dependency detected in the manifest (does not prove zero runtime dependencies)

**GitHub source:** [m4i-store/m4i_finance](https://github.com/m4i-store/m4i_finance)

## Source authority

The VPS copy at resources/[m4i]/m4i_finance was treated as the most current candidate. Compare the working tree against the GitHub branch and resolve modifications before merging; do not overwrite VPS files with an older checkout.

## Integration and configuration

This script should use m4i_bridge for cross-resource and framework interactions. A configuration section becomes editable in m4i_confige only after the script provides an explicit validated settings schema. Configuration Lua files, secrets and runtime credentials are not directly editable through the UI. Confirm settings and exports by inspecting this script's current source.

## Documentation status

Only manifest metadata and repository availability are verified on this page. Commands, configuration keys, exports, migrations and gameplay behavior must be documented from actual source before being labeled supported.

## 2026-10-23 Finance settings discovery

Confige 0.12.1 lists 34 Finance source configuration field names as reference-only metadata, including transaction limits, fees, invoice rules and creator constraints. Financial settings cannot be modified in this interface until a dedicated transactional, audited and permission-enforcing native Finance adapter has been created. No Finance source, account state or financial value was changed during this release.

## 2026-10-24 Confige V0.13 nonmonetary settings adapter

The private m4i_finance GitHub main commit 1ffccbf adds an audited, bounded, in-place GlobalState runtime adapter for BillingTargetDistance, CreatorPlacementDistance and CreatorMaxLocations. The Finance config remains authoritative. Monetary balances, fees, tax rates, account rights and live transaction thresholds are NOT editable through this panel. Confige owns revisioning, permission checks, mandatory backups and persisting the three nonmonetary settings only. The in-game acceptance test is pending.
