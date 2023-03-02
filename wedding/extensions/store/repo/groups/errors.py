"""Ошибки репозитория групп гостей."""
from wedding.extensions.store.global_errors import StoreError
from wedding.extensions.store.repo.groups.special_codes import GROUP_CONSTRAINT_ERROR, GROUP_STORE_ERROR

GROUP_MODEL_NAME = "GroupModel"


class GroupStoreError(StoreError):
    """Ошибка группы гостей"""

    special_code = GROUP_STORE_ERROR

    def __init__(self, msg: str, special_code: str | None = None):
        super().__init__(
            model=GROUP_MODEL_NAME,
            msg=msg,
            special_code=special_code,
        )


class GroupsConstraintError(GroupStoreError):
    """Конфликт данных групп гостей."""

    special_code = GROUP_CONSTRAINT_ERROR

    def __init__(self, msg: str):
        super().__init__(msg=msg)
