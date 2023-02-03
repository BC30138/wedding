from enum import Enum
from http import HTTPStatus
from typing import Type, Any

from fastapi.responses import JSONResponse
from fastapi import Request
from pydantic import BaseModel

from wedding.ctx.general_errors import DomainError

INTERNAL_ERROR_CODE = "INTERNAL_ERROR"

class ResponseStatus(Enum):
    success = "success"
    error = "error"


class BaseResponseSchema(BaseModel):
    status: str
    data: Any


class ResponseGenerator:
    @staticmethod
    def success_schema(schema: Type[BaseModel]) -> Type[BaseResponseSchema]:
        class Schema(BaseResponseSchema):
            data: schema

        return Schema

    @classmethod
    def success(cls, data: Any = None) -> BaseResponseSchema:
        return BaseResponseSchema(
            status=ResponseStatus.success.value,
            data=data,
        )

    @classmethod
    def domain_error(
        cls,
        exc: DomainError,
        status_code: int,
    ) -> JSONResponse:
        return JSONResponse(
            content={
                "status": ResponseStatus.error.value,
                "special_code": exc.special_code,
                "error_msg": exc.msg,
                "entity": exc.entity,
            },
            status_code=status_code
        )


async def internal_error_exception_handler(
    _request: Request,
    exc: Exception,
):
    return JSONResponse(
        content={
            "status": ResponseStatus.error.value,
            "special_code": getattr(exc, "special_code", INTERNAL_ERROR_CODE),
            "error_msg": str(exc),
        },
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    )