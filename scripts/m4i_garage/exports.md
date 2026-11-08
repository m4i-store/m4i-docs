# Exports — Client and Server APIs

**Current source:** `m4i_garage 0.1.140-alpha`. The original combined page for `0.1.123` has been replaced with **two separate current API references**, each grounded in the shipped Lua code.

## <u>Client-side</u> exports

**[Open Client Exports](client-exports.md)** — for scripts running on each player's FiveM client:

`GetGarages`, `GetGarage`, `GetCurrentGarage`, `IsPlayerInGarage`, `IsGarageUIOpen`, `OpenGarage`, `GetVehicleCondition`, `NotifyVehicleRepaired`.

These provide local state/UI requests and client repair observation. They **do not grant vehicle ownership** or server permission.

## <u>Server-side</u> exports

**[Open Server Exports](server-exports.md)** — for trusted resources running in FXServer:

`GetGarage`, `CanPlayerAccessGarage`, `HasVehicleAccess`, `GetVehicleByPlate`, `GetVehicleCondition`, `IsVehicleStored`, `GetVehicleEntity`, `GetGarageCharacterId`, `RegisterOwnedVehicle`, `GetVehicleStatus`, `GetGarages`, `PlayerHasVehicleKey`, `AuthorizeFullRepair`, `BeginFullRepair`.

**Sensitive functions are protected.** In particular `RegisterOwnedVehicle` requires an exact allowlisted dealership resource and repair permits require an allowlisted server resource. A client Lua call is not equivalent to a trusted server invocation.

Both reference pages include correct argument order, return values, error cases and **copyable Lua examples**.

[Installation](installation.md) · [External Integrations](integrations.md) · [Commands](commands.md).