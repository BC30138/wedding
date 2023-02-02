from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from wedding.extensions.store.database import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    guests = relationship("Guests", back_populates="user")
