"""Вспомогательные объекты для переноса данных между слоями."""
from dataclasses import dataclass
from typing import TypedDict

from wedding.ctx.forms.entity.structures import FormEntity


@dataclass
class FormData:
    group_id: int  # идентификатор группы гостей
    attend: bool  # будет ли группа гостей присутствовать?
    transfer: bool  # потребуется ли трансфер для коттеджа?
    sleepover: bool  # останутся с ночевой?
    plus: str | None = None  # ФИО +1

    def to_entity(self) -> FormEntity:
        """Создать сущность из данных."""
        return FormEntity(
            id=None,
            group_id=self.group_id,
            attend=self.attend,
            transfer=self.transfer,
            sleepover=self.sleepover,
            plus=self.plus,
        )


class LoadFormsFiltersDTO(TypedDict, total=False):
    group_ids: list[int] | None  # идентификаторы групп гостей
