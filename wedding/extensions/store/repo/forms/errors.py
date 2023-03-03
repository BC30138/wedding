"""Ошибки бд бланков ответов."""
from wedding.extensions.store.global_errors import StoreError
from wedding.extensions.store.repo.forms.special_codes import (
    FORM_CONSTRAINT_ERROR,
    FORM_DB_ERROR,
    FORM_MULTIPLE_ROWS_FOUND_ERROR,
)

FORM_MODEL_NAME = "FormModel"


class FormStoreError(StoreError):
    """Ошибка модели бланка ответов."""

    special_code = FORM_DB_ERROR

    def __init__(self, msg: str):
        super().__init__(
            model=FORM_MODEL_NAME,
            msg=msg,
        )


class FormsConstraintError(FormStoreError):
    """Конфликт данных бланков ответов."""

    special_code = FORM_CONSTRAINT_ERROR

    def __init__(self, msg: str):
        super().__init__(msg=msg)


class MultipleFormsFoundError(FormStoreError):
    """Найдено несколько бланков, когда должен был найтись один."""

    special_code = FORM_MULTIPLE_ROWS_FOUND_ERROR

    def __init__(self, msg: str):
        super().__init__(msg=msg)
