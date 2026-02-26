import requests
import time
import random
import os
from concurrent.futures import ThreadPoolExecutor

# إعدادات بسيطة
FILE_NAME = 'all_emails.txt'
TARGET_COUNT = 4000  # العدد اللي تبي تخلصه اليوم
THREADS = 10  # عدد الروابط اللي يفتحها بنفس اللحظة (تقدر تزيدها لـ 20)

def visit_url(item):
    """وظيفة لزيارة الرابط بسرعة بدون متصفح"""
    try:
        # تحويل النص لرابط بحث إذا لم يكن رابطاً
        url = item if item.startswith('http') else f"https://www.google.com/search?q={item}"
        
        # إرسال طلب سريع للموقع (بدون تحميل صور أو جافا سكريبت)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"✅ تم تحديث: {item[:20]}... الحالة: {response.status_code}")
        return True
    except Exception:
        print(f"❌ فشل الوصول لـ: {item[:20]}")
        return False

def run_fast_bot():
    if not os.path.exists(FILE_NAME):
        print("❌ ملف all_emails.txt غير موجود!")
        return

    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        print("🎉 القائمة فارغة!")
        return

    to_process = lines[:TARGET_COUNT]
    remaining = lines[TARGET_COUNT:]

    print(f"🚀 انطلاق! جاري معالجة {len(to_process)} رابط باستخدام {THREADS} خيوط معالجة (Threads)...")

    # تشغيل عدة روابط في نفس الوقت لتسريع العملية جداً
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.map(visit_url, to_process)

    # حفظ الروابط المتبقية في الملف
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        for line in remaining:
            f.write(line + '\n')

    print(f"🏁 انتهت المهمة! تم معالجة {len(to_process)} وبقي {len(remaining)} رابط.")

if __name__ == "__main__":
    start_time = time.time()
    run_fast_bot()
    print(f"⏱️ الوقت المستغرق: {round(time.time() - start_time, 2)} ثانية.")
