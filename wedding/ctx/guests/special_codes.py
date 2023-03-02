"""Специальные коды ошибок домена guests"""

GUEST_DOMAIN_ERROR = "GUEST_DOMAIN_ERROR"  # ошибка домена гостя (не уточняется какая)
GUEST_NOT_FOUND = "GUEST_NOT_FOUND"  # гость не найден
GUEST_VALIDATION_ERROR = "GUEST_VALIDATION_ERROR"  # ошибка валидации гостя
GUEST_UNRECOGNIZED_MALE = "GUEST_UNRECOGNIZED_MALE"  # неизвестное значение пола гостя
GUEST_MULTIPLE_FOUND = "GUEST_MULTIPLE_FOUND"  # найдено несколько гостей, когда ожидался один
