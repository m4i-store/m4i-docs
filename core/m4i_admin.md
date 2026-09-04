# m4i_admin

## Purpose

`m4i_admin` is the authorized in-game NUI for managing canonical `m4i_registry` definitions live.

Current release line: `0.2.0-alpha.1`.

Open the panel with:

```text
/m4iadmin
```

Authorization is always enforced on the server. The browser/NUI is never trusted as an authorization boundary.

## Current domains

The UI can browse, search, create, edit and soft-delete:

- items
- jobs
- gangs
- generic groups
- vehicles
- weapons
- locations

Changes are applied through `m4i_registry` and become visible to live consumers without restarting `m4i_core` or the FiveM server.

## Security model

An administrator must pass one of the server authorization paths, including the configured `m4i.admin` ACE or the native M4I admin contract.

The request flow is:

```text
NUI
 |
 v
m4i_admin client
 |
 v
m4i_admin server  <- permission/rate/payload validation
 |
 v
m4i_registry      <- canonical schema/version/duplicate validation
```

The registry write allowlist permits `m4i_admin`; M4I gameplay resources receive a read-only definition surface through `m4i_bridge`.

Server requests use bounded payload size, request IDs and per-source rate limiting. Registry-change forwarding is accepted only when the invoking resource is `m4i_registry`.

## Editing and optimistic concurrency

Each saved definition carries a version. Updates, deletes and rollbacks use `expectedVersion` so two administrators cannot silently overwrite one another.

If the version changed since the UI loaded it, the mutation fails and the administrator must refresh/review the newer definition.

## Duplicate/conflict behavior

The UI previews duplicate state before Save.

For job/gang/group names, the admin server also preflights the shared canonical group namespace so conflicts are understandable in the UI. The final race-safe authority remains the registry database unique constraint.

Example: if `police` already exists as a job, creating `police` as a gang or generic group is rejected.

## Smart Import

The Smart Import tab accepts JSON or static Lua definition tables and asks `m4i_registry` to parse them as data.

Typical supported source shapes include QBCore-style shared item/job/gang/vehicle tables and canonical/generic group data.

The preview classifies entries such as:

- `new`
- `exact_duplicate`
- `same_key_different_data`
- `restore_or_update`
- `possible_duplicate`
- `namespace_conflict`
- `invalid`

For an existing update/conflict, the UI fetches the actual entry directly from the server. It does not assume that entry is currently visible in the paginated catalog list.

For a job/gang/group namespace conflict, **Open existing** navigates to the canonical definition that already owns the key instead of preparing a duplicate draft.

Pasted Lua is never executed.

## History and rollback

Each registry mutation appends version history. The History tab can inspect prior versions and roll back by creating a new current version; historical rows are not deleted.

Soft delete disables an entry while retaining the definition/history for controlled restoration.

## Images/assets

The editor currently exposes image/asset-reference fields, but binary image upload and automatic materialization into an inventory-specific asset directory are **not shipped yet**.

That follow-up must validate MIME/type/size, hash files for deduplication, prevent path traversal/arbitrary writes, and use an inventory/provider-specific materializer rather than allowing the NUI to choose filesystem paths.

## Start order

```cfg
ensure oxmysql
ensure m4i_registry
ensure m4i_core
ensure m4i_bridge
ensure m4i_admin
```

For native M4I mode, registry must start before Core. `m4i_admin` starts after the runtime/bridge services it uses.
