from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

from resources.constants import DBConstants

Base = declarative_base()

class AddressBook(Base):
    __tablename__ = DBConstants.ADDRESS_BOOK

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)