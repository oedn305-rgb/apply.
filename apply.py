import smtplib
import os
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- الإعدادات الشخصية ---
EMAIL_USER = os.getenv('MY_EMAIL')
EMAIL_PASS = os.getenv('EMAIL_PASS')
MY_NAME = "مشعل المطيري"
NOON_CODE = "MSHL1" 

FILE_NAME = 'makkah_emails.txt' 
CV_FILE_PATH = "cv.pdf.pdf" 
# ضع هنا رابط المكنسة الحقيقي من نون
NOON_PRODUCT_URL = "https://www.noon.com/saudi-ar/p-12345" 

def run_triple_rotation_bot():
    if not os.path.exists(FILE_NAME):
        print("❌ ملف الإيميلات غير موجود!")
        return

    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        emails = [line.strip() for line in f if line.strip()]

    # الحد اليومي 200 رسالة لسلامة الحساب
    to_process = emails[:200]
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(EMAIL_USER, EMAIL_PASS)

    for index, email in enumerate(to_process):
        msg = MIMEMultipart()
        msg['From'] = f"{MY_NAME} <{EMAIL_USER}>"
        msg['To'] = email

        # --- نظام الترتيب الثلاثي (Modulo 3) ---
        step = index % 3

        if step == 0:
            # 1. وظائف مكة (الجديدة)
            msg['Subject'] = f"طلب عمل بمكة - موسم رمضان - {MY_NAME}"
            body = f"السلام عليكم، معكم {MY_NAME}، أبحث عن فرصة عمل ميدانية بمكة المكرمة. التواصل: 0552145971"
            # إرفاق الـ CV
            if os.path.exists(CV_FILE_PATH):
                with open(CV_FILE_PATH, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename=Mishal_CV.pdf")
                    msg.attach(part)
            type_tag = "وظيفة مكة 🕋"

        elif step == 1:
            # 2. تسويق منتج نون (المكنسة)
            msg['Subject'] = "🔥 عرض خاص: المكنسة اللاسلكية الذكية بخصم (MSHL1)"
            body = f"أهلاً بك، وفر مجهودك مع المكنسة اللاسلكية للبيت والسيارة.\n💰 كود الخصم: {NOON_CODE}\n🔗 الرابط: {NOON_PRODUCT_URL}"
            type_tag = "تسويق نون 💰"

        else:
            # 3. الاستهداف القديم (شركات ومقاولات)
            msg['Subject'] = "استعلام عن فرص تعاون وعمل - {MY_NAME}"
            body = f"تحية طيبة، أنا {MY_NAME}، مهتم بالعمل معكم في مشاريعكم القائمة بمكة. رقم التواصل: 0552145971"
            type_tag = "استهداف قديم 🏗️"

        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        try:
            server.send_message(msg)
            print(f"✅ [{index+1}/200] تم إرسال ({type_tag}) إلى: {email}")
        except Exception as e:
            print(f"❌ خطأ مع {email}: {e}")

        # وقت انتظار ذكي (بين 45 و 90 ثانية) لمنع الحظر
        time.sleep(random.randint(45, 90))

    server.quit()
    print("🚀 تم إكمال الـ 200 رسالة لليوم بنجاح بالترتيب الثلاثي!")

if __name__ == "__main__":
    run_triple_rotation_bot()
