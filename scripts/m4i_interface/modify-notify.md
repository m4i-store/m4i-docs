# Modify Notify

## Goal

Route notifications, TextUI, and progress bars to `m4i_interface` with safe fallback behavior.

This page gives ready-to-paste snippets for:

- ESX (`ESX_NOTIFY/Notify.lua`)
- Qbox (`ox_lib/resource/interface/client/notify.lua`)
- QBCore (`qb-core/client/functions.lua`)
- QBCore DrawText to TextUI (`qb-core/client/drawtext.lua`)
- ESX TextUI bridge (`es_extended/client/functions.lua`)
- Progressbar integration

## Common Payload Standard

Use this payload shape when sending notifications to `m4i_interface`:

```lua
{
    type = 'system', -- system | event | dm | moderation | job | video
    title = 'Server',
    message = 'Welcome',
    duration = 5000,
    icon = 'fas fa-bell'
}
```

## 1) ESX_NOTIFY - Replace `Notify` Function

File:

```text
ESX_NOTIFY/Notify.lua
```

Replace `Notify` with:

```lua
function Notify(notifyType, duration, message)
    local text = tostring(message or 'Notification')
    local mappedType = tostring(notifyType or 'info'):lower()

    if mappedType == 'warn' then mappedType = 'warning' end
    if mappedType == 'primary' then mappedType = 'inform' end
    if mappedType == 'info' then mappedType = 'inform' end

    if GetResourceState('m4i_interface') == 'started' then
        TriggerEvent('m4i_interface:notify', {
            type = 'system',
            category = 'system',
            title = 'ESX',
            message = text,
            duration = tonumber(duration) or 5000,
            metadata = {
                source = 'esx_notify',
                notifyType = mappedType
            }
        })
        return true
    end

    -- Fallback to native ESX notification when m4i_interface is unavailable
    TriggerEvent('esx:showNotification', text)
    return true
end
```

## 2) Qbox/Ox Lib - Replace `lib.notify`

File:

```text
ox_lib/resource/interface/client/notify.lua
```

Replace `lib.notify` with:

```lua
function lib.notify(data)
    data = data or {}
    local sound = settings.notification_audio and data.sound
    data.sound = nil
    data.position = data.position or settings.notification_position

    if GetResourceState('m4i_interface') == 'started' then
        TriggerEvent('m4i_interface:notify', {
            id = data.id,
            type = 'system',
            category = 'system',
            title = data.title or 'Notification',
            message = data.description or data.message or 'Notification',
            duration = tonumber(data.duration) or 5000,
            icon = data.icon,
            position = data.position,
            metadata = {
                source = 'ox_lib'
            }
        })
    else
        SendNUIMessage({
            action = 'notify',
            data = data
        })
    end

    if not sound then return end
    if sound.bank then lib.requestAudioBank(sound.bank) end

    local soundId = GetSoundId()
    PlaySoundFrontend(soundId, sound.name, sound.set, true)
    ReleaseSoundId(soundId)

    if sound.bank then ReleaseNamedScriptAudioBank(sound.bank) end
end
```

## 3) QBCore - Replace `QBCore.Functions.Notify`

File:

```text
qb-core/client/functions.lua
```

Replace `QBCore.Functions.Notify` with:

```lua
function QBCore.Functions.Notify(text, texttype, length, icon)
    local notifyType = tostring(texttype or 'primary'):lower()
    if notifyType == 'primary' then notifyType = 'inform' end
    if notifyType == 'warn' then notifyType = 'warning' end

    local messageText, messageTitle
    if type(text) == 'table' then
        messageText = text.text or text.message or 'Notification'
        messageTitle = text.caption or text.title or 'QBCore'
    else
        messageText = tostring(text or 'Notification')
        messageTitle = 'QBCore'
    end

    if GetResourceState('m4i_interface') == 'started' then
        TriggerEvent('m4i_interface:notify', {
            type = 'system',
            category = 'system',
            title = messageTitle,
            message = messageText,
            duration = tonumber(length) or 5000,
            icon = icon,
            metadata = {
                source = 'qbcore',
                notifyType = notifyType
            }
        })
        return
    end

    local fallback = {
        action = 'notify',
        type = texttype or 'primary',
        length = length or 5000,
        text = messageText
    }
    if messageTitle then fallback.caption = messageTitle end
    if icon then fallback.icon = icon end

    SendNUIMessage(fallback)
end
```

## Notification Exports and Events

## Client-side display

```lua
exports['m4i_interface']:Notify({
    type = 'system',
    title = 'Server',
    message = 'Welcome to MKS',
    duration = 5000
})
```

Or event:

```lua
TriggerEvent('m4i_interface:notify', {
    type = 'system',
    title = 'Server',
    message = 'Welcome to MKS',
    duration = 5000
})
```

## Server-side display

Preferred (bridge):

```lua
exports.m4i_bridge:NotifyPlayer(source, {
    type = 'system',
    title = 'Server',
    message = 'Your item has been used',
    duration = 5000
})
```

