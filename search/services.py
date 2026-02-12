from datetime import date
from django.db.models import Q

from products.models import Product
from stores.models import Store
from inventory.models import StockItem
from analytics.models import CustomerRequest


class ProductSearchService:
    @staticmethod
    def search_products(store_id: int, query: str, search_type: str = 'all',
                        user=None):
        """
        Search products by name, nutrient, or category.
        Returns products with their aisle locations in the given store.
        """
        store = Store.objects.get(id=store_id)

        # Build queryset based on search_type
        if search_type == 'product':
            products = Product.objects.filter(
                Q(name__icontains=query) | Q(sku__icontains=query),
                is_active=True
            )
        elif search_type == 'nutrient':
            products = Product.objects.filter(
                nutrients__name__icontains=query,
                is_active=True
            ).distinct()
        elif search_type == 'category':
            products = Product.objects.filter(
                categories__name__icontains=query,
                is_active=True
            ).distinct()
        else:  # 'all'
            products = Product.objects.filter(
                Q(name__icontains=query) |
                Q(nutrients__name__icontains=query) |
                Q(categories__name__icontains=query),
                is_active=True
            ).distinct()

        # Get stock locations in the specific store
        results = []
        for product in products.prefetch_related('categories', 'nutrients'):
            stock_items = StockItem.objects.filter(
                product=product,
                aisle__store=store,
                quantity__gt=0,
                expiry_date__gte=date.today()
            ).select_related('aisle')

            locations = [
                {
                    'aisle_number': item.aisle.number,
                    'aisle_name': item.aisle.name,
                    'quantity': item.quantity,
                    'message': f"Go to Aisle {item.aisle.number} ({item.aisle.name})"
                }
                for item in stock_items
            ]

            if locations:
                results.append({
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': str(product.price),
                        'categories': list(
                            product.categories.values_list('name', flat=True)
                        ),
                        'nutrients': list(
                            product.nutrients.values_list('name', flat=True)
                        ),
                    },
                    'locations': locations,
                    'total_quantity': sum(l['quantity'] for l in locations),
                })

        # Log the search request for analytics
        CustomerRequest.objects.create(
            user=user if user and user.is_authenticated else None,
            store=store,
            search_type=search_type if search_type != 'all' else 'product',
            search_query=query,
            results_count=len(results),
        )

        return results