import io

from apyio import AsyncStringIOWrapper


class WriteAsyncStringIOWrapper(AsyncStringIOWrapper):
    async def write(self, s):
        return super().write(s)


def StringIO(*args, **kwargs):
    """StringIO constructor shim for the async wrapper."""
    raw = io.StringIO(*args, **kwargs)
    return WriteAsyncStringIOWrapper(raw)
