from django.shortcuts import render


def index(request):
    return render(request, "blog/index.html")


def friend_list(request):
    return render(request, "blog/friend_list.html")


def new_friend_list(request):
    return render(request, "blog/new_friend_list.html")
