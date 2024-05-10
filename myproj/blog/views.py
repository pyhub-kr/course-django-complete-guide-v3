from django.http import HttpResponse
from django.shortcuts import render
from django_nextjs.render import render_nextjs_page


def whoami(request):
    status = 200 if request.user.is_authenticated else 401
    username = request.user.username or "anonymous"
    return HttpResponse(f"Your username is <strong>{username}</strong>.", status=status)


async def index(request):
    # return render(request, "blog/index.html")
    return await render_nextjs_page(request)
