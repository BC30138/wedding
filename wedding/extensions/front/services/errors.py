"""Ошибки сервисов фронтенд интерфейса."""
from wedding.extensions.front.general_errors import BadResponseData


class GuestNotProvided(BadResponseData):
    """Случай когда первый гость не найден в ответе от сервера."""
