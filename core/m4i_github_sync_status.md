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

The VPS contains m4i_dls, for which no matching repository has been created. This script contains GTA-related texture replacements, so its third-party asset licensing should be reviewed before uploading those assets. Private repositories were created for m4i_gameplay, m4i_garage, m4i_quickmenu and m4i_store, with manifest file references verified and sensitive runtime data excluded.

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


### Newly created private source repositories

- [m4i_gameplay](https://github.com/m4i-store/m4i_gameplay) — backed by the Roleplay VPS source; private repository. No running VPS files changed.
- [m4i_garage](https://github.com/m4i-store/m4i_garage) — backed by the Roleplay VPS source; private repository. No running VPS files changed.
- [m4i_quickmenu](https://github.com/m4i-store/m4i_quickmenu) — backed by the Roleplay VPS source; private repository. No running VPS files changed.
- [m4i_store](https://github.com/m4i-store/m4i_store) — backed by the Roleplay VPS source; private repository. No running VPS files changed.


The final Confige local-tested revision for this round is 15feffb. Repo source and additional docs were pushed, while GitHub Actions remained in failure without reported runner steps. No live restart or permission transfer took place.


## Latest local validation (2026-10-21)

m4i_confige commit 8e364f9 includes the local, quota-free 15-check CI runner and database-aware preflight. All 15 checks passed on the VPS. The resource/server configuration archive and 2.27 MB compressed MariaDB dump were checksum-verified. No production restart was performed. Remaining gates: authorize a trusted config editor through m4i.confige ACE and verify actual FiveM runtime behavior. Remote GitHub Actions remains quota-blocked; local CI is the preparation workaround.


## Dependency correction and final check

The newest m4i_confige source for this round is commit a24bef8. Its FiveM manifest explicitly depends on m4i_registry, m4i_core and m4i_bridge so the canonical registry must be present before the configuration editor loads. The current 15 local CI checks pass. No FXServer startup, config writer cutover, or live in-game acceptance testing was performed.


## Active Confige rollout and independent Admin canary — later 2026-10-21

m4i_confige v0.4.2-alpha, commit f154f47, passed a local 16-check CI suite including runtime health mocks. The Roleplay FXServer was restarted with no connected players, Confige loaded and its read-only runtime probe reported PASS for Core, Registry readiness, Bridge settings and theme reads. The live Registry and Bridge writer permissions now point to Confige, and the separate master-only owner ACE is in a protected untracked runtime file. Neither configuration nor any private identity was pushed to GitHub.

A distinct resource m4i_admin_next from the Admin draft branch was started alongside the legacy m4i_admin without replacing its local changes. Both resources appear in FiveM's loaded resource list, and the service is active. GUI operation in-game is pending. Source-drift-aware backup/rollback: /root/m4i-confige-precutover-20261021/cutover.py. Note that GitHub Actions is still quota constrained; local checks are the current validation path.


The separate m4i_admin_next canary source is available on m4i_admin branch canary/m4i-admin-next-20261021 at commit b6ae618.


## 2026-10-21 hotfix — client-side resource start

Confige 0.4.3-alpha commit 68eceb3 fixes a client join failure caused by declaring m4i_registry, which is server-only, as a manifest dependency. The failing user's Windows CitizenFX log explicitly identified this dependency. The refreshed source passed 16/16 local checks, was pushed to GitHub, and restarted on the VPS; Confige returned PASS for runtime service readiness. Actual in-game join retry is still unverified.


## Confige and Admin UI release (2026-10-21)

Confige 0.5.0-alpha at main commit 6818250 adds unified overview/navigation and protected runtime health. The separate m4i_admin_next canary 0.5.0-alpha at branch commit a3a5f68 adds structured staff operations pages, moderation warnings, basic revive/armour, waypoint/return and a validated vehicle catalog. The original m4i_admin source was intentionally not replaced. Browser navigation checks passed with mocked NUI responses, and no-player supervised restart loaded both releases on the Roleplay server. Next: test authenticated UIs in-game; implement comprehensive persistent moderation and framework integrations before promoting Admin Next as a full production replacement.

## 2026-10-22 Confige V0.6

Confige main a1e263f was deployed on the Roleplay VPS with a persistent Sidebar, 23 themes, six-language navigation, typography choices and Preview/Cancel/Save & Apply. Window Settings stores size and position locally per player. The live Bridge shared theme sanitizer was changed narrowly, backed up and checked; its source is available in draft cutover branch commit 76f9d4f.

The no-player service restart loaded 39 resources, with Confige health PASS after Registry initialization. 16/16 local CI and Chromium preview tests passed. Real player acceptance and integration of font/language across other independently implemented M4I interfaces are still pending.

## 2026-10-22 live control hub and upload

Confige 0.7.0-alpha main 7fe20c7, Inventory live command adapter 0.14.5-alpha from branch commit 1ecc295, and new private m4i_upload 0.1.0-alpha main df0d61d are deployed on the Roleplay VPS. Confige command index: 27 M4I folders, 44 literal source commands, 18 config-related files. Other non-integrated commands remain read-only until their adapters are written. Central M4I Upload initial library: 26 images; legacy original images preserved.

The startup warning on new resource directory permissions was corrected and re-tested. The final service log reported m4i_upload ready with 26 images and Confige runtime health PASS; 40 resources listed. Only the trusted master has m4i.upload ACE in a protected untracked server configuration. In-game upload and all cross-resource image consumers are pending acceptance tests.

## 2026-10-22 Confige V0.8 code ready, service reload deferred

GitHub main 36f1aa9 and Roleplay VPS source use Confige 0.8.0-alpha (full screen to 100%, expanded script-native launch buttons, integrated legacy Admin functions and audited Give Item). Three online players prevented a safe FXServer restart. Code is on disk but in-memory loaded resource still needs restart. Rollback archive and private ACL backup: /root/m4i-confige-v08-backup-20261022. Confige data and backups directories were fixed for write access by m4i_core_test to resolve snapshot persist failure, tested without restart. All 17 local checks passed and browser UI smoke passed.

Every M4I command and arbitrary Lua config is not universally hot editable; source-command entries lacking an adapter remain explicitly read-only for safety.

## 2026-10-22 Confige V0.9 staged, activation pending

M4I Confige main ad9a71e, HUD feature 65cbd27 and Garage feature 73744c2 introduce typed live HUD/Garage configurations and source-derived read-only Config catalogs. The VPS has the new source/manifests after verified backups, but a player was connected and no resource restart was performed. All 18 Confige local CI checks, HUD/Garage Lua mocks and Chromium UI smoke passed. Await controlled resource reload and real FiveM acceptance. Remaining M4I scripts still need validated hot adapters.

## 2026-10-22 Confige V0.9 runtime active, 40 resources

Confige main ad9a71e, Garage main 73744c2 and HUD feature branch 65cbd27 are installed on the Roleplay VPS. The first no-player restart revealed a root-owned 0600 manifest/source permission regression, temporarily preventing Confige from starting. This was corrected without changing private data/backups ownership, and a second no-player restart verified Confige/HUD/Garage started with 40 resources loaded. Confige health PASS after Registry initialization. Local CI 18/18, HUD/Garage mocks and Chromium UI smoke passed; first in-game settings save remains pending. Main HUD repository still depends on review of its earlier VPS sync source branch; do not independently fast-forward that repo without reviewing the full sync.
