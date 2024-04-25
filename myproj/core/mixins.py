from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict


class JSONResponseWrapperMixin:
    def finalize_response(
        self, request: Request, response: Response, *args, **kwargs
    ) -> Response:
        is_ok = 200 <= response.status_code < 400
        accepted_renderer = getattr(request, "accepted_renderer", None)

        if accepted_renderer is None or response.exception is True:
            response.data = {
                "ok": is_ok,
                "result": response.data,
            }
        elif isinstance(
            request.accepted_renderer, (JSONRenderer, BrowsableAPIRenderer)
        ):
            response.data = ReturnDict(
                {
                    "ok": is_ok,
                    "result": response.data,  # ReturnList
                },
                serializer=response.data.serializer,
            )

        return super().finalize_response(request, response, *args, **kwargs)
