import os
from dataclasses import dataclass
from dotenv import dotenv_values

ENV_FILE_PATH_KEY = "CURRENT_ENV"


@dataclass
class AppConfiguration:
    database_url: str

def make_app_configuration():
    env_file_path = os.environ[ENV_FILE_PATH_KEY]
    env_content = dotenv_values(env_file_path)
    return AppConfiguration(
        database_url=env_content["DATABASE_URL"],
    )

app_configuration = make_app_configuration()
