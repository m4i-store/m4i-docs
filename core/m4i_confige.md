# m4i_confige — Central Configuration Control

**Verified initial package:** 0.4.1-alpha at m4i-store/m4i_confige, commit 7a8e2f5 (2026-10-21). This is staged on Roleplay VPS, not yet activated in the production start order.

## Responsibilities
- One UI for M4I canonical definitions, global themes, registered script settings and resource inventory.
- Strict ACE m4i.confige verified on the server for every request, including edits and panel opening.
- Server-owned read/write API. NUI cannot decide its own authority or access Lua file paths.
- Mutations only via m4i_registry or m4i_bridge settings/theme API with expectedVersion/expectedRevision.
- Pre-mutation local snapshots (120-slot bounded ring), audit records (300-record ring) and optional redacted Discord webhook. Webhook secret stays in private server cfg, not GitHub.
- No unrestricted file editor, code execution, scripts start/stop, or unvalidated settings payloads.

## Script onboarding
All installed resources appear in Script Configuration inventory. In the initial build, only m4i_multicharacter has a live-editable settings adapter. To enable another script, define a typed settings document, validate every field server-side and support optimistic concurrency. Resource ownership of runtime settings remains in m4i_core through m4i_bridge.

## Required write-boundary cutover
1. Back up m4i_admin, m4i_registry, m4i_bridge, server.cfg and database. Do not put credentials into public backups.
2. Configure an explicit trusted identifier ACE m4i.confige; keep access denied by default.
3. Add m4i_confige as a registry-approved writer; once fully cut over, revoke m4i_admin from that list.
4. Change m4i_bridge settings and theme mutation permissions to m4i_confige only.
5. Ensure order: m4i_registry, m4i_core, m4i_bridge, m4i_confige.
6. Remove definitions, settings and theme UI/callbacks from m4i_admin after the replacement player/staff administrative panel has passed tests.
7. Verify a denied user cannot trigger any mutator or REST/NUI event; verify authorized edits, rollback, backups, webhook, concurrent revision failures, resource restarts and game restart persistence.

These are required steps for a production migration; the staged initial package alone does not perform the cutover.

## GitHub/VPS synchronization
Live server copies contain modified and sometimes untracked files not yet mirrored to GitHub. Review each resource diff first, exclude secrets and runtime data, validate source integrity, then use a reviewed commit or PR. Never reset the VPS to an older GitHub snapshot or automatically push .cfg secrets.

Repository: https://github.com/m4i-store/m4i_confige


## 2026-10-21 staging update

- The standalone Confige source was first staged at commit bfa3f8e, staged on VPS and synchronized to GitHub main.
- The script inventory can hand off to the native Garage Creator and Weather Dashboard. These target systems still require their own server-side permissions, and this handoff is not a generic raw Lua file editor.
- The server now supports an explicit read-only backup inventory command (m4iconfig:backupinfo) and a console-only restore command (m4iconfig:restore slot current_revision CONFIRM). All restore attempts must compare live revision and create a pre-restore backup.
- Mocked Lua tests cover ACE denial, registry changes, tool launch validation, failed backups, replay denial, console-only restores and optimistic revision constraints.
- A SHA-256-checked, owner-root-only rollback archive was created locally on the VPS at /root/m4i-confige-precutover-20261021. This is NOT an offsite database backup.
- A read-only cutover preflight is available under tools/preflight.py. It currently reports ready=false due to missing Confige ACE, no validated in-game cutover, and failing GitHub Actions job startup.
- Production server.cfg still starts legacy m4i_admin and NOT m4i_confige. The existing Bridge/Registry writer guards are unchanged.
- Do not merge the related draft PRs individually; coordinate a maintenance-window cutover.


## Native tool integrations
M4I Confige resource inventory now exposes whitelisted entry points for m4i_garage Garage Creator and m4i_weathersync Weather Dashboard. Both destination scripts continue enforcing their own server-side administrator permissions. This integration is a management launcher, not a wholesale config-file editor.


