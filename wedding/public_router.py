from fastapi import APIRouter

from wedding.extensions.front.router import router as front_router


def setup_public_router() -> APIRouter:
    router = APIRouter()
    router.include_router(
        router=front_router,
        prefix="/invitation",
    )
    return router
