# m4i_rental — التركيب

> الأوامر في هذه الصفحة تخص [V4 Review Build](source-status.md)، وليس `main` القديم أو الفرع الآخر الذي يستعمل `/rentalcreator`. ابدأ بسيرفر اختبار ونسخة احتياطية من المشروع وSQL وبيانات KVP.

## المتطلبات

FXServer مع OneSync، و`m4i_bridge` يوفر عقد v4 ومزود هوية شخصية وأرصدة وقاعدة بيانات جاهزة. قاعدة البيانات يجب أن تدعم مخطط InnoDB و`JSON_EXTRACT` المستعمل لاسترجاع عمليات الأداء. لا يحتاج هذا الـNUI إلى npm build، ولا يفرض ox_lib أو ox_target.

في بيئة M4I الأصلية يكون ترتيب التشغيل:

```cfg
ensure oxmysql
ensure m4i_registry
ensure m4i_core
ensure m4i_bridge
ensure m4i_rental

add_ace group.admin m4i.rental.admin allow
```

في بيئة مزود آخر، احتفظ بترتيب المزود الذي أعددته في Bridge؛ لا تغير framework لمجرد تركيب السكريبت. راجع [تركيب Bridge](../../core/m4i_bridge/installation.md).

## تركيب الملفات بدون تغيير الموديل

ضع فولدر الحزمة `m4i_rental` داخل `resources/[m4i]/m4i_rental`. احتفظ باسمه: تغيير الاسم يؤثر في الصادرات ومساحة KVP.

قبل التشغيل، أوقف النسخة القديمة التي توفر نفس موديلات CarRent، وعطل أي YMAP قديمة تضع المكتب في نفس الموضع. **لا تحذف الموديلات أو المابات الأخرى عشوائياً.** مصدر واحد للموديل وplacement واحد للمكتب يمنعان التكرار.

تحتاج الملفات الستة التالية داخل `stream/`:

```text
mks_carrent_v3.ydr
mks_carrent_v3.ytd
mks_carrent_v3.ytyp
mks_carrent_v3_front_door.ydr
mks_carrent_v3_rear_door.ydr
mks_carrent_v3_doors.ytyp
```

حزمة المراجعة تحتوي الملفات المحولة؛ لا تعيد تحويلها أو تستبدلها بإصدارات texture التجريبية السابقة. ملف `IMPORT_WITH_CODEWALKER_FIRST.txt` من الأساس القديم، وليس دليلاً وحده على غياب الملفات المحولة. فحص `tests/contracts.py` يقارن البصمات الأصلية.

## قاعدة البيانات

`Config.Rental.autoMigrate = true` ينفذ إنشاء الجداول عند بدء المورد. توجد أربع جداول جديدة: `m4i_rental_sites` و`m4i_rental_leases` و`m4i_rental_payments` و`m4i_rental_audit`.

إذا حساب SQL لا يملك CREATE، استورد `sql/schema.sql` بحساب مخول، ثم اضبط:

```lua
Config.Rental.autoMigrate = false
```

هذا إنشاء `IF NOT EXISTS`، وليس نظام ترقية يغير مخطط جدول قديم تلقائياً. لا تستبدل مخطط الفرع الآخر بهذا المخطط فوق بيانات حية؛ [اختلاف النسخ](source-status.md) مهم.

## أول تشغيل

```text
refresh
ensure m4i_rental
```

عند جاهزية SQL وBridge يظهر في console سجل `Rental v4 ready`. ادخل بشخصية، ثم استعمل `/rentaladmin` بصلاحية ACE. عضوية `group.admin` يجب أن تكون موجودة فعلاً؛ صلاحية txAdmin وحدها ليست بديلاً عن التحقق داخل المورد.

المكتب الأول يزرع غير منشور، بلا أثمنة أو سيارات أو مواقف افتراضية. أكمل **موقفين على الأقل وسيارة واحدة** ثم فعّل النشر. وجود البناية والموظف لا يعني أن checkout أصبح متاحاً.

## الإحداثيات الأولية

```lua
Config.Locations = {
    {
        id = 'rental_01',
        coords = vector3(122.6192, -1421.5071, 28.3415),
        heading = 243.7633,
    },
}
Config.Rental.seedNpc = {
    x = 123.5080, y = -1422.3895, z = 28.3415, h = 65.7342,
}
```

تستعمل الحزمة `Config.Locations[1]` للزرع الأول فقط عندما جدول المكاتب فارغ ولا توجد علامة الزرع في KVP. بعده تصبح SQL مصدر الأماكن؛ تغيير config لا يكتب فوق المكتب المحفوظ. عدّل المكان من Creator ولا تمسح KVP بغرض التحديث.

`Config.AutoSpawn = true` يفعل الظهور التلقائي للبنايات مع التحميل حسب القرب. `false` لا يوقف النظام المالي أو الموظفين؛ ليس مفتاح صيانة شاملاً.

## التراجع

احتفظ بإصدار المورد السابق ونسخة SQL/KVP قبل الاختبار. أوقف المبيعات وعالج العقود والمدفوعات المعلقة قبل تغيير الإصدار. إيقاف المورد يوقف إنفاذ الكراء إلى أن يعمل مجدداً، بينما الوقت الحقيقي لا يتجمد. لا تسقط جداول الكراء لإصلاح مشكلة عرض.

المصدر: `fxmanifest.lua` و`config.lua` و`server/store.lua` وتهيئة `server/rental.lua` في [لقطة المراجعة](source-status.md). مرجع المنصة: [Cfx OneSync](https://docs.fivem.net/docs/scripting-reference/onesync/).
