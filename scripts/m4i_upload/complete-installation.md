# M4I Upload — Complete Install and Wiring Images into Any Script

**Release:** `m4i_upload 0.2.1-alpha`, with `m4i_bridge 1.5.19-rc.1`, reviewed 7 November 2026.

## 1. Mandatory files and prerequisites

Upload is independent of player frameworks and may run with **M4I, QBCore, Qbox, ESX, or Ox Core**. It requires a FiveM NUI-capable server and persistent writable resource storage. It does **not** require an inventory, phone, SQL schema, radial or target. However, **new M4I consumer scripts should use M4I Bridge's image APIs**, so install `m4i_bridge` (and its own `oxmysql` dependency) if those integrations are needed.

Extract the inner folder with these files intact:

```text
resources/[m4i]/m4i_upload/
  fxmanifest.lua
  server/main.lua
  client/main.lua
  web/index.html
  web/app.js
  web/style.css
  web/image_processor.js
  web/gallery_cache.js
  web/vendor/...
  data/index.json       # persistent after first creation
  data/assets/          # uploaded image bytes
  data/backups/
  data/audit.json
```

The four `data/` entries are persistent user data; **never overwrite them during upgrades**. If a fresh resource has no existing `data/` data, allow initialization with writable storage as designed. The FXServer OS user needs write access to this resource's `data/`; a container/host with read-only resources cannot save images.

In `server.cfg`, start Bridge **before** Upload when using the recommended integration:

```cfg
# framework, oxmysql and selected Bridge providers have already started
ensure m4i_bridge
ensure m4i_upload
ensure m4i_garage   # optional consumer
```

Upload itself does not create or migrate QB/ESX/Ox player or item tables.

## 2. Permission setup

Only trusted administrators may mutate image data. Grant the exact ACE:

```cfg
add_ace group.admin m4i.upload allow
```

Ensure your real trusted admin principal is already assigned to `group.admin`; do not grant Upload permissions to `builtin.everyone`, ordinary users or a public client event. The admin opens the manager via **`/m4iupload`**, or a properly integrated M4I Confige UI.

**Images are public to connected clients.** Store no API secrets, passwords, identity cards, private player photos or restricted records. Categories only organise search and filtering; they are **not** access-control boundaries.

## 3. Image formats, global keys and storage limits

Use **Save original** to retain PNG, JPG/JPEG, WebP and GIF bytes, including animation, up to **4 MiB** per image. **Optimize image** is optional and converts to a static WebP preview; animated content loses motion if converted. Decode-only additional formats depend on the NUI and require explicit optimization.

Limits in the shipped source: **700 active images / 95 MiB active bytes / 32 MiB backup bytes**. Uploaded assets use a global ID such as `vehicle_sultan` or `phone`. **Upload once**; Inventory, Phone, Garage, Rental and any other UI can reference that same ID. Do not create duplicate physical images for arbitrary categories.

Global ID is **not a filesystem path or automatic image tag in unrelated NUI**. Consumers must actually read and render it.

## 4. Changes required in an existing Inventory, Garage, Phone or other NUI

### A. If the consumer already ships M4I Bridge image integration

Use the script's built-in image ID configuration, e.g. an existing item/vehicle image field. Set it to the correct Upload ID and verify that Bridge and Upload are started and the client's UI resolves it. The current M4I Inventory and Garage have specific global image logic; check their own version before editing their UI.

### B. If the consumer does NOT support global images yet

Add an adapter to that **consumer script**, not to Upload's storage implementation. A small client-side Lua example inside **your consumer**:

```lua
-- client.lua of YOUR NUI resource; add dependency 'm4i_bridge'
RegisterNetEvent('my_consumer:loadPicture', function(imageId)
    -- GetImage is ASYNCHRONOUS on the client; callback receives data URI or nil.
    exports.m4i_bridge:GetImage(imageId, function(uri)
        SendNUIMessage({
            type = 'm4i:image',
            key = imageId,
            src = uri
        })
    end)
end)
```

In the consumer's `fxmanifest.lua`, ensure `m4i_bridge` is declared as a dependency **only if this consumer uses Bridge**, and its original NUI files remain included. Do not blindly add or remove `ui_page` paths.

