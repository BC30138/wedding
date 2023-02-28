from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

from wedding.extensions.front.router import router as front_router

PUBLIC_PATH = "/public"


def setup_public_router(app: FastAPI) -> APIRouter:
    app.mount(  # workaround for https://github.com/tiangolo/fastapi/issues/1469
        f"{PUBLIC_PATH}/static",
        StaticFiles(directory="wedding/extensions/front/static"),
        name="static",
    )
    router = APIRouter()
    router.include_router(
        router=front_router,
        prefix="/invitation",
    )
    app.include_router(
        router=router,
        prefix=PUBLIC_PATH,
    )
    return router
