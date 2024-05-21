from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, extract
from datetime import datetime, timedelta
from src.database.models import Contact
from src.schemas import ContactCreate


def get_contacts(db: Session):
    return db.query(Contact).all()


def get_contact_by_id(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(db: Session, contact_id: int, contact: ContactCreate):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        return db_contact
    return None


def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return db_contact
    return None


def search_contacts(db: Session, query: str):
    return db.query(Contact).filter(
        or_(
            Contact.first_name.ilike(f"%{query}%"),
            Contact.last_name.ilike(f"%{query}%"),
            Contact.email.ilike(f"%{query}%")
        )
    ).all()


def get_upcoming_birthdays(db: Session):
    today = datetime.today().date()
    next_week = today + timedelta(days=7)
    result = (
        db.query(Contact)
        .filter(
            or_(
                and_(
                    extract("month", Contact.birthday) == today.month,
                    extract("day", Contact.birthday) >= today.day,
                    extract("day", Contact.birthday) <= next_week.day,
                ),
                and_(
                    extract("month", Contact.birthday) == next_week.month,
                    extract("day", Contact.birthday) >= today.day,
                    extract("day", Contact.birthday) <= next_week.day,
                ),
            )
        )
        .all()
    )
    return result
