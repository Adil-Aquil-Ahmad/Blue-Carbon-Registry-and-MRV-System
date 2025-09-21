# Email Functionality Setup Guide
# Blue Carbon Services Portal

## 🚀 Quick Setup

The email functionality is now integrated into your Blue Carbon Services Portal! Here's what happens:

### ✅ What's Already Working:
1. **Automatic Welcome Emails**: When users register, they receive a beautifully formatted welcome email
2. **Password Reset Emails**: Users can request password resets via email
3. **Professional Templates**: Government-style email templates with Blue Carbon branding
4. **Error Handling**: Email failures won't break user registration

### 📧 Email Configuration Setup:

#### Step 1: Update Email Credentials
Edit `email_config.py` file:

```python
# Replace these with your actual email settings:
SENDER_EMAIL = "your-email@gmail.com"  # Your email address
SENDER_PASSWORD = "your_app_password"  # Your app password (see below)
```

#### Step 2: Gmail Setup (Recommended)
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click "Security" → "2-Step Verification" → Enable it
3. Go to "App passwords" → Generate password for "Mail"
4. Use the 16-character password in `SENDER_PASSWORD`

#### Step 3: Test Email Functionality
```bash
cd blue-carbon-backend
python test_email.py
```

### 🔧 What Happens During Registration:

1. User fills registration form
2. Account is created in database
3. **NEW**: Welcome email is automatically sent
4. User receives professional email with:
   - Account confirmation
   - Login instructions
   - Portal features overview
   - Support contact information
   - Government branding

### 📧 Email Templates Include:

#### Welcome Email Features:
- **Professional Government Design** with Blue Carbon branding
- **Account Details** (username, email, role, organization)
- **Portal Features Overview** (project registration, MRV tools, etc.)
- **Quick Links** to login, help, and documentation
- **Support Information** with contact details
- **Security Information** and next steps

#### Password Reset Email Features:
- **Secure Reset Links** with expiration
- **Security Warnings** about link sharing
- **Professional Government Styling**
- **Clear Instructions** for password reset

### 🛠️ Technical Details:

#### Files Added/Modified:
1. `services/email_service.py` - Email sending functionality
2. `email_config.py` - Configuration settings
3. `services/auth.py` - Modified to send emails after registration
4. `test_email.py` - Test script for email functionality
5. `requirements.txt` - Updated dependencies

#### Email Security:
- Uses TLS encryption for secure email transmission
- App passwords instead of regular passwords
- Error handling to prevent registration failures
- No sensitive information in email logs

### 🔍 Troubleshooting:

#### If Emails Aren't Sending:
1. **Check email configuration** in `email_config.py`
2. **Verify app password** is generated correctly
3. **Check spam folder** for test emails
4. **Run test script**: `python test_email.py`
5. **Check firewall** allows outbound connections on port 587

#### Common Issues:
- **"Authentication failed"**: Wrong email/password
- **"Connection refused"**: Firewall blocking or wrong SMTP server
- **"Email not received"**: Check spam folder first

#### For Other Email Providers:
- **Outlook**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **Custom SMTP**: Contact your hosting provider

### 🌐 Production Deployment:

#### Environment Variables (Recommended):
```bash
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SENDER_EMAIL="bluecarbon.noreply@gov.in"
export SENDER_PASSWORD="your_app_password"
export FRONTEND_BASE_URL="https://your-domain.com"
```

#### Security Best Practices:
1. Use environment variables for credentials
2. Generate dedicated app passwords
3. Monitor email sending logs
4. Set up email rate limiting if needed
5. Use official government email addresses in production

### 📞 Support:

If you need help setting up email functionality:
1. Run the test script: `python test_email.py`
2. Check the troubleshooting section above
3. Verify your email provider's SMTP settings
4. Ensure 2-factor authentication is enabled for Gmail

The email system is designed to be robust - if email sending fails, user registration will still succeed, and an error will be logged for administrator review.

### 🎉 You're All Set!

Your Blue Carbon Services Portal now automatically sends professional welcome emails to new users, enhancing the user experience and providing them with important getting-started information!