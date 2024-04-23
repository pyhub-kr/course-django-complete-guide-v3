from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from .models import Post
from .serializers import PostSerializer


def post_list(request: HttpRequest) -> HttpResponse:
    post_qs = Post.objects.all()

    serializer = PostSerializer(instance=post_qs, many=True)
    list_data: ReturnList = serializer.data

    return JsonResponse(list_data, safe=False)


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)

    serializer = PostSerializer(instance=post)
    detail_data: ReturnDict = serializer.data

    return JsonResponse(detail_data)
