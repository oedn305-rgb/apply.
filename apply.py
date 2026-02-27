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
MY_NAME = "اكتب اسمك هنا" 

# إعدادات الملفات
CV_FILE_PATH = "cv.pdf.pdf" 
FILE_NAME = 'all_emails.txt'

def get_mail_server():
    """دالة لإنشاء اتصال جديد بالسيرفر"""
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_USER, EMAIL_PASS)
        return server
    except Exception as e:
        print(f"❌ فشل في إنشاء اتصال جديد: {e}")
        return None

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

    print(f"🚀 انطلاق.. محاولة إرسال {len(to_send)} إيميل...")

    # فتح أول اتصال
    server = get_mail_server()
    if not server: return

    sent_count = 0
    try:
        for index, email in enumerate(to_send, 1):
            # محاولة الإرسال مع نظام إعادة الاتصال التلقائي
            retry_limit = 2
            while retry_limit > 0:
                try:
                    msg = MIMEMultipart()
                    msg['From'] = f"{MY_NAME} <{EMAIL_USER}>"
                    msg['To'] = email
                    msg['Subject'] = f"Job Application - {MY_NAME}"

                    body = f"""Dear Recruitment Team,\n\nI am writing to express my strong interest in joining your esteemed organization.\n\nBest regards,\n{MY_NAME}"""
                    msg.attach(MIMEText(body, 'plain', 'utf-8'))

                    with open(CV_FILE_PATH, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header("Content-Disposition", f"attachment; filename=Professional_CV.pdf")
                        msg.attach(part)

                    server.send_message(msg)
                    print(f"✅ [{index}/200] تم الإرسال بنجاح إلى: {email}")
                    sent_count += 1
                    break # اخرج من حلقة الـ retry لو نجح الإرسال
                
                except (smtplib.SMTPServerDisconnected, smtplib.SMTPException):
                    print("🔄 انقطع الاتصال.. جاري إعادة الاتصال بالسيرفر...")
                    server = get_mail_server()
                    retry_limit -= 1
                    time.sleep(5)
                except Exception as e:
                    print(f"⚠️ فشل مع {email}: {e}")
                    break

            # انتظار عشوائي لمنع الحظر (بين 25 و 45 ثانية كما طلبت)
            time.sleep(random.randint(25, 45))

    finally:
        if server:
            try: server.quit()
            except: pass

        # تحديث القائمة (حذف الإيميلات التي تمت محاولة إرسالها فقط)
        # لضمان عدم ضياع الإيميلات لو توقف البوت فجأة
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            # نحذف فقط اللي مروا في الحلقة
            actually_processed = emails[index:] 
            for mail in actually_processed:
                f.write(mail + '\n')
        
        print(f"🏁 اكتملت المهمة. تم معالجة {index} إيميل.")

if __name__ == "__main__":
    run_job_search_bot()
