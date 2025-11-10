import os
import sys
from dotenv import load_dotenv # Import load_dotenv first

# Load environment variables as early as possible
load_dotenv()

from sqlalchemy.orm import Session

# Ensure the project root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import SessionLocal
from backend.models import User
from backend.auth import pwd_context

# --- Configuration ---
ADMIN_USERNAME = "admin@microlearn.com"
ADMIN_PASSWORD = "admin1234"

def seed_database():
    """
    Seeds the database with a default admin user if it doesn't exist.
    """
    print("Seeding database...")
    db: Session = SessionLocal()
    try:
        # Create all tables if they don't exist
        from backend.models import Base
        from backend.database import engine
        Base.metadata.create_all(bind=engine)

        # Check if admin user already exists
        db_user = db.query(User).filter(User.username == ADMIN_USERNAME).first()
        
        if not db_user:
            print(f"Admin user '{ADMIN_USERNAME}' not found. Creating...")
            
            # Hashing the password
            hashed_password = pwd_context.hash(ADMIN_PASSWORD)
            
            # Creating the user object
            db_user_obj = User(username=ADMIN_USERNAME, hashed_password=hashed_password)
            db.add(db_user_obj)
            db.commit()
            db.refresh(db_user_obj)
            
            print(f"Admin user '{ADMIN_USERNAME}' created successfully.")
        else:
            print(f"Admin user '{ADMIN_USERNAME}' already exists.")
            
    except Exception as e:
        print(f"An error occurred during seeding: {e}")
    finally:
        db.close()
        print("Database seeding finished.")

if __name__ == "__main__":
    seed_database()