## Audit integrity fix

Confige commit 15feffb adds fail-closed handling for corrupted on-disk backup indexes and expands mocked recovery tests to include Registry, Multicharacter settings, and global UI theme restores. The repo remains staged, not enabled in server.cfg.


## GitHub Actions quota workaround and guarded cutover (2026-10-21)

The user-supplied GitHub billing screenshot showed 3,000/3,000 included Actions minutes and 2GB/2GB included Actions storage consumed. The new workflow runs were terminating with no runner steps. A VPS local test runner, bash tools/local_ci.sh, was added at m4i_confige commit 8e364f9. Its 15 checks include Lua/JavaScript syntax, static contracts, mocked security and recovery, Bridge/Registry and staged Admin. The external Bridge before/after performance test fixture is excluded.

A read-only cutover preflight independently verifies the root-only code/config archive and compressed live database backup by SHA-256. It accepts a passing local CI result as substitute for quota-blocked GitHub Actions while still requiring a trusted, explicit m4i.confige ACE grant and genuine FiveM runtime tests. All three Confige server request modules reject fallback to m4i.admin.

No production FXServer restart or permission transfer has been performed. The database archive is held under /root/m4i-confige-precutover-20261021 on the VPS. Prepare an encrypted offsite backup before production deployment.

The optional safe administrator ACE template is config/ace.example.txt; grant only specific trusted licenses rather than indiscriminately broad staff groups.


## Dependency correction and final check

The newest m4i_confige source for this round is commit a24bef8. Its FiveM manifest explicitly depends on m4i_registry, m4i_core and m4i_bridge so the canonical registry must be present before the configuration editor loads. The current 15 local CI checks pass. No FXServer startup, config writer cutover, or live in-game acceptance testing was performed.


## 2026-10-21 supervised FiveM activation (latest status)

**Supersedes the earlier staging-only notes above:** Confige is now enabled in server.cfg and has been started by a supervised fivem-txadmin systemd restart at a moment with zero connected players. The enabled resource is m4i_confige version 0.4.2-alpha, source commit f154f47. Its read-only runtime dependency check logged result=PASS after a normal initial RETRY while m4i_registry was still initializing.

The production Bridge Settings/Theme writer gates were changed narrowly from m4i_admin to m4i_confige. The Registry writer allowlist was likewise changed to m4i_confige. Local source differences unrelated to the writer gate were preserved; no wholesale overwrites were made. An explicitly scoped m4i.confige ACE was added in a private runtime configuration for the one txAdmin master CitizenFX identity. Do not publish this configuration file or the numeric identifier.

The protected archive in /root/m4i-confige-precutover-20261021 contains checksummed code/configuration and a compressed SQL backup. The root-only cutover.py script records SHA-256 drift checks and can restore the four changed files on disk with --rollback, followed by a supervised service restart. The root-only manifest has been updated for the separate Admin canary described in core/m4i_admin_canary.md.

**Runtime verified:** FXServer service active, Confige resource loaded, Registry ready, Bridge resource settings read available, Bridge theme read available. **Not yet verified:** a real owner/admin player session opening /m4iconfig and saving then safely restoring an item or setting through NUI. Until a controlled in-game test, treat the UI write path as conditionally verified, not production-proven.


## FiveM client join failure — manifest dependency hotfix (2026-10-21)

The user's Windows FiveM log reported Could not find dependency m4i_registry for resource m4i_confige. Registry is a server-only resource, hence it is not a valid client dependency for a mixed client/server NUI resource. Confige incorrectly declared a manifest dependency that let the server start but prevented client join.

Confige release commit 68eceb3, version 0.4.3-alpha, removes that dependency while retaining ensure m4i_registry before ensure m4i_confige in server.cfg, and adds a static regression test. After release the local 16-test CI passed, the roleplay server was restarted with no connected players, the resource loaded, and server-side health returned PASS. Player reconnection after the fix has not yet been observed.


