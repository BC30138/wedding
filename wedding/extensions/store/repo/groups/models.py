"""Модели бд для группы гостей."""
from sqlalchemy import Column, ForeignKey, Integer, String

from wedding.ctx.groups.entity.group import GroupEntity
from wedding.extensions.store.database import Base
from wedding.extensions.store.utils.models import ReprMixin


class Groups(Base, ReprMixin):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    guest_1_id = Column(Integer, ForeignKey("guests.id"))
    guest_2_id = Column(Integer, ForeignKey("guests.id"))

    def to_entity(self) -> GroupEntity:
        return GroupEntity(
            id=self.id,
            name=self.name,
            guest_1_id=self.guest_1_id,
            guest_2_id=self.guest_2_id,
        )
