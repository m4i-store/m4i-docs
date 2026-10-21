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

- The standalone Confige source is now at commit bfa3f8e, staged on VPS and synchronized to GitHub main.
- The script inventory can hand off to the native Garage Creator and Weather Dashboard. These target systems still require their own server-side permissions, and this handoff is not a generic raw Lua file editor.
- The server now supports an explicit read-only backup inventory command (m4iconfig:backupinfo) and a console-only restore command (m4iconfig:restore slot current_revision CONFIRM). All restore attempts must compare live revision and create a pre-restore backup.
- Mocked Lua tests cover ACE denial, registry changes, tool launch validation, failed backups, replay denial, console-only restores and optimistic revision constraints.
- A SHA-256-checked, owner-root-only rollback archive was created locally on the VPS at /root/m4i-confige-precutover-20261021. This is NOT an offsite database backup.
- A read-only cutover preflight is available under tools/preflight.py. It currently reports ready=false due to missing Confige ACE, no validated in-game cutover, and failing GitHub Actions job startup.
- Production server.cfg still starts legacy m4i_admin and NOT m4i_confige. The existing Bridge/Registry writer guards are unchanged.
- Do not merge the related draft PRs individually; coordinate a maintenance-window cutover.


## Native tool integrations
M4I Confige resource inventory now exposes whitelisted entry points for m4i_garage Garage Creator and m4i_weathersync Weather Dashboard. Both destination scripts continue enforcing their own server-side administrator permissions. This integration is a management launcher, not a wholesale config-file editor.
