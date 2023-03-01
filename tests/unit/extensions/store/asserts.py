"""Функции хэлперы для сравнения объектов бд."""
from wedding.extensions.store.database import Base


def assert_model_fields(
    left_model: Base,
    right_model: Base,
    exclude: tuple[str] = (),
):
    """
    Сравнивает все поля, кроме указанных в exclude полей

    :param left_model: модель из бд для сравнения
    :param right_model: модель из бд для сравнения
    :param exclude: список полей, которые нужно исключить из сравнения
    """
    for column in left_model.__table__.columns:
        column_key = column.key
        if column_key in exclude:
            continue
        left_value = getattr(left_model, column_key)
        right_value = getattr(right_model, column_key)
        assert left_value == right_value
