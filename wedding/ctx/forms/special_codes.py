"""Специальные коды ошибок домена forms"""

FORM_DOMAIN_ERROR = "FORMS_DOMAIN_ERROR"  # ошибка домена бланков (не уточняется какая)
FORM_NOT_FOUND = "FORM_NOT_FOUND"  # бланк не найден
FORM_VALIDATION_ERROR = "FORM_VALIDATION_ERROR"  # ошибка валидации бланка
FORM_PLUS_ONE_FORBIDDEN = "FORM_PLUS_ONE_FORBIDDEN"  # парам нельзя звать +1
FORM_MULTIPLE_FOUND = "FORM_MULTIPLE_FOUND"  # найдено несколько бланков, когда ожидался один
