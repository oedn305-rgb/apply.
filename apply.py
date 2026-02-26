import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_cv_to_jobs(target_email):
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS") # كلمة سر التطبيقات من جوجل
    
    # رسالة احترافية للقطاعين الخاص والمدني
    subject = f"طلب انضمام - شهادة ثانوية - {target_email.split('@')[0]}"
    body = """
    السادة إدارة الموارد البشرية المحترمين،
    
    السلام عليكم ورحمة الله وبركاته،
    
    أتقدم إليكم بطلب وظيفة (تناسب مؤهل الثانوية العامة) في منظومتكم الموقرة. 
    لدي رغبة كبيرة في العمل بجد واجتهاد، والمساهمة في تحقيق أهداف الشركة/المؤسسة، 
    مع الالتزام التام بالأنظمة واللوائح المهنية.
    
    مرفق لكم السيرة الذاتية (CV) متضمنة كافة البيانات الشخصية ووسائل التواصل.
    
    في انتظار ردكم الكريم، وتفضلوا بقبول فائق الاحترام والتقدير.
    
    الاسم: [اكتب اسمك هنا]
    رقم التواصل: [اكتب رقمك هنا]
    """

    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = target_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # إرفاق ملف الـ CV
    filename = "cv.pdf"
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
        print(f"✅ تم التقديم بنجاح على: {target_email}")
    except Exception as e:
        print(f"❌ خطأ في الإرسال لـ {target_email}: {e}")

# ضع هنا كل الإيميلات التي تجدها في إعلانات الوظائف (ثانوي)
job_list = [
    "recruitment@company.com.sa",
    "hr.jobs@civil-sector.com",
    "careers@local-company.com"
]

if __name__ == "__main__":
    for job_email in job_list:
        send_cv_to_jobs(job_email)
        time.sleep(5) # انتظار 5 ثوانٍ بين كل إرسال لتجنب السبام
