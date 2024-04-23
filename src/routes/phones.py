from typing import List

from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session


from src.database.db import get_db
from src.schemas.schemas import PhoneNumberModel,PhoneNumberResponse
from src.repository import phones as repository_phones

router = APIRouter(prefix='/phones',tags=['phones'])



@router.get('/', response_model=List[PhoneNumberResponse])
async def read_phones(skip: int = 0,limit: int = 100,db: Session = Depends(get_db)):
    numbers = await repository_phones.get_numbers(skip,limit,db)
    return numbers

@router.post('/',response_model=PhoneNumberModel)
async def create_phone(body:PhoneNumberResponse, db: Session = Depends(get_db)):
    return await(repository_phones.create_phone_number(body,db))

@router.put('/{phone_id}',response_model=PhoneNumberModel)
async def update_phone(phone_id: int,body:PhoneNumberModel,db: Session = Depends(get_db)):
    number = await(repository_phones.update_phone(phone_id,body,db))
    if number is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Phone not Found')
    return number

@router.delete('/{phone_id}',response_model=PhoneNumberResponse)
async def remove_phone(phone_id:int,body:PhoneNumberResponse,db:Session = Depends(get_db)):
    number = await repository_phones.remove_phone(phone_id,body,db)
    if number is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Phone not found')
    return number