## UI console refresh — 0.5.0-alpha (2026-10-21)

Confige main commit 6818250 introduces a unified NUI management console. The opening Overview displays read-only runtime service status, registered/running M4I resources and counts of settings adapters and native management tools. Persistent primary navigation now includes Overview, Definitions, Script Inventory, Theme & Language, and Multicharacter. Existing Registry editing, validation, revision workflows, global theme settings, safe import, and audit/backup handling remain intact; this change does not create arbitrary Lua-file editing access.

Chromium browser interaction tests with a mocked NUI transport passed for all five route transitions. The running resource remains ACE-protected and its new health read is served through the existing authorized Confige action dispatcher. Production resource started after a no-player supervised restart; a privileged owner's in-game interface test remains outstanding.

## 2026-10-22 Confige V0.6 sidebar and window layout rollout

The Roleplay VPS now runs m4i_confige 0.6.0-alpha (GitHub main a1e263f). The updated interface has a fixed Sidebar for Overview, Definitions, M4I Scripts, Theme & Language, Multicharacter and Window Settings. The rail moves to the right for Arabic and Moroccan Darija. English, Arabic, Darija, French, Spanish and Italian are available. Main navigation and headings are translated; some resource-specific legacy settings labels still need localization.

There are 23 built-in themes, including M4I Admin Green, Kick Green and Matte Green, and server-audited custom palettes. Colors, locale and typography are previewed within Confige before Save & Apply. Cancel Preview restores the last saved snapshot. The backend saves through the existing permission-checked Bridge theme service, with backup, auditing and revision constraints. The Bridge sanitizer now preserves locale (including Darija), typography (modern, Arabic, compact, large), name and curated preset choice. The saved theme is broadcast to clients, but independent M4I UIs need field-specific integration to actually render a new font or language.

Window Settings supports dragging the top bar, resizing the bottom corner, size sliders, nine positions, three sizes, Cancel, Reset and Save. The geometry is clamped to the viewport and stored locally on each player's PC/browser, not broadcast to every player's monitor.

Verified protected backup is at /root/m4i-confige-v06-backup-20261022. The narrow live Bridge theme-file change preserves other VPS modifications. Related reviewed source is in the pending GitHub Bridge draft branch feat/confige-write-cutover commit 76f9d4f; do not merge the entire old cutover PR without independently reviewing other changes.

Local Confige CI: 16/16. Bridge theme sanitization mock: pass. Chromium UI smoke: pass for Preview, Cancel, theme Save payload, RTL, typography, window drag/resize and persistence. The Roleplay server was restarted with no connected players; 39 resources loaded and Confige runtime health reported PASS after Registry initialized. The actual in-game Save & Apply path and all external M4I UI font/language consumers remain to be user acceptance-tested.

## 2026-10-22 Script Control Hub V0.7 — staging, not live

A separate Confige branch feat/script-control-hub-v07 at commit 07f0053 builds a per-M4I-resource command directory. Admins select a script, see the commands discoverable from its declared Lua source, their verified descriptions where available, and the names of declared configuration files. Commands without validated resource adapters remain read-only and clearly labeled; introspection cannot guarantee complete discovery of dynamically registered commands.

The first integrated live edit path is m4i_inventory inventory.open: command alias using the m4iinv_ namespace, keyboard default, enabled flag, admin-only/all/disabled access, and a menu-hiding hint. The central store is revisioned, backed up and audited, and publishes a GlobalState snapshot to connected/late-joining clients. Confige refuses edits until the Inventory resource declares a compatible live adapter. Inventory enforces access on the server for self and vehicle open events, so client bypassing a hidden button does not bypass authorization. Security-tested mocks and a Chromium NUI interactive smoke passed.

