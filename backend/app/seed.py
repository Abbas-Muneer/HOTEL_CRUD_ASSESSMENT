from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.user import User


def seed_admin_user() -> None:
    db: Session = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == "admin").first()
        if existing:
            return
        user = User(
            username="admin",
            email="admin@hotel.local",
            hashed_password=get_password_hash("Admin@123"),
        )
        db.add(user)
        db.commit()
    finally:
        db.close()
