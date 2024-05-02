from django.db.models import Model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from core.mixins import (
    JSONResponseWrapperMixin,
    PermissionDebugMixin,
    TestFuncPermissionMixin,
)
from core.permissions import (
    IsAuthorOrReadonly,
    make_drf_permission_class,
    PermitSafeMethods,
)
from .models import Post
from .serializers import PostSerializer, PostListSerializer, PostDetailSerializer


# @api_view(["GET"])
# def post_list(request: Request) -> Response:
#     post_qs = Post.objects.all().defer("content").select_related("author")
#
#     serializer = PostListSerializer(instance=post_qs, many=True)
#     list_data: ReturnList = serializer.data
#
#     return Response(list_data)


# class PostListAPIView(JSONResponseWrapperMixin, PermissionDebugMixin, ListAPIView):
#     queryset = PostListSerializer.get_optimized_queryset()
#     serializer_class = PostListSerializer
#
#
# post_list = PostListAPIView.as_view()
#
#
# # @api_view(["GET"])
# # def post_detail(request: Request, pk: int) -> Response:
# #     post = get_object_or_404(Post, pk=pk)
# #
# #     serializer = PostDetailSerializer(instance=post)
# #     detail_data: ReturnDict = serializer.data
# #
# #     return Response(detail_data)
#
#
# class PostRetrieveAPIView(
#     JSONResponseWrapperMixin, PermissionDebugMixin, RetrieveAPIView
# ):
#     queryset = PostDetailSerializer.get_optimized_queryset()
#     serializer_class = PostDetailSerializer
#
#
# post_detail = PostRetrieveAPIView.as_view()
#
#
# class PostCreateAPIView(PermissionDebugMixin, CreateAPIView):
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
#
#
# post_new = PostCreateAPIView.as_view()
#
#
# class PostUpdateAPIView(PermissionDebugMixin, TestFuncPermissionMixin, UpdateAPIView):
#     TEST_FUNC_PERMISSION_CLASS_NAME = "PostUpdateAPIView"
#
#     queryset = PostSerializer.get_optimized_queryset()
#     serializer_class = PostSerializer
#
#     # permission_classes = [IsAuthorOrReadonly]
#     # permission_classes = [
#     #     make_drf_permission_class(
#     #         class_name="PostUpdateAPIView",
#     #         permit_safe_methods=True,
#     #         has_permission_test_func=lambda request, view: request.user.is_authenticated,
#     #         has_object_permission_test_func=(
#     #             lambda request, view, obj: obj.author == request.user
#     #         ),
#     #     ),
#     # ]
#     permission_classes = [PermitSafeMethods]
#
#     def has_permission(self, request: Request, view: APIView) -> bool:
#         return request.user.is_authenticated
#
#     def has_object_permission(self, request: Request, view: APIView, obj: Post) -> bool:
#         return obj.author == request.user
#
#     # def perform_update(self, serializer):
#     #     serializer.save()
#
#
# post_edit = PostUpdateAPIView.as_view()
#
#
# class PostDestroyAPIView(PermissionDebugMixin, DestroyAPIView):
#     queryset = Post.objects.all()
#     permission_classes = [IsAuthorOrReadonly]
#
#
# post_delete = PostDestroyAPIView.as_view()


class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadonly]

    def get_queryset(self):
        if self.action == "list":
            self.queryset = PostListSerializer.get_optimized_queryset()
        elif self.action == "retrieve":
            self.queryset = PostDetailSerializer.get_optimized_queryset()
        elif self.action in ("update", "partial_update"):
            self.queryset = PostSerializer.get_optimized_queryset()
        elif self.action == "destroy":
            self.queryset = Post.objects.all()

        return super().get_queryset()

    def get_serializer_class(self):
        # self.request.method == "GET"  # "list" or "retrieve"
        if self.action == "list":
            return PostListSerializer
        elif self.action == "retrieve":
            return PostDetailSerializer
        elif self.action in ("create", "update", "partial_update"):
            return PostSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# post_list = PostModelViewSet.as_view(
#     actions={
#         "get": "list",
#         "post": "create",
#     },
# )
#
# post_detail = PostModelViewSet.as_view(
#     actions={
#         "get": "retrieve",
#         "put": "update",
#         "patch": "partial_update",
#         "delete": "destroy",
#     },
# )
