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
        "redirect_uri": REDIRECT_URI,  # يجب أن يكون مطابقاً تماماً لما هو في جوجل كونسول
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=payload)
    
    if response.status_code != 200:
        # يمكنك طباعة الخطأ الفعلي للتصحيح: print(response.json())
        return "فشل جلب رمز الوصول من جوجل"

    token_data = response.json()
    access_token = token_data.get("access_token")
    
    # ... بقية كود جلب بيانات المستخدم
