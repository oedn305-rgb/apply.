import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_job_bot():
    # --- إعدادات المتصفح المتقدمة (للتشغيل في GitHub Actions) ---
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # تشغيل بدون واجهة رسومية
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # إضافة User-Agent حقيقي لتبدو كزائر طبيعي وليس بوت
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = None
    try:
        # تشغيل المحرك تلقائياً
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # قراءة ملف الروابط/الإيميلات
        FILE_NAME = 'all_emails.txt'
        if not os.path.exists(FILE_NAME):
            print(f"❌ خطأ: ملف {FILE_NAME} غير موجود!")
            return

        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            print("🎉 القائمة فارغة! لا يوجد روابط للمعالجة.")
            return

        # تحديد عدد الروابط المطلوب معالجتها اليوم (مثلاً 240)
        TARGET_COUNT = 240
        to_process = lines[:TARGET_COUNT]
        remaining = lines[TARGET_COUNT:]

        print(f"🚀 بدأ البوت.. المستهدف اليوم: {len(to_process)} رابط/إيميل")

        for index, item in enumerate(to_process, 1):
            try:
                # 1. التوجه للرابط (إذا كان item عبارة عن رابط مقال)
                # إذا كان item إيميل، يمكنك استبدال الرابط ببحث جوجل عنه
                target_url = item if item.startswith('http') else f"https://www.google.com/search?q={item}"
                
                print(f"🔗 [{index}/{len(to_process)}] زيارة: {target_url}")
                driver.get(target_url)
                
                # 2. انتظار عشوائي لتحميل الصفحة
                time.sleep(random.randint(3, 7))
                
                # 3. محاكاة حركة بشرية (النزول لأسفل الصفحة قليلاً)
                scroll_height = random.randint(300, 800)
                driver.execute_script(f"window.scrollTo(0, {scroll_height});")
                print(f"✅ تم التمرير (Scroll) بنجاح.")

                # 4. انتظار إضافي قبل الانتقال للرابط التالي
                time.sleep(random.randint(5, 10))

            except Exception as e:
                print(f"⚠️ فشل في معالجة {item}: {e}")
                continue

        # --- تحديث الملف (حذف ما تم معالجته) ---
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            for line in remaining:
                f.write(line + '\n')

        print("🏁 اكتملت المهمة بنجاح وتم تحديث القائمة!")

    except Exception as e:
        print(f"❌ خطأ فني في البوت: {e}")

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    run_job_bot()
