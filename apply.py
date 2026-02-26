import os
import smtplib
import time
from email.message import EmailMessage

def send_cv_to_jobs(target_email):
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    
    # إعداد الرسالة بنظام حديث يمنع أخطاء الـ bytes
    msg = EmailMessage()
    msg['Subject'] = "طلب انضمام للعمل - مؤهل ثانوية عامة"
    msg['From'] = MY_EMAIL
    msg['To'] = target_email
    msg.set_content("""
السلام عليكم ورحمة الله وبركاته،

أتقدم إليكم بطلب وظيفة تناسب مؤهل الثانوية العامة في شركتكم الموقرة.
مرفق لكم السيرة الذاتية (CV).

شاكر لكم وقتكم، وفي انتظار ردكم الكريم.
    """)

    # --- الجزء الذكي للتعامل مع اسم الملف ---
    # البوت سيجرب البحث عن الملف بالاسم المكرر أولاً ثم الاسم العادي
    possible_filenames = ["cv.pdf.pdf", "cv.pdf"]
    filename = None

    for name in possible_filenames:
        if os.path.exists(name):
            filename = name
            break
    # ---------------------------------------

    try:
        if filename:
            with open(filename, 'rb') as f:
                file_data = f.read()
                msg.add_attachment(
                    file_data,
                    maintype='application',
                    subtype='pdf',
                    filename=filename
                )
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(MY_EMAIL, EMAIL_PASS)
                server.send_message(msg)
            print(f"✅ تم الإرسال بنجاح إلى: {target_email}")
        else:
            print(f"❌ خطأ: لم أجد ملف cv.pdf أو cv.pdf.pdf في المستودع")
            
    except Exception as e:
        print(f"❌ فشل الإرسال لـ {target_email}: {str(e)}")

# قائمة الإيميلات (تأكد من وضع إيميلات حقيقية هنا)
job_list = [
    "recruitment@company.com.sa",
    "hr.jobs@civil-sector.com",
    "careers@local-company.com"
]

if __name__ == "__main__":
    for job_email in job_list:
        send_cv_to_jobs(job_email)
        time.sleep(5)
