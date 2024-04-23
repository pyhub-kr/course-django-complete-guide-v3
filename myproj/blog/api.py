from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

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


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all().defer("content").select_related("author")
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


class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


post_detail = PostRetrieveAPIView.as_view()