Then in the **consumer's own JavaScript**, listen to the incoming message and set the image source. Preserve the existing local image as fallback:

```js
const imageFallback = new Map();
window.addEventListener('message', (event) => {
  const packet = event.data;
  if (!packet || packet.type !== 'm4i:image' || typeof packet.key !== 'string') return;
  const img = document.querySelector('img[data-image-id="' +
    CSS.escape(packet.key) + '"]');
  if (!img) return;
  if (!imageFallback.has(img)) {
    imageFallback.set(img, img.getAttribute('src') || '');
  }
  const src = typeof packet.src === 'string' && packet.src.startsWith('data:image/')
    ? packet.src : imageFallback.get(img);
  img.src = src;
});
```

Your NUI must actually create an `img` with `data-image-id="your_global_id"` and trigger the Lua request at the right lifecycle point. This is an **adapter pattern**, not a drop-in automatic modification of an arbitrary vendor interface. If the NUI uses React/Vue/Svelte, integrate the async result into the component state and preserve its existing virtual DOM lifecycle rather than directly mutating `img.src`.

For server scripts, Bridge `GetImage(id)` returns a cached image data URI if available; **client** `GetImage(id, callback)` is asynchronous and must not be called as a synchronous function. Use `GetImages(callback)` / `GetImageMetadata(id, callback)` client-side where appropriate. Read the exported signatures in `m4i_bridge/exports/images_client.lua` and `images_server.lua` shipped with the version you install.

### C. Prevent slow/thrashing images

Cache the data URI keyed by global ID/revision. Fetch only when an image enters the visible UI/viewport; do not request every large original image in a list every frame. The Bridge client already deduplicates concurrent lookups and bounds parallel reads; the consumer should still avoid unnecessary DOM rebuilds. Subscribe to Bridge `m4i_bridge:client:imageUpdated`, `imageDeleted` or `imageLibraryChanged` events if you need immediate refresh; clear only the changed image cache, not the entire UI.

### D. Preserve local assets and cross-script compatibility

Existing `images/phone.png`, vehicle previews, icons and item thumbnails must continue to work when Upload/Bridge is unavailable. Do not overwrite those originals or inject an external URL where an image data URI is expected. Some third-party inventory UIs specifically require a **local `vehicle_cover.png`** even when Upload stores a global `vehicle_cover` image; those UIs need an actual adapter (or their expected local asset).

## 5. What is NOT automatic

| Customer request | Required manual change |
| --- | --- |
| Make QB inventory item show global uploaded picture | Integrate Bridge image lookup into that inventory NUI or provide its expected local file |
| Show custom photo in LB/QS phone | Integrate the phone app/page with an image ID; Phone custom-app registration remains separate |
| Show new addon vehicle image in Garage | Set proper global ID/model mapping and verify Garage UI actually requests that ID |
| Use the same picture in Rental or other M4I script | Add a Bridge image consumer adapter to that script's client + NUI if not shipped already |
| Add images from another third-party server script | Use the correct authenticated Bridge server/API and define how its NUI will receive the result |
| Use images as secret/private files | **Not supported**; uploaded bytes are intentionally readable by game clients |

## 6. Upgrades, backups, troubleshooting and QA

Back up the whole Upload `data/` including global IDs and audit. Preserve original images on disk, replace only installed **code/Web resources**, and verify that legacy keys still resolve. Verify FXServer resource start and folder write permissions. In game run `/m4iupload` with an authorized account; upload PNG, original GIF and a sample vehicle image; fetch the same ID from two independent NUI consumers.

If the image is blank: confirm exact ID and available metadata, asynchronous response, expected consumer DOM element, CSP/data URI allowance, NUI callback, local fallback and browser console errors. If image data appears very late: cache/visibility and large byte transfers are the likely diagnostic areas; do not blindly add a fixed timeout that hides the delay.

**Related:** [Basic Upload installation](installation.md), [Image Integration](integration.md), [Garage Complete Installation](../m4i_garage/complete-installation.md), [Provider Setup](../../core/m4i_bridge/complete-provider-setup.md), [Customer QA](../../shared/fivem-qa-checklist.md).