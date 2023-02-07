import re
from functools import wraps

from fastapi import Request


MOBILE_TEMPLATE_DIRECTORY = "mobile"
WEB_TEMPLATE_DIRECTORY = "web"


class MobilityRequest(Request):
    @property
    def is_mobile(self):
        return self.is_mobile


def mobile_template_parser(request: MobilityRequest, template_name: str) -> str:
    if request.is_mobile:
        return f"{MOBILE_TEMPLATE_DIRECTORY}/{template_name}"
    else:
        return f"{WEB_TEMPLATE_DIRECTORY}/{template_name}"


class MobilityManager:
    MOBILE_USER_AGENTS = "android|fennec|iemobile|iphone|opera (?:mini|mobi)|mobile"
    MOBILE_COOKIE = "mobile"

    def __init__(self):
        self.USER_AGENTS = re.compile(self.MOBILE_USER_AGENTS)

    def is_mobile(self, func):
        @wraps(func)
        async def inner(request: Request, *args, **kwargs):
            is_mobile = self.process_request(request=request)
            setattr(request, "is_mobile", is_mobile)
            return await func(request, *args, **kwargs)
        return inner

    def process_request(self, request: Request) -> bool:
        ua = request.headers.get("User-Agent", "").lower()
        mc = request.cookies.get(self.MOBILE_COOKIE)
        return mc == "on" or (mc != "off" and self.USER_AGENTS.search(ua) is not None)


mobility_manager = MobilityManager()
