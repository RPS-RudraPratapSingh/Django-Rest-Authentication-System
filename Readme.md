# Authentication API

A Django REST Framework–based authentication system with email OTP verification and session-based login.

## Features
- User signup with email OTP verification
- Secure password storage
- Session-based authentication (30-day expiry)
- Who-am-I endpoint for fetching logged-in user info
- Detailed error messages and `success` boolean responses

---

## 🚀 Deployment Guide

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
2. Create a Virtual Environment
Project originally created with Python 3.13.5.

Windows (PowerShell)
powershell
Copy
Edit
python -m venv venv
.\venv\Scripts\activate
macOS / Linux
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Set Up Environment Variables
Create a file named .env.local in the root directory:

ini
Copy
Edit
Email_User=your_host_email_id
Email_Pass="your_google_app_password"
SECURITY_KEY=your_django_secret_key
5. Run the Server
Windows
powershell
Copy
Edit
python backend/manage.py runserver
macOS / Linux
bash
Copy
Edit
python3 backend/manage.py runserver
📡 API Usage
1. Request OTP for Signup
Endpoint: POST /users/signup/
Body (JSON):

json
Copy
Edit
{
  "username": "example_user",
  "email": "example@example.com"
}
Response:

success: true if OTP sent

success: false with detail if error

2. Verify OTP & Create Account
Endpoint: POST /users/signup/
Body (JSON):

json
Copy
Edit
{
  "username": "example_user",
  "email": "example@example.com",
  "password": "secure_password",
  "otp": "123456"
}
3. Login
Endpoint: POST /users/login/
Body (JSON):

json
Copy
Edit
{
  "username": "example_user",
  "password": "secure_password"
}
Notes:

Stores user token in session

Session ID stored in cookies for persistent login (expires after 30 days)

4. Who Am I
Endpoint: GET /users/who_a_i/
Response:

403 if not logged in

JSON object with username and email if logged in:

json
Copy
Edit
{
  "username": "example_user",
  "email": "example@example.com"
}
👨‍💻 Developer Guide
Framework: Django, Django REST Framework

Auth Method: Session-based

Email Service: SMTP with Google App Password

Environment Variables: .env.local for sensitive credentials

Security: All sensitive values loaded from environment variables

