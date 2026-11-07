# M4I Garage — Complete Settings and Customization Reference

**Validated source:** `m4i_garage 0.1.139-alpha` on 7 November 2026. This page documents the editable top-level config values and server-validated runtime policy groups. It also explains **where each value is changed and what it affects**; it is not a request to replace the entire Lua file.

**Read with pictures:** [Garage UI Visual Walkthrough](visual-setup-guide.md). **Before installing:** [Complete Framework Install](complete-installation.md).

## 1. Choose the correct place to edit a setting

| Where | What it controls | How to apply |
| --- | --- | --- |
| **`m4i_garage/config.lua`** | Boot defaults, interactions, fees, security, cooldowns, feature switches | Backup; edit existing assignment once; carefully restart `m4i_garage` |
| **Garage Creator → Garage Editor** | Individual garage ID/name/type, category, polygon, spawns, access, NPC and blip | In-game `/garagecreator`; **Save Garage** and verify confirmed data |
| **Garage Creator → Vehicle Covers** | Cover class/model rules, allowed/denied zones, visibility/remove permissions, 3D offsets, emotes/fades | Change the server-authorized editor; save and refresh; validate GTA model streaming |
| **Garage Creator → System Settings** | Runtime garage-wide spawn/delivery policy and overview of some read-only limits | Edit allowed live fields and **Save**, not arbitrary displayed stats |
| **M4I Confige** (native M4I only) | Validated live `StoreDistance`, `TransferBaseFee`, `GpsPurchaseFee`, `DefaultImpoundFee` | Apply via authorized UI; values propagate through `m4i_garage_live_settings` GlobalState |
| **`m4i_bridge/config.lua`** | Select actual Framework, Inventory, Radial, Target, Keys, Phone, Banking etc. providers | [Bridge Provider Reference](../../core/m4i_bridge/complete-provider-setup.md); restart Bridge and consumers during maintenance |
| **Third-party vendor resources** | Actual inventory item catalog, installed radial/target/phone/keys, dealer purchase handler, mechanic repair permit | Follow exact matching vendor adapter guide; never assume Bridge modifies vendor files automatically |

A setting shown by the UI can be **read-only**. A value in the file can be **overridden at runtime** by a validated M4I Confige/GlobalState update. When troubleshooting, compare effective runtime value, `config.lua` and stored SQL settings.

## 2. Garage control and interactions

| `config.lua` key | Shipped value | Effect; when to change |
| --- | --- | --- |
| `Debug` | `false` | Additional diagnostics; use only temporarily |
| `InteractionMode` | `'radial'` | `'radial'` uses Bridge radial; `'keys'` uses keyboard E/H; choose keys if no working radial |
| `InteractionOpenKey` | `'E'` | Open key in keys mode; restart required |
| `InteractionStoreKey` | `'H'` | Store key in keys mode |
| `InteractionPrompt` | `true` | Display the on-screen action prompt where supported |
| `ZoneTickMs` | `600` | Periodic zone evaluation; smaller increases scanning load |
| `NearbyRadius` | `400.0` | Nearby entities/garage discovery radius; do not expand without performance tests |
| `StoreDistance` | `3.0` | Maximum player-to-vehicle Store range; Confige live range **1–8m** |
| `VehicleKeysDistance` | `3.0` | Proximity for owner temporary-key interactions |
| `SpawnClearance` | `3.0` | Fallback vehicle spawn obstruction distance; runtime global safety settings can override |
| `StoreFadeDurationMs` | `450` | Cosmetic fade on Store, not SQL timeout |
| `SpawnFadeDurationMs` | `450` | Cosmetic fade on Retrieve |
| `StorePassengerExitTimeoutMs` | `8000` | Wait for safe passenger exits before storing occupied car |
| `StorePassengerMaxSpeed` | `1.25` | Allow safe passenger exit only when near-stationary |
| `VehicleActionSlowLogMs` | `4000` | F8 diagnostic threshold for slow vehicle actions |
| `InteractDistance` | `3.0` | Proximity to interactive Garage control |
| `RadialMaxSpawnDistance` | `8.0` | XY distance from an actual bay where radial actions can appear |
| `RadialMaxSpawnHeight` | `2.0` | Height offset from bay tolerated for radial zone |
| `TemporaryKeyRange` | `2.0` | Range for temporary key sharing |
| `PlayerGarageRange` | `12.0` | Distance used by player-owned garage interactions |
| `NpcModel` | `'s_m_m_autoshop_02'` | GTA ped model for Garage NPC; must exist/stream correctly |

