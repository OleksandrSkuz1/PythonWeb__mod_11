from sqlalchemy import Boolean, Column, Integer, String, Date
from sqlalchemy.orm import relationship
from src.database.db import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    birthday = Column(Date, index=True)
    additional_data = Column(String, index=True)
