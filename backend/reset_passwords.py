from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password

PASSWORDS = {
    "admin@test.com": "19Pat90Rick97",
    "editor@test.com": "editor123",
    "viewer@test.com": "viewer123",
}

def reset():
    db = SessionLocal()

    for email, plain in PASSWORDS.items():
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"❌ User not found: {email}")
            continue

        user.hashed_password = hash_password(plain)
        print(f"✅ Reset password for {email}")

    db.commit()
    db.close()

if __name__ == "__main__":
    reset()

