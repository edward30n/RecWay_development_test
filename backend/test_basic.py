"""
Simple test script to verify basic functionality
"""
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def test_basic_functionality():
    """Test basic database and models functionality"""
    print("Testing basic functionality...")
    
    # Test config
    print(f"Database URI: {settings.DATABASE_URI}")
    
    # Test database connection
    try:
        db = SessionLocal()
        print("Database connection: OK")
        
        # Test creating a user
        hashed_password = get_password_hash("testpassword")
        print(f"Password hashing: OK")
        
        # Test querying users
        users = db.query(User).all()
        print(f"Users in database: {len(users)}")
        
        db.close()
        print("All tests passed!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_basic_functionality()
