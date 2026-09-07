# m4i_rental — حالة النسخة ومصادر التوثيق

تمت مراجعة المصادر في **2026-09-07**. هذه الصفحة تفصل بين الموديل المستقر ومرشحي كود الكراء؛ نشر الوثائق الرئيسية لا ينشر gameplay تلقائياً.

## ما النسخة التي تشرحها هذه الصفحات؟

**حزمة `m4i_rental_v4_REVIEW_BUILD.zip`، وليست `main` أو فرعاً نفترض أنه يساويها.** بصمة الأرشيف:

```text
SHA-256: da5e80b582e0228ded49da6f60fb061a8a067dac1d60aff94816720e04fc779b
```

جذر الحزمة `m4i_rental/`، ونسخة manifest `4.0.0`، وحالة التسليم `Review Build`. تقرأ أمثلة هذه الوثائق من كود الحزمة فعلياً. سجل البصمات التفصيلي في [source-snapshot.json](source-snapshot.json).

الأرشيف سلم في المحادثة الخاصة، وليس إصداراً عاماً مستضافاً في مستودع الوثائق. لا يوجد رابط تحميل عام جديد أو GitHub release ينشئه هذا التوثيق. لا تستعمل رابط sandbox من المحادثة كعنوان تنزيل عام في GitBook. للوصول إلى المصدر المنشور راجع [مستودع السكريبت](https://github.com/m4i-store/m4i_rental)، مع مطابقة النسخة قبل استعمال هذا الدليل.

## الفروع التي راجعت

| المصدر | المرجع المثبت | النطاق |
| --- | --- | --- |
| `m4i_rental/main` | [65092bbd](https://github.com/m4i-store/m4i_rental/tree/65092bbdc288c6898f00de135b3b349863c6e405) | ماب V3 وبيبان وإضاءة؛ ليس نظام الكراء V4 الكامل. |
| `feature/rental-system-v4` | [67a2c892](https://github.com/m4i-store/m4i_rental/tree/67a2c892df9f46dcb49af48615cbf5c6ce020b5d) | لا يثبت نشر الحزمة المحلية؛ README في هذا المرجع مازال عنوان المشروع فقط. |
| `feature/full-rental-system-v4` | [408b19ba](https://github.com/m4i-store/m4i_rental/tree/408b19ba7bc888f4c164544dfb37765a8a64fbff) | مرشح كود آخر مع [PR رقم 1](https://github.com/m4i-store/m4i_rental/pull/1)، وليس مصدر أمثلة هذه الحزمة. |
| الحزمة الموثقة | SHA-256 أعلاه | كود Review Build بأمر `/rentaladmin`؛ رفع gameplay المطابق غير متحقق. |

## اختلافات لا يجوز خلطها

| الخاصية | الحزمة الموثقة | README للمرشح الآخر `408b19ba` |
| --- | --- | --- |
| أمر الإدارة | `/rentaladmin` | `/rentalcreator` |
| ACE | `m4i.rental.admin` | `m4i_rental.admin` |
| حد العقود الافتراضي | 3 | يذكر 1 |
| السعر | `ceil` إلى وحدة صحيحة | يصف التقريب إلى منزلتين عشريتين |
| ملف SQL | `sql/schema.sql` | `sql/install.sql` |
| الفلوس | عبر `m4i_bridge` v4 | يصف استدعاءات مباشرة لـm4i_core |
| المفاتيح | `HasRentalKeys` و`HasLocalRentalKeys` | يصف `HasRentalKey` |

هذا الجدول يصف الاختلاف المقروء ولا يصادق على اكتمال المرشح الآخر. خصوصاً، مبرر README الآخر بأن Bridge لا يعرض عمليات فلوس لا يطابق [عقد Bridge v4 الحالي](https://github.com/m4i-store/m4i_bridge/blob/113ed579b70a72891186d31952659294d85dc584/docs/universal-core-contract-v4.md)؛ الحزمة الموثقة تعبر الـBridge فقط.

## مصدر كل مجموعة

`config.lua` و`shared/domain.lua` يحددان الحدود والأسعار والمدد. `server/rental.lua` يحدد العقود والسباون والتحقق والتجديد والاسترجاع وAPI. `server/payment.lua` و`server/store.lua` يحددان سجل الأداء وSQL. ملفات `client/` و`web/` تحدد التفاعل والـCreator ومفاتيح التحكم. بصمات هذه الملفات مثبتة في JSON المرفق، لتسهيل اكتشاف الانحراف عند اختيار الإصدار النهائي.

ملفات stream الستة تطابق Git blobs من الأساس `65092bbd`. هذا حفظ للبيانات الأصلية، وليس دليلاً بأن محرك FiveM اختبر من جديد.

## حالة الأدلة

`BUILD_REPORT.json` للحزمة يذكر نجاح الاختبارات المحلية، لكنه يذكر صراحة `live_fivem_tested=false` و`github_upload_verified=false`. فحص docs الحالي لا يغير هاتين الحقيقتين. اقرأ [دليل الاختبار](testing.md) للتمييز بين التقرير السابق وإعادة الفحص الحالية وبوابة FiveM.

عند إصدار gameplay نهائي: ثبت commit/tag وSHA الأرشيف، قارن الأوامر وSQL والـAPI، وحدّث هذا القسم. لا تجعل توثيقاً محتملاً دليلاً على ميزة لم تنفذ أو اختبار لم يجر.
