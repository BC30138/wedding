"""Бд модели бланка вопросов."""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from wedding.ctx.forms.entity.structures import FormEntity
from wedding.extensions.store.database import Base
from wedding.extensions.store.utils.models import ReprMixin


class Forms(Base, ReprMixin):
    __tablename__ = "forms"
    __table_args__ = {"comment": "Таблица бланков вопросов"}
    id = Column(Integer, primary_key=True, comment="Идентификатор бланка")
    group_id = Column(Integer, ForeignKey("groups.id"), unique=True, nullable=False, comment="Идентификатор группы")
    plus = Column(String, nullable=True, comment="Имя плюс одного")
    attend = Column(Boolean, nullable=False, comment="Прийдут ли гости из группы?")
    transfer = Column(Boolean, nullable=False, comment="Потребуется трансфер до коттеджа?")
    sleepover = Column(Boolean, nullable=False, comment="Останутся с ночевой?")

    @classmethod
    def from_entity(cls, entity: FormEntity) -> "Forms":
        return cls(
            id=entity.id,
            group_id=entity.group_id,
            plus=entity.plus,
            attend=entity.attend,
            transfer=entity.transfer,
            sleepover=entity.sleepover,
        )

    def to_entity(self) -> FormEntity:
        """Метод преобразует модель в сущность."""
        return FormEntity(
            id=self.id,
            group_id=self.group_id,
            plus=self.plus,
            attend=self.attend,
            transfer=self.transfer,
            sleepover=self.sleepover,
        )
