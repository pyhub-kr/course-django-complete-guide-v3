from django.contrib import admin
from .models import Note, Photo


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
