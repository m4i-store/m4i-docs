# m4i_core Production Rollout

## Principle

Native M4I now uses `m4i_core` as its standalone primary framework by default, but converting an **existing** production server is still a migration project, not a resource toggle.

Do not remove QBCore/Qbox/ESX/Ox Core from an existing production server until every dependent resource and persistent-data requirement has been audited.

## Safe rollout stages

### Stage 1 — repository release

- `m4i_core` standalone-primary release merged to `main`
- `m4i_bridge` native-M4I primary-default release merged to `main`
- feature/PR/post-merge CI passes
- code/diff review completed

This proves the code contract, not the migration of an existing production ecosystem.

### Stage 2 — isolated staging

Use a separate profile/database and **do not start another framework core** for the native standalone test.

Validate:

- `GetRuntimeInfo()` => `mode = primary`, `externalFrameworkRequired = false`
- bridge selects provider `m4i` from defaults without a framework override
- migrations
- player load/unload/reconnect
- resource restart recovery
- money operation-ID replay/conflict and persistence
- jobs/groups/duty
- metadata/status
- Data Layer snapshots/subscriptions/backpressure
- source/session reuse protection
- real client login and callbacks
- persistence after restart

### Stage 3 — production compatibility preflight

Before removing any existing framework resource:

1. inventory active framework and resources
2. identify every script with direct framework imports/exports/events
3. identify every script with direct framework-schema SQL
4. identify framework-owned persistent identifiers/foreign keys
5. classify resources as bridge-native, compatibility-ready, patch-required, replacement-required, or removable
6. back up production files/config
7. create a full database backup
8. verify rollback commands and backup readability

### Stage 4 — prepare the M4I cutover

Validated `m4i_core`/`m4i_bridge` files can be staged before the migration window, but remember that the shipped bridge default is now `m4i`.

Do not restart a production bridge with the new defaults until the cutover is intentional. If the old framework must remain active before migration, pin that compatibility provider explicitly in the production profile until the migration window.

### Stage 5 — data migration

Build and validate migrations for the actual production schema.

Typical mapping domains include:

- canonical user/character identity
- money/accounts
- jobs/groups/duty
- metadata/status
- licenses
- owned vehicles
- housing/property
- inventory/ownership references
- phone/business/other script-specific foreign keys

Never assume a framework ID and an M4I canonical ID are interchangeable.

### Stage 6 — controlled cutover

1. close player access
2. cleanly stop the server
3. take a final database backup
4. execute validated data migrations
5. remove/disable the explicit old-framework provider override so bridge uses shipped provider `m4i`
6. start `oxmysql`
7. start `m4i_core`
8. verify `GetRuntimeInfo()`, `IsReady()` and migration state
9. start `m4i_bridge`
10. verify provider `m4i` and native capabilities
11. start M4I/compatible gameplay resources
12. keep incompatible old-framework resources disabled
13. run smoke/reconnect/restart tests with administrators/testers
14. reopen only after validation passes

### Stage 7 — removal of old framework resources

Only after the native M4I cutover is proven should obsolete QBCore/Qbox/ESX/Ox Core resources be deleted from production.

Keeping a rollback copy outside the active resource tree for the first release window is safer than deleting it immediately.

### Stage 8 — rollback gate

Rollback immediately if critical invariants fail, including:

- wrong character identity
- money mismatch
- missing ownership
- job/permission mismatch
- repeated database errors
- duplicate sessions
- core/bridge provider instability

Rollback means restoring the previous provider/config and data backup according to the migration plan. Do not improvise live repairs against player data.

## Third-party resource policy

M4I-owned scripts should use `m4i_bridge`.

Framework-native third-party scripts require one of:

- approved reverse-compatibility shim targeting native M4I
- source patch to bridge APIs
- replacement with an M4I-native resource
- temporary retention only during a controlled compatibility/migration phase

A script with hard-coded framework SQL cannot be declared compatible merely because its public exports look similar.

## Current recommendation

The code architecture is now ready for the **standalone isolated runtime gate**: `oxmysql + m4i_core + m4i_bridge`, with no QBCore/Qbox/ESX/Ox Core running.

For an existing production server, complete that gate plus the production resource/data audit before deleting the old core.
