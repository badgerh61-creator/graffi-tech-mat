from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()

def upsert(email, pw, role, is_admin=False):
    u = db.query(User).filter_by(email=email).first()
    if not u:
        u = User(
            email=email,
            hashed_password=hash_password(pw),
            role=role,
            is_active=True,
            is_admin=is_admin,
        )
        db.add(u)
    else:
        u.hashed_password = hash_password(pw)
        u.role = role
        u.is_active = True
        u.is_admin = is_admin
    db.commit()

upsert("admin@test.com", "admin123", "admin", True)
upsert("editor@test.com", "editor123", "editor")
upsert("viewer@test.com", "viewer123", "viewer")

print("✅ Dev users ready")

