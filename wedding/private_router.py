from fastapi import APIRouter, FastAPI

from wedding.extensions.rest.groups.router import router as groups_router
from wedding.extensions.rest.guests.router import router as guests_router
from wedding.extensions.rest.invitations.router import router as invitations_router

PRIVATE_PATH = "/private"


def setup_private_router(app: FastAPI) -> None:
    router = APIRouter()
    router.include_router(
        router=groups_router,
        prefix="/groups",
    )
    router.include_router(
        router=guests_router,
        prefix="/guests",
    )
    router.include_router(
        router=invitations_router,
        prefix="/invitations",
    )
    app.include_router(router=router, prefix=PRIVATE_PATH)
