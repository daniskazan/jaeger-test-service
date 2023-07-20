from json import JSONDecodeError

from opentelemetry import trace

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import Message


class LoggingMiddleware(BaseHTTPMiddleware):
    @staticmethod
    async def __set_body(request: Request):
        receive_ = await request._receive()  # noqa

        async def receive() -> Message:
            return receive_

        request._receive = receive

    async def get_body(self, request):
        await self.__set_body(request)
        try:
            body = await request.json()
        except (JSONDecodeError, UnicodeDecodeError):
            body = {}
        return body

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        body = await self.get_body(request=request)
        span = trace.get_current_span()
        span.add_event("request.body", attributes=body)

        response = await call_next(request)

        return response
