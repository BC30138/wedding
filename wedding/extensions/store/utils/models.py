"""Хэлперы моделей бд."""


class ReprMixin:
    """Базовая модель бд."""

    def __repr__(self) -> str:
        representation = f"<{type(self).__name__}("
        columns_representations = []
        for column in self.__table__.columns:  # type: ignore
            column_key = column.key
            value = getattr(self, column_key)
            columns_representations.append(f"{column_key}={value}")
        representation += ", ".join(columns_representations)
        representation += ")>"
        return representation
