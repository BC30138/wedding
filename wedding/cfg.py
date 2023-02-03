import os
from dataclasses import dataclass
from dotenv import dotenv_values

DOTENV_PATH = ".env"

@dataclass
class AppConfiguration:
    database_url: str

def make_app_configuration():
    env_content = dotenv_values(DOTENV_PATH)
    return AppConfiguration(
        database_url=env_content["DATABASE_URL"],
    )

app_configuration = make_app_configuration()
