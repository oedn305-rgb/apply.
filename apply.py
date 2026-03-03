import smtplib
import os
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- الإعدادات الشخصية (تأكد من ضبط Secret في GitHub) ---
EMAIL_USER = os.getenv('MY_EMAIL')
EMAIL_PASS = os.getenv('EMAIL_PASS')
MY_NAME = "مشعل المطيري"
NOON_CODE = "MSHL1" 

# --- أسماء ملفاتك الحقيقية في المستودع ---
FILE_MAKKAH = 'makkah_emails.txt'     # وظائف مكة
FILE_OLD = 'all_emails.txt'          # الوظائف القديمة
FILE_MARKETING = 'million_emails.txt' # التسويق الذكي (الـ 47 دفعة)
CV_FILE_PATH = "cv.pdf.pdf"          # ملف السيرة الذاتية

def get_guaranteed_sale_content(email):
    """محرك الإقناع: يربط الشخص بمنتج ورسالة تضمن الشراء 100%"""
    email = email.lower()
    
    # 1. الأطباء والكوادر الصحية (الراحة والوقت)
    if any(x in email for x in ['health', 'moh', 'doctor', 'hospital', 'nurse', 'medical']):
        subject = "🩺 دكتور/ة، راحة قدميك خلال 'شفت' العمل الطويل (كود MSHL1)"
        body = (f"أهلاً بك يا بطل الصحة،\n\n"
                f"نعلم أن وقوفك لساعات طويلة يرهق قدميك ويؤثر على تركيزك. اخترنا لك حذاء Skechers الطبي الأكثر مبيعاً في نون، المصمم لراحة فائقة وامتصاص الصدمات.\n\n"
                f"🛍️ المنتج المقترح: أحذية سكيتشرز (Skechers) الطبية.\n"
                f"💰 كود الخصم (تقديراً لجهودكم): {NOON_CODE}\n"
                f"🔗 اطلبه الآن لراحتك: https://www.noon.com/saudi-ar/p-10923")

    # 2. الموظفين الماليين والمدراء (الفخامة والانطباع الأول)
    elif any(x in email for x in ['bank', 'rajhi', 'alinma', 'pif', 'pwc', 'finance', 'tadawul']):
        subject = "💼 عطر النيش الذي يسبق حضورك في اجتماعاتك (خصم MSHL1)"
        body = (f"تحية طيبة،\n\n"
                f"في عالم الأعمال، انطباعك الأول هو مفتاح نجاحك. عطر 'ديور ساواج' أو عطور النيش العالمية هي رفيقك المثالي للتميز.\n"
                f"احصل على الفخامة التي تليق بمقامك بخصم إضافي حصري لمنسوبي القطاع.\n\n"
                f"🛍️ المنتج المقترح: أرقى عطور النيش وساعات الماركات.\n"
                f"💰 كود البرستيج: {NOON_CODE}\n"
                f"🔗 تسوق الفخامة بذكاء: https://www.noon.com/saudi-ar/p-12345")

    # 3. المهندسين والفنيين (البطارية والتحمل في الميدان)
    elif any(x in email for x in ['sabic', 'aramco', 'maaden', 'eng', 'tech', 'se.com', 'acwa']):
        subject = "🔋 مهندسنا، لا تترك جوالك يخذلُك في قلب الموقع (كود MSHL1)"
        body = (f"أهلاً بك يا بطل الميدان،\n\n"
                f"العمل الميداني يتطلب طاقة لا تنتهي. شاحن Anker المتنقل بقوة 20,000mAh هو المنقذ لجوالك وأجهزتك في المواقع البعيدة والمشاريع الكبرى.\n\n"
                f"🛍️ المنتج المقترح: شاحن أنكر (Powercore) المعتمد.\n"
                f"💰 كود التوفير الميداني: {NOON_CODE}\n"
                f"🔗 اطلب سلاحك التقني: https://www.noon.com/saudi-ar/p-67890")

    # 4. الطلاب والأكاديميين (الإنجاز والتركيز)
    elif any(x in email for x in ['edu.sa', 'ksu', 'kau', 'pnu', 'university', 'tvtc']):
        subject = "☕️ رفيق ليالي المذاكرة: قهوتك المختصة في غرفتك (MSHL1)"
        body = (f"أهلاً بك،\n\n"
                f"لماذا تضيع وقتك في المقاهي؟ ماكينة Delonghi Dedica هي الحل لإعداد كوب الإسبريسو المثالي لبداية يوم مليء بالتركيز والتحصيل العلمي.\n\n"
                f"🛍️ المنتج المقترح: ماكينة ديلونجي ديديكا الأصلية.\n"
                f"💰 كود الطالب والمحاضر: {NOON_CODE}\n"
                f"🔗 اطلبها وابدأ الإبداع: https://www.noon.com/saudi-ar/p-11223")

    # 5. الرسالة العامة القوية (بقية الملف - استهداف منزلي)
    else:
        subject = "🏠 وفّري وقتك ومجهودك مع المكنسة اللاسلكية الذكية (MSHL1)"
        body = (f"أهلاً بك،\n\n"
                f"التنظيف اليومي لا يجب أن يكون متعباً. مكنسة شاومي اللاسلكية تصل لأصعب الأماكن وتوفر عليك ساعات من الجهد بمميزات ذكية.\n\n"
                f"🛍️ المنتج المقترح: مكنسة شاومي اللاسلكية (G10).\n"
                f"💰 كود التوفير المنزلي: {NOON_CODE}\n"
                f"🔗 تسوقي بذكاء الآن: https://www.noon.com/saudi-ar/p-44556")

    return subject, body

