from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role


class RoleInline(admin.TabularInline):
    model = Role
    extra = 1


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [RoleInline]
    list_display = ['username', 'email', 'assigned_store', 'is_active']
    list_filter = ['is_active', 'roles__role', 'assigned_store']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'store']
    list_filter = ['role', 'store']