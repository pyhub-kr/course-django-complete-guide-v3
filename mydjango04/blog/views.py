from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Post


@login_required
@permission_required("blog.view_post", raise_exception=False)
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return HttpResponse(f"{post.pk}번 글의 {post.slug}")


@login_required
@permission_required("blog.view_premium_post", login_url="blog:premium_user_guide")
def post_premium_detail(request, slug):
    return HttpResponse(f"프리미엄 컨텐츠 페이지 : {slug}")


def premium_user_guide(request):
    return HttpResponse("프리미엄 유저 가이드 페이지")


def post_list(request):
    query = request.GET.get("query", "").strip()

    post_qs = Post.objects.all()

    if query:
        post_qs = post_qs.filter(
            Q(title__icontains=query) | Q(tag_set__name__in=[query])
        )

    post_qs = post_qs.select_related("author")
    post_qs = post_qs.prefetch_related("tag_set")

    return render(
        request,
        "blog/post_list.html",
        {
            "query": query,
            "post_list": post_qs,
        },
    )


def search(request):
    query = request.GET.get("query", "").strip()
    return render(
        request,
        "blog/search.html",
        {
            "query": query,
        },
    )
