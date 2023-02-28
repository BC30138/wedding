"""Точка запуска приложения."""
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Инициация конфигурации
from wedding.cfg import app_configuration  # noqa
from wedding.extensions.rest.helpers import internal_error_exception_handler
from wedding.private_router import setup_private_router
from wedding.public_router import setup_public_router

PUBLIC_PATH = "/public"
PRIVATE_PATH = "/private"


def setup_app() -> FastAPI:
    app = FastAPI(docs_url=f"{PRIVATE_PATH}/swagger", exception_handlers={Exception: internal_error_exception_handler})

    private_router = setup_private_router()
    app.include_router(router=private_router, prefix=PRIVATE_PATH)

    app.mount(  # workaround for https://github.com/tiangolo/fastapi/issues/1469
        f"{PUBLIC_PATH}/static",
        StaticFiles(directory="wedding/extensions/front/static"),
        name="static",
    )
    public_router = setup_public_router()
    app.include_router(
        router=public_router,
        prefix=PUBLIC_PATH,
    )

    return app


app = setup_app()


if __name__ == "__main__":
    uvicorn.run("wedding.app:app", host="127.0.0.1", port=8000, reload=True)
