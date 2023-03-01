"""Хэлперы для фабрик бд."""
import inspect

from factory.alchemy import SESSION_PERSISTENCE_COMMIT, SESSION_PERSISTENCE_FLUSH, SQLAlchemyModelFactory

# Здесь творится какая-то безумная магия копипасты из интернета,
# которая делает factory_boy способным к работе с асинхронной бд


class BaseAsyncFactory(SQLAlchemyModelFactory):
    """Базовая фабрика для бд-моделей."""

    class Meta:
        sqlalchemy_session_persistence = SESSION_PERSISTENCE_FLUSH

    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        for key, value in kwargs.items():
            if inspect.isawaitable(value):
                kwargs[key] = await value
        return await super()._create(model_class, *args, **kwargs)

    @classmethod
    async def create_batch(cls, size, **kwargs):
        return [await cls.create(**kwargs) for _ in range(size)]

    @classmethod
    async def _save(cls, model_class, session, args, kwargs):
        session_persistence = cls._meta.sqlalchemy_session_persistence
        obj = model_class(*args, **kwargs)
        session.add(obj)
        if session_persistence == SESSION_PERSISTENCE_FLUSH:
            await session.flush()
        elif session_persistence == SESSION_PERSISTENCE_COMMIT:
            await session.commit()
        return obj
