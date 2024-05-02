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

from core.mixins import JSONResponseWrapperMixin, PermissionDebugMixin
from core.permissions import IsAuthorOrReadonly
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


class PostListAPIView(JSONResponseWrapperMixin, PermissionDebugMixin, ListAPIView):
    queryset = PostListSerializer.get_optimized_queryset()
    serializer_class = PostListSerializer


post_list = PostListAPIView.as_view()


# @api_view(["GET"])
# def post_detail(request: Request, pk: int) -> Response:
#     post = get_object_or_404(Post, pk=pk)
#
#     serializer = PostDetailSerializer(instance=post)
#     detail_data: ReturnDict = serializer.data
#
#     return Response(detail_data)


class PostRetrieveAPIView(
    JSONResponseWrapperMixin, PermissionDebugMixin, RetrieveAPIView
):
    queryset = PostDetailSerializer.get_optimized_queryset()
    serializer_class = PostDetailSerializer


post_detail = PostRetrieveAPIView.as_view()


class PostCreateAPIView(PermissionDebugMixin, CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


post_new = PostCreateAPIView.as_view()


class PostUpdateAPIView(PermissionDebugMixin, UpdateAPIView):
    queryset = PostSerializer.get_optimized_queryset()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadonly]

    # def perform_update(self, serializer):
    #     serializer.save()


post_edit = PostUpdateAPIView.as_view()


class PostDestroyAPIView(PermissionDebugMixin, DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrReadonly]


post_delete = PostDestroyAPIView.as_view()
