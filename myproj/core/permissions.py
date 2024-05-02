# core/permissions.py
from typing import Callable, Type, cast

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


def make_drf_permission_class(
    class_name: str = "PermissionClass",
    permit_safe_methods: bool = False,
    has_permission_test_func: Callable[[Request, APIView], bool] = None,
    has_permission_test_func_name: str = None,
    has_object_permission_test_func: Callable[[Request, APIView, Model], bool] = None,
    has_object_permission_test_func_name: str = None,
) -> Type[permissions.BasePermission]:

    def has_permission(self, request: Request, view: APIView) -> bool:
        if permit_safe_methods and request.method in permissions.SAFE_METHODS:
            return True
        if has_permission_test_func is not None:
            return has_permission_test_func(request, view)
        if has_permission_test_func_name is not None:
            test_func = getattr(view, has_permission_test_func_name)
            return test_func(request, view)
        return True

    def has_object_permission(
        self, request: Request, view: APIView, obj: Model
    ) -> bool:
        if permit_safe_methods and request.method in permissions.SAFE_METHODS:
            return True
        if has_object_permission_test_func is not None:
            return has_object_permission_test_func(request, view, obj)
        if has_object_permission_test_func_name is not None:
            test_func = getattr(view, has_object_permission_test_func_name)
            return test_func(request, view, obj)
        return True

    permission_class = type(
        class_name,
        (permissions.BasePermission,),
        {
            "has_permission": has_permission,
            "has_object_permission": has_object_permission,
        },
    )

    return cast(Type[permissions.BasePermission], permission_class)
