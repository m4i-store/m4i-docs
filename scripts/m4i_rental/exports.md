# m4i_rental — الصادرات والأحداث والأوامر

> هذه الأسماء تخص [V4 Review Build](source-status.md). صدّرات الفرع الآخر وأمر `/rentalcreator` ليست بدائل مكافئة تلقائياً.

## Server exports

### HasRentalKeys

```lua
local allowed = exports['m4i_rental']:HasRentalKeys(sourceId, plate)
```

يرجع boolean. يجب أن تطابق الشخصية الحالية مالك عقد `active` وألا يكون `expiresAt` قد انتهى. فشل الهوية يرجع false. لا يعطي ownership دائماً ولا يكتب إلى سكريبت مفاتيح خارجي.

### GetRentalRegistration

```lua
local registration = exports['m4i_rental']:GetRentalRegistration(plate)
-- nil، أو:
-- { owner = 'provider:characterId', name = 'اسم الشخصية',
--   expiresAt = unixSeconds, leaseId = id, temporary = true }
```

النتيجة nil بمجرد عدم وجود عقد نشيط صالح زمنياً، حتى قبل انتهاء مهلة الإزالة البصرية. لا ترسل بيانات المالك لجميع اللاعبين؛ طبق صلاحيات مورد الـMDT أو الإدارة الذي يستهلكها.

### IsRentalPlate

```lua
local isRental = exports['m4i_rental']:IsRentalPlate(plate)
```

يتحقق من سجل اللوحات في قاعدة البيانات، **بما فيه العقود التاريخية المنتهية**. true لا يعني وجود كراء نشيط أو مفتاح صالح. يمكن استعماله لمنع التخزين الدائم في garage. الاستدعاء يمر عبر SQL وقد ينتظر أو يفشل إذا قاعدة البيانات غير متاحة؛ لا تستعمله كل frame.

هذه الصادرات تقارن نص اللوحة كما هو. أزل المسافات المحيطة ووحد حالة الأحرف في موردك قبل الاستدعاء:

```lua
local function normalizePlate(value)
    if type(value) ~= 'string' then return nil end
    local plate = value:match('^%s*(.-)%s*$'):upper()
    if plate == '' or #plate > 8 then return nil end
    return plate
end
```

عند خطأ تكامل حساس، امنع الإجراء وسجل الخطأ؛ لا تفسر عدم توفر المورد أو SQL على أنه ملكية دائمة مباحة. لا تغير أسماء exports في نسخة منشورة دون تحديث مواردها المستهلكة.

## Client export

```lua
local allowed = exports['m4i_rental']:HasLocalRentalKeys(plate)
```

يعتمد على نسخة عقود اللاعب الموجودة محلياً. مناسب للواجهة وتكامل قيادة عادي، وليس مرجعاً موثوقاً لإعطاء مال أو ملكية أو تخزين سيارة. القرار الحساس يعاد على السيرفر.

## Server-local event

```lua
AddEventHandler('m4i_rental:registrationChanged', function(plate, registration)
    -- registration جدول عند تسجيل/تجديد العقد، أو nil عند انتهاء الصلاحية.
    -- حدّث التكامل المؤقت. لا تمنح مفتاحاً دائماً هنا.
end)
```

الحدث محلي للسيرفر باستعمال `TriggerEvent`، وليس نقطة دخول عبر `RegisterNetEvent`. هو إشعار تغيير، وليس replay كامل عند بدء كل مورد مستهلك. إذا بدأ موردك بعد التسليم، اقرأ الحالة من export؛ لا تعتمد على سماع الحدث القديم.

## الأوامر الافتراضية

| الأمر أو الزر | الجهة والاستعمال |
| --- | --- |
| `/rentaladmin` | داخل اللعبة، إنشاء وإدارة الفروع ومراجعة الأداء؛ ACE `m4i.rental.admin`. |
| `/myrentals` | عقود الشخصية الحالية. |
| `/rentalkey` أو U | قفل/فتح سيارة كراء نشيطة قريبة. |
| F6 / `m4irental_renew_yes` | مراجعة إشعار التجديد الأقرب إلى الانتهاء. |
| F7 / `m4irental_renew_no` | رفض تجديد ذلك الموعد مع إكمال الوقت الباقي. |
| E قرب الموظف | فتح واجهة الفرع. |
| E قرب الباب | فتح أو سد الضلف الأمامية معاً أو باب الخدمة مستقلاً. |
| `/mkscarrent_v3_preview [spawn|coords|clear]` | معاينة مكتب للإدارة إذا `PreviewEnabled` مفعل. |

`adminCommand` و`memberCommand` قابلان للتغيير في config؛ بقية الأسماء أعلاه مستقلة. المفاتيح المسجلة يمكن إعادة ربطها من إعدادات FiveM. لا تستعمل preview كبديل عن حفظ موضع الفرع الدائم في Creator.

المصدر: نهاية `server/rental.lua` و`server.lua` و`client/runtime.lua` و`client/vehicles.lua` داخل [لقطة المصدر](source-status.md).
