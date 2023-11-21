from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def root(request):
    return HttpResponse("hello vscode")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root),
]
