from django.contrib import admin
from .models import Post, Comment, Todo


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    pass
