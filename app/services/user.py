from app.models.user import User
from app.schemas.user import UserCreate
from app.database import SessionDep
from app.auth.security import get_password_hash
import bcrypt


def get_user(session: SessionDep, user_id: int):
    return session.query(User).filter(User.id == user_id).first()


def get_user_by_email(session: SessionDep, email: str):
    return session.query(User).filter(User.email == email).first()


def create_user(session: SessionDep, user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = User(email=user.email, hashed_password=hashed_password.decode("utf-8"))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
