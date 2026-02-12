from django.contrib import admin
from .models import Category, NutrientType, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'description']
    search_fields = ['name']


@admin.register(NutrientType)
class NutrientTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'price', 'shelf_life_days', 'is_active']
    list_filter = ['is_active', 'categories', 'nutrients']
    search_fields = ['name', 'sku']
    filter_horizontal = ['categories', 'nutrients']
