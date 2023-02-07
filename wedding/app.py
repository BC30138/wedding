"""Точка запуска приложения."""
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Инициация конфигурации
from wedding.cfg import app_configuration  # noqa

from wedding.extensions.rest.groups.router import router as groups_router
from wedding.extensions.rest.guests.router import router as guests_router
from wedding.extensions.front.router import router as front_router
from wedding.extensions.rest.helpers import internal_error_exception_handler


def setup_app():
    app = FastAPI(
        docs_url="/swagger",
        exception_handlers={Exception: internal_error_exception_handler}
    )
    app.mount("/static", StaticFiles(directory="wedding/extensions/front/static"), name="static")

    app.include_router(
        router=groups_router,
        prefix="/groups",
    )
    app.include_router(
        router=guests_router,
        prefix="/guests",
    )
    app.include_router(
        router=front_router,
    )

    return app

app = setup_app()

if __name__ == "__main__":
    uvicorn.run("wedding.app:app", host="0.0.0.0", port=8000)
