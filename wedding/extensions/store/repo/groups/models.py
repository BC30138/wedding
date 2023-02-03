from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from wedding.ctx.groups.entity.group import GroupEntity
from wedding.extensions.store.database import Base

class Groups(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    guests = relationship("Guests", back_populates="group")

    def to_entity(self):
        return GroupEntity(
            id=self.id,
            name=self.name,
            guests=[guest_model.to_entity() for guest_model in self.guests]
        )
