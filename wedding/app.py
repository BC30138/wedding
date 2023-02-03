"""Точка запуска приложения."""
from fastapi import FastAPI

# Инициация конфигурации
from wedding.cfg import app_configuration  # noqa

from wedding.extensions.rest.groups.router import router as groups_router
from wedding.extensions.rest.helpers import internal_error_exception_handler


def setup_app():
    app = FastAPI(
        docs_url="/swagger",
        exception_handlers={Exception: internal_error_exception_handler}
    )
    app.include_router(
        router=groups_router,
        prefix="/groups",
    )

    return app

app = setup_app()
