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
MY_NAME = "مشعل المطيري" # تم تحديث الاسم

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

    # التأكد من وجود ملف الإيميلات والسيرة الذاتية
    if not os.path.exists(FILE_NAME) or not os.path.exists(CV_FILE_PATH):
        print(f"❌ خطأ: تأكد من وجود {FILE_NAME} و {CV_FILE_PATH}")
        return

    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        emails = [line.strip() for line in f if line.strip()]

    if not emails:
        print("🎉 القائمة فارغة! تم إرسال كافة الإيميلات.")
        return

    # إرسال 200 إيميل في المرة الواحدة لمنع حظر الحساب
    to_send = emails[:200]
    
    print(f"🚀 انطلاق.. محاولة إرسال {len(to_send)} إيميل لشركات مكة...")

    server = get_mail_server()
    if not server: return

    sent_count = 0
    index = 0
    try:
        for index, email in enumerate(to_send, 1):
            retry_limit = 2
            while retry_limit > 0:
                try:
                    msg = MIMEMultipart()
                    msg['From'] = f"{MY_NAME} <{EMAIL_USER}>"
                    msg['To'] = email
                    # عنوان الرسالة جذاب لشركات مكة
                    msg['Subject'] = f"طلب توظيف موسم رمضان (ثانوي) - {MY_NAME}"

                    # نص الرسالة المخصص لوظائف مكة
                    body = f"""السلام عليكم ورحمة الله وبركاته،

أنا {MY_NAME}، حاصل على شهادة الثانوية العامة، وأرغب في التقدم للعمل لديكم في موسم رمضان المبارك بمكة المكرمة.

أبحث عن فرصة عمل ميدانية تشمل:
- توفير سكن وإعاشة.
- أو العمل بنظام الأجر اليومي.

مرفق لكم سيرتي الذاتية، وأنا متاح للمباشرة فوراً وجاهز لخدمة ضيوف الرحمن بكل جدية ونشاط.

للتواصل: 0552145971
تحياتي،
{MY_NAME}"""
                    
                    msg.attach(MIMEText(body, 'plain', 'utf-8'))

                    # إرفاق السيرة الذاتية
                    with open(CV_FILE_PATH, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header("Content-Disposition", f"attachment; filename=Mishal_AlMutairi_CV.pdf")
                        msg.attach(part)

                    server.send_message(msg)
                    print(f"✅ [{index}/{len(to_send)}] تم الإرسال بنجاح إلى: {email}")
                    sent_count += 1
                    break 
                
                except (smtplib.SMTPServerDisconnected, smtplib.SMTPException):
                    print("🔄 انقطع الاتصال.. جاري إعادة الاتصال بالسيرفر...")
                    server = get_mail_server()
                    retry_limit -= 1
                    time.sleep(5)
                except Exception as e:
                    print(f"⚠️ فشل مع {email}: {e}")
                    break

            # الانتظار العشوائي (بين 25 و 45 ثانية) لحماية إيميلك من الحظر
            time.sleep(random.randint(25, 45))

    finally:
        if server:
            try: server.quit()
            except: pass

        # تحديث ملف all_emails.txt وحذف من تم الإرسال لهم
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            remaining_emails = emails[index:] 
            for mail in remaining_emails:
                f.write(mail + '\n')
        
        print(f"🏁 اكتملت المهمة. تم معالجة {sent_count} إيميل بنجاح.")

if __name__ == "__main__":
    run_job_search_bot()