The Inventory adapter source is staged separately in m4i_inventory branch feat/confige-live-commands-v1, commit 1ecc295. It preserves the existing live inventory modifications and changes only the adapted client/server entry points plus manifest metadata. IMPORTANT: FiveM retains player-customized RegisterKeyMapping bindings locally; the implementation creates revisioned default mappings and makes previous revision handlers inert but cannot forcibly erase everyone else's personalized bindings. Hidden is a presentation hint, not secrecy from F8 console or client-side scripts.

**Neither branch is deployed to the active server yet.** A player was connected when the first release check was performed. Existing live Confige 0.6 and inventory sessions have been deliberately left unchanged to avoid interrupting players. Next rollout requires confirming the server is empty, creating a protected code+DB backup/rollback plan, applying only reconciled latest files, and restarting the affected services. Once live, each additional M4I script needs its own validated command/configuration adapter for hot apply; arbitrary Lua config edits cannot universally be made live without script support.

## 2026-10-22 activated Script Control Hub V0.7

Confige main 7fe20c7 is active on Roleplay VPS. M4I Scripts now shows per-resource command directories as lines. A checked source index covers 27 M4I resource folders with 44 statically detected commands and 18 config-related Lua file names. Dynamically registered commands can be missed; non-integrated command/config entries are clearly read-only. The first real hot-edit adapter belongs to Inventory 0.14.5-alpha (source branch feat/confige-live-commands-v1 commit 1ecc295), for Open Inventory name, keyboard default, visibility hint, enabled state and ACE-backed server access. Settings are revisioned, backed up, audited and replicated with GlobalState to current/future clients. FiveM stores user-modified keybindings locally: obsolete command handlers can be disabled but saved player binds cannot universally be overwritten remotely.

m4i_upload image library is available in the resource list with a protected Open Tool button and the in-game /m4iupload command. See scripts/m4i_upload/introduction.md.

The rollout had zero connected players. A protected snapshot lives at /root/m4i-control-hub-predeploy-20261022. After correcting upload directory permissions, 40 resources started, m4i_upload logged 26 catalog images, and Confige health PASS. Confige local CI 17/17; Upload server and browser tests passed. In-game Save & Apply and additional per-resource command/config adapters are still outstanding.

## 2026-10-22 Confige V0.8 — source prepared, runtime reload pending

Confige source on Roleplay VPS and GitHub main has been updated to 0.8.0-alpha at commit 36f1aa9; the code is also in feat/confige-script-suite-v08. The active FXServer resource still has previous code loaded until a controlled restart, which was deferred because three players were connected. Protected source and ACE backup: /root/m4i-confige-v08-backup-20261022.

The original Confige save failure (persist failed: data/backups/snapshot-001.json) was caused by the data/ and data/backups/ folders being owned by root and not writable by the FXServer service account m4i_core_test. The live folder ownership was fixed, mode set to 0750, and a temporary test file was written and removed successfully as the service account. No server restart needed for this permission correction; a real in-game Save still requires validation.

Window Settings now accepts 100% width and 100% height in the sliders, presets, and resize boundaries. A new integrated Admin Tools screen combines Registry definitions and Smart Import, Theme, Multicharacter settings, Garage Creator, Vehicle Recovery, and a new audited Give Item operation. Give Item uses a separate owner-only m4i.confige.giveitem ACE, verifies item in Registry, checks the target player's carrying capacity, performs a mandatory backup snapshot before using M4I Bridge AddItem, then logs the result. The private ACE has been staged for the next resource/server load.

Individual Script Control pages include explicit buttons for validated native management tools: Garage Creator and Recovery, Weather/Time, M4I Upload Image Library, and HUD Layout. Other source-discovered commands and config file names remain read-only until each script has a validated server-side live adapter. Generic source introspection cannot safely make arbitrary FiveM Lua config fields immediately writable.

Local Confige CI: 17/17 passes. Chromium NUI mock tested full-screen dimensions, integrated Admin Tools, Grant Item form, Inventory command controls, and script-specific tool buttons. Activation inside real FiveM is pending a safe maintenance window; the original server is still active.

