from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas import ContactResponse, ContactBase
from src.repository import contacts as contacts_repository

router = APIRouter()
contacts_router = APIRouter()
birthdays_router = APIRouter()

@router.get("/", response_model=list[ContactResponse])
async def get_contacts(db: Session = Depends(get_db)):
    return contacts_repository.get_contacts(db)


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact_by_id(contact_id: int, db: Session = Depends(get_db)):
    contact = contacts_repository.get_contact_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(contact: ContactBase, db: Session = Depends(get_db)):
    db_contact = contacts_repository.get_contact_by_id(db, contact.id)
    if db_contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Contact already exists.")
    return contacts_repository.create_contact(db, contact)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, contact: ContactBase, db: Session = Depends(get_db)):
    db_contact = contacts_repository.update_contact(db, contact_id, contact)
    if not db_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return db_contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = contacts_repository.delete_contact(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return db_contact


@router.get("/search/", response_model=list[ContactResponse])
async def search_contacts(query: str, db: Session = Depends(get_db)):
    return contacts_repository.search_contacts(db, query)


@router.get("/birthdays/", response_model=list[ContactResponse])
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    return contacts_repository.get_upcoming_birthdays(db)



