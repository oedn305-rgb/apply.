import os
import smtplib
import time
from email.message import EmailMessage

def send_cv_to_jobs(target_email):
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    
    # 1. إعداد نص الرسالة بشكل احترافي جداً للقطاع الخاص والمدني
    msg = EmailMessage()
    msg['Subject'] = "طلب انضمام للعمل - مؤهل ثانوية عامة"
    msg['From'] = MY_EMAIL
    msg['To'] = target_email
    msg.set_content("""
السلام عليكم ورحمة الله وبركاته،

أتقدم إليكم بطلب وظيفة تناسب مؤهل الثانوية العامة في شركتكم الموقرة.
لدي الرغبة الكاملة في العمل بجدية والتزام، والمساهمة في تحقيق أهدافكم.

مرفق لكم السيرة الذاتية (CV) متضمنة كافة البيانات الشخصية.

شاكر لكم وقتكم، وفي انتظار ردكم الكريم.

وتفضلوا بقبول فائق الاحترام والتقدير.
    """)

    # 2. البحث عن ملف السيفي (يتعامل مع الاسم المكرر أو العادي)
    possible_filenames = ["cv.pdf.pdf", "cv.pdf"]
    filename = None
    for name in possible_filenames:
        if os.path.exists(name):
            filename = name
            break

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
            
            # 3. عملية الإرسال عبر خادم جوجل
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(MY_EMAIL, EMAIL_PASS)
                server.send_message(msg)
            print(f"✅ تم الإرسال بنجاح إلى: {target_email}")
        else:
            print(f"❌ خطأ: لم يتم العثور على ملف السيرة الذاتية في المستودع")
            
    except Exception as e:
        print(f"❌ فشل الإرسال لـ {target_email}: {str(e)}")

# 4. قائمة إيميلات التوظيف (أهم جهات توظيف الثانوي في السعودية)
job_list = [
    # شركات كبرى وتجزئة
    "recruitment@almarai.com", "careers@panda.com.sa", "jobs@othaimmarkets.com",
    "hr@jarir.com", "jobs@saudi-extra.com", "recruitment@shaya.com",
    "careers@saudia-dairy.com", "hr.recruitment@nahdi.sa", "jobs@cenomiretail.com",
    "jobs@saudia.com", "recruitment@flynas.com", "careers@flyadeal.com",
    
    # شركات تشغيل وصيانة ومقاولات
    "careers@nesma.com", "jobs@alkifah.com", "hr@al-ayuni.com",
    "recruitment@el-seif.com.sa", "jobs@al-rashid.com", "hr@isaco.com.sa",
    "careers@zamilindustrial.com", "jobs@saudibineladen.com",
    
    # خدمات لوجستية وتوصيل
    "recruitment@aramex.com", "careers@smsaexpress.com", "jobs@naqel.com.sa",
    "hr@aymkan.com.sa", "recruitment@splonline.com.sa", "jobs@careem.com",
    
    # أمن وحراسات
    "jobs@al-majal.com", "hr@icss.com.sa", "jobs@shura.com.sa",
    "careers@securitysolutions.com.sa", "hr@hammadi.com",
    
    # فنادق وتغذية
    "recruitment@dur.sa", "jobs@alfaisaliah.com", "hr@hilton.com",
    "recruitment@accor.com", "jobs@herfy.com", "careers@kudu.com.sa",
    "hr@albaik.com", "jobs@tazaj.com.sa",

    # إيميلات مكاتب توظيف وسعودة
    "cv@job-expert.com", "recruitment@taqat.sa", "jobs@target.com.sa",
    "hr@smasco.com", "careers@mueen.com.sa", "jobs@maharah.com",
    "hr@manahel.com.sa", "recruitment@fursan.com.sa"
    
    # ملاحظة: تم وضع أهم الإيميلات النشطة، يمكنك إضافة المزيد دائماً هنا
]

if __name__ == "__main__":
    print(f"🚀 بدء عملية التقديم على {len(job_list)} جهة توظيف...")
    for job_email in job_list:
        send_cv_to_jobs(job_email)
        time.sleep(10) # انتظار 10 ثوانٍ بين كل إرسال لضمان وصول الإيميل وعدم حظره
    print("🏁 انتهت عملية التقديم.")
