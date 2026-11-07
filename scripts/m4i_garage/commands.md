# Commands, Key Bindings and Permissions

**Garage build:** `0.1.139-alpha`. Commands verified against `client/main.lua`, `server/admin.lua` and `server/doctor.lua`.

## Player and admin commands

| Command / key binding | Where to run | Who may use it | What it does |
| --- | --- | --- | --- |
| `/garagecreator` | In game | Authorized Garage admin only | Open in-game Creator and its locations/cover/preset/debug/settings tabs |
| `/covereditor` | In game | Authorized Garage admin only | Open Garage Creator directly at **Vehicle Covers** tab |
| `/covermapping` | In game | Authorized Garage admin only | Alias of `/covereditor` |
| `/garagerecovery` | In game | Authorized Garage admin only | Opens the supported recovery search UI; server still checks actor before action |
| `/garageadopt <CharacterID> <GarageID>` | In game | Authorized admin; only nearby valid unregistered vehicle | Adopt one test/legacy unregistered car to a Garage-owned vehicle, subject to server checks |
| `/impound` | In game | Authorized visitor standing by an actual Impound/Seized NPC | Opens nearby attendant interaction; **does not teleport or remotely open** a yard |
| `m4ig_doctor` | **FXServer console**, no slash required | Console only | Read-only provider/DB/framework readiness diagnostics |
| `+m4ig_open` / `-m4ig_open` | FiveM key mapping internals | Player in valid zone in keys mode | Bound to **E** by default; do not normally type manually |
| `+m4ig_store` / `-m4ig_store` | FiveM key mapping internals | Player at eligible signed car/bay in keys mode | Bound to **H** by default; do not normally type manually |

Only commands found in the reviewed source are listed. Do not copy commands such as `/givecar`, `/mdvall`, `/garagemenu` from an unrelated FiveM Garage product; M4I Garage does not automatically implement them.

## Grant Garage Creator safely

In `m4i_garage/config.lua`:

```lua
Config.CreatorAce = 'm4i.garage.admin'
```

In `server.cfg`, grant the exact ACE to an existing trusted admin group:

```cfg
add_ace group.admin m4i.garage.admin allow
```

Then ensure your actual user is a member of the `group.admin` principal **through your own existing authentication/role setup**. Garage's server also permits users recognized by Bridge `IsAdmin`. Do not grant `m4i.garage.admin` to `builtin.everyone`.

**Important:** an admin screenshot displaying a Delete button is not proof that any client can delete a Garage. The server verifies admin identity, existing vehicle references, revision and permitted action before mutation.

## Doctor command examples

In the FXServer host console / txAdmin live console:

```text
m4ig_doctor
```

What to look for:

- Bridge and `oxmysql` state `started`.
- Chosen framework and actual provider mapping, not accidentally two frameworks.
- Inventory and Target where configured.
- Radial `NOT REQUIRED (key mode)` only when `Config.InteractionMode='keys'`.
- No unknown missing providers when they are mandatory for the selected feature.
- Garage `ready: true`, final configured providers result.

The doctor is a **read-only preflight**; it does not migrate SQL, register cars or run real player gameplay tests.

## Changing Open/Store keys

In `m4i_garage/config.lua`:

```lua
Config.InteractionMode = 'keys'
Config.InteractionOpenKey = 'E'
Config.InteractionStoreKey = 'H'
Config.InteractionPrompt = true
```

FiveM key mappings can be user-remapped through their own key-binding settings. File changes take effect after a controlled resource restart, but an already customized player's local key mapping may differ from the default. In `'radial'` mode, confirm the actual Bridge radial provider and menu icon are registered; E/H actions are not a substitute for a broken radial.

## Admin adoption safely

```text
/garageadopt 1001 public_legion
```

The **1001** here is an illustrative *numeric Garage character ID*. On QB/ESX/Qbox, numeric Garage surrogate IDs can be much larger than the public `citizenid` displayed in game. If unsure, retrieve the numeric ID via the trusted server `GetGarageCharacterId` API; do not assume public display ID equals Garage custody owner. Adoption requires standing near a suitable previously unregistered car and a valid Garage with matching vehicle category.

This command is designed for a controlled admin staging/migration operation, **not** a free-money or mass-car-import player command.

## Developer functions are NOT chat commands

`GetGarageCharacterId`, `RegisterOwnedVehicle`, `GetVehicleByPlate`, `OpenGarage` and `NotifyVehicleRepaired` are **Lua exports**. Use them from a proper client or trusted server resource, not as slash commands. See [Client Exports](client-exports.md) and [Server Exports](server-exports.md).