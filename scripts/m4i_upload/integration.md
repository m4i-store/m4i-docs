# M4I Upload — Global Images in Inventory, Garage, Phone and Any NUI

**Version:** `m4i_upload 0.2.1-alpha` · Use the **M4I Bridge** image service for new integrations. It gives every script a shared ID namespace without requiring the image to be stored once per inventory/vehicle/phone category.

## Architecture

```text
M4I Inventory / Garage / Phone / Rental / custom NUI
           ↓ Bridge image API
        m4i_bridge
           ↓ checked image provider
        m4i_upload
           ↓
   data/index.json + data/assets/
```

The image categories are browsing metadata only. Any consumer can refer to the same ID, e.g. `vehicle_sultan`, without duplicating the original. Fallback to local assets when the global image has no matching key, Bridge/Upload is offline, or UI cannot decode the URI.

## Server-side: checked global image read

```lua
local image, reason = exports.m4i_bridge:GetImage('vehicle_sultan')
if not image then
    print('Image is unavailable: '..tostring(reason))
end
local info = exports.m4i_bridge:GetImageMetadata('vehicle_sultan')
```

A server script **may** call the legacy Upload API `exports.m4i_upload:GetImageDataUri(id)`, but new M4I consumer scripts should use Bridge so that compatibility and security boundaries remain stable.

## Client-side: asynchronous UI

Bridge's client image exports are implemented separately from the server. Resolve an image from the UI/client path, then update the NUI **asynchronously**. Avoid synchronous UI rendering depending on image transfers. The legacy Upload fallback uses the following documented callback:

```lua
exports.m4i_upload:GetImageDataUri('vehicle_sultan', function(uri)
    if uri then
        SendNUIMessage({
            type='m4i:image',
            key='vehicle_sultan',
            src=uri
        })
    end
end)
```

The receiver's JavaScript must implement its **own** handler for `m4i:image`. Merely calling `SendNUIMessage` does not automatically add an image to an unrelated third-party page.

## Common consumer scenarios

| Script | Global key usage | Keep existing behaviour |
| --- | --- | --- |
| Inventory | item ID such as `phone` or a configured alias | existing `phone.png` if key is missing |
| Garage | vehicle model or image key | existing vehicle thumbnail if key is missing |
| Phone | app artwork, car/boat/aircraft icons | phone-specific registration and its own UI lifecycle |
| Rental / dealer | vehicle or branch artwork | original local thumbnail and permission logic |
| Any external NUI | a configured image ID | own CSP, async image loader, cache and fallback |

Use a **single** global ID per logical asset. Large catalogs benefit from caching metadata separately and fetching original bytes on demand rather than eager-reading every multi-megabyte image.

## Privacy and permissions

Only trusted admins may upload/replace/delete using ACE `m4i.upload`. Readable images are intended to be public to connected clients. Do **not** store secrets, personal documents, or customer ID photos in the image library. Image categories do **not** implement access control.

## Verification

Upload an image using `/m4iupload`, use its exact ID in two independent scripts, restart the consumer, restart Upload, disconnect/reconnect, remove image and verify local fallback, and check that the first image does not visibly flash into place after a long layout shift. Also test GIF preserved as original and 4 MiB limits.

See [Installation](installation.md), [Bridge integrations](../../core/m4i_bridge/third-party-providers.md), and [QA checklist](../../shared/fivem-qa-checklist.md).