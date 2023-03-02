"""Сущность гостя и все что с ней связано."""
import logging
from dataclasses import dataclass
from enum import Enum

from wedding.ctx.guests.errors import GuestValidationEntityError
from wedding.ctx.guests.special_codes import GUEST_UNRECOGNIZED_MALE

logger = logging.getLogger().getChild("guest_entity")


class MaleEnum(Enum):
    """Пол."""

    male = "male"  # муж
    female = "female"  # жен


@dataclass
class GuestEntity:
    """Сущность гостя."""

    first_name: str  # Имя
    middle_name: str | None  # Отчество
    last_name: str  # Фамилия
    male: MaleEnum  # Пол гостя
    id: int | None = None  # Идентификатор гостя в бд

    @property
    def full_name(self) -> str:
        """Полное имя гостя в формате ФИО/ФИ."""
        full_name_list = [self.last_name, self.first_name]
        if self.middle_name:
            full_name_list.append(self.middle_name)
        return " ".join(full_name_list)

    @staticmethod
    def cast_male(value: str) -> MaleEnum:
        """Преобразовывает male из строки в enum."""
        try:
            return MaleEnum(value)
        except ValueError as exc:
            logger.warning("Unrecognized guest male=%s", value)
            raise GuestValidationEntityError(
                msg=f"Unrecognized guest male {value}",
                special_code=GUEST_UNRECOGNIZED_MALE,
            ) from exc
