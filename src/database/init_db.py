from sqlalchemy.orm import Session
from src.database.db import engine, SessionLocal, Base
from src.schemas import ContactCreate
from faker import Faker
from src.database.models import Contact

fake = Faker()

def create_fake_contacts(n=100):
    db = SessionLocal()
    try:
        # Створення таблиць
        Base.metadata.create_all(bind=engine)

        emails_used = set()  # Набір унікальних електронних адрес

        for _ in range(n):
            email = fake.unique.email()  # Генеруємо унікальний електронний адрес
            while email in emails_used:
                email = fake.unique.email()  # Якщо адрес вже використовується, генеруємо новий
            emails_used.add(email)  # Додаємо адрес до набору

            contact_data = ContactCreate(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=email,
                phone=fake.phone_number(),
                birthday=fake.date_of_birth(minimum_age=18, maximum_age=60),
                additional_data=fake.sentence()
            )
            db_contact = Contact(**contact_data.dict())
            db.add(db_contact)
        db.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_fake_contacts()