from typing import List

from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session

from src.database.models import User
from src.database.db import get_db
from src.schemas.schemas import EmailModel,EmailResponse
from src.repository import emails as repository_emails
from src.services.auth import auth_service
router = APIRouter(prefix='/emails',tags=['emails'])



@router.get('/', response_model=List[EmailResponse])
async def read_emails(skip: int = 0,limit: int = 100,db: Session = Depends(get_db), user:User = Depends(auth_service.get_current_user)):
    emails = await repository_emails.get_emails(skip,limit,db,user)
    return emails


@router.post('/',response_model=EmailResponse)
async def create_emails(body:EmailResponse,db:Session = Depends(get_db)):
    email = await repository_emails.create_email(body,db)
    return email

@router.put('/{email_id}',response_model=EmailModel)
async def update_phone(phone_id: int,body:EmailModel,db: Session = Depends(get_db)):
    email = await(repository_emails.update_email(phone_id,body,db))
    if email is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Email not Found')
    return email

@router.delete('/{email_id}',response_model=EmailResponse)
async def remove_phone(email_id:int,body:EmailResponse,db:Session = Depends(get_db)):
    email = await repository_emails.remove_eamil(email_id,body,db)
    if email is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Email not found')
    return email