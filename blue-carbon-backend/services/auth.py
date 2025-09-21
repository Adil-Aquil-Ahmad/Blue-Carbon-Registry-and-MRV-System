import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from models.auth_model import User, LoginSession, UserRole
from database import SessionLocal
from services.email_service import email_service

# Configuration
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using SHA-256 with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{password_hash}"
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            salt, stored_hash = hashed_password.split(':')
            password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return password_hash == stored_hash
        except ValueError:
            return False
    
    @staticmethod
    def create_access_token(user_id: int, username: str, role: str) -> str:
        """Create a JWT access token"""
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        payload = {
            "user_id": user_id,
            "username": username,
            "role": role,
            "exp": expire
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None
    
    @staticmethod
    def create_user(username: str, email: str, password: str, role: UserRole = UserRole.USER, 
                   organization_name: str = None, wallet_address: str = None) -> User:
        """Create a new user and send welcome email"""
        db = SessionLocal()
        try:
            # Check if user already exists
            existing_user = db.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                raise ValueError("Username or email already exists")
            
            # Create new user
            password_hash = AuthService.hash_password(password)
            new_user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                role=role,
                organization_name=organization_name,
                wallet_address=wallet_address
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            # Send welcome email after successful registration
            try:
                role_str = role.value if hasattr(role, 'value') else str(role)
                email_sent = email_service.send_registration_confirmation(
                    user_email=email,
                    username=username,
                    role=role_str,
                    organization_name=organization_name
                )
                if email_sent:
                    print(f"✅ Welcome email sent to {email}")
                else:
                    print(f"⚠️ Failed to send welcome email to {email}")
            except Exception as e:
                print(f"⚠️ Email sending error: {str(e)}")
                # Don't fail the registration if email fails
            
            return new_user
        finally:
            db.close()
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[User]:
        """Authenticate a user by username and password"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(
                (User.username == username) | (User.email == username)
            ).first()
            
            if user and user.is_active and AuthService.verify_password(password, user.password_hash):
                return user
            return None
        finally:
            db.close()
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Get user by ID"""
        db = SessionLocal()
        try:
            return db.query(User).filter(User.id == user_id, User.is_active == True).first()
        finally:
            db.close()
    
    @staticmethod
    def create_default_admin():
        """Create default admin user if none exists"""
        db = SessionLocal()
        try:
            admin_exists = db.query(User).filter(User.role == UserRole.ADMIN).first()
            if not admin_exists:
                admin_user = User(
                    username="admin",
                    email="admin@bluecarbon.com",
                    password_hash=AuthService.hash_password("admin123"),
                    role=UserRole.ADMIN,
                    organization_name="Blue Carbon Registry"
                )
                db.add(admin_user)
                db.commit()
                print("✅ Default admin user created: admin/admin123")
        finally:
            db.close()