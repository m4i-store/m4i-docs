# m4i_core Production Rollout

## Principle

A framework cutover is a migration project, not a resource toggle.

Do not remove QBCore/Qbox/ESX/Ox Core from an existing production server until every dependency and persistent-data requirement has been audited.

## Safe rollout stages

### Stage 1 — repository release

- `m4i_core` and `m4i_bridge` release candidates merged to `main`
- exact-head CI passes
- review findings closed

This proves the code release, not the production migration.

### Stage 2 — isolated staging

Use a separate profile/database.

Validate:

- migrations
- player load/unload/reconnect
- resource restart recovery
- money operations/idempotency
- jobs/groups/duty
- metadata/status
- bridge provider resolution
- real client login and callbacks
- persistence after restart

### Stage 3 — production preflight

Before touching production:

1. inventory active framework and resources
2. identify every script with direct framework imports
3. identify every script with direct framework-schema SQL
4. classify resources as bridge-native, compatibility-ready, patch-required, or removable
5. back up production files/config
6. create a full database backup
7. verify rollback commands and backup readability

### Stage 4 — stage code without cutover

It is acceptable to place validated resource files on the server while leaving the active framework unchanged.

However, remember that a running `m4i_core` may be considered as a framework fallback if the selected framework becomes unhealthy and M4I appears in bridge priority configuration.

For the safest pre-cutover staging, keep `m4i_core` stopped until the migration window or explicitly control the framework priority list.

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
4. execute validated migrations
5. configure `m4i_bridge` framework provider to `m4i`
6. start `oxmysql`
7. start `m4i_core`
8. verify `IsReady()` and migrations
9. start `m4i_bridge`
10. verify framework capabilities
11. start M4I/compatible gameplay resources
12. run smoke tests with administrators/testers
13. reopen only after validation passes

### Stage 7 — rollback gate

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

M4I-owned scripts should be migrated to `m4i_bridge` first.

Framework-native third-party scripts require one of:

- approved reverse-compatibility shim
- source patch to bridge APIs
- replacement with an M4I-native resource
- temporary retention of the original framework dependency

A script with hard-coded framework SQL cannot be declared compatible merely because its public exports look similar.

## Current recommendation

Until the production resource audit and migration tooling are complete:

- keep the existing production framework active
- use `m4i_bridge` as the compatibility boundary for new M4I scripts
- develop and benchmark the M4I Data Layer in staging
- move production to `m4i_core` only through the controlled cutover procedure above
