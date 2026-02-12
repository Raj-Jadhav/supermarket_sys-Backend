from rest_framework import serializers
from .models import StockItem


class AddStockSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    aisle_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    expiry_date = serializers.DateField(required=False, allow_null=True)
    batch_number = serializers.CharField(required=False, default='')


class StockItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    aisle_number = serializers.IntegerField(source='aisle.number', read_only=True)
    aisle_name = serializers.CharField(source='aisle.name', read_only=True)
    store_name = serializers.CharField(source='aisle.store.name', read_only=True)
    expiry_status = serializers.CharField(read_only=True)
    days_until_expiry = serializers.IntegerField(read_only=True)

    class Meta:
        model = StockItem
        fields = [
            'id', 'product', 'product_name', 'product_sku',
            'aisle', 'aisle_number', 'aisle_name', 'store_name',
            'quantity', 'expiry_date', 'expiry_status',
            'days_until_expiry', 'batch_number', 'stocked_date',
        ]


class UpdateStockSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0)