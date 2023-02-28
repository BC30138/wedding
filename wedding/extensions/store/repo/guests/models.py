from sqlalchemy import Column, Integer, String

from wedding.ctx.guests.entity.guest import GuestEntity, MaleEnum
from wedding.extensions.store.database import Base


class Guests(Base):
    __tablename__ = "guests"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String)
    last_name = Column(String, nullable=False)
    male = Column(String, nullable=False)

    def to_entity(self) -> GuestEntity:
        return GuestEntity(
            id=self.id,
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name,
            male=MaleEnum(self.male),
        )