## 2026-10-22 Confige V0.9 — typed live configuration adapters

Confige main ad9a71e (0.9.0-alpha) now has a schema-driven configuration panel inside each adapted M4I Script page. HUD has 6 supported settings: ShowLocation, ShowMinimapOnFoot, ShowMinimapInVehicle, MinimapEnabled, Units (kmh/mph), CinematicEnabled. Garage has 4 settings: StoreDistance, TransferBaseFee, GpsPurchaseFee and DefaultImpoundFee. The older Inventory command editor and Multicharacter settings editor remain supported.

Settings use an allowlist, typed validation, optimistic revisions, verified mandatory backups and audit logging. After a successful persistent write to Confige data/script_settings.json, the server publishes GlobalState snapshots to present and future clients. HUD consumes the new snapshots client-side, and Garage consumes them in server and client code. Confige refuses changes if a compatible resource adapter is not installed and started. 257 static Config property names from 9 M4I scripts are now discoverable without exposing raw values, but unsupported keys remain read-only. Other scripts need separate safe adapters rather than editing arbitrary Lua and pretending changes are hot.

Staged GitHub branches: m4i_hud feat/confige-live-settings-v09 commit 65cbd27 and m4i_garage feat/confige-live-settings-v09 commit 73744c2. Source/manifests have been installed in the Roleplay VPS and the old source backed up at /root/m4i-confige-v09-backup-20261022. Confige local CI passed 18/18; both adapter mock tests and browser UI smoke passed.

The server still had one connected player at the last check, so the updated scripts have not yet been reloaded. Source on disk is not the same as code already running in FXServer. The initial resource reload and first in-game Save & Apply test are outstanding before calling this release active/stable.

## 2026-10-22 Confige V0.9 activated after permission repair

This **supersedes the earlier pending-reload note**. A zero-player supervised restart was attempted, but FXServer initially refused to load Confige because the git checkout had created new resource files with mode 0600 under root ownership (the FiveM service account could not read fxmanifest.lua). This was diagnosed by checking file modes and reading as the actual FXServer account m4i_core_test. Only tracked Confige source files were made readable (mode 0644); runtime data and backups remained privately owned by m4i_core_test, mode 0750. The server was restarted again, with zero players, and the health endpoint confirmed **40 resources loaded, including Confige, HUD, Garage, Bridge and Registry**. Confige's health progressed from RETRY during Registry startup to **PASS**, with no Confige script startup errors observed.

Running FXServer now uses Confige **0.9.0-alpha** main ad9a71e, HUD **1.3.11-alpha** (source branch feat/confige-live-settings-v09, commit 65cbd27) and Garage **0.1.4-alpha** (GitHub main 73744c2). The HUD and Garage adapters have been installed and loaded, making their 6 and 4 supported settings eligible for later Save & Apply without resource restart. Confige local CI 18/18 and Chromium page interactions passed; Lua adapter mocks passed. **Actual owner in-game Save & Apply is still to be tested**, so the version retains alpha status. Remaining config properties across other M4I scripts are read-only references until those scripts adopt validated adapters.

## 2026-10-23 V0.10 live Rental / LedgeGrab settings

The Roleplay VPS now runs M4I Confige 0.10.0-alpha GitHub main commit cec37b0, extending the typed settings UI to four resources in addition to the existing Inventory command and Multicharacter specialized editors.

**m4i_rental:** InteractionDistance (1-6m), DrawDistance (6-50m), DoorsInteractionDistance (0.8-6m), and ExteriorLightingEnabled boolean. Runtime data is applied to live Config.Interaction, Config.Doors and Config.ExteriorLighting in client and server shared Lua through server-authoritative GlobalState.

**m4i_ledgegrab:** Enabled, RequireForwardIntent, AutoGrabWhileFalling, GrabInputGraceMs (150-2000ms) and NativeCooldownMs (300-5000ms). Clients consume GlobalState; Enabled also calls the resource's existing SetEnabled export to alter the actual runtimeEnabled local switch, not just the Lua Config table. Disabling blocks new grabs and does not forcibly cancel an existing player climbing animation.

