from django.shortcuts import render


def index(request):
    return render(request, "studio/index.html")


