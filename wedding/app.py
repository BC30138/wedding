"""Точка запуска приложения."""
import uvicorn
from fastapi import FastAPI

# Инициация конфигурации
from wedding.cfg import app_configuration  # noqa
from wedding.extensions.rest.helpers import internal_error_exception_handler
from wedding.log import setup_logger
from wedding.private_router import PRIVATE_PATH, setup_private_router
from wedding.public_router import setup_public_router


def setup_app() -> FastAPI:
    app = FastAPI(docs_url=f"{PRIVATE_PATH}/swagger", exception_handlers={Exception: internal_error_exception_handler})

    setup_logger()

    setup_private_router(app=app)
    setup_public_router(app=app)

    return app


app = setup_app()


if __name__ == "__main__":
    uvicorn.run("wedding.app:app", host="127.0.0.1", port=8000, reload=True)
