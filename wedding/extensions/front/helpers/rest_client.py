from fastapi import Request
from httpx import AsyncClient


async def get_rest_client(request: Request) -> AsyncClient:
    async with AsyncClient(app=request.app, base_url=str(request.base_url)) as client:
        yield client
