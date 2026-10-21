# M4I Roleplay source and documentation inventory

This table was generated from the VPS resource folders on 2026-10-21 and a connected GitHub repository listing. It is a **source inventory**, not a runtime verification report.

| VPS resource | Manifest version | GitHub repository | Docs |
| --- | --- | --- | --- |
| m4i_admin | 0.3.3-alpha | [Available](https://github.com/m4i-store/m4i_admin) | [Core](m4i_admin.md) |
| m4i_appearance | 4.1.0-alpha.1 | [Available](https://github.com/m4i-store/m4i_appearance) | [Script](../scripts/m4i_appearance/introduction.md) |
| m4i_appearance_assets | 0.1.0-rc.1 | [Available](https://github.com/m4i-store/m4i_appearance_assets) | [Script](../scripts/m4i_appearance_assets/introduction.md) |
| m4i_bridge | 1.5.1-rc.3 | [Available](https://github.com/m4i-store/m4i_bridge) | [Core](m4i_bridge/introduction.md) |
| m4i_chat | 0.1.0 | [Available](https://github.com/m4i-store/m4i_chat) | [Script](../scripts/m4i_chat/introduction.md) |
| m4i_confige | 0.4.0-alpha | [Available](https://github.com/m4i-store/m4i_confige) | [Core](m4i_confige.md) |
| m4i_core | 0.5.0-alpha.1 | [Available](https://github.com/m4i-store/m4i_core) | [Core](m4i_core/introduction.md) |
| m4i_dls | 1.0.0 | Not found — requires repository decision | [Script](../scripts/m4i_dls/introduction.md) |
| m4i_finance | 0.2.0-alpha.15 | [Available](https://github.com/m4i-store/m4i_finance) | [Script](../scripts/m4i_finance/introduction.md) |
| m4i_gameplay | 1.1.0 | Not found — requires repository decision | [Script](../scripts/m4i_gameplay/introduction.md) |
| m4i_garage | 0.1.3 | Not found — requires repository decision | [Script](../scripts/m4i_garage/introduction.md) |
| m4i_hud | 1.3.10 | [Available](https://github.com/m4i-store/m4i_hud) | [Script](../scripts/m4i_hud/introduction.md) |
| m4i_inventory | 0.14.4-alpha | [Available](https://github.com/m4i-store/m4i_inventory) | [Script](../scripts/m4i_inventory/introduction.md) |
| m4i_ledgegrab | 0.4.1 | [Available](https://github.com/m4i-store/m4i_ledgegrab) | [Script](../scripts/m4i_ledgegrab/introduction.md) |
| m4i_livingworld | 0.4.3-alpha.1 | [Available](https://github.com/m4i-store/m4i_livingworld) | [Script](../scripts/m4i_livingworld/introduction.md) |
| m4i_mechanic | 0.1.4-alpha | [Available](https://github.com/m4i-store/m4i_mechanic) | [Script](../scripts/m4i_mechanic/introduction.md) |
| m4i_multicharacter | 1.0.0-rc.8 | [Available](https://github.com/m4i-store/m4i_multicharacter) | [Script](../scripts/m4i_multicharacter/introduction.md) |
| m4i_quickmenu | 0.1.0 | Not found — requires repository decision | [Script](../scripts/m4i_quickmenu/introduction.md) |
| m4i_radialmenu | 0.2.0-alpha.1 | [Available](https://github.com/m4i-store/m4i_radialmenu) | [Script](../scripts/m4i_radialmenu/introduction.md) |
| m4i_registry | 0.2.0-alpha.3 | [Available](https://github.com/m4i-store/m4i_registry) | [Core](m4i_registry.md) |
| m4i_rental | 4.1.5 | [Available](https://github.com/m4i-store/m4i_rental) | [Script](../scripts/m4i_rental/introduction.md) |
| m4i_store | 0.2.0-alpha.3 | Not found — requires repository decision | [Script](../scripts/m4i_store/introduction.md) |
| m4i_target | 0.2.0-alpha.1 | [Available](https://github.com/m4i-store/m4i_target) | [Script](../scripts/m4i_target/introduction.md) |
| m4i_underworld | 0.5.0-dev | [Available](https://github.com/m4i-store/m4i_underworld) | [Script](../scripts/m4i_underworld/introduction.md) |
| m4i_weathersync | 1.1.3 | [Available](https://github.com/m4i-store/m4i_weathersync) | [Script](../scripts/m4i_weathersync/introduction.md) |

## Sync rules

- Treat VPS as the latest candidate, not an unquestioned safe snapshot. Review local changes before pushing.
- Never commit secrets, server.cfg credentials, logs, database or runtime cache.
- Missing GitHub repos cannot be automatically synchronized to a non-existent remote.
- Auto-generated introductions document only manifest-derived facts; full source/API documentation remains a separate task.
