from rest_framework import serializers
from .models import Category, NutrientType, Product


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon', 'parent', 'product_count']

    def get_product_count(self, obj):
        return obj.products.count()


class NutrientTypeSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(
        source='get_category_display', read_only=True
    )

    class Meta:
        model = NutrientType
        fields = ['id', 'name', 'category', 'category_display', 'description']


class ProductSerializer(serializers.ModelSerializer):
    category_names = serializers.SerializerMethodField()
    nutrient_names = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'description', 'price',
                  'categories', 'category_names', 'nutrients',
                  'nutrient_names', 'shelf_life_days', 'image',
                  'is_active', 'created_at']

    def get_category_names(self, obj):
        return list(obj.categories.values_list('name', flat=True))

    def get_nutrient_names(self, obj):
        return list(obj.nutrients.values_list('name', flat=True))


class ProductDetailSerializer(ProductSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    nutrients = NutrientTypeSerializer(many=True, read_only=True)

    class Meta(ProductSerializer.Meta):
        pass