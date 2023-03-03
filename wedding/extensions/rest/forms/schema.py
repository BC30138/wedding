"""Схемы для запросов к бланкам ответов."""
from pydantic import BaseModel

from wedding.ctx.forms.dto.data import FormData
from wedding.ctx.forms.entity.structures import FormEntity


class FormSchemaData(BaseModel):
    """Ответы."""

    group_id: int  # идентификатор группы
    attend: bool  # будут ли присутствовать
    transfer: bool  # потребуется ли трансфер
    sleepover: bool  # потребуется ли спальное место
    plus: str | None  # ФИО +1

    def to_dto(self) -> FormData:
        """Переводит ответы в объект для передачи между слоями."""
        return FormData(
            group_id=self.group_id,
            attend=self.attend,
            transfer=self.transfer,
            sleepover=self.sleepover,
            plus=self.plus,
        )


class FormSchema(FormSchemaData):
    """Бланк ответов"""

    id: int  # идентификатор бланка

    @classmethod
    def from_entity(cls, entity: FormEntity) -> "FormSchema":
        return cls(
            id=entity.id,
            group_id=entity.group_id,
            attend=entity.attend,
            transfer=entity.transfer,
            sleepover=entity.sleepover,
            plus=entity.plus,
        )
