# init_db.py
from database import engine
from models.db_model import Base, MRVData, ProjectData  # Explicitly import all models
from models.auth_model import User, LoginSession, UserRole  # Import auth models
from services.auth import AuthService

# Create all tables
Base.metadata.create_all(bind=engine)

# Create default admin user
AuthService.create_default_admin()

print("SUCCESS: Database initialized successfully!")
print("Tables created:", list(Base.metadata.tables.keys()))
