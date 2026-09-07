# m4i_rental — البنية والتكامل

> نطاق الصفحة هو [حزمة المراجعة المثبتة](source-status.md). كود فرع `feature/full-rental-system-v4` مختلف ولا تطبق عليه هذا العقد دون مقارنة.

## حدود المسؤولية

```text
NUI -> client/transport.lua -> m4i_bridge callback
    -> server/rental.lua -> server/bridge.lua -> m4i_bridge
                                              | framework: هوية وفلوس
                                              | database: جداول الكراء
                                              | permission / notify
```

`server/bridge.lua` نقطة تكامل الهوية والفلوس وSQL. يستعمل `GetFrameworkCapabilities` و`GetCharacterId` و`GetPlayerData` و`GetMoney` و`RemoveMoney` و`AddMoney` و`HasAcePermission` و`NotifyPlayer` وDB exports. التهيئة تستعمل `IsReady` و`RegisterCallback` و`UnregisterCallback`. العميل يستعمل `TriggerServerCallback` و`IsLoggedIn` و`GetPlayerData`.

توثق [نسخة Bridge المثبتة](https://github.com/m4i-store/m4i_bridge/blob/113ed579b70a72891186d31952659294d85dc584/docs/universal-core-contract-v4.md) عمليات الفلوس مع operationId اختياري. لا يوجد سبب للمرور مباشرة إلى m4i_core في حزمة المراجعة. لا يفترض المورد QBCore أو ESX ولا يغير provider من تلقاء نفسه.

## الهوية والفلوس

مفتاح المالك الحالي هو `provider:characterId`. هذا يميز الشخصيات ومزوديها، لكنه ليس migration تلقائية إلى معرف M4I موحد. تغيير provider أو خريطة معرفات الشخصيات يحتاج صيانة ومطابقة بيانات؛ لا تشغل المزود الجديد فوق عقود قديمة وتفترض انتقال الملكية.

`ready=true` مطلوب من capabilities. bank يجب أن يرجع رصيداً صالحاً. إذا كان cash غير مدعوم ومعلناً false، يمكن التعامل معه بصفر، وإلا غياب الرصيد يعيد `money_unavailable`. الدعم الفعلي لمنع تكرار المال يقرأ من `idempotentMoney`؛ راجع [دليل الأداء](payments.md).

## تخزين البيانات

| الجدول | المسؤولية |
| --- | --- |
| `m4i_rental_sites` | بيانات الفرع والمواضع والمواقف والكاتالوغ وrevision. |
| `m4i_rental_leases` | الشخصية والموديل واللوحة والحالة والنهاية وبيانات العقد. |
| `m4i_rental_payments` | requestId وحالة الأداء وأجزاؤه واسترجاعه. |
| `m4i_rental_audit` | حفظ أو حذف الفروع وقرارات مراجعة الأداء. |

SQL مصدر الحقيقة للعقود. KVP يحتفظ بعلامة الزرع `m4i_rental_seeded_v4` وسجل تبني العناصر `m4i_rental_entities`. لا تمسحهما لإجبار إعادة ضبط فرع موجود.

الجداول تستخدم payload JSON مع حقول مفهرسة. لا توجد في هذه الحزمة سياسة حذف تاريخ تلقائية؛ صمم retention بعد أخذ نسخة احتياطية، ولا تحذف عمليات review أو عقوداً غير مكتملة. يحمي revision حفظ الفرع والعقد من الكتابة فوق حالة تغيرت.

## العناصر والأمان

المكاتب والموظفون والأبواب نسخ محلية متسقة؛ سيارات الكراء عناصر ينشئها السيرفر بـ`CreateVehicleServerSetter` من نوع `automobile` وفي bucket 0. يتحقق النظام من model وtoken والعقد عند إعادة تبني عنصر. مجرد تشابه اللوحة أو network ID ليس دليلاً كافياً.

أسعار NUI ليست مصدر الثمن. السيرفر يتحقق من المالك والموقع والعرض والرصيد والمواقف وصلاحية الإدارة. تفاصيل تحريك السيارة وإخراج الركاب تعتمد أيضاً على عميل يمتلك التحكم الشبكي؛ العميل المعدل قد يتجاهلها، لذلك لا تعاملها كنظام anti-cheat مستقل.

التفاعل بالأبواب يدوي ومسافته تتحقق على السيرفر. لا يوجد قفل موظفين خاص بالباب الخلفي افتراضياً. تحرير المواقع بالـCreator لا يعدل موديل V3 نفسه.

## تكامل المفاتيح والـMDT والـgarage

استخدم [الصادرات](exports.md) وقت التحقق، لا تمنح مفتاحاً دائماً عند التسليم ثم تنسى إبطاله. لا يدخل المورد صفوف ملكية دائمة في `player_vehicles` أو `owned_vehicles`. الـMDT يقرأ التسجيل المؤقت، والـgarage يرفض اللوحات المعروفة ككراء ما لم ينفذ مساراً يحترم الانتهاء.

أسماء callbacks الداخلية ليست API مالية عامة للموارد الأخرى. إضافة تكامل جديد تحتاج استدعاءً موثقاً server-side واختبار صلاحيات؛ لا تستدعِ أحداث checkout ببيانات موثوقة من العميل.

## مراجع

[سياسة البيانات](../../shared/data-access-policy.md) و[قواعد التكامل](../../shared/integration-rules.md) و[Bridge exports](../../core/m4i_bridge/exports.md) تحدد حدود M4I العامة. مراجع Cfx: [OneSync](https://docs.fivem.net/docs/scripting-reference/onesync/)، [حماية الأحداث](https://docs.fivem.net/docs/developers/server-security/)، [NUI callbacks](https://docs.fivem.net/docs/scripting-manual/nui-development/nui-callbacks/).

مصدر التنفيذ: `server/bridge.lua` و`server/store.lua` و`server/rental.lua` و`client/transport.lua` و`sql/schema.sql` ضمن [لقطة المصدر](source-status.md).
