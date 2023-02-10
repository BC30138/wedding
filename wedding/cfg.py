import os
from urllib.parse import urlparse
from dataclasses import dataclass
from dotenv import dotenv_values

DOTENV_PATH = ".env"

@dataclass
class AppConfiguration:
    database_url: str
    async_database_url: str

def make_app_configuration():
    env_content = dotenv_values(DOTENV_PATH)
    if not env_content:
        env_content = os.environ

    database_url = urlparse(env_content["DATABASE_URL"])
    async_database_url = database_url._replace(scheme='postgresql+asyncpg')

    return AppConfiguration(
        database_url=str(database_url.geturl()),
        async_database_url=str(async_database_url.geturl()),
    )

app_configuration = make_app_configuration()
