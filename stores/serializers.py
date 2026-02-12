from rest_framework import serializers
from .models import Store, Aisle


class StoreSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(
        source='manager.get_full_name', read_only=True, default=None
    )
    aisle_count = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['id', 'name', 'address', 'phone', 'manager',
                  'manager_name', 'aisle_count', 'is_active',
                  'created_at', 'updated_at']

    def get_aisle_count(self, obj):
        return obj.aisles.count()


class AisleSerializer(serializers.ModelSerializer):
    allowed_category_names = serializers.SerializerMethodField()
    stock_count = serializers.SerializerMethodField()

    class Meta:
        model = Aisle
        fields = ['id', 'store', 'number', 'name', 'allowed_categories',
                  'allowed_category_names', 'stock_count']

    def get_allowed_category_names(self, obj):
        return list(obj.allowed_categories.values_list('name', flat=True))

    def get_stock_count(self, obj):
        return obj.stock_items.filter(quantity__gt=0).count()


class AisleDetailSerializer(AisleSerializer):
    stock_items = serializers.SerializerMethodField()

    class Meta(AisleSerializer.Meta):
        fields = AisleSerializer.Meta.fields + ['stock_items']

    def get_stock_items(self, obj):
        from inventory.serializers import StockItemSerializer
        items = obj.stock_items.filter(quantity__gt=0).select_related('product')
        return StockItemSerializer(items, many=True).data