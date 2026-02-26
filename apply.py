import time
import random

def start_sending():
    # 1. قراءة قائمة الإيميلات من ملفك
    with open('all_emails.txt', 'r') as f:
        emails = [line.strip() for line in f if line.strip()]

    # 2. تحديد كمية الإرسال لليوم (مثلاً 240)
    # يمكنك تغيير هذا الرقم يدوياً كل يوم (أول يوم 250 ثم 240)
    limit_per_day = 240 
    sent_count = 0

    print(f"🚀 تم تحميل {len(emails)} إيميل. سيبدأ الإرسال لـ {limit_per_day} جهة اليوم...")

    for email in emails:
        if sent_count >= limit_per_day:
            print("✅ اكتمل نصاب اليوم! البوت سيتوقف الآن.")
            break

        try:
            # --- هنا تضع كود الإرسال الخاص بك (Template) ---
            print(f"📧 جاري الإرسال إلى: {email}")
            
            # محاكاة عملية الإرسال
            # send_email_function(email) 
            
            sent_count += 1
            
            # --- أهم جزء للأمان: الفاصل الزمني العشوائي ---
            # البوت بينتظر بين كل إيميل وإيميل وقت عشوائي بين دقيقة ونصف إلى دقيقتين ونصف
            wait_time = random.randint(90, 150) 
            print(f"⏳ انتظار لمدة {wait_time} ثانية لتجنب الحظر...")
            time.sleep(wait_time)

        except Exception as e:
            print(f"❌ خطأ في الإرسال لـ {email}: {e}")

    # 3. تحديث الملف (حذف الإيميلات التي تم الإرسال لها)
    remaining_emails = emails[sent_count:]
    with open('all_emails.txt', 'w') as f:
        for mail in remaining_emails:
            f.write(mail + '\n')
    
    print(f"🏁 تم إرسال {sent_count} رسالة، وتحديث الملف للمرة القادمة.")

# تشغيل البوت
start_sending()
