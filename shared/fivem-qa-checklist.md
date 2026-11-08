# M4I FiveM — Customer Installation, Compatibility & Acceptance Checklist

> **CURRENT INSTALLATION — READ FIRST:** [Complete Upload installation — consumer UI code and permissions](complete-installation.md). This page is a companion guide; the full guide includes SQL, items, third-party script edits, provider compatibility and go-live steps. Also review [Source-audited limitations](./fivem-install-known-limitations.md).


**Applies to:** Bridge `1.5.19-rc.1`, Garage `0.1.139-alpha`, Upload `0.2.1-alpha` (7 November 2026). For customer QBCore/Qbox/ESX/Ox Core forks, source-level tests are not proof of end-to-end compatibility.

## Preflight

- [ ] Full SQL and resource backups exist and are restorable; no live player vehicles are active during an update.
- [ ] `fxmanifest.lua` is at the top of each **inner** resource folder; no nested `[escrow]` or `[open-source]` wrapper.
- [ ] Only the actual framework `m4i`, `qbcore`, `qbox`, `esx`, or `ox_core` is selected in `m4i_bridge/config.lua`; no conflicting `setr m4i_bridge_profile`.
- [ ] Every selected Inventory, UI, Notify, Progress, Radial, Target, Phone, Keys and Banking integration has a matching Bridge adapter with actual resource dependencies ready.
- [ ] `oxmysql`, the framework, installed third-party providers, Bridge and Garage start in the correct order; logs have no errors.
- [ ] The SQL schema was reviewed and applied to the **correct database**; no destructive migration or duplicate native garage controller.
- [ ] Permission ACE `m4i.upload` is restricted to trusted admins; Upload `data/` is backed up.

## Functional smoke tests

- [ ] Two clients log in, select/reselect characters, reconnect and retain the correct Garage identity (ESX identifier / QB citizen ID must never be used as Garage numeric ID).
- [ ] Test Garage open/store/take in a valid 3D zone and rejection **outside** it; blocked spawn under 3 m must fail safely.
- [ ] If radial mode is selected: item appears, is clickable and disappears after leaving zone; icon works with the real vendor UI. If keys: E opens/H stores. Police/impound NPC actions need Target.
- [ ] Test target entity add/remove, resource restart, client reconnection, and provider outage without ghost menus.
- [ ] Test actual personal bank payment, insufficient funds and refund **once**, including insurance/impound/seizure.
- [ ] Verify dealership trust, vehicle class, persistence of plate/owner/garage; do not automatically adopt foreign SQL rows.
- [ ] Test `vehicle_cover` fresh item, metadata/slot, five uses, cooldown same car, prop collision safety, restart while covered, no premature consumption.
- [ ] Damage cycle: dent, tank leak, broken glass, repair fully/partially, store/take, observer joins later; repaired damage must not resurrect.
- [ ] Phone installed/absent: supported LB or QS custom apps register and clean up; do not promise QB Phone/NPWD embed support without a separate adapter.
- [ ] Upload one global image, use same ID in inventory and Garage, check caching/fallback and unchanged original animation.
- [ ] Test 3+ configured garage types including public, personal/shared and impound/seize (job restrictions and release).

## Debug without guessing

1. Inspect **FXServer console** and **F8 client console**. Record framework, build, vendor name/version, resource load order and first relevant error.
2. Confirm `m4i_bridge` provider ID is the one selected in `config.lua`; use `GetProvider(domain)` from the correct side, and test readiness.
3. A third-party vendor's name in a menu does not prove its API shape matches a Bridge adapter. Check real `AddOption`/`RemoveOption`, `addLocalEntity`/`removeLocalEntity` and its callback format.
4. If no radial exists, switch Garage to keys mode in staging. If a missing NPC remains, fix Target separately.
5. For missing vehicle rows, compare Garage-owned tables and native `player_vehicles` / `owned_vehicles`; avoid running two garage controllers.
6. For missing images, check Upload `data/index.json`, write permissions, image ID and client async cache, not only the web path.
7. Reproduce on staging; record before/after logs, actions and screenshots, then apply fix to the shared code and retest all frameworks.

## Release and rollback

- [ ] Match file hashes and version manifests across M4I, QBCore, ESX, QBX (only deliberate `config.lua` profile differences).
- [ ] Validate six released ZIPs: `m4i_bridge`, `m4i_garage`, `m4i_upload` each in Escrow and Open Source, with docs present.
- [ ] Rebuild/publish **real** FiveM Asset Escrow separately; naming a ZIP `[escrow]` and listing `escrow_ignore` is not encryption.
- [ ] Keep the previous distribution ZIP and SQL backup for rollback; never delete Upload `data/`.
- [ ] Do not call deployment production-verified until real server + two-client gameplay tests pass.

**Primary guides:** [Bridge selector](../core/m4i_bridge/setup-selector.md), [Third-party adapters](../core/m4i_bridge/third-party-providers.md), [Garage install](../scripts/m4i_garage/framework-installation.md), [Upload install](../scripts/m4i_upload/installation.md).
## Source-audited feature gates (do not skip)

- [ ] Read [the actual installation limitations](fivem-install-known-limitations.md) before enabling or selling optional features; currently the paid AI Valet/Delivery payment path has missing `m4ig_valet_payments` schema in the installer and direct `m4i_account_ledger` dependency.
- [ ] Confirm Garage's extra runtime-created SQL tables are present and DB schema installation privileges were handled by a trusted migration account.
- [ ] If using Garage Phone or AI Valet, confirm the player owns an item literally named `phone`; the phone resource alone is not enough.
- [ ] If using Ox Inventory Cover, ensure a **customer** companion client item-use adapter exists; `m4i_test_compat` is TEST-only.
- [ ] On external frameworks, keep paid Delivery disabled until its schema and framework-neutral ledger/refund path pass real crash/restart and two-client tests.
- [ ] Old garage/phone/house/keys APIs have been inventoried and required shims implemented before stopping vendor garage gameplay.

