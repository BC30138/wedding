import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from tests.unit.extensions.store.repo.guests.factories import GuestsFactory
from wedding.cfg import app_configuration


@pytest.fixture(autouse=True)
def _init_factories(db_session: AsyncSession) -> None:
    """Инициализация сессии в фабриках."""
    GuestsFactory._meta.sqlalchemy_session = db_session


@pytest_asyncio.fixture
async def db_session():
    """Сессия базы данных."""
    engine = create_async_engine(app_configuration.async_database_url)
    connection = await engine.connect()
    trans = await connection.begin()

    Session = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)
    session = Session()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()
        await engine.dispose()
