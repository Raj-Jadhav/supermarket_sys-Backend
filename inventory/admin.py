from django.contrib import admin
from .models import StockItem


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'aisle', 'quantity', 'expiry_date',
                    'expiry_status', 'stocked_date']
    list_filter = ['aisle__store', 'expiry_date']
    search_fields = ['product__name', 'batch_number']
    readonly_fields = ['expiry_status', 'days_until_expiry']
