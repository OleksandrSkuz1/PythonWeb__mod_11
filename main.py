import time
from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.database.db import get_db, engine, Base
from src.database.models import Contact
from src.schemas import ContactResponse, ContactBase
from starlette.middleware.base import BaseHTTPMiddleware
from src.routes.contacts import router as contacts_router, birthdays_router

# Створення таблиць
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Підключення роутів з src/routes/contacts.py

app.include_router(contacts_router, prefix="/contacts", tags=["Contacts"])
app.include_router(birthdays_router, prefix="/contacts", tags=["Birthdays"])

class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers['Custom'] = 'Example'
        return response


app.add_middleware(CustomHeaderMiddleware)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
def root():
    return {"message": "Application V0.0.1"}

@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

@app.get("/contacts/", response_model=list[ContactResponse], tags=["Contacts"])
async def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()
    return contacts

@app.get("/contacts/{contact_id}", response_model=ContactResponse, tags=["Contacts"])
async def get_contact_by_id(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact

@app.post("/contacts/", response_model=ContactResponse, tags=["Contacts"])
async def create_contact(body: ContactBase, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(email=body.email).first()
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Contact already exists.")

    contact = Contact(first_name=body.first_name,
                      last_name=body.last_name,
                      email=body.email,
                      phone=body.phone,
                      birthday=body.birthday,
                      additional_data=body.additional_data
                      )
    db.add(contact)
    db.refresh(contact)
    db.commit()
    return contact

@app.put("/contacts/{contact_id}", response_model=ContactResponse, tags=["Contacts"])
async def update_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    contact.email = body.email
    contact.first_name = body.first_name
    contact.last_name = body.last_name
    contact.phone = body.phone
    contact.additional_data = body.additional_data
    contact.birthday = body.birthday
    db.commit()
    return contact

@app.delete("/contacts/{contact_id}", response_model=ContactResponse, tags=["Contacts"])
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    db.delete(contact)
    db.commit()
    return contact


