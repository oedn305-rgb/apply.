import smtplib
import os
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- جلب الإعدادات من Secrets (GitHub Actions) ---
EMAIL_USER = os.getenv('MY_EMAIL')
EMAIL_PASS = os.getenv('EMAIL_PASS')
MY_NAME = "اسمك الكامل" # تقدر تغيره لاسمك الحقيقي

CV_FILE_PATH = "cv.pdf.pdf" 
FILE_NAME = 'all_emails.txt'

def run_job_search_bot():
    if not EMAIL_USER or not EMAIL_PASS:
        print("❌ خطأ: لم يتم العثور على EMAIL_PASS أو MY_EMAIL في Secrets!")
        return

    if not os.path.exists(FILE_NAME) or not os.path.exists(CV_FILE_PATH):
        print("❌ خطأ: ملف الإيميلات أو السيفي غير موجود!")
        return

    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        emails = [line.strip() for line in f if line.strip()]

    if not emails:
        print("🎉 القائمة فارغة!")
        return

    to_send = emails[:200]
    remaining = emails[200:]

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        
        for index, email in enumerate(to_send, 1):
            try:
                msg = MIMEMultipart()
                msg['From'] = f"{MY_NAME} <{EMAIL_USER}>"
                msg['To'] = email
                msg['Subject'] = f"Job Application - {MY_NAME}"

                body = f"Dear Recruitment Team,\n\nPlease find my attached CV.\n\nBest regards,\n{MY_NAME}"
                msg.attach(MIMEText(body, 'plain', 'utf-8'))

                with open(CV_FILE_PATH, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename=cv.pdf")
                    msg.attach(part)

                server.send_message(msg)
                print(f"✅ [{index}/200] تم الإرسال إلى: {email}")
                time.sleep(random.randint(20, 40))
            except Exception as e:
                print(f"⚠️ فشل مع {email}: {e}")

        server.quit()

        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            for mail in remaining:
                f.write(mail + '\n')
        
    except Exception as e:
        print(f"❌ خطأ في السيرفر: {e}")

if __name__ == "__main__":
    run_job_search_bot()
