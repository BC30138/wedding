"""Структуры данных сущностей домена forms."""
from dataclasses import dataclass


@dataclass
class FormEntity:
    """Сущность бланка с ответами."""

    group_id: int  # идентификатор группы гостей
    attend: bool  # будет ли группа гостей присутствовать?
    transfer: bool  # потребуется ли трансфер для коттеджа?
    sleepover: bool  # останутся с ночевой?
    plus: str | None = None  # ФИО +1
    id: int | None = None  # Идентификатор бланка в бд
