from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Post


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return HttpResponse(f"{post.pk}번 글의 {post.slug}")
