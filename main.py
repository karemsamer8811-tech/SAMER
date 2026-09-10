import os
import requests
from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "hohosbid_super_secret_key")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "https://samer-production.up.railway.app/auth/callback"

MEDIAFIRE_URL = "https://www.mediafire.com/file/61ugass1zqpavlm/Hide_Online_v4.9.50_Mod__40_Updated__41_.apk/file"


@app.route("/")
def home():
  # رابط تسجيل الدخول التابع لجوجل
  google_login_url = (
      f"https://accounts.google.com/o/oauth2/v2/auth?client_id={GOOGLE_CLIENT_ID}"
      f"&redirect_uri={REDIRECT_URI}&response_type=code&scope=email%20profile"
  )

  return render_template_string(f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول بواسطة جوجل</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: Tahoma, sans-serif; }}
        body {{ background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; width: 100vw; padding: 20px; }}
        .login-container {{ background: #fff; width: 100%; max-width: 420px; padding: 40px 30px; border-radius: 16px; box-shadow: 0 4px 25px rgba(0,0,0,0.1); display: flex; flex-direction: column; align-items: center; }}
        h2 {{ margin-bottom: 30px; color: #1c1e21; font-size: 22px; text-align: center; font-weight: bold; }}
        .google-btn {{ width: 100%; padding: 15px; background: #4285F4; color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; display: flex; justify-content: center; align-items: center; text-decoration: none; gap: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }}
        .google-btn:hover {{ background: #357ae8; }}
    </style>
</head>
<body>
    <div class="login-container">
        <h2>تحميل لعبة Hide Online المهكرة</h2>
        <a href="{google_login_url}" class="google-btn">
            <span>تسجيل الدخول بحساب جوجل</span>
        </a>
    </div>
</body>
</html>
""")


@app.route("/auth/callback")
def auth_callback():
  code = request.args.get("code")
  if not code:
    return "فشل جلب رمز الوصول من جوجل"

  token_url = "https://oauth2.googleapis.com/token"
  payload = {
      "code": code,
      "client_id": GOOGLE_CLIENT_ID,
      "client_secret": GOOGLE_CLIENT_SECRET,
      "redirect_uri": REDIRECT_URI,
      "grant_type": "authorization_code",
  }

  response = requests.post(token_url, data=payload)

  if response.status_code != 200:
    return "فشل جلب رمز الوصول من جوجل"

  token_data = response.json()
  access_token = token_data.get("access_token")

  if not access_token:
    return "فشل جلب رمز الوصول من جوجل"

  # توجيه المستخدم مباشرة إلى رابط ملف التحميل بعد نجاح المصادقة
  return redirect(MEDIAFIRE_URL)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
