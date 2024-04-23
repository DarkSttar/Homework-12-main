from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import phones,contacts,emails,auth
from sqlalchemy.orm import Session
from fastapi import Depends
from src.database.db import get_db
app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(emails.router,prefix='/api')
app.include_router(phones.router,prefix='/api')



@app.get("/")
def index():
    return {"message": "ContactBook Application"}