The server-only settings store validates all names, values, bounds, optimistic revisions and required backup snapshots before committing and publishing. Existing HUD/Garage settings remain supported. Unsupported script command/config keys stay read-only. The UI code was also corrected: the first V0.10 attempt still had a HUD-only screen allowlist, so Rental/Garage/LedgeGrab fields were hidden despite the backend adapters. A browser regression test caught this; the UI now displays all four resource editors and supports clicking the script row/title as well as the Commands & settings button. The source-derived reference directory is explicitly separated from editable settings and no longer falsely reports 'No editable adapters' for these integrated resources.

Sources: m4i_confige main cec37b0; m4i_rental feature branch feat/confige-live-settings-v010 commit 266fbcc; m4i_ledgegrab feature branch feat/confige-live-settings-v010 commit b4b1542. The two resource repos' main branches were deliberately left unchanged because the freshest VPS code lives in independent sync branches and should not be overwritten by older main snapshots. Only each live resource's fxmanifest and a separate runtime adapter file were added on VPS; original gameplay files were not overwritten.

A zero-player protected snapshot before cutover was stored at /root/m4i-live-settings-v010-backup-20261023. Confige local CI 18/18, Rental and LedgeGrab client mock tests, and Chromium NUI interaction smoke (HUD, Rental, LedgeGrab, revisions and previews) passed. On the first restart all 40 resources began, and a browser regression revealed the hidden-form bug. A second controlled zero-player restart loaded the corrected Confige and verified 40 resources (all nine critical resources present), Confige Health PASS after Registry startup, and no fatal Confige/Rental/LedgeGrab errors in recent startup logs.

**Still alpha:** the owner should test actual in-game Save & Apply for a safe non-economic setting and verify client propagation. Beyond these exact allowlisted fields, other scripts and config properties need explicit live adapters. Historical FiveM keybinds may persist in player local preferences.

## 2026-10-23 V0.11 — live Mechanic and canonical WeatherSync configuration

Roleplay VPS now runs M4I Confige **0.11.0-alpha**, GitHub main **1621dbc**, with two more validated integrated resource editors:

- **m4i_mechanic:** TargetDistance (2–16 m), InvoicePairDistance (2–16 m), ControlTimeoutMs (500–8000 integer milliseconds), StatePollMs (750–10000 integer milliseconds). The new shared adapter updates M4IMechanicConfig on server and clients using server-owned GlobalState. Job authorization, finance access, allowed services, invoices and disallowed vehicle classes remain protected and read-only.
- **m4i_weathersync:** AutoWeather, ChangeEveryMinutes (0.25–720) and TransitionSeconds (0–300). Unlike other live resource adapters, WeatherSync's pre-existing state.json is the *single source of truth*: Confige queries a server-only GetConfigeSettings export and saves via a server-only ApplyConfigeSettings export protected by GetInvokingResource() == m4i_confige. Confige verifies the supplied revision, validates all fields, requires an audited backup, then delegates persistence to WeatherSync. WeatherSync verifies state.json readback and broadcasts its canonical weather state. Settings changed through the original WeatherSync administrative UI also increment the same revision, so stale Confige saves are rejected. No second copy of weather data is kept in Confige script_settings.json.

Total general typed live adapters: **six resources** — HUD, Garage, Rental, LedgeGrab, Mechanic and WeatherSync. Inventory has a separate validated live command editor; Multicharacter retains its specialized settings editor. Other discovered config.lua entries and commands remain read-only until their exact resource adapters are implemented. Changing unsupported Lua config values without restart is not promised.

