# m4i_upload — Shared Image Library

**Current release:** `m4i_upload 0.2.1-alpha` (7 November 2026). This standalone FiveM image resource is usable with native M4I, QBCore, Qbox/QBX, ESX Legacy and Ox Core. It stores image IDs and bytes independently of player framework money, jobs or inventory.

Upload an image **once**; scripts may display it by the same global ID in item thumbnails, vehicles, Phone, Garage, Rental, and any compatible NUI. Categories are for browsing/organization only. Existing local images remain a fallback when the global ID does not exist.

## Current setup

Start the `m4i_upload` resource from `resources/[m4i]/m4i_upload` and assign the `m4i.upload` ACE only to trusted admins. Use `/m4iupload` for the manager. Back up `data/index.json`, `data/assets/`, `data/backups/` and `data/audit.json` before updating the package.

Original PNG, JPEG, WebP and GIF bytes can be preserved unchanged up to **4 MiB** each; optimization is optional and creates a static WebP when selected. Catalog limits are 700 assets / 95 MiB active / 32 MiB historical backup storage. Animated sources retain their frames only when saved original; images are not private to clients.

New M4I consumers should resolve image IDs through `m4i_bridge`, not hardcode Upload's internal storage format. Neither Upload nor Bridge can automatically insert image data into an unrelated third-party NUI; that UI needs a receiving adapter.

**Start here:** [Installation on any framework](installation.md) · [Global image integrations](integration.md) · [Bridge provider selector](../../core/m4i_bridge/third-party-providers.md).