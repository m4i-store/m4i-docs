# Framework Installation Selector — M4I Garage

> **Customer-owned native row deletion setting (new in 0.1.140-alpha):** QBCore, Qbox and ESX can select `DeleteOnNativeRowMissing = false/true` under `Config.NativeVehicleCompatibility` in Garage's `config.lua`. **`Enabled=true` is required**, and only cars with verified prior native links qualify. The default is **false**. See [SQL Ownership and Admin Deletion](sql-ownership-and-deletion.md).


**Start here:** [Complete Garage Installation from Zero](installation.md).

Choose the ONE core actually installed on your FiveM server. Each framework page tells you exactly which resource to install, which `server.cfg` lines to keep/add, which Bridge provider ID to select and which Inventory/phone/keys/vehicle-table integration may require changes.

| Framework | Bridge ID | Dedicated installation |
| --- | --- | --- |
| M4I Core | `m4i` | **[Install on M4I](frameworks/m4i.md)** |
| QBCore | `qbcore` | **[Install on QBCore](frameworks/qbcore.md)** |
| Qbox / QBX | `qbox` | **[Install on Qbox](frameworks/qbox.md)** |
| ESX Legacy | `esx` | **[Install on ESX](frameworks/esx.md)** |
| Ox Core | `ox_core` | **[Install on Ox Core — live QA pending](frameworks/ox-core.md)** |

**Never install a second framework.** Bridge uses the selected framework you already run. Inventory, Target, Radial, Keys and Phone are **chosen providers**, not universally mandatory resources. The current `m4i_garage` can work in `Config.InteractionMode='keys'` without a radial.

**Critical:** owned cars in native QB/ESX tables are not automatically imported into Garage. Read [Migrating Safely](updating.md). For Cover item or dealer integration, see [Required External Edits](integrations.md).

[Installation](installation.md) · [Troubleshooting](troubleshooting.md) · [Go-Live Checklist](verification.md).