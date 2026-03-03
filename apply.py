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

# --- أسماء الملفات الثلاثة ---
FILE_MAKKAH = 'makkah_emails.txt'      # ملف وظائف مكة
FILE_OLD = 'old_jobs_emails.txt'       # ملف الوظائف القديم
FILE_MARKETING = 'million_emails.txt'  # ملف التسويق الجديد (الـ 47 دفعة)

CV_FILE_PATH = "cv.pdf" 
NOON_PRODUCT_URL = "https://www.noon.com" 

def load_emails(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    return []

def run_triple_rotation_bot():
    # تحميل الإيميلات من الـ 3 مصادر
    emails_makkah = load_emails(FILE_MAKKAH)
    emails_old = load_emails(FILE_OLD)
    emails_marketing = load_emails(FILE_MARKETING)

    if not (emails_makkah or emails_old or emails_marketing):
        print("❌ لا توجد إيميلات في أي ملف!")
        return

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(EMAIL_USER, EMAIL_PASS)

    # حلقة لإرسال 200 رسالة يومياً
    for i in range(200):
        msg = MIMEMultipart()
        msg['From'] = f"{MY_NAME} <{EMAIL_USER}>"
        
        # التبديل بين الملفات (0: مكة، 1: قديم، 2: تسويق)
        step = i % 3
        
        if step == 0 and emails_makkah:
            target_email = emails_makkah.pop(0)
            msg['Subject'] = f"طلب عمل ميداني بمكة - موسم رمضان - {MY_NAME}"
            body = f"السلام عليكم، معكم {MY_NAME}، أبحث عن فرصة عمل بمكة. التواصل: 0552145971"
            type_tag = "وظيفة مكة 🕋"
            # إرفاق الـ CV
            if os.path.exists(CV_FILE_PATH):
                with open(CV_FILE_PATH, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename=Mishal_CV.pdf")
                    msg.attach(part)

        elif step == 1 and emails_old:
            target_email = emails_old.pop(0)
            msg['Subject'] = f"استفسار عن فرص تعاون - {MY_NAME}"
            body = f"تحية طيبة، أنا {MY_NAME}، سبق وتواصلت معكم ومهتم بالعمل في مشاريعكم القائمة. رقمي: 0552145971"
            type_tag = "استهداف قديم 🏗️"

        elif emails_marketing:
            target_email = emails_marketing.pop(0)
            msg['Subject'] = "🔥 عرض خاص: خصم إضافي من نون حصرياً (MSHL1)"
            body = f"أهلاً بك، وفر مجهودك ومالك مع عروض نون القوية.\n💰 كود الخصم الإضافي: {NOON_CODE}\n🔗 تسوق الآن: {NOON_PRODUCT_URL}"
            type_tag = "تسويق نون الجديد 💰"
        else:
            continue # إذا خلص ملف، يكمل للي بعده

        msg['To'] = target_email
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        try:
            server.send_message(msg)
            print(f"✅ [{i+1}/200] تم إرسال ({type_tag}) إلى: {target_email}")
        except Exception as e:
            print(f"❌ خطأ مع {target_email}: {e}")

        # وقت انتظار ذكي (45-90 ثانية) لحماية حسابك
        time.sleep(random.randint(45, 90))

    server.quit()
    print("🚀 تم إنجاز الـ 200 رسالة بنجاح!")

if __name__ == "__main__":
    run_triple_rotation_bot()
