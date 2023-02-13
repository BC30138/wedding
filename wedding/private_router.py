from fastapi import APIRouter

from wedding.extensions.rest.groups.router import router as groups_router
from wedding.extensions.rest.guests.router import router as guests_router


def setup_private_router() -> APIRouter:
    router = APIRouter()
    router.include_router(
        router=groups_router,
        prefix="/groups",
    )
    router.include_router(
        router=guests_router,
        prefix="/guests",
    )
    return router
