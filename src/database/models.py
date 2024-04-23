from sqlalchemy import Column,Integer,String,func,Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer,primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    emails = relationship("Email",backref='contacts')
    phone_numbers = relationship("PhoneNumber", backref='contacts')
    born_date = Column('born_date',DateTime)
    created_at = Column('created_at',DateTime,default=func.now())
    user_id = Column(Integer,ForeignKey('users.id'))

class User(Base):
    __tablename__ ='users'

    id = Column(Integer,primary_key=True)
    username = Column(String(25),nullable=False,unique=True)
    password = Column(String(25),nullable=False)
    email = Column(String(100),nullable=False,unique=True)
    contacts = relationship('Contact',backref='user')
    refresh_token = Column(String(255),nullable=True)
    

class Email(Base):
    __tablename__ = 'emails'
    id = Column(Integer,primary_key=True)
    email = Column(String(100), nullable=False,unique=True)
    user_id = Column(Integer,ForeignKey('contacts.id'))

class PhoneNumber(Base):
    __tablename__ = 'phonenumbers'
    id = Column(Integer,primary_key=True)
    number = Column(String(100), nullable=False,unique=True)
    user_id = Column(Integer,ForeignKey('contacts.id'))