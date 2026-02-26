import smtplib
import os
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- جلب الإعدادات من Secrets ---
EMAIL_USER = os.getenv('MY_EMAIL')
EMAIL_PASS = os.getenv('EMAIL_PASS')
# هنا اكتب اسمك الحقيقي ليظهر في نهاية الرسالة
MY_NAME = "اكتب اسمك هنا" 

# إعدادات الملفات
CV_FILE_PATH = "cv.pdf.pdf" 
FILE_NAME = 'all_emails.txt'

def run_job_search_bot():
    if not EMAIL_USER or not EMAIL_PASS:
        print("❌ خطأ: لم يتم العثور على EMAIL_PASS أو MY_EMAIL في Secrets!")
        return

    if not os.path.exists(FILE_NAME) or not os.path.exists(CV_FILE_PATH):
        print(f"❌ خطأ: تأكد من وجود {FILE_NAME} و {CV_FILE_PATH}")
        return

    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        emails = [line.strip() for line in f if line.strip()]

    if not emails:
        print("🎉 القائمة فارغة! تم إرسال كافة الإيميلات.")
        return

    to_send = emails[:200]
    remaining = emails[200:]

    print(f"🚀 انطلاق.. محاولة إرسال {len(to_send)} إيميل بمقدمة احترافية...")

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

                # المقدمة الاحترافية بدون عبارة "اسمك الكامل" الزائدة
                body = f"""
Dear Recruitment Team,

I am writing to express my strong interest in joining your esteemed organization. 

With a solid commitment to professional excellence and a proactive approach to problem-solving, I am confident that my skills and dedication will be a valuable asset to your team. I have long admired your company's reputation for innovation, and I am eager to contribute to your ongoing success.

Please find my attached CV for more details about my experience and qualifications. I look forward to the opportunity of a personal interview to discuss how I can add value to your company.

Best regards,
{MY_NAME}
                """
                msg.attach(MIMEText(body, 'plain', 'utf-8'))

                # إرفاق السيفي
                with open(CV_FILE_PATH, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename=Professional_CV.pdf")
                    msg.attach(part)

                server.send_message(msg)
                print(f"✅ [{index}/200] تم الإرسال بنجاح إلى: {email}")
                
                # انتظار عشوائي لمنع الحظر
                time.sleep(random.randint(25, 45))

            except Exception as e:
                print(f"⚠️ فشل مع {email}: {e}")
                continue

        server.quit()

        # تحديث القائمة (حذف الإيميلات المرسلة)
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            for mail in remaining:
                f.write(mail + '\n')
        
        print("🏁 اكتملت المهمة بنجاح.")

    except Exception as e:
        print(f"❌ فشل في الاتصال بالسيرفر: {e}")

if __name__ == "__main__":
    run_job_search_bot()