**Example, no radial installed:**

```lua
-- Edit existing values, do not append duplicates.
Config.InteractionMode = 'keys'
Config.InteractionOpenKey = 'E'
Config.InteractionStoreKey = 'H'
```

In keys mode, ordinary Open/Store no longer relies on a vendor radial; **NPC target interactions may still need a working Bridge Target**.

## 3. Native framework vehicle SQL and migration

| Key | Shipped value | Impact |
| --- | --- | --- |
| `NativeVehicleCompatibility.Enabled` | `false` | Optional projection **from Garage-owned rows to native QB/ESX/Qbox readable tables**; not an importer |
| `NativeVehicleCompatibility.SyncIntervalMs` | `0` | Startup projection + event updates; zero avoids a constant 15s full-table scan |
| `NativeVehicleCompatibility.QbPhoneCallback` | `true` | Register QB's narrow garage vehicle-list callback if native compatibility is enabled |

**Change only after** creating and validating Garage ownership, backing up both databases/tables, and auditing old garage / phone / police / keys resources. Do not let original garage gameplay and M4I Garage both spawn/store the same vehicle. ESX `owned_vehicles` and QB `player_vehicles` are not automatically imported into `m4ig_vehicles`.

## 4. Cover settings and 3D behaviour

| Key | Shipped value | Effect |
| --- | --- | --- |
| `VehicleCoverItem` | `'vehicle_cover'` | Exact inventory item name. Changing name requires end-to-end bridge/inventory changes; the shipped external charging code specifically expects `vehicle_cover` |
| `CoverUncoverDistance` | `3.5` | Near-cover E interaction distance; server additionally validates distance |
| `CoverActionCooldownSeconds` | `15` | Per-vehicle minimum time between successful Cover and Uncover / re-cover; 0 disables, max 3600 seconds |
| `VehicleCoverTintIndex` | `13` | GTA tint variation where cover prop material supports tint; not all models do |
| `CreatorAce` | `'m4i.garage.admin'` | ACE that authorizes staff Garage Creator and privileged edits |

If enabling the cover item, first add the **correct vendor item definition and Use action**, [including Ox client adapter](vehicle-cover-item.md). Do not give the item to players if they can't use it. A native cover model/stream fallback can be used where your custom YDR/YTD is absent.

**Live Cover editor** has additional group and model settings: `clearance`, `minPlayerSpawnDistance`, visibility `owner/access/everyone/jobs`, who may uncover `owner/access/jobs`, appearance `alpha`, collision, stream distance, `fadeMs`, `pollMs`, apply/remove animation, apply/remove durations, fade out, entry delay, player freeze, and collision disable on removal. These are **runtime Cover rule data**, not new standalone `Config.*` variables. Use the graphical editor and its validations, not arbitrary client event writes.

## 5. Garage Creator limits, creator camera and model classes

| Key | Shipped value | Meaning |
| --- | --- | --- |
| `MinPolygonPoints` | `3` | Minimum points required by a valid Garage zone |
| `MaxPolygonPoints` | `128` | Lua upper limit for polygon vertices; UI can expose a smaller per-policy limit |
| `MaxSpawns` | `256` | Script limit for legacy/large imported bay sets; do not confuse with UI screenshot showing a preview policy of 32 |
| `MaxGarages` | `800` | Maximum overall Garage entries |
| `MaxVehiclePropertiesBytes` | `16000` | Maximum serialized vehicle-property payload |
| `CreatorCamera.moveSpeed` | `16.0` | Free Cam base move speed |
| `CreatorCamera.fastMultiplier` | `3.0` | Sprint/fast mode multiplier |
| `CreatorCamera.mouseSensitivity` | existing table value | Free Cam mouse input; adjust carefully |
| `CreatorCamera.focusFov` | `75.0` | Free Cam FOV |
| `CreatorCamera.maxRayDistance` | `850.0` | Maximum Free Cam placement ray |
| `CreatorCamera.previewModel` | `'sultan'` | Vehicle model used for Creator preview |
| `VehicleTypes` | land automobile / water boat / air plane | Default GTA spawn categories; don't map a boat to a car type |

