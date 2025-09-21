# init_db.py
from database import engine
from models.db_model import Base
from services.auth import AuthService

# Create all tables
Base.metadata.create_all(bind=engine)

# Create default admin user
AuthService.create_default_admin()

print("✅ Database initialized successfully!")
