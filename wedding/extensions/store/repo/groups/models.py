"""Модели бд для группы гостей."""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from wedding.ctx.groups.entity.group import GroupEntity
from wedding.extensions.store.database import Base


class Groups(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    sleep_place = Column(Boolean, default=True, nullable=False)
    finalize = Column(Boolean, default=False, nullable=False)
    guest_1_id = Column(Integer, ForeignKey("guests.id"))
    guest_2_id = Column(Integer, ForeignKey("guests.id"))

    def to_entity(self):
        return GroupEntity(
            id=self.id,
            name=self.name,
            sleep_place=self.sleep_place,
            finalize=self.finalize,
            guest_1_id=self.guest_1_id,
            guest_2_id=self.guest_2_id,
        )
