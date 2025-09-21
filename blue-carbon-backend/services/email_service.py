import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
import os
from datetime import datetime
from email_config import *

class EmailService:
    def __init__(self):
        # Email configuration from config file
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.sender_email = SENDER_EMAIL
        self.sender_password = SENDER_PASSWORD
        self.sender_name = SENDER_NAME
        self.use_tls = USE_TLS
        
    def send_email(self, to_email: str, subject: str, html_content: str, text_content: str = None) -> bool:
        """Send an email to the specified recipient"""
        try:
            # Create message container
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.sender_name} <{self.sender_email}>"
            message["To"] = to_email
            
            # Create the plain-text and HTML version of your message
            if text_content:
                text_part = MIMEText(text_content, "plain")
                message.attach(text_part)
            
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, message.as_string())
            
            return True
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            return False
    
    def send_registration_confirmation(self, user_email: str, username: str, role: str, organization_name: str = None) -> bool:
        """Send registration confirmation email"""
        subject = "Welcome to Blue Carbon Services Portal - Registration Successful"
        
        # HTML email template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to Blue Carbon Services Portal</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
                    color: white;
                    padding: 30px 20px;
                    text-align: center;
                    border-radius: 8px 8px 0 0;
                }}
                .logo {{
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }}
                .content {{
                    background: #ffffff;
                    padding: 30px;
                    border: 1px solid #e5e7eb;
                    border-radius: 0 0 8px 8px;
                }}
                .welcome-box {{
                    background: #f0f9ff;
                    border: 1px solid #bfdbfe;
                    border-radius: 8px;
                    padding: 20px;
                    margin: 20px 0;
                }}
                .info-grid {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                    margin: 20px 0;
                }}
                .info-item {{
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 6px;
                    border-left: 4px solid #1e3a8a;
                }}
                .info-label {{
                    font-weight: bold;
                    color: #1e3a8a;
                    font-size: 14px;
                }}
                .info-value {{
                    color: #374151;
                    margin-top: 5px;
                }}
                .features {{
                    background: #f9fafb;
                    border-radius: 8px;
                    padding: 20px;
                    margin: 20px 0;
                }}
                .feature-list {{
                    list-style: none;
                    padding: 0;
                }}
                .feature-list li {{
                    padding: 8px 0;
                    border-bottom: 1px solid #e5e7eb;
                }}
                .feature-list li:before {{
                    content: "✓";
                    color: #10b981;
                    font-weight: bold;
                    margin-right: 10px;
                }}
                .cta-button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #10b981, #059669);
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .footer {{
                    background: #374151;
                    color: #9ca3af;
                    padding: 20px;
                    text-align: center;
                    font-size: 14px;
                    margin-top: 30px;
                    border-radius: 8px;
                }}
                .footer-links {{
                    margin: 15px 0;
                }}
                .footer-links a {{
                    color: #93c5fd;
                    text-decoration: none;
                    margin: 0 10px;
                }}
                .govt-seal {{
                    text-align: center;
                    margin: 20px 0;
                    padding: 15px;
                    background: #fef7ed;
                    border: 1px solid #fed7aa;
                    border-radius: 8px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo">🌊 Blue Carbon Services Portal</div>
                <div>Government of India | Ministry of Environment, Forest and Climate Change</div>
            </div>
            
            <div class="content">
                <h2 style="color: #1e3a8a; margin-top: 0;">Welcome to Blue Carbon Services Portal!</h2>
                
                <p>Dear <strong>{username}</strong>,</p>
                
                <div class="welcome-box">
                    <h3 style="color: #1e3a8a; margin-top: 0;">🎉 Registration Successful!</h3>
                    <p>Your account has been successfully created on the Blue Carbon Services Portal. You are now part of India's premier platform for marine ecosystem conservation and blue carbon initiatives.</p>
                </div>
                
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">Username</div>
                        <div class="info-value">{username}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Email</div>
                        <div class="info-value">{user_email}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Role</div>
                        <div class="info-value">{role.replace('_', ' ').title()}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Registration Date</div>
                        <div class="info-value">{datetime.now().strftime("%B %d, %Y")}</div>
                    </div>
                </div>
                
                {f'''
                <div class="info-item" style="grid-column: 1 / -1; margin-top: 15px;">
                    <div class="info-label">Organization</div>
                    <div class="info-value">{organization_name}</div>
                </div>
                ''' if organization_name else ''}
                
                <div class="features">
                    <h4 style="color: #1e3a8a; margin-top: 0;">🚀 What You Can Do Now:</h4>
                    <ul class="feature-list">
                        <li>Register and manage blue carbon projects</li>
                        <li>Access MRV (Monitoring, Reporting, Verification) tools</li>
                        <li>Submit carbon stock assessments and monitoring data</li>
                        <li>Connect with marine conservation experts</li>
                        <li>Access government services and documentation</li>
                        <li>Participate in community-driven conservation initiatives</li>
                        <li>Track and manage carbon credits</li>
                        <li>Access training and capacity building resources</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{LOGIN_URL}" class="cta-button">
                        🔑 Login to Your Account
                    </a>
                </div>
                
                <div class="govt-seal">
                    <strong>🏛️ Government of India Initiative</strong><br>
                    <span style="font-size: 14px;">This portal is developed by National Informatics Centre (NIC) in collaboration with the Ministry of Environment, Forest and Climate Change for promoting blue carbon initiatives across India's coastal regions.</span>
                </div>
                
                <div style="background: #fef3c7; border: 1px solid #fcd34d; border-radius: 8px; padding: 15px; margin: 20px 0;">
                    <h4 style="color: #92400e; margin-top: 0;">📋 Next Steps:</h4>
                    <ol style="color: #92400e; margin: 10px 0;">
                        <li>Complete your profile with additional details</li>
                        <li>Verify your organization credentials (if applicable)</li>
                        <li>Explore the services and documentation available</li>
                        <li>Join upcoming training sessions and workshops</li>
                    </ol>
                </div>
                
                <div style="background: #ecfdf5; border: 1px solid #bbf7d0; border-radius: 8px; padding: 15px; margin: 20px 0;">
                    <h4 style="color: #047857; margin-top: 0;">🆘 Need Help?</h4>
                    <p style="color: #047857; margin: 10px 0;">Our support team is here to help you get started:</p>
                    <ul style="color: #047857;">
                        <li>📧 Email: <a href="mailto:{SUPPORT_EMAIL}" style="color: #047857;">{SUPPORT_EMAIL}</a></li>
                        <li>📞 Helpline: {SUPPORT_PHONE} (Toll Free)</li>
                        <li>🌐 Help Center: <a href="{HELP_URL}" style="color: #047857;">Visit Help Section</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer">
                <div><strong>Blue Carbon Services Portal</strong></div>
                <div>Government of India | National Informatics Centre (NIC)</div>
                <div class="footer-links">
                    <a href="{ABOUT_URL}">About Us</a> |
                    <a href="{HELP_URL}">Help</a> |
                    <a href="{TERMS_URL}">Terms & Conditions</a> |
                    <a href="{CONTACT_URL}">Contact Us</a>
                </div>
                <div style="margin-top: 15px; font-size: 12px;">
                    This is an automated email. Please do not reply to this message.<br>
                    If you did not create this account, please contact our support team immediately.
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_content = f"""
        Welcome to Blue Carbon Services Portal!
        
        Dear {username},
        
        Your account has been successfully created on the Blue Carbon Services Portal.
        
        Account Details:
        - Username: {username}
        - Email: {user_email}
        - Role: {role.replace('_', ' ').title()}
        - Registration Date: {datetime.now().strftime("%B %d, %Y")}
        {f"- Organization: {organization_name}" if organization_name else ""}
        
        You can now:
        • Register and manage blue carbon projects
        • Access MRV tools and documentation
        • Submit monitoring data and assessments
        • Connect with marine conservation experts
        • Access government services
        
        Login to your account: {LOGIN_URL}
        
        Need help? Contact us:
        Email: {SUPPORT_EMAIL}
        Phone: {SUPPORT_PHONE}
        
        Blue Carbon Services Portal
        Government of India | National Informatics Centre (NIC)
        """
        
        return self.send_email(user_email, subject, html_content, text_content)
    
    def send_password_reset(self, user_email: str, username: str, reset_token: str) -> bool:
        """Send password reset email"""
        subject = "Blue Carbon Services Portal - Password Reset Request"
        
        reset_link = f"{RESET_PASSWORD_URL}?token={reset_token}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #1e3a8a; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #ffffff; padding: 30px; border: 1px solid #e5e7eb; border-radius: 0 0 8px 8px; }}
                .reset-button {{ display: inline-block; background: #dc2626; color: white; padding: 15px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; margin: 20px 0; }}
                .warning {{ background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 15px; margin: 20px 0; color: #991b1b; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🌊 Blue Carbon Services Portal</h2>
                <p>Password Reset Request</p>
            </div>
            
            <div class="content">
                <h3>Password Reset Request</h3>
                <p>Dear <strong>{username}</strong>,</p>
                <p>We received a request to reset your password for your Blue Carbon Services Portal account.</p>
                
                <div style="text-align: center;">
                    <a href="{reset_link}" class="reset-button">Reset Your Password</a>
                </div>
                
                <div class="warning">
                    <strong>⚠️ Security Notice:</strong>
                    <ul>
                        <li>This link will expire in 1 hour for security purposes</li>
                        <li>If you didn't request this reset, please ignore this email</li>
                        <li>Never share this link with anyone</li>
                    </ul>
                </div>
                
                <p>If the button doesn't work, copy and paste this link into your browser:</p>
                <p style="word-break: break-all; background: #f9fafb; padding: 10px; border-radius: 4px;">{reset_link}</p>
                
                <p>If you need assistance, contact our support team at {SUPPORT_EMAIL}</p>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Password Reset Request - Blue Carbon Services Portal
        
        Dear {username},
        
        We received a request to reset your password.
        
        Reset your password by visiting: {reset_link}
        
        This link will expire in 1 hour.
        If you didn't request this reset, please ignore this email.
        
        Need help? Contact: {SUPPORT_EMAIL}
        
        Blue Carbon Services Portal
        Government of India
        """
        
        return self.send_email(user_email, subject, html_content, text_content)

# Create a singleton instance
email_service = EmailService()