Deployment details: initial missing Mechanic shared directory halted file installation before any restart; the directory was created and source/file permissions tested using the real FXServer user m4i_core_test. Source/manifests were verified and installed atomically. A protected rollback archive and a separate copy of WeatherSync state.json were saved in /root/m4i-live-settings-v011-backup-20261023. With zero players online, a supervised restart loaded Confige, Mechanic and WeatherSync and all other core modules, totaling 40 resources. WeatherSync logged restoration of state.json, Confige health advanced from expected RETRY (Registry starting) to **PASS**, and systemd service remained active. Confige local CI **18/18** passed, WeatherSync canonical permissions/revision/native-dashboard mock passed, Mechanic shared Lua tests passed, and Chromium Confige UI interaction mocks passed.

GitHub: Confige main 1621dbc, WeatherSync main 7cd42ca, Mechanic main 402fb5c. No production DB contents or WeatherSync state.json were committed. Actual owner-led **in-game Save & Apply** and player-client propagation have not yet been acceptance-tested; do not tag this alpha as Stable until they are verified.

## 2026-10-23 — Confige 0.12.1 active: Target, Radial and Finance discovery

Current M4I Confige GitHub main is b788112 (0.12.1-alpha). Its general typed live adapter coverage is now eight resources: HUD, Garage, Rental, LedgeGrab, Mechanic, WeatherSync, Target and Radial. Inventory command controls and Multicharacter have independent specialized editors.

M4I Target (main 781b356) adds a client-side runtime adapter for RaycastDistance, DefaultInteractionDistance, MaxOptions and CloseOnSelect; its source values are validated and distributed by server-owned GlobalState. M4I Radial (main 2b9c2a6) adds a runtime adapter for MaxRootItems, MaxSubmenuItems and MaxDepth. Both update the in-memory configuration tables that the original clients use. The adapters DO NOT change registered commands or locally stored player keybindings; these need separate resource contracts.

Confige validates bounded typed fields, optimistic revisions, owner permissions and mandatory pre-mutation snapshots before publishing updates. Unsupported script controls/config fields are shown as reference-only. Finance uses the M4IFinanceConfig namespace, so patch 0.12.1 shows 34 curated Finance setting names as read-only reference metadata. No financial values, player account details, fee schedules, tax rates or transaction behavior were modified. Finance must get a native audited server-authoritative transactional adapter before write access can be enabled.

Safe deploy: checked backups at /root/m4i-live-settings-v012-backup-20261023 and /root/m4i-confige-v0121-backup-20261023. Target/Radial source previously had local uncommitted VPS modifications; they were preserved, with only each manifest and a new client adapter file installed. GitHub branches were fast-forwarded to main from isolated checkout, not by resetting VPS files. Supervised restarts were gated on 0 players. The latest service check showed Active, 40 resources loaded, Confige Health PASS after Registry initialization, and local CI 18/18. Client Lua mocks and Chromium UI Save/Cancel/revision tests passed, but a real in-game owner Save & Apply and player propagation test is still required before calling the release stable.

The VPS root partition remains about 97% full (approximately 2.3 GiB free). Do not store unbounded images, build caches or backups without reviewing space.

## 2026-10-24 V0.13-alpha — Finance guarded live options and M4I Chat

Confige main **9fb77ca** adds two more validated typed live resource editors, bringing the general adapter total to **10**: HUD, Garage, Rental, LedgeGrab, Mechanic, WeatherSync, Target, Radial, Finance (safe nonmonetary subset), and Chat. Inventory and Multicharacter remain specialized editors.

- **Finance**, main **1ffccbf**: BillingTargetDistance (1.5–6 m), CreatorPlacementDistance (5–30 m), CreatorMaxLocations (20–500 integer). These settings are actually consumed by Finance's live billing distance checks and authorized location creator on the server. An in-place shared adapter updates the existing M4IFinanceConfig tables after server-side Confige schema validation, optimistic revision checks, verified pre-mutation snapshot and audit. Financial values (balances, taxBps, fee schedules, payout, transaction limits), account permissions and ledger data remain read-only and unchanged. The private GitHub Finance main now includes source from the active VPS, excluding runtime data, logs, keys, environment files, test output and obvious secrets.
- **Chat**, main **df90a97**: MaxMessageLength (40–500 integer), MaxMessages (20–150), ClosedVisibleMs (1000–30000), RateLimitMs (250–5000). The server keeps authority over length and rate limiting. Client-side chat presentation receives state updates and NUI chat:config messages without reopening Chat. OpenCommand and DefaultKey are deliberately NOT live-editable due to persisted FiveM player keymaps.

