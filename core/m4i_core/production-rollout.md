# m4i_core Production Rollout

## Principle

Native M4I now uses `m4i_registry + m4i_core` as its canonical definition/runtime foundation and `m4i_bridge` defaults to provider `m4i`.

Converting an **existing** production server is still a migration project, not a resource toggle.

Do not remove QBCore/Qbox/ESX/Ox Core from an existing production server until every dependent resource and persistent-data requirement has been audited.

## Safe rollout stages

### Stage 1 — repository release

Current code-side prerequisites include:

- canonical Registry group-definition release merged to `m4i_registry/main`
- registry-backed Core 0.3 merged to `m4i_core/main`
- read-only definition surface merged to `m4i_bridge/main`
- live admin group/import hardening merged to `m4i_admin/main`
- feature/PR/post-merge CI green for each changed runtime repository
- manual diff/security review completed

This proves code contracts. It does not prove migration of an existing production ecosystem.

### Stage 2 — isolated database/profile gate

Use a dedicated profile/database clone. Do **not** start another framework core in the native standalone test.

Start:

```text
oxmysql
m4i_registry
m4i_core
m4i_bridge
m4i_admin
```

Validate at minimum:

- Registry schema v2 migration
- canonical job/gang/group shared-name constraint
- legacy `m4i_groups` definition import without overwriting Registry-owned definitions
- canonical `unemployed` seed
- Core schema v3 membership migration to `group_domain`
- `GetRuntimeInfo()` => primary mode, no external framework required, registry required
- bridge provider `m4i`
- Bridge item/job/gang/group/vehicle/weapon/location definition reads
- player load/unload/reconnect
- source/session reuse protection
- money operation-ID replay/conflict and persistence
- jobs/groups/duty
- metadata/status
- Data Layer snapshots/subscriptions/backpressure
- live Registry definition change -> affected Core player refresh without restart
- disabling/removing a currently relevant job grade/definition and expected Core repair/fail-closed behavior
- job/gang/group duplicate-name rejection, including a concurrency/race case
- `/m4iadmin` authorization and CRUD
- Smart Import standard data plus namespace conflicts
- controlled Registry/Core/Bridge restarts
- persistence and final DB invariants after full profile restart

Binary image upload/automatic inventory asset materialization is not in the current release and is not part of this gate yet.

### Stage 3 — production compatibility preflight

Before disabling/removing any existing framework resource:

1. inventory the active framework and every resource
2. find direct framework manifest dependencies/imports/exports/events
3. find direct framework-schema SQL
4. identify framework-owned persistent IDs/foreign keys
5. classify each resource: bridge-native, compatibility-ready, patch-required, replacement-required, removable
6. inventory definition sources (items/jobs/gangs/vehicles/etc.) and plan canonical Registry import
7. back up production files/config
8. create a full database backup
9. verify backup readability and rollback procedure

### Stage 4 — stage M4I files without accidental cutover

Validated releases can be staged before the migration window.

The bridge default framework provider is `m4i`. If the old production framework must remain active before the migration window, pin that compatibility provider explicitly and do not restart into the native default accidentally.

Do not start Registry/Core automatic migrations against production merely to “prepare” without the approved backup/migration window.

### Stage 5 — data/definition migration plan

Typical migration domains include:

- canonical user/character identity
- money/accounts
- jobs/gangs/groups and membership/duty
- item/job/gang/vehicle shared definitions into `m4i_registry`
- metadata/status
- licenses
- owned vehicles
- housing/property
- inventory/ownership references
- phone/business/script-specific foreign keys

Never assume a framework ID and M4I canonical ID are interchangeable.

For native M4I group definitions, Registry must become canonical **before** Core 0.3 membership migration/runtime is started.

### Stage 6 — controlled cutover

1. close player access
2. cleanly stop the production server
3. take a final database/file backup
4. execute any validated pre-migration transforms
5. configure Bridge for native provider `m4i` (remove old explicit provider override only now)
6. start `oxmysql`
7. start `m4i_registry`
8. verify Registry schema/import/defaults and collision checks
9. start `m4i_core`
10. verify Core v3 membership migration, `GetRuntimeInfo()` and `IsReady()`
11. start `m4i_bridge`
12. verify provider `m4i`, native Data Layer capabilities and definition exports
13. start `m4i_admin` and compatible gameplay resources
14. keep incompatible old-framework resources disabled
15. run admin/tester smoke + reconnect + controlled restart tests
16. compare critical data/invariants with migration expectations
17. reopen only after all gates pass

### Stage 7 — stabilization before deletion

Do not immediately delete old framework files after the first successful boot.

Prefer keeping rollback copies **outside the active resource path** or leaving old resource files stopped/disabled during an initial stability window.

Observe:

- identity/session correctness
- money/ledger invariants
- membership/job/duty correctness
- inventory/vehicle/property ownership
- DB/log errors
- Registry/Core/Bridge restart/recovery behavior

### Stage 8 — remove obsolete framework resources

Delete obsolete QBCore/Qbox/ESX/Ox Core resources only after the native M4I cutover and compatibility audit are proven stable.

### Stage 9 — rollback gate

Rollback immediately if critical invariants fail, including:

- wrong character identity
- money mismatch
- missing ownership
- job/group/permission mismatch
- Registry canonical-definition corruption/collision
- repeated database errors
- duplicate sessions
- unstable Core/Bridge provider behavior

Rollback means restoring the previous provider/config and verified data/file backup according to the migration plan. Do not improvise live repairs against active player data.

## Legacy `m4i_groups` policy

The latest Registry/Core migrations deliberately **do not drop** the historical `m4i_groups` table.

On an upgraded M4I database it can be used as one-way migration input/rollback evidence. Active Core 0.3 runtime no longer treats it as the job/gang/group definition source.

Do not manually drop it until isolated and production migration verification is complete and a separate cleanup decision is approved.

## Third-party resource policy

M4I-owned scripts should use `m4i_bridge`.

Framework-native third-party scripts require one of:

- approved reverse-compatibility shim
- source patch to Bridge APIs
- replacement with an M4I-native resource
- temporary retention during controlled compatibility/migration

A script with hard-coded framework SQL cannot be declared compatible merely because public exports look similar.

## Current recommendation

The repositories are ready for the **new registry-backed isolated real FiveM runtime gate**.

That gate must be rerun because the previous isolated runtime evidence predates Registry 0.2 / Core 0.3 / Admin 0.2 group-definition architecture.

For an existing production server, complete that isolated gate plus the production resource/data audit before deleting the old core.