Use the [real Garage Editor screenshots](visual-setup-guide.md) for ID, Name, Storage Mode, Category, GPS Blip, Allowed GTA Vehicle Classes and Jobs JSON; values saved in the UI are **per-location** and not global defaults.

## 6. Vehicles, damage, full repair and persistence

| Key | Shipped value | Effect |
| --- | --- | --- |
| `DebugVehicleDamagePersistence` | `true` | Extra diagnostics for damage persistence; disable outside intentional testing if noisy |
| `RepairObservationTickMs` | `2000` (clamped 1500–5000) | How often an eligible signed vehicle may be observed for verified repairs |
| `ConditionAutoSaveTickMs` | `30000` | Periodic in-world condition observation |
| `ConditionAutoSaveNearMeters` | `12.0` | Observe eligible vehicles near owning players |
| `ConditionAutoSaveHeartbeatMs` | `120000` | Periodic condition persistence heartbeat |
| `ConditionAutoSaveDbCooldownMs` | `25000` | Limit repeated condition DB saves |
| `RepairVerificationMaxStoreWaitMs` | `22000` | Bounded wait for independent observations when Store follows repair |
| `VehicleDeformation.typeBlacklist` | `bike,boat,heli,plane,submarine,train` | Vehicle types excluded from the deformation subsystem |
| `VehicleDeformation.modelBlacklist` | empty | Exclude exact GTA models verified to have unsupported deformation |
| `VehicleDeformation.plateBlacklist` | empty | Exclude special plates for validated reasons |
| `RepairTrustedResources` | `m4i_mechanic`, `m4i_admin_next` | Trusted **server resource names** allowed to issue the full-repair permit |

**Mechanic example:** a custom mechanic must first have a real trusted **server-side completed repair** event, call the Garage permit contract and be in `Config.RepairTrustedResources`. A client-only full repair may look clean until Store, but later retrieve old deformation. See [Garage damage/repair](damage-persistence.md).

## 7. Fees, insurance, impound, police and delivery

| Key | Shipped value | What it changes |
| --- | --- | --- |
| `TransferBaseFee` | `500` | Default car transfer fee; M4I Confige live validation **0–50000** |
| `GpsPurchaseFee` | `5000` | Garage GPS purchase; M4I Confige live range **0–50000** |
| `DefaultImpoundFee` | `100` | Default owner impound pickup; Confige live range **0–50000** |
| `MinimumSeizureReleaseFee` | `100` | Lower fee bound for newly created police seizure |
| `SeizedCheckoutSeconds` | `60` | Temporary police checkout before auto-return |
| `AuthorizedSeizureJobs` | `police=0,sheriff=0,fib=0` | Exact framework job/grade permissions for seizure; do not broaden lightly |
| `InsuranceFee` | `2000` | Coverage purchase fee |
| `InsuranceDurationDays` | `30` | Coverage duration |
| `InsuranceRenewWindowDays` | `7` | Renewal first offered this many days before expiration |
| `InsuranceReminderDays` | `{7,5,3,1}` | Warning schedule |
| `InsuranceReminderPollMinutes` | `15` | How often reminder records are checked |
| `InsuranceClaimFee` | `100` | Claim service fee; separate impound pickup may still apply |
| `DeliveryEnabled` | `true` **in TEST config** | Optional AI valet. **Set false on external frameworks until code/schema/ledger integration is fixed** |
| `DeliveryFee` | `100` | Charged for accepted valet dispatch; never use as substitute for validating payments |
| `DeliveryDriverModel` | `'s_m_m_gentransport'` | NPC model for valet |
| `DeliveryMaxConcurrent` | `3` | Server-wide concurrent delivery sessions |
| `DeliverySpawnMin` | `70.0` | Lower bound for valet vehicle spawn radius |
| `DeliverySpawnMax` | `180.0` | Upper bound for valet vehicle spawn radius |
| `DeliveryArrivalDistance` | `8.0` | Arrival condition |
| `DeliveryTimeoutMs` | `180000` | Timeout before cancellation/recovery |

