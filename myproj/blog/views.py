from django.shortcuts import render

from core.decorators import login_required_hx


def index(request):
    return render(request, "blog/index.html")


@login_required_hx
def friend_list(request):
    return render(request, "blog/friend_list.html")


def new_friend_list(request):
    return render(request, "blog/new_friend_list.html")
