import smtplib
import os
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- الإعدادات من Secrets ---
EMAIL_USER = os.getenv('MY_EMAIL')
EMAIL_PASS = os.getenv('EMAIL_PASS')
MY_NAME = "مشعل المطيري"

# الملفات
MAKKAH_FILE = 'makkah_emails.txt'
OLD_FILE = 'all_emails.txt'
CV_FILE_PATH = "cv.pdf.pdf" 

def get_mail_server():
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_USER, EMAIL_PASS)
        return server
    except Exception as e:
        print(f"❌ فشل الاتصال: {e}")
        return None

def run_smart_bot():
    if not EMAIL_USER or not EMAIL_PASS:
        print("❌ خطأ في Secrets!")
        return

    # 1. تحديد أي ملف سنستخدم (الأولوية لمكة)
    current_file = ""
    is_makkah = False

    if os.path.exists(MAKKAH_FILE) and os.path.getsize(MAKKAH_FILE) > 0:
        current_file = MAKKAH_FILE
        is_makkah = True
        print("📍 الأولوية الآن: وظائف مكة المكرمة...")
    elif os.path.exists(OLD_FILE) and os.path.getsize(OLD_FILE) > 0:
        current_file = OLD_FILE
        is_makkah = False
        print("🔄 تم الانتهاء من مكة، العودة للاستهداف القديم...")
    else:
        print("🎉 كل القوائم فارغة! تم إرسال جميع الإيميلات.")
        return

    # قراءة الإيميلات من الملف المختار
    with open(current_file, 'r', encoding='utf-8') as f:
        emails = [line.strip() for line in f if line.strip()]

    to_send = emails[:200]
    server = get_mail_server()
    if not server: return

    index = 0
    try:
        for index, email in enumerate(to_send, 1):
            msg = MIMEMultipart()
            msg['From'] = f"{MY_NAME} <{EMAIL_USER}>"
            msg['To'] = email

            # تخصيص العنوان والنص حسب نوع الملف
            if is_makkah:
                msg['Subject'] = f"طلب توظيف موسم رمضان (ثانوي) - {MY_NAME}"
                body = f"السلام عليكم، أنا {MY_NAME}، متاح للعمل الميداني بمكة في موسم رمضان (ثانوي). أحتاج سكن وإعاشة أو أجر يومي. التواصل: 0552145971"
            else:
                msg['Subject'] = f"Job Application - {MY_NAME}"
                body = f"Dear Recruitment Team,\n\nI am writing to express my interest in joining your organization.\n\nBest regards,\n{MY_NAME}\nPhone: 0552145971"

            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # إرفاق السيرة الذاتية
            if os.path.exists(CV_FILE_PATH):
                with open(CV_FILE_PATH, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename=Mishal_CV.pdf")
                    msg.attach(part)

            try:
                server.send_message(msg)
                print(f"✅ تم الإرسال إلى ({'مكة' if is_makkah else 'عام'}): {email}")
            except Exception as e:
                print(f"⚠️ خطأ مع {email}: {e}")

            time.sleep(random.randint(25, 45))

    finally:
        if server: server.quit()
        # تحديث الملف اللي استخدمناه وحذف المرسل
        with open(current_file, 'w', encoding='utf-8') as f:
            for mail in emails[index:]:
                f.write(mail + '\n')
        
        print(f"🏁 انتهت الدفعة الحالية.")

if __name__ == "__main__":
    run_smart_bot()
