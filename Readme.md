👨‍💻 Developer Guide
1. Overview
This project is a Django REST Framework–based authentication system with:

Custom User model (CustomUser)

Custom Token Authentication stored in sessions

OTP-based email verification before account creation

Session-based authentication that persists for 30 days

The system has four main API endpoints:

/users/signup/ → Requests OTP

/users/verification/ → Verifies OTP & creates user

/users/login/ → Logs in and stores session token

/users/who_am_i/ → Retrieves logged-in user data

2. Project Structure
bash
Copy
Edit
backend/
├── users/
│   ├── views.py               # API views for signup, verification, login, who_am_i
│   ├── models.py               # CustomUser, CustomToken, VerificationTable
│   ├── AuthenticationClass.py  # CustomAuthentication logic
│   ├── PermissionClasses.py    # IsAuthenticated permission
│   ├── urls.py                  # Endpoint routing
│   └── ...
├── manage.py
└── ...
3. Models
CustomUser
Extends AbstractBaseUser

Uses username as the USERNAME_FIELD

Stores email, is_Active, and is_Admin

CustomToken
Extends DRF’s Token

One-to-one relation with CustomUser

Used for session-based token storage

VerificationTable
Temporary table for pending signups

Stores OTP and expiry timestamp

4. Authentication Flow
Signup Request (/users/signup/)
Checks if username/email already exists.

Removes any previous OTPs for the same username/email.

Generates a 6-digit OTP and expiry time (10 minutes).

Saves to VerificationTable.

Sends OTP via email using Django’s send_mail().

Verification (/users/verification/)
Validates email, username, password, otp.

Checks if verification record exists.

Ensures OTP hasn’t expired.

Creates CustomUser, sets password.

Creates CustomToken for the user.

Deletes the verification record.

Login (/users/login/)
Validates username and password.

If valid, retrieves/creates a CustomToken.

Stores token in request.session.

Who Am I (/users/who_am_i/)
Uses CustomAuthentication to check for token in session.

If authenticated, returns username & email.

5. Authentication & Permissions
CustomAuthentication
Checks for "token" in request.session.

Retrieves corresponding CustomToken and returns (user, None) if valid.

Returns None if no token or invalid.

IsAuthenticated
Returns True if request.user is authenticated.

Blocks request otherwise.

6. Session Handling
Tokens are stored in Django sessions, meaning:

Server-side session data is stored in your configured session backend (DB, cache, file).

Clients maintain session state using cookies.

Default session expiry is 30 days (can be changed in settings.py via SESSION_COOKIE_AGE).

7. Email Sending
Uses Django’s built-in send_mail() function.

Requires SMTP configuration in settings.py:

python
Copy
Edit
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("Email_User")
EMAIL_HOST_PASSWORD = os.environ.get("Email_Pass")
8. Environment Variables
All sensitive values are stored in .env.local:

ini
Copy
Edit
Email_User=your_host_email_id
Email_Pass="your_google_app_password"
SECURITY_KEY=your_django_secret_key
9. Error Handling
All error responses follow:

json
Copy
Edit
{
  "success": false,
  "detail": "Error message"
}
Success responses:

json
Copy
Edit
{
  "success": true,
  "detail": "Optional message"
}
10. Extending the System
Custom User Fields: Add more fields to CustomUser and run migrations.

Different Email Providers: Change EMAIL_HOST and credentials.

Token Expiry: Implement expiry by adding a timestamp field in CustomToken.

Switch to JWT: Replace CustomAuthentication with DRF’s JWTAuthentication.

11. Known Limitations
OTP verification is tied to both email and username — if either changes, verification fails.

OTPs are deleted after verification but not after expiry unless requested.

Login endpoint returns 404 for both non-existent users and wrong passwords to prevent user enumeration.