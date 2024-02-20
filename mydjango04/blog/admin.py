from django.contrib import admin
from .models import Post, Comment, Tag, Memo, MemoGroup


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


class MemoTabularInline(admin.TabularInline):
    model = Memo
    fields = ["message", "status"]


@admin.register(MemoGroup)
class MemoGroupAdmin(admin.ModelAdmin):
    inlines = [MemoTabularInline]
