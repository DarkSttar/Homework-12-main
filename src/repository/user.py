from fastapi import Depends

from sqlalchemy.orm import Session


from src.database.db import get_db
from src.database.models import User
from src.schemas.users import UserSchema


async def get_user_by_email(email: str, db:Session = Depends(get_db)):
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserSchema, db: Session = Depends(get_db)):
    new_user = User(**body.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session = Depends(get_db)):
    user.refresh_token = token
    await db.commit()
