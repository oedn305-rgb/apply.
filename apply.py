import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_cv_to_jobs(target_email):
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    
    # رسالة احترافية للتقديم على القطاع الخاص والمدني (ثانوي)
    subject = f"طلب انضمام للعمل - مؤهل ثانوية عامة"
    body = """
    السادة إدارة الموارد البشرية المحترمين،
    
    السلام عليكم ورحمة الله وبركاته،
    
    أتقدم إليكم بطلب وظيفة تناسب مؤهل الثانوية العامة في شركتكم الموقرة. 
    لدي الرغبة الكاملة في العمل بجدية والتزام، والمساهمة في نجاحاتكم وتطوير مهاراتي المهنية.
    
    مرفق لكم السيرة الذاتية (CV) متضمنة كافة البيانات الشخصية ووسائل التواصل.
    
    شاكر لكم وقتكم، وفي انتظار ردكم الكريم.
    
    وتفضلوا بقبول فائق الاحترام والتقدير.
    """

    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = target_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # تحديد اسم ملف السيفي (تأكد أن الملف المرفوع اسمه cv.pdf أو cv.pdf.pdf)
    filename = "cv.pdf"
    if not os.path.exists(filename):
        filename = "cv.pdf.pdf" # محاولة ثانية في حال وجود الاسم المكرر

    try:
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {filename}")
            msg.attach(part)
            
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(MY_EMAIL, EMAIL_PASS)
            server.send_message(msg)
        print(f"✅ تم الإرسال بنجاح إلى: {target_email}")
    except Exception as e:
        print(f"❌ فشل الإرسال لـ {target_email}: {e}")

# قائمة إيميلات التوظيف (أضف هنا أي إيميل جديد تجده)
job_list = [
    "recruitment@company.com.sa",
    "hr.jobs@civil-sector.com",
    "careers@local-company.com"
]

if __name__ == "__main__":
    if not job_list:
        print("القائمة فارغة، يرجى إضافة إيميلات!")
    else:
        for job_email in job_list:
            send_cv_to_jobs(job_email)
            time.sleep(5) # انتظار بسيط لتجنب الحظر
