from django.contrib import admin
from .models import CustomerRequest


@admin.register(CustomerRequest)
class CustomerRequestAdmin(admin.ModelAdmin):
    list_display = ['search_query', 'search_type', 'store', 'user',
                    'results_count', 'created_at']
    list_filter = ['search_type', 'store', 'created_at']
    search_fields = ['search_query']
    readonly_fields = ['created_at']