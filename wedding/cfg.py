import os
from dataclasses import dataclass
from urllib.parse import urlparse

from dotenv import load_dotenv


@dataclass
class AppConfiguration:
    database_url: str
    async_database_url: str


def make_app_configuration() -> AppConfiguration:
    load_dotenv()
    env_content = os.environ

    database_url = urlparse(env_content["DATABASE_URL"])
    async_database_url = database_url._replace(scheme="postgresql+asyncpg")

    return AppConfiguration(
        database_url=str(database_url.geturl()),
        async_database_url=str(async_database_url.geturl()),
    )


app_configuration = make_app_configuration()
