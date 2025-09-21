#!/usr/bin/env python3
"""
Interactive Email Configuration Setup
Blue Carbon Services Portal

This script helps you configure email settings interactively.
"""

import os
import sys

def print_header():
    print("=" * 60)
    print("🌊 Blue Carbon Services Portal")
    print("📧 Email Configuration Setup")
    print("=" * 60)

def gmail_setup_guide():
    print("\n📱 Gmail Setup Guide:")
    print("1. Go to: https://myaccount.google.com/")
    print("2. Click 'Security' in the left sidebar")
    print("3. Under 'Signing in to Google', click '2-Step Verification'")
    print("4. If not enabled, enable 2-Step Verification")
    print("5. Scroll down and click 'App passwords'")
    print("6. Select 'Mail' and your device")
    print("7. Google will generate a 16-character password")
    print("8. Copy this password (you'll need it below)")
    print("\n" + "⚠️ IMPORTANT: Use the 16-character App Password, NOT your regular Gmail password!")

def other_smtp_guide():
    print("\n🌐 Other Email Providers:")
    print("• Outlook: smtp-mail.outlook.com:587")
    print("• Yahoo: smtp.mail.yahoo.com:587") 
    print("• Custom: Contact your hosting provider")

def get_email_config():
    print("\n📝 Enter Your Email Configuration:")
    
    # Get email provider choice
    print("\nChoose your email provider:")
    print("1. Gmail (recommended)")
    print("2. Outlook/Hotmail")
    print("3. Yahoo")
    print("4. Other (custom SMTP)")
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        print("✅ Gmail selected")
        gmail_setup_guide()
    elif choice == "2":
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587
        print("✅ Outlook selected")
    elif choice == "3":
        smtp_server = "smtp.mail.yahoo.com"
        smtp_port = 587
        print("✅ Yahoo selected")
    elif choice == "4":
        smtp_server = input("Enter SMTP server (e.g., mail.yourhost.com): ").strip()
        smtp_port = int(input("Enter SMTP port (usually 587): ").strip() or "587")
        print("✅ Custom SMTP selected")
    else:
        print("❌ Invalid choice, defaulting to Gmail")
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
    
    # Get email credentials
    sender_email = input(f"\nEnter your email address: ").strip()
    
    if not sender_email:
        print("❌ Email address is required!")
        return None
    
    print(f"\nFor {sender_email}:")
    if choice == "1":
        print("⚠️ Enter your 16-character App Password (NOT your regular password)")
    
    sender_password = input("Enter your email password/app password: ").strip()
    
    if not sender_password:
        print("❌ Password is required!")
        return None
    
    # Get sender name
    sender_name = input("Enter sender name (default: Blue Carbon Services Portal): ").strip()
    if not sender_name:
        sender_name = "Blue Carbon Services Portal"
    
    return {
        'smtp_server': smtp_server,
        'smtp_port': smtp_port,
        'sender_email': sender_email,
        'sender_password': sender_password,
        'sender_name': sender_name
    }

def update_config_file(config):
    """Update the email_config.py file with new settings"""
    config_file = "email_config.py"
    
    try:
        # Read current config
        with open(config_file, 'r') as f:
            content = f.read()
        
        # Replace values
        content = content.replace(
            'SMTP_SERVER = "smtp.gmail.com"',
            f'SMTP_SERVER = "{config["smtp_server"]}"'
        )
        content = content.replace(
            'SMTP_PORT = 587',
            f'SMTP_PORT = {config["smtp_port"]}'
        )
        content = content.replace(
            'SENDER_EMAIL = "bluecarbon.noreply@gov.in"',
            f'SENDER_EMAIL = "{config["sender_email"]}"'
        )
        content = content.replace(
            'SENDER_PASSWORD = "your_app_password_here"',
            f'SENDER_PASSWORD = "{config["sender_password"]}"'
        )
        content = content.replace(
            'SENDER_NAME = "Blue Carbon Services Portal"',
            f'SENDER_NAME = "{config["sender_name"]}"'
        )
        
        # Write updated config
        with open(config_file, 'w') as f:
            f.write(content)
        
        print(f"✅ Configuration updated in {config_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating config file: {e}")
        return False

def test_email_config():
    """Offer to test the email configuration"""
    test = input("\n🧪 Would you like to test your email configuration? (y/n): ").strip().lower()
    
    if test in ['y', 'yes']:
        print("\n🚀 Starting email test...")
        print("Run this command to test: python test_email.py")
        
        # Try to run the test automatically
        try:
            import subprocess
            result = subprocess.run([sys.executable, "test_email.py"], 
                                 capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print("✅ Test script executed successfully")
            else:
                print(f"⚠️ Test script output: {result.stdout}")
                print(f"⚠️ Test script errors: {result.stderr}")
        except Exception as e:
            print(f"⚠️ Could not run test automatically: {e}")
            print("Please run manually: python test_email.py")

def main():
    print_header()
    
    # Check if we're in the right directory
    if not os.path.exists("email_config.py"):
        print("❌ Error: email_config.py not found!")
        print("Please run this script from the blue-carbon-backend directory")
        return
    
    print("This script will help you configure email settings for the portal.")
    print("You'll need access to your email account settings.")
    
    proceed = input("\n📧 Ready to configure email? (y/n): ").strip().lower()
    
    if proceed not in ['y', 'yes']:
        print("Setup cancelled.")
        return
    
    # Get configuration
    config = get_email_config()
    
    if not config:
        print("❌ Configuration failed!")
        return
    
    # Show summary
    print("\n📋 Configuration Summary:")
    print(f"SMTP Server: {config['smtp_server']}:{config['smtp_port']}")
    print(f"Email: {config['sender_email']}")
    print(f"Sender Name: {config['sender_name']}")
    print(f"Password: {'*' * len(config['sender_password'])}")
    
    confirm = input("\n✅ Save this configuration? (y/n): ").strip().lower()
    
    if confirm in ['y', 'yes']:
        if update_config_file(config):
            print("\n🎉 Email configuration completed successfully!")
            print("\nNext steps:")
            print("1. Test your configuration: python test_email.py")
            print("2. Start your backend server: python main.py")
            print("3. Register a test user to see the welcome email")
            
            test_email_config()
        else:
            print("❌ Failed to save configuration")
    else:
        print("Configuration not saved.")

if __name__ == "__main__":
    main()