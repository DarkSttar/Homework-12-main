from datetime import datetime
from typing import List,Optional
from pydantic import BaseModel,Field,EmailStr

class PhoneNumberModel(BaseModel):
    number: str = Field(max_length=12)
class PhoneNumberResponse(PhoneNumberModel):
    id: int

    class Config:
        orm_mode = True

class EmailModel(BaseModel):
    email: EmailStr = Field(max_length=50)


class EmailResponse(EmailModel):
    id: int

    class Config:
        orm_mode = True    


class ContactBase(BaseModel):
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    born_date: datetime


class ContactModel(ContactBase):
    emails: List[int]
    phone_numbers: List[int]


class ContactResponse(ContactBase):
    id:int
    created_at: datetime
    emails: List[EmailResponse]
    phone_numbers: List[PhoneNumberResponse]
