import smtplib
import os
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- الإعدادات الاحترافية ---
EMAIL_USER = 'your_email@gmail.com'  # بريدك الإلكتروني
EMAIL_PASS = 'your_app_password'     # كلمة مرور التطبيق
MY_NAME = "اسمك الكامل"
CV_FILE_PATH = "my_cv.pdf"           # اسم ملف السيرة الذاتية (يجب أن يكون بنفس المجلد)

def send_professional_email(to_email):
    try:
        # 1. إنشاء الرسالة
        msg = MIMEMultipart()
        msg['From'] = f"{MY_NAME} <{EMAIL_USER}>"
        msg['To'] = to_email
        msg['Subject'] = f"Job Application - {MY_NAME} - Seeking New Opportunities"

        # 2. نص الرسالة (جذاب ومختصر)
        body = f"""
Dear Recruitment Team,

I hope this email finds you well.

I am writing to express my interest in joining your esteemed organization. With my background and experience, I believe I can be a valuable asset to your team. 

Please find my attached CV for your review. I look forward to the possibility of discussing how my skills can contribute to your company.

Best Regards,
{MY_NAME}
        """
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # 3. إرفاق السيرة الذاتية (PDF)
        if os.path.exists(CV_FILE_PATH):
            with open(CV_FILE_PATH, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename= {CV_FILE_PATH}")
                msg.attach(part)

        # 4. الاتصال بالسيرفر والإرسال
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ تم الإرسال بنجاح إلى: {to_email}")
        return True
    except Exception as e:
        print(f"❌ خطأ مع {to_email}: {e}")
        return False

def run_job_search_bot():
    FILE_NAME = 'all_emails.txt'
    if not os.path.exists(FILE_NAME):
        print("❌ خطأ: ملف الإيميلات غير موجود!")
        return

    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        emails = [line.strip() for line in f if line.strip()]

    if not emails:
        print("🎉 اكتملت جميع القوائم!")
        return

    # معالجة 200 إيميل فقط لليوم لضمان الأمان
    to_send = emails[:200]
    remaining = emails[200:]

    print(f"🚀 انطلاق البوت.. إرسال {len(to_send)} إيميل اليوم.")

    for index, email in enumerate(to_send, 1):
        success = send_professional_email(email)
        
        if success:
            # انتظار عشوائي بين 20 و 45 ثانية (مهم جداً لتجنب السبام)
            sleep_time = random.randint(20, 45)
            print(f"😴 انتظار {sleep_time} ثانية... [{index}/200]")
            time.sleep(sleep_time)

    # تحديث الملف وحذف من تم الإرسال لهم
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        for mail in remaining:
            f.write(mail + '\n')

    print("🏁 انتهت مهمة اليوم بنجاح!")

if __name__ == "__main__":
    run_job_search_bot()
