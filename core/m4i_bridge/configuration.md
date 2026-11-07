# M4I Bridge — Current Customer Configuration

**Release:** `1.5.19-rc.1` (7 November 2026). For a full installation profile, see [Installation & Framework Selector](setup-selector.md). For actual third-party options, see [Provider IDs & Custom Integrations](third-party-providers.md).

## Edit this one file

Open `resources/[m4i]/m4i_bridge/config.lua`. The customer-friendly table is `M4IBridgeConfig`:

```lua
M4IBridgeConfig = {
    Framework = 'm4i',
    Inventory = 'framework',
    UI = 'framework',
    Notify = 'framework',
    Progress = 'framework',
    Radial = 'framework',
    Target = 'framework',
    Phone = 'auto',
    Vehicles = 'auto',
    Keys = 'framework',
    Dispatch = 'framework',
    Banking = 'framework',
    Appearance = 'framework',
    Database = 'framework',
}
```

Choose `Framework = 'm4i'`, `'qbcore'`, `'qbox'`, `'esx'`, or `'ox_core'` according to the **actual installed core**. Change the other domains only to Bridge-adapter IDs shipped with the script or to an adapter you implemented. Each domain selection is independent: your server can use QBCore framework with Ox Target, for example, if both matching adapters work.

### Default framework provider bundles

- **M4I:** `m4i_inventory`, `m4i_hud`, `m4i_target`, `m4i_radialmenu`; start `m4i_registry` and `m4i_core` first.
- **QBCore:** `qb_inventory`, `qb_textui`, QB notify, `qb_target`, `qb_radialmenu`, `progressbar`.
- **Qbox:** `ox_inventory`, `ox_lib`, Qbox notify, `ox_target`, `qbx_radialmenu`.
- **ESX:** `esx_inventory`, `esx_textui`, ESX notify, `ox_target`, `m4i_radialmenu`, `esx_progressbar`. If the customer's ESX uses `ox_inventory` instead, explicitly choose that adapter.
- **Ox Core:** `ox_inventory`, `ox_target` and selected UI/Radial adapters; validate real implementation and dependencies.

The default provider is a **configuration**, not a package installer. No replacement Inventory, Phone, Target or Radial is downloaded automatically. For missing radial Garage can use `Config.InteractionMode='keys'`.

## Important: avoid conflicting overrides

Legacy `setr m4i_bridge_profile <framework>` in `server.cfg` overrides `Framework` in `config.lua`. Remove conflicting old `setr` lines or make the value identical. Internal `config/providers.lua` and `config/third_party.lua` build adapter selection from the customer config; **do not replace them**. Add a new adapter implementation under `adapters/<domain>/<provider_id>/` if the customer's actual vendor version needs it.

The Bridge's framework selection will not silently fall back to a different framework when the chosen one fails. Verify provider readiness, player money, inventory, callbacks, notifications and restart recovery before production.

## Beyond the simple config

The shipped internal `config/default.lua` and `config/features.lua` define security, callbacks, logging, performance and feature flags. Keep defaults until a tested requirement justifies a change. Banking personal balances must not be replaced with society/job-account SQL queries. Use Garage's server permission and vehicle custody APIs for any external dealership/mechanic logic.

**Related:** [Garage installer](../../scripts/m4i_garage/framework-installation.md) · [Third-party recipes](../../scripts/m4i_garage/integration-recipes.md) · [Acceptance checklist](../../shared/fivem-qa-checklist.md).