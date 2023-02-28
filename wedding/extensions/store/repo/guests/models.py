"""Бд модели гостей."""
from sqlalchemy import Column, Integer, String

from wedding.ctx.guests.entity.guest import GuestEntity, MaleEnum
from wedding.extensions.store.database import Base


class Guests(Base):
    __tablename__ = "guests"
    __table_args__ = {"comment": "Таблица гостей"}
    id = Column(Integer, primary_key=True, comment="Идентификатор гостя")
    first_name = Column(String, nullable=False, comment="Имя гостя")
    middle_name = Column(String, comment="Отчество гостя")
    last_name = Column(String, nullable=False, comment="Фамилия гостя")
    male = Column(String, nullable=False, comment="Пол гостя")

    def to_entity(self) -> GuestEntity:
        """Метод преобразует модель в сущность."""
        return GuestEntity(
            id=self.id,
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name,
            male=MaleEnum(self.male),
        )
