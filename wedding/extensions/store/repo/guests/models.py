from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from wedding.extensions.store.database import Base

class Guests(Base):
    __tablename__ = "guests"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("Users", back_populates="guests")

