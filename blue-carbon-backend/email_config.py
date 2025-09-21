# Email Configuration for Blue Carbon Services Portal
# Update these settings according to your email provider

# SMTP Server Configuration
SMTP_SERVER = "smtp.gmail.com"  # Gmail SMTP server
SMTP_PORT = 587  # TLS port
USE_TLS = True

# Email Credentials
# For Gmail, use an "App Password" instead of your regular password
# Generate App Password: Google Account > Security > 2-Step Verification > App passwords
SENDER_EMAIL = "prabhdeep1701@gmail.com"  # Replace with your actual email
SENDER_PASSWORD = "miys azfg zzkm nrrq"  # Replace with your app password
SENDER_NAME = "Team Zylose"

# Frontend URLs (update these if your app runs on different ports/domains)
FRONTEND_BASE_URL = "http://localhost:3000"
LOGIN_URL = f"{FRONTEND_BASE_URL}/auth/login"
RESET_PASSWORD_URL = f"{FRONTEND_BASE_URL}/auth/reset-password"
HELP_URL = f"{FRONTEND_BASE_URL}/help"
ABOUT_URL = f"{FRONTEND_BASE_URL}/about"
TERMS_URL = f"{FRONTEND_BASE_URL}/terms"
CONTACT_URL = f"{FRONTEND_BASE_URL}/contact"

# Support Contact Information
SUPPORT_EMAIL = "bluecarbon.help@gov.in"
SUPPORT_PHONE = "1800-XXX-XXXX"

# Email Templates Configuration
EMAIL_TEMPLATES = {
    "registration": {
        "subject": "Welcome to Blue Carbon Services Portal - Registration Successful",
        "from_name": "Blue Carbon Services Portal"
    },
    "password_reset": {
        "subject": "Blue Carbon Services Portal - Password Reset Request",
        "from_name": "Blue Carbon Services Portal"
    },
    "verification": {
        "subject": "Blue Carbon Services Portal - Email Verification Required",
        "from_name": "Blue Carbon Services Portal"
    }
}

# Government Information
GOVT_MINISTRY = "Ministry of Environment, Forest and Climate Change"
GOVT_ORGANIZATION = "Government of India"
DEVELOPER_ORG = "National Informatics Centre (NIC)"

# Logo and Branding
LOGO_URL = f"{FRONTEND_BASE_URL}/logo_1.png"
PORTAL_NAME = "Blue Carbon Services Portal"

# Email Security Settings
EMAIL_TIMEOUT = 30  # seconds
MAX_RETRY_ATTEMPTS = 3

# Environment specific settings
import os

# Override with environment variables if available
SMTP_SERVER = os.getenv("SMTP_SERVER", SMTP_SERVER)
SMTP_PORT = int(os.getenv("SMTP_PORT", SMTP_PORT))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", SENDER_EMAIL)
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", SENDER_PASSWORD)
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", FRONTEND_BASE_URL)

# Instructions for Setup:
# 1. For Gmail: Enable 2-factor authentication and generate an App Password
# 2. For other providers: Update SMTP_SERVER and SMTP_PORT accordingly
# 3. Update SENDER_EMAIL and SENDER_PASSWORD with your credentials
# 4. Ensure firewall allows outbound connections on the SMTP port
# 5. Test email sending with a simple test script before deployment

"""
Quick Setup Guide for Gmail:

1. Go to Google Account settings (https://myaccount.google.com/)
2. Select "Security" from the left panel
3. Under "Signing in to Google", select "2-Step Verification"
4. Enable 2-Step Verification if not already enabled
5. At the bottom of the page, select "App passwords"
6. Select "Mail" and choose your device
7. Google will generate a 16-character password
8. Use this password in SENDER_PASSWORD above
9. Replace SENDER_EMAIL with your Gmail address

For other email providers:
- Microsoft Outlook: smtp-mail.outlook.com, port 587
- Yahoo Mail: smtp.mail.yahoo.com, port 587
- Custom SMTP: Contact your hosting provider for details
"""