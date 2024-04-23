from typing import List

from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session
from src.database.models import User
from src.services.auth import auth_service

from src.database.db import get_db
from src.schemas.schemas import ContactBase,ContactModel,ContactResponse
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts',tags=['contacts'])



@router.get('/', response_model=List[ContactResponse])
async def read_contact(skip: int = 0,limit: int = 100,db: Session = Depends(get_db)):
    users = await repository_contacts.get_contacts(skip,limit,db)
    return users

@router.get('/upcomingbirthdays', response_model=List[ContactResponse])
async def read_contact_with_upcoming_birthdays(db:Session = Depends(get_db),user:User = Depends(auth_service.get_current_user)):
    users = await repository_contacts.get_contacts_with_upcoming_birthdays(db,user)
    return users
@router.get('/firstname/{first_name}', response_model=ContactResponse)
async def read_contact_by_first_name(first_name:str,db:Session = Depends(get_db) ,user:User = Depends(auth_service.get_current_user)):
    user = await repository_contacts.get_contact_by_first_name(first_name,db,user)
    if user is None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User Not Found')
    return user

@router.get('/lastname/{name}',response_model=ContactResponse)
async def read_contact_by_last_name(name:str, db:Session = Depends(get_db), user:User = Depends(auth_service.get_current_user)):
    user = await repository_contacts.get_contact_by_last_name(name,db)
    if user is None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User Not Found')
    return user

@router.get('/email/{email}',response_model=ContactResponse)
async def read_contact_by_email(email:str,db:Session = Depends(get_db), currentuser:User = Depends(auth_service.get_current_user)):
    user = await repository_contacts.get_contact_by_email(email,db,currentuser)
    if user is None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User Not Found')
    return user
@router.post('/',response_model=ContactResponse)
async def create_contact(body:ContactModel,db: Session = Depends(get_db)):
    user = await repository_contacts.create_contacts(body,db)
    return user


@router.put('/{contact_id}',response_model=ContactResponse)
async def update_contact(contact_id:int,body:ContactModel,db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_contacts.update_contact(contact_id,body,db, current_user)
    if user is None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User Not Found')
    return user

@router.delete('/{contact_id}',response_model=ContactResponse)
async def remove_contact(contact_id:int, body:ContactResponse,db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.delete_contact(contact_id,body,db)
    if contact is None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')
    return contact