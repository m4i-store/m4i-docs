# M4I Admin Next — safe canary

The first-generation staff-only Admin application from [m4i_admin draft PR #3](https://github.com/m4i-store/m4i_admin/pull/3) was cloned to a distinct resource named **m4i_admin_next** on 2026-10-21. This is NOT yet a full feature replacement for QBCore/QS/Code admin panels.

## Commands

- /m4iadminnext opens the new staff administration canary (master identity only).
- /m4iitemnext me|id item amount tests the registry-backed inventory grant for authorized operators.
- /m4inoclipnextoff disables canary noclip.
- /m4ispectatenextoff exits the canary spectate mode.
- /m4iadmin still opens the original Admin resource.

The new resource has isolated m4i_admin_next client/server event names, a M4IAdminNextConfig namespace and permissions starting with m4i.adminnext. All related ACE scopes have been granted only to the txAdmin master through a private server file; the actual identifier is not included in the repository.

## Verified

Lua, JavaScript, static and mocked permission checks passed against the transformed canary. The standard fivem-txadmin service restart started **both** m4i_admin and m4i_admin_next, and the FiveM info endpoint listed both while the service was active.

## Still required before promoting canary to stable

Log in as the authorized master and test /m4iadminnext. Confirm roster/online updates, goto/bring, freeze/unfreeze, heal, spectate exit, noclip exit, inventory grants, kick permissions and webhook behavior only in a controlled test session. Do not test destructive actions on ordinary players. Keep the existing resource as the stable fallback; do not copy files from the canary over the existing dirty Admin directory without a separate validated merge.

This canary is built from the draft PR, with resource/event/config namespace substitutions; changes to the canonical m4i_admin source should be made and reviewed through its own PR before release.


## GitHub canary source

The transformed live-canary source was also pushed without any runtime ACE secrets to the dedicated branch [canary/m4i-admin-next-20261021](https://github.com/m4i-store/m4i_admin/tree/canary/m4i-admin-next-20261021), commit b6ae618. The canonical main branch and draft feature PR remain separate; the existing production m4i_admin code is not overwritten.
