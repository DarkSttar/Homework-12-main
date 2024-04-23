from typing import List

from sqlalchemy.orm import Session

from src.database.models import PhoneNumber
from src.schemas.schemas import PhoneNumberModel

async def get_numbers(skip: int,limit:int, db:Session) -> List[PhoneNumber]:
    return db.query(PhoneNumber).offset(skip).limit(limit).all()


async def create_phone_number(body:PhoneNumberModel,db:Session):
    number = PhoneNumber(number=body.number)
    db.add(number)
    db.commit()
    db.refresh(number)
    return number

async def update_phone(phone_id:int, body:PhoneNumberModel,db:Session) -> PhoneNumber:
    number = db.query(PhoneNumber).filter(PhoneNumber.id == phone_id).first()
    if number:
        number.number = body.number
        db.commit()
    return number

async def remove_phone(phone_id:int, body:PhoneNumberModel,db:Session) -> PhoneNumber:
    number = db.query(PhoneNumber).filter(PhoneNumber.id == phone_id).first()
    if number:
        db.delete(number)
        db.commit()
    return number