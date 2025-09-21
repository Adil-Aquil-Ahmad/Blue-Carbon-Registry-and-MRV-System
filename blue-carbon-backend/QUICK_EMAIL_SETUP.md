# 📧 Manual Email Configuration Guide
# Blue Carbon Services Portal

## Quick Setup Options:

### Option 1: 🤖 Automated Setup (Recommended)
```bash
cd blue-carbon-backend
python setup_email.py
```

### Option 2: ✏️ Manual Configuration

#### For Gmail:
1. **Generate App Password:**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification (if not already)
   - Click "App passwords" 
   - Select "Mail" → Generate password
   - Copy the 16-character password

2. **Update email_config.py:**
```python
SENDER_EMAIL = "your-email@gmail.com"           # Your Gmail address
SENDER_PASSWORD = "abcd efgh ijkl mnop"         # 16-character app password
```

#### For Outlook/Hotmail:
```python
SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@outlook.com"
SENDER_PASSWORD = "your_password"
```

#### For Yahoo:
```python
SMTP_SERVER = "smtp.mail.yahoo.com" 
SMTP_PORT = 587
SENDER_EMAIL = "your-email@yahoo.com"
SENDER_PASSWORD = "your_app_password"
```

#### For Custom SMTP:
```python
SMTP_SERVER = "mail.your-domain.com"
SMTP_PORT = 587  # or 465 for SSL
SENDER_EMAIL = "noreply@your-domain.com"
SENDER_PASSWORD = "your_password"
```

## 🧪 Testing Your Setup:

### Test Command:
```bash
cd blue-carbon-backend
python test_email.py
```

### What to expect:
1. Choose test type (registration or password reset)
2. Enter your email for testing
3. Check inbox (and spam folder!)
4. Verify email formatting and links

## 🔧 Troubleshooting:

### "Authentication Failed":
- ✅ Check email/password are correct
- ✅ For Gmail: Use App Password, not regular password
- ✅ Enable 2-factor authentication

### "Connection Refused": 
- ✅ Check SMTP server and port
- ✅ Verify firewall allows outbound port 587
- ✅ Try different SMTP server

### "Email Not Received":
- ✅ Check spam/junk folder first
- ✅ Wait a few minutes for delivery
- ✅ Try sending to different email address
- ✅ Check email provider's sending limits

## 🚀 Ready to Use:

Once configured, your portal will automatically:
- ✅ Send welcome emails to new users
- ✅ Include account details and portal features
- ✅ Provide login links and support information
- ✅ Use professional government styling

## 📞 Need Help?

Run the automated setup script:
```bash
python setup_email.py
```

This will guide you through the entire process step-by-step!