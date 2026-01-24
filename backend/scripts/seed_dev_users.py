from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()

def create_user(email, password, role, is_admin=False):
    user = User(
        email=email,
        hashed_password=hash_password(password),
        role=role,
        is_active=True,
        is_admin=is_admin,
    )
    db.add(user)

create_user("admin@test.com", "admin123", "admin", True)
create_user("owner@test.com", "owner123", "owner")
create_user("editor@test.com", "editor123", "editor")
create_user("viewer@test.com", "viewer123", "viewer")

db.commit()
db.close()

print("✅ Users recreated with bcrypt hashes")

