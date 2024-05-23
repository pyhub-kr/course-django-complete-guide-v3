# accounts/api.py

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer


@api_view(["GET"])
@permission_classes([])
@renderer_classes([JSONRenderer])
def status(request: Request) -> Response:
    messages = [
        {
            "message": message.message,
            "tags": message.tags,
        }
        for message in request._messages
    ]

    return Response(
        {
            "is_authenticated": request.user.is_authenticated,
            "username": request.user.username or "anonymous",
            "messages": messages,
        }
    )
