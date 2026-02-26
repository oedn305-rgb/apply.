import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- إعدادات الجدول ---
FILE_NAME = 'all_emails.txt'
DAILY_LIMIT = 240 

def start_bot():
    # إعدادات المتصفح للعمل في سيرفر (وضع الخفاء)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # قراءة الإيميلات
    if not os.path.exists(FILE_NAME):
        print("❌ الملف غير موجود!")
        return

    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        all_emails = [line.strip() for line in f if line.strip()]

    if not all_emails:
        print("🎉 القائمة فارغة!")
        return

    to_send = all_emails[:DAILY_LIMIT]
    remaining = all_emails[DAILY_LIMIT:]

    print(f"🚀 بدء الإرسال لـ {len(to_send)} إيميل...")

    for index, email in enumerate(to_send, 1):
        try:
            # --- هنا تضع خطوات الإرسال الخاصة بك ---
            # مثال: driver.get(f"رابط_البحث_أو_الإيميل")
            print(f"[{index}/{len(to_send)}] جاري المعالجة: {email}")
            
            # الانتظار الآمن (المعدل السريع)
            time.sleep(random.randint(20, 45))

        except Exception as e:
            print(f"❌ خطأ مع {email}: {e}")

    # تحديث الملف (حذف من تم الإرسال لهم)
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        for mail in remaining:
            f.write(mail + '\n')

    driver.quit()
    print("✅ انتهت المهمة بنجاح.")

if __name__ == "__main__":
    start_bot()
