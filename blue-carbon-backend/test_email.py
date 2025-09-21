#!/usr/bin/env python3
"""
Email Test Script for Blue Carbon Services Portal

This script tests the email functionality without creating actual user accounts.
Run this to verify your email configuration is working correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.email_service import email_service
from email_config import *

def test_email_configuration():
    """Test basic email configuration"""
    print("🧪 Testing Email Configuration...")
    print(f"SMTP Server: {SMTP_SERVER}:{SMTP_PORT}")
    print(f"Sender Email: {SENDER_EMAIL}")
    print(f"Frontend URL: {FRONTEND_BASE_URL}")
    print()

def test_registration_email():
    """Test registration confirmation email"""
    print("📧 Testing Registration Confirmation Email...")
    
    # Test email address (replace with your email for testing)
    test_email = input("Enter your email address for testing: ").strip()
    
    if not test_email:
        print("❌ No email provided. Skipping test.")
        return False
    
    try:
        success = email_service.send_registration_confirmation(
            user_email=test_email,
            username="TestUser123",
            role="ngo",
            organization_name="Test Marine Conservation NGO"
        )
        
        if success:
            print(f"✅ Registration email sent successfully to {test_email}")
            print("Check your inbox (and spam folder) for the welcome email.")
            return True
        else:
            print(f"❌ Failed to send registration email to {test_email}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending registration email: {str(e)}")
        return False

def test_password_reset_email():
    """Test password reset email"""
    print("\n🔐 Testing Password Reset Email...")
    
    test_email = input("Enter your email address for testing: ").strip()
    
    if not test_email:
        print("❌ No email provided. Skipping test.")
        return False
    
    try:
        # Generate a fake reset token for testing
        fake_token = "test_reset_token_123456789"
        
        success = email_service.send_password_reset(
            user_email=test_email,
            username="TestUser123",
            reset_token=fake_token
        )
        
        if success:
            print(f"✅ Password reset email sent successfully to {test_email}")
            print("Check your inbox (and spam folder) for the reset email.")
            return True
        else:
            print(f"❌ Failed to send password reset email to {test_email}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending password reset email: {str(e)}")
        return False

def main():
    """Run all email tests"""
    print("=" * 60)
    print("🌊 Blue Carbon Services Portal - Email Test Suite")
    print("=" * 60)
    
    # Test configuration
    test_email_configuration()
    
    # Check if email credentials are configured
    if SENDER_PASSWORD == "your_app_password_here":
        print("⚠️  WARNING: Email credentials not configured!")
        print("Please update email_config.py with your actual email settings.")
        print("\nFor Gmail:")
        print("1. Enable 2-factor authentication")
        print("2. Generate an App Password")
        print("3. Update SENDER_EMAIL and SENDER_PASSWORD in email_config.py")
        print()
        return
    
    print("Choose test to run:")
    print("1. Registration confirmation email")
    print("2. Password reset email")
    print("3. Both tests")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        test_registration_email()
    elif choice == "2":
        test_password_reset_email()
    elif choice == "3":
        print("Running both tests...\n")
        test_registration_email()
        test_password_reset_email()
    elif choice == "4":
        print("Exiting...")
    else:
        print("❌ Invalid choice!")
    
    print("\n" + "=" * 60)
    print("✅ Email testing completed!")
    print("If emails are not received, check:")
    print("- Email credentials in email_config.py")
    print("- Spam/junk folder")
    print("- Firewall settings")
    print("- SMTP server connectivity")
    print("=" * 60)

if __name__ == "__main__":
    main()