Broadcast:

```lua
exports.m4i_bridge:NotifyAll({
    type = 'event',
    title = 'City Event',
    description = 'Meet at Legion Square',
    duration = 8000
})
```

Direct event fallback:

```lua
TriggerClientEvent('m4i_interface:notify', source, {
    type = 'system',
    title = 'Server',
    message = 'Action completed',
    duration = 5000
})
```

## Snippet: QBCore DrawText to TextUI

File:

```text
qb-core/client/drawtext.lua
```

Replace internals with:

```lua
local function hideText()
    if GetResourceState('m4i_interface') == 'started' then
        exports['m4i_interface']:CloseTextUI()
        return
    end

    SendNUIMessage({ action = 'HIDE_TEXT' })
end

local function drawText(text, position)
    if GetResourceState('m4i_interface') == 'started' then
        exports['m4i_interface']:OpenTextUI(text, 'lightgreen', position or 'right')
        return
    end

    SendNUIMessage({
        action = 'DRAW_TEXT',
        data = { text = text, position = position or 'left' }
    })
end

local function changeText(text, position)
    if GetResourceState('m4i_interface') == 'started' then
        exports['m4i_interface']:OpenTextUI(text, 'lightgreen', position or 'right')
        return
    end

    SendNUIMessage({
        action = 'CHANGE_TEXT',
        data = { text = text, position = position or 'left' }
    })
end
```

## Snippet: ESX.TextUI to okokTextUI

File:

```text
es_extended/client/functions.lua
```

Edit `ESX.TextUI` and `ESX.HideUI`:

```lua
function ESX.TextUI(msg, color)
    local text = tostring(msg or '')
    local uiColor = color or 'lightgreen'

    if GetResourceState('m4i_interface') == 'started' then
        TriggerEvent('okokTextUI:Open', text, uiColor, 'right')
        return
    end

    -- fallback to your original ESX.TextUI implementation
end

function ESX.HideUI()
    if GetResourceState('m4i_interface') == 'started' then
        TriggerEvent('okokTextUI:Close')
        return
    end

    -- fallback to your original ESX.HideUI implementation
end
```

## Progressbar Integration

## QBCore - Replace `QBCore.Functions.Progressbar`

File:

```text
qb-core/client/functions.lua
```

Replace function with:

```lua
function QBCore.Functions.Progressbar(name, label, duration, useWhileDead, canCancel, disableControls, animation, prop, propTwo, onFinish, onCancel)
    if GetResourceState('m4i_interface') == 'started' then
        local mergedProp = nil
        if prop and propTwo then
            mergedProp = { prop, propTwo }
        elseif prop then
            mergedProp = prop
        elseif propTwo then
            mergedProp = propTwo
        end

        local success = exports['m4i_interface']:ProgressBar({
            duration = tonumber(duration) or 5000,
            label = label or name or 'Processing...',
            useWhileDead = useWhileDead == true,
            canCancel = canCancel ~= false,
            disable = {
                move = disableControls and (disableControls.move or disableControls.disableMovement) or false,
                sprint = disableControls and (disableControls.sprint or disableControls.disableSprint) or false,
                car = disableControls and (disableControls.car or disableControls.disableCarMovement) or false,
                combat = disableControls and (disableControls.combat or disableControls.disableCombat) or false,
                mouse = disableControls and (disableControls.mouse or disableControls.disableMouse) or false
            },
            anim = animation and {
                dict = animation.animDict or animation.dict,
                clip = animation.anim or animation.clip,
                flag = animation.flags or animation.flag,
                scenario = animation.task or animation.scenario
            } or nil,
            prop = mergedProp
        })

        if success then
            if onFinish then onFinish() end
        else
            if onCancel then onCancel() end
        end
        return
    end

    if GetResourceState('progressbar') ~= 'started' then
        error('progressbar needs to be started in order for QBCore.Functions.Progressbar to work')
    end

    exports['progressbar']:Progress({
        name = name:lower(),
        duration = duration,
        label = label,
        useWhileDead = useWhileDead,
        canCancel = canCancel,
        controlDisables = disableControls,
        animation = animation,
        prop = prop,
        propTwo = propTwo,
    }, function(cancelled)
        if not cancelled then
            if onFinish then onFinish() end
        else
            if onCancel then onCancel() end
        end
    end)
end
```

## Direct Progress Export

```lua
local success = exports['m4i_interface']:ProgressBar({
    duration = 5000,
    label = 'Processing...',
    canCancel = true
})
```

## Server-Side Progress (Bridge)

```lua
exports.m4i_bridge:StartProgress(source, {
    duration = 5000,
    label = 'Processing...'
})
```

## Notes

- Keep a backup before replacing framework files.
- After edits, restart resources:
  - `ensure m4i_interface`
  - `restart qb-core` or `restart ox_lib` or `restart es_extended`
- If you use QBCore only, ESX snippets are optional.
