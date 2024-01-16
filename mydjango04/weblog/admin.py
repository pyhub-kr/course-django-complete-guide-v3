from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline

from .models import Post, Comment


class CommentTabularInline(GenericTabularInline):
    model = Comment
    fields = ["message", "rating"]
    extra = 0

    # def has_change_permission(self, request, obj=None):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False

    # def has_add_permission(self, request, obj):
    #     return False


class CommentStackedInline(GenericStackedInline):
    model = Comment
    fields = ["message", "rating"]
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentTabularInline]
    # inlines = [CommentStackedInline]
