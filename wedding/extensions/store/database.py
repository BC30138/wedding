from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from wedding.cfg import app_configuration
from wedding.extensions.store import repo
from wedding.extensions.store.utils.utils import import_sqlalchemy_models

Base = declarative_base()
import_sqlalchemy_models(repo)

engine = create_async_engine(app_configuration.async_database_url)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # noqa


async def db_session() -> AsyncSession:
    async with async_session() as session:
        yield session
