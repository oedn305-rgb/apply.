import smtplib
import os
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- الإعدادات الشخصية ---
EMAIL_USER = os.getenv('MY_EMAIL')
EMAIL_PASS = os.getenv('EMAIL_PASS')
MY_NAME = "مشعل المطيري"
NOON_CODE = "MSHL1" 

# --- أسماء ملفاتك الحقيقية ---
FILE_MAKKAH = 'makkah_emails.txt'     # ملف وظائف مكة
FILE_OLD = 'all_emails.txt'          # ملف الوظائف القديم (الأساسي)
FILE_MARKETING = 'million_emails.txt' # ملف التسويق الجديد (الـ 47 دفعة)

CV_FILE_PATH = "cv.pdf.pdf"          # اسم ملف الـ CV عندك
NOON_PRODUCT_URL = "https://www.noon.com" 

def load_and_pop_email(file_path):
    """يقرأ الإيميلات، يأخذ الأول، ويمسحه من الملف لعدم التكرار"""
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if not lines:
        return None
    
    target_email = lines[0].strip()
    # إعادة كتابة الملف بدون أول إيميل (مسح التكرار)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines[1:])
        
    return target_email

def run_triple_rotation_bot():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(EMAIL_USER, EMAIL_PASS)

    print("🚀 بدء عملية الإرسال الثلاثية (200 رسالة)...")

    for i in range(200):
        msg = MIMEMultipart()
        msg['From'] = f"{MY_NAME} <{EMAIL_USER}>"
        
        step = i % 3
        target_email = None
        type_tag = ""

        if step == 0:
            target_email = load_and_pop_email(FILE_MAKKAH)
            if target_email:
                msg['Subject'] = f"طلب عمل ميداني بمكة - موسم رمضان - {MY_NAME}"
                body = f"السلام عليكم، معكم {MY_NAME}، أبحث عن فرصة عمل بمكة. التواصل: 0552145971"
                type_tag = "وظيفة مكة 🕋"
                # إرفاق الـ CV
                if os.path.exists(CV_FILE_PATH):
                    with open(CV_FILE_PATH, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header("Content-Disposition", f"attachment; filename=Mishal_CV.pdf")
                        msg.attach(part)

        elif step == 1:
            target_email = load_and_pop_email(FILE_OLD)
            if target_email:
                msg['Subject'] = f"استفسار عن فرص تعاون وعمل - {MY_NAME}"
                body = f"تحية طيبة، أنا {MY_NAME}، مهتم بالعمل معكم في مشاريعكم القائمة بمكة. رقمي: 0552145971"
                type_tag = "استهداف قديم 🏗️"

        else:
            target_email = load_and_pop_email(FILE_MARKETING)
            if target_email:
                msg['Subject'] = "🔥 عرض خاص: خصم إضافي من نون (كود: MSHL1)"
                body = f"أهلاً بك، وفر مجهودك ومالك مع عروض نون القوية.\n💰 كود الخصم الإضافي: {NOON_CODE}\n🔗 تسوق الآن: {NOON_PRODUCT_URL}"
                type_tag = "تسويق نون الجديد 💰"

        # إذا لم يجد إيميل في الملف المحدد، يحاول سحب واحد من ملف التسويق (المليون) كبديل
        if not target_email:
            target_email = load_and_pop_email(FILE_MARKETING)
            type_tag = "تسويق نون (بديل) 💰"

        if target_email:
            msg['To'] = target_email
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            try:
                server.send_message(msg)
                print(f"✅ [{i+1}/200] أرسل ({type_tag}) إلى: {target_email}")
            except Exception as e:
                print(f"❌ خطأ مع {target_email}: {e}")
            
            # وقت انتظار ذكي (45-90 ثانية)
            time.sleep(random.randint(45, 90))
        else:
            print("⚠️ لا توجد إيميلات متبقية في أي ملف!")
            break

    server.quit()
    print("🏁 انتهت الـ 200 رسالة بنجاح وتم تحديث الملفات.")

if __name__ == "__main__":
    run_triple_rotation_bot()
