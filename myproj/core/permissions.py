# core/permissions.py

from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAuthorOrReadonly(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    # 2차 필터
    def has_object_permission(
        self, request: Request, view: APIView, obj: Model
    ) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        # 삭제는 관리자만 가능
        # if request.method == "DELETE":
        #     return request.user.is_staff

        if not hasattr(obj, "author"):  # author 필드가 있다면, 레코드 조회 수행
            return False

        return obj.author == request.user
