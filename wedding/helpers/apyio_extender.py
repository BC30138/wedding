import io
from typing import Any

from apyio import AsyncStringIOWrapper


class WriteAsyncStringIOWrapper(AsyncStringIOWrapper):
    async def write(self, s: Any) -> Any:
        return super().write(s)


def StringIO(*args: Any, **kwargs: Any) -> WriteAsyncStringIOWrapper:
    """StringIO constructor shim for the async wrapper."""
    raw = io.StringIO(*args, **kwargs)
    return WriteAsyncStringIOWrapper(raw)