def load_and_pop_email(file_path):
    """يقرأ الإيميل ويمسحه من الملف لمنع التكرار"""
    if not os.path.exists(file_path): return None
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if not lines: return None
    target_email = lines[0].strip()
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines[1:])
    return target_email

def run_triple_rotation_bot():
    if not EMAIL_USER or not EMAIL_PASS:
        print("❌ خطأ: لم يتم ضبط بيانات الإيميل في Variables!")
        return

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(EMAIL_USER, EMAIL_PASS)

    print("🚀 بدء الإرسال الذكي لـ 200 رسالة...")

    for i in range(200):
        msg = MIMEMultipart()
        msg['From'] = f"{MY_NAME} <{EMAIL_USER}>"
        step = i % 3
        target_email = None

        # الروتيشن الثلاثي
        if step == 0:
            target_email = load_and_pop_email(FILE_MAKKAH)
            if target_email:
                msg['Subject'] = f"طلب عمل ميداني بمكة - {MY_NAME}"
                body = f"السلام عليكم، معكم {MY_NAME}، أبحث عن فرصة عمل بمكة المكرمة. التواصل: 0552145971"
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
                msg['Subject'] = f"استفسار عن فرص تعاون - {MY_NAME}"
                body = f"تحية طيبة، أنا {MY_NAME}، مهتم بالعمل معكم في مشاريعكم القائمة. رقم التواصل: 0552145971"

        else:
            target_email = load_and_pop_email(FILE_MARKETING)
            if target_email:
                msg['Subject'], body = get_guaranteed_sale_content(target_email)

        if target_email:
            msg['To'] = target_email
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            try:
                server.send_message(msg)
                print(f"✅ [{i+1}/200] تم الإرسال إلى: {target_email}")
            except Exception as e:
                print(f"❌ فشل مع {target_email}: {e}")
            
            # وقت انتظار عشوائي لمنع الحظر (45-90 ثانية)
            time.sleep(random.randint(45, 90))
        else:
            print("⚠️ انتهت الإيميلات في الملفات.")
            break

    server.quit()
    print("🏁 مهمة اليوم انتهت بنجاح!")

if __name__ == "__main__":
    run_triple_rotation_bot()
