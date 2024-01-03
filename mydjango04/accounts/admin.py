from django.contrib import admin
from .models import User, SuperUser


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(SuperUser)
class SuperUserAdmin(admin.ModelAdmin):
    pass
