# m4i_rental — الإعدادات

> تخص القيم [حزمة V4 الموثقة](source-status.md). لا تنسخ `Config.Rental` من فرع آخر فوقها؛ الأسماء والعقد ليست متطابقة.

## المصدر الدائم للمكاتب

`Config.Locations[1]` و`Config.Rental.seedNpc` يحددان الزرع الأول فقط. الأماكن، النشر، المواقف والكاتالوغات المحفوظة تقرأ من `m4i_rental_sites`. لا يضيف ملء عدة عناصر في `Config.Locations` عدة فروع بعد التهيئة؛ أنشئ الفروع من Creator.

## إعدادات التشغيل الافتراضية

| المفتاح | القيمة | المعنى |
| --- | --- | --- |
| `Config.AutoSpawn` | `true` | الظهور التلقائي للبنايات، وليس مفتاحاً لتجميد العقود. |
| `Config.ModelTimeoutMs` | `15000` | مهلة انتظار تحميل موديل محلي بالميلي ثانية. |
| `Config.PreviewEnabled` | `true` | إتاحة معاينة المكتب للإدارة. |
| `Config.Rental.adminAce` | `m4i.rental.admin` | صلاحية الإدارة التي يتحقق منها السيرفر. |
| `Config.Rental.adminCommand` | `rentaladmin` | أمر إدارة الفروع. |
| `Config.Rental.memberCommand` | `myrentals` | لوحة عقود الشخصية. |
| `Config.Rental.maxSites` | `100` | الحد الأعلى للفروع. |
| `Config.Rental.maxActivePerCharacter` | `3` | حد العقود النشيطة وطلبات التسليم pending للشخصية. |
| `Config.Rental.maxDurationSeconds` | `30 * 86400` | أقصى مدة في عملية شراء أو تجديد واحدة. |
| `Config.Rental.warningSeconds` | `300` | سقف المهلة قبل إشعار التجديد. |
| `Config.Rental.cleanupSeconds` | `120` | الإزالة التدريجية بعد توقف السيارة وخلوها. |
| `Config.Rental.quoteSeconds` | `60` | صلاحية عرض الأداء. |
| `Config.Rental.rpcTimeoutMs` | `30000` | مهلة استجابة Bridge RPC. |
| `Config.Rental.interactionDistance` | `2.4` | مسافة تفاعل اللاعب مع الموظف. |
| `Config.Rental.serverInteractionDistance` | `4.5` | مسافة تحقق السيرفر عند المحل. |
| `Config.Rental.spawnClearance` | `3.0` | نصف قطر فحص خلو موقف السيارة. |
| `Config.Rental.creatorRange` | `500.0` | نطاق حركة كاميرا Creator بالنسبة للشخصية. |
| `Config.Rental.requireIdempotentMoney` | `false` | تفعيل true يشترط مزود فلوس يدعم منع التكرار الدائم. |
| `Config.Rental.autoMigrate` | `true` | إنشاء جداول الكراء إن لم تكن موجودة. |
| `Config.Rental.currency` | `$` | رمز العرض؛ لا يغير نوع حسابات المزود. |

`locale = 'ar'` موجود في config، لكن الواجهة الحالية تحمل نصوصاً عربية في ملفات الويب؛ لا تعتبر تغيير الحقل نظام ترجمة مكتمل اللغات.

مدة الاختيار عدد صحيح من الدقائق أو الساعات أو الأيام. الحد الأدنى دقيقة. حساب السعر يفرض أيضاً حداً أعلى ثابتاً قدره 30 يوماً للعملية؛ رفع config وحده لا يتجاوز هذا التحقق. يمكن أن تمتد النهاية الإجمالية أكثر من 30 يوماً بتجديدات متعددة، ما لم تضف سياسة أخرى.

## الموظف

```lua
Config.Rental.clerkModel = 's_m_m_highsec_02'
Config.Rental.clerkScenario = 'WORLD_HUMAN_CLIPBOARD'
Config.Rental.clerkZOffset = 0.0
Config.Rental.seedName = 'CarRent | Los Santos'
```

لتعطيل الحركة ضع `clerkScenario = ''`. راجع ارتفاع رجلي الموظف في اللعبة قبل تغيير `clerkZOffset`؛ لا ينقص متر تلقائياً من الإحداثيات. model وscenario إعدادان عامان، بينما موضع الموظف واتجاهه يختلفان حسب الفرع.

## البيبان والضو

`Config.Doors.enabled = true` يحافظ على جوج ضلف أمامية وباب خلفي مستقل. التفاعل بـE وليس قرباً أوتوماتيكياً. زاوية الأمام `90.0` والخلف `92.0`، والسرعة `115.0` درجة/ثانية، ومسافة التفاعل `1.85`. الخلف غير مقفل على الموظفين افتراضياً؛ كل لاعب قريب يمكنه التفاعل.

`Config.ExteriorLighting.enabled = true`، ومسافة الرسم `70.0`، و`nightOnly = false`. يمكن قصر الإضاءة الإضافية على الليل بتغيير الأخير إلى true. أقسام `canopy` و`logo` و`rear` تضبط أضواء السكريبت؛ لا تعيد بناء مصابيح YDR أو خامة الشعار المضيئة. تعطيلها لا يمحو الإضاءة المدمجة في الموديل.

## حدود Creator الثابتة

ID حتى 48 محرفاً صغيراً من أحرف إنجليزية وأرقام و`_` و`-`، ويبدأ بحرف أو رقم. الاسم حتى 100 بايت. model حتى 64 محرفاً من أحرف وأرقام و`_`؛ لا يقبل تكرار الموديل داخل نفس الكاتالوغ.

الكاتالوغ 1–20 سيارة، وثمن الساعة عدد صحيح من 1 إلى 1,000,000. رابط الصورة HTTPS حتى 512 بايت. المواقف 2–10، على مسافة 4–120 متراً من مركز المكتب، وبين مركزي أي موقفين 2.5 متر على الأقل. الموظف في نطاق 12 متراً من المكتب. فحص الموقف دائرة مركزية وليس اختباراً هندسياً كاملاً لأبعاد كل مركبة.

تستعمل المركبات نوع `automobile` وrouting bucket رقم `0`. دعم أنواع أخرى أو عوالم معزولة يحتاج تعديل كود واختباراً، وليس تغيير اسم model فقط.

المصدر: `config.lua` و`shared/domain.lua` و`server/rental.lua` و`client/runtime.lua` في [لقطة المصدر](source-status.md).
