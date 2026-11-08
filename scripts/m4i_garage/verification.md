# Verification Checklist — Ready for Your Server?


> **New optional native deletion check for 0.1.140-alpha:** Test `DeleteOnNativeRowMissing=false` (preserves Garage car), and `true` only on a disposable linked stored car after backup. Confirm no deletion before 180 seconds, protected `out`/covered/seized/impounded cars stay untouched, and archive+audit exist after an eligible delete. [Detailed QA behavior](sql-ownership-and-deletion.md).


**Product:** M4I Garage `0.1.140-alpha`. A healthy `m4ig_doctor` result is **necessary but not sufficient**. Real in-game behavior and DB state still have to pass the acceptance plan.

## Installation baseline

- [ ] A single correct framework runs: `m4i`, `qbcore`, `qbox`, `esx` or a separately QA-validated `ox_core`.
- [ ] `oxmysql`, `m4i_bridge`, `m4i_garage` started without error and use the **same intended database**.
- [ ] Imported `m4i_garage/sql/install.sql` without modifying/dropping original framework vehicle tables.
- [ ] Any optional runtime-created Garage schemas and migration privileges reviewed.
- [ ] Existing `server.cfg` has no conflicting `m4i_bridge_profile` overrides or duplicated `ensure` entries.
- [ ] `m4ig_doctor` runs from console and identifies the correct framework plus real inventory/target/radial adapters.
- [ ] Admin ACE `m4i.garage.admin` assigned to a trusted principal only.
- [ ] An authorized admin can open `/garagecreator`, edit/save a location and see it after refresh.

## One active Garage and one real vehicle

- [ ] New Garage has unique ID, category, 3D PolyZone with safe height and valid spawn bay/heading.
- [ ] Vehicle is **registered in Garage custody** using trusted server identity and ownership, not merely present in native QB/ESX tables.
- [ ] User can open in Radial or E/H keys mode near the actual zone and parking bay.
- [ ] Owner sees the correct vehicle; another user without access does not.
- [ ] Car retrieves into a collision-free bay and the correct network owner can control it.
- [ ] Car stores safely with any passengers able to leave; no occupied vehicle is deleted.
- [ ] Log out/reconnect and check the stored status and same plate/model/location.
- [ ] Restart test instance in a planned window; no duplication or phantom cars.

## Vehicle physics and full repair

- [ ] Fuel, engine, body, tank health, windows, doors and relevant mesh deformation persist after Store/Retrieve.
- [ ] Full repair through a verified permit removes damage after Store/Retrieve.
- [ ] Partial repair doesn't reset all older damage.
- [ ] Repair doesn't refill fuel unintentionally.
- [ ] Another player's untrusted client event can't clear damage or perform a full repair.

## Permissions, custody, money

- [ ] Job/grade restricted Garage denies unauthorized players.
- [ ] Shared/temporary keys match the expected Garage permissions.
- [ ] Police seized facility protects legal holds from ordinary retrieval/claims.
- [ ] Impound/Insurance/GPS/Transfer fee comes from the actual **personal** bank provider.
- [ ] Failure for insufficient money changes neither vehicle state nor balance.
- [ ] Simultaneous requests from two clients don't charge twice or duplicate a car.

## Optional features (test only if enabled)

- [ ] Cover item exists in actual inventory and usable callback functions.
- [ ] Cover use fails safely for wrong owner, no item, forbidden zone, moving car or cooldown.
- [ ] Intended five-use accounting is confirmed by real inventory receipts.
- [ ] Cover prop streams/alignment works in game; solid collision removal doesn't launch vehicle.
- [ ] Insurance renewal window, reminders and claim safety floor work.
- [ ] GPS is purchased once and persisted.
- [ ] Garage phone app is actually compatible; inventory contains exact `phone` item.
- [ ] Paid AI Valet remains **disabled until real schema/ledger compatibility and restart/refund QA**.

## Cross-framework checks

| Framework | Specific check |
| --- | --- |
| M4I | Native registry + M4I Inventory/Target/Radial/Bridge initialization correct |
| QBCore | Buyer Garage ID mapped from QB identity; QB Inventory/Target/Keys/funds and player_vehicles migration plan |
| Qbox/QBX | Bridge `Framework='qbox'`; Ox Inventory use adapter, Ox Target, QBX Radial and entity-based keys |
| ESX | Actual ESX item schema and bank provider, inventory choice, old owned_vehicles rows safely preserved |
| Ox Core | **Full independent live QA required** for identity, money, jobs, keys, vehicle registration, phone and restart |

## Go-live evidence

Record the date, Garage/Bridge versions, framework, vendor names and versions, two test player IDs (not secret tokens), SQL backup path, screenshots of Garage Creator/player list and the observed pass/fail results. For a failed feature, label it **unsupported/unverified with this vendor release** instead of promising universal compatibility.

**Start here:** [Installation](installation.md) · [Troubleshooting](troubleshooting.md) · [Known Limitations](../../shared/fivem-install-known-limitations.md).