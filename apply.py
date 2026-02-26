import time
import random
import os

# ==========================================
# إعدادات الجدول (تقدر تعدلها هنا)
# ==========================================
FILE_NAME = 'all_emails.txt'
DAILY_LIMIT = 240       # عدد الرسايل اليومية
MIN_WAIT = 20           # أقل وقت انتظار (ثانية)
MAX_WAIT = 45           # أكثر وقت انتظار (ثانية)
# ==========================================

def start_bot():
    # 1. التأكد من وجود ملف الإيميلات
    if not os.path.exists(FILE_NAME):
        print(f"❌ خطأ: ملف {FILE_NAME} غير موجود في نفس المجلد!")
        return

    # 2. قراءة الإيميلات من الملف
    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        all_emails = [line.strip() for line in f if line.strip()]

    if not all_emails:
        print("🎉 مبروك! القائمة خلصت بالكامل، ما فيه إيميلات متبقية.")
        return

    # تحديد العدد المطلوب إرساله اليوم
    total_to_send = min(len(all_emails), DAILY_LIMIT)
    emails_for_today = all_emails[:total_to_send]
    remaining_emails = all_emails[total_to_send:]

    print(f"🚀 تشغيل البوت... المستهدف اليوم: {total_to_send} إيميل")
    print("-" * 40)

    sent_successfully = 0

    for index, email in enumerate(emails_for_today, 1):
        try:
            # 🛑 [مكان وضع كود الإرسال حقك - Template] 🛑
            # هنا تحط الأوامر اللي تفتح الإيميل وتضغط إرسال
            print(f"[{index}/{total_to_send}] جاري الإرسال إلى: {email}")
            
            # محاكاة لعملية الإرسال
            # (حط كود الأكشن حقك هنا)
            
            sent_successfully += 1
            
            # الفاصل الزمني (تم تقليله بناءً على طلبك)
            if index < total_to_send:
                wait = random.randint(MIN_WAIT, MAX_WAIT)
                print(f"⏳ انتظار آمن لمدة {wait} ثانية...")
                time.sleep(wait)

        except Exception as e:
            print(f"❌ فشل الإرسال لـ {email}: {e}")

    # 3. تحديث الملف وحذف الإيميلات اللي أرسلنا لها
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        for mail in remaining_emails:
            f.write(mail + '\n')

    print("-" * 40)
    print(f"🏁 انتهت مهمة اليوم بنجاح!")
    print(f"✅ تم إرسال: {sent_successfully}")
    print(f"📝 المتبقي في الملف لبكرة: {len(remaining_emails)} إيميل")

if __name__ == "__main__":
    start_bot()
