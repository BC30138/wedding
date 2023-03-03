"""Ошибки домена forms."""
from wedding.ctx.forms.special_codes import (
    FORM_DOMAIN_ERROR,
    FORM_MULTIPLE_FOUND,
    FORM_NOT_FOUND,
    FORM_VALIDATION_ERROR,
)
from wedding.ctx.general_errors import DomainError

FORM_ENTITY_NAME = "FormEntity"


class FormEntityError(DomainError):
    """Ошибка связанная с сущностью бланком ответов."""

    special_code = FORM_DOMAIN_ERROR

    def __init__(self, msg: str, special_code: str | None = None):
        super().__init__(
            entity=FORM_ENTITY_NAME,
            msg=msg,
            special_code=special_code,
        )


class FormNotFoundEntityError(FormEntityError):
    """Бланк не найден"""

    special_code = FORM_NOT_FOUND

    def __init__(self, msg: str | None):
        msg = "Form not found" if msg is None else msg
        super().__init__(msg=msg)


class FormValidationEntityError(FormEntityError):
    """Ошибка валидации гостя."""

    special_code = FORM_VALIDATION_ERROR

    def __init__(self, msg: str | None, special_code: str | None):
        msg = "Form validation error" if msg is None else msg
        super().__init__(
            msg=msg,
            special_code=special_code,
        )


class MultipleFormsEntityError(FormEntityError):
    """Несколько бланков найдено, когда ожидался один."""

    special_code = FORM_MULTIPLE_FOUND

    def __init__(self, msg: str | None):
        msg = "Multiple forms found" if msg is None else msg
        super().__init__(msg=msg)
