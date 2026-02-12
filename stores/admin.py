from django.contrib import admin

from .models import Store, Aisle


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'manager', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'address']


@admin.register(Aisle)
class AisleAdmin(admin.ModelAdmin):
    list_display = ['store', 'number', 'name']
    list_filter = ['store']
    filter_horizontal = ['allowed_categories']
