import time
import random
import os

# --- إعدادات الجدول والأمان ---
FILE_NAME = 'all_emails.txt'
DAILY_LIMIT = 240       # عدد الرسائل لليوم الواحد
MIN_WAIT = 90           # أقل وقت انتظار بين الرسائل (بالثواني)
MAX_WAIT = 150          # أكثر وقت انتظار بين الرسائل (بالثواني)

def bot_engine():
    # 1. التأكد من وجود ملف الإيميلات
    if not os.path.exists(FILE_NAME):
        print(f"❌ خطأ: ملف {FILE_NAME} غير موجود!")
        return

    # 2. قراءة الإيميلات من الملف
    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        all_emails = [line.strip() for line in f if line.strip()]

    if not all_emails:
        print("🎉 مبروك! انتهت جميع الإيميلات في القائمة.")
        return

    total_to_send = min(len(all_emails), DAILY_LIMIT)
    emails_to_send = all_emails[:total_to_send]
    remaining_emails = all_emails[total_to_send:]

    print(f"🚀 البوت بدأ العمل..")
    print(f"📬 مستهدف اليوم: {total_to_send} إيميل.")
    print(f"⏳ الوقت المتوقع لإنهاء مهمة اليوم: حوالي {round((total_to_send * (MIN_WAIT+MAX_WAIT)/2)/3600, 1)} ساعة.")
    print("-" * 30)

    sent_successfully = 0

    for index, email in enumerate(emails_to_send, 1):
        try:
            # -------------------------------------------------------
            # 🛑 مكان وضع قالب الإرسال (Template) الخاص بك:
            # هنا تضع الأوامر التي تفتح المتصفح أو تضغط "إرسال"
            print(f"[{index}/{total_to_send}] جاري الإرسال إلى: {email}...")
            
            # محاكاة عملية الإرسال (استبدلها بكود الأكشن حقك)
            # send_action(email) 
            
            # -------------------------------------------------------

            sent_successfully += 1
            
            # نظام الأمان: انتظار عشوائي بين كل رسالة والثانية
            if index < total_to_send: # لا ينتظر بعد آخر رسالة
                wait = random.randint(MIN_WAIT, MAX_WAIT)
                print(f"✅ تم. انتظر {wait} ثانية للأمان قبل الإيميل التالي...")
                time.sleep(wait)

        except Exception as e:
            print(f"❌ فشل الإرسال لـ {email}: {e}")

    # 3. تحديث الملف (حذف الإيميلات اللي أرسلنا لها)
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        for mail in remaining_emails:
            f.write(mail + '\n')

    print("-" * 30)
    print(f"🏁 مهمة اليوم انتهت!")
    print(f"✅ أرسل بنجاح لـ: {sent_successfully}")
    print(f"📝 تم تحديث ملف الإيميلات. المتبقي للمرات القادمة: {len(remaining_emails)}")

if __name__ == "__main__":
    bot_engine()
