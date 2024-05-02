from colorama import Fore
from django.conf import settings
from django.db.models import Model
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


class PermissionDebugMixin:
    if settings.DEBUG:

        def get_label_text(self, is_permit: bool) -> str:
            return (
                f"{Fore.GREEN}Permit{Fore.RESET}"  # colorama 라이브러리 활용
                if is_permit
                else f"{Fore.RED}Deny{Fore.RESET}"
            )

        def check_permissions(self, request: Request) -> None:
            print(f"{request.method} {request.path} has_permission")
            for permission in self.get_permissions():
                is_permit: bool = permission.has_permission(request, self)
                print(
                    f"\t{permission.__class__.__name__} = {self.get_label_text(is_permit)}"
                )
                if not is_permit:
                    self.permission_denied(
                        request,
                        message=getattr(permission, "message", None),
                        code=getattr(permission, "code", None),
                    )

        def check_object_permissions(self, request: Request, obj: Model) -> None:
            print(f"{request.method} {request.path} has_object_permission")
            for permission in self.get_permissions():
                is_permit: bool = permission.has_object_permission(request, self, obj)
                print(
                    f"\t{permission.__class__.__name__} = {self.get_label_text(is_permit)}"
                )
                if not is_permit:
                    self.permission_denied(
                        request,
                        message=getattr(permission, "message", None),
                        code=getattr(permission, "code", None),
                    )
