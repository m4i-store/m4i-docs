# M4I GitHub ↔ Roleplay VPS synchronization status (2026-10-21)

These changes are **staged for review**. VPS running resources, production startup order and runtime credentials were not modified by this GitHub sync. Branch merges and actual deployment remain pending, and the staged configuration center cannot safely write until Bridge/Registry cutover occurs.

| Resource | Status | Link | Scope |
| --- | --- | --- | --- |
| m4i_confige | pushed main | [Review](https://github.com/m4i-store/m4i_confige/commit/7a8e2f5) | initial 0.4.1-alpha from live VPS |
| m4i_admin | draft PR | [Review](https://github.com/m4i-store/m4i_admin/pull/3) | staff-only 0.4.1-alpha, not deployed |
| m4i_bridge | draft PR | [Review](https://github.com/m4i-store/m4i_bridge/pull/8) | VPS source reconciliation + Confige-only settings/theme writes |
| m4i_registry | draft PR | [Review](https://github.com/m4i-store/m4i_registry/pull/3) | VPS source reconciliation + Confige-only registry writer |
| m4i_appearance | draft PR | [Review](https://github.com/m4i-store/m4i_appearance/pull/1) | VPS source delta |
| m4i_core | draft PR | [Review](https://github.com/m4i-store/m4i_core/pull/7) | VPS source delta |
| m4i_inventory | draft PR | [Review](https://github.com/m4i-store/m4i_inventory/pull/2) | VPS source delta without data |
| m4i_ledgegrab | draft PR | [Review](https://github.com/m4i-store/m4i_ledgegrab/pull/1) | VPS source delta |
| m4i_multicharacter | draft PR | [Review](https://github.com/m4i-store/m4i_multicharacter/pull/1) | VPS source delta |
| m4i_rental | draft PR | [Review](https://github.com/m4i-store/m4i_rental/pull/2) | VPS source delta |
| m4i_hud | draft PR | [Review](https://github.com/m4i-store/m4i_hud/pull/1) | VPS UI, script and asset delta |
| m4i_finance | draft PR | [Review](https://github.com/m4i-store/m4i_finance/pull/1) | VPS source delta; excludes runtime business/world presets |
| m4i_radialmenu | no differing safe source | [Review](https://github.com/m4i-store/m4i_radialmenu) | audit found no new diff against remote main for approved files |
| m4i_target | no differing safe source | [Review](https://github.com/m4i-store/m4i_target) | audit found no new diff against remote main for approved files |

## Missing same-name GitHub repositories

The VPS contains m4i_dls, m4i_gameplay, m4i_garage, m4i_quickmenu, and m4i_store, with no matching repository in the available m4i-store listing. These cannot be marked synchronized without establishing repositories and reviewing rights.

## Other resources not yet reconciled

m4i_livingworld, m4i_mechanic, m4i_underworld and m4i_weathersync have VPS sources without an active .git checkout and need a separate diff/audit against their respective repositories; current local source cannot be assumed identical to GitHub. m4i_appearance_assets and m4i_chat had no observed tracked delta. Resource binary assets and runtime data are not included in this source status.

## Verification and remaining blockers

- Local Lua syntax and static contract checks passed for the staged Confige and staff-only Admin builds. Admin mocked unit authorization tests also passed.
- Registry and Bridge cutover branches passed Lua syntax and their Python static checks. One Bridge performance unit test expects an external ../../before fixture and cannot pass in a clean checkout.
- At the time of inspection, GitHub Actions reported failed validate jobs with empty steps for the initial m4i_confige push and staff Admin feature branch. Treat remote CI as **unresolved**, not green.
- The new Admin UI is a basic staff tool suite, not feature parity with all QB/QS/CodeM menus. Confige live-edit currently supports Multicharacter settings and theme/registry; all other M4I scripts appear in inventory as read-only until validated adapters are built.
- Never merge a Registry writer revoke without simultaneously deploying the corresponding Confige and Bridge writer changes and verifying user ACE rights and backups.
- No FiveM live test for these branches has been performed. Do not claim production readiness based solely on mocked or syntax tests.

## Deployment order

Back up resources, database and server.cfg; inspect all draft PRs; review CI; set restricted Confige ACE and webhook secrets server-side; deploy matched Registry/Bridge/Confige package together in controlled maintenance; test edits and rollbacks; then migrate standalone staff Admin and remove legacy config controls.


## 2026-10-21 late-stage preflight

Initial Confige build f75cca4 added native Garage/Weather launcher, backup recovery and server authorization tests. Follow-up commit bfa3f8e added a no-mutation cutover preflight. A root-only and SHA-256-verified local code/config archive was created. The validator reports explicit blockers: the trusted m4i.confige ACE grant is absent; there is no complete real FiveM runtime test; GitHub Actions CI has failures with zero reported job steps. The production resource was deliberately not activated. Until these are resolved, existing m4i_admin remains the active config tool.
