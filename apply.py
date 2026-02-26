import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # إعدادات لتسريع التصفح ومنع الصور
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # وضع مهلة زمنية قصيرة (20 ثانية كحد أقصى لتحميل أي صفحة)
    driver.set_page_load_timeout(20) 
    return driver

def run_job_bot():
    FILE_NAME = 'all_emails.txt'
    if not os.path.exists(FILE_NAME):
        print("❌ الملف غير موجود")
        return

    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        print("🎉 القائمة انتهت")
        return

    to_process = lines[:240]
    remaining = lines[240:]
    
    driver = get_driver()
    print(f"🚀 انطلاق.. معالجة {len(to_process)} رابط")

    for index, item in enumerate(to_process, 1):
        # إعادة تشغيل المتصفح كل 40 رابط للحفاظ على السرعة
        if index % 40 == 0:
            driver.quit()
            driver = get_driver()

        try:
            url = item if item.startswith('http') else f"https://www.google.com/search?q={item}"
            print(f"⚡ [{index}] جاري الدخول: {item[:30]}...")
            
            driver.get(url)
            # انتظار بسيط جداً (3-5 ثواني كافية مع منع الصور)
            time.sleep(random.randint(3, 5))
            
        except TimeoutException:
            print(f"⚠️ تم تخطي {item[:20]} بسبب التأخر في الاستجابة")
        except Exception as e:
            print(f"❌ خطأ بسيط: {e}")

    # حفظ الباقي فوراً
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        for line in remaining:
            f.write(line + '\n')

    driver.quit()
    print("🏁 انتهى العمل بنجاح!")

if __name__ == "__main__":
    run_job_bot()
