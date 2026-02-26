import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# --- إعداداتك ---
FILE_NAME = 'all_emails.txt'
DAILY_LIMIT = 240 

def start_job():
    # 1. تشغيل المتصفح (كروم)
    driver = webdriver.Chrome() 
    driver.get("https://mail.google.com") # أو رابط قالبك
    
    print("⚠️ سجل دخولك يدوياً الآن في المتصفح، ثم اضغط Enter هنا بالكود...")
    input() 

    # 2. قراءة الملف
    if not os.path.exists(FILE_NAME): return
    with open(FILE_NAME, 'r') as f:
        emails = [line.strip() for line in f if line.strip()]

    to_send = emails[:DAILY_LIMIT]
    remaining = emails[DAILY_LIMIT:]

    for index, email in enumerate(to_send, 1):
        try:
            # --- بداية عملية الإرسال الفعلية ---
            # هنا البوت يضغط على زر "إنشاء رسالة"
            # ملاحظة: المسميات (ID) تختلف حسب قالبك
            print(f"[{index}/{DAILY_LIMIT}] إرسال إلى: {email}")

            # مثال: كتابة الإيميل (هنا تضع أوامر القالب حقك)
            # driver.find_element(By.NAME, "to").send_keys(email)
            
            # --- انتهى الإرسال ---

            # الانتظار الآمن (عشان ما تطلع الدائرة الصفراء للأبد)
            wait = random.randint(20, 45)
            time.sleep(wait)

        except Exception as e:
            print(f"خطأ: {e}")

    # 3. تحديث القائمة
    with open(FILE_NAME, 'w') as f:
        for m in remaining: f.write(m + '\n')
    
    driver.quit()
    print("✅ انتهت المهمة وتحدث الملف.")

start_job()
