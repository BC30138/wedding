from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

from wedding.extensions.front.router import router as front_router
from wedding.extensions.rest.forms.router import router as forms_router

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
    router.include_router(
        router=forms_router,
        prefix="/forms",
    )
    app.include_router(
        router=router,
        prefix=PUBLIC_PATH,
    )
    return router
