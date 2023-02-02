"""Точка запуска приложения."""
from fastapi import FastAPI

# Инициация конфигурации
from wedding.cfg import app_configuration  # noqa

from wedding.extensions.rest.users.router import router as users_router

def setup_app():
    app = FastAPI(
        docs_url="/swagger",
    )
    app.include_router(
        router=users_router,
        prefix="/users",
    )

    return app

app = setup_app()
