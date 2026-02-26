import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_job_bot():
    # --- إعدادات المتصفح الصامتة (عشان يشتغل في GitHub بدون شاشة) ---
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    try:
        # تشغيل المحرك تلقائياً
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # قراءة ملف الإيميلات
        FILE_NAME = 'all_emails.txt'
        if not os.path.exists(FILE_NAME):
            print("❌ خطأ: ملف all_emails.txt غير موجود!")
            return

        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            emails = [line.strip() for line in f if line.strip()]

        if not emails:
            print("🎉 القائمة انتهت بالكامل!")
            return

        # الجدول الزمني: 240 إيميل اليوم
        to_send = emails[:240]
        remaining = emails[240:]

        print(f"🚀 بدأ البوت.. المستهدف اليوم: {len(to_send)} إيميل")

        for index, email in enumerate(to_send, 1):
            # هنا البوت "يتصفح" الإيميل (تقدر تضيف كود الإرسال الفعلي هنا)
            print(f"✅ معالجة: {email} [{index}/{len(to_send)}]")
            
            # انتظار عشوائي سريع (بين 5 و 12 ثانية) عشان ما يطول "الفر"
            time.sleep(random.randint(5, 12)) 

        # حفظ القائمة الجديدة (حذف اللي أرسلنا لهم)
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            for mail in remaining:
                f.write(mail + '\n')

        driver.quit()
        print("🏁 اكتملت المهمة بنجاح!")

    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    run_job_bot()
