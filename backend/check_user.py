import os
import sys
from dotenv import load_dotenv

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

def verify_admin_password():
    """
    Connects to the DB and verifies the admin user's password.
    """
    print("Verifying admin user password...")
    db: Session = SessionLocal()
    try:
        # Find the admin user
        user = db.query(User).filter(User.username == ADMIN_USERNAME).first()
        
        if not user:
            print(f"FAILURE: Admin user '{ADMIN_USERNAME}' not found in the database.")
            return

        print(f"User '{ADMIN_USERNAME}' found. Verifying password...")
        
        # Verify the password
        is_correct = pwd_context.verify(ADMIN_PASSWORD, user.hashed_password)
        
        if is_correct:
            print("\nSUCCESS: Password verification successful!")
            print("The password stored in the database for the admin user is correct.")
        else:
            print("\nFAILURE: Password verification failed!")
            print("The stored password hash does not match the provided password.")
            
    except Exception as e:
        print(f"An error occurred during verification: {e}")
    finally:
        db.close()
        print("Verification script finished.")

if __name__ == "__main__":
    verify_admin_password()