V0.13 local CI passed 18/18, native Finance and Chat adapters passed bounded/revision/financial-invariant Lua tests, and Chromium mocked save/cancel/revision UI tests passed. After deploying manifests and individual adapters onto the Roleplay M4I_TEST resources, the full resource restart was performed only when 0 players were online. A root-protected rollback archive and checksum are stored under /root/m4i-v013-backup-20261024. The server currently runs 40 resources and Confige Health PASS, with Finance and Chat started. Real in-game owner Save & Apply and player-client propagation remain to be accepted: this is still alpha.

**Important 2026-10-24 incident and recovery:** during the initial M4I_TEST restart, oxmysql could not be found because the oxmysql resource was a symlink into /var/www/fivem/.resource-backups/resources-before-20260828-144457/[standalone]/oxmysql, a rollback tree removed during an earlier backup cleanup. Finance, Registry, Core and Confige consequently failed. This was resolved by installing a self-contained local oxmysql 2.14.1 directory from the already present MKS installation at M4I_TEST.base/resources/[standalone]/oxmysql (NOT a symlink), preserving all DB data and config. A new zero-player restart restored 40 resources and Confige PASS; no new MySQL errors appeared in that clean boot. Momo/Nexoria remains STOPPED and its systemd autostart DISABLED as requested. Future backup cleanups MUST check symlink target references before removal, and never assume backups are unused based only on age.

## 2026-10-24 V0.14-alpha — Store live settings, Appearance camera staged

M4I Confige main d64de17 (0.14.0-alpha) adds a live m4i_store typed adapter to the ten earlier general adapters, totalling ELEVEN active typed resource editors.
- m4i_store main c0e6f56 (0.2.0-alpha.4) changes InteractionDistance (1–6m) in client/server and DrawDistance (6–45m) in the client. The authoritative Store server already reads M4IStoreConfig.Interaction.distance in its proximity check, so the change genuinely applies without restart after the initial adapter install. Prices, products, purchases and finance integrations remain unaffected.
- m4i_appearance camera adapter is in GitHub feature branch feat/confige-camera-v014 at d20b62e, with four bounded camera-only controls: CameraFov, CameraTransitionMs, CameraSmoothing and CameraZoomStep. It changes the existing V4 Config.Camera table in place, and can update the FOV of an already-active camera. However, M4I_TEST server.cfg deliberately comments out m4i_appearance and runs rcore_clothing as the canonical player appearance provider. Therefore this Appearance adapter is STAGED / OFFLINE, NOT included in the count of active resources. Do not launch Appearance alongside RCore without a separate migration and provider conflict check. GitHub main remains unchanged due diverged V4 source and live VPS modifications, including a modified tattoo service.

m4i_gameplay also remains excluded: native weapon wheel and ped-pickup flags are cached once at startup in its client scripts, so offering these as no-restart editable settings without refactoring would be misleading.

Checked root-protected rollback archive: /root/m4i-v014-backup-20261024. Only manifests and standalone adapter source files were installed into existing resource directories; no other source code was overwritten. A first attempt detected Store's missing shared/ directory before restarting; it was created with correct ownership and the staged files installed and verified. A supervised zero-player restart then succeeded. 40 resources loaded, m4i_store active, m4i_appearance deliberately offline, oxmysql healthy, Confige Health PASS, and fivem-momo still stopped. Confige CI 18/18, native Lua mocks and Chromium UI Save/Cancel simulation passed. Real Master in-game Save & Apply and client propagation still need acceptance tests.