**Known issue:** `m4ig_valet_payments` is referenced by paid valet, but not created by the shipped `sql/install.sql` reviewed, and the recovery logic references the M4I-only `m4i_account_ledger`. See [Known Limitations](../../shared/fivem-install-known-limitations.md). Don't advertise Valet as ready on non-M4I frameworks without fixing the real code.

## 8. SQL-backed global spawn, police emote and delivery policy

Garage's `shared/garage_global_options.lua` defines **SQL-backed validated policies**. These are **not** standalone `Config.*` keys: use Garage Creator → System Settings, save through authorized backend, and verify effective values.

### Spawn group

| Property | Default | Accepted bounds / use |
| --- | --- | --- |
| `minPlayerDistance` | 3m | 3–100m; no spawn closer than this to player |
| `maxPlayerDistance` | 30m | 3–2000m, must be ≥ min |
| `unlimitedMax` | true | Whether normal maximum-distance constraint is relaxed |
| `selectionMode` | `nearest_safe` | `nearest_safe`, `farthest`, `balanced` |
| `minVehicleDistance` | 3m | 0.5–3m vehicle clearance |
| `minCoverDistance` | 3m | 0.5–3m cover clearance |
| `minPedDistance` | 2m | 0–8m pedestrian clearance |
| `maxHeightDifference` | 2.5m | 0–30m safe Z gap |
| `requireClearGround` | false | Require validated clear placement ground |
| `retryCount` | 3 | 1–15 attempts |

### Police emotes group

`registeredEmote='clipboard'`, `worldEmote='inspect'`, `checkoutEmote='clipboard'`; durations `2600`, `1800`, `1800` ms (valid 0–10000 integer); `freezeOfficer=true`. `customEmotes` supports up to 16 validated animation dictionaries/clips or scenarios; no arbitrary executable, URL or untrusted script. Edit in the authorized UI and test compatibility with the police job.

### Optional AI delivery group

Defaults: `drivingStyle='normal'` (`passive,normal,aggressive,very_aggressive`), `minRadius=70` (30–600), `maxRadius=180` (30–900, at least 20 above minimum), `arrivalDistance=8` (4–30), `timeoutSeconds=180` (60–600 integer), `retryCount=2` (0–5), `roadsideOnly=true`, `avoidHighways=false`, `avoidVisibleSpawn=true`, `sendNotifications=true`, and `maxCallsPerCharacter=1`. **These settings do not repair the paid-valet ledger issue.**

## 9. Dealership, phone, keys, image and third-party overrides

- `TrustedVehicleRegistrars={}` by default: add **only a real trusted dealership resource name**, and integrate its server purchase with `GetGarageCharacterId` + `RegisterOwnedVehicle`. This is a security permission, not a business name list.
- `Config.VehicleTypes` and Bridge `Vehicles` classification must agree with the model's actual GTA class, boat/heli/plane category and garage bay.
- The current Garage Phone list and delivery checks require an inventory item exactly **`phone`**; setting Bridge `Phone='lb_phone'` or `'qs_smartphone'` does not rename the item.
- The selected vehicle keys resource must actually support Bridge's keys contract; some use plates, QBX uses networked entity handles. See [Bridge provider guide](../../core/m4i_bridge/complete-provider-setup.md).
- Upload global image IDs are not injected into every vendor NUI automatically. The Garage's own image UI must resolve image ID, while a third-party inventory may need a PNG at its own image path.

## 10. Safely change a setting

1. Take a backup of `config.lua`, Garage SQL and current location settings.
2. Choose the right owner: **Lua file**, **Garage Creator**, or **M4I Confige**. Do not edit the same setting in all three and assume precedence.
3. Change only supported fields, preserve Lua syntax/types. For a job allowlist, use **exact resource/framework keys**, not player-visible labels.
4. Save with the appropriate server validation; for config.lua reboot its resource during a safe maintenance window when cars are not being stored/spawned.
5. Verify with `m4ig_doctor`, actual in-game screen, two clients, real permissions, payment and image/vehicle persistence.
6. On failure, restore matching config/SQL backup; do not blindly reset live vehicle/cover state.

**Related:** [Real UI screenshots](visual-setup-guide.md) · [Garage damage/repair](damage-persistence.md) · [Complete Installation](complete-installation.md) · [Vehicle Cover Item](vehicle-cover-item.md) · [Source-audited limitations](../../shared/fivem-install-known-limitations.md).