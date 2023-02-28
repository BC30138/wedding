"""Базовые ошибки для фронтенд интерфейса."""


class ServiceError(Exception):
    """Ошибка в работе сервиса."""

    special_code = "UNEXPECTED_SERVICE_ERROR"  # специальный код, когда код не указан

    def __init__(self, service: str, msg: str, special_code: str | None = None):
        """
        :param service: название сервиса
        :param msg: сообщение в ошибке
        :param special_code: специальный код ошибки
        """
        self.service = service
        self.msg = msg
        if special_code is not None:
            self.special_code = special_code
        super().__init__(self.msg)


class BadResponseData(ServiceError):
    """Ошибка, когда ожидался другой ответ в сервисе."""

    special_code = "BAD_RESPONSE"
