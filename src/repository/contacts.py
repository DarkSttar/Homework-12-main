

from typing import List
from sqlalchemy import func
import datetime
from sqlalchemy.orm import Session

from src.database.models import Contact,PhoneNumber,Email,User
from src.schemas.schemas import ContactBase,ContactModel,ContactResponse

async def get_contacts(skip: int,limit:int, db:Session , user:User) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

async def get_contact_by_first_name(name:str,db:Session, user:User) -> Contact:
    return db.query(Contact).filter_by(Contact.first_name == name, Contact.user_id == user.id).first()

async def get_contact_by_last_name(name:str,db:Session, user:User) -> Contact:
    return db.query(Contact).filter_by(Contact.last_name == name, Contact.user_id == user.id).first()
    
async def get_contact_by_email(email:str,db:Session, user:User) -> Contact:
    return db.query(Contact).join(Contact.emails).filter_by(Email.email == email, Contact.id == user.id).first()

async def get_contacts_with_upcoming_birthdays(db: Session, user:User) -> List[Contact]:
    
    today = datetime.date.today()
    next_week = today + datetime.timedelta(days=7)

    contacts = db.query(Contact).filter(
        func.extract('day', Contact.born_date) >= today.day,
        func.extract('day', Contact.born_date) <= next_week.day,
        Contact.user_id == user.id

    ).all()

    return contacts
        
        
async def create_contact(body: ContactModel,db:Session, user:User) -> Contact:
    phones = db.query(PhoneNumber).filter(PhoneNumber.id.in_(body.phone_numbers)).all()
    emails = db.query(Email).filter(Email.id.in_(body.emails)).all()
    contact = Contact(first_name=body.first_name,last_name=body.last_name,emails=emails,phone_numbers=phones,born_date=body.born_date)
    contact.user_id = user.id
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def update_contact(contact_id: int, body:ContactModel,db:Session,user:User) -> Contact:
    contact = db.query(Contact).filter(Contact.id == contact_id,Contact.user_id == user.id).first()
    if contact:
        phones = db.query(PhoneNumber).filter(PhoneNumber.id.in_(body.phone_numbers)).all()
        emails = db.query(Email).filter(Email.id.in_(body.emails)).all()
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.emails = emails
        contact.phone_numbers = phones
        contact.born_date = body.born_date
        db.commit()
    return contact  

async def delete_contact(contact_id:int, body:ContactModel,db:Session, user:User) -> Contact:
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


